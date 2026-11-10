import hashlib, json, os, sys, time, urllib.request
from collections import defaultdict
from datetime import datetime

# Relatório de vendas dos links de afiliado.
# Uso: python relatorio.py 7   (mostra os últimos 7 dias no terminal; padrão 1)
# Toda vez também salva no Obsidian uma nota com dia, semana e mês lado a lado.

PASTA_OBSIDIAN = os.environ.get("BOT_OBSIDIAN",
                                "")  # "" desliga
PERIODOS = [("Dia", 1), ("Semana", 7), ("Mês", 30)]
CONFIG_PATH = os.environ.get("BOT_CONFIG", r"C:\bot-config\config.txt")   # senhas fora da pasta do bot

def ler_config(caminho=CONFIG_PATH):
    config = {}
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            if "=" in linha:
                chave, valor = linha.strip().split("=", 1)
                config[chave.strip()] = valor.strip()
    return config

cfg = ler_config()

def chamar_shopee(consulta):
    payload = json.dumps({"query": consulta})
    ts = str(int(time.time()))
    assinatura = hashlib.sha256((cfg["SHOPEE_APPID"] + ts + payload + cfg["SHOPEE_SECRET"]).encode()).hexdigest()
    req = urllib.request.Request(
        "https://open-api.affiliate.shopee.com.br/graphql",
        data=payload.encode(), method="POST",
        headers={"Content-Type": "application/json",
                 "Authorization": f"SHA256 Credential={cfg['SHOPEE_APPID']}, Timestamp={ts}, Signature={assinatura}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        dados = json.loads(resp.read())
    if "errors" in dados:
        raise Exception(dados["errors"])
    return dados["data"]

def buscar_vendas(inicio, fim):
    vendas, scroll = [], None
    while True:
        extra = f', scrollId: "{scroll}"' if scroll else ""
        consulta = ('{ conversionReport(purchaseTimeStart: %d, purchaseTimeEnd: %d, limit: 500%s) { '
                    'nodes { purchaseTime totalCommission utmContent '
                    'orders { items { itemName qty itemTotalCommission } } } '
                    'pageInfo { hasNextPage scrollId } } }') % (inicio, fim, extra)
        dados = chamar_shopee(consulta)["conversionReport"]
        vendas += dados["nodes"]
        if not dados["pageInfo"]["hasNextPage"]:
            return vendas
        scroll = dados["pageInfo"]["scrollId"]

def reais(valor):
    return f"R$ {float(valor or 0):,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")

def resumir(vendas):
    # As etiquetas do link chegam juntas no utmContent (ex.: "telegram-simples-airfryer")
    r = {"vendas": len(vendas), "total": 0.0, "canal": defaultdict(float), "tipo": defaultdict(float),
         "palavra": defaultdict(float), "produtos": defaultdict(lambda: [0, 0.0])}
    for v in vendas:
        comissao = float(v.get("totalCommission") or 0)
        etiquetas = [e for e in (v.get("utmContent") or "").split("-") if e] + ["sem etiqueta"] * 3
        r["total"] += comissao
        r["canal"][etiquetas[0]] += comissao
        r["tipo"][etiquetas[1]] += comissao
        r["palavra"][etiquetas[2]] += comissao
        for pedido in v.get("orders") or []:
            for item in pedido.get("items") or []:
                r["produtos"][item.get("itemName", "?")][0] += int(item.get("qty") or 0)
                r["produtos"][item.get("itemName", "?")][1] += float(item.get("itemTotalCommission") or 0)
    return r

def maiores(grupo, n=10):
    return sorted(grupo.items(), key=lambda x: -x[1])[:n]

def imprimir(r, dias, inicio):
    print(f"Vendas de {datetime.fromtimestamp(inicio):%d/%m %H:%M} até agora ({dias} dia(s))\n")
    if not r["vendas"]:
        print("Nenhuma venda no período.")
        return
    print(f"Vendas: {r['vendas']} | Comissão total: {reais(r['total'])}\n")
    for titulo, chave in [("Por canal", "canal"), ("Por tipo", "tipo"), ("Por palavra", "palavra")]:
        print(titulo + ":")
        for nome, valor in maiores(r[chave]):
            print(f"  {nome:20} {reais(valor)}")
        print()
    print("Produtos que mais renderam:")
    for nome, (qtd, valor) in sorted(r["produtos"].items(), key=lambda x: -x[1][1])[:10]:
        print(f"  {reais(valor):>12}  {qtd}x  {nome[:60]}")

def barra(valor, maximo, largura=12):
    return "█" * max(1, round(largura * valor / maximo)) if maximo and valor > 0 else ""

def celula(texto):
    return str(texto).replace("|", "/")

def pizza(titulo, grupo):
    fatias = [(n, v) for n, v in maiores(grupo, 8) if v > 0]
    if not fatias:
        return []
    linhas = ["```mermaid", f"pie showData title {titulo}"]
    linhas += [f'    "{n.replace(chr(34), "")}" : {v:.2f}' for n, v in fatias]
    return linhas + ["```", ""]

def nota_obsidian(resumos, agora):
    mes = resumos["Mês"]
    linhas = ["---", "tags: [bot-ofertas, relatorio]", f"atualizado: {agora:%Y-%m-%d %H:%M}", "---",
              f"# 📊 Relatório de vendas — {agora:%d/%m/%Y %H:%M}", "",
              "| Período | Vendas | Comissão | |", "|---|--:|--:|---|"]
    maior_total = max(r["total"] for r in resumos.values())
    for nome, _ in PERIODOS:
        r = resumos[nome]
        linhas.append(f"| {nome} | {r['vendas']} | {reais(r['total'])} | {barra(r['total'], maior_total)} |")
    linhas.append("")
    if not mes["vendas"]:
        linhas += ["> [!note] Nenhuma venda nos últimos 30 dias",
                   "> É normal no começo: a Shopee demora para registrar as vendas.", ""]
        return "\n".join(linhas)
    linhas += ["## 🥧 De onde vem a comissão (mês)", ""]
    linhas += pizza("Simples x Caro", mes["tipo"]) + pizza("Por canal", mes["canal"])
    linhas += ["## 🔑 Palavras que mais renderam", "",
               "| Palavra | Dia | Semana | Mês | |", "|---|--:|--:|--:|---|"]
    topo = maiores(mes["palavra"], 15)
    for palavra, valor in topo:
        linhas.append(f"| {celula(palavra)} | {reais(resumos['Dia']['palavra'].get(palavra, 0))} "
                      f"| {reais(resumos['Semana']['palavra'].get(palavra, 0))} | {reais(valor)} "
                      f"| {barra(valor, topo[0][1])} |")
    linhas += ["", "## 🏆 Produtos que mais renderam (mês)", "",
               "| Produto | Unidades | Comissão | |", "|---|--:|--:|---|"]
    produtos = sorted(mes["produtos"].items(), key=lambda x: -x[1][1])[:15]
    for nome, (qtd, valor) in produtos:
        linhas.append(f"| {celula(nome[:70])} | {qtd} | {reais(valor)} | {barra(valor, produtos[0][1][1])} |")
    return "\n".join(linhas) + "\n"

def salvar_no_obsidian(texto, agora):
    if not PASTA_OBSIDIAN or not os.path.isdir(PASTA_OBSIDIAN):
        return
    pasta = os.path.join(PASTA_OBSIDIAN, "Relatórios")
    os.makedirs(pasta, exist_ok=True)
    for arquivo in (os.path.join(PASTA_OBSIDIAN, "Relatório - último.md"),
                    os.path.join(pasta, f"Relatório {agora:%Y-%m-%d}.md")):
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(texto)
    print(f"\nNota salva no Obsidian: Bot Ofertas/Relatórios/Relatório {agora:%Y-%m-%d}")

dias = int(sys.argv[1]) if len(sys.argv) > 1 else 1
agora = datetime.now()
fim = int(time.time())
maior_periodo = max(dias, max(d for _, d in PERIODOS))
try:
    vendas = buscar_vendas(fim - maior_periodo * 86400, fim)
except Exception as e:
    print("A Shopee recusou o relatório:", e)
    print("Copie essa mensagem e use para ajustar o bot.")
    sys.exit(1)

def no_periodo(d):
    return [v for v in vendas if int(v.get("purchaseTime") or 0) >= fim - d * 86400]

imprimir(resumir(no_periodo(dias)), dias, fim - dias * 86400)
salvar_no_obsidian(nota_obsidian({nome: resumir(no_periodo(d)) for nome, d in PERIODOS}, agora), agora)
