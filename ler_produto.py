import html
import json
import re
import sys

import requests

CABECALHOS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
}


def meta(pagina, propriedade):
    padrao = (
        r'<meta[^>]+(?:property|name)=["\']' + re.escape(propriedade) +
        r'["\'][^>]+content=["\']([^"\']*)["\']'
    )
    achou = re.search(padrao, pagina, re.IGNORECASE)
    return html.unescape(achou.group(1)) if achou else None


def preco_do_json_ld(pagina):
    for bloco in re.findall(
        r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>',
        pagina, re.DOTALL | re.IGNORECASE,
    ):
        try:
            dados = json.loads(bloco)
        except json.JSONDecodeError:
            continue
        itens = dados if isinstance(dados, list) else [dados]
        for item in itens:
            ofertas = item.get("offers") if isinstance(item, dict) else None
            if isinstance(ofertas, list) and ofertas:
                ofertas = ofertas[0]
            if isinstance(ofertas, dict) and ofertas.get("price"):
                return str(ofertas["price"])
    return None


def candidatos_preco(pagina):
    """Procura possíveis preços na página, por vários padrões."""
    padroes = {
        "json price": r'"price"\s*:\s*"?([0-9]+(?:\.[0-9]+)?)"?',
        "json amount": r'"amount"\s*:\s*"?([0-9]+(?:\.[0-9]+)?)"?',
        "json original_price": r'"original_price"\s*:\s*"?([0-9]+(?:\.[0-9]+)?)"?',
        "fracao": r'andes-money-amount__fraction[^>]*>([0-9\.]+)<',
        "texto R$": r'R\$\s*([0-9\.]+,[0-9]{2})',
    }
    achados = {}
    for nome, padrao in padroes.items():
        achados[nome] = re.findall(padrao, pagina)[:6]
    return achados


def ler_produto(link):
    resposta = requests.get(link, headers=CABECALHOS, timeout=30,
                            allow_redirects=True)
    pagina = resposta.text
    open("pagina.html", "w", encoding="utf-8").write(pagina)
    foto = meta(pagina, "og:image")
    return {
        "status": resposta.status_code,
        "url_final": resposta.url[:90] + "...",
        "nome": meta(pagina, "og:title"),
        "foto": foto,
        "foto_jpg": foto.replace(".webp", ".jpg") if foto else None,
        "preco": preco_do_json_ld(pagina) or meta(pagina, "product:price:amount"),
        "candidatos_de_preco": candidatos_preco(pagina),
    }


if __name__ == "__main__":
    link = sys.argv[1] if len(sys.argv) > 1 else input("Cole o link: ").strip()
    produto = ler_produto(link)
    for chave, valor in produto.items():
        print(f"{chave}: {valor}")
