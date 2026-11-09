import csv
import time

import requests

from ler_produto import ler_produto
from postar_oferta import baixar_imagem, html, ler_config

ARQUIVO = "ofertas.csv"
PAUSA_ENTRE_POSTS = 20  # segundos


def ler_planilha():
    for codificacao in ("utf-8-sig", "cp1252"):
        try:
            with open(ARQUIVO, encoding=codificacao, newline="") as f:
                return list(csv.DictReader(f, delimiter=";"))
        except UnicodeDecodeError:
            continue
    raise SystemExit("Não consegui ler o ofertas.csv (codificação).")


def salvar_planilha(linhas):
    campos = ["link", "preco_de", "preco_por", "cupom", "titulo", "postado"]
    with open(ARQUIVO, "w", encoding="utf-8-sig", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=campos, delimiter=";")
        escritor.writeheader()
        escritor.writerows(linhas)


def para_numero(texto):
    return float(texto.replace(".", "").replace(",", "."))


def encurtar(titulo, limite=70):
    if len(titulo) <= limite:
        return titulo
    return titulo[:limite].rsplit(" ", 1)[0]


def montar_legenda(titulo, preco_de, preco_por, cupom, link):
    linhas = [f"🔥 <b>{html.escape(titulo)}</b>", ""]
    if preco_de:
        desconto = int((1 - para_numero(preco_por) / para_numero(preco_de)) * 100)
        linhas.append(f"De <s>R$ {preco_de}</s>")
        linhas.append(f"💸 Por <b>R$ {preco_por}</b> ({desconto}% OFF)")
    else:
        linhas.append(f"💸 Por <b>R$ {preco_por}</b>")
    if cupom:
        linhas.append(f"🎟 Cupom: <code>{html.escape(cupom)}</code>")
    linhas += ["", f"👉 <a href=\"{link}\">Pegar promoção</a>"]
    return "\n".join(linhas)


def enviar(config, foto_url, legenda):
    imagem = baixar_imagem(foto_url)
    resposta = requests.post(
        f"https://api.telegram.org/bot{config['TOKEN']}/sendPhoto",
        data={"chat_id": config["CANAL"], "caption": legenda, "parse_mode": "HTML"},
        files={"photo": ("foto.jpg", imagem)},
        timeout=60,
    )
    dados = resposta.json()
    return dados.get("ok"), dados.get("description")


if __name__ == "__main__":
    config = ler_config()
    linhas = ler_planilha()
    pendentes = [l for l in linhas if not (l.get("postado") or "").strip()]
    print(f"{len(pendentes)} oferta(s) para postar.")

    for i, linha in enumerate(pendentes):
        link = linha["link"].strip()
        produto = ler_produto(link)
        titulo = (linha.get("titulo") or "").strip() or encurtar(produto["nome"] or "")
        foto = produto["foto_jpg"] or produto["foto"]
        if not titulo or not foto:
            print(f"Pulei {link}: não consegui ler nome/foto.")
            continue
        legenda = montar_legenda(
            titulo, linha["preco_de"].strip(), linha["preco_por"].strip(),
            (linha.get("cupom") or "").strip(), link,
        )
        ok, erro = enviar(config, foto, legenda)
        print("ok:", ok, "|", titulo, "|", erro or "")
        if ok:
            linha["postado"] = "sim"
            salvar_planilha(linhas)
        if i < len(pendentes) - 1:
            time.sleep(PAUSA_ENTRE_POSTS)
