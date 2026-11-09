# Mercado Livre (09/11): a VITRINE da Central de Afiliados e o "Compartilhar" (link meli.la).
# Não há API oficial de afiliado no Mercado Livre e a busca pública pede login, então o bot usa a sessão
# do Gabriel: os cookies ficam em ml_cookies.txt, na MESMA pasta do config.txt (fora do bot, nunca no Git).
# Nada aqui mostra cookie nem código de segurança. A cada uso a sessão é renovada e os cookies novos são
# gravados de volta no arquivo (assim ela não vence).
import http.cookiejar
import json
import os
import re
import urllib.error
import urllib.request

CONFIG_PATH = os.environ.get("BOT_CONFIG", r"C:\bot-config\config.txt")
COOKIES_ML = os.path.join(os.path.dirname(CONFIG_PATH), "ml_cookies.txt")
BASE = "https://www.mercadolivre.com.br"
HUB = BASE + "/afiliados/hub?is_affiliate=true"
NAVEGADOR = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/130.0.0.0 Safari/537.36")


class SessaoCaiu(Exception):
    """O Mercado Livre pediu login: os cookies precisam ser exportados de novo."""


class SessaoML:
    def __init__(self, arquivo=COOKIES_ML):
        self.arquivo = arquivo
        if not os.path.exists(arquivo):
            raise SessaoCaiu(f"não achei {arquivo}")
        self.jar = http.cookiejar.MozillaCookieJar(arquivo)
        self.jar.load(ignore_discard=True, ignore_expires=True)
        self.abrir = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar)).open
        self.csrf = self.tag = None
        self.entrar()

    def _pedir(self, url, corpo=None):
        cab = {"User-Agent": NAVEGADOR, "Accept-Language": "pt-BR,pt;q=0.9"}
        if corpo is not None:
            cab.update({"Accept": "application/json, text/plain, */*", "Content-Type": "application/json",
                        "x-custom-origin": BASE, "x-csrf-token": self.csrf, "x-csrf": self.csrf,
                        "Origin": BASE, "Referer": HUB})
        dados = json.dumps(corpo).encode() if corpo is not None else None
        try:
            with self.abrir(urllib.request.Request(url, data=dados, headers=cab), timeout=30) as r:
                final, texto = r.geturl(), r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise SessaoCaiu(f"HTTP {e.code}")
            raise
        if "account-verification" in final or "/login" in final:
            raise SessaoCaiu("pediu login")
        self._guardar()
        return texto

    def _guardar(self):
        # Cookies renovados de volta no arquivo (a sessão continua viva); falhar aqui não para o bot
        try:
            self.jar.save(ignore_discard=True, ignore_expires=True)
        except OSError:
            pass

    def entrar(self):
        html = self._pedir(HUB)
        csrf = re.search(r'<meta[^>]+name="csrf-token"[^>]+content="([^"]+)"', html)
        tag = re.search(r'"tags":\[\{"tag":"([^"]+)"', html)
        if not csrf or not tag:
            raise SessaoCaiu("a Central de Afiliados abriu sem o código de segurança")
        self.csrf, self.tag = csrf.group(1), tag.group(1)

    def _api(self, caminho, corpo):
        try:
            return json.loads(self._pedir(BASE + caminho, corpo))
        except (SessaoCaiu, ValueError):
            self.entrar()                       # código de segurança venceu: pega outro e tenta 1 vez
            return json.loads(self._pedir(BASE + caminho, corpo))

    def buscar(self, termo, offset=0):
        resp = self._api("/affiliate-program/api/hub/search?is_affiliate=true&device=desktop",
                         {"search": termo, "sort": "relevance", "filters": [], "offset": offset})
        return [ler_card(c) for c in resp["polycard_client_model"]["polycards"]]

    def gerar_link(self, card):
        corpo = {"itemId": card["produto"] or card["id"], "type": "product",
                 "extraCommission": card["comissao_extra"], "itemAddToList": card["id"], "tag": self.tag,
                 "urls": [card["url"]]}
        resp = self._api("/affiliate-program/api/v2/affiliates/createLink", corpo)
        return resp["urls"][0]["short_url"] if resp.get("total_success") else None


def ler_card(card):
    meta, comp = card.get("metadata", {}), {c["type"]: c for c in card.get("components", [])}
    preco = comp.get("price", {}).get("price", {})
    review = str(comp.get("review_compacted", {}))
    nota = re.search(r"Classificação ([\d.]+)", review)
    vendidos = re.search(r"\+(\d+)(mil)?\s*vendidos", review)
    ganhos = re.search(r"GANHOS\D{0,40}?(\d+)%", json.dumps(card.get("components"), ensure_ascii=False))
    fotos = card.get("pictures", {}).get("pictures") or [{}]
    return {
        "id": meta.get("id"), "produto": meta.get("product_id"), "url": meta.get("url"),
        "comissao_extra": meta.get("extra_commission", "false"),
        "nome": comp.get("title", {}).get("title", {}).get("text", ""),
        "preco": (preco.get("current_price") or {}).get("value"),
        "preco_antes": (preco.get("previous_price") or {}).get("value"),
        "desconto": (preco.get("discount_label") or {}).get("text", ""),
        "nota": float(nota.group(1)) if nota else None,
        "vendidos": int(vendidos.group(1)) * (1000 if vendidos.group(2) else 1) if vendidos else 0,
        "comissao": int(ganhos.group(1)) if ganhos else None,
        "foto": f"https://http2.mlstatic.com/D_NQ_NP_{fotos[0].get('id')}-O.jpg" if fotos[0].get("id") else "",
    }


def para_oferta(c):
    # No formato que o motor do bot (postar_shopee.py) já entende, para reaproveitar todos os filtros
    preco, antes = float(c["preco"] or 0), float(c["preco_antes"] or 0)
    if antes > preco > 0:
        desconto = round((1 - preco / antes) * 100)
    else:
        m = re.search(r"(\d+)%", c["desconto"] or "")
        desconto = int(m.group(1)) if m else 0
    return {
        "itemId": c["id"], "productName": c["nome"], "price": preco, "priceDiscountRate": desconto,
        "precoAntes": antes if antes > preco else 0,
        "sales": c["vendidos"], "ratingStar": c["nota"] or 0, "commissionRate": (c["comissao"] or 0) / 100,
        "imageUrl": c["foto"], "offerLink": "", "shopType": [], "loja": "mercadolivre",
        "pixOnly": "Pix" in (c["desconto"] or ""),
        # ganhos extras da marca: ganha o bônus de comissão extra do motor
        "sellerCommissionRate": 0.01 if str(c["comissao_extra"]).lower() == "true" else 0,
        "_ml": c,
    }
