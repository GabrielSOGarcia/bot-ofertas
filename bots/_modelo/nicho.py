# MODELO para um bot novo da Shopee (ex.: Shopee geral). Para criar:
#   1. Copie esta pasta com o nome do bot (ex.: bots/geral) — sem "_" no começo
#   2. Crie o canal no Telegram, ponha o bot do canal como administrador e coloque no config.txt
#      a linha CANAL_GERAL=@nome_do_canal (o Gabriel faz; nunca mexer no config.txt pelo código)
#   3. Troque abaixo o que for diferente do Casa. O que não estiver aqui fica igual ao Casa.
#   4. No painel do Telegram: /ligar geral
# Pastas que começam com "_" (como esta) são ignoradas pelo painel.

CHAVE_CANAL = "CANAL_GERAL"

# Lista de produtos: substitui a do Casa inteira (categoria: palavras de busca)
PALAVRAS = {
    "exemplo": ["fone bluetooth", "smartwatch", "mochila"],
}
CAROS = ["notebook", "celular"]

# Marcas: soma às do Casa (as do Casa continuam valendo)
MARCAS = MARCAS + ["Apple", "Lenovo"]

# Chamadas que só fazem sentido na casa: troque pelas do nicho
CHAMADAS_GERAIS = ["🔥 ACHADO DO DIA", "👀 OLHA ESSE PREÇO", "😍 TODO MUNDO TÁ LEVANDO",
                   "😱 VALE MUITO A PENA", "🛒 QUEM VIU, LEVOU"]
CHAMADAS_POR_TIPO = []
CHAMADAS_CARO = ["💎 PRODUTO TOP COM PREÇO DE OPORTUNIDADE", "😮 ESSE PREÇO NÃO É TODO DIA"]
CHAMADAS_ATE_100 = ["🤑 PRECINHO CAMARADA"]
NICHO_IA = "achadinhos em geral"   # a IA revisa pensando nesse público

# Outros ajustes podem ser trocados aqui também (ex.: INTERVALO_MIN = 10)
