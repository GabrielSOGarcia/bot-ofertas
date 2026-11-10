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
# 10/11, Gabriel: "dá ênfase nos ORIGINAIS, tá pegando muita cópia". Ordem: 1º importado original (Azzaro,
# Invictus, Dior, Bleu de Chanel...), 2º original de qualquer marca (Natura, Boticário...), 3º árabes, 4º dupes
# pouco conhecidos e cheirosos, 5º por último as cópias/contratipos (ex.: "Salvo da Vida", cópia do Sauvage).
# Sempre com desconto bom. Foto de catálogo agora vale (FOTO_CATALOGO_OK): perfume original quase sempre só tem ela.
TEXTO_MODELO_IA = (
    "Modelo ideal: perfume ORIGINAL com desconto de verdade. A preferência é: 1º importado original de marca "
    "famosa, 2º original nacional (Natura, Boticário, Eudora...), 3º árabe original (Lattafa, Al Wataniah...), "
    "depois dupes e perfumes inspirados/contratipos (o nome deve dizer 'inspirado' quando for). "
    "Recuse: decant, amostra, réplica falsificada vendida como se fosse o original, foto gerada por inteligência "
    "artificial, e produto que não seja perfume, colônia ou body splash.\n")
FOTO_CATALOGO_OK = True       # 10/11: Idôle, La Vie Est Belle, Libre e Asad eram barrados só pela foto de catálogo
VENDAS_LOJA_COMUM_ML = 2000   # 10/11, Gabriel: loja comum (verde) vale a partir de +2 mil vendas (era 5 mil)

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
    "tarde": ["💎 Tarde perfumada: 1 Million, Invictus, Le Male, árabes... confere os que baixaram de preço hoje.",
              "🎁 Perfume é presente que nunca erra: olha as promoções de hoje e já garante o seu (ou o de alguém)."],
    "noite": ["🌙 Noite de promoção: os perfumes mais desejados com desconto, antes que o preço volte.",
              "😍 Fixação que todo mundo elogia, pagando bem menos: confere os perfumes de hoje aqui no grupo."],
}
# 09/11 17h, Gabriel: "diminui o tempo do perfume: mínimo 6, máximo 12" (cada post sai entre 6 e 12 min depois
# do anterior). Das 8h à meia-noite isso dá uns 100 posts, então o máximo do dia sobe para 100.
WHATSAPP_INTERVALO = 6
WHATSAPP_INTERVALO_MAX = 12
WHATSAPP_MAX_DIA = 100
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
    # 1º OS FAMOSOS (09/11 19h: primeiro as buscas que EXISTEM na vitrine de afiliados; as outras voltam vazias)
    ("famoso masculino", ["perfume importado masculino", "perfume masculino", "1 million", "invictus",
                          "rabanne masculino", "armani code", "armani", "jean paul gaultier masculino", "le male",
                          "calvin klein masculino", "ck be", "perfume masculino eau de parfum",
                          "sauvage eau de parfum", "sauvage dior", "ultra male", "le male elixir",
                          "eros versace", "stronger with you", "acqua di gio profumo",
                          "the most wanted azzaro", "azzaro wanted", "y yves saint laurent", "boss bottled",
                          "212 vip men", "bleu de chanel", "phantom rabanne"]),
    ("♀ famoso feminino", ["good girl carolina herrera", "very good girl", "212 vip rosé", "carolina herrera feminino",
                           "la vie est belle", "idôle lancôme", "olympea", "lady million", "fame rabanne",
                           "libre yves saint laurent", "scandal jean paul gaultier", "my way armani",
                           "j'adore dior", "miss dior", "coco mademoiselle", "born in roma", "eternity calvin klein",
                           "lancôme feminino", "jean paul gaultier feminino"]),
    # (09/11: a vitrine de afiliados NÃO tem Dior, Chanel, Carolina Herrera, Versace, Azzaro, YSL... essas buscas
    # voltam vazias e o bot passa para a próxima; ficam na lista caso a vitrine passe a ter. 10/11: Gabriel pediu
    # para manter Dior, Chanel, Prada, Carolina Herrera e Polo, porque às vezes a vitrine traz)
    ("famoso masculino", ["prada masculino", "polo ralph lauren", "carolina herrera masculino"]),
    # 2º ORIGINAIS NACIONAIS (qualquer marca original)
    ("perfume nacional masculino", ["malbec", "kaiak", "natura homem", "quasar", "zaad", "egeo masculino",
                                    "essencial masculino", "uomini", "boticário masculino", "eudora masculino",
                                    "hinode masculino", "clash boticário", "kaiak k max"]),
    ("♀ perfume nacional feminino", ["natura una", "essencial feminino", "lily boticário", "floratta",
                                     "egeo feminino", "glamour boticário", "ilía natura", "kriska",
                                     "boticário feminino", "eudora feminino"]),
    # 3º ÁRABES (originais das marcas árabes)
    ("árabe masculino", ["perfume asad", "club de nuit intense", "khamrah", "fakhar black",
                         "maison alhambra masculino", "al wataniah masculino", "perfume árabe masculino",
                         "lattafa masculino", "afnan 9pm"]),
    ("♀ árabe feminino", ["yara lattafa", "sabah al ward", "durrat al aroos", "fakhar rose",
                          "maison alhambra feminino", "perfume árabe feminino", "lattafa feminino"]),
    # 4º DUPES pouco conhecidos e cheirosos (ex.: Shockwave, que o Gabriel gosta)
    # (10/11: a vitrine ainda não tem Shockwave; a busca volta vazia e o bot passa para a próxima. Pôr aqui os
    # nomes que o Gabriel lembrar: o título do anúncio precisa ter as palavras da busca)
    ("dupe masculino", ["shockwave"]),
    # 5º POR ÚLTIMO as cópias/contratipos (ex.: "Salvo da Vida", cópia do Sauvage)
    ("cópia masculino", ["perfume inspirado masculino", "contratipo masculino", "salvo da vida"]),
    ("♀ cópia feminino", ["perfume inspirado feminino", "contratipo feminino"]),
    ("♀ body splash", ["body splash", "body splash victoria's secret", "body splash wepink"]),
]
# As duas entradas "famoso masculino" viram uma só (o dicionário PALAVRAS juntaria pela chave e perderia a 1ª)
_juntas = {}
for _c, _bs in PERFUMES:
    _juntas.setdefault(_c, []).extend(b for b in _bs if b not in _juntas.get(_c, []))
PERFUMES = list(_juntas.items())
PALAVRAS = {c: bs for c, bs in PERFUMES}
# 09/11 19h, Gabriel: "tá postando muito perfume feminino... ênfase no perfume MASCULINO IMPORTADO, preço muito
# bom, comissão muito boa". Sem alternar ♀/♂: o peso decide. Importado masculino 6 vezes por volta, dupe masculino
# 3, nacional masculino 2, os femininos 1 (uns 3 masculinos para cada feminino)
# 10/11, Gabriel: ORIGINAIS primeiro. Por volta do rodízio: importado masculino 6, importado feminino 2,
# nacional masculino 3, nacional feminino 1, árabe masculino 2, árabe feminino 1, dupe 1, cópias 1 cada e
# body splash 1. As cópias ficam com ~1 a cada 18 posts (antes os dupes/árabes eram 3 de cada 15)
for _c, _p in [("famoso masculino", 6), ("♀ famoso feminino", 2),
               ("perfume nacional masculino", 3), ("♀ perfume nacional feminino", 1),
               ("árabe masculino", 2), ("♀ árabe feminino", 1),
               ("dupe masculino", 1), ("cópia masculino", 1), ("♀ cópia feminino", 1),
               ("♀ body splash", 1)]:
    PESO_CATEGORIA[_c] = _p
# 10/11 17h, Gabriel: "dá mais ênfase pro masculino agora... primeiro os originalzão, bruto; depois vai do mais
# pop e regredindo". Sai do perfume: ♀ cópia feminino e ♀ body splash. Feminino só os originais (famoso,
# nacional e árabe), peso 1. O masculino segue a ordem: importado 6 > nacional 3 > árabe 2 > dupe 1 > cópia 1
for _k in ["♀ cópia feminino", "♀ body splash"]:
    PALAVRAS.pop(_k, None)
    PERFUMES = [(c, bs) for c, bs in PERFUMES if c != _k]
PESO_CATEGORIA["♀ famoso feminino"] = 1
CATEGORIA_SEM_REPETIR = 1   # com 7 categorias, a regra dos 40 posts virava revezamento e ignorava o peso
FILTROS_ML = ["best_seller", "extra_commission"]   # cada busca traz também os mais vendidos e os de ganhos extras
# "Caro" (1 a cada poucos posts): os de luxo, além dos famosos que já estão na lista normal
# 10/11, Gabriel: "arruma os caros". A lista antiga (Bleu de Chanel Parfum, Aventus Creed, Tom Ford, Dior Homme,
# Chanel nº5, Black Opium...) NÃO existe na vitrine de afiliados: a busca voltava vazia ou com qualquer coisa
# (178 achados, 151 "não combina com a busca"). Testado na vitrine (com Mais vendidos e Ganhos extras): o que
# traz importado original acima de R$ 250 é a MARCA como está no título + gênero, ou "eau de parfum masculino".
# Ex.: 1 Million, Invictus Victory, Phantom, Le Male Elixir, The Scent Magnetic, The Most Wanted, Eros, Good Girl,
# Scandal, Idôle, La Vie Est Belle, Light Blue, Libre Intense, Eternity. (armani/1 million já estão nos famosos)
IMPORTADOS = [
    ("luxo masculino", ["rabanne masculino", "jean paul gaultier masculino", "hugo boss", "azzaro",
                        "versace", "carolina herrera masculino", "eau de parfum masculino",
                        "eau de toilette masculino", "bleu de chanel", "perfume dior", "yves saint laurent",
                        "armani masculino", "le male", "bvlgari masculino"]),
    # (10/11 17h: masculino primeiro; o feminino caro ficou só com os 3 mais populares)
    ("♀ luxo feminino", ["carolina herrera feminino", "lancome feminino", "perfume chanel"]),
]
CAROS = [b for _, bs in IMPORTADOS for b in bs]
ALTERNAR_FEMININO = False   # 09/11 19h: o masculino tem prioridade (ver PESO_CATEGORIA)

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
CHAMADAS_GERAIS = ["🔥 ACHADO DO DIA", "👃 PERFUME DE GRIFE GASTANDO POUCO", "😍 FIXAÇÃO QUE TODO MUNDO ELOGIA",
                   "😱 ESSE PREÇO NÃO DURA", "🛒 QUEM VIU, LEVOU", "🎁 PRESENTE QUE ACERTA"]
CHAMADAS_POR_TIPO = [
    (["árabe", "lattafa", "asad", "khamrah", "yara", "fakhar", "club de nuit", "alhambra", "wataniah",
      "sabah al ward", "durrat"], ["🕌 PERFUME ÁRABE QUE ESTOURA", "🔥 O ÁRABE QUEM TODO MUNDO QUER"]),
    (["body splash"], ["🌸 CHEIRINHO O DIA INTEIRO"]),
]
CHAMADAS_CARO = ["💎 IMPORTADO ORIGINAL COM DESCONTO", "😮 IMPORTADO NESSE PREÇO NÃO É TODO DIA",
                 "🏆 PERFUME DE GRIFE EM PROMOÇÃO"]
CHAMADAS_ATE_100 = ["🤑 PERFUME BOM POR MENOS DE 100"]
