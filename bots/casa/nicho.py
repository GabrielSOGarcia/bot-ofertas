# Bot "Achadinhos de Casa" (Shopee). Usa as listas e ajustes do postar_shopee.py como estão:
# este é o bot original, então aqui só fica o que é dele.
CHAVE_CANAL = "CANAL"   # canal do Telegram: linha CANAL=... do config.txt

# ---------- 07/11: capa de sofá e sabonete de marca com mais vez ----------
# Gabriel (depois da opinião da mãe, que já vendeu por link: "tem que ser coisa com diferencial, de qualidade"):
# "sabonete... capa de sofá também é bom, pode encher". Cada linha é uma CATEGORIA própria do rodízio
# (tem a vez dela em toda volta); antes a capa de sofá era 1 busca dentro de "sofá e poltrona".
CASA_MAIS = [
    ("capa de sofá", ["capa de sofá", "capa de sofá retrátil", "capa de sofá elástica", "capa de sofá impermeável",
                      "capa de sofá 3 lugares", "capa de sofá de canto", "capa de sofá 2 lugares"]),
    ("protetor e manta de sofá", ["protetor de sofá", "protetor de sofá impermeável", "manta para sofá"]),
    ("sabonete de marca", ["sabonete granado", "sabonete phebo", "kit sabonetes granado", "sabonete ekos",
                           "sabonete líquido natura", "sabonete tododia", "sabonete boticário", "kit sabonete natura"]),
    # 08/11: a tia pediu "ventilador de teto que vem com a lâmpada embutida" (e comprou 3 duchas pelo link)
    ("ventilador de teto", ["ventilador de teto", "ventilador de teto com luminária", "ventilador de teto com lâmpada",
                            "ventilador de teto com controle remoto", "ventilador de teto led", "ventilador de teto 3 pás"]),
    # 08/11: prints do Gabriel da vitrine de afiliado (comissão extra, 13% a 33%, milhares de vendas)
    ("manta e almofada para sofá", ["kit manta e capas de almofada", "manta decorativa para sofá",
                                    "kit capas de almofada", "almofada decorativa"]),
    ("potes herméticos", ["potes herméticos", "jogo de potes herméticos", "potes de vidro hermético",
                          "kit potes herméticos acrílico"]),
    ("cobre leito e peseira", ["kit cobre leito casal", "cobre leito queen", "peseira para cama", "kit peseira"]),
    ("cozinha prática", ["cozedor de ovos elétrico", "nicho porta tempero", "kit utensílios de silicone",
                         "forma de gelo de silicone", "bomba elétrica para galão", "cesto de roupa suja"]),
    ("quintal e jardim", ["mangueira mágica", "mangueira expansível", "tela de sombreamento"]),
    # 08/11: posts de referência que o Gabriel mandou (8 mil curtidas): cozinha e lavanderia organizadas
    ("galheteiro e porta detergente", ["galheteiro de vidro", "kit galheteiro azeite e vinagre", "galheteiro",
                                       "dispenser de detergente com suporte para esponja", "porta detergente com esponja",
                                       "porta detergente e esponja"]),
    ("porta pão e boleira", ["porta pão com tampa", "porta pão de acrílico", "porta pão de bambu",
                             "boleira com tampa", "boleira de vidro com cúpula", "boleira com cúpula"]),
    ("potes e temperos de vidro", ["potes de vidro com tampa de bambu", "kit potes de vidro tampa de bambu",
                                   "porta temperos de vidro com colher", "kit porta temperos com colher de bambu",
                                   "porta condimentos de vidro"]),
    ("pano de prato", ["kit pano de prato", "pano de prato de algodão", "kit panos de prato xadrez",
                       "pano de prato atoalhado"]),
    ("lavanderia organizada", ["dispenser de sabão em pó", "dispenser de amaciante", "kit potes para lavanderia",
                               "porta sabão líquido com dosador", "pote para sabão em pó com tampa"]),
    # 08/11: mercado em promoção de verdade ("azeite de 50 por 30"), só marca boa
    # (a marca vem no fim do título: busca genérica + "azeite + marca" que o bot monta sozinho pela marca forte)
    ("azeite e vinagre de marca", ["azeite extra virgem", "azeite de oliva", "azeite português", "azeite trufado",
                                   "vinagre balsâmico", "vinagre balsâmico de modena", "kit azeite"]),
    ("limpeza em galão", ["detergente 5l", "sabão líquido 5l", "amaciante 5l", "desinfetante 5l",
                          "lava roupas 5l"]),
    ("bucha e esponja em pacote", ["kit esponja de cozinha", "esponja scotch-brite", "kit esponjas de cozinha",
                                   "esponja mágica", "kit esponja mágica", "bucha multiuso", "esponja dupla face"]),
]
def _sem_acento(t):
    return " ".join(unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower().split())
for _cat, _buscas in CASA_MAIS:
    PALAVRAS[_cat] = _buscas
    TIPOS_PROPRIOS = TIPOS_PROPRIOS + _buscas
PALAVRAS = {c: (l if c in dict(CASA_MAIS) else [p for p in l if p not in {b for _, bs in CASA_MAIS for b in bs}])
            for c, l in PALAVRAS.items()}   # tira a busca repetida da lista antiga ("capa de sofá" estava em "sala")
CATEGORIAS_EXTRA = [(c, [_sem_acento(b) for b in bs]) for c, bs in CASA_MAIS] + CATEGORIAS_EXTRA
# Peso: são ~300 categorias, então 1 vez por volta seria 1 capa de sofá a cada 4 ou 5 dias. Com peso 3 ela tem
# 3 vezes a vez em cada volta (e nunca repete nos últimos 40 posts)
PESO_CATEGORIA = {"capa de sofá": 3, "protetor e manta de sofá": 2, "sabonete de marca": 3, "ventilador de teto": 3,
                  "manta e almofada para sofá": 2, "potes herméticos": 2, "cobre leito e peseira": 2,
                  "cozinha prática": 2,
                  # 08/11: as primeiras vendas (07/11): ducha higiênica 3x, garrafa térmica, jogo americano e
                  # suporte de notebook. O bot também aprende sozinho com o relatório (ver "Aprende com as vendas")
                  "chuveiro e ducha": 2, "garrafa térmica": 2, "mesa posta": 2, "escritório": 2,
                  # 08/11: posts de referência e mercado em promoção
                  "galheteiro e porta detergente": 2, "porta pão e boleira": 2, "potes e temperos de vidro": 2,
                  "pano de prato": 2, "lavanderia organizada": 2, "azeite e vinagre de marca": 2,
                  "limpeza em galão": 2, "bucha e esponja em pacote": 2}
# Azeite e vinagre: só marca boa (como a panela só Tramontina). Galheteiro e porta azeite não precisam de marca
MARCAS_POR_TIPO = MARCAS_POR_TIPO + [
    (["azeite", "azeite extra virgem", "azeite de oliva", "azeite português", "azeite trufado",
      "vinagre balsâmico", "kit azeite"],
     ["Gallo", "Andorinha", "Borges", "Carbonell", "La Española", "Oliveira da Serra", "Cardeal", "Figueira da Foz",
      "Serrata", "Olivas do Sul", "Filippo Berio", "Colavita", "Cocinero", "Carrefour", "Castelo", "De Nigris",
      "Mazzetti", "Toscano", "Paganini", "Nova Oliva", "Vale Fértil", "Pietro Coricelli", "Monini", "De Cecco"]),
]
MARCAS = MARCAS + ["Gallo", "Andorinha", "Borges", "Carbonell", "La Española", "Oliveira da Serra", "Figueira da Foz",
                   "Serrata", "Olivas do Sul", "Filippo Berio", "Colavita", "Carrefour", "De Nigris", "Mazzetti",
                   "Toscano", "Paganini", "Nova Oliva", "Pietro Coricelli", "Monini", "Scotch-Brite", "Ypê", "Limpol"]
MARCA_OPCIONAL = MARCA_OPCIONAL + ["galheteiro", "porta azeite", "borrifador de azeite", "spray de azeite",
                                   "porta detergente", "dispenser de detergente", "porta pão", "boleira",
                                   "pano de prato", "esponja mágica", "bucha multiuso", "porta temperos",
                                   "porta condimentos", "dispenser de sabão", "dispenser de amaciante",
                                   "porta sabão líquido"]
# Mercado só com promoção de verdade: azeite/vinagre 25%+ de desconto, limpeza em galão 20%+ (o resto 10%)
DESCONTO_MINIMO_TIPO = [(["azeite", "vinagre balsâmico", "kit azeite"], 25),
                        (["detergente 5", "sabão líquido 5", "amaciante 5", "desinfetante 5", "lava roupas 5"], 20)]
MARCAS = MARCAS + ["Volare", "Spirit", "Fan Bello"] + ["Granado", "Phebo", "Natura", "O Boticário", "Boticário", "Avon", "Eudora", "Tododia", "Ekos"]
