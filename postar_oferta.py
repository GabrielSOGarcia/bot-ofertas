import html
import requests

CONFIG_PATH = r"C:\bot-config\config.txt"   # senhas ficam fora da pasta do bot


def ler_config(caminho=CONFIG_PATH):
    config = {}
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if "=" in linha and not linha.startswith("#"):
                chave, valor = linha.split("=", 1)
                config[chave.strip()] = valor.strip()
    return config


def montar_legenda(nome, preco_de, preco_por, cupom, link):
    linhas = [f"🔥 <b>{html.escape(nome)}</b>", ""]
    if preco_de:
        linhas.append(f"De <s>R$ {preco_de}</s>")
    linhas.append(f"💸 Por <b>R$ {preco_por}</b>")
    if cupom:
        linhas.append(f"🎟 Cupom: <code>{html.escape(cupom)}</code>")
    linhas += ["", f"👉 <a href=\"{link}\">Pegar promoção</a>"]
    return "\n".join(linhas)


def baixar_imagem(foto_url):
    # Baixa a foto no seu computador e envia como arquivo (mais confiável
    # do que pedir para o Telegram buscar o link da imagem)
    cabecalhos = {"User-Agent": "Mozilla/5.0"}
    resposta = requests.get(foto_url, headers=cabecalhos, timeout=30)
    resposta.raise_for_status()
    return resposta.content


def postar_oferta(config, foto_url, legenda):
    imagem = baixar_imagem(foto_url)
    url = f"https://api.telegram.org/bot{config['TOKEN']}/sendPhoto"
    resposta = requests.post(
        url,
        data={
            "chat_id": config["CANAL"],
            "caption": legenda,
            "parse_mode": "HTML",
        },
        files={"photo": ("foto.jpg", imagem)},
        timeout=60,
    )
    dados = resposta.json()
    print("ok:", dados.get("ok"), "| descrição:", dados.get("description"))


if __name__ == "__main__":
    config = ler_config()

    # Dados de teste: troque pelos de um produto real depois
    nome = "Chaleira Elétrica 1.8L Inox"
    preco_de = "199,80"
    preco_por = "99,90"
    cupom = ""
    link = "https://www.mercadolivre.com.br"
    foto_url = "https://picsum.photos/600/600.jpg"

    legenda = montar_legenda(nome, preco_de, preco_por, cupom, link)
    postar_oferta(config, foto_url, legenda)
