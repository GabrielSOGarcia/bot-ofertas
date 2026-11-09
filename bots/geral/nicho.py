# Bot "Achadinhos & Promoções" (geral), criado em 06/11 a partir do bots/_modelo.
# Combinado com o Gabriel: de tudo um pouco + os melhores achados de casa; critérios mais leves que o Casa
# (marca não é obrigatória abaixo de R$ 200, 500+ vendas); mesmo chip do WhatsApp, grupo próprio, 90 por dia.
# 06/11 noite: lista expandida (~700 buscas) com foco no público FEMININO: 55% das categorias são de
# mulher (beleza, maquiagem, cabelo, moda, calçados, bolsas, lingerie, acessórios, fitness, bebê, casa/decoração)
# e 45% o resto (celular, eletrônicos, games, moda masculina, esporte, carro, ferramentas, pet, papelaria).
# O rodízio sorteia por CATEGORIA, então a proporção de categorias é a proporção dos posts.
# Chaves "f_" = público feminino (conta nos 55%); as outras = masculino/geral. O que não está aqui fica igual ao Casa.

CHAVE_CANAL = "CANAL_GERAL"   # só se um dia postar no Telegram (TELEGRAM_POSTAR=1); hoje é só WhatsApp
NICHO_IA = ("achadinhos e promoções da Shopee (público principal: mulheres; também casa, celular, eletrônicos, "
            "moda, esporte, bebê, pet)")

# ---------- Critérios mais leves (Gabriel, 06/11) ----------
EXIGIR_MARCA_SEMPRE = False   # abaixo de R$ 200 pode sem marca (de R$ 200 para cima continua com marca)
VENDAS_MINIMAS = 1000         # 08/11, Gabriel: "copia o algoritmo do Casa" (era 500 e saía coisa nada a ver)
WHATSAPP_MAX_DIA = 90

TEXTO_MODELO_IA = (
    "Modelo ideal: produto útil e bem avaliado, com desconto de verdade, de preferência de marca conhecida, "
    "e foto REAL do produto (foto de produto de verdade ou de um ambiente real; foto de modelo vestindo a "
    "roupa pode). Recuse foto gerada por inteligência artificial ou render artificial, e recuse produto "
    "estranho ou que não seja do tipo buscado. Recuse também: foto sensual ou vulgar (lingerie só em foto "
    "de catálogo, sem pose sensual), peça de reposição (borracha, válvula, resistência, placa), refil vendido "
    "sozinho, produto usado, seminovo, recondicionado, réplica ou falsificado, controle remoto pirata/universal e "
    "TV box, emagrecedor ou promessa milagrosa de saúde. Suplemento de academia (whey, creatina) e vitamina PODEM. Fone, carregador, cabo, capinha e película PODEM (são produtos do canal), desde que sejam produto "
    "de verdade e não peça de outro aparelho.\n")

# ---------- Lista de produtos (substitui a do Casa inteira) ----------
PALAVRAS = {
    # ===================== PÚBLICO FEMININO (f_) =====================
    "f_maquiagem": [
        "base líquida", "base matte", "base boca rosa", "corretivo", "corretivo líquido", "pó compacto", "pó solto",
        "blush", "blush em bastão", "bronzer", "contorno em bastão", "iluminador", "primer facial",
        "fixador de maquiagem", "bruma fixadora", "paleta de sombras", "paleta de sombras nude",
        "paleta mari maria", "delineador", "delineador em gel", "máscara de cílios", "máscara de cílios maybelline",
        "cílios postiços", "cílios magnéticos", "curvex", "henna para sobrancelha", "gel para sobrancelha",
        "batom", "batom matte", "batom líquido", "batom ruby rose", "gloss labial", "lip tint", "lip oil",
        "kit maquiagem", "kit maquiagem completo", "kit vult", "pincel de maquiagem", "kit pincéis de maquiagem",
        "esponja de maquiagem", "removedor de maquiagem", "demaquilante bifásico", "espelho de maquiagem com luz",
        "necessaire", "necessaire de maquiagem", "maleta de maquiagem", "organizador de maquiagem",
    ],
    "f_pele": [
        "protetor solar facial", "protetor solar com cor", "protetor solar corporal", "hidratante facial",
        "sérum facial", "vitamina c facial", "ácido hialurônico", "niacinamida", "retinol", "sabonete facial",
        "água micelar", "tônico facial", "esfoliante facial", "máscara facial", "máscara de argila",
        "patch para olheiras", "creme para olheiras", "creme anti idade", "kit skincare", "rolo de jade",
        "gua sha", "escova de limpeza facial", "hidratante corporal", "loção hidratante", "óleo corporal",
        "creme para mãos", "creme para os pés", "esfoliante corporal", "manteiga corporal", "sabonete íntimo",
        "hidratante labial", "protetor labial", "autobronzeador", "bronzeador", "desodorante feminino",
        "hidratante wepink", "kit wepink",
    ],
    "f_cabelo": [
        "shampoo", "condicionador", "máscara capilar", "máscara de hidratação capilar", "óleo capilar",
        "leave in", "creme para pentear", "kit cronograma capilar", "kit shampoo e condicionador", "ampola capilar",
        "reparador de pontas", "protetor térmico", "shampoo a seco", "tônico capilar", "gelatina capilar",
        "mousse para cachos", "kit cachos", "tinta de cabelo", "matizador", "kit siàge", "kit truss",
        "chapinha", "prancha de cabelo", "secador de cabelo", "escova secadora", "escova rotativa",
        "modelador de cachos", "difusor de cabelo", "escova de cabelo", "escova raquete", "presilha de cabelo",
        "piranha de cabelo", "scrunchie", "tiara", "touca de cetim", "fronha de cetim", "modelador sem calor",
    ],
    "f_perfume": [
        "perfume feminino", "perfume feminino importado", "perfume árabe feminino", "body splash",
        "body splash wepink", "perfume wepink", "kit body splash", "body mist", "colônia feminina",
        "perfume natura", "perfume boticário", "perfume capilar", "kit perfume feminino", "hidratante perfumado",
    ],
    "f_unhas": [
        "esmalte", "kit esmaltes", "esmalte em gel", "cabine uv para unhas", "kit unha de gel", "unha postiça",
        "kit manicure", "alicate de cutícula", "lixa de unha", "base fortalecedora", "removedor de esmalte",
        "polygel", "adesivo de unha",
    ],
    "f_moda": [
        "vestido", "vestido midi", "vestido longo", "vestido de festa", "vestido canelado", "blusa feminina",
        "cropped", "body feminino", "camiseta feminina", "regata feminina", "blazer feminino", "cardigan",
        "suéter feminino", "calça feminina", "calça wide leg", "calça jeans feminina", "calça pantalona",
        "short jeans feminino", "saia midi", "saia longa", "macacão feminino", "conjunto feminino",
        "conjunto de linho", "pijama feminino", "camisola", "robe", "moletom feminino", "jaqueta feminina",
        "jaqueta jeans feminina", "biquíni", "maiô", "saída de praia", "kimono",
    ],
    "f_intima": [
        "calcinha", "kit calcinhas", "calcinha de algodão", "calcinha lupo", "calcinha sem costura", "sutiã", "sutiã sem bojo",
        "sutiã com bojo", "sutiã sem aro", "top sem costura", "meia calça",
    ],
    "f_calcados": [
        "sandália feminina", "sandália rasteira", "sandália de salto", "sandália plataforma", "papete", "tamanco",
        "mule feminino", "salto alto", "scarpin", "sapatilha", "bota feminina", "bota cano curto",
        "coturno feminino", "tênis feminino", "tênis casual feminino", "tênis plataforma", "tênis branco feminino",
        "chinelo feminino", "chinelo nuvem", "slide feminino", "havaianas", "crocs",
    ],
    "f_bolsas": [
        "bolsa feminina", "bolsa transversal", "bolsa tiracolo", "bolsa de ombro", "bolsa tote", "bolsa baú",
        "bolsa de mão", "clutch", "bolsa de praia", "mochila feminina", "carteira feminina", "porta cartão",
        "pochete feminina",
    ],
    "f_acessorios": [
        "brinco", "kit brincos", "brinco de argola", "colar feminino", "colar com pingente", "pulseira feminina",
        "anel feminino", "kit semijoias", "porta joias", "relógio feminino", "óculos de sol feminino",
        "cinto feminino", "chapéu de praia", "smartwatch feminino",
    ],
    "f_fitness": [
        "legging", "legging fitness", "short fitness", "conjunto fitness", "top fitness", "macaquinho fitness",
        "garrafa de água motivacional", "tapete de yoga", "mini band", "bola de pilates", "tênis de academia feminino",
    ],
    "f_casa_decor": [
        "vela aromática", "difusor de aromas", "home spray", "almofada decorativa", "manta para sofá",
        "tapete felpudo", "quadro decorativo", "vaso decorativo", "planta artificial", "espelho redondo",
        "luminária", "fita led", "jogo de lençol", "edredom", "travesseiro", "kit cama", "toalha de banho",
        "roupão", "tapete de banheiro", "kit banheiro", "cabide aveludado", "caixa organizadora",
        "organizador de bolsas", "organizador de gaveta", "sapateira", "arara de roupas",
    ],
    "f_cozinha": [
        "air fryer", "panela elétrica de arroz", "jogo de panelas", "panela antiaderente", "liquidificador portátil",
        "mixer de mão", "garrafa térmica", "copo térmico stanley", "pote hermético", "kit potes de vidro",
        "organizador de geladeira", "porta temperos giratório", "triturador manual de puxar",
        "caneca mixer automática", "espumador de leite", "cafeteira", "cafeteira de cápsula", "sanduicheira",
        "forno elétrico", "jogo de facas", "tábua de corte", "utensílios de silicone", "marmita elétrica",
        "pipoqueira", "chaleira elétrica", "balança de cozinha", "jogo americano", "aparelho de jantar",
        "jogo de copos", "taça de vinho",
    ],
    "f_limpeza": [
        "mop giratório", "mop spray", "aspirador vertical", "aspirador portátil", "vassoura mágica",
        "kit panos de microfibra", "escova elétrica de limpeza", "limpa vidros", "tira manchas", "sabão líquido",
        "amaciante", "lustra móveis", "dispenser de sabão em pó", "cesto de roupa", "varal de chão",
        "tábua de passar", "ferro de passar", "vaporizador de roupas", "lixeira automática",
        "aromatizador de ambiente", "rodo mágico",
    ],
    # ===================== MASCULINO E GERAL =====================
    "celular": [
        "capinha de celular", "capa iphone", "capa samsung", "capinha magsafe", "película de vidro",
        "película privacidade", "carregador turbo", "carregador iphone", "carregador samsung 25w",
        "carregador usb c", "carregador 3 em 1", "carregador por indução", "carregador magsafe",
        "carregador portátil", "power bank", "power bank magsafe", "cabo usb tipo c", "cabo lightning",
        "cabo para iphone", "fonte iphone 20w", "suporte de celular", "suporte veicular para celular",
        "suporte magnético para celular", "tripé para celular", "ring light", "pau de selfie", "gimbal",
        "airtag", "rastreador bluetooth", "popsocket", "cordão para celular",
    ],
    "som": [
        "fone de ouvido bluetooth", "fone bluetooth", "fone sem fio", "airpods", "fone jbl", "fone galaxy buds",
        "fone qcy", "fone de ouvido com fio", "fone de condução óssea", "headset gamer", "headphone",
        "headphone bluetooth", "caixa de som bluetooth", "caixa de som jbl", "caixinha de som portátil",
        "caixa de som à prova d'água", "microfone sem fio", "microfone de lapela", "karaokê",
    ],
    "relogio": [
        "smartwatch", "relógio inteligente", "apple watch", "pulseira para apple watch",
        "pulseira para smartwatch", "smart band", "mi band", "amazfit",
    ],
    "computador": [
        "mouse sem fio", "mouse gamer", "teclado sem fio", "teclado gamer", "teclado mecânico",
        "kit teclado e mouse", "mousepad gamer", "webcam", "hub usb c", "pen drive", "cartão de memória", "ssd",
        "hd externo", "memória ram", "roteador wifi", "repetidor wifi", "suporte para notebook",
        "mochila para notebook", "capa para notebook", "kindle", "capa para kindle", "capa para ipad",
        "caneta touch", "luminária led rgb", "mesa gamer",
    ],
    "games": [
        "controle de videogame", "controle ps5", "controle xbox", "controle para celular", "headset ps5",
        "jogo ps5", "carregador de controle", "suporte para controle",
    ],
    "smart": [
        "echo dot", "echo pop", "fire tv stick", "lâmpada inteligente", "tomada inteligente",
        "câmera de segurança wifi", "câmera ip", "projetor portátil", "mini projetor",
    ],
    "m_moda": [
        "camiseta masculina", "camiseta básica", "kit camisetas", "camisa polo", "camisa social",
        "bermuda masculina", "bermuda jeans", "calça jeans masculina", "calça jogger", "moletom masculino",
        "jaqueta masculina", "jaqueta corta vento", "cueca", "kit cuecas", "kit meias", "meia esportiva",
        "pijama masculino", "boné", "boné aba reta", "carteira masculina", "cinto masculino", "relógio masculino",
        "óculos de sol masculino", "corrente masculina", "perfume masculino", "perfume masculino importado",
        "perfume árabe masculino", "mochila masculina", "pochete masculina",
    ],
    "m_calcados": [
        "tênis masculino", "tênis casual masculino", "tênis de corrida", "tênis nike",
        "tênis puma", "tênis fila", "tênis olympikus", "tênis mizuno", "tênis asics", "tênis new balance",
        "chinelo masculino", "slide masculino", "sapatênis", "chuteira", "chuteira society",
    ],
    "m_barba": [
        "aparador de barba", "aparador de pelos", "barbeador elétrico", "máquina de cortar cabelo", "kit barba",
        "óleo para barba", "balm para barba", "pomada modeladora",
    ],
    "esporte": [
        "corda de pular", "faixa elástica", "kit elástico extensor", "halter", "kit halteres", "anilha",
        "barra de porta", "caneleira de peso", "roda abdominal", "luva de academia", "munhequeira",
        "coqueteleira", "garrafa squeeze academia", "bolsa de academia", "bola de futebol",
        "raquete de beach tennis", "bola de beach tennis", "bola de vôlei", "camisa de time",
        "capacete de bicicleta", "luz de bicicleta", "barraca de camping", "lanterna de cabeça",
    ],
    "carro": [
        "aspirador automotivo", "kit lavagem automotiva", "shampoo automotivo", "cera automotiva",
        "pretinho automotivo", "carregador veicular", "transmissor fm bluetooth", "câmera veicular", "câmera de ré",
        "som automotivo", "central multimídia", "tapete automotivo", "capa de banco automotivo",
        "organizador de porta malas", "aromatizador automotivo", "compressor de ar portátil", "calibrador de pneu",
        "macaco hidráulico", "lâmpada led automotiva", "para-sol para carro", "capacete", "capa de chuva para moto",
        "baú para moto", "luva para moto", "intercomunicador moto",
    ],
    "ferramentas": [
        "parafusadeira", "furadeira", "kit ferramentas", "jogo de chaves", "trena", "nível a laser", "alicate",
        "caixa de ferramentas", "lanterna tática", "lanterna recarregável", "kit brocas",
    ],
    "pet": [
        "ração para cachorro", "ração para gato", "petisco para cachorro", "ossinho para cachorro",
        "caminha para cachorro", "caminha para gato", "arranhador para gato", "comedouro", "comedouro elevado",
        "fonte para gato", "caixa de areia para gato", "areia para gato", "coleira", "peitoral para cachorro",
        "guia retrátil", "brinquedo para cachorro", "brinquedo para gato", "varinha para gato",
        "tapete higiênico", "caixa de transporte pet", "bolsa de transporte pet", "shampoo para cachorro",
        "escova para pet", "cortador de unha pet", "roupinha para cachorro", "casinha de cachorro",
        "tapete gelado pet", "bebedouro portátil pet",
    ],
    "papelaria": [
        "caderno", "caderno inteligente", "caderno universitário", "fichário", "planner", "agenda 2027",
        "kit canetas", "caneta gel", "marca texto", "post-it", "kit lettering", "washi tape", "calculadora",
        "organizador de mesa",   # 09/11: sem estojo, mochila escolar, lápis de cor, aquarela (coisa de criança)
    ],
    "m_mais": [   # 06/11 noite: Gabriel pediu 50/50 ("também existe homem nesse mundo")
        "regata masculina", "regata dry fit", "camiseta dry fit", "camiseta oversized masculina",
        "kit meias nike", "meia cano alto", "meia invisível masculina", "meia de compressão",
        "tênis esportivo masculino", "tênis para academia masculino", "tênis de basquete", "tênis de futsal",
        "bola de basquete", "bola de basquete wilson", "raquete de tênis", "raquete de tênis wilson",
        "bola de tênis", "tabela de basquete",
        "mochila de viagem", "mochila antifurto", "mochila impermeável", "mala de bordo masculina",
        "headphone sem fio", "fone esportivo", "fone com cancelamento de ruído", "fone gamer sem fio",
        "short de treino masculino", "bermuda tactel", "sunga", "short de praia masculino",
        "kit churrasco", "faca de churrasco", "copo térmico de cerveja", "cooler", "caixa térmica",
        "mouse gamer sem fio", "teclado gamer rgb", "headset gamer sem fio", "mousepad gamer rgb",
        "vara de pesca", "molinete", "carretilha de pesca", "kit pesca",
        "relógio digital masculino", "relógio esportivo", "relógio garmin",
    ],
    "geral_mais": [   # 06/11, Gabriel: "posta muitos suplementos... tecnologia, perfumes, gadgets de qualquer nicho"
        # suplementos (os outros grupos postam muito)
        "whey protein", "whey protein concentrado", "whey growth", "creatina", "creatina monohidratada",
        "pré treino", "bcaa", "glutamina", "hipercalórico", "barra de proteína", "pasta de amendoim",
        "ômega 3", "multivitamínico", "vitamina d", "magnésio",
        # tecnologia e gadgets de qualquer nicho
        "drone", "drone com câmera", "câmera de ação", "câmera instantânea", "mini impressora térmica",
        "projetor de galáxia", "luminária lua", "relógio despertador digital", "mini ventilador portátil",
        "game stick", "console retrô", "mini game portátil", "óculos de realidade virtual",
        "pilhas recarregáveis", "carregador de pilhas", "lâmpada com câmera", "tag rastreadora",
        "teclado dobrável", "smart ring", "balança de bioimpedância",
        # perfume e cuidados masculinos
        "perfume lattafa", "perfume asad", "perfume club de nuit", "perfume masculino árabe",
        "kit perfume masculino", "perfume malbec", "perfume kaiak", "perfume quasar", "body spray masculino",
        "desodorante masculino", "kit skincare masculino", "protetor solar masculino", "shampoo masculino",
        "sabonete masculino",
    ],
    "f_mais": [   # para manter perto de 50/50
        "colágeno", "colágeno verisol", "biotina", "vitamina para cabelo", "goma de vitamina",
        "copo stanley rosa", "garrafa com canudo", "garrafa térmica rosa", "capinha feminina", "case de airpods",
        "luminária fofa", "umidificador fofo",
    ],
    "viagem": [
                "mala de viagem", "mala de bordo", "kit malas", "organizador de mala", "necessaire de viagem",
        "travesseiro de pescoço", "balança de mala", "cadeado de mala", "bolsa de viagem",
    ],
}
CAROS = [
    # Celular e lançamentos
    "iphone", "iphone 15", "iphone 16", "iphone 17", "iphone pro max", "samsung galaxy s25", "samsung galaxy s24",
    "samsung galaxy a56", "samsung galaxy a36", "samsung galaxy z flip", "celular motorola", "motorola edge",
    "celular xiaomi", "redmi note", "apple watch series", "galaxy watch", "airpods pro", "galaxy buds",
    "jbl flip", "jbl charge", "jbl boombox", "jbl partybox",
    # Computador e games
    "macbook", "macbook air", "notebook", "notebook gamer", "notebook lenovo", "notebook dell", "ipad",
    "tablet samsung", "kindle paperwhite", "monitor gamer", "cadeira gamer", "playstation 5", "xbox series",
    "nintendo switch",
    # Casa grande
    "smart tv 43", "smart tv 50", "smart tv 55", "smart tv 58", "smart tv 60", "smart tv 65", "smart tv 4k", "soundbar", "geladeira frost free", "geladeira inverse",
    "geladeira duplex", "máquina de lavar", "lava e seca", "lava louças", "fogão 5 bocas", "micro-ondas",
    "air fryer oven", "robô aspirador", "aspirador vertical sem fio", "cafeteira expresso", "ar condicionado split",
    "cama box casal", "colchão casal", "sofá retrátil", "fechadura digital",
    # Beleza e moda (feminino)
    "perfume importado", "perfume árabe", "kit perfume importado", "secador de cabelo profissional",
    "escova rotativa profissional", "chapinha profissional", "bolsa de couro", "relógio feminino de marca",
    "tênis nike air", "tênis adidas", "relógio casio", "relógio technos",
    "perfume carolina herrera", "perfume lancôme", "perfume good girl", "bolsa arezzo", "sandália schutz",
    "kit maquiagem profissional", "secador taiff", "escova rotativa philco", "kit skincare la roche posay",
    "smartwatch feminino samsung", "relógio feminino michael kors", "sapatênis feminino de couro",
    # Esporte (09/11: sem os de bebê)
    "headphone sony", "smartwatch garmin", "tênis nike air max", "furadeira bosch", "parafusadeira makita",
    "bicicleta ergométrica", "esteira elétrica", "bicicleta aro 29", "patinete elétrico",
]

# ---------- Marcas (somam às do Casa) ----------
MARCAS = MARCAS + [
    # Celular, eletrônicos e games
    "Apple", "iPhone", "iPad", "MacBook", "AirPods", "Redmi", "Realme", "Poco", "Lenovo", "Asus", "Acer", "Dell",
    "Baseus", "Anker", "Ugreen", "Haylou", "QCY", "Edifier", "Logitech", "Redragon", "HyperX", "Havit",
    "Kingston", "SanDisk", "Mercusys", "Huawei", "Amazfit", "Nintendo", "PlayStation", "Xbox", "Pioneer",
    "Geonav", "Kindle", "Galaxy", "Jabra", "Sennheiser", "Microsoft", "Kodak", "GoPro", "DJI",
    # Beleza, maquiagem, cabelo e perfume
    "WePink", "We Pink", "Vult", "Ruby Rose", "Boca Rosa", "Mari Maria", "Bruna Tavares", "Dailus", "Dalla",
    "Maybelline", "Revlon", "Payot", "Natura", "O Boticário", "Boticário", "Eudora", "Siàge", "Avon",
    "L'Oréal", "Loreal", "Elseve", "Salon Line", "Lola", "Wella", "Pantene", "Tresemmé", "Truss", "Braé",
    "Amend", "Haskell", "Kérastase", "Inoar", "Skala", "Novex", "Neutrogena", "La Roche-Posay", "Cerave",
    "Bioré", "Principia", "Creamy", "Sallve", "Garnier", "Episol", "Isdin", "Vichy", "Eucerin", "Cetaphil",
    "Bioderma", "Tracta", "Adcos", "Remington", "Gillette", "Impala", "Risqué", "Max Love", "Macrilan",
    "Lattafa", "Al Wataniah", "Maison Alhambra", "Armaf", "Carolina Herrera", "Paco Rabanne", "Calvin Klein",
    "Victoria's Secret", "Lancôme", "Dior", "Chanel", "Azzaro", "Antonio Banderas", "Benetton",
    # Moda, calçados, lingerie e acessórios
    "Nike", "Adidas", "Puma", "Olympikus", "Mizuno", "Fila", "Havaianas", "Ipanema", "Grendha", "Melissa",
    "Crocs", "Under Armour", "Kappa", "Penalty", "Topper", "Asics", "New Balance", "Vans", "Converse",
    "Lupo", "Hope", "Liz", "Trifil", "Mormaii", "Speedo", "Oakley", "Ray-Ban", "Chilli Beans", "Samsonite",
    "Casio", "Technos", "Orient", "Mondaine", "Vivara", "Rommanel", "Arezzo", "Schutz", "Santa Lolla",
    "Moleca", "Beira Rio", "Vizzano", "Piccadilly", "Usaflex", "Dakota",
    # Pet
    "Pedigree", "Whiskas", "Golden", "Premier", "Royal Canin", "Special Dog", "GranPlus", "Chalesco",
    # Carro, moto e ferramentas
    "Wilson", "Garmin", "Jordan", "Spalding", "Head", "Babolat", "Shimano", "Marine Sports",
    "Michelin", "Vonixx", "Meguiar's", "Pro Tork", "Makita", "DeWalt", "Stanley", "Tramontina",
    # Papelaria
    "Faber-Castell", "BIC", "Tilibra", "Stabilo", "Pilot", "Compactor", "Jandaia", "Foroni",
]

# ---------- O que o Casa bloqueia e aqui é produto (pet, bebê, carregador, cabo, roupa íntima...) ----------
_LIBERADAS = {
    "coleira", "ração", "comedouro", "arranhador", "areia sanitária", "para cachorro", "para gato",
    "cachorro", "cachorros", "cães", "gato", "gatos", "pet shop", "para pet", "cama pet", "manta pet",
    "coberta pet", "roupa pet", "para bebê", "poltrona de alimentação", "cadeira de alimentação",
    "cadeira de refeição", "carregador", "adaptador", "cabo usb", "cabo p2", "fonte bivolt",
    "fonte de alimentação", "calcinha", "sutiã", "lingerie", "suplemento",
}
BLOQUEADAS = [b for b in BLOQUEADAS if b not in _LIBERADAS and b not in BLOQUEADAS_CASA] + [
    "seminovo", "semi novo", "recondicionado", "usado", "vitrine", "réplica", "primeira linha", "inspired",
    "inspiração", "contratipo", "termogênico", "inspirado", "inspirada", "inspirados",   # 08/11: perfume cópia "queima gordura", "seca barriga",
    # 08/11, Gabriel: "relógio pirateado, caixona de ouro, não gostei"
    "rolex", "patek", "hublot", "audemars", "richard mille", "cartier", "bvlgari", "estilo luxo",
]

# ---------- 09/11, Gabriel: NADA infantil no Geral ("sem brinquedo, sem canetinha, nada que é infantil...
# sabonete infantil, banheira, cadeirinha, mamadeira") ----------
INFANTIL = [
    "infantil", "infantis", "criança", "crianças", "bebê", "bebês", "bebe", "baby", "kids", "kid", "juvenil",
    "menino", "meninos", "menina", "meninas", "recém nascido", "recém-nascido", "newborn", "maternidade",
    "gestante", "amamentação", "brinquedo", "brinquedos", "boneca", "bonecas", "boneco", "bonecos", "reborn",
    "pelúcia", "lego", "blocos de montar", "massinha", "slime", "canetinha", "canetinhas", "hidrocor",
    "giz de cera", "escolar", "fralda", "fraldas", "lenço umedecido", "lenços umedecidos", "mamadeira",
    "chupeta", "mordedor", "chocalho", "babador", "naninha", "móbile", "berço", "cercadinho", "andador",
    "cadeirinha", "banheira", "carrinho de bebê", "bebê conforto", "trocador", "body bebê", "pomada para assaduras",
    "patrulha canina", "peppa", "turma da mônica", "galinha pintadinha", "mundo bita", "hot wheels", "barbie",
    "fisher-price", "fisher price", "frozen", "homem aranha",
]
BLOQUEADAS = BLOQUEADAS + INFANTIL
# O que tem a palavra mas não é de criança (brinquedo de pet, pantufa de pelúcia, Babyliss, baby doll...)
BLOQUEIO_EXCETO = {
    "brinquedo": ["cachorro", "gato", "pet", "cães", "caes"], "brinquedos": ["cachorro", "gato", "pet"],
    "mordedor": ["cachorro", "gato", "pet"], "baby": ["liss", "doll"], "pelúcia": ["chinelo", "pantufa", "manta",
    "cobertor", "almofada"], "banheira": ["cachorro", "gato", "pet"], "andador": ["idoso", "adulto"],
    "cadeirinha": ["praia", "cachorro", "pet"], "boneco": ["funko"], "bonecos": ["funko"],
}

# ---------- 08/11: relógio e calçado só de marca; sapato de homem em cor sóbria ----------
# Gabriel: "um sapato vermelho, feio pra caralho; um relógio pirateado... relógio coloca um pouquinho de marca,
# uns Casio, um trem mais ajeitadinho". Tipo de marca forte = só posta com uma dessas marcas (ver MARCAS_POR_TIPO)
_MARCAS_RELOGIO = ["Casio", "G-Shock", "Technos", "Orient", "Mondaine", "Champion", "Seiko", "Citizen", "Lince",
                   "Timex", "Fossil", "Michael Kors", "Tommy Hilfiger", "Lacoste", "Armani Exchange", "Tissot",
                   "Vivara", "Garmin", "Condor", "Allora", "Speedo", "Mormaii"]
_MARCAS_CALCADO = ["Nike", "Adidas", "Puma", "Olympikus", "Mizuno", "Fila", "Asics", "New Balance", "Vans",
                   "Converse", "Skechers", "Under Armour", "Kappa", "Penalty", "Topper", "Umbro", "Diadora",
                   "Rainha", "Moleca", "Beira Rio", "Vizzano", "Piccadilly", "Usaflex", "Dakota", "Modare",
                   "Ramarim", "Bottero", "Via Marte", "Azaleia", "Comfortflex", "Bebecê", "Arezzo", "Schutz",
                   "Santa Lolla", "Melissa", "Grendha", "Ipanema", "Havaianas", "Petite Jolie", "Mississipi",
                   "Democrata", "Ferracini", "Pegada", "West Coast", "Freeway", "Kildare", "Mormaii", "Kenner",
                   "Rider", "Cartago", "Crocs", "Bibi", "Klin", "Pampili", "Kidy", "Ortopé", "Molekinha", "Molekinho"]
MARCAS_POR_TIPO = MARCAS_POR_TIPO + [
    (["relógio masculino", "relógio feminino", "relógio digital", "relógio esportivo", "relógio casio",
      "relógio technos", "relógio feminino de marca", "relógio orient", "relógio mondaine"], _MARCAS_RELOGIO),
    (["tênis masculino", "tênis feminino", "tênis casual", "tênis de corrida", "tênis esportivo",
      "tênis para academia", "tênis de academia", "tênis de basquete", "tênis de futsal", "tênis plataforma",
      "tênis branco", "tênis infantil", "sapatênis", "sapato", "bota", "coturno", "sandália", "salto", "tamanco",
      "mule", "sapatilha", "mocassim", "scarpin", "papete", "chuteira"], _MARCAS_CALCADO),
]
MARCAS = MARCAS + [m for m in _MARCAS_RELOGIO + _MARCAS_CALCADO if m not in MARCAS]
PALAVRAS["m_moda"] = PALAVRAS["m_moda"] + ["relógio casio vintage", "relógio casio g-shock", "relógio orient",
                                           "relógio mondaine", "relógio technos masculino"]
COR_SOBRIA_EXTRA = ["sapato", "sapatênis", "mocassim", "tênis masculino",
                                       "tênis casual masculino", "bota masculina", "relógio masculino"]

# Tipos que precisam das 2 primeiras palavras (senão "brinquedo para cachorro" cairia junto do infantil)
TIPOS_PROPRIOS = TIPOS_PROPRIOS + [
    "brinquedo para cachorro", "brinquedo para gato", "shampoo para cachorro", "caminha para cachorro",
    "caminha para gato", "tapete higiênico", "tapete gelado pet", "tapete de yoga", "tapete de atividades",
    "tapete de eva", "tapete automotivo", "tapete felpudo", "tapete de banheiro", "capa de banco automotivo",
    "capa de celular", "capa iphone", "capa samsung", "capa para notebook", "capa para kindle", "capa para ipad",
    "capa de chuva para moto", "caixa de transporte pet", "caixa de areia", "caixa de som", "caixinha de som",
    "caixa de ferramentas", "caixa organizadora", "garrafa squeeze academia", "garrafa de água motivacional",
    "mochila infantil", "mochila escolar", "mochila para notebook", "mochila feminina", "mochila masculina",
    "lancheira infantil", "garrafinha infantil", "relógio inteligente", "relógio feminino", "relógio masculino",
    "suporte veicular", "suporte de celular", "suporte magnético para celular", "suporte para notebook",
    "suporte para controle", "aspirador automotivo", "carregador veicular", "carregador de controle",
    "carrinho de bebê", "bicicleta ergométrica", "lâmpada led automotiva", "luminária led rgb", "cadeira gamer",
    "cadeira de alimentação", "cadeirinha para carro", "protetor solar", "protetor térmico", "protetor labial",
    "escova para pet", "escova secadora", "escova de cabelo", "escova raquete", "escova rotativa",
    "escova de limpeza facial", "escova elétrica de limpeza", "máscara de cílios", "máscara capilar",
    "máscara de hidratação", "máscara facial", "máscara de argila", "kit maquiagem", "organizador de maquiagem",
    "organizador de mala", "organizador de porta malas", "organizador de bolsas", "organizador de gaveta",
    "organizador de geladeira", "organizador de mesa", "kit manicure", "kit body bebê", "kit higiene bebê",
    "kit shampoo", "kit halteres", "kit elástico", "kit canetas", "kit lavagem", "kit meias", "kit teclado",
    "kit cuecas", "kit camisetas", "kit calcinhas", "kit brincos", "kit semijoias", "kit esmaltes",
    "kit unha de gel", "kit cronograma", "kit cachos", "kit skincare", "kit pincéis", "kit body splash",
    "kit perfume", "kit wepink", "kit vult", "kit siàge", "kit truss", "kit barba", "kit ferramentas",
    "kit brocas", "kit pintura", "kit lettering", "kit malas", "kit potes", "kit panos", "kit cama",
    "kit banheiro", "kit berço", "fone jbl", "caixa de som jbl", "smart band", "blocos de montar",
    "body de bebê", "body splash", "body mist", "body feminino", "bola de pilates", "bolsa maternidade",
    "bolsa de academia", "bolsa de transporte pet", "bolsa de viagem", "bolsa de praia", "lenço umedecido",
    "hidratante labial", "hidratante wepink", "hidratante perfumado", "creme para pentear", "creme para olheiras",
    "creme anti idade", "creme para mãos", "creme para os pés", "óleo capilar", "óleo corporal", "óleo para barba",
    "sabonete íntimo", "sabonete facial", "perfume capilar", "perfume masculino", "perfume árabe masculino",
    "perfume feminino", "perfume árabe feminino", "shampoo a seco", "shampoo automotivo", "camisa de time",
    "camisa polo", "camisa social", "conjunto fitness", "conjunto infantil", "vestido infantil",
    "pijama infantil", "pijama masculino", "pijama feminino", "roupa infantil", "tênis infantil",
    "sandália infantil", "tênis de academia", "luva de academia", "luva para moto", "garrafa térmica",
    "cesto de roupa", "pote hermético", "lâmpada inteligente", "câmera veicular", "câmera de ré",
    "câmera de segurança", "câmera ip", "mini band", "mini projetor", "máquina de cortar cabelo",
    "porta joias", "porta cartão", "chinelo nuvem", "jogo de chaves", "jogo ps5", "jogo da memória",
    "lanterna tática", "lanterna recarregável", "lanterna de cabeça", "tapete de yoga", "faixa elástica",
    "aparador de barba", "aparador de pelos",
    # roupa e acessório com gênero no nome (senão "calça feminina" e "calça jogger" viram a mesma categoria)
    "calça feminina", "calça wide leg", "calça jeans feminina", "calça pantalona", "calça jeans masculina",
    "calça jogger", "camiseta feminina", "camiseta masculina", "camiseta básica", "carteira feminina",
    "carteira masculina", "chinelo feminino", "chinelo masculino", "cinto feminino", "cinto masculino",
    "conjunto feminino", "conjunto de linho", "jaqueta feminina", "jaqueta jeans feminina", "jaqueta masculina",
    "jaqueta corta vento", "macacão feminino", "macacão bebê", "meia calça", "meia esportiva", "moletom feminino",
    "moletom masculino", "pochete feminina", "pochete masculina", "short jeans feminino", "short fitness",
    "slide feminino", "slide masculino", "top sem costura", "top fitness", "tênis feminino",
    "tênis casual feminino", "tênis plataforma", "tênis branco feminino", "óculos de sol feminino",
    "óculos de sol masculino", "pulseira feminina", "smartwatch feminino", "alicate de cutícula",
    "pomada para assaduras", "pomada modeladora", "aromatizador de ambiente", "aromatizador automotivo",
    "travesseiro de pescoço", "jogo de lençol", "jogo americano", "jogo de facas", "porta temperos",
    "caneca mixer", "galaxy watch", "galaxy buds", "fone galaxy buds", "casinha de cachorro",
    "necessaire de viagem", "espelho redondo",
    "regata masculina", "regata dry fit", "camiseta dry fit", "camiseta oversized", "meia cano alto",
    "meia invisível", "meia de compressão", "tênis esportivo", "tênis para academia", "tênis de basquete",
    "tênis de futsal", "tênis de corrida", "bola de basquete", "raquete de tênis", "bola de tênis",
    "tabela de basquete", "mochila de viagem", "mochila antifurto", "mochila impermeável", "mala de bordo",
    "headphone sem fio", "fone esportivo", "fone com cancelamento", "fone gamer", "short de treino",
    "short de praia", "bermuda tactel", "copo térmico de cerveja", "caixa térmica", "kit churrasco",
    "faca de churrasco", "mouse gamer", "teclado gamer", "headset gamer", "mousepad gamer",
    "relógio digital", "relógio esportivo", "relógio garmin", "kit pesca", "vara de pesca",
    "whey protein", "barra de proteína", "pasta de amendoim", "pré treino", "vitamina d", "vitamina para cabelo",
    "goma de vitamina", "drone com câmera", "câmera de ação", "câmera instantânea", "mini impressora",
    "projetor de galáxia", "luminária lua", "relógio despertador", "mini ventilador", "game stick",
    "console retrô", "mini game", "óculos de realidade virtual", "carregador de pilhas", "lâmpada com câmera",
    "tag rastreadora", "teclado dobrável", "smart ring", "balança de bioimpedância", "perfume lattafa",
    "perfume asad", "perfume club de nuit", "perfume masculino árabe", "kit perfume masculino", "perfume malbec",
    "perfume kaiak", "perfume quasar", "body spray masculino", "desodorante masculino", "kit skincare masculino",
    "protetor solar masculino", "shampoo masculino", "sabonete masculino", "colágeno verisol",
    "copo stanley rosa", "garrafa com canudo", "garrafa térmica rosa", "capinha feminina", "case de airpods",
    "luminária fofa", "umidificador fofo",
]

# ---------- Rodízio: categorias do Geral (ganham das do Casa) ----------
# Os tipos vêm sem acento e no singular ("tênis" -> "teni", "óculos" -> "oculo", "cílios" -> "cilio").
# Categorias de mulher começam com "♀ " (o teste conta para os 55%).
CATEGORIAS_EXTRA = [
    # ---------- Feminino ----------
    ("♀ maquiagem: rosto", ["base", "corretivo", "po", "blush", "bronzer", "contorno", "iluminador", "primer",
                            "fixador", "bruma"]),
    ("♀ maquiagem: olhos", ["paleta", "delineador", "mascara de cilios", "cilio", "curvex", "henna", "gel"]),
    ("♀ maquiagem: boca", ["batom", "glos", "lip", "hidratante labial", "protetor labial"]),
    ("♀ maquiagem: kit e pincel", ["kit maquiagem", "pincel", "kit pinceis", "kit vult", "esponja", "removedor",
                                   "demaquilante"]),
    ("♀ necessaire e espelho", ["espelho", "necessaire", "maleta", "organizador de maquiagem"]),
    ("♀ skincare", ["protetor solar", "hidratante", "serum", "vitamina", "acido", "niacinamida", "retinol",
                    "sabonete facial", "agua", "tonico", "esfoliante", "mascara facial", "mascara de argila",
                    "patch", "creme para olheiras", "creme anti idade", "kit skincare", "rolo", "gua",
                    "escova de limpeza facial"]),
    ("♀ corpo", ["hidratante corporal", "locao", "oleo corporal", "creme para maos", "creme para os pes",
                 "manteiga", "sabonete intimo", "autobronzeador", "bronzeador", "desodorante", "hidratante wepink",
                 "kit wepink"]),
    ("♀ cabelo: tratamento", ["shampoo", "condicionador", "mascara capilar", "mascara de hidratacao", "oleo capilar",
                              "kit cronograma", "kit shampoo", "ampola", "reparador",
                              "protetor termico", "shampoo a seco", "tonico", "kit siage", "kit truss"]),
    ("♀ cachos e cor", ["leave", "creme para pentear", "gelatina", "mousse", "kit cachos", "tinta", "matizador"]),
    ("♀ cabelo: aparelhos", ["chapinha", "prancha", "secador", "escova secadora", "escova rotativa", "modelador",
                             "difusor"]),
    ("♀ cabelo: acessórios", ["escova de cabelo", "escova raquete", "presilha", "piranha", "scrunchie", "tiara",
                              "touca", "fronha"]),
    ("♀ perfume", ["perfume", "perfume feminino", "perfume arabe feminino", "body splash", "kit body splash", "body mist",
                   "colonia", "perfume natura", "perfume boticario", "perfume capilar", "kit perfume",
                   "hidratante perfumado", "perfume wepink"]),
    ("♀ unhas", ["alicate de cuticula", "esmalte", "kit esmaltes", "cabine", "kit unha de gel", "unha", "kit manicure", "alicate de cuticula",
                 "lixa", "base fortalecedora", "removedor de esmalte", "polygel", "adesivo"]),
    ("♀ vestido e saia", ["macacao feminino", "vestido", "saia", "macacao feminino", "kimono", "saida"]),
    ("♀ blusa e casaco", ["camiseta feminina", "jaqueta feminina", "jaqueta jeans feminina", "moletom feminino", "blusa", "cropped", "body feminino", "camiseta feminina", "regata", "blazer", "cardigan",
                          "sueter", "moletom feminino", "jaqueta feminina", "jaqueta jeans feminina"]),
    ("♀ calça e short", ["calca wide leg", "calca pantalona", "short jeans feminino", "conjunto de linho", "calca feminina", "calca wide", "calca jeans feminina", "calca pantalona",
                         "short jeans feminino", "conjunto feminino", "conjunto linho"]),
    ("♀ pijama e praia", ["pijama feminino", "camisola", "robe", "biquini", "maio"]),
    ("♀ calcinha e sutiã", ["meia calca", "calcinha", "kit calcinhas", "sutia", "top sem costura", "meia calca"]),
    ("♀ sandália e salto", ["sandalia", "sandalia feminina", "papete", "tamanco", "mule", "salto", "scarpin",
                            "sapatilha"]),
    ("♀ tênis e bota feminino", ["tenis feminino", "tenis casual feminino", "tenis plataforma", "tenis branco feminino", "bota", "coturno", "teni feminino", "teni casual feminino", "teni plataforma",
                                 "teni branco feminino", "tenis de academia"]),
    ("♀ chinelo", ["chinelo feminino", "slide feminino", "chinelo nuvem", "slide feminino", "havaiana", "croc"]),
    ("♀ bolsa", ["carteira feminina", "pochete feminina", "bolsa", "bolsa feminina", "bolsa transversal", "bolsa tiracolo", "bolsa ombro", "bolsa tote",
                 "bolsa bau", "bolsa mao", "clutch", "bolsa de praia", "mochila feminina", "carteira feminina",
                 "porta cartao", "pochete feminina"]),
    ("♀ joias e acessórios", ["cinto feminino", "pulseira feminina", "brinco", "kit brincos", "colar", "pulseira feminina", "anel", "kit semijoias",
                              "porta joias", "cinto feminino", "chapeu"]),
    ("♀ relógio e óculos", ["oculos de sol feminino", "relogio feminino", "oculo", "smartwatch feminino"]),
    ("♀ fitness", ["short fitness", "top fitness", "legging", "short fitnes", "conjunto fitness", "top fitnes", "macaquinho",
                   "garrafa de agua motivacional", "tapete de yoga", "mini band", "bola de pilates"]),
    ("♀ casa: aroma", ["aromatizador de ambiente", "vela", "difusor de aromas", "home", "aromatizador"]),
    ("♀ casa: decoração", ["almofada decorativa", "manta", "tapete felpudo", "quadro", "vaso", "planta", "espelho redondo"]),
    ("♀ casa: luz", ["luminaria", "fita"]),
    ("♀ casa: cama", ["jogo de lencol", "edredom", "travesseiro", "kit cama"]),
    ("♀ casa: banho", ["toalha banho", "roupao", "tapete de banheiro", "kit banheiro"]),
    ("♀ casa: organização", ["cabide", "caixa organizadora", "organizador de bolsas", "organizador de gaveta",
                             "sapateira", "arara"]),
    ("♀ cozinha: eletro", ["cafeteira expresso", "air", "panela eletrica", "liquidificador", "mixer", "cafeteira", "sanduicheira",
                           "forno", "marmita", "pipoqueira", "chaleira", "balanca cozinha"]),
    ("♀ cozinha: panela e faca", ["jogo de facas", "jogo panelas", "panela", "jogo de facas", "tabua corte", "utensilio"]),
    ("♀ cozinha: potes e garrafa", ["porta temperos", "garrafa termica", "copo termico", "pote hermetico", "kit potes",
                                    "organizador de geladeira", "porta temperos"]),
    ("♀ cozinha: gadgets", ["caneca mixer", "triturador", "caneca", "espumador"]),
    ("♀ mesa posta", ["jogo americano", "jogo de copos", "aparelho", "jogo copos", "taca"]),
    ("♀ limpeza do chão", ["robo", "mop", "aspirador", "aspirador vertical", "aspirador portatil", "vassoura", "rodo"]),
    ("♀ limpeza: produtos", ["kit panos", "escova eletrica de limpeza", "limpa", "tira", "sabao", "amaciante",
                             "lustra", "dispenser sabao"]),
    ("♀ lavanderia", ["cesto de roupa", "varal", "tabua passar", "ferro", "vaporizador", "lixeira"]),
    # ---------- Masculino e geral ----------
    ("regata e dry fit", ["regata masculina", "regata dry fit", "camiseta dry fit", "camiseta oversized"]),
    ("meias", ["meia cano alto", "meia invisivel", "meia de compressao", "kit meias"]),
    ("tênis esportivo", ["tenis esportivo", "tenis para academia", "tenis de basquete", "tenis de futsal",
                         "tenis de corrida"]),
    ("basquete e tênis (Wilson)", ["bola de basquete", "raquete de tenis", "bola de tenis", "tabela de basquete"]),
    ("mochila e mala", ["mochila de viagem", "mochila antifurto", "mochila impermeavel", "mala de bordo"]),
    ("headphone e fone esportivo", ["headphone sem fio", "fone esportivo", "fone com cancelamento", "fone gamer",
                                    "headphone"]),
    ("short e sunga", ["short de treino", "short de praia", "bermuda tactel", "sunga"]),
    ("churrasco e cerveja", ["kit churrasco", "faca de churrasco", "copo termico de cerveja", "cooler",
                             "caixa termica"]),
    ("periférico gamer", ["mouse gamer", "teclado gamer", "headset gamer", "mousepad gamer"]),
    ("pesca", ["vara de pesca", "molinete", "carretilha", "kit pesca"]),
    ("relógio esportivo", ["relogio digital", "relogio esportivo", "relogio garmin", "smartwatch garmin"]),
    ("♀ colágeno e vitaminas", ["colageno", "colageno verisol", "biotina", "vitamina para cabelo",
                                 "goma de vitamina"]),
    ("♀ fofuras", ["copo stanley rosa", "garrafa com canudo", "garrafa termica rosa", "capinha feminina",
                   "case de airpods", "luminaria fofa", "umidificador fofo"]),
    ("suplemento: proteína", ["whey protein", "whey", "barra de proteina", "pasta de amendoim", "hipercalorico"]),
    ("suplemento: creatina e pré", ["creatina", "pre treino", "bcaa", "glutamina"]),
    ("vitaminas", ["omega", "multivitaminico", "vitamina d", "magnesio"]),
    ("drone e câmera", ["drone", "drone com camera", "camera de acao", "camera instantanea", "mini impressora"]),
    ("gadget de quarto e mesa", ["projetor de galaxia", "luminaria lua", "relogio despertador", "mini ventilador",
                                 "lampada com camera"]),
    ("games retrô e VR", ["game stick", "console retro", "mini game", "oculos de realidade virtual"]),
    ("gadgets úteis", ["pilha", "carregador de pilhas", "tag rastreadora", "teclado dobravel", "smart ring",
                       "balanca de bioimpedancia"]),
    ("perfume masculino árabe e importado", ["perfume lattafa", "perfume asad", "perfume club de nuit",
                                             "perfume masculino arabe", "kit perfume masculino"]),
    ("perfume masculino nacional", ["perfume malbec", "perfume kaiak", "perfume quasar", "body spray masculino",
                                    "desodorante masculino"]),
    ("cuidados masculinos", ["kit skincare masculino", "protetor solar masculino", "shampoo masculino",
                             "sabonete masculino"]),
    ("capinha e película", ["capinha", "capa de celular", "capa iphone", "capa samsung", "pelicula", "popsocket",
                            "cordao"]),
    ("carregador e cabo", ["carregador", "power", "cabo", "fonte", "carregador veicular", "carregador de controle"]),
    ("acessório de celular", ["suporte de celular", "suporte veicular", "suporte magnetico para celular", "tripe",
                              "ring", "pau", "gimbal", "airtag", "rastreador"]),
    ("fone", ["galaxy buds", "fone galaxy buds", "fone", "fone jbl", "airpod", "headset", "headphone", "galaxy bud"]),
    ("caixa de som", ["caixa de som", "caixinha de som", "caixa de som jbl", "soundbar", "microfone", "karaoke",
                      "jbl"]),
    ("relógio inteligente", ["galaxy watch", "smartwatch", "relogio inteligente", "apple", "galaxy watch", "pulseira", "smart band",
                             "mi", "amazfit"]),
    ("celular e tablet", ["celular", "iphone", "samsung", "motorola", "redmi", "ipad", "tablet", "kindle"]),
    ("computador", ["mouse", "mousepad", "teclado", "kit teclado", "webcam", "hub", "pen", "cartao", "ssd", "hd",
                    "memoria", "notebook", "macbook", "monitor", "roteador", "repetidor", "suporte para notebook",
                    "mochila para notebook", "capa para notebook", "capa para kindle", "capa para ipad", "caneta touch",
                    "luminaria led rgb", "mesa gamer", "cadeira gamer"]),
    ("videogame", ["controle", "headset ps5", "jogo ps5", "suporte para controle", "playstation", "xbox", "nintendo"]),
    ("casa inteligente", ["echo", "fire", "lampada inteligente", "tomada", "camera de seguranca", "camera ip",
                          "projetor", "mini projetor", "fechadura"]),
    ("camiseta e camisa", ["camiseta basica", "camiseta masculina", "camiseta basica", "kit camisetas", "camisa polo", "camisa social"]),
    ("calça e bermuda", ["calca jogger", "bermuda", "calca jeans masculina", "calca jogger"]),
    ("casaco masculino", ["jaqueta corta vento", "moletom masculino", "jaqueta masculina", "jaqueta"]),
    ("cueca e meia", ["meia esportiva", "cueca", "kit cuecas", "kit meias", "meia esportiva", "pijama masculino"]),
    ("boné e acessório", ["oculos de sol masculino", "bone", "carteira masculina", "cinto masculino", "corrente", "pochete masculina",
                          "mochila masculina"]),
    ("relógio masculino", ["relogio masculino", "relogio", "relogio casio", "relogio technos"]),
    ("perfume masculino", ["perfume masculino", "perfume arabe masculino", "perfume importado", "perfume arabe",
                           "kit perfume importado"]),
    ("tênis e chinelo masculino", ["teni masculino", "teni casual masculino", "teni corrida", "teni", "sapateni",
                                   "chinelo masculino", "slide masculino"]),
    ("barba e pelos", ["pomada modeladora", "aparador de barba", "aparador de pelos", "barbeador", "maquina de cortar cabelo", "kit barba",
                       "oleo para barba", "balm", "pomada modeladora"]),
    ("academia", ["corda", "faixa elastica", "kit elastico", "halter", "kit halteres", "anilha", "barra",
                  "caneleira", "roda", "luva de academia", "munhequeira", "coqueteleira", "garrafa squeeze academia",
                  "bolsa de academia", "bicicleta ergometrica", "esteira"]),
    ("esporte de bola", ["bola", "raquete", "camisa de time", "chuteira"]),
    ("bike e camping", ["capacete de bicicleta", "luz", "barraca", "lanterna de cabeca", "bicicleta", "patinete"]),
    ("carro: limpeza", ["aspirador automotivo", "kit lavagem", "shampoo automotivo", "cera", "pretinho",
                        "aromatizador automotivo"]),
    ("carro: eletrônicos", ["transmissor", "camera veicular", "camera de re", "som", "central"]),
    ("carro: acessórios", ["tapete automotivo", "capa de banco automotivo", "organizador de porta malas",
                           "lampada led automotiva", "sol", "para"]),
    ("carro: pneu", ["compressor", "calibrador", "macaco"]),
    ("moto", ["capacete", "capa de chuva para moto", "bau", "luva para moto", "intercomunicador"]),
    ("ferramentas", ["parafusadeira", "furadeira", "kit ferramentas", "jogo de chaves", "trena", "nivel",
                     "alicate", "caixa de ferramentas", "lanterna tatica", "lanterna recarregavel", "kit brocas"]),
    ("pet: comida", ["racao", "petisco", "ossinho"]),
    ("pet: cama e casinha", ["caminha para cachorro", "caminha para gato", "arranhador", "casinha de cachorro",
                             "tapete gelado pet"]),
    ("pet: comedouro", ["comedouro", "fonte", "bebedouro"]),
    ("pet: higiene", ["caixa de areia", "areia", "tapete higienico", "shampoo para cachorro", "escova para pet",
                      "cortador"]),
    ("pet: passeio", ["coleira", "peitoral", "guia", "roupinha", "caixa de transporte pet", "bolsa de transporte pet"]),
    ("pet: brinquedo", ["brinquedo para cachorro", "brinquedo para gato", "varinha"]),
    ("papelaria: caderno", ["caderno", "fichario", "planner", "agenda"]),
    ("papelaria: canetas", ["kit canetas", "caneta", "marca", "post", "lapi", "aquarela", "kit lettering", "washi"]),
    ("papelaria: escola", ["estojo", "mochila escolar", "calculadora", "organizador de mesa"]),
    ("viagem", ["balanca mala", "travesseiro de pescoco", "mala", "kit malas", "organizador de mala", "necessaire de viagem", "travesseiro de pescoco",
                "balanca de mala", "cadeado", "bolsa de viagem"]),
    ("♀ casa grande: cozinha", ["geladeira", "fogao", "micro"]),
    ("♀ casa grande: lavar", ["maquina lavar", "lava seca", "maquina", "lava", "lava louca"]),
    ("tv", ["smart"]),
    ("ar-condicionado", ["ar"]),
    ("♀ casa grande: cama e sofá", ["cama", "colchao", "sofa"]),
]

# ---------- Chamadas (sem "casa" nas genéricas) ----------
CHAMADAS_GERAIS = ["🔥 ACHADO DO DIA", "👀 OLHA ESSE PREÇO", "😍 TODO MUNDO TÁ LEVANDO",
                   "😱 VALE MUITO A PENA", "🛒 QUEM VIU, LEVOU"]
CHAMADAS_CARO = ["💎 PRODUTO TOP COM PREÇO DE OPORTUNIDADE", "😮 ESSE PREÇO NÃO É TODO DIA"]
CHAMADAS_ATE_100 = ["🤑 PRECINHO CAMARADA"]
CHAMADAS_POR_TIPO = CHAMADAS_POR_TIPO + [
    (["fone", "headset", "caixa de som", "caixinha de som"], ["🎧 SOM NA FAIXA"]),
    (["smartwatch", "relógio inteligente", "smart band", "pulseira inteligente"], ["⌚ TUDO NO PULSO"]),
    (["carregador", "power bank", "cabo"], ["🔋 BATERIA SEMPRE CHEIA"]),
    (["iphone", "samsung galaxy", "celular"], ["📱 CELULAR NOVO NA MÃO"]),
    (["chapinha", "prancha", "secador", "escova secadora", "escova rotativa", "modelador"],
     ["💇‍♀️ CABELO DE SALÃO EM CASA"]),
    (["base", "batom", "gloss", "paleta", "máscara de cílios", "blush", "corretivo", "maquiagem"],
     ["💄 MAKE DE DIVA"]),
    (["perfume", "body splash", "body mist", "colônia"], ["🌸 CHEIROSA O DIA TODO"]),
    (["sérum", "skincare", "hidratante facial", "vitamina c", "protetor solar"], ["✨ PELE DE PÊSSEGO"]),
    (["vestido", "blusa", "cropped", "saia", "calça", "conjunto"], ["👗 LOOK PRONTO"]),
    (["sandália", "salto", "tênis feminino", "bota", "sapatilha", "chinelo"], ["👠 PÉ LINDO E CONFORTÁVEL"]),
    (["bolsa", "clutch", "carteira feminina"], ["👜 A BOLSA DO MOMENTO"]),
    (["brinco", "colar", "anel", "semijoias", "pulseira feminina"], ["💍 BRILHO NO LOOK"]),
    (["cachorro", "gato", "pet", "coleira", "comedouro"], ["🐶 SEU PET VAI AMAR"]),
    (["halter", "academia", "yoga", "corda de pular", "elástico", "fitness", "legging"], ["💪 BORA TREINAR"]),
    (["automotivo", "carro", "veicular", "pneu", "moto", "capacete"], ["🚗 CARRO NOS TRINQUES"]),
    (["caderno", "caneta", "planner", "agenda", "estojo", "lápis"], ["✏️ MATERIAL QUE DÁ GOSTO DE USAR"]),
    (["whey", "creatina", "pré treino", "bcaa", "barra de proteína", "hipercalórico"], ["💪 SHAPE EM DIA"]),
    (["drone", "câmera de ação", "game stick", "console", "realidade virtual", "projetor"], ["🤩 GADGET DE RESPEITO"]),
]

# ---------- 07/11: marca que o povo confia, menos coisa de mercado ----------
# A mãe do Gabriel (já vendeu por link): "ninguém entra no link pra comprar creme Nivea ou piranha de cabelo, isso
# a gente compra passando no supermercado; tem que ser assertivo: Boticário, Natura, Avon, perfume, creme de
# qualidade, eletrodoméstico". Gabriel: "enche de Avon, Boticário, Natura, sabonete... capa de sofá também".
# Cada linha abaixo é uma CATEGORIA própria do rodízio (cada uma tem a vez dela em toda volta), por isso a marca
# está dividida em várias: quanto mais categorias, mais vezes ela aparece no dia.
# As buscas começam pelo nome da linha (o filtro exige que o nome do produto comece parecido com a busca).
MARCAS_DE_CONFIANCA = [
    ("♀ Boticário: perfume", ["floratta", "lily boticário", "glamour boticário", "egeo boticário",
                              "coffee woman", "elysée boticário", "boticário feminino"]),
    ("♀ Boticário: corpo e banho", ["nativa spa", "cuide-se bem", "hidratante boticário", "sabonete boticário",
                                    "body splash boticário", "kit boticário"]),
    ("♀ Boticário: maquiagem", ["make b boticário", "intense boticário", "batom boticário", "máscara de cílios boticário"]),
    ("♀ Natura: perfume", ["natura essencial", "natura luna", "natura kriska", "natura ilía", "natura humor",
                           "natura una perfume"]),
    ("♀ Natura: corpo e banho", ["natura tododia", "natura ekos", "hidratante tododia", "polpa ekos",
                                 "sabonete natura", "kit natura"]),
    ("♀ Natura: maquiagem e cabelo", ["natura una", "batom natura", "natura lumina", "natura plant"]),
    ("♀ Avon: perfume e corpo", ["far away avon", "avon attraction", "avon surreal", "avon 300 km",
                                 "hidratante avon", "kit avon"]),
    ("♀ Avon: maquiagem", ["batom avon", "avon power stay", "máscara de cílios avon", "avon true"]),
    ("♀ Eudora", ["eudora", "kit eudora", "eudora glam", "eudora niina secrets"]),
    ("♀ sabonete de marca", ["sabonete granado", "sabonete phebo", "kit sabonetes granado", "sabonete ekos",
                             "sabonete líquido natura", "sabonete tododia"]),
    ("♀ capa de sofá", ["capa de sofá", "capa de sofá retrátil", "capa de sofá elástica",
                        "capa de sofá impermeável", "protetor de sofá", "capa de sofá de canto"]),
    # 08/11: a tia pediu ventilador de teto com lâmpada. Sem ♀: entra na vez do "masculino/geral" da alternância
    ("ventilador de teto", ["ventilador de teto", "ventilador de teto com luminária", "ventilador de teto com lâmpada",
                            "ventilador de teto com controle remoto", "ventilador de teto led"]),
    # 08/11: prints da vitrine de afiliado (comissão extra, milhares de vendas)
    ("♀ manta e almofada para sofá", ["kit manta e capas de almofada", "manta decorativa para sofá",
                                      "kit capas de almofada"]),
    ("♀ potes herméticos", ["potes herméticos", "jogo de potes herméticos", "potes de vidro hermético",
                            "kit potes herméticos acrílico"]),
    ("♀ cobre leito e peseira", ["kit cobre leito casal", "cobre leito queen", "peseira para cama", "kit peseira"]),
    ("♀ cozinha prática", ["cozedor de ovos elétrico", "nicho porta tempero", "kit utensílios de silicone",
                           "forma de gelo de silicone", "cesto de roupa suja"]),
    ("quintal e jardim", ["mangueira mágica", "mangueira expansível", "tela de sombreamento",
                          "bomba elétrica para galão"]),
    # masculino, para não desequilibrar o 50/50
    ("Boticário masculino", ["boticário masculino", "egeo masculino", "arbo boticário", "uomini boticário",
                             "zaad boticário", "kit boticário masculino"]),
    ("Natura e Avon masculino", ["natura homem", "natura essencial masculino", "kaiak natura",
                                 "avon masculino", "kit natura masculino"]),
]
def _sem_acento(t):
    return " ".join(unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower().split())
for _cat, _buscas in MARCAS_DE_CONFIANCA:
    PALAVRAS[_cat] = _buscas
    TIPOS_PROPRIOS = TIPOS_PROPRIOS + _buscas   # cada busca é o próprio tipo (senão "kit boticário" virava "kit")
# Na frente: ganham das categorias antigas ("capa de sofá" não cai em "sofá e poltrona")
CATEGORIAS_EXTRA = [(c, [_sem_acento(b) for b in bs]) for c, bs in MARCAS_DE_CONFIANCA] + CATEGORIAS_EXTRA
# Peso 2: cada uma tem a vez 2 vezes em cada volta do rodízio (as outras 1). Dá ~1 em cada 5 posts dessas marcas
PESO_CATEGORIA = {c: 2 for c, _ in MARCAS_DE_CONFIANCA}
# 07/11, Gabriel: "pra repetir o masculino tem que fazer o feminino". Um post ♀, o próximo sem ♀, e assim vai
ALTERNAR_FEMININO = True
PESO_CATEGORIA["ventilador de teto"] = 3
PESO_CATEGORIA["♀ capa de sofá"] = 3       # 08/11, Gabriel: "capa de sofá no algoritmo"
# 08/11: o que já vendeu (ducha, garrafa térmica, jogo americano, suporte de notebook) tem vez dobrada.
# O bot também aprende sozinho com o relatório de vendas (postar_shopee.py, "Aprende com as vendas")
for _c in ["chuveiro e ducha", "♀ cozinha: potes e garrafa", "♀ mesa posta", "computador"]:
    PESO_CATEGORIA[_c] = max(PESO_CATEGORIA.get(_c, 1), 2)
MARCAS = MARCAS + ["Granado", "Phebo", "Make B", "Tododia", "Ekos", "Quem Disse, Berenice",
                   "Volare", "Spirit", "Fan Bello"]

# Coisa de supermercado / baratinha que ninguém clica (saem da lista)
_DE_MERCADO = [
    "piranha de cabelo", "presilha de cabelo", "scrunchie", "tiara", "lixa de unha", "removedor de esmalte",
    "adesivo de unha", "shampoo", "condicionador", "hidratante corporal", "loção hidratante", "creme para mãos",
    "creme para os pés", "desodorante feminino", "sabão líquido", "amaciante", "limpa vidros", "tira manchas",
    "lustra móveis", "desodorante masculino", "sabonete masculino", "sabonete íntimo",
]
PALAVRAS = {c: [p for p in l if p not in _DE_MERCADO] for c, l in PALAVRAS.items()}

TEXTO_MODELO_IA = TEXTO_MODELO_IA + (
    "Prefira marca que o povo confia (O Boticário, Natura, Avon, Eudora, Granado e as marcas conhecidas de cada "
    "tipo). Recuse coisa baratinha de supermercado que ninguém compra pelo link (grampo, piranha de cabelo, "
    "creme comum de farmácia, produto de limpeza comum).\n")
CHAMADAS_POR_TIPO = CHAMADAS_POR_TIPO + [
    (["boticário", "natura", "avon", "eudora", "floratta", "nativa spa", "tododia", "ekos", "granado", "phebo"],
     ["💖 MARCA QUE TODO MUNDO CONFIA", "🌸 CHEIROSA O DIA TODO"]),
    (["capa de sofá", "protetor de sofá"], ["🛋️ SOFÁ COM CARA DE NOVO"]),
]

# ---------- 08/11 (noite): o Geral no padrão do Casa ----------
# Gabriel: "o Casa tá excelente... o geral foi feito do dia pra noite. Onde você acha que é necessário colocar
# marca, coloque... tá postando muita coisa feminina, eu quero ver mais coisa de homem também. Posta uns gadgets...
# muito cabo, carregador, iPhone, Samsung... cueca Lupo, Nike, Wilson, 100% algodão, roupa de treinar de
# poliéster, masculino e feminino... creatina, Max, Growth... Curaprox, Boticário, Avon, Principia, kits".
NICHO_IA = ("achadinhos e promoções da Shopee (público de homens e mulheres meio a meio: tecnologia, celular, "
            "gadgets, suplemento, roupa e treino, beleza de marca, casa; NADA infantil: recuse brinquedo, roupa "
            "infantil, produto de bebê ou criança, canetinha e material escolar)")
# Como o Casa: produto de marca na frente; sem marca só se for muito bem avaliado (nota 4,7+ e 1000+ vendas)
EXIGIR_MARCA_SEMPRE = True

# Tipo de MARCA FORTE (como a panela do Casa só Tramontina): só posta com uma destas marcas, e o bot busca
# também "produto + marca" (ex.: "carregador turbo Baseus", "creatina Growth")
_MARCAS_CARGA = ["Apple", "Samsung", "Baseus", "Anker", "Ugreen", "Xiaomi", "Motorola", "Geonav", "i2GO", "ELG",
                 "Intelbras", "Multilaser", "Belkin", "Philips", "Lenovo", "Essager", "Mcdodo"]
_MARCAS_FONE = ["JBL", "Samsung", "Galaxy", "Apple", "AirPods", "Xiaomi", "Redmi", "QCY", "Haylou", "Edifier",
                "Sony", "Lenovo", "Philips", "Baseus", "Soundcore", "Anker", "Motorola", "HyperX", "Redragon",
                "Havit", "Logitech", "Jabra", "Sennheiser", "Beats", "Huawei", "Realme", "Shokz", "Bose",
                "Skullcandy", "Multilaser", "ELG", "i2GO", "Tranya"]
_MARCAS_RELOGIO_SMART = ["Apple", "Samsung", "Galaxy", "Xiaomi", "Amazfit", "Huawei", "Garmin", "Haylou", "Redmi",
                         "Mibro", "Kieslect", "Polar", "Honor", "Realme", "Lenovo", "Motorola", "Technos",
                         "Mondaine", "Champion"]
_MARCAS_SUPLEMENTO = ["Growth", "Max Titanium", "Integralmédica", "Integral Médica", "Soldiers Nutrition", "Soldiers",
                      "Black Skull", "Dux", "Probiótica", "Optimum Nutrition", "Darkness", "Atlhetica", "Vitafor",
                      "Essential Nutrition", "Nutrify", "New Millen", "FTW", "Body Action", "Dr. Peanut",
                      "Dr Peanut", "Mais Mu", "Puravida", "Nutrata", "Sanavita", "Equaliv", "Lavitan", "Centrum",
                      "Nature's Bounty", "Vitgold", "Catarinense", "Adaptogen", "Iridium",
                      "Dark Lab", "Darklab", "Under Labz", "Bold Snacks", "Integral Medica"]
_MARCAS_CUECA = ["Lupo", "Calvin Klein", "Hering", "Mash", "Puket", "Zorba", "Duomo", "Selene", "Polo Wear",
                 "Tommy Hilfiger", "Nike", "Adidas", "Puma", "Olympikus", "Mizuno", "Fila", "Under Armour",
                 "Penalty", "Trifil", "Reserva", "Aramis", "Hope", "Speedo", "Mormaii", "Track & Field", "Liz",
                 "Ralph Lauren", "Polo Ralph Lauren", "Hugo Boss", "Boss", "Lacoste", "Jockey"]
MARCAS_POR_TIPO = MARCAS_POR_TIPO + [
    (["carregador", "carregador turbo", "carregador iphone", "carregador samsung", "carregador usb c",
      "carregador 3 em 1", "carregador por indução", "carregador magsafe", "carregador portátil", "power bank",
      "cabo usb", "cabo usb tipo c", "cabo usb c", "cabo lightning", "cabo para iphone", "fonte iphone",
      "carregador veicular", "hub usb c"], _MARCAS_CARGA),
    (["carregador de pilhas", "pilhas recarregáveis"], ["Elgin", "Duracell", "Panasonic", "Energizer", "Philips",
                                                       "Sony", "Rayovac", "Multilaser", "Flex"]),
    (["fone", "fone de ouvido", "fone de ouvido bluetooth", "fone bluetooth", "fone sem fio", "headphone",
      "headphone bluetooth", "headphone sem fio", "headset", "headset gamer", "headset gamer sem fio",
      "fone esportivo", "fone com cancelamento de ruído", "fone gamer sem fio", "fone de condução óssea",
      "fone de ouvido com fio"], _MARCAS_FONE),
    (["smartwatch", "relógio inteligente", "smart band", "mi band", "pulseira inteligente"], _MARCAS_RELOGIO_SMART),
    (["whey", "whey protein", "whey protein concentrado", "creatina", "creatina monohidratada", "pré treino",
      "bcaa", "glutamina", "hipercalórico", "barra de proteína", "pasta de amendoim", "beta alanina",
      "ômega 3", "multivitamínico", "vitamina d", "magnésio", "colágeno", "colágeno verisol"], _MARCAS_SUPLEMENTO),
    (["cueca", "kit cuecas", "cueca boxer", "kit cueca boxer", "kit meias", "meia esportiva", "meia cano alto",
      "meia invisível masculina", "meia de compressão"], _MARCAS_CUECA),
]
# Capinha, película, suporte e cabo de carregador de controle: o povo compra sem marca (não trava)
MARCA_OPCIONAL = MARCA_OPCIONAL + ["capinha", "capa de celular", "capa iphone", "capa samsung", "película",
                                   "suporte de celular", "suporte veicular", "tripé", "ring light", "pau de selfie",
                                   "popsocket", "cordão para celular", "carregador de controle", "capinha magsafe"]
MARCAS = MARCAS + [m for m in _MARCAS_CARGA + _MARCAS_FONE + _MARCAS_RELOGIO_SMART + _MARCAS_SUPLEMENTO
                   + _MARCAS_CUECA + ["Curaprox", "Oral-B", "Colgate", "Sensodyne", "Elgin", "Duracell",
                                      "Principia", "Creamy", "Sallve", "Wilson"] if m not in MARCAS]

# Mais buscas nas categorias que já existem (cabo, carregador, iPhone, Samsung)
PALAVRAS["celular"] = PALAVRAS["celular"] + [
    "carregador turbo 20w", "carregador apple 20w", "carregador samsung 45w", "carregador baseus",
    "carregador ugreen", "cabo usb c 2 metros", "cabo usb c para lightning", "cabo usb c 100w",
    "cabo lightning 2 metros", "cabo samsung usb c", "power bank 10000mah", "power bank 20000mah",
    "carregador portátil magsafe", "capa iphone 16", "capa iphone 15", "capa samsung galaxy s24",
    "película iphone 16", "película samsung galaxy", "carregador magsafe apple"]
PALAVRAS["computador"] = PALAVRAS["computador"] + ["mouse sem fio logitech", "teclado sem fio logitech",
                                                   "hub usb c baseus", "ssd externo", "pen drive sandisk"]

# Categorias novas (cada uma tem a vez dela; as de homem não têm ♀ e entram na vez do masculino)
GERAL_PADRAO_CASA = [
    ("gadgets da hora", ["mini projetor portátil", "suporte magnético veicular", "lanterna tática recarregável",
                         "mini aspirador portátil", "fire tv stick", "echo pop", "câmera de segurança wifi",
                         "smart tag", "carregador por indução 3 em 1"]),
    ("roupa de treino", ["camiseta dry fit masculina", "camiseta nike masculina", "regata de treino masculina",
                         "short nike masculino", "bermuda de treino masculina", "calça de treino masculina",
                         "camiseta de treino poliéster", "camiseta adidas masculina"]),
    ("camiseta 100% algodão", ["camiseta 100% algodão masculina", "camiseta básica 100% algodão",
                               "kit camisetas básicas algodão", "camiseta hering", "camisa polo algodão"]),
    ("cueca e meia de marca", ["cueca boxer", "kit cueca boxer", "kit cuecas", "kit meias", "meia esportiva",
                               "cueca 100% algodão", "cueca lupo algodão"]),
    ("♀ roupa de treino", ["legging lupo", "top lupo", "conjunto fitness feminino", "legging poliamida",
                           "short fitness lupo", "conjunto lupo feminino", "top nike feminino"]),
    ("escova de dente de marca", ["escova curaprox", "kit curaprox", "escova de dente elétrica oral-b",
                                  "escova oral-b", "creme dental curaprox", "escova de dente colgate"]),
    ("♀ Principia e skincare de marca", ["kit principia", "sérum principia", "principia skincare", "kit creamy",
                                         "sallve", "cerave", "kit la roche posay"]),
    ("♀ kits de presente", ["kit presente boticário", "kit presente natura", "kit presente avon",
                            "kit presente eudora", "kit floratta", "kit nativa spa"]),
    ("kit presente masculino", ["kit presente masculino boticário", "kit malbec", "kit kaiak", "kit quasar",
                                "kit natura homem", "kit egeo"]),
]
_buscas_novas = {b for _, bs in GERAL_PADRAO_CASA for b in bs}
PALAVRAS = {c: [p for p in l if p not in _buscas_novas] for c, l in PALAVRAS.items()}   # sem busca repetida
for _cat, _buscas in GERAL_PADRAO_CASA:
    PALAVRAS[_cat] = _buscas
    TIPOS_PROPRIOS = TIPOS_PROPRIOS + _buscas
CATEGORIAS_EXTRA = [(c, [_sem_acento(b) for b in bs]) for c, bs in GERAL_PADRAO_CASA] + CATEGORIAS_EXTRA

# Mais vez para o que o Gabriel pediu (no lado masculino da alternância: um ♀, um destes, e assim vai)
for _c, _p in [("carregador e cabo", 3), ("fone", 3), ("gadgets da hora", 3), ("celular e tablet", 2),
               ("acessório de celular", 2), ("relógio inteligente", 2), ("caixa de som", 2), ("gadgets úteis", 2),
               ("suplemento: proteína", 3), ("suplemento: creatina e pré", 3), ("vitaminas", 2),
               ("roupa de treino", 2), ("camiseta 100% algodão", 2), ("cueca e meia de marca", 2),
               ("escova de dente de marca", 2), ("kit presente masculino", 2), ("periférico gamer", 2),
               ("tênis esportivo", 2), ("perfume masculino árabe e importado", 2), ("basquete e tênis (Wilson)", 2),
               ("♀ roupa de treino", 2), ("♀ Principia e skincare de marca", 2), ("♀ kits de presente", 2)]:
    PESO_CATEGORIA[_c] = max(PESO_CATEGORIA.get(_c, 1), _p)

TEXTO_MODELO_IA = TEXTO_MODELO_IA + (
    "No nome, ponha a especificação que o comprador procura quando o título tiver: comprimento do cabo (2 Metros), "
    "potência do carregador (20W), capacidade (10.000mAh, 256GB), peso do suplemento (1kg, 300g), quantidade do kit "
    "(Kit 5 Cuecas) e o modelo do celular/fone. Nada de inventar: só o que está no título.\n")
CHAMADAS_POR_TIPO = CHAMADAS_POR_TIPO + [
    (["cueca", "meia"], ["🩲 CONFORTO O DIA INTEIRO"]),
    (["dry fit", "treino", "legging", "top lupo"], ["💪 BORA TREINAR"]),
    (["curaprox", "oral-b", "escova de dente"], ["🦷 SORRISO LIMPINHO"]),
    (["kit presente"], ["🎁 PRESENTE CERTEIRO"]),
]

# ---------- Mensagem dos grupos ----------
# Os 2 grupos, com o deste bot primeiro (o Casa lista na ordem contrária)
GRUPOS = [("🔗 Achadinhos & Promoções", "https://chat.whatsapp.com/CONVITE_DO_GRUPO_GERAL"),
          ("🏠 Achadinhos de Casa", "https://chat.whatsapp.com/CONVITE_DO_GRUPO_CASA")]
