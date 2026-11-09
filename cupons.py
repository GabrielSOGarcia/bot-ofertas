# Cupons da Shopee: lidos e escritos no cupons.txt (pasta principal do bot).
# Usado pelo postar_shopee.py (linha do cupom no post e alerta de cupom) e pelo painel.py
# (você cola o cupom no Telegram e ele vem para cá).
import re
from datetime import date, datetime

CABECALHO = (
    "# Cupons da Shopee (valem para todos os bots da Shopee). Um por linha:\n"
    "# CÓDIGO | desconto (10% ou 70 para R$ 70) | compra mínima | limite do desconto (- = sem) | válido até | descrição\n"
    "# Ex.: OFERTAS10 | 10% | 49 | 50 | 11/11/2026 | 10% OFF acima de R$ 49, limitado a R$ 50\n"
    "# Cupom vencido não aparece nos posts e sai do arquivo quando o painel salvar.\n"
)

def numero(texto):
    # "R$ 49,90" -> 49.9 | "1.000" -> 1000 | "" ou "-" -> None
    t = re.sub(r"[^\d,.]", "", str(texto or ""))
    if not t:
        return None
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+", t):
        t = t.replace(".", "")
    try:
        return float(t)
    except ValueError:
        return None

def num_txt(v):
    return f"{v:g}".replace(".", ",")

def ler_data(texto, hoje=None):
    # "11/11", "11/11/26" ou "11/11/2026". Sem ano: este ano (ou o próximo, se a data já passou)
    hoje = hoje or date.today()
    m = re.fullmatch(r"\s*(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\s*", str(texto or ""))
    if not m:
        return None
    dia, mes, ano = int(m[1]), int(m[2]), m[3]
    try:
        if ano:
            return date(int(ano) + (2000 if len(ano) == 2 else 0), mes, dia)
        d = date(hoje.year, mes, dia)
        return d if d >= hoje else date(hoje.year + 1, mes, dia)
    except ValueError:
        return None

def descricao_auto(c):
    off = f"{num_txt(c['valor'])}% OFF" if c["porcentagem"] else f"R$ {num_txt(c['valor'])} OFF"
    if c["minimo"]:
        off += f" acima de R$ {num_txt(c['minimo'])}"
    if c["porcentagem"] and c["limite"]:
        off += f", limitado a R$ {num_txt(c['limite'])}"
    return off

def novo(codigo, desconto, minimo=None, limite=None, validade=None, descricao="", hoje=None):
    # Monta um cupom a partir de textos ("10%" ou "70", "49", "50", "11/11"). None se não der.
    codigo = str(codigo or "").strip().upper()
    if not re.fullmatch(r"[A-Z0-9]{4,20}", codigo):
        return None
    valor = numero(desconto)
    porcentagem = str(desconto).strip().endswith("%")
    if not valor or (porcentagem and valor > 90):
        return None
    hoje = hoje or date.today()
    if isinstance(validade, date):
        venc = validade
    else:
        venc = ler_data(validade, hoje) or hoje   # sem data: vale só hoje
    c = {"codigo": codigo, "porcentagem": porcentagem, "valor": valor, "minimo": numero(minimo) or 0,
         "limite": numero(limite) if porcentagem else None, "validade": venc,
         "descricao": " ".join(str(descricao or "").replace("|", "/").split())}
    c["descricao"] = c["descricao"] or descricao_auto(c)
    return c

def ler(caminho, so_validos=True, hoje=None):
    hoje = hoje or date.today()
    cupons = []
    try:
        with open(caminho, encoding="utf-8") as f:
            linhas = f.readlines()
    except FileNotFoundError:
        return []
    for linha in linhas:
        if linha.strip().startswith("#") or "|" not in linha:
            continue
        p = [x.strip() for x in linha.split("|")] + [""] * 6
        try:
            venc = datetime.strptime(p[4], "%d/%m/%Y").date()
        except ValueError:
            continue
        c = novo(p[0], p[1], p[2], None if p[3] in ("", "-") else p[3], venc, p[5], hoje)
        if c and (not so_validos or c["validade"] >= hoje):
            cupons.append(c)
    return cupons

def linha(c):
    desconto = f"{num_txt(c['valor'])}%" if c["porcentagem"] else num_txt(c["valor"])
    limite = num_txt(c["limite"]) if c["limite"] else "-"
    return (f"{c['codigo']} | {desconto} | {num_txt(c['minimo'])} | {limite} | "
            f"{c['validade']:%d/%m/%Y} | {c['descricao']}")

def salvar(caminho, cupons, hoje=None):
    # Salva só os que ainda valem (vencido sai sozinho), do que vence antes para o que vence depois
    hoje = hoje or date.today()
    validos = sorted((c for c in cupons if c["validade"] >= hoje), key=lambda c: (c["validade"], c["codigo"]))
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(CABECALHO + "".join(linha(c) + "\n" for c in validos))
    return validos

def adicionar(cupons, novos):
    # Cupom com o mesmo código é substituído pelo novo
    codigos = {c["codigo"] for c in novos}
    return [c for c in cupons if c["codigo"] not in codigos] + list(novos)

def desconto(c, preco):
    if preco < c["minimo"]:
        return 0.0
    if c["porcentagem"]:
        valor = preco * c["valor"] / 100
        return min(valor, c["limite"]) if c["limite"] else valor
    return min(c["valor"], preco)

def melhor(cupons, preco, minimo_rs=0):
    # O cupom que mais economiza nesse preço (ou None se nenhum economiza pelo menos minimo_rs)
    opcoes = [(desconto(c, preco), c) for c in cupons]
    valor, cupom = max(opcoes, key=lambda x: x[0], default=(0, None))
    return (cupom, valor) if cupom and valor >= max(minimo_rs, 0.01) else (None, 0.0)
