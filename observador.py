# Bot B: observa canais do WhatsApp de outros afiliados e mostra o que mais engaja (visualizações e
# reações), para dar ideias de produto ao bot A. Só LÊ: não copia post nem link de ninguém. O bot A
# sempre busca o produto na Shopee e gera o link de afiliado dele.
# Os dados da leitura vêm do whatsapp/servidor.js (GET /canal/mensagens). Aqui fica só a análise.
import json, re, statistics

ARQUIVO = "canais_observados.json"     # dentro da pasta de cada bot: {"canais": [{id, nome}], "lidas": {...}}
# (09/11, Gabriel: "quero que todo canal meu observe a concorrência, já criado observando") Os canais
# observados valem para TODOS os bots: a lista comum fica em bots/_todos/ (o painel ignora pastas com "_",
# o whatsapp/servidor.js lê bots/*/canais_observados.json, então lê esta também). As listas antigas de cada
# bot continuam valendo (somam).
PASTA_TODOS = "_todos"
import os

def carregar_todos(pasta_bots):
    # Todos os canais observados, de todas as pastas de bots/ (sem repetir)
    dados = {"canais": []}
    try:
        pastas = sorted(os.listdir(pasta_bots))
    except OSError:
        return dados
    for p in pastas:
        for c in carregar(os.path.join(pasta_bots, p, ARQUIVO))["canais"]:
            if not any(x["id"] == c["id"] for x in dados["canais"]):
                dados["canais"].append(c)
    return dados

def caminho_todos(pasta_bots):
    os.makedirs(os.path.join(pasta_bots, PASTA_TODOS), exist_ok=True)
    return os.path.join(pasta_bots, PASTA_TODOS, ARQUIVO)

def tirar_de_todos(pasta_bots, canal_id):
    tirou = False
    for p in os.listdir(pasta_bots):
        caminho = os.path.join(pasta_bots, p, ARQUIVO)
        if os.path.exists(caminho):
            dados = carregar(caminho)
            if tirar_canal(dados, canal_id):
                salvar(caminho, dados)
                tirou = True
    return tirou

def carregar(caminho):
    try:
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
    except (OSError, ValueError):
        dados = {}
    dados.setdefault("canais", [])
    return dados

def salvar(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)

def adicionar_canal(dados, canal_id, nome, convite=None, oficial=False):
    # oficial = canal da própria Shopee: o observador avisa no painel de cada post novo dele
    for c in dados["canais"]:
        if c["id"] == canal_id:
            if convite:
                c["convite"] = convite      # guarda o código do link: serve de segunda via de leitura
            if oficial:
                c["oficial"] = True
            return False
    dados["canais"].append({"id": canal_id, "nome": nome or canal_id, "convite": convite, "oficial": oficial})
    return True

def tirar_canal(dados, canal_id):
    antes = len(dados["canais"])
    dados["canais"] = [c for c in dados["canais"] if c["id"] != canal_id]
    return len(dados["canais"]) < antes

SEM_TITULO = re.compile(r"^\W*(de|por|a partir de|cupom|compre|pegue|link|use|ganhe|frete|r\$)\b", re.I)

def titulo_do_produto(texto):
    # O nome do produto costuma ser a linha mais "de nome" do começo do post: sem link, sem preço,
    # sem chamada tipo "BAIXOU O PREÇO". Pega a maior linha curta que sobrar.
    linhas = [re.sub(r"[*_~`]", "", l).strip() for l in (texto or "").splitlines()]
    candidatas = []
    for l in linhas[:8]:
        limpa = re.sub(r"[^\w\s\-+/.,%$()ºª]", "", l, flags=re.UNICODE).strip()
        if len(limpa) < 8 or "http" in l or "R$" in l or SEM_TITULO.match(limpa):
            continue
        if limpa.isupper() and len(limpa.split()) <= 4:     # "BAIXOU O PREÇO", "ACHADO DO DIA"
            continue
        candidatas.append(limpa)
    return max(candidatas[:3], key=len) if candidatas else ""

def preco_do_texto(texto):
    achados = re.findall(r"R\$\s*([\d.]+,\d{2})", texto or "")
    return achados[-1] if achados else ""       # em "De X por Y" o último é o preço de agora

def tem_link_de_oferta(texto):
    return bool(re.search(r"shopee\.com\.br|shope\.ee|mercadolivre|amzn\.to|amazon\.com\.br", texto or ""))

def ranquear(mensagens, canal_nome):
    # Pontuação = visualizações da mensagem dividido pela mediana do canal (compara canais grandes e
    # pequenos). Só entram posts de oferta (com link e um título que pareça produto).
    com_views = [m["views"] for m in mensagens if m.get("views")]
    if not com_views:
        # Posts recebidos ao vivo não trazem visualizações: todos valem 1 e o que pesa é o produto
        # aparecer em mais de um canal / mais de uma vez (melhores() soma isso)
        mensagens = [dict(m, views=1) for m in mensagens]
        com_views = [1]
    mediana = statistics.median(com_views) or 1
    saida = []
    for m in mensagens:
        titulo = titulo_do_produto(m.get("texto", ""))
        if not titulo or not tem_link_de_oferta(m.get("texto", "")):
            continue
        saida.append({"canal": canal_nome, "titulo": titulo, "preco": preco_do_texto(m["texto"]),
                      "views": m.get("views", 0), "reacoes": m.get("reacoes", 0),
                      "nota": round(m.get("views", 0) / mediana, 2)})
    return saida

def melhores(todos, quantos=10):
    # Mesmo produto em mais de um canal: junta e conta (produto repetido pesa mais)
    juntos = {}
    for r in todos:
        chave = re.sub(r"\W+", " ", r["titulo"].lower()).strip()[:40]
        atual = juntos.get(chave)
        if atual:
            atual["canais"].add(r["canal"])
            atual["nota"] = round(max(atual["nota"], r["nota"]) + 0.5, 2)
            atual["views"] = max(atual["views"], r["views"])
        else:
            juntos[chave] = dict(r, canais={r["canal"]})
    return sorted(juntos.values(), key=lambda r: (r["nota"], r["views"]), reverse=True)[:quantos]
