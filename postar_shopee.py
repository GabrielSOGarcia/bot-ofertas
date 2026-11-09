import hashlib, json, random, time, urllib.error, urllib.request, urllib.parse
import base64, html, io, math, os, re, shutil, sys, unicodedata
from collections import Counter
from datetime import date, datetime, timedelta
import cupons
try:
    from PIL import Image
except ImportError:
    Image = None

# ================= AJUSTES (mexa só aqui) =================
# Produtos populares do dia a dia (a maioria dos posts)
PALAVRAS = {
    "cozinha": [
        "panela", "panela inox", "panela de cerâmica", "panela de pedra", "jogo de panelas", "frigideira", "panela de pressão",
        "air fryer", "forno elétrico", "micro-ondas", "prato", "jogo de pratos",
        "talheres", "faqueiro", "copo", "jogo de copos", "conjunto de copos", "xícara",
        "caneca", "taça", "garrafa", "garrafa térmica", "garrafa de café", "jarra",
        "pote hermético", "pote de vidro", "escorredor de louça", "tábua de corte",
        "tábua de corte de madeira", "tábua de corte de bambu", "kit utensílios de bambu",
        "faca de cozinha", "assadeira", "forma de bolo", "marmita", "marmita de vidro",
        "lancheira", "liquidificador", "batedeira", "cafeteira", "chaleira elétrica",
        "sanduicheira", "mixer", "processador de alimentos", "panela elétrica de arroz",
        "pano de prato de algodão", "toalha de mesa", "porta tempero", "utensílios de silicone",
        "balança de cozinha", "organizador de geladeira", "porta ovos", "jogo americano",
        "suporte para panelas", "lixeira de pia", "panela esmaltada", "bule esmaltado",
        "conjunto de facas", "pano de prato", "tapete seca louça", "filtro de barro", "filtro de água",
        # Organização da cozinha (acrílico, mantimentos, geladeira)
        "organizador de armário de cozinha", "organizador de acrílico", "porta mantimentos",
        "pote de mantimentos", "dispenser de cereais", "organizador de geladeira acrílico",
        "porta frios", "porta papel toalha", "fruteira", "cesta de pão",
        # Mesa e preparo
        "aparelho de jantar", "jogo de jantar", "jogo de xícaras", "jogo de taças", "travessa de vidro",
        "refratário", "boleira", "copo térmico", "garrafa de água", "cafeteira italiana",
        "chaleira de inox", "escorredor de macarrão", "ralador", "descascador", "luva térmica",
        "jogo de utensílios de inox", "pipoqueira", "grill elétrico", "torradeira",
        "espremedor de frutas", "cafeteira expresso", "panela de pressão elétrica",
    ],
    "quarto": [
        "travesseiro", "lençol", "jogo de lençol", "fronha", "edredom", "cobertor",
        "colcha", "kit colcha", "protetor de colchão", "cabeceira", "criado-mudo", "cabide",
        "cabide de madeira", "cabide aveludado", "cabide de plástico",
        "organizador de guarda-roupa", "sapateira", "blackout", "abajur",
        "cobre leito", "jogo de cama casal", "jogo de cama queen", "manta de microfibra",
        "jogo de cama 100% algodão", "jogo de lençol 100% algodão",
        "cortina blackout", "arara de roupas", "cabideiro", "baú organizador",
        "organizador de maquiagem", "espelho de chão",
    ],
    "banheiro": [
        "toalha de banho", "jogo de toalhas", "toalha de rosto", "roupão", "jogo de toalhas 100% algodão",
        "tapete banheiro", "tapete de pedra", "cortina de box", "porta escova", "porta cotonete",
        "porta algodão", "saboneteira", "espelho",
        "dispenser sabonete", "sabonete líquido", "sabonete em barra", "sabonete de glicerina",
        "lenço umedecido", "bucha de banho", "bucha vegetal", "esponja de banho",
        "organizador de banheiro", "cesto de roupa suja", "cesto de roupa suja de bambu",
        "chuveiro", "ducha", "prateleira de banheiro",
        "kit sabonete", "papel higiênico", "papel higiênico folha tripla",
        "papel higiênico 24 rolos", "papel toalha", "escova de dente", "kit escova de dente",
        "escova de dente elétrica", "creme dental", "enxaguante bucal", "toalheiro",
        "porta papel higiênico", "lixeira de banheiro", "porta shampoo", "assento sanitário",
        "jogo de tapete para banheiro", "toalha de mão",
    ],
    "sala": [
        "capa de sofá", "almofada", "manta para sofá", "rack tv", "painel tv", "mesa de centro",
        "mesa de sala", "estante", "tapete de sala", "cortina sala", "luminária", "lustre",
        "quadro decorativo", "vaso decorativo", "planta artificial", "relógio de parede",
        "puff", "poltrona", "suporte de tv", "suporte de tv articulado",
        "aparador", "prateleira flutuante", "nicho decorativo", "espelho decorativo",
        "porta retrato", "luminária de chão", "lâmpada led", "manta decorativa", "tapete",
    ],
    "moveis": [
        "mesa de jantar", "mesa dobrável", "cadeira", "banqueta", "banco", "armário", "gaveteiro",
        "organizador de gaveta", "caixa organizadora", "organizador de bambu", "prateleira",
        "cesto organizador", "escrivaninha", "cadeira de escritório", "organizador de cabos",
    ],
    "eletro": [
        "ventilador", "climatizador", "aquecedor elétrico", "umidificador", "aspirador de pó",
        "ferro de passar", "vaporizador", "secadora de roupa", "purificador de água",
        "lâmpada inteligente", "tomada inteligente", "interruptor inteligente",
        # Alexa e TV
        "echo dot", "echo pop", "echo show", "fire tv stick", "mi tv stick",
        "chromecast", "controle remoto",
        "ventilador de teto", "bebedouro", "lavadora de alta pressão", "aspirador vertical",
        "câmera de segurança", "balança corporal", "cooktop",
    ],
    "limpeza": [
        "mop", "vassoura", "rodo", "balde", "kit limpeza", "varal", "varal de chão",
        "cesto de roupa", "tábua de passar", "lixeira", "lixeira 50 litros", "lixeira de inox",
        "cesto de lixo", "kit panos de microfibra",
        "detergente líquido", "bucha mágica", "esponja de cozinha", "sabão em pó",
        "sabão líquido", "amaciante", "desinfetante", "prendedor de roupa",
        "organizador de lavanderia", "escova de limpeza", "pano de chão", "pano multiuso",
        "vinagre de limpeza", "aromatizador de ambiente", "difusor de aromas",
        "percarbonato de sódio", "tira manchas",
        # Lavanderia
        "varal retrátil", "varal de alumínio", "varal de parede", "varal de teto",
        "dosador de sabão em pó", "porta sabão em pó", "sabão em barra", "alvejante",
        "água sanitária",
        # Limpeza da casa
        "mop giratório", "mop spray", "lustra móveis", "limpa vidros", "limpador multiuso",
        "luva de limpeza", "escova sanitária", "saco de lixo", "pedra sanitária",
    ],
    "externa": [
        "rede de descanso", "cadeira de jardim", "vaso de planta", "mangueira de jardim",
        "suporte para mangueira", "enrolador de mangueira",
        "churrasqueira", "churrasqueira portátil", "luminária solar", "kit churrasco",
        "faca para churrasco", "conjunto de facas para churrasco",
        "caixa térmica", "cadeira de praia", "guarda-sol", "piscina inflável", "regador",
        "esguicho", "kit jardinagem",
    ],
}
# Mais variedade (26/10): entra no fim de cada categoria acima
PALAVRAS_MAIS = {
    "cozinha": [
        "jogo de panelas inox", "jogo de panelas antiaderente", "jogo de panelas cerâmica",
        "caçarola", "panela de ferro", "frigideira antiaderente", "frigideira de inox",
        "frigideira grill", "wok", "leiteira", "cuscuzeira", "caldeirão", "panela de pressão inox",
        "assadeira de vidro", "assadeira antiaderente", "forma de pizza", "forma de pudim",
        "forma de silicone", "jogo de talheres", "faqueiro inox", "jogo de facas", "faca do chef",
        "afiador de facas", "tesoura de cozinha", "espátula de silicone", "concha de inox",
        "pegador de massas", "colher de pau", "abridor de vinho", "saca-rolhas", "porta talheres",
        "escorredor de pratos", "dispenser de detergente", "porta detergente", "porta esponja",
        "rodinho de pia", "lixeira de cozinha", "lixeira com pedal", "lixeira automática",
        "garrafa térmica de inox", "bule de inox", "jarra de vidro", "jarra de suco", "jarra térmica",
        "copo de vidro", "copo long drink", "taça de vinho", "taça de cristal", "jogo de canecas",
        "caneca de porcelana", "xícara de café", "pratos de porcelana", "prato fundo",
        "prato de sobremesa", "jogo de sobremesa", "saladeira", "travessa", "petisqueira",
        "porta bolo", "queijeira", "manteigueira", "açucareiro", "porta guardanapo", "sousplat",
        "toalha de mesa redonda", "caminho de mesa", "pote de vidro hermético", "pote térmico",
        "marmita térmica", "garrafa de vidro", "squeeze", "porta tempero giratório",
        "moedor de pimenta", "organizador de temperos", "porta pão", "tábua de frios",
        "balde de gelo", "forma de gelo", "coqueteleira",
        # Eletro de cozinha
        "liquidificador portátil", "batedeira planetária", "mixer de mão", "multiprocessador",
        "cafeteira elétrica", "cafeteira de cápsula", "chaleira elétrica inox", "fritadeira elétrica",
        "fritadeira sem óleo", "forno elétrico de bancada", "micro-ondas 20 litros",
        "micro-ondas 30 litros", "panela elétrica multifuncional", "máquina de waffle",
        "fogão de indução portátil", "cooktop 2 bocas", "cooktop 4 bocas", "coifa",
        "depurador de ar", "panificadora", "centrífuga de alimentos", "espremedor de laranja",
        "moedor de café", "mini forno", "detergente para lava louças",
    ],
    "quarto": [
        "travesseiro de pluma", "travesseiro viscoelástico", "travesseiro de corpo",
        "protetor de travesseiro", "lençol com elástico", "lençol de solteiro", "lençol queen",
        "jogo de lençol king", "edredom casal", "edredom queen", "cobertor de microfibra",
        "cobertor casal", "colcha matelassê", "saia para cama box", "colchão inflável",
        "cabeceira estofada", "penteadeira", "cômoda", "sapateira de porta", "organizador de sapatos",
        "cabide infantil", "organizador de roupas", "caixa organizadora com tampa", "saco a vácuo",
        "porta joias", "espelho de parede", "luminária de mesa", "ventilador de mesa", "persiana",
        "varão de cortina",
    ],
    "banheiro": [
        "jogo de banheiro", "kit banheiro", "toalha de banho gigante", "toalha de banho felpuda",
        "toalha de piso", "roupão de banho", "tapete de banheiro antiderrapante",
        "cortina de banheiro", "chuveiro elétrico", "ducha higiênica", "torneira de banheiro",
        "torneira de cozinha", "torneira gourmet", "espelho de banheiro", "armário de banheiro",
        "gabinete de banheiro", "kit acessórios banheiro", "porta toalha", "gancho adesivo",
        "prateleira de canto", "balança de banheiro", "lenço de papel", "hastes flexíveis",
        "sabonete líquido refil", "sabonete infantil",
        # Subitens (06/11, Gabriel): variações do mesmo item; o rodízio trata como um tipo só
        "ducha higiênica redonda", "ducha higiênica quadrada", "ducha higiênica branca",
        "ducha higiênica de plástico", "ducha higiênica cromada", "ducha higiênica com registro",
        "ducha higiênica preta",
        "cortina de tecido", "cortina de linho", "cortina blackout de tecido", "cortina rolô",
        "cortina de bambu", "persiana rolô", "cortina com ilhós",
    ],
    "sala": [
        "sofá cama", "poltrona decorativa", "puff baú", "rack para sala", "estante de livros",
        "mesa lateral", "mesa de centro de vidro", "tapete grande", "tapete felpudo", "tapete shaggy",
        "cortina de voil", "almofadas decorativas", "capa de almofada", "manta de tricô",
        "vaso de cerâmica", "planta artificial grande", "quadro para sala", "relógio de parede grande",
        "luminária pendente", "arandela", "lustre de cristal", "fita led", "caixa de som bluetooth",
    ],
    "moveis": [
        "mesa de jantar 4 lugares", "mesa de jantar 6 lugares", "cadeira de jantar",
        "cadeira estofada", "cadeira de madeira", "banqueta alta", "banco de madeira",
        "estante organizadora", "armário multiuso", "armário de cozinha", "balcão de cozinha",
        "carrinho organizador", "nicho", "prateleira de parede", "mesa de computador",
        "escrivaninha com gavetas", "estante de madeira", "mesa para escritório", "sapateira vertical",
        "suporte de tv de parede", "rack com painel para tv", "cortina para janela",
        "tela mosquiteira para janela", "lençol casal", "jogo de lençol casal",
        "tomada inteligente positivo", "lâmpada inteligente positivo", "câmera wi-fi positivo",
        # Pedidos de 05/11 (vistos nos canais que vendem bem): baú, cama, suportes de TV, prateleiras, lixeiras
        "baú recamier", "baú calçadeira", "calçadeira para cama", "cama de solteiro", "cama viúva",
        "cama box solteiro", "cama box viúva", "cama box king", "cama king size",
        "suporte de tv fixo", "suporte de tv com braço", "suporte de tv de teto", "suporte de tv giratório",
        "suporte para tv 32 a 55", "suporte para tv 55 a 75", "suporte de mesa para tv",
        "prateleira de madeira", "prateleira de parede decorativa", "prateleira organizadora",
        "lixeira com tampa", "lixeira de 30 litros", "lixeira de 100 litros", "lixeira dupla coleta seletiva",
    ],
    "eletro": [
        "ventilador de coluna", "ventilador de parede", "circulador de ar", "aquecedor a óleo",
        "climatizador de ar portátil", "desumidificador", "purificador de ar", "ferro a vapor",
        "vaporizador de roupas", "máquina de costura", "campainha sem fio", "filtro de linha",
        "luminária de emergência", "aspirador portátil", "aspirador de pó sem fio", "mop a vapor",
        "lâmpada inteligente wi-fi",
        # Cuidado pessoal (as mulheres compram muito) e massagem
        "secador de cabelo", "escova secadora", "prancha de cabelo", "modelador de cachos",
        "massageador de pés", "massageador elétrico", "massageador de pescoço", "soprador de folhas",
        "passadeira a vapor", "secador de roupas",
        # Pedidos de 05/11
        "impressora multifuncional", "impressora tanque de tinta", "impressora wi-fi", "estabilizador",
        "estabilizador 300va", "filtro de linha 6 tomadas", "filtro de linha com usb", "régua de tomadas",
        "extensão elétrica", "benjamim t", "adaptador de tomada", "removedor de pelos de roupa",
        "aparador de pelos", "tira pelos elétrico", "ar condicionado portátil",
    ],
    "limpeza": [
        "vassoura de pelo", "vassoura mágica", "rodo mágico", "pá de lixo", "kit vassoura e pá",
        "balde com espremedor", "balde dobrável", "esfregão", "flanela", "pano de microfibra",
        "esponja dupla face", "lã de aço", "detergente concentrado", "sabão de coco",
        "sabão líquido para roupas", "amaciante concentrado", "desinfetante perfumado",
        "limpador perfumado", "desengordurante", "tira limo", "limpador de piso", "cera para piso",
        "inseticida", "repelente elétrico", "bloco sanitário", "gel sanitário",
        "desodorizador sanitário", "spray aromatizador", "difusor de varetas",
        "água perfumada para roupas", "prendedor de roupa de madeira", "carrinho de feira",
        # Pedidos de 05/11
        "espuma desengordurante", "limpa grelha", "limpa forno", "limpa air fryer", "rolo tira pelos",
        "rolo adesivo para roupa", "escova tira pelos de pet", "removedor de fiapos",
    ],
    "externa": [
        "conjunto de jardim", "espreguiçadeira", "ombrelone", "rede de dormir", "mesa de jardim",
        "churrasqueira a carvão", "churrasqueira elétrica", "espeto de churrasco",
        "tábua para churrasco", "kit espetos", "cooler", "garrafão térmico", "refletor led",
        "aspersor de jardim", "tesoura de poda", "carrinho de mão", "escada de alumínio",
        "jogo de ferramentas", "caixa de ferramentas", "parafusadeira", "furadeira", "trena",
        "tábua de madeira para churrasco", "churrasqueira de bafo", "grill de mesa",
        "escova para limpar churrasqueira", "escova de aço para grelha", "limpa grelha de churrasqueira",
    ],
}
# Expansão de 06/11 (pedido do Gabriel: passar de 392 para 500+ itens e muito mais subitens, só coisas de
# casa, nada chamativo). 137 itens novos e 307 subitens novos; conferido para não repetir os que já existiam.
PALAVRAS_MAIS_2 = {
    "cozinha": [
        "moedor de pimenta elétrico", "moedor de sal e pimenta", "cafeteira italiana de alumínio",
        "cafeteira italiana inox", "prensa francesa", "chaleira esmaltada", "chaleira com apito",
        "leiteira antiaderente", "cuscuzeira de inox", "wok antiaderente", "frigideira de ferro",
        "frigideira funda", "frigideira para ovo", "grelha de ferro", "chapa de ferro para fogão",
        "chapa bifeteira", "sanduicheira de fogão", "ralador de inox 4 faces", "fatiador de legumes",
        "mandolina fatiador", "descascador de legumes", "espremedor de alho", "espremedor de limão",
        "abridor de latas", "saca-rolhas elétrico", "porta temperos", "porta temperos giratório",
        "porta temperos de vidro", "porta talheres de bambu", "peneira de inox", "funil de inox",
        "pegador de massa", "kit espátulas de silicone", "fouet de inox", "rolo de massa",
        "tapete de silicone para forno", "forma de cupcake", "boleira com tampa", "fruteira de mesa",
        "fruteira de chão", "galheteiro", "travessa de porcelana", "travessa refratária",
        "jogo americano de fibra", "guardanapo de tecido", "kit pano de prato", "avental de cozinha",
        "descanso de panela", "balança de cozinha digital", "timer de cozinha", "termômetro culinário",
        "filtro de torneira", "panela de barro", "caldeirão de alumínio", "forma de pão",
        "pipoqueira de inox", "pipoqueira de alumínio", "fondue", "kit fondue", "cortador de pizza",
        "bloco de facas", "jarra medidora", "colher medidora", "copo medidor", "kit potes de mantimentos",
        "pote para mantimentos", "porta cápsulas", "suporte para cápsulas de café",
        "copo térmico com tampa", "caneca térmica", "garrafa squeeze", "pilão de madeira", "almofariz",
        "pincel culinário de silicone", "bico de confeitar", "kit bico de confeitar", "batedor de ovos",
        "tigela de vidro", "bowl de cerâmica", "kit tigelas", "forma de gelo de silicone", "kit caipirinha",
        "decanter", "suqueira", "dispenser de bebidas", "porta azeite", "triturador de alho",
        "mini processador", "marmiteira elétrica",
    ],
    "quarto": [
        "protetor de colchão impermeável", "pillow top", "pillow top casal", "travesseiro de espuma",
        "travesseiro cervical", "travesseiro ortopédico", "kit fronhas", "mesa de cabeceira",
        "penteadeira com espelho", "cômoda 4 gavetas", "espelho de corpo inteiro", "abajur de cabeceira",
        "luminária de cabeceira", "cabide de veludo", "kit cabides", "organizador de closet",
        "colmeia organizadora", "manta de sofá e cama", "jogo de cama king", "lençol de malha",
        "cortina para quarto", "tapete para quarto", "mosquiteiro", "mosquiteiro de cama", "dossel",
        "relógio despertador", "despertador digital",
    ],
    "banheiro": [
        "porta escova de dente", "dispenser de sabonete", "dispenser de sabonete automático",
        "toalheiro de parede", "toalheiro elétrico", "prateleira de vidro",
        "prateleira de banheiro de inox", "kit lavabo", "porta maquiagem", "cesto de roupa de banheiro",
        "tapete de banheiro de algodão", "chuveiro a gás", "chuveiro com pressurizador", "chuveiro de teto",
        "chuveiro inteligente", "registro de chuveiro", "misturador de banheiro", "cuba de apoio",
        "cuba de banheiro", "vaso sanitário", "assento sanitário almofadado",
        "box para banheiro", "porta xampu de canto", "nicho de banheiro", "espelho com led",
        "espelho redondo de banheiro", "tapete de box", "barra de apoio", "barra de apoio para banheiro",
        "banco para banho", "espelho de aumento", "organizador de pia", "máquina de cortar cabelo",
        "aparador de barba", "barbeador elétrico", "depilador elétrico", "irrigador oral",
    ],
    "sala": [
        "mesa de centro redonda", "mesa lateral de sala", "vaso de cerâmica decorativo", "cachepot",
        "kit capas de almofada", "cesto de vime", "cesto decorativo", "abajur de mesa", "difusor elétrico",
        "vela aromática", "castiçal", "bandeja decorativa", "espelho redondo", "espelho decorativo redondo",
        "tapete de sala grande", "tapete redondo", "porta controle remoto", "suporte para controle",
        "escultura decorativa", "enfeite de mesa", "flor artificial", "arranjo de flores artificiais",
        "relógio de mesa", "porta revistas", "aparador de livros", "globo decorativo", "quadro de cortiça",
        "lousa decorativa",
    ],
    "moveis": [
        "mesa dobrável de parede", "cadeira dobrável", "buffet", "buffet para sala", "cristaleira",
        "mesa de canto", "armário de lavanderia", "armário para lavanderia", "beliche", "bicama",
        "cama auxiliar", "cadeira gamer", "mesa para notebook", "suporte para notebook",
        "apoio para os pés", "estante de escritório", "gaveteiro de escritório", "arquivo de aço",
        "mesa de jantar redonda", "conjunto de mesa e cadeiras", "banco baú", "recamier",
        "mesa de cabeceira suspensa", "rack suspenso", "painel ripado", "biombo", "biombo decorativo",
        "carrinho bar", "carrinho de chá", "estante escada", "mesa bistrô", "conjunto bistrô",
        "mesa de bar", "cadeira de balanço", "bancada de trabalho",
    ],
    "eletro": [
        "cafeteira programável", "moedor de café elétrico", "grill e sanduicheira", "batedeira de mão",
        "espremedor de frutas elétrico", "centrífuga de frutas", "purificador de água gelada",
        "umidificador de ar", "aquecedor de ambiente", "extratora de limpeza", "enceradeira",
        "câmera de segurança wi-fi", "câmera de segurança externa", "sensor de presença",
        "luminária de led", "fita de led", "chaleira elétrica de inox", "forno micro-ondas",
        "liquidificador de alta potência", "sorveteira", "máquina de crepe", "panquequeira",
        "iogurteira elétrica", "máquina de pão", "bebedouro de garrafão", "mini lavadora de roupas",
        "olho mágico digital", "cadeado", "cadeado com senha",
    ],
    "limpeza": [
        "mop de microfibra", "pano multiuso reutilizável", "escova de limpeza elétrica",
        "removedor de manchas", "saco de lixo reforçado", "lava roupas líquido", "varal de chão dobrável",
        "suporte para vassoura", "porta sacolas", "dispensador de sacolas", "balde mop", "rodo de pia",
        "limpa estofados", "desentupidor", "desentupidor de pia", "limpa ralo", "álcool 70",
        "robô limpa vidros", "escova para roupa", "removedor de bolinhas de roupa",
    ],
    "externa": [
        "mangueira de jardim 30 metros", "esguicho de alta pressão", "vaso autoirrigável",
        "cadeira de área externa", "cadeira de piscina", "lona de piscina", "acendedor de carvão",
        "pegador de churrasco", "faca de churrasco", "tábua de carne", "avental de churrasco",
        "nível a laser", "jogo de chaves", "alicate", "martelo", "serra tico-tico", "esmerilhadeira",
        "lixadeira", "kit brocas", "jogo de soquetes", "chave de fenda elétrica", "kit ferramentas",
        "caixa organizadora de ferramentas", "escada dobrável", "carrinho de compras dobrável",
        "lanterna recarregável", "luminária solar de jardim", "refletor solar",
        "pendente para área gourmet", "cortador de grama", "cortador de grama elétrico",
        "aparador de grama", "pulverizador", "pulverizador de jardim", "tesoura de grama",
        "pá de jardinagem", "luva de jardinagem", "gazebo", "tenda", "cadeira de camping",
        "mesa de camping", "bolsa térmica",
    ],
}
# Produtos vistos pelo Gabriel numa loja boa da Shopee (Magazine MGP, nota 4,9, 06/11): o item, o subitem e o
# produto específico com marca. Ficaram de fora brinquedo, itens do Mickey (chamativos) e desodorante.
PALAVRAS_MAIS_3 = {
    "cozinha": [
        "garrafa térmica 1 litro", "garrafa térmica Tuut", "garrafa térmica Jade", "garrafa térmica Khadija",
        "garrafa térmica dourada", "jogo de panelas de indução", "jogo de panelas cerâmica 7 peças",
        "jogo de panelas fundo triplo", "panela de pressão de indução", "panela de pressão 4,2 litros",
        "caldeirão de cerâmica", "caldeirão de indução", "frigideira grill", "bistequeira",
        "chaleira Mimo Style", "chaleira inox com apito", "cuscuzeira Lyor", "cuscuzeira individual",
        "descanso de panela de bambu", "kit descanso de panela", "organizador de talheres de bambu",
        "jogo americano de bambu", "porta pão de bambu", "açucareiro de bambu",
        "potes de vidro com tampa de bambu", "porta condimentos de vidro", "abridor de coco",
        "torre de chopp", "porta copos", "jogo de porta copos",
    ],
    "banheiro": [
        "jogo de banheiro de porcelana", "kit banheiro de bambu", "kit banheiro Lyor",
        "máquina de cortar cabelo Wahl", "barbeador Wahl", "enxaguante bucal",
    ],
    "quarto": [
        "guarda-roupa dobrável", "guarda-roupa de tecido", "arara closet com prateleira",
    ],
    "eletro": [
        "purificador de água New Up", "purificador de água não elétrico", "purificador de água Electrolux",
        "fogão elétrico portátil", "cooktop portátil Elgin", "fogareiro elétrico duplo",
        "mini processador Mallory", "triturador de alimentos", "air fryer Mallory", "air fryer de vidro",
        "grill Cadence", "escova secadora Cadence", "omeleteira elétrica", "pipoqueira elétrica sem óleo",
        "chaleira elétrica de porcelana", "extratora Vonder", "robô aspirador com mop",
        "liquidificador portátil",
    ],
    "externa": [
        "furadeira parafusadeira 12v", "parafusadeira a bateria", "cortador de piso e azulejo",
        # Natal (época boa de venda; decoração de casa)
        "árvore de natal", "árvore de natal 180cm", "pisca pisca led", "enfeite de natal", "guirlanda de natal",
    ],
}
# Aba "Casa" do app de afiliados com COMISSÃO EXTRA (8% a 25%), vista pelo Gabriel em 06/11. Muito Natal e
# Ano Novo (época de venda forte). Natal/Ano Novo não passam pelo filtro de cor sóbria (ver pede_cor_sobria).
PALAVRAS_MAIS_4 = {
    "sala": [
        "decoração de natal de mesa", "kit decoração de natal", "almofada de natal", "capa de almofada de natal",
        "porta bombom de natal", "mini árvore de natal", "árvore de natal 1,50m", "árvore de natal pinheiro",
        "enfeites para árvore de natal", "bolinhas de natal", "saia para árvore de natal",
        "cordão de luz de natal", "pisca pisca 100 leds", "cortina de led", "cortina de luz fada",
        "decoração de ano novo", "kit balão ano novo", "espelho orgânico", "espelho flame",
        "luminária de nossa senhora",
    ],
    "cozinha": [
        "toalha de mesa de natal", "toalha de mesa retangular 6 lugares", "jogo americano de natal",
        "kit marmitas 750ml", "potes marmita com trava", "abridor de lata automático", "taça de vidro diamante",
        "kit taças de vidro", "recipiente para frutas e verduras", "forma de gelo com tampa", "amolador de facas",
    ],
    "limpeza": [
        "percarbonato de sódio", "tira manchas oxi", "sabão líquido 5 litros", "sabão líquido Omo 5 litros",
        "eliminador de odor de pet", "desinfetante para xixi de cachorro",
    ],
    "banheiro": [
        "kit toalha de banho", "kit 4 toalhas de banho", "torneira dourada de banheiro",
    ],
    "quarto": [
        "cortina blackout pvc", "sapateira basculante", "prateleira de canto mdf",
    ],
    "externa": [
        "tela de sombreamento", "tela de sombreamento 98%", "cordão de luz solar", "churrasqueira portátil a bafo",
        "parafusadeira 25v", "parafusadeira Nakasaki", "kit ferramentas maleta",
    ],
}
# Segundo lote da mesma aba (06/11). Pétalas de rosa (casamento) ficaram de fora.
PALAVRAS_MAIS_5 = {
    "sala": [
        "bolas de natal 3cm", "kit bolas de natal com estrela", "enfeite de natal personalizado",
        "balão feliz natal", "cascata de luzes de natal", "luminária de natal", "prendedor de cortina de natal",
        "cordão de led solar 300 leds", "revestimento ripado autocolante", "painel ripado adesivo",
        "umidificador difusor com essências",
    ],
    "cozinha": [
        "escorredor de pratos preto", "escorredor de louça de aço inox", "borrifador de azeite", "spray de azeite",
        "jogo americano redondo", "balança de cozinha 10kg", "assadeira de inox com tampa",
        "conjunto de panelas 10 peças", "copo de vidro canelado", "kit potes herméticos com tampa de bambu",
        "cortador de legumes em cubos", "picador de legumes", "kit peneira de inox", "mini seladora de embalagens",
    ],
    "quarto": [
        "kit 50 cabides de veludo", "cesto organizador com tampa de bambu", "organizador de cobertor",
        "saco organizador de roupa", "colmeia organizadora de gaveta", "cabideiro de porta", "gancho de porta",
    ],
    "banheiro": [
        "rack de banheiro", "kit acessórios de banheiro preto e dourado",
    ],
    "limpeza": [
        "lixeira com sensor",
    ],
    "externa": [
        "lona impermeável", "bico de mangueira alta pressão", "mangueira expansível",
    ],
}
# Lista de desejos da Amazon do Gabriel (06/11): coador, garrafa de café, prateleira de banheiro, porta treco,
# tigelas inox/madeira, formas inox e o que vai em cima/embaixo da panela para não queimar nem respingar.
PALAVRAS_MAIS_6 = {
    "cozinha": [
        "coador de café", "coador de café de inox", "coador de café permanente", "coador de pano",
        "suporte para coador de café", "garrafa térmica para café", "garrafa térmica Termopro",
        "bowl de inox", "conjunto de tigelas de inox", "tigela de inox", "bowl de madeira", "tigela de madeira",
        "saladeira de madeira", "kit formas de inox", "forma de inox", "forma de bolo de inox",
        "difusor de calor para fogão", "chapa difusora para panela", "tela anti respingo", "tampa anti respingo",
    ],
    "banheiro": [
        "prateleira de canto para banheiro", "porta shampoo de inox", "porta shampoo de canto",
        "prateleira de banheiro sem furar", "porta shampoo preto", "escova de banho cabo longo",
        "touca de banho",
    ],
    "sala": [
        "porta treco", "bandeja organizadora de couro", "porta chaves de mesa", "suporte de celular de mesa",
    ],
}
# Gadgets baratinhos que viralizam na Shopee (Gabriel, 06/11): triturador de puxar na cordinha, caneca que
# mexe o café sozinha, mixer de leite/cappuccino de apertar o botão e outros "negocinhos" de cozinha
PALAVRAS_MAIS_7 = {
    "cozinha": [
        "triturador manual de puxar", "mini triturador de alimentos manual", "processador manual de alimentos",
        "triturador de alho manual", "picador de alimentos manual",
        "caneca mixer automática", "caneca magnética mixer", "caneca autoagitadora",
        "mixer de leite", "batedor de leite elétrico", "espumador de leite", "mixer para cappuccino",
        "mini batedor elétrico de mão", "mixer para café",
        "cortador de legumes espiral", "fatiador de ovos", "separador de gema", "abridor de pote",
        "descascador de alho de silicone", "porta temperos magnético", "copo medidor", "colher medidora digital",
        "organizador de tampas de panela", "dispenser de arroz",
        # geladeira: os potinhos de plástico/acrílico para ovo, leite, frutas...
        "porta ovos para geladeira", "organizador de geladeira com tampa", "kit organizador de geladeira",
        "organizador de geladeira para latas", "pote organizador de geladeira",
        # temperos: prateleira que gira
        "porta temperos giratório", "organizador giratório de temperos", "prateleira giratória de temperos",
        # facas na parede
        "suporte magnético para facas", "barra magnética para facas", "porta facas de parede",
    ],
    "limpeza": [   # lavanderia
        "dispenser de sabão em pó", "dispenser de amaciante", "porta sabão líquido com dosador",
        "kit potes para lavanderia", "organizador de lavanderia com dosador", "pote para sabão em pó com tampa",
    ],
}
for _mais in (PALAVRAS_MAIS, PALAVRAS_MAIS_2, PALAVRAS_MAIS_3, PALAVRAS_MAIS_4, PALAVRAS_MAIS_5, PALAVRAS_MAIS_6,
              PALAVRAS_MAIS_7):
    for _cat, _lista in _mais.items():
        PALAVRAS[_cat] = PALAVRAS[_cat] + [p for p in _lista if p not in PALAVRAS[_cat]]
# Produtos caros (os que dão mais comissão): têm um rodízio só deles e saem com mais frequência
CARO_A_CADA_MIN = 3    # fora do pico: 1 caro a cada 3 ou 4 posts (sorteado)
CARO_A_CADA_MAX = 4
CARO_PICO_MIN = 2      # no pico (18h-20h, quando mais gente compra): 1 caro a cada 2 ou 3 posts
CARO_PICO_MAX = 3
CAROS = [
    "geladeira", "fogão", "smart tv", "caixa de som", "guarda-roupa", "toalha buddemeyer",
    "mesa de escritório", "cama box", "sofá", "colchão", "máquina de lavar",
    "ar-condicionado", "robô aspirador", "air fryer oven", "cobertor karsten",
    "cadeira de escritório ergonômica", "babá eletrônica", "soundbar", "fechadura digital",
    "lava louças", "cama de casal", "lava e seca", "freezer", "fogão 5 bocas", "adega",
    "sofá retrátil", "cooktop de indução", "guarda-roupa casal",
    "geladeira frost free", "geladeira duplex", "geladeira inverse", "fogão 4 bocas",
    "forno de embutir", "máquina de lavar 12kg", "máquina de lavar 15kg", "tanquinho",
    "ar condicionado split", "ar condicionado inverter", "smart tv 75", "smart tv 4k",
    "home theater", "sofá 3 lugares", "sofá de canto", "conjunto de sala de jantar",
    "cama box casal", "cama box queen", "colchão casal", "colchão queen", "guarda-roupa 6 portas",
    "cozinha compacta", "frigobar", "freezer vertical", "poltrona do papai",
    "mesa regulável de altura", "cadeira de escritório presidente", "janela de alumínio",
    "rack para tv 65", "guarda-roupa solteiro",
    "impressora multifuncional tanque de tinta", "cama box king", "colchão king", "cama box viúva",
    "ar condicionado 9000 btus", "ar condicionado 12000 btus", "ar condicionado 18000 btus",
    # Campanha Brastemp do canal Criadores e Afiliados Shopee (06/11): 15% de comissão em vendas por redes sociais
    "máquina de lavar Brastemp 18kg", "máquina de lavar Brastemp 14kg", "lava louças Brastemp 8 serviços",
    "geladeira Brastemp frost free duplex 415 litros", "geladeira Brastemp frost free 412 litros inox",
    "geladeira Brastemp frost free duplex 333 litros", "freezer horizontal 528 litros", "freezer 142 litros",
    # Geladinha de escritório, freezer de mercado, cervejeira, adega e churrasqueira
    "frigobar retrô", "frigobar pequeno", "freezer horizontal", "freezer horizontal 2 portas",
    "cervejeira", "geladeira expositora", "adega de vinho", "churrasqueira a gás",
    "churrasqueira elétrica grande", "cadeira de massagem", "poltrona massageadora",
    # TV: vários tamanhos para variar (a marca é sorteada na busca: ver MARCAS_POR_TIPO)
    "smart tv 32", "smart tv 43", "smart tv 50", "smart tv 55", "smart tv 58", "smart tv 60", "smart tv 65",
    # Mesa de jantar: mais garagens (antes só "conjunto de sala de jantar" e saía sempre a mesma busca)
    "conjunto sala de jantar 6 cadeiras", "conjunto sala de jantar 4 cadeiras", "mesa de jantar madeira maciça",
]
# Bebê e beleza saíram do Casa (06/11, Gabriel: "pode tirar"): agora são do bot Geral (Achadinhos & Promoções)
FORA_DO_CASA = ["lenço umedecido", "sabonete infantil", "máquina de cortar cabelo", "máquina de cortar cabelo Wahl",
                "aparador de barba", "aparador de pelos", "barbeador elétrico", "barbeador Wahl", "depilador elétrico",
                "secador de cabelo", "escova secadora", "escova secadora Cadence", "prancha de cabelo",
                "modelador de cachos", "babá eletrônica"]
PALAVRAS = {cat: [p for p in lista if p not in FORA_DO_CASA] for cat, lista in PALAVRAS.items()}
CAROS = [p for p in CAROS if p not in FORA_DO_CASA]
PRECO_MINIMO_CARO = 100   # produto caro abaixo disso é acessório (ex.: organizador de geladeira)
# Marcas conhecidas: produto simples com marca tem preferência; produto caro precisa ter marca
MARCAS = [
    # Eletro e eletrônicos
    "Electrolux", "Brastemp", "Consul", "Mondial", "Philco", "Britânia", "Arno", "Oster",
    "Walita", "Philips", "Black+Decker", "Black Decker", "Cadence", "Mallory", "Lenoxx",
    "Hamilton Beach", "KitchenAid", "Cuisinart", "Midea", "Panasonic", "Samsung", "LG", "TCL",
    "Sony", "JBL", "Multilaser", "Positivo", "Xiaomi", "Elgin", "Gree", "Springer", "Agratto",
    "Ventisol", "WAP", "Kärcher", "Fischer", "Esmaltec", "Dako", "Continental", "Atlas",
    "Lorenzetti", "Hydra", "Fame", "Nespresso", "Dolce Gusto", "Três Corações", "Polishop",
    "Motorola", "Intelbras", "Yale", "Papaiz", "KaBuM", "AOC", "Semp", "Toshiba",
    # Freezer, cervejeira e expositor (de mercado) e churrasqueira
    "Metalfrio", "Gelopar", "Fricon", "Venax", "Imbera", "Arke",
    # Cabelo, massagem e jardim
    "Taiff", "Gama Italy", "Babyliss", "Wahl", "Relaxmedic", "Vonder",
    # Impressora, estabilizador, filtro de linha e limpeza de forno/grelha
    "Epson", "HP", "Canon", "Brother", "Ragtech", "TS Shara", "Force Line", "iClamper", "Zip Clean", "My Place", "3M",
    # Vistas na Magazine MGP (06/11)
    "Mimo Style", "Ecokitchen", "Tuut", "New Up", "Famastil", "Razi", "Nakasaki", "Termopro",
    # Alexa, casa inteligente e TV (Alexa/Google em "compatível com Alexa" não contam)
    # ("Google" e "Amazon" não entram: "Interruptor Tuya Alexa Google" passava como marca)
    "Echo Dot", "Echo Pop", "Echo Show", "Fire TV Stick", "Chromecast", "Roku", "TP-Link", "Tapo",
    # Higiene
    "Nivea", "Dove", "Protex", "Palmolive", "Giorno Bagno", "Francis", "Granado", "Phebo",
    "Lux", "Johnson's", "Johnson", "Huggies", "Pampers", "Turma da Mônica",
    "Marco Boni", "Ricca", "Océane",
    "Curaprox", "Oral-B", "Colgate", "Sensodyne", "Listerine",
    # Papel higiênico e papel toalha ("Neve" em "Branco Neve" não conta: ver sem_assistente)
    "Neve", "Personal", "Mili", "Scott", "Snob",
    # Banheiro, luz e organização
    "Astra", "Tigre", "Avant", "Taschibra", "Ourolux", "Paramount", "Martiplast", "Arthi",
    "Oxford", "Porto Brasil", "Biona", "Stanley", "Tron", "Venti-Delta", "Libell",
    "Coleman", "Invicta", "Secalux", "Termolar", "Kleenex", "Deca", "Docol", "Suggar", "Singer",
    "Clamper", "Artely", "Tecnomobili", "Carraro", "São Carlos",
    # Ferramentas e inseticidas
    "Bosch", "Vonder", "SBP", "Raid", "Baygon",
    # Suporte de TV
    "ELG", "Brasforma", "Multivisão",
    # Filtro de água
    "Stéfani", "São João", "IBBL", "Latina",
    # Cozinha e utilidades
    "Tramontina", "Brinox", "Rochedo", "Panelux", "Clock", "Eirilar", "Nigro",
    "Marinex", "Nadir", "Duralex", "Tupperware", "Mor", "Ewel",
    "Plasútil", "Sanremo", "Ordene", "Coza", "Euro Home", "Wolff", "Lyor", "Ceraflame", "Tefal",
    # Cama, mesa e banho
    "Buddemeyer", "Santista", "Karsten", "Altenburg", "Teka", "Camesa", "Döhler", "Trussardi",
    "Ortobom", "Castor", "Probel", "Herval", "Fibrasca", "Duoflex", "Lepper", "Corttex",
    # Móveis
    "Madesa", "Politorno", "Kappesberg", "Bertolini", "Itatiaia", "Mobly", "Tok&Stok",
    # Limpeza
    "Ypê", "Omo", "Ariel", "Downy", "Minuano", "Limpol",
    "Scotch-Brite", "Scotch Brite", "Bombril", "Flash Limp", "Pinho Sol", "Lysoform",
    "Vanish", "Mr Músculo", "Condor", "Bettanin", "Noviça", "Brilhante", "Tixan", "Surf",
    "Comfort", "Perfex", "Glade", "Bom Ar", "Via Aroma", "Qboa", "Poliflor", "Peroba",
    "Mucambo", "Harpic", "Cif", "Finish", "Ajax",
]
# Tipos com marca forte: o bot também busca "produto + marca" e só posta se a marca for
# uma das marcas do tipo (vale o trecho mais longo que combinar com a palavra buscada)
MARCAS_POR_TIPO = [
    (["panela", "panelas", "frigideira", "panela de pressão", "assadeira", "forma de bolo", "faqueiro",
      "talheres", "faca de cozinha", "utensílios", "conjunto de facas", "cafeteira italiana",
      "chaleira de inox", "ralador", "descascador", "escorredor de macarrão", "caçarola", "wok",
      "leiteira", "cuscuzeira", "caldeirão", "jogo de facas", "faca do chef", "afiador",
      "tesoura de cozinha", "forma", "concha", "pegador", "colher de pau", "bule de inox"],
     ["Tramontina", "Panelux", "Rochedo", "Brinox", "Clock", "Eirilar", "Ceraflame", "Tefal"]),
    (["organizador", "organizadora", "porta mantimentos", "pote de mantimentos", "dispenser de cereais",
      "porta frios", "porta papel toalha", "dosador", "porta sabão", "fruteira", "cesta de pão",
      "baú organizador"],
     ["Ordene", "Coza", "Paramount", "Martiplast", "Arthi", "Plasútil", "Sanremo", "Electrolux",
      "Brinox", "Euro Home", "Tupperware", "Lyor"]),
    (["papel higiênico"], ["Neve", "Personal", "Mili", "Scott", "Snob"]),
    (["papel toalha"], ["Snob", "Scott", "Neve", "Personal", "Mili"]),
    (["escova de dente", "creme dental", "enxaguante bucal"],
     ["Curaprox", "Oral-B", "Colgate", "Sensodyne", "Listerine"]),
    (["varal"], ["Mor", "Secalux", "Tramontina", "Brinox"]),
    (["assento sanitário"], ["Astra", "Tigre"]),
    (["caixa térmica"], ["Coleman", "Invicta", "Mor"]),
    (["panela esmaltada", "bule esmaltado", "esmaltada", "esmaltado"],
     ["Ewel", "Tramontina", "Rochedo", "Brinox"]),
    (["filtro de barro"], ["Stéfani", "São João"]),
    (["filtro de água", "purificador de água", "purificador", "bebedouro"],
     ["Electrolux", "Brastemp", "Consul", "IBBL", "Latina", "Esmaltec", "Lorenzetti", "Libell"]),
    (["smart tv"], ["Samsung", "LG", "TCL", "AOC", "Philips", "Philco", "Toshiba", "Semp", "Roku",
                    "Sony"]),
    (["bucha de banho", "bucha vegetal", "esponja de banho"], ["Marco Boni", "Ricca", "Océane"]),
    (["aromatizador", "difusor de aromas"], ["Glade", "Bom Ar", "Via Aroma"]),
    (["air fryer", "liquidificador", "batedeira", "mixer", "sanduicheira", "cafeteira", "chaleira",
      "processador", "panela elétrica", "micro-ondas", "forno elétrico", "ferro de passar",
      "aspirador de pó", "ventilador", "climatizador", "aquecedor", "umidificador", "vaporizador",
      "pipoqueira", "grill", "torradeira", "espremedor", "panela de pressão elétrica",
      "fritadeira", "multiprocessador", "panificadora", "centrífuga", "moedor de café", "mini forno",
      "coifa", "depurador", "máquina de waffle", "fogão de indução", "mop a vapor", "circulador",
      "desumidificador", "purificador de ar"],
     ["Mondial", "Electrolux", "Philco", "Britânia", "Arno", "Oster", "Cadence", "Walita",
      "Philips", "Black+Decker", "Black Decker", "WAP", "Ventisol", "Midea", "Nespresso",
      "Dolce Gusto", "Três Corações", "Tron", "Venti-Delta", "Suggar", "Fischer"]),
    (["inseticida", "repelente"], ["SBP", "Raid", "Baygon"]),
    (["lençol", "edredom", "cobertor", "toalha de banho", "toalha de rosto", "jogo de toalhas",
      "travesseiro", "colcha", "fronha", "roupão", "jogo de cama", "cobre leito",
      "manta de microfibra", "toalha de mão"],
     ["Santista", "Buddemeyer", "Karsten", "Altenburg", "Teka", "Camesa", "Döhler", "Fibrasca",
      "Ortobom", "Duoflex"]),
    (["pote", "marmita", "lancheira"], ["Electrolux", "Tupperware", "Sanremo", "Plasútil", "Marinex"]),
    (["porta escova", "porta cotonete", "porta algodão", "saboneteira", "dispenser sabonete",
      "organizador de banheiro", "prateleira de banheiro", "espelho", "tapete de pedra",
      "porta papel higiênico", "porta shampoo", "toalheiro"],
     ["Lyor", "Coza", "Ordene", "Euro Home"]),
    (["manta para sofá", "capa de sofá", "almofada", "tapete de sala", "cortina sala"],
     ["Döhler", "Karsten", "Lepper", "Corttex", "Santista", "Camesa"]),
    (["controle remoto"], ["Samsung", "LG", "TCL", "Philco", "Sony", "Philips", "AOC", "Semp",
                           "Toshiba", "Panasonic"]),
    (["detergente", "sabão", "amaciante", "desinfetante", "esponja", "bucha", "pano de chão",
      "pano multiuso", "tira manchas", "percarbonato", "água sanitária", "alvejante",
      "lustra móveis", "limpa vidros", "limpador", "luva de limpeza", "pedra sanitária",
      "escova sanitária", "saco de lixo"],
     ["Ypê", "Omo", "Ariel", "Brilhante", "Tixan", "Surf", "Comfort", "Downy", "Vanish", "Pinho Sol",
      "Scotch-Brite", "Bombril", "Flash Limp", "Bettanin", "Perfex", "Limpol", "Minuano", "Qboa",
      "Poliflor", "Peroba", "Mucambo", "Harpic", "Cif", "Mr Músculo", "Lysoform", "Condor",
      "Finish", "Ajax"]),
    (["sabonete", "sabonete líquido", "sabonete em barra", "sabonete de glicerina"],
     ["Giorno Bagno", "Francis", "Palmolive", "Granado", "Phebo", "Dove", "Nivea", "Protex", "Lux",
      "Johnson's", "Johnson"]),
    (["lenço umedecido"], ["Huggies", "Pampers", "Johnson's", "Johnson", "Turma da Mônica"]),
    # 08/11, Gabriel: "chuveiro tem que ser um Lorenzetti, um trem mais bom" (a ducha higiênica não: ver abaixo)
    (["chuveiro", "chuveiro elétrico", "ducha elétrica"],
     ["Lorenzetti", "Hydra", "Fame", "Zagonel", "Corona", "Enerbras", "Deca", "Docol"]),
]
MARCAS = MARCAS + [m for m in ["Zagonel", "Corona", "Enerbras", "Deca", "Docol"] if m not in MARCAS]
# MARCA À VONTADE (08/11, Gabriel: "não precisa ser necessariamente de marca... ventilador de teto, capa de sofá,
# mesa, garrafa, mousepad, coisinha mais besta"; "aspirador, cama, um pouquinho de marca, não necessariamente").
# Nesses tipos a marca deixa de ser obrigatória (mesmo no caro e no tipo de marca forte acima): o bot continua
# buscando "produto + marca" e a de marca ganha na escolha (loja comum com marca vem antes da sem marca), mas o
# sem marca bem avaliado também pode sair. Obrigatória continua: geladeira, TV e os caros em geral, chuveiro,
# eletro de cozinha (air fryer...), panela, filtro, limpeza e higiene.
MARCA_OPCIONAL = [
    "ventilador", "circulador", "capa de sofá", "protetor de sofá", "manta para sofá", "manta", "almofada",
    "tapete", "cortina", "organizador", "organizadora", "porta mantimentos", "pote", "marmita", "lancheira",
    "porta frios", "porta papel toalha", "dosador", "porta sabão", "fruteira", "cesta de pão", "baú organizador",
    "dispenser de cereais", "porta escova", "porta cotonete", "porta algodão", "saboneteira", "dispenser sabonete",
    "prateleira de banheiro", "espelho", "porta papel higiênico", "porta shampoo", "toalheiro", "varal",
    "aspirador de pó", "aspirador vertical", "aspirador portátil", "lençol", "jogo de lençol", "edredom", "cobertor",
    "travesseiro", "colcha", "fronha", "jogo de cama", "cobre leito", "toalha", "roupão", "mesa", "cama",
    "garrafa", "copo térmico", "mousepad", "caixa térmica", "aromatizador", "difusor de aromas", "bucha de banho",
    "ducha higiênica", "luminária", "umidificador",
    # 08/11 (prints da Shopee com comissão extra): coisinha de casa que vende muito sem marca
    "utensílios de silicone", "forma de gelo", "cobre leito", "peseira", "nicho", "cesto de roupa",
]

def marca_opcional(palavra):
    busca = normalizar(palavra or "")
    if "robo" in busca:                        # robô aspirador sem marca é bomba
        return False
    # (aceita o plural: "potes herméticos" é "pote")
    return any(re.search(r"(?<!\w)" + re.escape(normalizar(t)) + r"(?:s|es)?(?!\w)", busca) for t in MARCA_OPCIONAL)
VENDAS_MINIMAS_MARCA = 1000  # (não usado desde 06/11: régua única de 1000+ vendas abaixo de R$ 200)
# IA (Gemini) para deixar o nome do post natural. Precisa da linha GEMINI_KEY=... no config.txt;
# sem ela, ou se a IA falhar ou devolver nome ruim, o bot usa as regras de limpeza de sempre.
GEMINI_MODELO = "gemini-3.5-flash-lite"
REVISOES_IA_POR_BUSCA = 2   # se a IA recusar, tenta o próximo produto (no máximo 2 por busca)
BLOQUEADAS = [
    # Conteúdo sexual ou adulto
    "sexy", "sensual", "lingerie", "calcinha", "sutiã", "fio dental", "vibrador",
    "preservativo", "sex shop", "nudez",
    # Armas
    "arma", "airsoft", "paintball", "espingarda", "munição", "taser",
    "spray de pimenta", "estilingue", "soco inglês", "katana", "espada", "facão",
    # Tabaco e drogas
    "cigarro", "vape", "narguilé", "tabaco", "maconha", "cannabis",
    # Itens médicos e suplementos
    "termômetro", "oxímetro", "medidor de pressão", "nebulizador", "remédio",
    "suplemento", "emagrecedor", "lente de contato",
    # Produtos para animais
    "coleira", "ração", "comedouro", "arranhador", "areia sanitária",
    "para cachorro", "para gato", "cachorro", "cachorros", "cães", "gato", "gatos",
    "pet shop", "para pet", "cama pet", "manta pet", "coberta pet", "roupa pet",
    # Inflamáveis
    "álcool em gel", "álcool 70", "álcool 96", "álcool etílico", "álcool líquido",
    "álcool combustível", "gasolina", "fogos de artificio",
    # Festa e enfeites fora do esquema
    "festão", "varal de luz", "cordão de luz", "pisca pisca", "pisca-pisca", "fio de fada",
    "balão", "balões", "bexiga", "fantasia", "decoração de festa", "topo de bolo",
    "lembrancinha",
    # Nicho e personalizados
    "carimbo", "personalizado", "personalizada", "personalizados", "personalizadas",
    "toalha de mesa transparente", "essência", "base amaciante", "base para amaciante",
    # Peças de reposição (ex.: "Borracha Panela Pressão Tramontina")
    "borracha panela", "borracha para panela", "borracha de vedação", "anel de vedação",
    "vedação", "válvula", "reposição", "peça de reposição", "compatível", "compatíveis",
    # Cabos e peças avulsas (controle remoto só original de TV: ver peca_de_outro)
    "controle universal", "similar", "genérico", "paralelo", "tv box", "refil para mop",
    "refil mop", "refil de mop", "refis para mop", "refil avulso", "cabo hdmi", "cabo de força", "cabo de energia",
    "cabo usb", "cabo p2", "extensão elétrica", "fonte de alimentação", "fonte bivolt",
    "carregador", "adaptador", "antena", "conversor digital", "placa eletrônica",
    "placa de controle", "placa de potência", "resistência para", "resistência chuveiro",
    "termostato", "gaxeta", "correia", "dobradiça", "pé de borracha",
    "vela para filtro", "vela filtro", "refil para filtro", "refil filtro", "refil para purificador",
    # Bebê fora do esquema de casa (ex.: "Poltrona de Alimentação Infantil" na busca "poltrona")
    "poltrona de alimentação", "cadeira de alimentação", "cadeira de refeição", "para bebê",
    # Outros
    "réplica",
]
# Bebê e beleza que aparecem em outras buscas do Casa (ex.: "Trocador Anatômico" na busca "cômoda").
# O bot Geral tira esta lista do bloqueio (lá é produto).
BLOQUEADAS_CASA = ["trocador", "fralda", "fraldas", "lenço umedecido", "lenços umedecidos", "chapinha",
                   "prancha alisadora", "prancha de cabelo", "barbeador", "depilador", "secador de cabelo",
                   "escova secadora", "mamadeira", "chupeta", "babá eletrônica"]
BLOQUEADAS = BLOQUEADAS + BLOQUEADAS_CASA
# Peça para outro aparelho: "... para TV", "... para Geladeira". Só passa se o aparelho for
# o que foi buscado (ex.: "Organizador para Geladeira" na busca "organizador de geladeira")
APARELHOS = [
    "tv", "smart tv", "televisão", "geladeira", "refrigerador", "freezer", "fogão", "cooktop",
    "máquina de lavar", "lavadora", "lava louças", "micro-ondas", "microondas", "air fryer",
    "fritadeira", "liquidificador", "batedeira", "cafeteira", "aspirador", "robô aspirador",
    "ventilador", "ar-condicionado", "ar condicionado", "panela de pressão", "chuveiro", "ducha",
    "purificador", "filtro de água", "notebook", "celular", "videogame",
]
INTERVALO_MIN = 6      # minutos entre posts (sorteado entre o mínimo e o máximo)
INTERVALO_MAX = 15
PICO_INICIO = 18       # horário de pico: das 18h...
PICO_FIM = 20          # ...até as 20h posta mais rápido
PICO_MIN = 3           # minutos
PICO_MAX = 6
HORA_INICIO = 8        # posta das 8h...
HORA_FIM = 24          # ...até meia-noite (0 e 24 = o dia todo). Dá uns 105 posts por dia
SILENCIO_INICIO = 0    # das 0h...
SILENCIO_FIM = 8       # ...até as 8h posta sem notificar
# REGRA FINAL (06/11, Gabriel): produto abaixo de R$ 200: qualquer loja, nota 4,5+ e 1000+ vendas.
# De PRECO_REGRA_CARO (R$ 200) para cima, "vasculhada melhor": nota 4,7+, marca conhecida obrigatória e
# 100+ vendas (VENDAS_MINIMAS_CARO; produto caro vende menos). A nota é a média dos COMPRADORES daquele
# anúncio (ratingStar da API), não a nota da loja.
NOTA_MINIMA = 4.5
NOTA_MINIMA_CARO = 4.7
PRECO_REGRA_CARO = 200

def preco_caro(p):
    return float(p.get("price") or 0) >= PRECO_REGRA_CARO

def nota_boa(p):
    return float(p.get("ratingStar") or 0) >= (NOTA_MINIMA_CARO if preco_caro(p) else NOTA_MINIMA)
VENDAS_MINIMAS = 1000       # produtos simples: só os bem vendidos (06/11: era 3000, "dá uma respirada")
VENDAS_MINIMAS_CARO = 100   # produto caro vende menos na Shopee, mas precisa ser de marca
PESO_VENDAS = 0.25     # pesos da pontuação de escolha (somam 1)
PESO_NOTA = 0.15
PESO_COMISSAO = 0.25   # conta o valor em R$ que a gente ganha (preço x %), não só a %
PESO_DESCONTO = 0.15
PESO_PRECO = 0.2       # 06/11, Gabriel: "sempre tenta achar o melhor preço" (o mais barato da busca ganha)
# 09/11: as 5 vendas de 07-08/11 foram TODAS de "COMISSÃO EXTRA" (a loja paga 6% a 16% além dos 3% da Shopee).
# Produto com comissão da loja ganha este bônus na escolha (a comissão maior já conta no PESO_COMISSAO)
BONUS_COMISSAO_EXTRA = 0.15

def comissao_extra(p):
    # % que a LOJA paga a mais (0 se não paga ou se a Shopee não mandou o campo)
    try:
        return float(p.get("sellerCommissionRate") or 0)
    except (TypeError, ValueError):
        return 0.0
# TV boa = preço bom PARA O TAMANHO (Gabriel, 06/11: "Samsung de 60 por 1.200, 1.500; TCL 55 4K por 2.000;
# uma TVzinha de 32 por 1.200 é loucura"). Acima do teto do tamanho, a TV é recusada; entre as que passam,
# vai a mais barata por polegada. Tamanho que não está aqui usa o teto do tamanho menor mais próximo.
TETO_TV = {24: 800, 32: 950, 40: 1400, 43: 1600, 50: 2100, 55: 2400, 58: 2600, 60: 2800, 65: 3400,
           70: 4200, 75: 5000, 85: 8000, 98: 15000}
# Comissão mínima: passa se a % for boa OU se o valor em R$ por venda for bom
# (ex.: jogo de pratos de R$ 34 com 3% = R$ 1,02 não passa; air fryer de R$ 389 com 3% = R$ 11,67 passa)
COMISSAO_MINIMA = 6        # %
VALOR_COMISSAO_MINIMO = 4  # R$ por venda
LOJA_OFICIAL_SEMPRE = True # só posta de Loja Oficial Shopee (seguro pro cliente; False = qualquer loja)
# ...ou de Loja Indicada da Shopee (shopType 2 = Indicada, 4 = Indicada+) se o produto for muito bom.
# Motivo (05/11): o bot recusava achados ótimos (ex.: Espuma Desengordurante nota 4,7, 58% off, 5 mil
# vendas) só por não ser Oficial. A Oficial continua tendo preferência. LOJA_INDICADA = 0 desliga.
# LOJAS (06/11, regra decidida com o Gabriel): QUALQUER loja passa se o produto cumprir a régua de nota e
# vendas (abaixo de R$ 200: 4,5+ e 1000+; de R$ 200 para cima: 4,7+, 100+ e marca). Quando a busca acha
# várias, a preferência é:
#   1º Loja Oficial  2º Loja Indicada pela Shopee  3º loja comum com marca conhecida  4º loja comum sem marca
# Motivo: rodadas de ~2600 produtos com ZERO aprovados (o funil loja + vendas + marca levava 399 bons a 0),
# e os canais que mais engajam postam muito de loja comum. Marca dá preferência,
# mas só é obrigatória em produto caro e em tipo de marca forte (panela = Tramontina, Rochedo...).
LOJA_INDICADA = 1              # 0 = Indicada deixa de ser aceita (/lojaindicada)
LOJA_COMUM_MARCA = 1           # 0 = loja comum deixa de ser aceita (/lojacomum)
DESCONTO_MINIMO = 10   # só posta produto com pelo menos 10% de desconto (grupo de achados)
EXIGIR_MARCA_SEMPRE = True  # modelo ideal: todo post com marca conhecida (False = só nos tipos de marca forte)
DESCONTO_MINIMO_RISCADO = 10   # abaixo de 10% de desconto não mostra o "De R$ ..." riscado
TENTATIVAS_ENVIO = 3   # se o Telegram falhar, tenta de novo antes de desistir do post
RASTREAR_LINKS = True  # etiqueta cada link (canal, tipo, palavra) para o relatório de vendas
PASTA_OBSIDIAN = os.environ.get("BOT_OBSIDIAN",   # no servidor: BOT_OBSIDIAN="" (sem Obsidian lá)
                                "")  # "" desliga
# Mensagem dos grupos: sai sozinha (não no fim do post), com saudação do horário e um link
# por grupo. Lista vazia = mensagem desligada. Ex.: ("🏠 Casa (WhatsApp)", "https://...")
GRUPOS_MIN = 15       # a mensagem dos grupos sai a cada 15 posts (90 por dia = 6 vezes)...
GRUPOS_MAX = 15        # ...(MIN = MAX: sempre 15; para sortear, ex.: 15 e 22)
SAUDACOES = [(0, 12, "☀️ BOM DIAAA!!"), (12, 18, "🌤️ BOA TARDEEE!!"), (18, 24, "🌙 BOA NOITEEE!!")]
# (09/11) Frase do grupo depois da saudação, no contexto de cada grupo (o nicho.py de cada bot troca).
# Uma é sorteada por vez: {"dia": [...], "tarde": [...], "noite": [...]}
FRASES_GRUPO = {
    "dia": ["☕ Café passado e casa arrumada: hoje tem achadinho pra deixar o seu cantinho mais lindo gastando pouco.",
            "🏠 Começando o dia com os achadinhos de casa que mais valem a pena: cozinha, banheiro, quarto e sala."],
    "tarde": ["🛋️ Pausa pro café? Aproveita e dá uma olhada nos achadinhos de casa de hoje, tem coisa boa demais.",
              "🧺 Organizar a casa fica mais fácil (e mais barato) com os achadinhos que separamos pra você."],
    "noite": ["🌙 Casa em silêncio, hora de garimpar: os melhores achadinhos de casa do dia estão aqui no grupo.",
              "🛏️ Antes de dormir, confere os achadinhos de casa de hoje. Amanhã pode não ter mais nesse preço!"],
}
# Os grupos (nome, link). Cada bot põe o dele primeiro. Link vazio = ainda não tem: fica de fora da mensagem
NOME_GRUPO_CASA, LINK_GRUPO_CASA = "🏠 Achadinhos de Casa", "https://chat.whatsapp.com/CONVITE_DO_GRUPO_CASA"
NOME_GRUPO_GERAL, LINK_GRUPO_GERAL = "🔗 Achadinhos & Promoções", "https://chat.whatsapp.com/CONVITE_DO_GRUPO_GERAL"
NOME_GRUPO_PERFUME, LINK_GRUPO_PERFUME = "✈️ Duty Free Perfumes","https://chat.whatsapp.com/CONVITE_DO_GRUPO_PERFUME"
GRUPOS = [(NOME_GRUPO_CASA, LINK_GRUPO_CASA), (NOME_GRUPO_GERAL, LINK_GRUPO_GERAL),
          (NOME_GRUPO_PERFUME, LINK_GRUPO_PERFUME)]
ARQUIVO_GRUPOS = "mensagem_grupos.txt"
ARQUIVO_POSTADOS = "postados.txt"
SEM_REPETIR = 15       # palavra e tipo de produto não se repetem nos últimos 15 posts
CATEGORIA_SEM_REPETIR = 40   # 06/11: a categoria (mesa de jantar, TV...) evita os últimos 40 posts, somando simples e
                             # caros (Gabriel viu 3 mesas de jantar em 40 posts: uma vinha dos caros, outra dos simples)
ARQUIVO_HISTORICO = "historico.txt"
ARQUIVO_CICLO = "ciclo.txt"   # rodízio: palavras que já tiveram a vez nesta volta da lista
# Rodízio por TIPO de produto: palavras do mesmo tipo ("smart tv 32", "smart tv 55"...) dividem
# uma vez só por volta. O tipo é a 1ª palavra que importa ("jogo de panelas" -> panela)...
TIPOS_GENERICOS = {"porta", "organizador", "tapete", "mesa", "toalha", "cadeira", "caixa", "cesto",
                   "suporte", "papel", "escova", "maquina", "agua", "tira", "saco", "capa", "carrinho",
                   "balanca", "filtro", "dispenser", "luva", "tesoura", "moedor", "protetor", "lampada",
                   "pano", "tabua", "lava", "ducha", "mini"}   # ...menos nestas, que usam as 2 primeiras
                                                   # ("porta tempero" e "porta shampoo" são tipos diferentes)
TIPOS_PROPRIOS = ["panela de pressão", "panela elétrica", "freezer horizontal", "geladeira expositora",
                  "churrasqueira elétrica", "churrasqueira a gás", "secador de cabelo",
                  "caneca mixer", "caneca magnética", "caneca autoagitadora",
                  "prateleira giratória", "barra magnética", "kit potes para lavanderia", "pote para sabão",
                  "aparador de barba", "aparador de pelos", "aparador de grama"]   # não é o aparador (móvel)   # tipo separado mesmo começando igual
SINONIMOS_TIPO = {"ducha": "chuveiro"}                       # "ducha" sozinha conta como chuveiro
MAX_PALAVRAS_RODADA = 40   # palavras buscadas por rodada no máximo (~120 buscas; a lista toda de uma vez estoura o limite da Shopee)
ALERTA_SEM_POST_MIN = 45   # minutos sem postar (dentro do horário) até o painel avisar
ESPERA_SEM_POST = 120      # segundos até tentar de novo quando a rodada não achou nada
ESPERA_APOS_LIMITE = 600   # idem quando a Shopee barrou por excesso de buscas
# Aparelhos de tomada: o título diz a voltagem e a ordem é bivolt > 220V > 110V (110V só em último caso)
ELETRICOS = [
    "geladeira", "freezer", "frigobar", "cervejeira", "adega", "fogão", "cooktop", "forno", "micro-ondas",
    "máquina de lavar", "lava e seca", "lava louças", "tanquinho", "secadora", "air fryer", "fritadeira",
    "liquidificador", "batedeira", "cafeteira", "sanduicheira", "grill", "torradeira", "pipoqueira",
    "mixer", "processador", "espremedor", "panela elétrica", "panela de pressão elétrica", "chaleira elétrica",
    "aspirador", "mop a vapor", "ventilador", "circulador", "climatizador", "aquecedor", "umidificador",
    "desumidificador", "purificador", "ar-condicionado", "ar condicionado", "ferro de passar", "ferro a vapor", "vaporizador",
    "passadeira", "secador", "escova secadora", "prancha", "modelador", "massageador",
    "cadeira de massagem", "poltrona massageadora", "soprador", "churrasqueira elétrica", "bebedouro",
    "lavadora", "chuveiro", "ducha", "máquina de costura", "parafusadeira", "furadeira", "sorveteira",
    "iogurteira", "fogareiro elétrico", "lâmpada", "luminária", "geladeira expositora",
    "impressora", "estabilizador", "removedor de pelos", "aparador de pelos", "tira pelos elétrico",
    # 06/11: qualquer busca com "elétrico/elétrica" e os aparelhos da expansão
    "elétrico", "elétrica", "máquina de cortar", "aparador de barba", "aparador de grama", "barbeador",
    "depilador", "irrigador", "extratora", "enceradeira", "lixadeira", "esmerilhadeira", "serra",
    "máquina de pão", "máquina de crepe", "panquequeira", "centrífuga", "mini lavadora",
]
# Medida no título: litros/kg/garrafas (capacidade) e tamanho (móvel, cama, colchão, escada...)
COM_CAPACIDADE = ["geladeira", "freezer", "frigobar", "cervejeira", "adega", "máquina de lavar", "forno",
                  "lava e seca", "tanquinho", "secadora", "air fryer", "fritadeira", "panela elétrica",
                  "panela de pressão elétrica", "forno elétrico", "micro-ondas", "bebedouro", "caixa térmica",
                  "cooler"]
COM_MEDIDAS = ["guarda-roupa", "cama", "colchão", "escada", "estante", "mesa", "sala de jantar", "rack", "painel",
               "sofá", "armário", "sapateira", "cozinha", "tapete", "cortina", "escrivaninha", "cômoda",
               "penteadeira", "cabeceira", "prateleira", "balcão", "gaveteiro", "nicho", "espelho",
               "persiana", "janela", "box", "toldo", "lona", "piscina",
               "biombo", "beliche", "bicama", "buffet", "cristaleira", "gazebo", "tenda", "bancada", "recamier",
               # aparelho grande: o tamanho importa (cabe no apartamento?)
               "geladeira", "freezer", "frigobar", "cervejeira", "adega", "forno", "churrasqueira",
               "fogão", "cooktop", "lava louças", "máquina de lavar", "ar condicionado", "climatizador"]
FOTOS_AVALIADAS = 5    # entre os 5 melhores, prefere foto que não seja só fundo branco
LIMITE_FUNDO_BRANCO = 0.8
COR_FUNDO = (226, 232, 240)   # foto de fundo branco: o fundo vira esse cinza-azulado clarinho
TOLERANCIA_FUNDO = 10         # quanto o branco do fundo pode variar (acima de ~15 começa a
                              # pintar partes brancas do produto)
                              # COR_FUNDO = None desliga
MAX_PALAVRAS_NOME = 5  # tamanho do nome limpo no post
# Chamadas (primeira linha do post). As gerais servem para qualquer produto.
CHAMADAS_GERAIS = ["🔥 ACHADO DO DIA", "👀 OLHA ESSE PREÇO", "😍 TODO MUNDO TÁ LEVANDO",
                   "😱 VALE MUITO A PENA", "🛒 QUEM VIU, LEVOU",
                   "✨ SUA CASA MERECE"]
CHAMADAS_CARO = ["💎 PRODUTO TOP COM PREÇO DE OPORTUNIDADE", "🏆 UPGRADE NA CASA",
                 "😮 ESSE PREÇO NÃO É TODO DIA"]
CHAMADAS_ATE_100 = ["🏠 CASA BONITA GASTANDO POUCO"]   # entra nos produtos de até R$ 100
NICHO_IA = "achadinhos de casa"   # como a IA chama o canal na revisão ("canal de achadinhos de casa")
# O que a IA recusa na revisão (o bot Geral troca: lá carregador e cabo são produto, não peça)
TEXTO_MODELO_IA = (
    "Modelo ideal: produto de marca conhecida, com desconto de verdade, útil para o público do canal, "
    "e foto REAL do produto (foto de produto de verdade ou de um ambiente real). "
    "Recuse foto gerada por inteligência artificial ou render artificial, e recuse produto "
    "estranho, acessório ou que não seja do tipo buscado. Recuse também produto de nicho: "
    "peça de reposição (borracha, válvula, resistência, placa), cabo, carregador, refil "
    "vendido sozinho, controle remoto que não seja o original da marca da TV (pirata, "
    "compatível ou universal), TV box, ou qualquer coisa que só serve para consertar ou completar outro "
    "aparelho. O canal posta o produto principal (a TV, não o controle da TV).\n"
    "Se o título disser 100% algodão (cueca, calcinha, camiseta, toalha, jogo de cama, fronha, travesseiro), "
    "ponha '100% Algodão' no nome. Não cite outro tecido (poliamida, poliéster, elastano).\n")
CATEGORIAS_EXTRA = []   # categorias do rodízio só do bot (nicho.py); entram antes das do Casa (ver CATEGORIAS)
PESO_CATEGORIA = {}     # (07/11) {"capa de sofá": 3}: a categoria tem a vez 3 vezes em cada volta do rodízio
                        # (sem peso = 1). Continua sem repetir nos últimos 40 posts (CATEGORIA_SEM_REPETIR)
ALTERNAR_FEMININO = False   # (07/11, geral) True: um post de categoria "♀", o próximo de uma sem "♀" (masculino,
                            # tecnologia, carro...), e assim vai. Só quebra se o lado da vez não tiver o que buscar.
# Chamadas por tipo: só entram quando a palavra buscada é desse tipo (vale o trecho mais longo
# que combinar, assim "cortina de box" é banheiro e não sala)
CHAMADAS_POR_TIPO = [
    (["panela", "panelas", "frigideira", "air fryer", "forno", "micro-ondas", "assadeira",
      "forma de bolo", "liquidificador", "batedeira", "mixer", "processador", "sanduicheira",
      "cafeteira", "chaleira", "utensílios", "faca de cozinha", "tábua de corte", "fogão", "lava louças",
      "garrafa", "garrafa térmica", "garrafa de café", "balança de cozinha"],
     ["🍳 O QUERIDINHO DAS COZINHAS", "👩‍🍳 PRA QUEM AMA COZINHAR"]),
    (["prato", "pratos", "copo", "copos", "taça", "xícara", "caneca", "talheres", "faqueiro", "jarra", "jogo americano",
      "toalha de mesa", "mesa de jantar"],
     ["🍽️ MESA POSTA DE RESPEITO", "✨ PRA RECEBER BEM AS VISITAS"]),
    (["pote", "porta tempero", "porta ovos", "organizador", "escorredor", "suporte para panelas",
      "caixa organizadora", "cesto organizador", "gaveteiro", "prateleira", "sapateira", "cabide",
      "lixeira", "marmita", "lancheira", "guarda-roupa", "armário"],
     ["📦 TUDO NO SEU LUGAR", "🧺 ORGANIZAÇÃO QUE DÁ GOSTO"]),
    (["travesseiro", "lençol", "fronha", "edredom", "cobertor", "colcha", "protetor de colchão",
      "colchão", "cama box", "cabeceira", "criado-mudo"],
     ["😴 NOITE DE SONO DE HOTEL", "🛏️ QUARTO DOS SONHOS"]),
    (["toalha de banho", "toalha de rosto", "jogo de toalhas", "toalha buddemeyer", "roupão",
      "tapete banheiro", "tapete de pedra", "saboneteira", "sabonete", "dispenser sabonete",
      "porta escova", "porta cotonete",
      "porta algodão", "chuveiro", "ducha", "cortina de box"],
     ["🛁 BANHEIRO DE REVISTA", "🧴 BANHO COM CARA DE SPA"]),
    (["mop", "vassoura", "rodo", "balde", "kit limpeza", "panos de microfibra", "bucha", "esponja",
      "detergente", "sabão", "amaciante", "desinfetante", "escova de limpeza", "aspirador",
      "robô aspirador", "máquina de lavar", "secadora", "varal", "prendedor", "tábua de passar",
      "ferro de passar", "vaporizador", "cesto de roupa"],
     ["🧽 FAXINA EM METADE DO TEMPO", "✨ CASA LIMPA SEM ESFORÇO"]),
    (["sofá", "capa de sofá", "almofada", "manta para sofá", "rack", "painel tv", "mesa de centro",
      "mesa de sala", "tapete de sala", "quadro", "vaso decorativo", "planta artificial",
      "relógio de parede", "luminária", "lustre", "abajur", "cortina", "blackout", "puff", "poltrona",
      "espelho",
      "estante"],
     ["🛋️ SALA AINDA MAIS ACONCHEGANTE", "🖼️ DECORAÇÃO QUE MUDA O AMBIENTE"]),
    (["smart tv", "caixa de som", "soundbar"], ["🍿 CINEMA EM CASA"]),
    (["babá eletrônica"], ["👶 SOSSEGO PRA QUEM TEM BEBÊ"]),
    (["fechadura digital"], ["🔐 SEGURANÇA SEM CHAVE"]),
    (["ventilador", "climatizador", "ar-condicionado"], ["🥵 ADEUS, CALORÃO"]),
    (["aquecedor"], ["🥶 ADEUS, FRIO"]),
    (["escrivaninha", "cadeira de escritório", "mesa de escritório", "organizador de cabos"],
     ["💻 HOME OFFICE NOTA 10"]),
    (["lâmpada inteligente", "tomada inteligente"], ["💡 CASA INTELIGENTE GASTANDO POUCO"]),
    (["churrasqueira", "kit churrasco"], ["🍖 BORA FAZER UM CHURRASCO"]),
    (["rede de descanso", "cadeira de jardim", "vaso de planta", "mangueira", "luminária solar"],
     ["🌿 ÁREA EXTERNA DOS SONHOS"]),
]
# Cupons (cupons.txt na pasta principal, vale para todos os bots da Shopee; o painel do Telegram
# preenche quando você cola o cupom lá)
CUPOM_DESCONTO_MINIMO = 5   # R$: cupom que economiza menos que isso não aparece no post
CUPONS_MIN = 25             # alerta de cupom sai depois de um número sorteado de posts entre 25...
CUPONS_MAX = 35             # ...e 35 (só se tiver cupom valendo)
LINK_CUPONS = ""            # link de afiliado da página de cupons da Shopee (vai no alerta). "" = sem link
CHAVE_CANAL = "CANAL"       # linha do config.txt com o canal deste bot (ex.: CANAL_GERAL no bot geral)
# Ofertas copiadas dos concorrentes (06/11, Gabriel: "copie as ofertas dos canais que estamos observando, os preços
# deles são bons"): o produto que os canais/grupos observados postam entra aqui com o NOSSO link (ver postar_copiado)
COPIAR_OFERTAS = 1          # 0 = desliga (/copiar casa 0)
COPIADOS_A_CADA = 2         # no máximo 1 oferta copiada a cada 2 posts (o resto é a busca normal, para variar)
COPIADOS_HORAS = 6          # só ofertas postadas por eles nas últimas 6 h (preço de agora)
COPIADOS_VENDAS_MINIMAS = 50
COPIADOS_POR_RODADA = 12    # links novos abertos por rodada, no máximo (cada um é 1 consulta na Shopee)
# WhatsApp (programa whatsapp/servidor.js no mesmo servidor). Os grupos/canais de cada bot ficam em
# whatsapp_destinos.txt na pasta do bot (o painel preenche com /zapdestino)
WHATSAPP_URL = "http://127.0.0.1:3010"
WHATSAPP_MAX_DIA = 90       # lançamento (06/11): 90 por dia, das 8h à meia-noite, o pico (18h-20h) com o dobro
TELEGRAM_POSTAR = 0         # 0 = só o WhatsApp recebe (o ritmo é o dele); 1 = o Telegram recebe junto (/telegramligar)
WHATSAPP_INTERVALO = 5     # minutos no mínimo entre posts no WhatsApp (os do dia se espalham até HORA_FIM)
WHATSAPP_INTERVALO_MAX = 0 # (07/11) >0 = cada post sai entre WHATSAPP_INTERVALO e este máximo (sorteado), sem espalhar
                           # pelo dia; ex.: /zapintervalo casa 8 20. 0 = desligado (espalha os do dia, como antes)
# Com 90: ~11-12 min entre posts no horário normal e ~6 min no pico (cada minuto do pico vale 2 na conta)
CONFIG_PATH = os.environ.get("BOT_CONFIG", r"C:\bot-config\config.txt")   # senhas fora da pasta do bot
# (09/11) De qual loja vêm os produtos: "shopee" (Casa e Geral) ou "mercadolivre" (bot de perfume: a vitrine da
# Central de Afiliados com a sessão do Gabriel, ver mercadolivre.py). O nicho.py troca.
LOJA = "shopee"
COMBINA_EM_QUALQUER_LUGAR = False   # True: a busca combina se os termos aparecem em qualquer parte do nome
SINONIMOS_BUSCA = {}                # {"perfume": ["parfum", "colonia"...]}: termo da busca que vale por outro no nome
BUSCAS_ML = []                      # (Geral) buscas que vão no Mercado Livre em vez da Shopee (achados fortes)
# ===========================================================

# ================= QUAL BOT =================
# "python postar_shopee.py casa" usa a pasta bots/casa. O nicho.py de lá troca o que for diferente
# neste bot (lista de produtos, marcas, canal...); o que ele não trocar fica como está acima (o Casa).
# Os arquivos de controle (postados, histórico, rodízio...) ficam na pasta de cada bot.
PASTA_PRINCIPAL = os.path.dirname(os.path.abspath(__file__))
BOT = sys.argv[1] if len(sys.argv) > 1 else "casa"
PASTA_BOT = os.path.join(PASTA_PRINCIPAL, "bots", BOT)
PALAVRAS_DO_CASA = [p for _l in PALAVRAS.values() for p in _l] + list(CAROS)   # antes do nicho trocar (copiados)
COR_SOBRIA_EXTRA = []   # o nicho põe tipos que pedem cor sóbria (somam no COR_SOBRIA_TIPOS, definido mais abaixo)
if os.path.exists(os.path.join(PASTA_BOT, "nicho.py")):
    with open(os.path.join(PASTA_BOT, "nicho.py"), encoding="utf-8") as _f:
        exec(_f.read())
# Números que o painel do Telegram pode mudar sem reiniciar (ficam no ajustes.txt do bot)
AJUSTAVEIS = ["INTERVALO_MIN", "INTERVALO_MAX", "PICO_INICIO", "PICO_FIM", "PICO_MIN", "PICO_MAX",
              "HORA_INICIO", "HORA_FIM", "COMISSAO_MINIMA", "VALOR_COMISSAO_MINIMO", "DESCONTO_MINIMO",
              "NOTA_MINIMA", "GRUPOS_MIN", "GRUPOS_MAX", "CUPONS_MIN", "CUPONS_MAX",
              "CARO_A_CADA_MIN", "CARO_A_CADA_MAX", "CARO_PICO_MIN", "CARO_PICO_MAX",
              "WHATSAPP_MAX_DIA", "WHATSAPP_INTERVALO", "WHATSAPP_INTERVALO_MAX", "TELEGRAM_POSTAR", "LOJA_INDICADA", "LOJA_COMUM_MARCA",
              "COPIAR_OFERTAS", "COPIADOS_A_CADA"]
PADROES = {k: globals()[k] for k in AJUSTAVEIS}
ARQUIVO_AJUSTES = "ajustes.txt"
ARQUIVO_STATUS = "status.json"            # o painel lê: posts de hoje, último post, ajustes em uso
ARQUIVO_POSTAR_AGORA = "postar_agora"     # o painel cria: o bot posta já, sem esperar o intervalo
ARQUIVO_MANDAR_CUPONS = "mandar_cupons"   # o painel cria: o bot manda o alerta de cupom já
ARQUIVO_MANDAR_GRUPOS = "mandar_grupos"   # o painel cria (/zapconvite): o bot manda a mensagem dos grupos já
ARQUIVO_CONTAGEM_CUPONS = "mensagem_cupons.txt"
ARQUIVO_ZAP_DESTINOS = "whatsapp_destinos.txt"   # ids dos grupos/canais (um por linha; # = comentário)
ARQUIVO_ZAP_PAUSA = "whatsapp_pausado"            # existe = WhatsApp pausado (o bot cria se der erro)
ARQUIVO_ZAP_CONTAGEM = "whatsapp_contagem.json"

def ler_config(caminho=CONFIG_PATH):
    config = {}
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            if "=" in linha:
                chave, valor = linha.strip().split("=", 1)
                config[chave.strip()] = valor.strip()
    return config

cfg = ler_config()

CATEGORIA = {palavra: cat for cat, lista in PALAVRAS.items() for palavra in lista}
SIMPLES = list(CATEGORIA)

class ErroShopee(Exception):
    pass

class ErroLimite(ErroShopee):
    # "Rate limit exceeded" (10030): buscou demais, não é a busca que está errada
    pass

class ErroTemporario(ErroShopee):
    # "System Error" (10000): falha do lado da Shopee, passa sozinha. Não pode descer para a busca simples
    pass

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
        if any("10030" in str(e) or "rate limit" in str(e).lower() for e in dados["errors"]):
            raise ErroLimite(dados["errors"])
        if any("10000" in str(e) or "system error" in str(e).lower() for e in dados["errors"]):
            raise ErroTemporario(dados["errors"])
        raise ErroShopee(dados["errors"])
    return dados["data"]

# Da busca mais completa para a mais simples: se a Shopee recusar um nível, desce para o próximo
NIVEIS_BUSCA = [
    # 09/11: + comissão da LOJA (a "COMISSÃO EXTRA" do painel de afiliado). Se a Shopee recusar, desce para o de baixo
    (", sortType: 2", " shopType productLink shopName priceMin priceMax sellerCommissionRate shopeeCommissionRate"),
    (", sortType: 2", " shopType productLink shopName priceMin priceMax"),   # + faixa de preço das versões (06/11)
    (", sortType: 2", " shopType productLink shopName"),   # + nome da loja (marca de quem vende)
    (", sortType: 2", " shopType productLink"),   # mais vendidos + loja oficial + link para etiquetar
    (", sortType: 2", " shopType"),               # mais vendidos + loja oficial
    ("", ""),                                     # busca simples
]
nivel_busca = 0
busca_por_comissao = True   # vira False se a Shopee não aceitar a ordem por comissão

def montar_consulta(palavra, limite, extras_args, extras_campos):
    return ('{ productOfferV2(keyword: "%s", limit: %d%s) { nodes { '
            'itemId productName price imageUrl offerLink sales '
            'ratingStar commissionRate priceDiscountRate%s } } }') % (palavra, limite, extras_args, extras_campos)

def buscar_shopee(palavra, limite=30):
    global nivel_busca
    while True:
        extras_args, extras_campos = NIVEIS_BUSCA[nivel_busca]
        try:
            return chamar_shopee(montar_consulta(palavra, limite, extras_args, extras_campos))["productOfferV2"]["nodes"]
        except (ErroLimite, ErroTemporario):
            raise                              # limite/falha passageira não é recusa: não desce para a busca simples
        except ErroShopee as e:
            if nivel_busca == len(NIVEIS_BUSCA) - 1:
                raise
            nivel_busca += 1
            print(f"  Aviso: a Shopee recusou parte da busca ({e}). Usando uma busca mais simples.")

def buscar_por_comissao(palavra, limite=30):
    # Mesma busca, mas com os de maior comissão primeiro (sortType 5): acha a mesma marca
    # pagando mais (ex.: Dove a 8% em vez de 3%). Se a Shopee recusar, para de tentar.
    global busca_por_comissao
    if not busca_por_comissao or "sortType: 2" not in NIVEIS_BUSCA[nivel_busca][0]:
        return []
    extras_args, extras_campos = NIVEIS_BUSCA[nivel_busca]
    try:
        consulta = montar_consulta(palavra, limite, extras_args.replace("sortType: 2", "sortType: 5"),
                                   extras_campos)
        return chamar_shopee(consulta)["productOfferV2"]["nodes"]
    except (ErroLimite, ErroTemporario):
        raise
    except ErroShopee as e:
        busca_por_comissao = False
        print(f"  Aviso: a Shopee não aceitou a busca por comissão ({e}). Seguindo só com a normal.")
        return []

PAUSA_ENTRE_BUSCAS = PAUSA_ENTRE_BUSCAS if "PAUSA_ENTRE_BUSCAS" in globals() else 0.7   # segundos entre buscas:
# rápido demais gera "System Error" na Shopee (o nicho do Mercado Livre põe mais)

_sessao_ml = {"s": None, "avisado": False}

def sessao_ml():
    # A sessão do Mercado Livre (abre 1 vez e reaproveita). Se o Mercado Livre pedir login, avisa o painel
    # 1 vez e para de buscar até os cookies serem exportados de novo
    import mercadolivre
    if _sessao_ml["s"] is None:
        try:
            _sessao_ml["s"] = mercadolivre.SessaoML()
            _sessao_ml["avisado"] = False
        except mercadolivre.SessaoCaiu as e:
            if not _sessao_ml["avisado"]:
                _sessao_ml["avisado"] = True
                avisar_painel(f"🔑 <b>{html.escape(BOT)}</b>: a sessão do Mercado Livre caiu ({html.escape(str(e))}). "
                              "No Firefox, logado no Mercado Livre: extensão Get cookies.txt LOCALLY > Export, e "
                              "mande o arquivo para o bot-config do servidor como ml_cookies.txt.")
            raise ErroShopee(f"sessão do Mercado Livre: {e}")
    return _sessao_ml["s"]

def eh_busca_ml(termo):
    # (09/11) Bot da Shopee com algumas buscas no Mercado Livre (BUSCAS_ML do nicho; vale também "busca + marca")
    t = normalizar(termo)
    return any(t == normalizar(b) or t.startswith(normalizar(b) + " ") for b in BUSCAS_ML)

def buscar_mercadolivre(termo):
    import mercadolivre
    time.sleep(max(PAUSA_ENTRE_BUSCAS, 1.5))
    try:
        achados = sessao_ml().buscar(termo)
        if LOJA != "mercadolivre":             # no Geral: + os MAIS VENDIDOS dessa busca (o popular de verdade)
            time.sleep(1.5)
            vistos = {c["id"] for c in achados}
            achados += [c for c in sessao_ml().buscar(termo, filtros=["best_seller"]) if c["id"] not in vistos]
        return [mercadolivre.para_oferta(c) for c in achados]
    except mercadolivre.SessaoCaiu as e:
        _sessao_ml["s"] = None                 # na próxima busca tenta abrir de novo (e avisa se não der)
        raise ErroShopee(f"sessão do Mercado Livre: {e}")

def buscar_com_repeticao(termo):
    # Busca normal + por comissão. Se a Shopee responder "System Error" (falha passageira),
    # espera um pouco e tenta de novo (até 2 vezes) antes de desistir daquela palavra.
    if LOJA == "mercadolivre" or eh_busca_ml(termo):
        return buscar_mercadolivre(termo)
    for tentativa in range(3):
        try:
            time.sleep(PAUSA_ENTRE_BUSCAS)
            achados = buscar_shopee(termo)
            time.sleep(PAUSA_ENTRE_BUSCAS)
            return achados + buscar_por_comissao(termo)
        except ErroTemporario:
            if tentativa == 2:
                raise
            time.sleep(3 * (tentativa + 1))

def link_rastreado(p, palavra, caro, canal):
    # Link curto com etiquetas (canal, tipo, palavra) que aparecem no relatório de vendas da Shopee
    if p.get("loja") == "mercadolivre":
        # meli.la da conta de afiliado (o mesmo link no WhatsApp e no Telegram). Sem link, não posta
        if not p.get("offerLink"):
            p["offerLink"] = sessao_ml().gerar_link(p["_ml"]) or ""
        if not p["offerLink"]:
            raise ErroShopee("o Mercado Livre não gerou o link de afiliado")
        return p["offerLink"]
    if not RASTREAR_LINKS or not p.get("productLink"):
        return p["offerLink"]
    etiquetas = [canal, "caro" if caro else "simples", re.sub(r"[^a-z0-9]", "", normalizar(palavra))[:30],
                 re.sub(r"[^a-z0-9]", "", normalizar(BOT))[:30]]
    consulta = 'mutation { generateShortLink(input: {originUrl: %s, subIds: %s}) { shortLink } }' % (
        json.dumps(p["productLink"]), json.dumps(etiquetas))
    try:
        return chamar_shopee(consulta)["generateShortLink"]["shortLink"]
    except Exception as e:
        print(f"  Aviso: não consegui gerar o link etiquetado ({e}). Usando o link normal.")
        return p["offerLink"]

def carregar_postados():
    try:
        with open(ARQUIVO_POSTADOS, encoding="utf-8") as f:
            return set(l.strip() for l in f if l.strip())
    except FileNotFoundError:
        return set()

def salvar_postado(item_id):
    with open(ARQUIVO_POSTADOS, "a", encoding="utf-8") as f:
        f.write(str(item_id) + "\n")

def preco_br(valor):
    return f"{float(valor):,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")

def normalizar(texto):
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return " ".join(sem_acento.lower().split())

def sem_assistente(nome):
    # "Tomada Inteligente compatível com Alexa": o "compatível" aí não é peça pirata,
    # e Alexa/Google aí não são a marca do produto
    # (e "Branco Neve" é cor, não a marca Neve)
    nome = re.sub(r"(compativel|compativeis|funciona) com (a |o )?(alexa|google)( (assistente|home))?"
                  r"( e (a |o )?(alexa|google)( (assistente|home))?)?", " ", normalizar(nome))
    return re.sub(r"branc[oa] neve", " ", nome)

# Natal e Ano Novo (08/11, Gabriel: "pode liberar"): em novembro e dezembro pisca-pisca e luzinhas passam;
# balão só se o título for de Natal/Ano Novo (balão de aniversário continua fora)
LIBERADOS_FIM_DE_ANO = ["pisca pisca", "pisca-pisca", "varal de luz", "cordão de luz", "fio de fada",
                        "balão", "balões"]
SO_COM_TEMA = ["balão", "balões"]

def bloqueado(nome, hoje=None):
    nome = sem_assistente(nome)
    liberados = set()
    if (hoje or datetime.now().date()).month in (11, 12):
        tema = re.search(r"natal|natalin|ano novo|reveillon", nome)
        liberados = {normalizar(t) for t in LIBERADOS_FIM_DE_ANO if tema or t not in SO_COM_TEMA}
    # (09/11) BLOQUEIO_EXCETO (nicho.py): {"brinquedo": ["cachorro", "gato"]} = bloqueia "brinquedo", menos o de pet
    exceto = {normalizar(k): [normalizar(x) for x in v] for k, v in globals().get("BLOQUEIO_EXCETO", {}).items()}
    def salvo(t):
        return any(re.search(r"\b" + re.escape(x), nome) for x in exceto.get(t, []))
    return any(normalizar(t) not in liberados and re.search(r"\b" + re.escape(normalizar(t)) + r"\b", nome)
               and not salvo(normalizar(t)) for t in BLOQUEADAS)

def peca_de_outro(nome, palavra):
    # "Capa para Smart TV" na busca "capa de sofá": é coisa de outro aparelho, não posta
    nome, busca = normalizar(nome), normalizar(palavra)
    if "controle" in nome.split()[:2]:
        # Controle remoto: só na busca de controle e só original (nada de compatível/pirata)
        return not ("controle" in busca and re.search(r"(?<!\w)original(?!\w)", nome))
    for a in map(normalizar, APARELHOS):
        if (re.search(r"(?<!\w)(para|pra|p/) (o |a )?" + re.escape(a) + r"(?!\w)", nome)
                and not re.search(r"(?<!\w)" + re.escape(a) + r"(?!\w)", busca)):
            return True
    return False

def marca_no_nome(nome):
    # Devolve a marca conhecida que aparece no nome (escrita do jeito da lista), ou None
    nome = sem_assistente(nome)
    for m in MARCAS:
        if re.search(r"(?<!\w)" + re.escape(normalizar(m)) + r"(?!\w)", nome):
            return m
    return None

def tem_marca(nome):
    return marca_no_nome(nome) is not None

def marca_do_produto(p):
    # Marca pelo título; se o título não tiver, pelo nome da loja (ex.: "Mondial Loja Oficial")
    return marca_no_nome(p["productName"]) or marca_no_nome(p.get("shopName") or "")

def marcas_do_tipo(palavra):
    busca = normalizar(palavra)
    melhor, marcas = 0, []
    for trechos, lista in MARCAS_POR_TIPO:
        for t in trechos:
            t = normalizar(t)
            if len(t) > melhor and re.search(r"(?<!\w)" + re.escape(t) + r"(?!\w)", busca):
                melhor, marcas = len(t), lista
    return marcas

PALAVRAS_VAZIAS = {"de", "da", "do", "das", "dos", "para", "com", "sem", "em", "kit", "jogo",
                   "conjunto", "novo", "nova", "un", "unidades", "peca", "pecas"}

def termos(texto):
    # Palavras que importam no nome, sem acento, sem número e sem o "s" do plural
    palavras = re.findall(r"[a-z]+", normalizar(texto))
    return [p[:-1] if len(p) > 3 and p.endswith("s") else p
            for p in palavras if len(p) > 1 and p not in PALAVRAS_VAZIAS]

ACESSORIOS = {"saco", "capa", "suporte", "refil", "arraste", "engrenagem", "reposicao", "fita",
              "organizador", "tampa", "protetor", "filtro", "lampada", "adesivo", "pelicula", "cesto",
              "borracha", "anel", "valvula", "pino", "cabo", "alca", "puxador", "peca",
              "controle", "carregador", "fonte", "adaptador", "antena", "resistencia", "gaxeta",
              "correia", "vela"}

def combina(nome, palavra):
    # O termo principal da busca aparece logo no começo do nome (evita "Carimbo ... + Almofada"
    # em "almofada") e os outros ficam perto dele, antes ou depois, a até 3 palavras
    # (evita "Mesa de Cabeceira ... Quarto Sala" em "mesa de sala"; aceita "Karsten Cobertor")
    busca, produto = termos(palavra), termos(nome)
    if COMBINA_EM_QUALQUER_LUGAR:
        # (09/11, perfume) "Natura Una Artisan Feminino Eau de Parfum" combina com "perfume feminino":
        # cada termo da busca (ou um sinônimo dele) aparece em qualquer parte do nome
        sin = {termos(k)[0]: {s for v in vs for s in termos(v)} for k, vs in SINONIMOS_BUSCA.items() if termos(k)}
        return bool(busca) and all(t in produto or sin.get(t, set()) & set(produto) for t in busca)
    for inicio in [i for i, t in enumerate(produto[:4]) if t == busca[0]]:
        # "Saco Organizador Cobertor", "Arraste Copo": acessório antes do produto buscado
        if any(t in ACESSORIOS and t not in busca for t in produto[:inicio]):
            continue
        perto = produto[max(0, inicio - 3):inicio + 4]
        if all(termo in perto for termo in busca[1:]):
            return True
    return False

def parecido(nome, outro):
    # Mesmo tipo de produto: começa igual ou divide boa parte dos termos (fora os de enfeite)
    a, b = termos(nome), termos(outro)
    # (09/11, perfume) "Perfume ... Eau de Parfum": palavras que todo produto do nicho tem não contam
    genericos = {t for g in globals().get("PARECIDO_IGNORAR", []) for t in termos(g)}
    a, b = [t for t in a if t not in genericos], [t for t in b if t not in genericos]
    if not a or not b:
        return False
    comuns = (set(a) & set(b)) - ENFEITES
    return a[0] == b[0] or len(comuns) >= max(3, min(len(set(a)), len(set(b))) // 2)

ENFEITES = {"moderno", "moderna", "modernos", "modernas", "minimalista", "luxo", "luxuoso",
            "luxuosa", "premium", "original", "promocao", "oferta", "lancamento", "top",
            "envio", "imediato", "pronta", "entrega", "qualidade", "alta", "resistente",
            "pratico", "pratica", "bonito", "bonita", "lindo", "linda", "elegante",
            "sofisticado", "sofisticada", "novidade", "super", "mega", "incrivel",
            "perfeito", "perfeita", "barato", "barata", "promo"}
PEQUENAS = {"de", "da", "do", "das", "dos", "para", "com", "em", "e", "sem", "a", "o", "no", "na",
            "ate", "ou", "por", "pra", "anti"}
# Frases de propaganda que saem do nome antes de tudo
PROPAGANDA = [r"\b(?:[ao]\s+)?mais\s+(?:querid|vendid)[oa]s?(?:\s+do\s+brasil)?\b",
              r"\bsucesso(?:\s+de\s+vendas)?\b", r"\bviral(?:\s+(?:do|no)\s+tiktok)?\b",
              r"\bqueridinh[oa]s?(?:\s+do\s+brasil)?\b", r"\blan[cç]amento\b", r"\bpromo[cç][aã]o\b"]
SIGLAS = {"tv", "lg", "led", "usb", "pvc", "jbl", "wap", "btu", "hd", "rgb", "uv", "tcl", "wifi"}

GRAFIA_MARCAS = {normalizar(m): m for m in MARCAS if " " not in m}

def nome_valido(nome, palavra=None):
    # Pelo menos 2 palavras de verdade e, se souber a busca, todas as palavras dela no nome
    reais = [w for w in re.findall(r"[^\W\d_]+", nome)
             if len(w) >= 2 and normalizar(w) not in PALAVRAS_VAZIAS | PEQUENAS]
    if len(reais) < 2:
        return False
    if palavra is not None and COMBINA_EM_QUALQUER_LUGAR:
        return combina(nome, palavra)          # (perfume) com os sinônimos: "Eau de Parfum" vale como "perfume"
    return palavra is None or set(termos(palavra)) <= set(termos(nome))

def nome_curto(nome, palavra=None):
    # Verificação dupla: limpa cada pedaço do nome (entre "+", "|", " - ", vírgula...) e só
    # aceita um resultado que faça sentido. Se nenhum fizer, devolve None e o produto é descartado.
    nome = re.sub(r"^\s*(?:\d+\s*(?:,|ou|e|a|/)\s*)+\d+\s+", "", nome)   # "1, 2 ou 4 Capa..." -> "Capa..."
    nome = re.sub(r"\b\d+\s+(?:a|ou)\s+\d+\b\s*", "", nome)             # "Kit 5 a 25 Toalhas" -> "Kit Toalhas"
    nome = re.sub(r"^\s*\d+(?:[.,]\d+)?\s*(?:metros?|litros?|pe[çc]as?|p[çc]s|unidades?|un|"
                  r"l|ml|kg|g|cm|mm|m|w|v)\b\.?(?:\s+de\b)?\s*", "", nome,
                  flags=re.IGNORECASE)                                   # "1.8L Panela..." / "40 Metros Hera..." -> "Panela..." / "Hera..."
    nome = re.sub(r"^\s*(?:metros?|litros?|pe[çc]as?|unidades?)\s+(?:de\s+)?", "", nome,
                  flags=re.IGNORECASE)                                   # sobrou a unidade sozinha no começo
    nome = re.sub(r"^\s*\d+\s+(?=[^\W\d_])", "", nome)                  # "1 Planta Artificial" -> "Planta Artificial"
    for padrao in PROPAGANDA:                                            # "A MAIS Querida do Brasil!" sai
        nome = re.sub(padrao, " ", nome, flags=re.IGNORECASE)
    pedacos = [p for p in re.split(r"\s+[|–—+-]\s+|[,;()\[\]|!?]", nome) if p.strip()]   # "+" só com espaço (Black+Decker fica)
    for pedaco in pedacos:
        limpo = limpar_nome(pedaco)
        if nome_valido(limpo, palavra):
            return limpo
    return None

def limpar_nome(nome):
    # Tira palavras de enfeite, limita o tamanho e arruma maiúsculas
    nome = re.sub(r"\b[Cc]/\s*", "com ", nome)
    nome = re.sub(r"\b[Ss]/\s*", "sem ", nome)
    tudo_maiusculo = nome.isupper()
    saida, contadas = [], 0
    for palavra in nome.split():
        if "/" in palavra and not any(c.isdigit() for c in palavra):
            palavra = palavra.split("/")[0]                              # "Multi-camadas/de" -> "Multi-camadas"
            if not palavra:
                continue
        base = normalizar(palavra).strip(".!:")
        if base in ENFEITES or re.fullmatch(r"20\d\d", base):
            continue
        if base in ("ate", "faz", "rende", "tipo") and saida:   # "Até 150kg", "Rende 50L", "Tipo...": especificação
            break
        if base not in PEQUENAS:
            if contadas == MAX_PALAVRAS_NOME:
                break
            contadas += 1
        if base in GRAFIA_MARCAS:
            saida.append(GRAFIA_MARCAS[base])                            # "black+decker" -> "Black+Decker"
        elif base in SIGLAS:
            saida.append(palavra.upper())
        elif base in PEQUENAS and saida:
            saida.append(palavra.lower())
        elif any(c.isdigit() for c in palavra) or (palavra.isupper() and len(palavra) <= 4 and not tudo_maiusculo):
            saida.append(palavra)
        else:
            saida.append(palavra[:1].upper() + palavra[1:].lower())
    while saida and (normalizar(saida[-1]) in PEQUENAS or saida[-1].isdigit()
                     or (len(saida[-1]) <= 2 and normalizar(saida[-1]) not in SIGLAS)):
        saida.pop()
    return " ".join(saida) or nome.strip()

imagens_baixadas = {}

def baixar_imagem(url):
    # Baixa cada foto uma vez só (serve para o teste de fundo branco e para a IA)
    if url not in imagens_baixadas:
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                imagens_baixadas[url] = resp.read()
        except Exception:
            imagens_baixadas[url] = None
        if len(imagens_baixadas) > 60:
            del imagens_baixadas[next(iter(imagens_baixadas))]
    return imagens_baixadas.get(url)

def chamar_gemini(partes, json_saida=False):
    chave = cfg.get("GEMINI_KEY")
    if not chave:
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODELO}:generateContent"
    config = {"temperature": 0.2}
    if json_saida:
        config["responseMimeType"] = "application/json"
    corpo = json.dumps({"contents": [{"parts": partes}], "generationConfig": config}).encode()
    req = urllib.request.Request(url, data=corpo, method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": chave})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            dados = json.loads(resp.read())
        return dados["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"  Aviso: IA indisponível ({type(e).__name__}). Usando só as regras.")
        return None

def validar_nome_ia(nome, p, palavra):
    # O nome da IA só vale se tiver o produto buscado, a marca (quando existir), no máximo
    # 8 palavras e nenhuma palavra inventada fora do título original
    marca = marca_do_produto(p)
    nome = (nome or "").strip().splitlines()[0].strip(" \"'“”.*-") if (nome or "").strip() else ""
    permitidos = set(termos(p["productName"])) | set(termos(palavra)) | set(termos(marca or ""))
    if (not nome or len(nome) > 60 or len(nome.split()) > 8
            or not nome_valido(nome, palavra) or bloqueado(nome)
            or (marca and normalizar(marca) not in normalizar(nome))
            or not set(termos(nome)) <= permitidos):
        return None
    return nome

def revisar_com_ia(p, palavra):
    # Segunda verificação (só com GEMINI_KEY): a IA vê a foto e os dados do post, sugere um nome
    # limpo e diz se o post segue o modelo ideal. Devolve None quando não dá para usar a IA.
    marca = marca_do_produto(p)
    pedido = (
        f"Você revisa posts de um canal de {NICHO_IA} da Shopee para o público brasileiro.\n"
        + TEXTO_MODELO_IA
        + ("Este tipo de produto precisa de COR SÓBRIA: recuse se o produto da foto for rosa, laranja, verde, "
           "amarelo, roxo ou vermelho vivo; aceite preto, branco, cinza, bege, marrom, azul ou ciano. "
           "Cortina blackout boa é preta, branca, cinza ou marrom.\n" if pede_cor_sobria(palavra) else "")
        + f"Tipo buscado: {palavra}\nTítulo original: {p['productName']}\n"
        f"Marca: {marca or 'nenhuma'}\nPreço: R$ {preco_br(p['price'])} "
        f"({int(float(p.get('priceDiscountRate') or 0))}% de desconto)\n"
        f"Desconto grande: {'sim' if desconto_grande(p) else 'não'}\n"
        + TEXTO_CHAMADA_IA +
        "Responda só em JSON, assim: {\"nome\": \"título curto e natural em português, até 6 palavras, "
        "com o tipo do produto" + (f" e a marca {marca}" if marca else "") + ", sem inventar nada\", "
        "\"chamada\": \"...\", \"beneficio\": \"...\", "
        "\"foto\": \"real\" ou \"catalogo\" ou \"ia\", \"aprovado\": true ou false, "
        "\"motivo\": \"explicação curta\"}")
    partes = [{"text": pedido}]
    imagem = baixar_imagem(p.get("imageUrl", ""))
    if imagem:
        partes.append({"inline_data": {"mime_type": "image/jpeg",
                                       "data": base64.b64encode(imagem).decode()}})
    resposta = chamar_gemini(partes, json_saida=True)
    if not resposta:
        return None
    try:
        dados = json.loads(resposta.strip().strip("`").removeprefix("json").strip())
    except ValueError:
        return None
    foto = str(dados.get("foto", "")).lower()
    aprovado = bool(dados.get("aprovado")) and foto != "ia"
    motivo = str(dados.get("motivo") or ("foto de IA" if foto == "ia" else "fora do modelo ideal"))
    return {"aprovado": aprovado, "nome": validar_nome_ia(dados.get("nome"), p, palavra),
            "foto": foto, "motivo": motivo, "chamada": validar_chamada_ia(dados.get("chamada"), p),
            "beneficio": validar_beneficio_ia(dados.get("beneficio"))}

# ---------- Chamada e frase de benefício escritas pela IA (06/11, pedido do Gabriel) ----------
# Antes a chamada era sorteada de uma lista ("VALE MUITO A PENA", "SUA CASA MERECE") e saía genérica:
# "SUA CASA MERECE" num kit de garrafa térmica não faz sentido. Agora a IA olha a FOTO e o produto primeiro
# e escreve uma chamada que fala do uso dele, mais uma frase de benefício (como os canais que mais engajam:
# "Perfeito para guardar tudo e ainda deixar o quarto mais elegante 😍"). Chamada de preço só com desconto
# grande. Se a IA falhar ou escrever algo genérico, volta a lista antiga (escolher_chamada).
MOSTRAR_BENEFICIO = False     # 06/11: o Gabriel gostou da chamada, mas não quer a frase de benefício no post
DESCONTO_GRANDE = 40          # % a partir do qual chamada de preço ("OLHA ESSE PREÇO") faz sentido
CHAMADAS_PROIBIDAS = ["VALE MUITO A PENA", "SUA CASA MERECE", "ACHADO DO DIA", "TODO MUNDO TÁ LEVANDO",
                      "QUEM VIU, LEVOU", "QUEM VIU LEVOU", "ESSE PREÇO NÃO É TODO DIA", "OFERTA IMPERDÍVEL",
                      "CASA BONITA GASTANDO POUCO", "PROMOÇÃO", "CONFIRA"]
CHAMADAS_DE_PRECO = ["PREÇO", "BARATO", "DESCONTO", "OFF", "%", "CORRE", "ACABA", "QUEIMA", "BAIXOU"]
TEXTO_CHAMADA_IA = (
    "Agora escreva o texto do post. PRIMEIRO olhe a foto e entenda o que é o produto e para que serve.\n"
    "\"chamada\": 2 a 5 palavras em MAIÚSCULAS, começando com 1 emoji que combine com o produto, falando do "
    "USO ou do BENEFÍCIO concreto deste produto, com jeito de amiga indicando. Exemplos do estilo: garrafa "
    "térmica -> \"☕ CAFÉ QUENTE O DIA TODO\"; rolo de massa -> \"🥟 MASSA CASEIRA SEM ESFORÇO\"; caixa térmica "
    "-> \"🧊 BEBIDA GELADA NO ROLÊ\"; fechadura digital -> \"🔐 ADEUS, CHAVE PERDIDA\"; abajur -> \"💡 LUZ "
    "GOSTOSA PRA LER\"; mop espanador -> \"🧹 POEIRA ATÉ EMBAIXO DA CAMA\". PROIBIDO frase que serve para "
    "qualquer produto: \"VALE MUITO A PENA\", \"SUA CASA MERECE\", \"ACHADO DO DIA\", \"TODO MUNDO TÁ LEVANDO\", "
    "\"QUEM VIU, LEVOU\". Chamada sobre preço (\"😱 OLHA ESSE PREÇO\", \"📉 METADE DO PREÇO\") só se "
    "Desconto grande = sim.\n"
    "\"beneficio\": 1 frase curta (8 a 16 palavras), natural, dizendo para que serve ou por que é bom, "
    "terminando com 1 emoji. Só o que a foto e o título mostram; não invente medida, material ou função.\n"
    "ORTOGRAFIA: antes de responder, revise \"nome\", \"chamada\" e \"beneficio\" palavra por palavra: português "
    "do Brasil correto, com todos os acentos (É, Ã, Ç, Ê...), sem letra trocada ou faltando, e a frase tem que "
    "fazer sentido para este produto. Gíria leve (\"pra\", \"tá\", \"rolê\") pode; erro de escrita não. "
    "O \"nome\" começa pelo produto, nunca por medida ou unidade solta (errado: \"Metros Hera Verde\"; certo: "
    "\"Hera Artificial Trepadeira 40 Metros\"). Se for pacote ou kit (título ou foto mostram a quantidade), "
    "o \"nome\" diz quantas unidades vêm (ex.: \"Lenço Umedecido Pampers 592 Unidades\", \"Kit 10 Panos de Prato\"). "
    "Móvel, mesa, cortina, geladeira, freezer, forno e micro-ondas: o \"nome\" diz a medida ou os litros que o título "
    "mostra (ex.: \"Mesa de Jantar Madesa 1,60m 6 Lugares\", \"Cortina Blackout 2,80m x 2,30m\", \"Geladeira Brastemp "
    "375 Litros\", \"Forno Elétrico Philco 46 Litros\").\n")

def desconto_grande(p):
    # Anúncio com versões de preços diferentes: "METADE DO PREÇO" seria de outra versão, então não vale
    return float(p.get("priceDiscountRate") or 0) >= DESCONTO_GRANDE and variacao_preco(p) <= VARIACAO_A_PARTIR

def validar_chamada_ia(chamada, p):
    chamada = " ".join(str(chamada or "").split()).upper()
    if not chamada or len(chamada) > 45 or len(chamada.split()) > 7:
        return None
    sem_emoji = re.sub(r"[^\wÀ-ÿ%, ]", "", chamada).strip()
    if any(proibida in sem_emoji for proibida in CHAMADAS_PROIBIDAS):
        return None
    if not desconto_grande(p) and any(t in chamada for t in CHAMADAS_DE_PRECO):
        return None                                # fala de preço sem o desconto justificar
    if not re.match(r"^[^\wÀ-ÿ]", chamada):         # sem emoji no começo: põe um neutro
        chamada = "✨ " + chamada
    return chamada

def validar_beneficio_ia(beneficio):
    beneficio = " ".join(str(beneficio or "").split())
    if not beneficio or len(beneficio) > 140 or len(beneficio.split()) < 5 or "http" in beneficio:
        return None
    return beneficio[0].upper() + beneficio[1:]

# Cor sóbria (06/11, Gabriel): em cortina, cama, tapete, sofá etc. a foto não pode ter cor chamativa
# (rosa, laranja, verde, amarelo, roxo, vermelho vivo). Bom: preto, branco, cinza, bege, marrom, azul/ciano.
# Ex.: cortina blackout rosa não faz sentido; blackout preta, branca ou marrom sim.
COR_SOBRIA_TIPOS = ["cortina", "persiana", "jogo de cama", "lençol", "jogo de lençol", "colcha", "edredom",
                    "cobertor", "manta", "toalha", "tapete", "passadeira de tapete", "sofá", "poltrona", "puff",
                    "almofada", "capa de sofá", "cadeira estofada", "cabeceira", "cama box", "colchão",
                    "recamier", "pillow top", "fronha", "dossel", "biombo"] + COR_SOBRIA_EXTRA
LIMITE_COR_CHAMATIVA = 0.12   # mais que 12% da foto em cor chamativa = recusa

def pede_cor_sobria(palavra):
    busca = normalizar(palavra)
    if "natal" in busca or "ano novo" in busca:  # decoração de época: vermelho e dourado são o certo
        return False
    return any(re.search(r"(?<!\w)" + re.escape(normalizar(t)), busca) for t in COR_SOBRIA_TIPOS)

def cor_chamativa(url):
    # Quanto da foto é cor chamativa (0 a 1). Marrom, bege e azul não contam: marrom é laranja escuro,
    # bege é laranja quase sem cor; o rosa claro (rosa bebê) conta mesmo sendo clarinho.
    if Image is None:
        return 0
    try:
        img = Image.open(io.BytesIO(baixar_imagem(url))).convert("HSV").resize((60, 60))
    except Exception:
        return 0
    chamativos = 0
    for h, s, v in img.getdata():
        h, s, v = h * 360 / 255, s / 255, v / 255
        rosa = (290 <= h < 350 and s > 0.15 and v > 0.45) or ((h >= 350 or h < 8) and s > 0.2 and v > 0.6)
        laranja = 12 <= h < 42 and s > 0.6 and v > 0.75
        amarelo = 42 <= h < 68 and s > 0.55 and v > 0.7
        verde = 68 <= h < 165 and s > 0.35 and v > 0.4
        roxo = 255 <= h < 290 and s > 0.3 and v > 0.35
        if rosa or laranja or amarelo or verde or roxo:
            chamativos += 1
    return chamativos / 3600

def fundo_branco(url):
    # Olha a borda da foto: se quase tudo for branco, é foto "de catálogo" sem graça
    if Image is None:
        return False
    try:
        img = Image.open(io.BytesIO(baixar_imagem(url))).convert("RGB").resize((60, 60))
    except Exception:
        return False
    borda = [img.getpixel((x, y)) for x in range(60) for y in range(60)
             if x < 4 or y < 4 or x > 55 or y > 55]
    brancos = sum(1 for r, g, b in borda if min(r, g, b) >= 235)
    return brancos / len(borda) >= LIMITE_FUNDO_BRANCO

def foto_com_fundo(url):
    # Produto branco em fundo branco quase some: pinta só o fundo (o branco que encosta na
    # borda da foto) de uma cor clarinha, e o produto se destaca. Devolve None se não precisar.
    if Image is None or not COR_FUNDO or not fundo_branco(url):
        return None
    try:
        from PIL import ImageChops, ImageDraw, ImageFilter
        img = Image.open(io.BytesIO(baixar_imagem(url))).convert("RGB")
        w, h = img.size
        passo = max(1, min(w, h) // 20)
        pontos = ([(x, y) for x in range(0, w, passo) for y in (0, h - 1)]
                  + [(x, y) for y in range(0, h, passo) for x in (0, w - 1)])
        marcada = img.copy()                       # marca o fundo de magenta para virar máscara
        for xy in pontos:
            if min(marcada.getpixel(xy)) >= 235:   # ainda branco (não marcado nem produto)
                ImageDraw.floodfill(marcada, xy, (255, 0, 255), thresh=TOLERANCIA_FUNDO)
        # O que mudou entre a marcada e a original é o fundo
        mascara = ImageChops.difference(marcada, img).convert("L").point(lambda v: 255 if v else 0)
        mascara = mascara.filter(ImageFilter.GaussianBlur(1))   # borda suave, sem serrilhado
        img = Image.composite(Image.new("RGB", img.size, COR_FUNDO), img, mascara)
        saida = io.BytesIO()
        img.save(saida, "JPEG", quality=92)
        return saida.getvalue()
    except Exception as e:
        print(f"  Aviso: não deu para ajustar o fundo da foto ({type(e).__name__}).")
        return None

def carregar_historico(quantos=None):
    try:
        with open(ARQUIVO_HISTORICO, encoding="utf-8") as f:
            linhas = [l.rstrip("\n").split("\t", 1) for l in f if "\t" in l]
    except FileNotFoundError:
        return []
    return linhas[-(quantos or SEM_REPETIR):]

def chave_nome(nome):
    # Mesmo anúncio com outro link/loja (ex.: Air Fryer Philco 11L saiu 2x): compara o nome sem maiúsculas e espaços
    return "nome:" + " ".join(nome.lower().split())

def nomes_ja_postados():
    # TODOS os nomes já postados (o historico.txt inteiro, não só os últimos 15)
    try:
        with open(ARQUIVO_HISTORICO, encoding="utf-8") as f:
            return {chave_nome(l.rstrip("\n").split("\t", 1)[1]) for l in f if "\t" in l}
    except FileNotFoundError:
        return set()

def salvar_historico(palavra, nome):
    with open(ARQUIVO_HISTORICO, "a", encoding="utf-8") as f:
        f.write(f"{palavra}\t{' '.join(nome.split())}\n")

ARQUIVO_ITENS_POSTADOS = "itens_postados.txt"   # itemId<TAB>busca (08/11: para ligar a venda à categoria)

def salvar_item_postado(item_id, palavra):
    try:
        with open(ARQUIVO_ITENS_POSTADOS, "a", encoding="utf-8") as f:
            f.write(f"{item_id}\t{palavra}\n")
    except OSError as e:
        print("  Aviso: não consegui anotar o item postado:", e)

def registrar_no_obsidian(p, palavra, caro, link):
    # Uma linha por post na nota do mês (Postagens/Postagens AAAA-MM.md)
    if not PASTA_OBSIDIAN or not os.path.isdir(PASTA_OBSIDIAN):
        return
    agora = datetime.now()
    pasta = os.path.join(PASTA_OBSIDIAN, "Postagens")
    arquivo = os.path.join(pasta, f"Postagens {agora:%Y-%m}.md")
    try:
        os.makedirs(pasta, exist_ok=True)
        novo = not os.path.exists(arquivo)
        with open(arquivo, "a", encoding="utf-8") as f:
            if novo:
                f.write(f"---\ntags: [bot-ofertas, postagens]\n---\n# 📝 Postagens {agora:%m/%Y}\n\n"
                        "| Quando | Tipo | Palavra | Produto | Preço | Desconto | Comissão | Vendidos |\n"
                        "|---|---|---|---|--:|--:|--:|--:|\n")
            nome = (p.get("nome_post") or p["productName"]).replace("|", "/").replace("[", "(").replace("]", ")")
            vendidos = f"{int(p.get('sales') or 0):,}".replace(",", ".")
            f.write(f"| {agora:%d/%m %H:%M} | {'💎 caro' if caro else 'simples'} | {palavra} | [{nome}]({link}) "
                    f"| R$ {preco_br(p['price'])} | {int(float(p.get('priceDiscountRate') or 0))}% "
                    f"| {float(p.get('commissionRate') or 0) * 100:.0f}% | {vendidos} |\n")
    except OSError as e:
        print("  Aviso: não consegui anotar no Obsidian:", e)

def ler_contagem(arquivo, minimo, maximo):
    # Guarda: posts desde a última mensagem e em qual post sai a próxima
    try:
        with open(arquivo, encoding="utf-8") as f:
            contagem, alvo = map(int, f.read().split())
        return contagem, alvo
    except (FileNotFoundError, ValueError):
        return 0, random.randint(minimo, maximo)

def salvar_contagem(arquivo, contagem, alvo):
    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(f"{contagem} {alvo}\n")

def mandar_mensagem(texto):
    return chamar_telegram("sendMessage", {"chat_id": cfg[CHAVE_CANAL], "parse_mode": "HTML", "text": texto,
                                           "link_preview_options": '{"is_disabled": true}',
                                           "disable_notification": "true" if horario_silencioso() else "false"})

def texto_grupos(canal="telegram"):
    e = ESTILOS[canal]
    esc = e["escapar"]
    hora = datetime.now().hour
    saudacao = next((s for ini, fim, s in SAUDACOES if ini <= hora < fim), SAUDACOES[0][2])
    grupos = [(nome, link) for nome, link in GRUPOS if link.startswith("http")]   # sem link ainda: fica de fora
    if len(grupos) > 1:
        convite = ("👉 Conhece nossos grupos de ofertas? Entra no que combina com você "
                   "ou manda pra família e pros amigos:\n\n")
    else:
        convite = "📲 Manda o link do grupo pra família e pros amigos aproveitarem também:\n\n"
    periodo = "dia" if hora < 12 else "tarde" if hora < 18 else "noite"
    frase = random.choice(FRASES_GRUPO.get(periodo) or [""])
    texto = f"{e['negrito'].format(esc(saudacao))}\n\n" + (f"{esc(frase)}\n\n" if frase else "")
    if linha_campanha():                           # 11.11, Black Friday, 12.12 (no dia e na véspera)
        texto += e["negrito"].format(esc(linha_campanha())) + "\n\n"
    texto += convite
    texto += "".join(f"{e['negrito'].format(esc(nome))}\n{esc(link)}\n\n" for nome, link in grupos)
    return texto + "🔔 Dica: fixa o grupo e ativa as notificações pra não perder nenhum achado!"

def carregar_cupons():
    return cupons.ler(os.path.join(PASTA_PRINCIPAL, "cupons.txt"))

def texto_cupons(lista, canal="telegram"):
    e = ESTILOS[canal]
    esc = e["escapar"]
    texto = e["negrito"].format("🚨 ALERTA DE CUPOM") + "\n\n"
    for c in lista:
        texto += (f"🎟️ {e['codigo'].format(esc(c['codigo']))}\n{esc(c['descricao'])}\n"
                  f"⏰ Válido até {c['validade']:%d/%m}\n\n")
    if LINK_CUPONS:
        texto += f"👉 Pegue mais cupons aqui: {esc(LINK_CUPONS)}\n\n"
    dica = "Toque no código para copiar e cole no carrinho" if canal == "telegram" else "Copie o código e cole no carrinho"
    return texto + f"📋 {dica} da Shopee. Cupons limitados: use antes que acabem!"

def mandar_alerta_cupons():
    # Devolve True se mandou (ou se não tem cupom valendo, aí não tem o que mandar)
    lista = carregar_cupons()
    if not lista or LOJA == "mercadolivre":     # cupom da Shopee não vai no grupo do Mercado Livre
        return True
    try:
        if TELEGRAM_POSTAR:
            mandar_mensagem(texto_cupons(lista, "telegram"))
        if destinos_whatsapp():
            r = chamar_whatsapp("/enviar", {"destinos": destinos_whatsapp(),
                                            "texto": texto_cupons(lista, "whatsapp"), "imagem": None})
            if not r.get("ok"):
                raise RuntimeError(r.get("erro") or "WhatsApp não aceitou")
        print(f"  Alerta de cupom enviado ({len(lista)} cupom(ns)).")
        return True
    except Exception as e:
        print(f"  Não deu para mandar o alerta de cupom ({type(e).__name__}); tenta no próximo post.")
        return False

def enviar_mensagem_grupos(quando):
    # Mensagem "Bom dia/Boa tarde/Boa noite + links dos grupos". Devolve True se saiu.
    try:
        if TELEGRAM_POSTAR:
            mandar_mensagem(texto_grupos("telegram"))
        if destinos_whatsapp():
            # Só texto (sem foto), nos mesmos grupos dos posts
            r = chamar_whatsapp("/enviar", {"destinos": destinos_whatsapp(),
                                            "texto": texto_grupos("whatsapp"), "imagem": None})
            if not r.get("ok"):
                raise RuntimeError(r.get("erro") or "WhatsApp não aceitou")
        print(f"  Mensagem dos grupos enviada ({quando}).")
        return True
    except Exception as e:
        print(f"  Não deu para mandar a mensagem dos grupos ({type(e).__name__}); tenta no próximo post.")
        return False

def contar_post_e_mandar_extras():
    # Chamado a cada post feito: quando chega no número sorteado, manda a mensagem dos grupos
    # e o alerta de cupom (cada um com a sua contagem)
    if GRUPOS:
        contagem, alvo = ler_contagem(ARQUIVO_GRUPOS, GRUPOS_MIN, GRUPOS_MAX)
        contagem += 1
        if contagem >= alvo and enviar_mensagem_grupos(f"depois de {contagem} posts"):
            contagem, alvo = 0, random.randint(GRUPOS_MIN, GRUPOS_MAX)
        salvar_contagem(ARQUIVO_GRUPOS, contagem, alvo)
    if carregar_cupons() and LOJA != "mercadolivre":   # os cupons são da Shopee: não vão no grupo de perfume
        contagem, alvo = ler_contagem(ARQUIVO_CONTAGEM_CUPONS, CUPONS_MIN, CUPONS_MAX)
        contagem += 1
        if contagem >= alvo and mandar_alerta_cupons():
            contagem, alvo = 0, random.randint(CUPONS_MIN, CUPONS_MAX)
        salvar_contagem(ARQUIVO_CONTAGEM_CUPONS, contagem, alvo)

def vez_do_caro(historico):
    # Conta os posts simples desde o último caro: o caro sai entre o MIN-ésimo e o MAX-ésimo post
    # (sorteado; no pico, com os números do pico)
    if PICO_INICIO <= datetime.now().hour < PICO_FIM:
        minimo, maximo = CARO_PICO_MIN, CARO_PICO_MAX
    else:
        minimo, maximo = CARO_A_CADA_MIN, CARO_A_CADA_MAX
    simples = 0
    for palavra, _ in reversed(historico):
        if palavra in CAROS:
            break
        simples += 1
    if simples >= maximo - 1:
        return True
    return simples >= minimo - 1 and random.random() < 1 / (maximo - simples)

def valor_comissao(p):
    # Quanto a gente ganha por venda, em R$
    return float(p.get("price") or 0) * float(p.get("commissionRate") or 0)

def comissao_boa(p):
    return (float(p.get("commissionRate") or 0) * 100 >= COMISSAO_MINIMA
            or valor_comissao(p) >= VALOR_COMISSAO_MINIMO)

def pontuacoes(candidatos):
    # Cada critério é dividido pelo maior valor da rodada; vendas em escala logarítmica
    vendas = [math.log1p(int(p.get("sales") or 0)) for p in candidatos]
    notas = [float(p.get("ratingStar") or 0) for p in candidatos]
    comissoes = [math.log1p(valor_comissao(p)) for p in candidatos]
    descontos = [float(p.get("priceDiscountRate") or 0) for p in candidatos]
    precos = [float(p.get("price") or 0) for p in candidatos]
    max_v, max_n, max_c = max(vendas) or 1, max(notas) or 1, max(comissoes) or 1
    max_d = max(descontos) or 1
    min_p = min((x for x in precos if x > 0), default=1)
    # Dia de campanha (11.11, Black Friday, 12.12): o desconto vale o dobro na escolha (é o que o povo caça)
    peso_d = PESO_DESCONTO * (CAMPANHA_PESO_DESCONTO if estado_campanha["fase"] == "dia" else 1)
    return [PESO_VENDAS * v / max_v + PESO_NOTA * n / max_n + PESO_COMISSAO * c / max_c
            + peso_d * d / max_d + PESO_PRECO * (min_p / pr if pr > 0 else 0)
            + (BONUS_COMISSAO_EXTRA if comissao_extra(p) > 0 else 0)
            for v, n, c, d, pr, p in zip(vendas, notas, comissoes, descontos, precos, candidatos)]

# Anúncio com VERSÕES de preços diferentes (06/11, a mãe do Gabriel: varal "com abas" na foto por R$ 59,90, mas
# os 59,90 eram do "sem abas" mais simples, "quase uma enganação"). A Shopee manda priceMin e priceMax:
#   diferença até 15%: post normal | até 60%: "A partir de R$ X" (sem o "De" riscado) e aviso de que o preço muda
#   conforme o modelo | mais de 60%: não posta (a versão barata é isca)
# 06/11, decisão do Gabriel ("menos dor de cabeça: a foto é daquele produto, o preço é daquele produto"):
# só posta anúncio de PREÇO ÚNICO. Versões de cor/voltagem com o mesmo preço passam; versões com preço diferente
# (até 15% é arredondamento/voltagem) não. O "A partir de" fica no código, mas não é mais usado.
VARIACAO_A_PARTIR = 1.15
VARIACAO_MAXIMA = 1.15

def faixa_preco(p):
    minimo = float(p.get("priceMin") or p.get("price") or 0)
    maximo = float(p.get("priceMax") or minimo)
    return minimo, max(minimo, maximo)

def variacao_preco(p):
    minimo, maximo = faixa_preco(p)
    return maximo / minimo if minimo > 0 else 1.0

def eh_tv(palavra):
    b = normalizar(palavra)
    return b.startswith(("smart tv", "tv ")) or b in ("tv", "televisao") or b.startswith("televisao")

def polegadas(nome, palavra=""):
    # "Smart TV 55\" 4K", "55 Polegadas", "TV 43 pol"; senão o tamanho da busca ("smart tv 55")
    n = normalizar(nome).replace("”", '"').replace("''", '"')
    for padrao in (r'(?<![\d.,])(\d{2,3})\s*(?:"|pol\b|polegadas|inch|in\b)', r'\btv\s*(?:led\s*|smart\s*)?(\d{2,3})\b'):
        m = re.search(padrao, n)
        if m and 19 <= int(m.group(1)) <= 120:
            return int(m.group(1))
    m = re.search(r"(\d{2,3})\b", normalizar(palavra))
    return int(m.group(1)) if m and 19 <= int(m.group(1)) <= 120 else None

def teto_tv(pol):
    tamanhos = [t for t in sorted(TETO_TV) if t <= pol]
    return TETO_TV[tamanhos[-1]] if tamanhos else min(TETO_TV.values())

def tv_cara(p, palavra):
    # True se é TV e o preço passa do teto do tamanho (TV sem tamanho no título nem na busca não é barrada)
    if not eh_tv(palavra):
        return False
    pol = polegadas(p["productName"], palavra)
    return bool(pol) and float(p.get("price") or 0) > teto_tv(pol)

def preco_por_polegada(p, palavra):
    pol = polegadas(p["productName"], palavra) if eh_tv(palavra) else None
    return float(p.get("price") or 0) / pol if pol else 0

chamadas_recentes = []

def chamadas_do_tipo(palavra):
    # Pega o grupo cujo trecho mais longo aparece (como palavra inteira) na palavra buscada
    busca = normalizar(palavra)
    melhor, frases = 0, []
    for trechos, opcoes in CHAMADAS_POR_TIPO:
        for t in trechos:
            t = normalizar(t)
            if len(t) > melhor and re.search(r"(?<!\w)" + re.escape(t) + r"(?!\w)", busca):
                melhor, frases = len(t), opcoes
    return frases

def escolher_chamada(p, palavra, caro):
    if p.get("chamada_ia"):                    # a IA viu a foto e escreveu uma chamada deste produto
        chamadas_recentes.append(p["chamada_ia"])
        del chamadas_recentes[:-5]
        return p["chamada_ia"]
    opcoes = CHAMADAS_GERAIS + (CHAMADAS_CARO if caro else []) + chamadas_do_tipo(palavra)
    vendas = int(p.get("sales") or 0)
    desconto = int(float(p.get("priceDiscountRate") or 0))
    if vendas >= 1000:
        opcoes.append(f"🔥 MAIS DE {vendas // 1000} MIL VENDIDOS")
    if desconto >= DESCONTO_MINIMO_RISCADO:
        opcoes.append("🚨 BAIXOU O PREÇO")
    if desconto >= 40:
        opcoes.append(f"📉 {desconto}% MAIS BARATO")
    if float(p["price"]) <= 50:
        opcoes.append("🤑 BARATINHO DEMAIS")
    if float(p["price"]) <= 100:
        opcoes += CHAMADAS_ATE_100
    # Sem a IA: tira as frases genéricas e fica com as que dizem um fato ou combinam com o tipo
    opcoes = [c for c in opcoes if not any(pr in c for pr in CHAMADAS_PROIBIDAS)] or opcoes
    if not desconto_grande(p):                 # "OLHA ESSE PREÇO" só com desconto grande de verdade
        opcoes = [c for c in opcoes if c == "🚨 BAIXOU O PREÇO"
                  or not any(t in c for t in CHAMADAS_DE_PRECO)] or opcoes
    opcoes = [c for c in opcoes if c not in chamadas_recentes] or opcoes
    chamada = random.choice(opcoes)
    chamadas_recentes.append(chamada)
    del chamadas_recentes[:-5]
    return chamada

# Cada app escreve negrito e riscado de um jeito
ESTILOS = {
    "telegram": {"negrito": "<b>{}</b>", "riscado": "<s>{}</s>", "codigo": "<code>{}</code>",
                 "escapar": html.escape},
    "whatsapp": {"negrito": "*{}*", "riscado": "~{}~", "codigo": "`{}`", "escapar": lambda t: t},
}

def montar_texto(p, chamada, canal="telegram", link=None):
    e = ESTILOS[canal]
    esc = e["escapar"]
    preco = float(p["price"])
    desconto = int(float(p.get("priceDiscountRate") or 0))
    vendas = int(p.get("sales") or 0)
    nota = float(p.get("ratingStar") or 0)
    nome = p.get("nome_post") or nome_curto(p["productName"]) or p["productName"]
    texto = f"{esc(chamada)}\n\n{e['negrito'].format(esc(nome))}\n\n"
    if estado_campanha["fase"] == "dia":           # selo da campanha (11.11, Black Friday, 12.12) em cima do post
        loja_nome = "MERCADO LIVRE" if p.get("loja") == "mercadolivre" else "SHOPEE"
        texto = e["negrito"].format(esc(f"🛍️ {estado_campanha['nome']} {loja_nome}")) + "\n" + texto
    if MOSTRAR_BENEFICIO and p.get("beneficio"):   # frase da IA: para que serve / por que é bom
        texto += f"{esc(p['beneficio'])}\n\n"
    if variacao_preco(p) > VARIACAO_A_PARTIR:
        # Versões com preços diferentes: honesto é "a partir de", sem o "De" riscado (que é de outra versão)
        texto += e["negrito"].format(f"A partir de R$ {preco_br(preco)}") + "\n"
        texto += "(o preço muda conforme o modelo escolhido)\n"
    else:
        if DESCONTO_MINIMO_RISCADO <= desconto < 100:
            antigo = float(p.get("precoAntes") or 0) or preco / (1 - desconto / 100)   # ML manda o "de" exato
            texto += f"De {e['riscado'].format('R$ ' + preco_br(antigo))}\n"
        texto += e["negrito"].format(f"Por R$ {preco_br(preco)}" + (" no Pix" if p.get("pixOnly") else "")) + "\n"
    cupom, economia = (cupons.melhor(carregar_cupons(), preco, CUPOM_DESCONTO_MINIMO)
                       if p.get("loja") != "mercadolivre" else (None, 0))   # cupom da Shopee não vale no ML
    if cupom:
        texto += (f"🎟️ Com o cupom {e['codigo'].format(esc(cupom['codigo']))}: "
                  + e["negrito"].format(f"R$ {preco_br(preco - economia)}") + "\n")
    texto += "\n"
    vendidos = f"{vendas // 1000} mil+" if vendas >= 1000 else f"{vendas}+"
    texto += f"⭐ {nota:.1f}".replace(".", ",") + f" | {vendidos} vendidos\n"
    if p.get("loja") == "mercadolivre":
        texto += (esc(selo_loja_ml(p)) + "\n") if selo_loja_ml(p) else ""
    elif loja_oficial(p):
        texto += "✅ Loja Oficial Shopee\n"
    elif loja_indicada(p):
        texto += "✅ Loja Indicada Shopee\n"
    texto += f"\n🛒 Compre aqui: {esc(link or p['offerLink'])}"
    return texto

def horario_silencioso():
    hora = datetime.now().hour
    return SILENCIO_INICIO <= hora < SILENCIO_FIM

def chamar_telegram(metodo, campos, foto=None):
    url = f"https://api.telegram.org/bot{cfg['TOKEN']}/{metodo}"
    if foto is None:
        dados, tipo = urllib.parse.urlencode(campos).encode(), "application/x-www-form-urlencoded"
    else:
        # Foto ajustada no próprio bot: vai como arquivo (multipart)
        limite = "----bot" + hashlib.md5(foto).hexdigest()
        partes = [f'--{limite}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
                  for k, v in campos.items()]
        partes.append(f'--{limite}\r\nContent-Disposition: form-data; name="photo"; '
                      f'filename="foto.jpg"\r\nContent-Type: image/jpeg\r\n\r\n'.encode() + foto + b"\r\n")
        dados, tipo = b"".join(partes) + f"--{limite}--\r\n".encode(), f"multipart/form-data; boundary={limite}"
    req = urllib.request.Request(url, data=dados, headers={"Content-Type": tipo})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["ok"]

def postar_no_telegram(p, texto):
    campos = {"chat_id": cfg[CHAVE_CANAL], "parse_mode": "HTML",
              "disable_notification": "true" if horario_silencioso() else "false"}
    foto = foto_com_fundo(p["imageUrl"])
    for tentativa in range(1, TENTATIVAS_ENVIO + 1):
        try:
            if foto:
                return chamar_telegram("sendPhoto", dict(campos, caption=texto), foto)
            return chamar_telegram("sendPhoto", dict(campos, photo=p["imageUrl"], caption=texto))
        except urllib.error.HTTPError as e:
            if e.code == 400 and foto:
                print("  Telegram recusou a foto ajustada, enviando a foto original.")
                foto = None
                continue
            if e.code == 400:
                # O Telegram não aceitou a foto: manda só o texto (o link mostra a prévia do produto)
                print("  Telegram recusou a foto, enviando só o texto.")
                try:
                    return chamar_telegram("sendMessage", dict(campos, text=texto))
                except Exception as e2:
                    print("  Falha ao enviar o texto:", e2)
                    return False
            erro = e
        except Exception as e:
            erro = e
        print(f"  Telegram falhou (tentativa {tentativa}/{TENTATIVAS_ENVIO}): {erro}")
        if tentativa < TENTATIVAS_ENVIO:
            time.sleep(10 * tentativa)
    return False

def avisar_painel(texto):
    # Aviso no painel do Telegram (só para o Gabriel), ex.: WhatsApp pausou
    if not cfg.get("PAINEL_TOKEN") or not cfg.get("PAINEL_ADMIN"):
        return
    try:
        req = urllib.request.Request(f"https://api.telegram.org/bot{cfg['PAINEL_TOKEN']}/sendMessage",
                                     data=urllib.parse.urlencode({"chat_id": cfg["PAINEL_ADMIN"], "text": texto,
                                                                  "parse_mode": "HTML"}).encode())
        urllib.request.urlopen(req, timeout=20).close()
    except Exception as e:
        print("  Não consegui avisar no painel:", type(e).__name__)

def chamar_whatsapp(caminho, dados=None, timeout=90):
    corpo = json.dumps(dados).encode() if dados is not None else None
    req = urllib.request.Request(WHATSAPP_URL + caminho, data=corpo, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}")

def destinos_whatsapp():
    try:
        with open(ARQUIVO_ZAP_DESTINOS, encoding="utf-8") as f:
            return [l.split("#")[0].strip() for l in f if l.split("#")[0].strip()]
    except FileNotFoundError:
        return []

def contagem_whatsapp():
    hoje = datetime.now().strftime("%Y-%m-%d")
    try:
        with open(ARQUIVO_ZAP_CONTAGEM, encoding="utf-8") as f:
            dados = json.load(f)
    except (OSError, ValueError):
        dados = {}
    if dados.get("dia") != hoje:
        dados = {"dia": hoje, "posts": 0, "ultimo": dados.get("ultimo", 0), "proximo": dados.get("proximo")}
    return dados

def motivo_sem_whatsapp():
    # Ritmo próprio do WhatsApp (o chip novo não pode postar no ritmo do Telegram): no máximo
    # WHATSAPP_MAX_DIA por dia, espalhados até a hora de parar, nunca antes de WHATSAPP_INTERVALO.
    # Devolve por que este post não vai para o WhatsApp (None = vai); o log mostra o motivo
    if not destinos_whatsapp():
        return "sem grupo/canal: /zapdestino"
    if os.path.exists(ARQUIVO_ZAP_PAUSA) and not voltou_da_queda():
        return "pausado: /zap mostra o motivo"
    c = contagem_whatsapp()
    faltam = WHATSAPP_MAX_DIA - c["posts"]
    if faltam <= 0:
        return f"já foram os {WHATSAPP_MAX_DIA} de hoje"
    agora = datetime.now()
    # Espalha os posts que faltam até a hora de parar. Com 999 ou mais por dia ("sem limite", modo de
    # teste) não espalha: vale só o intervalo mínimo (ex.: /zapritmo casa 999 1 = 1 a 1,25 min)
    if WHATSAPP_INTERVALO_MAX > WHATSAPP_INTERVALO:
        # Faixa fixa (/zapintervalo): o tempo até o próximo é sorteado UMA vez, logo depois de cada post
        espaco = c.get("proximo") or WHATSAPP_INTERVALO   # sem sorteio ainda (acabou de ligar): o mínimo
        espaco = min(max(espaco, WHATSAPP_INTERVALO), WHATSAPP_INTERVALO_MAX)   # se mudou a faixa no meio
    else:
        espalhar = 0
        if WHATSAPP_MAX_DIA < 999:
            espalhar = 0.8 * minutos_pesados(agora) / faltam
            if PICO_INICIO <= agora.hour < PICO_FIM:
                espalhar /= 2                      # pico: posta no dobro da velocidade
        espaco = max(WHATSAPP_INTERVALO, espalhar) * random.uniform(1, 1.25)
    passou = (time.time() - c["ultimo"]) / 60
    if passou < espaco:
        estado_rodada["espera_zap"] = (espaco - passou) * 60
        return f"último no WhatsApp há {passou:.0f} min, o próximo sai depois de uns {espaco:.0f} min"
    return None

def minutos_pesados(agora):
    # Minutos até a hora de parar, com os do pico contando 2 (o pico recebe o dobro de posts)
    ja = agora.hour * 60 + agora.minute
    fim = HORA_FIM * 60
    pico = max(0, min(fim, PICO_FIM * 60) - max(ja, PICO_INICIO * 60))
    return max(0, fim - ja) + pico

def vez_do_whatsapp():
    return motivo_sem_whatsapp() is None

MARCA_QUEDA = "[queda] "   # pausa por conexão caída: some sozinha quando o WhatsApp volta (07/11)

def voltou_da_queda():
    # Pausa por queda (chip desconectou um pouco, programa reiniciando): se o WhatsApp já voltou,
    # tira a pausa sozinho. Pausa por outro motivo continua esperando o /zapligar.
    try:
        with open(ARQUIVO_ZAP_PAUSA, encoding="utf-8") as f:
            if not f.read().startswith(MARCA_QUEDA):
                return False
        if not chamar_whatsapp("/status", timeout=10).get("conectado"):
            return False
    except Exception:
        return False
    try:
        os.remove(ARQUIVO_ZAP_PAUSA)
    except OSError:
        pass
    print("  WhatsApp voltou: tirei a pausa sozinho")
    return True

def pausar_whatsapp(motivo, queda=False):
    with open(ARQUIVO_ZAP_PAUSA, "w", encoding="utf-8") as f:
        f.write((MARCA_QUEDA if queda else "") + motivo)
    print(f"  WhatsApp PAUSADO: {motivo}" + (" (volta sozinho quando reconectar)" if queda else ""))
    if queda:
        return   # sem aviso aqui: o programa do WhatsApp avisa se a queda passar de 10 min
    avisar_painel(f"⚠️ <b>{html.escape(BOT)}</b>: posts no WhatsApp pausados.\nMotivo: {html.escape(motivo)}\n"
                  f"Quando resolver: /zapligar {html.escape(BOT)}")

def postar_no_whatsapp(p, chamada, palavra, caro):
    print(f"  WhatsApp: enviando para {len(destinos_whatsapp())} destino(s)...")
    link = link_rastreado(p, palavra, caro, "whatsapp")
    foto = foto_com_fundo(p["imageUrl"]) or baixar_imagem(p["imageUrl"])
    try:
        r = chamar_whatsapp("/enviar", {"destinos": destinos_whatsapp(),
                                        "texto": montar_texto(p, chamada, "whatsapp", link),
                                        "imagem": base64.b64encode(foto).decode() if foto else None})
    except Exception as e:
        pausar_whatsapp(f"o programa do WhatsApp não respondeu ({type(e).__name__})", queda=True)
        return False
    if not r.get("ok"):
        erros = r.get("erro") or "; ".join(x.get("erro", "") for x in r.get("resultados", []))
        # Desconectado / conexão fechada = queda passageira; o resto (ex.: chip saiu do grupo) espera você
        queda = bool(re.search(r"desconectado|connection closed|timed out|not open", erros or "", re.I))
        pausar_whatsapp(erros or "erro desconhecido", queda=queda)
        return False
    c = contagem_whatsapp()
    c["posts"] += 1
    c["ultimo"] = time.time()
    c["proximo"] = (random.uniform(WHATSAPP_INTERVALO, WHATSAPP_INTERVALO_MAX)
                    if WHATSAPP_INTERVALO_MAX > WHATSAPP_INTERVALO else None)
    with open(ARQUIVO_ZAP_CONTAGEM, "w", encoding="utf-8") as f:
        json.dump(c, f)
    falhas = [x for x in r.get("resultados", []) if not x.get("ok")]
    print(f"  WhatsApp: postado ({c['posts']}/{WHATSAPP_MAX_DIA} hoje)"
          + (f", falhou em {len(falhas)} destino(s)" if falhas else ""))
    return True

def conferir_modelo_ideal(p, palavra):
    # Última conferência antes de postar (modelo ideal: "Air Fryer Mondial de R$ 600 por R$ 389").
    # Devolve a lista do que está fora do padrão; vazia = pode postar.
    problemas = []
    marca = marca_do_produto(p)
    nome = p.get("nome_post") or ""
    if EXIGIR_MARCA_SEMPRE and not marca and not bem_avaliado_sem_marca(p) and not marca_opcional(palavra):
        problemas.append("sem marca conhecida")
    if marca and normalizar(marca) not in normalizar(nome):
        problemas.append("marca fora do nome")
    if float(p.get("priceDiscountRate") or 0) < DESCONTO_MINIMO:
        problemas.append("sem desconto")
    if not nota_boa(p):
        problemas.append("nota baixa")
    if not nome_valido(nome, palavra) or bloqueado(nome):
        problemas.append("nome ruim")
    if peca_de_outro(p["productName"], palavra):
        problemas.append("peça de outro aparelho")
    if float(p.get("price") or 0) <= 0:
        problemas.append("sem preço")
    return problemas

def carregar_ciclo():
    try:
        with open(ARQUIVO_CICLO, encoding="utf-8") as f:
            return set(l.strip() for l in f if l.strip())
    except FileNotFoundError:
        return set()

def salvar_ciclo(ciclo):
    # Grava num arquivo temporário e troca de uma vez: se o servidor cair no meio da gravação, o
    # rodízio antigo fica inteiro (antes um arquivo pela metade fazia o rodízio recomeçar do zero)
    temporario = ARQUIVO_CICLO + ".tmp"
    with open(temporario, "w", encoding="utf-8") as f:
        f.write("".join(p + "\n" for p in sorted(ciclo)))
        f.flush()
        os.fsync(f.fileno())
    os.replace(temporario, ARQUIVO_CICLO)

def tipo_do_produto(palavra):
    busca = normalizar(palavra)
    for t in sorted(map(normalizar, TIPOS_PROPRIOS), key=len, reverse=True):
        if busca.startswith(t):
            return t
    ts = termos(palavra) or [busca]
    tipo = " ".join(ts[:2]) if ts[0] in TIPOS_GENERICOS else ts[0]
    return SINONIMOS_TIPO.get(tipo, tipo)

# Rodízio por CATEGORIA (as "garagens" do Gabriel): cada busca é uma garagem ("smart tv 43",
# "smart tv 32"...) e as garagens parecidas formam uma categoria ("televisão"). Postou uma TV,
# a categoria televisão só volta depois que TODAS as outras categorias da lista tiveram a vez
# (postaram ou não acharam nada bom). Aí volta com outra garagem (outra TV). Quem não está
# aqui é categoria sozinha (o próprio tipo). A ordem importa: o 1º que bater vale.
ARQUIVO_CATEGORIAS = "categorias.txt"
CATEGORIAS = [
    ("cozinha: tapete", ["tapete silicone", "tapete seca"]),
    ("tapete", ["tapete", "capacho"]),
    ("cama e roupa de cama", ["cama", "colchao", "protetor colchao", "protetor travesseiro", "saia", "pillow",
                              "cabeceira", "beliche", "bicama", "recamier", "calcadeira", "dossel", "mosquiteiro",
                              "lencol", "edredom", "colcha", "cobre", "fronha", "cobertor", "manta", "travesseiro",
                              "organizador cobertor"]),
    ("televisão", ["smart", "tv", "televisao", "monitor"]),
    ("suporte e rack de tv", ["suporte tv", "suporte mesa", "rack", "painel"]),
    ("tv box", ["fire", "mi", "chromecast"]),
    ("som", ["home", "soundbar", "caixa som", "echo"]),
    ("mesa e sala de jantar", ["mesa jantar", "sala", "mesa cadeira", "cadeira jantar", "mesa sala", "bistro",
                               "mesa bistro", "mesa bar", "cadeira", "banqueta", "buffet", "cristaleira", "aparador"]),
    ("mesa de centro e lateral", ["mesa centro", "mesa canto", "mesa lateral", "mesa cabeceira", "criado"]),
    ("escritório", ["mesa escritorio", "mesa computador", "mesa notebook", "mesa regulavel", "escrivaninha",
                    "cadeira escritorio", "cadeira gamer", "gaveteiro", "suporte notebook", "arquivo"]),
    ("área externa", ["mesa jardim", "cadeira jardim", "cadeira area", "jardim", "cadeira piscina", "cadeira praia",
                      "mesa camping", "cadeira camping", "espreguicadeira", "ombrelone", "gazebo", "tenda", "rede",
                      "cadeira balanco"]),
    ("sofá e poltrona", ["sofa", "capa sofa", "poltrona", "puff", "cadeira massagem", "cadeira estofada",
                         "cadeira madeira", "cadeira dobravel"]),
    ("guarda-roupa e closet", ["guarda", "comoda", "sapateira", "arara", "cabideiro", "organizador closet",
                               "organizador guarda", "penteadeira"]),
    ("toalha de banho", ["toalha", "toalha banho", "toalha mao", "toalha rosto", "toalha piso", "roupao",
                         "toalha buddemeyer"]),
    ("mesa posta", ["toalha mesa", "caminho", "americano", "guardanapo", "sousplat", "porta guardanapo"]),
    ("cortina", ["cortina", "blackout", "persiana", "varao"]),
    ("panela", ["panela", "panela de pressao", "cacarola", "caldeirao", "frigideira", "wok", "leiteira",
                "cuscuzeira", "fondue"]),
    ("panela elétrica e air fryer", ["panela eletrica", "air", "fritadeira", "forno", "mini forno", "grill",
                                     "churrasqueira eletrica", "micro"]),
    ("louça", ["prato", "jantar", "aparelho", "sobremesa", "xicara", "caneca", "bowl", "tigela", "travessa",
               "refratario", "saladeira"]),
    ("copo e taça", ["copo", "taca", "jarra", "decanter", "suqueira"]),
    ("talheres e facas", ["talhere", "faqueiro", "faca", "bloco", "afiador", "amolador"]),
    ("triturador e picador", ["triturador", "picador", "mini triturador", "processador", "mini processador"]),
    ("mixer e batedor de leite", ["mixer", "batedor", "espumador", "mini batedor", "caneca mixer",
                                  "caneca magnetica", "caneca autoagitadora"]),
    ("café", ["cafeteira", "moedor cafe", "prensa", "coador", "suporte coador", "porta capsula", "suporte capsula"]),
    ("garrafa térmica", ["garrafa", "garrafao", "squeeze", "copo termico"]),
    ("geladeira e freezer", ["geladeira", "geladeira expositora", "freezer", "freezer horizontal", "frigobar",
                             "cervejeira", "adega"]),
    ("fogão e cooktop", ["fogao", "cooktop", "fogareiro", "coifa"]),
    ("lavar e secar roupa", ["maquina lavar", "lava seca", "tanquinho", "secadora", "mini lavadora"]),
    ("ar e ventilador", ["ar", "ventilador", "climatizador", "circulador"]),
    ("aspirador", ["aspirador", "robo"]),
    ("iluminação", ["luminaria", "abajur", "lustre", "pendente", "arandela", "lampada led", "refletor", "fita"]),
    ("natal e ano novo", ["arvore", "bola", "bolinha", "pisca", "cascata", "cordao", "guirlanda", "enfeite",
                          "decoracao", "balao", "porta bombom", "mini arvore"]),
    ("lixeira", ["lixeira", "cesto lixo"]),
    ("limpeza do chão", ["mop", "vassoura", "rodo", "esfregao", "balde", "pa", "pano chao"]),
    ("organizador", ["organizador", "caixa organizadora", "colmeia", "cesto organizador", "saco organizador"]),
    ("ferramentas", ["ferramenta", "soquete", "chave", "broca", "caixa ferramenta", "martelo", "alicate",
                     "furadeira", "parafusadeira", "esmerilhadeira", "lixadeira", "serra", "trena", "nivel"]),
    ("tempero e pote", ["porta tempero", "porta condimento", "organizador tempero", "pote", "prateleira giratoria",
                        "organizador giratorio", "marmita",
                        "porta mantimento", "dispenser cereai"]),
    ("facas na parede", ["suporte magnetico", "barra magnetica", "porta faca"]),
    ("lavanderia", ["dispenser sabao", "dispenser amaciante", "porta sabao", "organizador lavanderia",
                    "kit potes para lavanderia", "pote para sabao", "dosador"]),
    ("tábua", ["tabua carne", "tabua churrasco", "tabua corte", "tabua frio", "tabua madeira"]),
    ("chuveiro e ducha", ["chuveiro", "ducha higienica", "registro"]),
    ("prateleira de banheiro", ["prateleira", "porta shampoo", "porta xampu", "nicho"]),
    ("espelho", ["espelho"]),
    ("barba e pelos", ["aparador de barba", "aparador de pelos"]),   # senão o "aparador" (móvel) levava para mesa
    ("jardim", ["aparador de grama"]),
    ("filtro e purificador", ["filtro agua", "filtro barro", "filtro torneira", "purificador"]),
    ("tomada e extensão", ["filtro linha", "extensao", "regua", "adaptador", "benjamim", "estabilizador"]),
    ("churrasqueira", ["churrasqueira", "churrasqueira a gas", "churrasco", "espeto", "grelha", "escova aco",
                       "escova limpar"]),
]
CATEGORIAS = CATEGORIAS_EXTRA + CATEGORIAS   # as do bot (nicho.py) ganham das do Casa
CATEGORIAS_EM_ALTA = []   # 08/11: preenchida pelo que os outros grupos postam e a gente não buscava
EM_ALTA = []              # as buscas novas dessas categorias

def categoria_do_produto(palavra):
    # Nome exato do tipo ganha ("cadeira escritorio" -> escritório); depois o começo ("tapete sala" -> tapete)
    tipo = tipo_do_produto(palavra)
    for nome, tipos in CATEGORIAS_EM_ALTA + CATEGORIAS:   # as "em alta nos grupos" (aprendidas) primeiro
        if tipo in tipos:
            return nome
    for nome, tipos in CATEGORIAS:
        if any(tipo.startswith(t + " ") for t in tipos):
            return nome
    return tipo

def carregar_categorias():
    try:
        with open(ARQUIVO_CATEGORIAS, encoding="utf-8") as f:
            return set(l.strip() for l in f if l.strip())
    except FileNotFoundError:
        return set()

def salvar_categorias(categorias):
    temporario = ARQUIVO_CATEGORIAS + ".tmp"
    with open(temporario, "w", encoding="utf-8") as f:
        f.write("".join(c + "\n" for c in sorted(categorias)))
        f.flush()
        os.fsync(f.fileno())
    os.replace(temporario, ARQUIVO_CATEGORIAS)

def mesmo_tipo(palavra):
    # Todas as palavras (das duas listas) do mesmo tipo: "cooktop 4 bocas" leva junto "cooktop de indução"
    tipo = tipo_do_produto(palavra)
    return {p for p in SIMPLES + CAROS if tipo_do_produto(p) == tipo}

def loja_oficial(p):
    return 1 in (p.get("shopType") or [])

def loja_indicada(p):
    return bool({2, 4} & set(p.get("shopType") or []))

def bem_avaliado_sem_marca(p):
    # Sem marca conhecida, a garantia é a reputação: a mesma régua de todos (nota 4,7+ e 1000+ vendas)
    # De R$ 200 para cima a marca é obrigatória: sem marca nunca passa
    return not preco_caro(p) and nota_boa(p) and int(p.get("sales") or 0) >= VENDAS_MINIMAS

def degrau_loja(p):
    # REGRA ÚNICA (06/11, decisão final): qualquer loja passa com nota 4,7+ e 1000+ vendas (conferidas nos
    # filtros de nota e vendas). O degrau só decide a PREFERÊNCIA quando a busca acha várias:
    # 1 Oficial, 2 Indicada, 3 comum com marca conhecida, 4 comum sem marca. None = loja recusada.
    if p.get("loja") == "mercadolivre":
        return degrau_loja_ml(p)
    if loja_oficial(p):
        return 1
    if LOJA_INDICADA and loja_indicada(p):
        return 2
    if not LOJA_COMUM_MARCA:                   # /lojacomum desliga: só Oficial e Indicada
        return None
    return 3 if marca_do_produto(p) else 4

# (09/11, Gabriel, perfume do Mercado Livre) A escada de lojas: 1º a loja OFICIAL DA MARCA do perfume (Azzaro
# vendendo Azzaro); 2º as lojas grandes (o próprio Mercado Livre, Sephora, Amazon...); 3º outras lojas oficiais e
# as indicadas pelo Mercado Livre (MercadoLíder Platinum/Gold); 4º loja comum, só muito bem avaliada (reputação
# verde) e com muitas vendas. O resto fica de fora.
LOJAS_GRANDES_ML = ["Mercado Livre", "Sephora", "Amazon", "Época Cosméticos", "Beleza na Web", "The Beauty Box",
                    "O Boticário", "Boticário", "Natura", "Eudora", "Avon", "Drogasil", "Droga Raia", "Magalu",
                    "Magazine Luiza", "Americanas", "Carrefour", "Casas Bahia", "Netshoes", "Dafiti"]
VENDAS_LOJA_COMUM_ML = 5000   # loja comum: pelo menos +5 mil vendas (e reputação verde)

def vendedor_ml(p):
    if "_vendedor" not in p:
        try:
            s = sessao_ml()
            p["_vendedor"] = s.vendedor(p["_ml"])
            if p["_vendedor"] is None:
                print(f"  Aviso: não li a loja de {p['productName'][:40]}: {getattr(s, 'ultimo_problema', '?')}")
        except Exception as e:
            print(f"  Aviso: não consegui ver a loja de {p['productName'][:40]} ({type(e).__name__}: {str(e)[:80]}).")
            p["_vendedor"] = None
    return p["_vendedor"]

def degrau_loja_ml(p):
    v = vendedor_ml(p)
    if not v:
        return None
    nome = normalizar(v["nome"])
    marca = normalizar(marca_do_produto(p) or "")
    if v["oficial"] and marca and (marca in nome or nome in marca):
        return 1
    if any(re.search(r"(?<!\w)" + re.escape(normalizar(l)) + r"(?!\w)", nome) for l in LOJAS_GRANDES_ML):
        return 2
    if v["oficial"] or v["lider"] in ("platinum", "gold"):
        return 3
    # (o total de vendas da loja nem sempre vem: vale também o produto com muitas vendas)
    if v["reputacao"] == "5_green" and max(v["vendas"], int(p.get("sales") or 0)) >= VENDAS_LOJA_COMUM_ML:
        return 4
    return None

def selo_loja_ml(p):
    # A linha de confiança do post ("✅ Loja oficial Azzaro", "✅ MercadoLíder Platinum")
    v = p.get("_vendedor")
    if not v:
        return ""
    if v["oficial"]:
        return f"✅ Loja oficial {v['nome']}"
    if v["lider"] == "platinum":
        return f"✅ Vendido por {v['nome']} (MercadoLíder Platinum)"
    if v["lider"] == "gold":
        return f"✅ Vendido por {v['nome']} (MercadoLíder Gold)"
    mil = f"+{v['vendas'] // 1000} mil vendas" if v["vendas"] >= 1000 else ""
    return f"✅ Vendido por {v['nome']}" + (f" ({mil})" if mil else "")

def loja_aceita(p):
    return degrau_loja(p) is not None

# (08/11, Gabriel: "azeite de 50 por 30... tem que ser promoção") Tipo de mercado só vale com desconto grande:
# [(trechos da busca, desconto mínimo em %)]. O nicho.py preenche; vazio = vale o DESCONTO_MINIMO de sempre
DESCONTO_MINIMO_TIPO = DESCONTO_MINIMO_TIPO if "DESCONTO_MINIMO_TIPO" in globals() else []

def desconto_minimo(palavra):
    busca = normalizar(palavra or "")
    # a busca que COMEÇA com o trecho ("azeite gallo" sim; "porta azeite" não)
    return max([DESCONTO_MINIMO] + [m for trechos, m in DESCONTO_MINIMO_TIPO
                                    if any(busca.startswith(normalizar(t)) for t in trechos)])

def motivo_recusa(p, palavra, caro, minimo, postados, nomes_recentes):
    # O primeiro filtro em que o produto cai (None = passou em todos); o log mostra os mais comuns
    nome = p["productName"]
    if str(p["itemId"]) in postados or chave_nome(nome) in postados:
        return "já postado"
    if bloqueado(nome) or peca_de_outro(nome, palavra):
        return "bloqueado/peça"
    if not combina(nome, palavra):
        return "não combina com a busca"
    if any(parecido(nome, n) for n in nomes_recentes):
        return "parecido com post recente"
    if not nota_boa(p):
        return "nota baixa"
    if float(p.get("priceDiscountRate") or 0) < desconto_minimo(palavra):
        return "desconto baixo"
    if not comissao_boa(p):
        return "comissão baixa"
    if LOJA_OFICIAL_SEMPRE and not loja_aceita(p):
        return "loja sem reputação suficiente"
    # Abaixo de R$ 200: 1000+ vendas. De R$ 200 para cima: 100+ (caro vende menos), mas com marca
    if int(p.get("sales") or 0) < (VENDAS_MINIMAS_CARO if preco_caro(p) else minimo):
        return "poucas vendas"
    if preco_caro(p) and not marca_do_produto(p) and not marca_opcional(palavra):
        return "caro sem marca"
    if caro and float(p["price"]) < PRECO_MINIMO_CARO:
        return "barato demais para caro"
    if tv_cara(p, palavra):
        return "TV cara pelo tamanho"
    if variacao_preco(p) > VARIACAO_MAXIMA:
        return "preço isca (versões com preços muito diferentes)"
    return None

def eletrico(palavra):
    busca = normalizar(palavra)
    return any(re.search(r"(?<!\w)" + re.escape(normalizar(t)), busca) for t in ELETRICOS)

def voltagem(nome):
    # "Bivolt", "220V", "110V" ou "110V ou 220V" (anúncio com as duas opções); None se não diz
    n = normalizar(nome)
    if re.search(r"bi-?\s?volt", n):
        return "Bivolt"
    v220 = re.search(r"(?<!\d)220\s*v", n) or re.search(r"(?<!\d)(110|127)\s*v?\s*(/|e|ou|-)\s*220", n)
    v110 = re.search(r"(?<!\d)(110|127)\s*v", n)
    if v220 and v110:
        return "110V ou 220V"
    return "220V" if v220 else "110V" if v110 else None

def ordem_voltagem(p, palavra):
    # 0 bivolt, 1 tem 220V, 2 só 110V, 3 não diz (só sai se não tiver outro). Não elétrico: tudo 0
    if not eletrico(palavra):
        return 0
    return {"Bivolt": 0, "220V": 1, "110V ou 220V": 1, "110V": 2}.get(voltagem(p["productName"]), 3)

def _metros(valor, unidade):
    # "200" (cm) -> "2m", "190" -> "1,90m", "45" -> "45cm"
    numero = float(valor.replace(",", "."))
    cm = numero * 100 if unidade == "m" or (not unidade and numero < 10) else numero
    if cm < 100:
        return f"{cm:.0f}cm"
    m = f"{cm / 100:.0f}" if round(cm) % 100 == 0 else f"{cm / 100:.2f}".replace(".", ",")
    return f"{m}m"

def medida(nome, palavra):
    # Medida que o comprador quer ver: litros de geladeira, kg de lavar e o tamanho (móvel, cama,
    # escada, aparelho grande). Aparelho grande pode ter os dois: "416 Litros 70cm x 1,85m"
    busca = normalizar(palavra)
    partes = []
    if any(re.search(r"(?<!\w)" + re.escape(normalizar(t)), busca) for t in COM_CAPACIDADE):
        partes.append(capacidade(normalizar(nome)))
    if any(re.search(r"(?<!\w)" + re.escape(normalizar(t)), busca) for t in COM_MEDIDAS):
        partes.append(tamanho(normalizar(nome), busca))
    return " ".join(p for p in partes if p) or None

def capacidade(n):
    litros = re.search(r"(?<![\d,.])(\d{1,4}(?:[.,]\d)?)\s*(l|lt|lts|litros?)\b", n)
    if litros:
        return f"{litros.group(1)} Litros"
    kg = re.search(r"(?<![\d,.])(\d{1,2}(?:[.,]5)?)\s*kg\b", n)
    if kg:
        return f"{kg.group(1)}kg"
    garrafas = re.search(r"(?<!\d)(\d{1,3})\s*garrafas", n)
    if garrafas:
        return f"{garrafas.group(1)} Garrafas"
    return None

def tamanho(n, busca):
    if "escada" in busca:
        degraus = re.search(r"(?<!\d)(\d{1,2})\s*degraus", n)
        if degraus:
            return f"{degraus.group(1)} Degraus"
    num = r"(\d{1,3}(?:[.,]\d{1,2})?)\s*(?:(cm|m)(?![a-z]))?"   # o "m" de "Madesa" não é metro
    dims = re.search(num + r"\s*[x×]\s*" + num + r"(?:\s*[x×]\s*" + num + r")?", n)
    if dims:
        g = dims.groups()
        pares = [(g[i], g[i + 1]) for i in (0, 2, 4) if g[i]]
        unidade = next((u for _, u in pares if u), None)   # "200x190cm": o cm vale para os dois
        valores = [float(v.replace(",", ".")) for v, _ in pares]
        decimais = all(("," in v or "." in v) and 0.3 <= float(v.replace(",", ".")) <= 10 for v, _ in pares)
        if unidade or all(v >= 10 for v in valores) or decimais:   # "2x1" (kit) não é medida; "2,80 x 2,30" é (m)
            medidas = " x ".join(_metros(v, u or unidade) for v, u in pares)
            return _com_lugares(medidas, n, busca)
    # 06/11: uma medida só ("Mesa 1,60m", "Cortina 3 metros", "Rack 180cm") e lugares ("6 Lugares")
    unico = re.search(r"(?<![\d,.x×])(\d{1,3}(?:[.,]\d{1,2})?)\s*(cm|metros?|m)(?![a-z])", n)
    if unico:
        valor, unidade = unico.group(1), "m" if unico.group(2).startswith("m") else "cm"
        numero = float(valor.replace(",", "."))
        if (unidade == "m" and 0.3 <= numero <= 10) or (unidade == "cm" and numero >= 20):
            return _com_lugares(_metros(valor, unidade), n, busca)
    return _com_lugares(None, n, busca)

def _com_lugares(medidas, n, busca):
    # Mesa e sofá: "6 Lugares" diz o tamanho para quem compra (junto da medida, se tiver)
    lugares = (re.search(r"(?<!\d)(\d{1,2})\s*(?:lugares|cadeiras)", n)    # "com 6 Cadeiras" = 6 Lugares
               if re.search(r"\b(mesa|sofa|conjunto)\b", busca) else None)
    partes = [p for p in (medidas, f"{lugares.group(1)} Lugares" if lugares else None) if p]
    return " ".join(partes) or None

# Medida OBRIGATÓRIA (06/11, Gabriel: "sempre coloque medida em mesa, geladeira, fornos, freezer, cortina"):
# a busca que começa com um desses só posta anúncio que diz a medida/litros no título
MEDIDA_OBRIGATORIA = ["mesa", "geladeira", "freezer", "frigobar", "forno", "micro-ondas", "cortina", "persiana",
                      "guarda-roupa", "colchão", "cama", "sofá", "conjunto de sala de jantar", "conjunto sala de jantar"]

def exige_medida(palavra):
    b = normalizar(palavra)
    return any(b.startswith(normalizar(t)) for t in MEDIDA_OBRIGATORIA)

UNIDADES_PACOTE = {"unidades": "Unidades", "unidade": "Unidades", "unid": "Unidades", "und": "Unidades",
                   "un": "Unidades", "lencos": "Unidades", "fraldas": "Unidades", "pecas": "Peças",
                   "pcs": "Peças", "rolos": "Rolos", "folhas": "Folhas", "capsulas": "Cápsulas",
                   "saquinhos": "Unidades", "sacos": "Unidades", "toalhas": "Unidades", "pares": "Pares"}

def quantidade(nome):
    # Produto em pacote/kit: "Lenço Umedecido Pampers 592 Unidades" (o comprador quer saber quanto vem).
    # Pega o MAIOR "número + unidade" do título (o total, não o de cada pacote)
    achados = []
    for n, u in re.findall(r"(\d+(?:\.\d{3})*)\s*(unidades|unidade|unid|und|un|len[çc]os|fraldas|pe[çc]as|"
                           r"p[çc]s|rolos|folhas|c[áa]psulas|saquinhos|sacos|toalhas|pares)\b", nome, re.I):
        qtd = int(n.replace(".", ""))
        if qtd >= 2:
            achados.append((qtd, UNIDADES_PACOTE[normalizar(u)]))
    # Vários pacotes: "4 pacotes de 148", "148 lenços cada - 4 pacotes", "4x148 unidades" -> 592
    texto = normalizar(nome)
    for a, b in (re.findall(r"(\d+)\s*pacotes?\s*(?:de|com|c/)\s*(\d+)", texto)
                 + [(y, x) for x, y in re.findall(r"(\d+)\s*(?:unidades|un|lencos|fraldas)?\s*cada\D{0,20}?(\d+)\s*pacotes?", texto)]
                 + re.findall(r"\b(\d{1,2})\s*x\s*(\d{2,4})\s*(?:unidades|un|lencos|fraldas)\b", texto)):
        if 2 <= int(a) <= 50 and int(b) >= 2:
            achados.append((int(a) * int(b), "Unidades"))
    if not achados:
        return None
    qtd, u = max(achados)
    return f"{qtd} {u}"

# (07/11) Eletrônico sem o modelo não vende: "Celular Xiaomi Redmi Note" (era Note 14 Pro 5G 256GB)
PRECISA_MODELO = ["celular", "smartphone", "iphone", "galaxy", "redmi", "xiaomi", "poco", "motorola", "moto g",
                  "moto e", "realme", "notebook", "macbook", "tablet", "ipad", "kindle", "smartwatch",
                  "apple watch", "galaxy watch", "amazfit", "mi band", "airpods", "galaxy buds", "fone",
                  "headphone", "jbl", "playstation", "xbox", "nintendo", "console", "monitor", "processador"]
MODELO_PALAVRAS = {"pro", "max", "plus", "ultra", "lite", "mini", "fe", "neo", "5g", "4g", "edge", "prime",
                   "power", "play", "air", "se", "oled", "turbo", "fusion", "slim"}

def com_modelo(nome, original, palavra):
    # Põe de volta o modelo que o limpador/IA tirou: depois da palavra do nome que vem por último no título,
    # junta o que vem a seguir no título enquanto for modelo ("14", "Pro", "5G", "A56", "i5") e para no
    # armazenamento ("256GB" entra e encerra). Só para eletrônico (PRECISA_MODELO).
    alvo = normalizar(f"{palavra} {original}")
    if not any(re.search(r"(?<!\w)" + re.escape(t) + r"(?!\w)", alvo) for t in PRECISA_MODELO):
        return nome
    tit = original.split()
    tit_n = [normalizar(w).strip(".,;:()[]") for w in tit]
    pal = nome.split()
    posicoes = [(max((i for i, t in enumerate(tit_n) if t == normalizar(w).strip(".,;:")), default=-1), k)
                for k, w in enumerate(pal)]
    fim, k = max(posicoes)
    if fim < 0:
        return nome
    ja = set(normalizar(nome).split())
    extra = []
    for w, b in zip(tit[fim + 1:fim + 7], tit_n[fim + 1:fim + 7]):
        if not b or b in ja:
            break
        if re.fullmatch(r"\d+\s*(gb|tb)", b):
            extra.append(b.upper())                       # "256gb" -> "256GB" e para aqui (o resto é RAM...)
            break
        if any(c.isdigit() for c in b) or b in MODELO_PALAVRAS:
            extra.append(w.strip(".,;:()[]") if not b.isalpha() else w[:1].upper() + w[1:].lower())
        else:
            break
    if not extra:
        return nome
    return " ".join(pal[:k + 1] + extra + pal[k + 1:])

# (08/11, Gabriel: "coloca nome nas coisas... se tem unidade, onde dá para colocar metros, a medida você coloca")
# A especificação que o comprador procura, tirada do título: (trechos da busca/título, [(regex, formato)])
_NUM = r"(?<![\d,.])"
ESPECIFICACOES = [
    (["cabo", "extensor usb", "fita led", "mangueira", "cordão de luz", "pisca pisca", "varal de luz"],
     [(_NUM + r"(\d{1,2}(?:[.,]\d)?)\s*(?:m|mt|mts|metros?)(?![a-z])", "{} Metros")]),
    (["carregador", "fonte", "power bank", "cabo", "hub usb", "carregador por indução"],
     [(_NUM + r"(\d{2,3})\s*w(?![a-z])", "{}W")]),
    (["power bank", "bateria portátil", "carregador portátil"],
     [(_NUM + r"(\d{1,2}[.]?\d{3})\s*mah", "{}mAh")]),
    (["pen drive", "cartão de memória", "ssd", "hd externo", "memória ram"],
     [(_NUM + r"(\d{1,4})\s*(gb|tb)(?![a-z])", "{}{}")]),
    (["whey", "creatina", "pré treino", "pre treino", "hipercalórico", "bcaa", "glutamina", "pasta de amendoim",
      "colágeno", "beta alanina"],
     [(_NUM + r"(\d(?:[.,]\d{1,2})?)\s*kg(?![a-z])", "{}kg"), (_NUM + r"(\d{2,4})\s*g(?![a-z])", "{}g")]),
    (["perfume", "body splash", "colônia", "deo colônia", "eau de", "parfum", "deo parfum"],
     [(_NUM + r"(\d{2,3})\s*ml(?![a-z])", "{}ml")]),
    # 08/11: azeite e limpeza em galão ("Detergente Ypê 5 Litros", "Azeite Gallo 500ml")
    (["azeite", "vinagre", "detergente", "sabão líquido", "amaciante", "desinfetante", "lava roupas"],
     [(_NUM + r"(\d{1,2}(?:[.,]\d)?)\s*(?:l|lt|lts|litros?)(?![a-z])", "{} Litros"),
      (_NUM + r"(\d{3,4})\s*ml(?![a-z])", "{}ml")]),
]

def especificacoes(p, palavra, nome=""):
    alvo = normalizar(f"{palavra} {p['productName']}")
    titulo = normalizar(p["productName"])
    saida = []
    for trechos, regras in ESPECIFICACOES:
        if not any(re.search(r"(?<!\w)" + re.escape(normalizar(t)), alvo) for t in trechos):
            continue
        if any(re.search(regra, normalizar(nome)) for regra, _ in regras):
            continue                                   # o nome já diz ("2m", "20W", "1kg")
        for regra, formato in regras:
            m = re.search(regra, titulo)
            if m:
                g = [x.upper() if x in ("gb", "tb") else x for x in m.groups()]
                texto = formato.format(*g)
                if texto not in saida:
                    saida.append(texto)
                break                                  # kg OU g, não os dois
    return saida

def completar_nome(p, palavra):
    # "Geladeira Brastemp Inox" -> "Geladeira Brastemp Inox 416 Litros 220V"
    # "Lenço Umedecido Pampers" -> "Lenço Umedecido Pampers 592 Unidades"
    # "Cabo USB-C Baseus" -> "Cabo USB-C Baseus 2 Metros 100W" | "Creatina Growth" -> "Creatina Growth 250g"
    nome = com_modelo(p["nome_post"], p["productName"], palavra)
    extras = [medida(p["productName"], palavra)]
    qtd = quantidade(p["productName"])
    if qtd and not re.search(r"\d+\s*(?:unidades|pe[çc]as|rolos|folhas|c[áa]psulas|pares|un)\b", nome, re.I):
        extras.append(qtd)
    if eletrico(palavra):
        extras.append(voltagem(p["productName"]))
    for extra in extras:
        if not extra or normalizar(extra).replace(" ", "") in normalizar(nome).replace(" ", ""):
            continue
        litros = re.match(r"([\d.,]+) Litros$", extra)     # "4L" já no nome = "4 Litros" (não repete)
        if litros and re.search(r"(?<![\d,.])" + re.escape(litros.group(1)) + r"\s*(l|lt|lts|litros?)\b", normalizar(nome)):
            continue
        nome = f"{nome} {extra}"
    for extra in especificacoes(p, palavra, nome):     # metros, W, mAh, GB, g/kg, ml (só o que o nome não diz)
        nome = f"{nome} {extra}"
    return com_algodao(nome, p["productName"])

# (09/11, Gabriel: "sempre informa se é 100% algodão... cueca, calcinha, toalha, jogo de cama, travesseiro.
# Poliamida não. O que não for, você não informa"). Só quando o TÍTULO da Shopee diz 100% algodão / puro algodão
_ALGODAO_100 = re.compile(r"100\s*%\s*(?:de\s+)?algod[aã]o|algod[aã]o\s*100\s*%|puro\s+algod[aã]o|algod[aã]o\s+puro", re.I)
_OUTROS_TECIDOS = re.compile(r"\s*(?:\b(?:de|em|com)\s+)?\b(?:poliamida|poli[eé]ster|elastano)\b", re.I)

def com_algodao(nome, titulo):
    nome = _OUTROS_TECIDOS.sub("", nome).strip()          # tecido sintético não vai no nome
    if not _ALGODAO_100.search(titulo or "") or _ALGODAO_100.search(nome):
        return nome
    # "Cueca Lupo Algodão" -> "Cueca Lupo 100% Algodão"; sem "algodão" no nome, vai no fim
    trocado = re.sub(r"\b(?:de\s+|em\s+)?algod[aã]o\b", "100% Algodão", nome, count=1, flags=re.I)
    return trocado if trocado != nome else f"{nome} 100% Algodão"

def publicar(escolhido, palavra, caro):
    # Manda o produto já escolhido (busca normal ou destaque do painel) e registra. Devolve True se saiu.
    chamada = escolher_chamada(escolhido, palavra, caro)
    # WhatsApp é o foco: quando é a vez dele, sai lá PRIMEIRO, depois no Telegram
    motivo_zap = motivo_sem_whatsapp()
    enviou_whatsapp = False
    if motivo_zap:
        print(f"  WhatsApp: não vai neste post ({motivo_zap}).")
    else:
        enviou_whatsapp = postar_no_whatsapp(escolhido, chamada, palavra, caro)
        if enviou_whatsapp:
            # Grava JÁ que postou: se o bot cair logo depois, ao voltar ele não manda o mesmo produto
            salvar_postado(escolhido["itemId"])
    if TELEGRAM_POSTAR:
        link = link_rastreado(escolhido, palavra, caro, "telegram")
        deu_certo = postar_no_telegram(escolhido, montar_texto(escolhido, chamada, "telegram", link))
    else:
        # só o WhatsApp: vale como postado se o WhatsApp mandou (o texto de volta diz se foi)
        link = link_rastreado(escolhido, palavra, caro, "whatsapp")
        deu_certo = enviou_whatsapp
        print("  Telegram: pausado (só o WhatsApp recebe). Para voltar: /telegramligar")
    if deu_certo:
        if not enviou_whatsapp:            # (se foi no WhatsApp, já gravou logo depois de enviar)
            salvar_postado(escolhido["itemId"])
        salvar_historico(palavra, escolhido["productName"])
        salvar_item_postado(escolhido["itemId"], palavra)   # para saber de qual busca veio a venda
        registrar_no_obsidian(escolhido, palavra, caro, link)
        comissao = float(escolhido.get("commissionRate") or 0) * 100
        comissao_rs = preco_br(valor_comissao(escolhido))
        modo = "silencioso" if horario_silencioso() else "com notificação"
        tipo = "CARO" if caro else "simples"
        extra = comissao_extra(escolhido) * 100
        print(f"  Postado ({tipo}, {palavra}, {modo}): {escolhido['nome_post']} | comissão {comissao:.0f}% (R$ {comissao_rs})"
              + (f" | COMISSÃO EXTRA da loja {extra:.0f}%" if extra else ""))
        salvar_status(escolhido["nome_post"])
        contar_post_e_mandar_extras()      # mensagem dos grupos (a cada 15) e alerta de cupom
    else:
        print("  Não deu para postar agora; tenta de novo na próxima rodada.")
    return deu_certo

# ---------- Destaques: produto exato colado no painel (/destaque LINK) ----------
# Campanhas do canal oficial da Shopee (ex.: Brastemp com 15% de comissão) vêm com o link do anúncio. O
# painel grava itemId/shopId em destaques.txt e o bot posta esse anúncio na próxima vez, antes da busca normal.
# Não passa pelos filtros de nota/vendas/loja (quem escolheu foi o Gabriel); só não repete o que já saiu.
ARQUIVO_DESTAQUES = "destaques.txt"   # uma linha por produto: itemId<TAB>shopId<TAB>link

def ler_destaques():
    try:
        with open(ARQUIVO_DESTAQUES, encoding="utf-8") as f:
            return [l.rstrip("\n").split("\t") for l in f if l.count("\t") >= 2]
    except FileNotFoundError:
        return []

def tirar_destaque(item_id):
    restantes = [d for d in ler_destaques() if d[0] != str(item_id)]
    with open(ARQUIVO_DESTAQUES, "w", encoding="utf-8") as f:
        f.write("".join("\t".join(d) + "\n" for d in restantes))

def buscar_por_item(item_id, shop_id):
    _, extras_campos = NIVEIS_BUSCA[nivel_busca]
    consulta = ('{ productOfferV2(itemId: %d, shopId: %d, limit: 1) { nodes { itemId productName price imageUrl '
                'offerLink sales ratingStar commissionRate priceDiscountRate%s } } }') % (
                int(item_id), int(shop_id), extras_campos)
    return chamar_shopee(consulta)["productOfferV2"]["nodes"]

def postar_destaque():
    # Devolve True se tentou postar um destaque (o bot não faz a busca normal nesta rodada)
    postados = carregar_postados()
    for item_id, shop_id, link in ler_destaques():
        if item_id in postados:
            tirar_destaque(item_id)
            continue
        try:
            nodes = buscar_por_item(item_id, shop_id)
        except (ErroLimite, ErroTemporario):
            print("  Destaque: a Shopee não respondeu agora; tento na próxima rodada.")
            return False
        except Exception as e:
            print(f"  Destaque {item_id}: a Shopee recusou ({e}).")
            nodes = []
        if not nodes:
            tirar_destaque(item_id)
            avisar_painel(f"⚠️ <b>{html.escape(BOT)}</b>: não achei na Shopee o destaque {html.escape(link)} "
                          "(anúncio fora do ar ou sem programa de afiliados). Tirei da fila.")
            continue
        p = nodes[0]
        nome = nome_curto(p["productName"]) or " ".join(p["productName"].split()[:8])
        p["nome_post"] = nome
        revisao = revisar_com_ia(p, nome)     # só para o nome ficar bonito; o produto foi escolhido a dedo
        if revisao and revisao.get("nome"):
            p["nome_post"] = revisao["nome"]
        if revisao:
            p["chamada_ia"], p["beneficio"] = revisao.get("chamada"), revisao.get("beneficio")
        p["nome_post"] = completar_nome(p, p["nome_post"])
        caro = float(p.get("price") or 0) >= PRECO_REGRA_CARO
        print(f"  Destaque do painel: {p['nome_post']}")
        if publicar(p, p["nome_post"], caro):
            tirar_destaque(item_id)
        return True
    return False

# ---------- Ofertas copiadas dos concorrentes (06/11) ----------
# O programa do WhatsApp guarda o que os canais observados (whatsapp/leituras.json) e os grupos dos outros
# afiliados (whatsapp/grupos_observados.json) postam. Daqui sai o link da Shopee de cada oferta: o bot abre o link,
# acha o produto (itemId/shopId) e busca ele na Shopee com o NOSSO link de afiliado (o deles nunca vai no post).
# Passa pelos filtros de segurança (peça, nota, desconto, comissão, preço único, TV cara, medida, marca no caro,
# revisão da IA). O Casa pega o que é de casa; o Geral pega o resto. No máximo 1 copiada a cada COPIADOS_A_CADA.
PASTA_WHATSAPP = os.path.join(PASTA_PRINCIPAL, "whatsapp")
ARQUIVO_COPIADOS_VISTOS = "copiados_vistos.txt"     # links já analisados por este bot (não abre de novo)
ARQUIVO_ULTIMO_COPIADO = "ultimo_copiado.txt"       # tamanho do histórico quando saiu a última copiada

def _ler_json(caminho):
    try:
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}

def links_dos_concorrentes(horas=None):
    # [(quando, link, origem)] dos links da Shopee postados pelos observados, do mais novo para o mais velho
    desde = time.time() - (horas or COPIADOS_HORAS) * 3600
    achados = []
    for jid, c in _ler_json(os.path.join(PASTA_WHATSAPP, "leituras.json")).items():
        for m in (c.get("ao_vivo") or []) + (c.get("mensagens") or []):
            if (m.get("quando") or 0) >= desde:
                achados += [(m["quando"], l, c.get("nome") or jid) for l in re.findall(r"https?://\S+", m.get("texto") or "")]
    # 08/11, Gabriel: "repetir o que eles fazem... aqui ele tá mandando mais, aqui pode vender mais".
    # Engajamento de cada post: reações + 3 por grupo a mais que postou o mesmo produto (mesmo título)
    posts_grupos = []
    for jid, g in _ler_json(os.path.join(PASTA_WHATSAPP, "grupos_observados.json")).items():
        for p in g.get("posts") or []:
            if (p.get("quando") or 0) >= desde:
                posts_grupos.append((p, g.get("nome") or jid))
    grupos_do_titulo = {}
    for p, origem in posts_grupos:
        grupos_do_titulo.setdefault(_chave_titulo(p.get("texto")), set()).add(origem)
    pontos = {}
    for p, origem in posts_grupos:
        mais = len(grupos_do_titulo.get(_chave_titulo(p.get("texto")), ())) - 1
        for l in p.get("links") or []:
            achados.append((p["quando"], l, origem))
            pontos[l] = max(pontos.get(l, 0), len(p.get("reacoes") or {}) + 3 * max(0, mais))
    vistos, saida = set(), []
    # O que mais engaja primeiro; empate (canais não têm reação): o mais novo
    for quando, link, origem in sorted(achados, key=lambda a: (-pontos.get(a[1], 0), -a[0])):
        ponto = pontos.get(link, 0)
        link = link.rstrip(".,;)*_~")
        _pontos_links[link] = max(_pontos_links.get(link, 0), ponto)
        if re.search(r"shopee\.com\.br|shope\.ee", link) and link not in vistos:
            vistos.add(link)
            saida.append((quando, link, origem))
    return saida

def _chave_titulo(texto):
    # As 5 primeiras palavras do nome do produto no post (para achar o mesmo produto em grupos diferentes)
    try:
        import concorrentes
        t = concorrentes.titulo(texto or "")
    except Exception:
        t = (texto or "").split("\n")[0]
    return " ".join(re.findall(r"[a-z]{3,}", normalizar(t))[:5])

def ids_do_link(link):
    # (shopId, itemId) de shopee.com.br/product/LOJA/ITEM, ...-i.LOJA.ITEM ou link curto (abre e vê aonde leva)
    for tentativa in range(2):
        m = (re.search(r"/product/(\d+)/(\d+)", link) or re.search(r"-i\.(\d+)\.(\d+)", link)
             or re.search(r"shopee\.com\.br/[^/?\s]+/(\d+)/(\d+)", link))
        if m:
            return m.group(1), m.group(2)
        if tentativa == 0 and re.search(r"(s\.shopee\.com\.br|shope\.ee)/", link):
            try:
                req = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=20) as resp:
                    link = urllib.parse.unquote(resp.geturl())
            except Exception:
                return None
    return None

_tipos_casa = None
def eh_de_casa(nome):
    global _tipos_casa
    if _tipos_casa is None:
        _tipos_casa = {tipo_do_produto(p) for p in PALAVRAS_DO_CASA}
    return tipo_do_produto(nome) in _tipos_casa

def deste_bot(nome):
    # O Casa fica com o que é de casa; o Geral (e qualquer outro bot) com o resto: o mesmo produto não sai nos 2
    return eh_de_casa(nome) if BOT == "casa" else not eh_de_casa(nome)

def motivo_copiado(p, postados, nomes_recentes):
    nome = p["productName"]
    if str(p["itemId"]) in postados or chave_nome(nome) in postados:
        return "já postado"
    if not deste_bot(nome):
        return "é do outro grupo"
    if bloqueado(nome):
        return "bloqueado/peça"
    if any(parecido(nome, n) for n in nomes_recentes):
        return "parecido com post recente"
    if not nota_boa(p):
        return "nota baixa"
    if float(p.get("priceDiscountRate") or 0) < DESCONTO_MINIMO:
        return "desconto baixo"
    if not comissao_boa(p):
        return "comissão baixa"
    if int(p.get("sales") or 0) < COPIADOS_VENDAS_MINIMAS:
        return "poucas vendas"
    if preco_caro(p) and not marca_do_produto(p):
        return "caro sem marca"
    if variacao_preco(p) > VARIACAO_MAXIMA:
        return "preço isca (versões com preços muito diferentes)"
    if tv_cara(p, nome):
        return "TV cara pelo tamanho"
    if exige_medida(nome) and not medida(nome, nome):
        return "sem medida"
    return None

def vez_do_copiado():
    try:
        with open(ARQUIVO_ULTIMO_COPIADO, encoding="utf-8") as f:
            ultimo = int(f.read().strip() or 0)
    except (OSError, ValueError):
        return True
    return len(carregar_historico(10 ** 6)) - ultimo >= COPIADOS_A_CADA - 1

_copiados_esperando = {}   # link -> produto que esperou o lado da vez (♀/♂)
_pontos_links = {}         # link -> engajamento (reações + grupos)
ARQUIVO_PRODUTOS_CONCORRENTES = "produtos_concorrentes.json"   # nome REAL na Shopee de cada link aberto

def anotar_produto_concorrente(link, p, origem):
    # 08/11: o texto do post dos outros tem propaganda ("absurdo", "cupom no Mercado Livre", "inspirado no..."),
    # então as buscas novas saem do nome do produto na Shopee, que o bot descobre aqui ao abrir o link
    dados = _ler_json(ARQUIVO_PRODUTOS_CONCORRENTES)
    limite = time.time() - 7 * 86400
    dados = {l: d for l, d in dados.items() if d.get("quando", 0) >= limite}
    dados[link] = {"nome": p["productName"], "quando": time.time(), "origem": origem,
                   "pontos": _pontos_links.get(link, 0)}
    try:
        with open(ARQUIVO_PRODUTOS_CONCORRENTES, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False)
    except OSError:
        pass

def postar_copiado():
    # Devolve True se postou uma oferta copiada (aí a busca normal fica para a próxima rodada)
    if not COPIAR_OFERTAS or not vez_do_copiado():
        return False
    try:
        with open(ARQUIVO_COPIADOS_VISTOS, encoding="utf-8") as f:
            vistos = set(l.strip() for l in f if l.strip())
    except OSError:
        vistos = set()
    # (os que esperam o lado da vez ficam guardados e não gastam consulta de novo)
    todos = [(q, l, o) for q, l, o in links_dos_concorrentes() if l not in vistos]
    for l in set(_copiados_esperando) - {l for _, l, _ in todos}:
        del _copiados_esperando[l]                 # passou das 6 h: esquece
    novos = ([x for x in todos if x[1] in _copiados_esperando]
             + [x for x in todos if x[1] not in _copiados_esperando][:COPIADOS_POR_RODADA])
    if not novos:
        return False
    postados = carregar_postados() | nomes_ja_postados()
    historico = carregar_historico()
    nomes_recentes = [n for _, n in historico]
    quer_fem = (not categoria_do_produto(historico[-1][0]).startswith("♀")) if ALTERNAR_FEMININO and historico else None
    motivos = Counter()
    try:
        for _, link, origem in novos:
            vistos.add(link)
            p = _copiados_esperando.pop(link, None)
            if p is None:
                ids = ids_do_link(link)
                if not ids:
                    motivos["link não abriu"] += 1
                    continue
                try:
                    nodes = buscar_por_item(ids[1], ids[0])
                except (ErroLimite, ErroTemporario):
                    vistos.discard(link)           # a Shopee não respondeu agora: tenta de novo depois
                    break
                except Exception:
                    nodes = []
                if not nodes:
                    motivos["sem afiliado"] += 1
                    continue
                p = nodes[0]
                anotar_produto_concorrente(link, p, origem)
            motivo = motivo_copiado(p, postados, nomes_recentes)
            if motivo:
                motivos[motivo] += 1
                continue
            # 08/11: a copiada também respeita "um feminino, um masculino" (antes pulava a alternância e o
            # Geral enchia de coisa feminina dos outros grupos). Do outro lado: espera a vez dela (até 6 h)
            if quer_fem is not None and categoria_do_produto(p["productName"]).startswith("♀") != quer_fem:
                vistos.discard(link)
                _copiados_esperando[link] = p
                motivos["espera o lado da vez (♀/♂)"] += 1
                continue
            p["nome_post"] = nome_curto(p["productName"]) or " ".join(p["productName"].split()[:8])
            palavra = p["nome_post"]
            revisao = revisar_com_ia(p, palavra)
            if revisao and not revisao["aprovado"]:
                motivos["IA recusou"] += 1
                continue
            if revisao and revisao.get("nome"):
                p["nome_post"] = revisao["nome"]
            if revisao:
                p["chamada_ia"], p["beneficio"] = revisao.get("chamada"), revisao.get("beneficio")
            if conferir_modelo_ideal(p, palavra):
                motivos["fora do modelo ideal"] += 1
                continue
            p["nome_post"] = completar_nome(p, palavra)
            print(f"  Oferta copiada de {origem}: {p['nome_post']} (R$ {preco_br(p['price'])})")
            if publicar(p, palavra, preco_caro(p)):
                with open(ARQUIVO_ULTIMO_COPIADO, "w", encoding="utf-8") as f:
                    f.write(str(len(carregar_historico(10 ** 6))))
                return True
            return False
    finally:
        with open(ARQUIVO_COPIADOS_VISTOS, "w", encoding="utf-8") as f:
            f.write("".join(l + "\n" for l in list(vistos)[-5000:]))
    if motivos:
        print("  Copiadas: nenhuma passou (" + ", ".join(f"{m} {n}" for m, n in motivos.most_common()) + ")")
    return False

# ---------- Modo campanha (06/11, Gabriel: "pode começar") ----------
# Nos dias das grandes campanhas da Shopee o pessoal compra muito mais (cupom e frete grátis para todo lado).
# No DIA: 30% mais posts no WhatsApp, caro a cada 2-3 posts, alerta de cupom a cada 10-15, selo da campanha em
# cima de cada post e a mensagem dos grupos com "HOJE É ...". Na VÉSPERA (esquenta): a mensagem dos grupos avisa
# "AMANHÃ É ...". Nos dois casos a mensagem dos grupos sai 1 vez logo no começo do dia.
# Painel: /campanha casa (mostra) | /campanha casa 11.11 (liga agora, para testar) | desligada | auto
CAMPANHA_RITMO = 1.3                    # posts do dia x 1,3 (90 -> 117)
CAMPANHA_PESO_DESCONTO = 2              # 08/11: no dia, o desconto pesa 2x na escolha do produto
CAMPANHA_DESCONTO_MINIMO = 20           # 08/11: no dia, só posta com 20%+ de desconto (se a busca não tiver, vale o normal)
ARQUIVO_CAMPANHA = "campanha"           # o painel escreve: nome (liga à força) ou "desligada"; sem arquivo = datas
ARQUIVO_CAMPANHA_AVISO = "campanha_avisada.txt"
estado_campanha = {"nome": None, "fase": None}

def campanhas_do_ano(ano):
    # (nome, primeiro dia, último dia). Black Friday = a sexta depois da 4ª quinta de novembro, até a segunda
    primeiro_nov = date(ano, 11, 1)
    quinta = primeiro_nov + timedelta(days=(3 - primeiro_nov.weekday()) % 7 + 21)
    sexta = quinta + timedelta(days=1)
    return [("11.11", date(ano, 11, 11), date(ano, 11, 11)),
            ("BLACK FRIDAY", sexta, sexta + timedelta(days=3)),
            ("12.12", date(ano, 12, 12), date(ano, 12, 12))]

def campanha_de_hoje(hoje=None):
    try:
        with open(ARQUIVO_CAMPANHA, encoding="utf-8") as f:
            forcada = f.read().strip()
    except OSError:
        forcada = ""
    if forcada.lower() == "desligada":
        return None, None
    if forcada:
        return forcada.upper(), "dia"
    hoje = hoje or datetime.now().date()
    for nome, inicio, fim in campanhas_do_ano(hoje.year):
        if inicio <= hoje <= fim:
            return nome, "dia"
        if hoje == inicio - timedelta(days=1):
            return nome, "esquenta"
    return None, None

def aplicar_campanha():
    nome, fase = campanha_de_hoje()
    estado_campanha.update(nome=nome, fase=fase)
    if fase == "dia":
        g = globals()
        if g["WHATSAPP_MAX_DIA"] < 999:                  # 999 = modo teste, sem limite: não mexe
            g["WHATSAPP_MAX_DIA"] = int(round(g["WHATSAPP_MAX_DIA"] * CAMPANHA_RITMO))
        g.update(CARO_A_CADA_MIN=2, CARO_A_CADA_MAX=3, CARO_PICO_MIN=2, CARO_PICO_MAX=2, CUPONS_MIN=10, CUPONS_MAX=15)
    agora = datetime.now()
    if fase and HORA_INICIO <= agora.hour < HORA_FIM:
        chave = f"{agora:%Y-%m-%d} {fase} {nome}"
        try:
            with open(ARQUIVO_CAMPANHA_AVISO, encoding="utf-8") as f:
                avisado = f.read().strip()
        except OSError:
            avisado = ""
        if avisado != chave:                             # 1ª vez no dia: a mensagem dos grupos sai já
            with open(ARQUIVO_CAMPANHA_AVISO, "w", encoding="utf-8") as f:
                f.write(chave)
            open(ARQUIVO_MANDAR_GRUPOS, "w").close()
            print(f"  Campanha {nome} ({'hoje' if fase == 'dia' else 'amanhã'}): mensagem dos grupos agendada.")

def linha_campanha():
    nome, fase = estado_campanha["nome"], estado_campanha["fase"]
    if fase == "dia":
        return f"🔥 HOJE É {nome} NA SHOPEE! Cupom e frete grátis o dia todo: as melhores ofertas vão sair aqui."
    if fase == "esquenta":
        return f"⏰ AMANHÃ É {nome} NA SHOPEE! Ativa as notificações do grupo: as ofertas começam cedo."
    return None

# ---------- Aprende com as vendas (08/11, Gabriel: "pode fazer tudo") ----------
# Lê o relatório de vendas de afiliado da Shopee (os últimos 30 dias; a Shopee atualiza o dia anterior ~10h30),
# liga cada venda ao post que o bot fez (pelo itemId ou pelo nome no historico.txt) e dá mais vez no rodízio
# para a categoria que vendeu: 1 ou 2 unidades = peso 2, 3+ = peso 3 (nunca baixa o peso que já tinha).
# Venda de link que não saiu deste bot (ex.: a tia mandou o link dela) não conta. Se a Shopee não deixar ler o
# relatório, o bot segue igual e usa o que aprendeu da última vez (vendas_aprendidas.json).
ARQUIVO_VENDAS = "vendas_aprendidas.json"
VENDAS_DIAS = 30
PESO_BASE = dict(PESO_CATEGORIA)        # o peso que o nicho deu, antes de aprender

def consultar_vendas(inicio, fim, campo_qtd=" qty"):
    itens, scroll = [], ""
    for _ in range(20):                                   # 20 páginas de 500 é muito mais que o necessário
        consulta = ('{ conversionReport(purchaseTimeStart: %d, purchaseTimeEnd: %d, limit: 500%s) { nodes { '
                    'orders { items { itemId itemName%s } } } pageInfo { hasNextPage scrollId } } }') % (
                        inicio, fim, f', scrollId: "{scroll}"' if scroll else "", campo_qtd)
        relatorio = chamar_shopee(consulta)["conversionReport"]
        for venda in relatorio.get("nodes") or []:
            for pedido in venda.get("orders") or []:
                itens.extend(pedido.get("items") or [])
        pagina = relatorio.get("pageInfo") or {}
        if not pagina.get("hasNextPage") or not pagina.get("scrollId"):
            break
        scroll = pagina["scrollId"]
        time.sleep(PAUSA_ENTRE_BUSCAS)
    return itens

def ler_vendas_salvas():
    try:
        with open(ARQUIVO_VENDAS, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}

def aplicar_aprendido():
    # Peso final = o do nicho, mais vez para o que está em alta nos outros grupos (2) e para o que vendeu (2 ou 3)
    vendas = ler_vendas_salvas().get("vendas", {})
    alta = _ler_json(ARQUIVO_EM_ALTA)
    PESO_CATEGORIA.clear()
    PESO_CATEGORIA.update(PESO_BASE)
    novas = [(b, bool(f)) for b, f in alta.get("buscas") or []]
    EM_ALTA[:] = [b for b, _ in novas]
    CATEGORIAS_EM_ALTA[:] = [(nome, [tipo_do_produto(b) for b, f in novas if f == fem])
                             for nome, fem in (("♀ em alta nos grupos", True), ("em alta nos grupos", False))
                             if any(f == fem for _, f in novas)]
    for cat in list(alta.get("categorias") or []) + [n for n, _ in CATEGORIAS_EM_ALTA]:
        PESO_CATEGORIA[cat] = max(PESO_CATEGORIA.get(cat, 1), 2)
    for cat, qtd in vendas.items():
        PESO_CATEGORIA[cat] = max(PESO_CATEGORIA.get(cat, 1), 3 if qtd >= 3 else 2)

# ---------- Aprende com os outros grupos (08/11, Gabriel: "o bot vê os outros grupos... compara... e já começa
# a mandar mais no nosso, tudo automático") ----------
# 1x por dia (junto das vendas), com o que o chip guardou dos grupos dos outros afiliados nos últimos 3 dias
# (whatsapp/grupos_observados.json). Engajamento = reações + 1 por post + 3 por grupo diferente que postou.
#  - Categoria que a gente já tem e está entre as 8 que mais engajam lá: peso 2 no rodízio.
#  - Produto que eles postam e a gente NÃO busca (até 6, com 2+ grupos ou 5+ reações): vira busca nova, nas
#    categorias "♀ em alta nos grupos" / "em alta nos grupos" (peso 2). Passa pelos mesmos filtros de sempre.
# A cópia direta das ofertas continua (postar_copiado), agora pegando primeiro a que mais engaja.
ARQUIVO_EM_ALTA = "em_alta_grupos.json"
EM_ALTA_DIAS = 3
EM_ALTA_CATEGORIAS = 8
EM_ALTA_BUSCAS = 6
_PALAVRAS_PROPAGANDA = {"oferta", "ofertas", "promocao", "promo", "original", "originais", "novo", "nova",
                        "lancamento", "frete", "gratis", "envio", "imediato", "pronta", "entrega", "top", "super",
                        "premium", "barato", "achadinho", "achadinhos", "imperdivel", "queima", "estoque",
                        "ml", "kg", "cm", "mm", "un", "pcs", "pc", "und", "unid", "cor", "cores", "tamanho"}

def busca_do_titulo(titulo):
    palavras = [w for w in re.findall(r"[a-z]+", normalizar(titulo))
                if len(w) > 2 and w not in PALAVRAS_VAZIAS and w not in _PALAVRAS_PROPAGANDA]
    return " ".join(palavras[:4]) if len(palavras) >= 2 else None

def aprender_com_concorrentes():
    import concorrentes
    desde = time.time() - EM_ALTA_DIAS * 86400
    nossas = {categoria_do_produto(p) for p in SIMPLES + CAROS}
    tem, falta = {}, {}
    for jid, g in _ler_json(os.path.join(PASTA_WHATSAPP, "grupos_observados.json")).items():
        for post in g.get("posts") or []:
            if (post.get("quando") or 0) < desde:
                continue
            titulo = concorrentes.titulo(post.get("texto") or "")
            if not titulo or bloqueado(normalizar(titulo)) or not deste_bot(titulo):
                continue
            cat = categoria_do_produto(titulo)
            if cat not in nossas:              # produto novo: só pelo nome real da Shopee (abaixo)
                continue
            a = tem.setdefault(cat, {"reacoes": 0, "posts": 0, "grupos": set(), "titulos": []})
            a["reacoes"] += len(post.get("reacoes") or {})
            a["posts"] += 1
            a["grupos"].add(g.get("nome") or jid)
            a["titulos"].append(titulo)
    # O que eles postam e a gente não busca: pelo NOME NA SHOPEE dos links que o bot abriu (sem a propaganda)
    for d in _ler_json(ARQUIVO_PRODUTOS_CONCORRENTES).values():
        nome = d.get("nome") or ""
        if d.get("quando", 0) < desde or not nome or bloqueado(normalizar(nome)) or not deste_bot(nome):
            continue
        if categoria_do_produto(nome) in nossas:
            continue
        a = falta.setdefault(tipo_do_produto(nome), {"reacoes": 0, "posts": 0, "grupos": set(), "titulos": []})
        a["reacoes"] += int(d.get("pontos") or 0)
        a["posts"] += 1
        a["grupos"].add(d.get("origem") or "?")
        a["titulos"].append(nome)
    def pontos(a):
        return a["reacoes"] + a["posts"] + 3 * len(a["grupos"])
    categorias = [c for c, a in sorted(tem.items(), key=lambda x: -pontos(x[1]))
                  if a["posts"] >= 2][:EM_ALTA_CATEGORIAS]
    buscas = []
    for tipo, a in sorted(falta.items(), key=lambda x: -pontos(x[1])):
        if len(buscas) >= EM_ALTA_BUSCAS:
            break
        if len(a["grupos"]) < 2 and a["reacoes"] < 5:
            continue
        busca = busca_do_titulo(Counter(a["titulos"]).most_common(1)[0][0])
        if busca and busca not in [b for b, _ in buscas] and not bloqueado(busca):
            buscas.append((busca, concorrentes.publico(" ".join(a["titulos"])) == "♀"))
    antes = _ler_json(ARQUIVO_EM_ALTA)
    novo = {"atualizado": f"{datetime.now():%d/%m %H:%M}", "categorias": categorias, "buscas": buscas}
    try:
        with open(ARQUIVO_EM_ALTA, "w", encoding="utf-8") as f:
            json.dump(novo, f, ensure_ascii=False)
    except OSError as e:
        print("  Aviso: não consegui salvar o em alta dos grupos:", e)
    print(f"  Outros grupos: em alta {', '.join(categorias) or 'nada ainda'}"
          + (f" | buscas novas: {', '.join(b for b, _ in buscas)}" if buscas else ""))
    if (categorias or buscas) and (antes.get("categorias") != categorias
                                   or [list(x) for x in antes.get("buscas") or []] != [list(x) for x in buscas]):
        avisar_painel(f"👀 <b>{html.escape(BOT)}</b> olhou os outros grupos ({EM_ALTA_DIAS} dias). Mais vez para: "
                      + html.escape(", ".join(categorias) or "-")
                      + ("\nBuscas novas: " + html.escape(", ".join(b for b, _ in buscas)) if buscas else ""))

def ligar_vendas(itens):
    # Venda -> busca do post -> categoria. {categoria: unidades vendidas}
    por_id, por_nome = {}, {}
    try:
        with open(ARQUIVO_ITENS_POSTADOS, encoding="utf-8") as f:
            por_id = dict(l.rstrip("\n").split("\t", 1) for l in f if "\t" in l)
    except OSError:
        pass
    try:
        with open(ARQUIVO_HISTORICO, encoding="utf-8") as f:
            for l in f:
                if "\t" in l:
                    palavra, nome = l.rstrip("\n").split("\t", 1)
                    por_nome[chave_nome(nome)] = palavra
    except OSError:
        pass
    vendas = Counter()
    for item in itens:
        palavra = por_id.get(str(item.get("itemId"))) or por_nome.get(chave_nome(item.get("itemName") or ""))
        if palavra:        # só venda de post do bot (sem sub_id, tipo o ventilador da tia, não conta)
            vendas[categoria_do_produto(palavra)] += int(item.get("qty") or 1)
    return dict(vendas)

def aprender_com_vendas():
    salvas = ler_vendas_salvas()
    agora = int(time.time())
    try:
        try:
            itens = consultar_vendas(agora - VENDAS_DIAS * 86400, agora)
        except ErroShopee:                                # se a Shopee não tiver o campo da quantidade
            itens = consultar_vendas(agora - VENDAS_DIAS * 86400, agora, "")
    except Exception as e:
        print(f"  Vendas: não deu para ler o relatório da Shopee ({type(e).__name__}); uso o da última vez.")
        return
    vendas = ligar_vendas(itens)
    print(f"  Vendas: {len(itens)} item(ns) no relatório, {sum(vendas.values())} de posts deste bot"
          + (": " + ", ".join(f"{c} {q}" for c, q in sorted(vendas.items(), key=lambda x: -x[1])) if vendas else "."))
    try:
        with open(ARQUIVO_VENDAS, "w", encoding="utf-8") as f:
            json.dump({"atualizado": f"{datetime.now():%d/%m %H:%M}", "vendas": vendas}, f, ensure_ascii=False)
    except OSError as e:
        print("  Aviso: não consegui salvar as vendas aprendidas:", e)
    if vendas and vendas != salvas.get("vendas"):         # mudou: conta no painel (1 vez)
        avisar_painel(f"📈 <b>{html.escape(BOT)}</b> aprendeu com as vendas (30 dias). Mais vez no rodízio para: "
                      + html.escape(", ".join(f"{c} ({q})" for c, q in sorted(vendas.items(), key=lambda x: -x[1]))))

def aprender():
    # Vendas + outros grupos, e aplica no rodízio. Um erro numa parte não impede a outra nem o bot
    # (o relatório de vendas é o da Shopee: o bot do Mercado Livre só aprende com os outros grupos)
    partes = (aprender_com_concorrentes,) if LOJA == "mercadolivre" else (aprender_com_vendas, aprender_com_concorrentes)
    for parte in partes:
        try:
            parte()
        except Exception as e:
            print(f"  Aviso: {parte.__name__} falhou ({type(e).__name__}: {e}).")
    aplicar_aprendido()

# Buscas de época (06/11, Gabriel): Natal e Ano Novo saem sozinhas da lista quando a data passa e voltam no ano
# seguinte, sem ninguém precisar mexer. (palavras, (mês, dia) de começo, (mês, dia) de fim); fim pode virar o ano.
EPOCAS = [
    (["natal", "guirlanda", "pisca pisca", "papai noel"], (10, 1), (12, 25)),
    (["ano novo", "reveillon"], (12, 1), (1, 1)),
]

def na_epoca(palavra, hoje=None):
    hoje = hoje or datetime.now().date()
    busca = normalizar(palavra)
    for trechos, inicio, fim in EPOCAS:
        if any(t in busca for t in trechos):
            dia = (hoje.month, hoje.day)
            return inicio <= dia <= fim if inicio <= fim else (dia >= inicio or dia <= fim)
    return True                                # produto de qualquer época

def marcar_vez(usadas, cat):
    # Postou: categoria com peso 3 (PESO_CATEGORIA) ganha "cat#1" e "cat#2" antes de esperar a volta acabar
    peso = PESO_CATEGORIA.get(cat.split("|")[-1], 1)
    extras = sum(1 for u in usadas if u.startswith(cat + "#"))
    return usadas | {f"{cat}#{extras + 1}" if extras + 1 < peso else cat}

def tentar(lista, caro, postados, palavras_recentes, nomes_recentes):
    # Rodízio por CATEGORIA (ver CATEGORIAS): a categoria que postou só volta depois que todas as
    # outras da lista tiveram a vez, e volta com a próxima garagem (busca). A garagem que não achou
    # produto bom sai da volta; quando a categoria não tem mais garagem para tentar, a vez dela passou.
    # Caros e simples têm voltas separadas ("caro|cama" e "cama"), senão a lista curta dos caros
    # liberava cama/mesa dos simples cedo demais; o "recente" (últimos 15 posts) vale para as duas.
    lista = [p for p in lista if na_epoca(p)] or lista   # Natal/Ano Novo só na época deles
    ciclo = carregar_ciclo()                   # garagens (buscas) que já tiveram a vez
    usadas = carregar_categorias()             # categorias que já tiveram a vez nesta volta
    def chave(p):
        return ("caro|" if caro else "") + categoria_do_produto(p)
    grupos = {}                                # categoria -> suas garagens (buscas)
    for p in lista:
        grupos.setdefault(chave(p), []).append(p)
    if set(grupos) <= usadas:                  # todas as categorias tiveram a vez: volta nova de categorias
        usadas = {u for u in usadas if u.split("#")[0] not in grupos}   # (o "#1" é a vez extra de quem tem peso)
    for cat, ps in grupos.items():
        if cat not in usadas and all(p in ciclo for p in ps):
            ciclo -= set(ps)                   # é a vez da categoria e as garagens dela já rodaram: recomeçam
    salvar_ciclo(ciclo)
    salvar_categorias(usadas)
    # Há quantos posts cada categoria saiu (simples e caros juntos: a mesa de jantar pode vir das duas listas)
    hist = carregar_historico(300)
    ha_quanto = {}
    for i, (p, _) in enumerate(hist):
        ha_quanto[categoria_do_produto(p)] = len(hist) - i
    for p in palavras_recentes:                # (o teste passa as recentes sem o arquivo)
        ha_quanto.setdefault(categoria_do_produto(p), 1)
    def distancia(p):
        return ha_quanto.get(categoria_do_produto(p), 999)
    da_vez = [p for p in lista if p not in ciclo and chave(p) not in usadas] or list(lista)
    # 1º: da vez e sem sair nos últimos 40 posts. Se as da vez saíram há pouco (ex.: a última categoria da volta
    # dos caros acabou de sair pelos simples), pega outra que não saiu nos últimos 40, mesmo fora da ordem da
    # volta: repetir de perto é pior. Se nem assim (lista curta), a que saiu há mais tempo.
    todas = [p for p in lista if p not in ciclo] or list(lista)
    palavras = ([p for p in da_vez if distancia(p) > CATEGORIA_SEM_REPETIR]
                or [p for p in todas if distancia(p) > CATEGORIA_SEM_REPETIR])
    if not palavras:
        maior = max(distancia(p) for p in todas)
        palavras = [p for p in todas if distancia(p) >= maior * 0.9]
    if ALTERNAR_FEMININO and hist:
        # Um feminino, um masculino: o lado da vez é o contrário do último post (simples e caros juntos)
        quer_fem = not categoria_do_produto(hist[-1][0]).startswith("♀")
        def do_lado(ps):
            return [p for p in ps if categoria_do_produto(p).startswith("♀") == quer_fem]
        palavras = (do_lado(palavras)
                    or do_lado([p for p in todas if distancia(p) > CATEGORIA_SEM_REPETIR])
                    or do_lado([p for p in todas if distancia(p) > 15])
                    or palavras)

    def teve_a_vez(palavra):
        # Não postou: se a categoria não tem mais garagem para tentar nesta volta, a vez dela passou
        if all(q in ciclo for q in grupos.get(chave(palavra), [])):
            salvar_categorias(carregar_categorias() | {chave(palavra)})
    random.shuffle(palavras)
    tentadas = achados = falhas = 0
    motivos, exemplo = Counter(), []
    for palavra in palavras:
        if palavra in ciclo:                   # o tipo dela acabou de postar nesta mesma rodada
            continue
        if tentadas >= MAX_PALAVRAS_RODADA:    # buscar a lista inteira de uma vez estoura o limite da Shopee
            break
        ciclo.add(palavra)
        salvar_ciclo(ciclo)
        tentadas += 1
        marcas_fortes = marcas_do_tipo(palavra)
        # Tipo com marca forte: busca também "produto + marca" (ex.: "panela de pressão Tramontina")
        buscas = ([f"{palavra} {random.choice(marcas_fortes)}"] if marcas_fortes else []) + [palavra]
        produtos, vistos = [], set()
        for termo in buscas:
            try:
                for p in buscar_com_repeticao(termo):
                    if p["itemId"] not in vistos:
                        vistos.add(p["itemId"])
                        produtos.append(p)
            except ErroLimite:
                ciclo.discard(palavra)         # não foi culpa da palavra: ela continua na volta
                salvar_ciclo(ciclo)
                print("  A Shopee pediu para ir mais devagar (limite de buscas). Paro e tento na próxima rodada.")
                estado_rodada["limite"] = True
                return False
            except Exception as e:
                falhas += 1
                print(f"  Erro buscando '{termo}': {e}")
        achados += len(produtos)
        minimo = VENDAS_MINIMAS_CARO if caro else VENDAS_MINIMAS
        bons = []
        for p in produtos:
            motivo = motivo_recusa(p, palavra, caro, minimo, postados, nomes_recentes)
            if motivo:
                motivos[motivo] += 1
                if motivo not in ("não combina com a busca", "já postado") and not exemplo:
                    exemplo.append(f"{p['productName'][:50]} | nota {p.get('ratingStar')} | desconto "
                                   f"{p.get('priceDiscountRate')} | comissão {p.get('commissionRate')} | "
                                   f"loja {p.get('shopType')} | vendas {p.get('sales')} -> {motivo}")
            else:
                bons.append(p)
        for p in bons:
            p["nome_post"] = nome_curto(p["productName"], palavra)
            marca = marca_do_produto(p)
            if p["nome_post"] and marca and normalizar(marca) not in normalizar(p["nome_post"]):
                palavras_nome = p["nome_post"].split()
                if normalizar(palavras_nome[-1]) == normalizar(marca.split()[0]):
                    palavras_nome.pop()                # "…60cm Euro" (marca cortada) -> tira o pedaço
                p["nome_post"] = " ".join(palavras_nome + [marca])   # "Panela de Pressão" -> "… Panelux"
        motivos["nome ruim"] += sum(1 for p in bons if not p["nome_post"])
        bons = [p for p in bons if p["nome_post"]]
        # Tipo com marca forte: só vale marca do tipo (ex.: panela só Tramontina, Rochedo...)
        com_marca = [p for p in bons if marca_do_produto(p)
                     and (not marcas_fortes or marca_do_produto(p) in marcas_fortes)]
        if marca_opcional(palavra):            # ventilador, capa de sofá, mesa...: marca à vontade (de marca na frente)
            aceitos = sorted(bons, key=lambda p: p not in com_marca)
        elif caro or marcas_fortes:            # caro e tipo de marca forte: só com marca
            aceitos = com_marca
        elif EXIGIR_MARCA_SEMPRE:              # os outros: sem marca só se muito bem avaliado (nota + vendas)
            aceitos = com_marca + [p for p in bons if p not in com_marca and bem_avaliado_sem_marca(p)]
        else:
            aceitos = bons
        motivos["sem marca"] += len(bons) - len(aceitos)
        bons = aceitos
        if exige_medida(palavra):              # mesa, geladeira, forno, cortina...: sem medida no título não vai
            com_medida = [p for p in bons if medida(p["productName"], palavra)]
            motivos["sem medida"] += len(bons) - len(com_medida)
            bons = com_medida
        if not bons:
            teve_a_vez(palavra)
            continue
        if estado_campanha["fase"] == "dia":   # dia de campanha: desconto grande na frente (se a busca tiver)
            bons = [p for p in bons if float(p.get("priceDiscountRate") or 0) >= CAMPANHA_DESCONTO_MINIMO] or bons
        pontos = pontuacoes(bons)
        # Aparelho de tomada: bivolt primeiro, depois 220V, 110V só em último caso
        # e, entre esses, o anúncio que diz a medida (o comprador quer saber se cabe)
        ordem = sorted(range(len(bons)), key=lambda i: (preco_por_polegada(bons[i], palavra),   # TV: a mais barata por polegada (0 nos outros)
                                                        degrau_loja(bons[i]) or 9,   # escada de lojas: 1º Oficial...
                                                        ordem_voltagem(bons[i], palavra),
                                                        medida(bons[i]["productName"], palavra) is None,
                                                        -pontos[i]))
        # Os melhores primeiro, mas foto que não é só fundo branco na frente (sort estável)
        avaliados = [bons[i] for i in ordem[:FOTOS_AVALIADAS * 2]]
        if pede_cor_sobria(palavra):
            # Cortina, cama, tapete, sofá...: foto com cor chamativa (rosa, laranja, verde...) fica de fora
            sobrios = [c for c in avaliados if cor_chamativa(c["imageUrl"]) <= LIMITE_COR_CHAMATIVA]
            motivos["cor chamativa"] += len(avaliados) - len(sobrios)
            avaliados = sobrios
        candidatos = sorted(avaliados[:FOTOS_AVALIADAS],
                            key=lambda c: (degrau_loja(c) or 9, ordem_voltagem(c, palavra),
                                           medida(c["productName"], palavra) is None,
                                           fundo_branco(c["imageUrl"])))
        escolhido = None
        for cand in candidatos[:REVISOES_IA_POR_BUSCA]:
            revisao = revisar_com_ia(cand, palavra)
            if revisao and not revisao["aprovado"]:
                print(f"  IA recusou ({palavra}): {cand['nome_post']} | {revisao['motivo']}")
                motivos["IA recusou"] += 1
                continue
            if revisao and revisao["nome"]:
                cand["nome_post"] = revisao["nome"]
            if revisao:
                cand["chamada_ia"], cand["beneficio"] = revisao.get("chamada"), revisao.get("beneficio")
            problemas = conferir_modelo_ideal(cand, palavra)
            if problemas:
                print(f"  Fora do modelo ideal ({palavra}): {', '.join(problemas)}.")
                motivos["fora do modelo ideal"] += 1
                continue
            cand["nome_post"] = completar_nome(cand, palavra)   # + medidas/litros e voltagem
            escolhido = cand
            break
        if not escolhido:
            teve_a_vez(palavra)
            continue
        # Postou: a categoria inteira (todas as garagens dela) espera as outras categorias terem a vez
        salvar_categorias(marcar_vez(carregar_categorias(), chave(palavra)))
        publicar(escolhido, palavra, caro)
        return True
    principais = ", ".join(f"{m} {n}" for m, n in motivos.most_common() if n) or "nada para filtrar"
    falhou = f" {falhas} buscas falharam na Shopee." if falhas else ""
    print(f"  ({'caros' if caro else 'simples'}: {tentadas} palavras buscadas, {achados} produtos achados, "
          f"nenhum passou nos filtros. Recusados por: {principais}){falhou}")
    ultimo_resumo["texto"] = (f"Última rodada: {tentadas} palavras, {achados} produtos achados, nenhum passou.{falhou} "
                              f"Recusados por: " + ", ".join(f"{m} {n}" for m, n in motivos.most_common(4) if n))
    if exemplo:
        print("  Exemplo de recusado:", exemplo[0])
    return False

estado_rodada = {"limite": False}   # a Shopee barrou por excesso de buscas nesta rodada?
ultimo_resumo = {"texto": ""}       # resumo da última rodada sem post: vai junto no alerta de bot parado

def rodada():
    # Devolve True se postou
    estado_rodada["limite"] = False
    if not TELEGRAM_POSTAR:
        # Só o WhatsApp recebe: o ritmo é dele. Se ainda não é a vez, nem gasta buscas na Shopee.
        motivo_zap = motivo_sem_whatsapp()
        if motivo_zap:
            print(f"  Sem post agora: WhatsApp ({motivo_zap}).")
            return True
    if postar_destaque():                       # produto colado no painel tem a vez antes da busca normal
        return True
    if postar_copiado():                        # oferta boa que os concorrentes postaram (1 a cada 2 posts)
        return True
    postados = carregar_postados() | nomes_ja_postados()
    historico = carregar_historico()
    palavras_recentes = {palavra for palavra, _ in historico}
    nomes_recentes = [nome for _, nome in historico]
    if vez_do_caro(historico):
        if tentar(CAROS, True, postados, palavras_recentes, nomes_recentes):
            return True
        if estado_rodada["limite"]:
            return False
        print("  Nenhum produto caro disponível agora, indo de produto simples.")
    if tentar(SIMPLES + [b for b in EM_ALTA if b not in SIMPLES], False, postados, palavras_recentes, nomes_recentes):
        return True
    print("  Nenhum produto novo nesta rodada.")
    return False

def aplicar_ajustes():
    # ajustes.txt (o painel do Telegram escreve) muda os números sem reiniciar; sem ele, valem os de cima
    globals().update(PADROES)
    try:
        with open(ARQUIVO_AJUSTES, encoding="utf-8") as f:
            linhas = f.readlines()
    except FileNotFoundError:
        return
    for linha in linhas:
        chave, _, valor = linha.partition("=")
        if chave.strip() in AJUSTAVEIS:
            try:
                v = float(valor.strip().replace(",", "."))
                globals()[chave.strip()] = int(v) if v == int(v) else v
            except ValueError:
                print(f"  Aviso: ajuste inválido no {ARQUIVO_AJUSTES}: {linha.strip()}")

def salvar_status(post=None):
    try:
        with open(ARQUIVO_STATUS, encoding="utf-8") as f:
            status = json.load(f)
    except (OSError, ValueError):
        status = {}
    agora = datetime.now()
    if status.get("dia") != f"{agora:%d/%m/%Y}":
        status.update(dia=f"{agora:%d/%m/%Y}", posts_hoje=0)
    if post:
        status.update(posts_hoje=status["posts_hoje"] + 1, ultimo=post, ultimo_em=f"{agora:%H:%M}")
    status.update(visto_em=f"{agora:%d/%m %H:%M}", ajustes={k: globals()[k] for k in AJUSTAVEIS},
                  campanha=(f"{estado_campanha['nome']} ({'hoje' if estado_campanha['fase'] == 'dia' else 'amanhã'})"
                            if estado_campanha["fase"] else None))
    try:
        with open(ARQUIVO_STATUS, "w", encoding="utf-8") as f:
            json.dump(status, f, ensure_ascii=False)
    except OSError as e:
        print("  Aviso: não consegui salvar o status:", e)

alerta_parado = {"avisado": False}

def verificacao_geral():
    # Uma vez por dia, quando começa o horário de postar (e depois de cada reinício): confere servidor,
    # Shopee, Google, Telegram, painel, WhatsApp e os canais observados, e manda o resultado no painel.
    # Assim um problema aparece às 8h, e não horas depois. Ver verificacao.py
    try:
        import verificacao
        resultados = verificacao.verificar(cfg, os.getcwd(), WHATSAPP_URL)
        texto = verificacao.resumo(resultados, BOT, f"{datetime.now():%d/%m %H:%M}")
        avisar_painel(texto)
        problemas = [f"{nome}: {detalhe}" for ok, nome, detalhe in resultados if ok is False]   # ⏳ esperando não conta
        print("  Verificação geral:", "tudo certo" if not problemas else "; ".join(problemas))
    except Exception as e:
        print("  Verificação geral falhou:", type(e).__name__, e)

def verificar_parado():
    # Dentro do horário de postar, sem nenhum post há ALERTA_SEM_POST_MIN minutos: avisa no painel (1 vez
    # por parada). Conta a partir da hora de começar do dia, para não avisar às 8h por causa da madrugada.
    agora = datetime.now()
    inicio_hoje = agora.replace(hour=HORA_INICIO, minute=0, second=0, microsecond=0).timestamp()
    try:
        ultimo = os.path.getmtime(ARQUIVO_HISTORICO)
    except OSError:
        ultimo = 0
    # (09/11) conta também a partir de quando o bot ligou: bot novo ligado às 15h não está "parado desde as 8h"
    parado = (time.time() - max(ultimo, inicio_hoje, INICIO_BOT)) / 60
    limite = ALERTA_SEM_POST_MIN
    if not TELEGRAM_POSTAR:
        # só o WhatsApp recebe: o ritmo dele é mais lento, e depois do máximo do dia não há mais post
        limite = max(limite, WHATSAPP_INTERVALO * 1.25 + 30)
        if contagem_whatsapp()["posts"] >= WHATSAPP_MAX_DIA:
            parado = 0
    if parado < limite:
        alerta_parado["avisado"] = False
    elif not alerta_parado["avisado"]:
        alerta_parado["avisado"] = True
        avisar_painel(f"⚠️ <b>{html.escape(BOT)}</b>: faz {parado:.0f} min sem postar. "
                      + (html.escape(ultimo_resumo["texto"]) + "\n" if ultimo_resumo["texto"] else "")
                      + f"Detalhes em /log {html.escape(BOT)} 30")
        print(f"  Alerta mandado no painel: {parado:.0f} min sem postar.")

def dormir(segundos):
    # Espera o intervalo, mas acorda na hora se o painel pedir um post (devolve True nesse caso)
    fim = time.time() + segundos
    while time.time() < fim:
        if os.path.exists(ARQUIVO_MANDAR_GRUPOS):   # /zapconvite no painel: manda a mensagem dos grupos já
            os.remove(ARQUIVO_MANDAR_GRUPOS)
            enviar_mensagem_grupos("o painel pediu")
        if os.path.exists(ARQUIVO_POSTAR_AGORA):
            os.remove(ARQUIVO_POSTAR_AGORA)
            print("  Painel pediu um post agora.")
            return True
        time.sleep(min(10, max(0, fim - time.time())))
    return False

def preparar_pasta_bot():
    if not os.path.isdir(PASTA_BOT):
        sys.exit(f"Não achei a pasta do bot: {PASTA_BOT}")
    if BOT == "casa":
        # Antes de ter vários bots esses arquivos ficavam na pasta principal: o Casa herda (cópia)
        for arquivo in (ARQUIVO_POSTADOS, ARQUIVO_HISTORICO, ARQUIVO_CICLO, ARQUIVO_GRUPOS):
            antigo, novo = os.path.join(PASTA_PRINCIPAL, arquivo), os.path.join(PASTA_BOT, arquivo)
            if os.path.exists(antigo) and not os.path.exists(novo):
                shutil.copy2(antigo, novo)
    os.chdir(PASTA_BOT)

preparar_pasta_bot()
INICIO_BOT = time.time()
print(f"Bot {BOT} rodando. Para parar: Ctrl+C")
forcar = False
ultima_verificacao = None
ultimas_vendas = None
while True:
    aplicar_ajustes()
    aplicar_campanha()                            # 11.11, Black Friday, 12.12: muda o ritmo por cima dos ajustes
    agora = datetime.now()
    print(f"[{agora:%d/%m %H:%M}]")
    no_horario = HORA_INICIO <= agora.hour < HORA_FIM
    if no_horario and os.path.exists(ARQUIVO_MANDAR_CUPONS) and mandar_alerta_cupons():
        os.remove(ARQUIVO_MANDAR_CUPONS)
    postou = True
    if no_horario and ultima_verificacao != agora.date():
        ultima_verificacao = agora.date()
        verificacao_geral()
    if ultimas_vendas != (agora.date(), agora.hour >= 11):   # ao ligar e de novo depois das 11h (relatório novo)
        ultimas_vendas = (agora.date(), agora.hour >= 11)
        aprender()                                # vendas da Shopee + o que engaja nos outros grupos
    if no_horario or forcar:
        try:
            postou = rodada()
        except Exception as e:
            print("  Erro na rodada:", e)
            postou = False
    else:
        print("  Fora do horário, aguardando.")
    salvar_status()
    if no_horario:
        verificar_parado()
    if not postou:
        # Não achou nada: não espera o intervalo inteiro (era 6 a 15 min parado), tenta de novo logo.
        # Se a Shopee barrou por excesso de buscas, espera mais para ela liberar.
        espera = ESPERA_APOS_LIMITE if estado_rodada["limite"] else ESPERA_SEM_POST
        print(f"  Tento de novo em {espera // 60} min.")
        forcar = dormir(espera)
    elif not TELEGRAM_POSTAR:
        # Só WhatsApp: o ritmo é o dele (motivo_sem_whatsapp). Dorme até a vez do próximo post
        # (entre 30 s e 10 min), senão o intervalo do Telegram (6-15 min) segurava os 180 por dia
        motivo_sem_whatsapp()
        espera = estado_rodada.pop("espera_zap", 60)
        forcar = dormir(int(max(30, min(espera, 600))))
    elif PICO_INICIO <= datetime.now().hour < PICO_FIM:
        forcar = dormir(random.randint(PICO_MIN * 60, PICO_MAX * 60))
    else:
        forcar = dormir(random.randint(INTERVALO_MIN * 60, INTERVALO_MAX * 60))
