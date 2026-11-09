# Teste do Mercado Livre (09/11): o bot de perfume vai usar a VITRINE da Central de Afiliados, que já traz
# nome, preço de/por, desconto, nota, vendidos e comissão, e o "Compartilhar", que gera o link meli.la.
# Os dois só funcionam com a sessão logada do Gabriel: os cookies ficam em ml_cookies.txt, na MESMA pasta do
# config.txt (fora do bot). Este teste NUNCA mostra cookie nem código de segurança.
#
# Uso:  python testar_ml.py                      busca "perfume masculino" e mostra 5 produtos
#       python testar_ml.py "perfume feminino"   outra busca
#       python testar_ml.py "perfume" --link     também gera o link de afiliado do 1º produto
import http.cookiejar
import json
import os
import re
import sys
import urllib.request

CONFIG_PATH = os.environ.get("BOT_CONFIG", r"C:\bot-config\config.txt")
COOKIES_ML = os.path.join(os.path.dirname(CONFIG_PATH), "ml_cookies.txt")
BASE = "https://www.mercadolivre.com.br"
HUB = BASE + "/afiliados/hub?is_affiliate=true"
NAVEGADOR = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/130.0.0.0 Safari/537.36")


class SessaoML:
    def __init__(self, arquivo=COOKIES_ML):
        if not os.path.exists(arquivo):
            raise SystemExit(f"Não achei {arquivo}. Exporte os cookies do Mercado Livre (formato cookies.txt) para lá.")
        self.jar = http.cookiejar.MozillaCookieJar(arquivo)
        self.jar.load(ignore_discard=True, ignore_expires=True)
        self.abrir = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar)).open
        self.csrf, self.tag = self._entrar()

    def _pedir(self, url, corpo=None, extras=None):
        cab = {"User-Agent": NAVEGADOR, "Accept-Language": "pt-BR,pt;q=0.9"}
        if corpo is not None:
            cab.update({"Accept": "application/json, text/plain, */*", "Content-Type": "application/json",
                        "x-custom-origin": BASE, "x-csrf-token": self.csrf, "x-csrf": self.csrf,
                        "Origin": BASE, "Referer": HUB})
        cab.update(extras or {})
        dados = json.dumps(corpo).encode() if corpo is not None else None
        with self.abrir(urllib.request.Request(url, data=dados, headers=cab), timeout=30) as r:
            return r.geturl(), r.read().decode("utf-8", "replace")

    def _entrar(self):
        url, html = self._pedir(HUB)
        if "account-verification" in url or "/login" in url or 'name="csrf-token"' not in html:
            raise SystemExit("O Mercado Livre não aceitou a sessão (pediu login). Exporte os cookies de novo.")
        csrf = re.search(r'<meta[^>]+name="csrf-token"[^>]+content="([^"]+)"', html)
        tag = re.search(r'"tags":\[\{"tag":"([^"]+)"', html)
        if not csrf or not tag:
            raise SystemExit("Entrei na Central de Afiliados, mas não achei o código de segurança ou a etiqueta.")
        return csrf.group(1), tag.group(1)

    def buscar(self, termo, offset=0):
        # A vitrine: {"search": "...", "sort": "relevance", "filters": [], "offset": 0}
        _, texto = self._pedir(BASE + "/affiliate-program/api/hub/search?is_affiliate=true&device=desktop",
                               {"search": termo, "sort": "relevance", "filters": [], "offset": offset})
        return [ler_card(c) for c in json.loads(texto)["polycard_client_model"]["polycards"]]

    def gerar_link(self, p):
        # O "Compartilhar": devolve o link curto meli.la com a etiqueta de afiliado
        corpo = {"itemId": p["produto"] or p["id"], "type": "product", "extraCommission": p["comissao_extra"],
                 "itemAddToList": p["id"], "tag": self.tag, "urls": [p["url"]]}
        _, texto = self._pedir(BASE + "/affiliate-program/api/v2/affiliates/createLink", corpo)
        resp = json.loads(texto)
        return resp["urls"][0]["short_url"] if resp.get("total_success") else None


def ler_card(card):
    meta, comp = card.get("metadata", {}), {c["type"]: c for c in card.get("components", [])}
    preco = comp.get("price", {}).get("price", {})
    nota = re.search(r"Classificação ([\d.]+)", str(comp.get("review_compacted", {})))
    vendidos = re.search(r"\+([\d]+)(mil)?\s*vendidos", str(comp.get("review_compacted", {})))
    ganhos = re.search(r"(\d+)%", str(card.get("components")).split("GANHOS", 1)[-1]) if "GANHOS" in str(card) else None
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
        "foto": f"https://http2.mlstatic.com/D_NQ_NP_{fotos[0].get('id')}-O.webp" if fotos[0].get("id") else "",
    }


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    termo = args[0] if args else "perfume masculino"
    ml = SessaoML()
    print("Sessão do Mercado Livre OK (Central de Afiliados abriu).")
    produtos = ml.buscar(termo)
    print(f"Busca '{termo}': {len(produtos)} produtos. Os 5 primeiros:")
    for p in produtos[:5]:
        de = f"de R$ {p['preco_antes']} " if p["preco_antes"] else ""
        print(f"  - {p['nome'][:70]} | {de}por R$ {p['preco']} {p['desconto']} | nota {p['nota']} | "
              f"{p['vendidos']}+ vendidos | comissão {p['comissao']}%")
    if "--link" in sys.argv and produtos:
        print("Link de afiliado do 1º:", ml.gerar_link(produtos[0]) or "a geração falhou")
