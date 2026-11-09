# Bot "Perfumes" (09/11): grupo de perfume do MERCADO LIVRE, masculino e feminino alternando (um ♀, um ♂).
# Combinado com o Gabriel: 1 grupo só no começo (perfume se compra muito de presente; os grupos de referência
# misturam); separar quando passar de ~500-1000 pessoas. Só perfume original de marca, com desconto de verdade.
# Os produtos e o link vêm da vitrine da Central de Afiliados do Mercado Livre (mercadolivre.py), com a sessão
# do Gabriel (ml_cookies.txt ao lado do config.txt).

LOJA = "mercadolivre"
CHAVE_CANAL = "CANAL_PERFUME"   # só se um dia postar no Telegram; hoje é só WhatsApp
NICHO_IA = ("perfumes ORIGINAIS de marca, masculinos e femininos, do Mercado Livre (importados, árabes e "
            "nacionais como Natura e Boticário). Recuse decant, amostra, perfume 'inspirado', contratipo ou réplica")

# ---------- Critérios ----------
EXIGIR_MARCA_SEMPRE = True
DESCONTO_MINIMO = 15          # perfume com desconto de verdade (Natura a preço cheio não vai)
VENDAS_MINIMAS = 500          # o Mercado Livre mostra "+500", "+1000", "+5mil"...
VENDAS_MINIMAS_CARO = 50      # importado caro vende menos
NOTA_MINIMA = 4.5
NOTA_MINIMA_CARO = 4.6
COPIAR_OFERTAS = 0            # a cópia dos outros grupos é de link da Shopee
GRUPOS = []                   # mensagem dos grupos: entra quando o grupo de perfume existir
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

BLOQUEADAS = BLOQUEADAS + [
    "inspirado", "inspirada", "inspirados", "inspired", "inspiração", "contratipo", "réplica", "replica",
    "decant", "amostra", "amostras", "tester", "primeira linha", "1ª linha", "similar", "versão de",
]

# ---------- O que buscar (substitui a lista do Casa inteira) ----------
# Categorias "♀" = vez do feminino; as outras = vez do masculino (ALTERNAR_FEMININO)
PERFUMES = [
    ("perfume árabe masculino", ["perfume árabe masculino", "lattafa masculino", "perfume asad", "khamrah",
                                 "club de nuit", "fakhar black", "maison alhambra", "al wataniah masculino"]),
    ("perfume nacional masculino", ["malbec", "kaiak", "natura homem", "quasar", "zaad", "egeo masculino",
                                    "essencial masculino", "uomini", "boticário masculino"]),
    ("♀ perfume árabe feminino", ["perfume árabe feminino", "yara lattafa", "sabah al ward", "durrat al aroos",
                                  "lattafa feminino", "fakhar rose", "maison alhambra feminino"]),
    ("♀ perfume nacional feminino", ["natura una", "essencial feminino", "lily boticário", "floratta",
                                     "egeo feminino", "glamour boticário", "ilía natura", "kriska",
                                     "boticário feminino"]),
    ("♀ body splash", ["body splash", "body splash victoria's secret", "body splash wepink"]),
]
PALAVRAS = {c: bs for c, bs in PERFUMES}
# Importados: a vez do "caro" (1 a cada poucos posts)
IMPORTADOS = [
    ("perfume importado masculino", ["1 million", "invictus", "sauvage", "bleu de chanel", "212 vip men",
                                     "eros versace", "acqua di gio", "le male", "polo ralph lauren",
                                     "hugo boss masculino", "azzaro", "phantom", "stronger with you", "ck one"]),
    ("♀ perfume importado feminino", ["good girl", "la vie est belle", "212 vip rosé", "olympea", "j'adore",
                                      "coco mademoiselle", "idôle", "my way", "scandal", "lady million", "fame"]),
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
