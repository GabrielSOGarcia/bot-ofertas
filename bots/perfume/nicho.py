# Bot "Perfumes" (09/11): grupo de perfume do MERCADO LIVRE, masculino e feminino alternando (um ♀, um ♂).
# Combinado com o Gabriel: 1 grupo só no começo (perfume se compra muito de presente; os grupos de referência
# misturam); separar quando passar de ~500-1000 pessoas. Sempre com desconto de verdade.
# 09/11 15h40, Gabriel: "perfume é perfume: pode ser cópia, pouco conhecido ou conhecido". O que manda é a LOJA:
# 1º loja oficial da marca, 2º lojas grandes (Mercado Livre, Sephora, Amazon...), 3º outras oficiais e
# MercadoLíder, 4º loja comum muito bem avaliada e com muitas vendas (ver degrau_loja_ml no postar_shopee.py).
# Os produtos e o link vêm da vitrine da Central de Afiliados do Mercado Livre (mercadolivre.py), com a sessão
# do Gabriel (ml_cookies.txt ao lado do config.txt).

LOJA = "mercadolivre"
CHAVE_CANAL = "CANAL_PERFUME"   # só se um dia postar no Telegram; hoje é só WhatsApp
NICHO_IA = ("perfumes masculinos e femininos do Mercado Livre: importados, árabes, nacionais (Natura, Boticário), "
            "marcas pouco conhecidas e perfumes inspirados/contratipos, todos valem")
TEXTO_MODELO_IA = (
    "Modelo ideal: perfume ou body splash com desconto de verdade e foto REAL do produto. Pode ser marca famosa, "
    "árabe, nacional, pouco conhecida ou perfume inspirado/contratipo (o nome deve dizer 'inspirado' quando for). "
    "Recuse: decant, amostra, réplica falsificada vendida como se fosse o original, foto gerada por inteligência "
    "artificial, e produto que não seja perfume, colônia ou body splash.\n")

# ---------- Critérios ----------
EXIGIR_MARCA_SEMPRE = False   # perfume é perfume: a garantia vem da loja (escada de lojas), não da marca
DESCONTO_MINIMO = 20          # 09/11, Gabriel: "promoção boa, muito boa mesmo" (Natura a preço cheio não vai)
# Pontuação dentro de cada busca (somam 1): desconto pesa mais que no Casa; o mais barato pesa pouco (o que
# importa é o perfume famoso em promoção). Comissão, vendas e nota continuam. A loja vem antes (escada de lojas)
PESO_DESCONTO = 0.3
PESO_COMISSAO = 0.25
PESO_VENDAS = 0.25
PESO_NOTA = 0.15
PESO_PRECO = 0.05
VENDAS_MINIMAS = 500          # o Mercado Livre mostra "+500", "+1000", "+5mil"...
VENDAS_MINIMAS_CARO = 50      # importado caro vende menos
NOTA_MINIMA = 4.5
NOTA_MINIMA_CARO = 4.6
COPIAR_OFERTAS = 0            # a cópia dos outros grupos é de link da Shopee
# Mensagem dos grupos: o de perfume primeiro (o link dele entra em LINK_GRUPO_PERFUME no postar_shopee.py)
GRUPOS = [(NOME_GRUPO_PERFUME, LINK_GRUPO_PERFUME), (NOME_GRUPO_CASA, LINK_GRUPO_CASA),
          (NOME_GRUPO_GERAL, LINK_GRUPO_GERAL)]
FRASES_GRUPO = {
    "dia": ["🌸 Bom dia cheiroso: perfume famoso, árabe e nacional com desconto de verdade, só de loja boa.",
            "✨ Começa o dia perfumado! Separamos os perfumes que estão com o melhor preço hoje."],
    "tarde": ["💎 Tarde perfumada: Sauvage, 1 Million, Good Girl, árabes... confere os que baixaram de preço hoje.",
              "🎁 Perfume é presente que nunca erra: olha as promoções de hoje e já garante o seu (ou o de alguém)."],
    "noite": ["🌙 Noite de promoção: os perfumes mais desejados com desconto, antes que o preço volte.",
              "😍 Fixação que todo mundo elogia, pagando bem menos: confere os perfumes de hoje aqui no grupo."],
}
WHATSAPP_MAX_DIA = 40         # o chip é o mesmo do Casa e do Geral: começa devagar
MAX_PALAVRAS_NOME = 8         # "Perfume Árabe Al Wataniah Sabah Al Ward" (a linha + a marca precisam caber)
MAX_PALAVRAS_RODADA = 15     # buscas no Mercado Livre por rodada (com calma, é a sessão do Gabriel)
PAUSA_ENTRE_BUSCAS = 2

# A vitrine do Mercado Livre acha "Natura Una Artisan Feminino Eau de Parfum" na busca "perfume feminino":
# a busca combina se cada termo (ou um sinônimo) aparece em qualquer parte do nome
COMBINA_EM_QUALQUER_LUGAR = True
SINONIMOS_BUSCA = {
    "perfume": ["parfum", "toilette", "colonia", "edp", "edt", "fragrancia", "deo", "eau"],
    "masculino": ["homem", "men", "homme", "him", "masculina", "uomo"],
    "feminino": ["mulher", "woman", "women", "femme", "her", "feminina", "donna"],
}

# "Parecido com post recente" olha as palavras do nome: estas, que todo perfume tem, não contam
PARECIDO_IGNORAR = ["perfume", "perfumes", "eau de parfum", "eau de toilette", "parfum", "toilette", "edp", "edt",
                    "deo", "colônia", "desodorante", "masculino", "feminino", "árabe", "importado", "original",
                    "spray", "unissex", "body splash", "fragrância"]

# Cópia/inspirado pode (Gabriel, 09/11). Fica de fora: réplica (falsificado vendido como original), decant e
# amostra (frasquinho fracionado) e tester
BLOQUEADAS = [b for b in BLOQUEADAS if b not in ("similar", "essência")] + [
    "réplica", "replica", "primeira linha", "1ª linha", "decant", "amostra", "amostras", "tester",
]

# ---------- O que buscar (substitui a lista do Casa inteira) ----------
# 09/11 16h, Gabriel: "dá preferência pros perfumes mais conhecidos (Sauvage Dior Eau de Parfum, One Million,
# Ultra Male; Carolina Herrera...). Depois pros dupes (as cópias). Seja masculino ou feminino."
# Categorias "♀" = vez do feminino; as outras = vez do masculino (ALTERNAR_FEMININO: um ♀, um ♂).
# O peso (PESO_CATEGORIA) faz a preferência: famosos 3 vezes por volta, dupes 2, nacionais e body splash 1.
PERFUMES = [
    # 1º OS FAMOSOS
    ("famoso masculino", ["sauvage eau de parfum", "sauvage dior", "1 million", "ultra male", "le male elixir",
                          "le male", "invictus", "eros versace", "stronger with you", "acqua di gio profumo",
                          "the most wanted azzaro", "azzaro wanted", "y yves saint laurent", "boss bottled",
                          "212 vip men", "bleu de chanel", "phantom rabanne", "armani code", "ck be",
                          "jean paul gaultier masculino", "rabanne masculino"]),
    ("♀ famoso feminino", ["good girl carolina herrera", "very good girl", "212 vip rosé", "carolina herrera feminino",
                           "la vie est belle", "idôle lancôme", "olympea", "lady million", "fame rabanne",
                           "libre yves saint laurent", "scandal jean paul gaultier", "my way armani",
                           "j'adore dior", "miss dior", "coco mademoiselle", "born in roma", "eternity calvin klein",
                           "lancôme feminino", "jean paul gaultier feminino"]),
    # (09/11: a vitrine de afiliados NÃO tem Dior, Chanel, Carolina Herrera, Versace, Azzaro, YSL... essas buscas
    # voltam vazias e o bot passa para a próxima; ficam na lista caso a vitrine passe a ter)
    # 2º OS DUPES (cópias/inspirados e os árabes que imitam os famosos)
    ("dupe masculino", ["perfume inspirado masculino", "contratipo masculino", "perfume asad", "club de nuit intense",
                        "khamrah", "fakhar black", "maison alhambra masculino", "al wataniah masculino",
                        "perfume árabe masculino", "lattafa masculino"]),
    ("♀ dupe feminino", ["perfume inspirado feminino", "contratipo feminino", "yara lattafa", "sabah al ward",
                         "durrat al aroos", "fakhar rose", "maison alhambra feminino", "perfume árabe feminino",
                         "lattafa feminino"]),
    # 3º nacionais e body splash
    ("perfume nacional masculino", ["malbec", "kaiak", "natura homem", "quasar", "zaad", "egeo masculino",
                                    "essencial masculino", "uomini", "boticário masculino"]),
    ("♀ perfume nacional feminino", ["natura una", "essencial feminino", "lily boticário", "floratta",
                                     "egeo feminino", "glamour boticário", "ilía natura", "kriska",
                                     "boticário feminino"]),
    ("♀ body splash", ["body splash", "body splash victoria's secret", "body splash wepink"]),
]
PALAVRAS = {c: bs for c, bs in PERFUMES}
for _c, _p in [("famoso masculino", 3), ("♀ famoso feminino", 3), ("dupe masculino", 2), ("♀ dupe feminino", 2)]:
    PESO_CATEGORIA[_c] = _p
# "Caro" (1 a cada poucos posts): os de luxo, além dos famosos que já estão na lista normal
IMPORTADOS = [
    ("luxo masculino", ["bleu de chanel parfum", "sauvage elixir", "aventus creed", "tom ford masculino",
                        "dior homme intense", "layton parfums de marly"]),
    ("♀ luxo feminino", ["chanel n5", "coco mademoiselle chanel", "black opium", "delina parfums de marly",
                         "tom ford feminino", "good girl supreme"]),
]
CAROS = [b for _, bs in IMPORTADOS for b in bs]
ALTERNAR_FEMININO = True

def _sem_acento(t):
    return " ".join(unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower().split())
TIPOS_PROPRIOS = TIPOS_PROPRIOS + [b for _, bs in PERFUMES + IMPORTADOS for b in bs]   # cada busca é o tipo
CATEGORIAS_EXTRA = [(c, [_sem_acento(b) for b in bs]) for c, bs in PERFUMES + IMPORTADOS] + CATEGORIAS_EXTRA

# ---------- Marcas e linhas de perfume (somam às do Casa) ----------
MARCAS = MARCAS + [
    # importados
    "Carolina Herrera", "Paco Rabanne", "Rabanne", "Dior", "Chanel", "Giorgio Armani", "Armani", "Versace",
    "Azzaro", "Jean Paul Gaultier", "Lancôme", "Yves Saint Laurent", "YSL", "Dolce & Gabbana", "Hugo Boss",
    "Calvin Klein", "Ralph Lauren", "Montblanc", "Givenchy", "Prada", "Valentino", "Mugler", "Kenzo",
    "Antonio Banderas", "Benetton", "Victoria's Secret", "Ariana Grande", "Lacoste", "Diesel", "Ferrari",
    "Creed", "Tom Ford", "Parfums de Marly", "Boss", "Sauvage", "1 Million", "Ultra Male", "Le Male", "Invictus",
    # árabes (marca e linhas famosas que aparecem sem a marca no título)
    "Lattafa", "Al Wataniah", "Maison Alhambra", "Armaf", "Afnan", "Rasasi", "Ajmal", "Al Haramain", "Orientica",
    "Fakhar", "Khamrah", "Asad", "Yara", "Club de Nuit", "Sabah Al Ward", "Durrat Al Aroos", "Badee Al Oud",
    # nacionais
    "Natura", "O Boticário", "Boticário", "Eudora", "Avon", "Jequiti", "Mahogany", "Ciclo", "WePink", "We Pink",
    "Malbec", "Kaiak", "Zaad", "Egeo", "Quasar", "Floratta", "Lily", "Essencial", "Una", "Ilía", "Kriska",
    "Uomini", "Glamour",
]

# ---------- Chamadas ----------
CHAMADAS_GERAIS = ["🔥 ACHADO DO DIA", "👃 CHEIRO DE RICO GASTANDO POUCO", "😍 FIXAÇÃO QUE TODO MUNDO ELOGIA",
                   "😱 ESSE PREÇO NÃO DURA", "🛒 QUEM VIU, LEVOU", "🎁 PRESENTE QUE ACERTA"]
CHAMADAS_POR_TIPO = [
    (["árabe", "lattafa", "asad", "khamrah", "yara", "fakhar", "club de nuit", "alhambra", "wataniah",
      "sabah al ward", "durrat"], ["🕌 PERFUME ÁRABE QUE ESTOURA", "🔥 O ÁRABE QUEM TODO MUNDO QUER"]),
    (["body splash"], ["🌸 CHEIRINHO O DIA INTEIRO"]),
]
CHAMADAS_CARO = ["💎 IMPORTADO ORIGINAL COM DESCONTO", "😮 IMPORTADO NESSE PREÇO NÃO É TODO DIA",
                 "🏆 PERFUME DE GRIFE EM PROMOÇÃO"]
CHAMADAS_ATE_100 = ["🤑 PERFUME BOM POR MENOS DE 100"]
