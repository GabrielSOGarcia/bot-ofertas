# Observador de grupos (06/11): o que os OUTROS grupos de ofertas postam (o chip está neles) e o que mais
# engaja (reações). O programa do WhatsApp guarda em whatsapp/grupos_observados.json; o painel mostra
# (/concorrentes e /concorrentestop) e o analisar_grupos.py cruza com as nossas listas para achar o que
# eles postam e a gente ainda não busca. Só leitura.
import re
import unicodedata

def normalizar(s):
    s = unicodedata.normalize("NFKD", str(s).lower())
    return "".join(c for c in s if not unicodedata.combining(c))

# Palavras que dizem para quem é o produto (aproximado: serve para ver a proporção, não para filtrar)
FEMININO = ["feminin", "mulher", "maquiagem", "batom", "gloss", "rimel", "cilios", "sombra", "blush", "base liquida",
            "corretivo", "skincare", "serum", "hidratante facial", "vestido", "saia", "cropped", "blusa", "sutia",
            "calcinha", "lingerie", "biquini", "maio", "legging", "sandalia", "rasteira", "salto", "sapatilha",
            "bolsa", "clutch", "brinco", "colar", "semijoia", "esmalte", "unha", "chapinha", "prancha", "secador",
            "escova secadora", "babyliss", "cachos", "shampoo", "condicionador", "mascara capilar", "body splash",
            "perfume feminino", "wepink", "boca rosa", "vult", "ruby rose", "bebe", "fralda", "mamadeira",
            "infantil", "boneca", "gestante", "maternidade", "depilador", "absorvente", "necessaire"]
MASCULINO = ["masculin", "homem", "barba", "barbeador", "cueca", "chuteira", "bermuda", "sunga", "regata masculina",
             "ferramenta", "furadeira", "parafusadeira", "chave de", "automotiv", "carro", "moto", "capacete", "pneu",
             "gamer", "ps5", "playstation", "xbox", "nintendo", "controle", "pesca", "molinete", "churrasco",
             "cerveja", "futebol", "basquete", "whey", "creatina", "perfume masculino", "aparador de pelos"]

def publico(texto):
    t = normalizar(texto)
    f = sum(1 for p in FEMININO if p in t)
    m = sum(1 for p in MASCULINO if p in t)
    return "♀" if f > m else "♂" if m > f else ""

_LIXO = re.compile(r"^[\W_]*(oferta|promo|achadinho|corre|aproveita|cupom|olha|imperdivel|link|compre|confira)\b", re.I)

def titulo(texto):
    # A linha que parece o nome do produto: sem link, sem preço, com letras; pula a chamada ("🔥 OFERTA!")
    linhas = [l.strip(" *_~-•") for l in str(texto).splitlines()]
    boas = [l for l in linhas if l and "http" not in l and "R$" not in l and len(re.findall(r"[A-Za-zÀ-ÿ]{3,}", l)) >= 2]
    limpas = [l for l in boas[:5] if not _LIXO.match(normalizar(l))]
    # 08/11: a 1ª linha costuma ser a CHAMADA em maiúsculas ("NOTINHA DE CAFÉ DELICIOSA", "FÁCIL DE TOMAR");
    # o nome do produto vem depois, em letra normal. Prefere a linha que não é toda maiúscula
    for l in limpas:
        letras = re.sub(r"[^A-Za-zÀ-ÿ]", "", l)
        if letras and not letras.isupper():
            return re.sub(r"[^\w\sÀ-ÿ%,.()/+-]", "", l).strip()[:90]
    for l in limpas:
        return re.sub(r"[^\w\sÀ-ÿ%,.()/+-]", "", l).strip()[:90]
    return (boas[0] if boas else (linhas[0] if linhas else ""))[:90]

def preco_final(post):
    # O último preço do texto costuma ser o "por" (De R$ 399 por R$ 229)
    precos = post.get("precos") or []
    return precos[-1] if precos else ""
