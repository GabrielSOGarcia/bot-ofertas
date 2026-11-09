import hashlib, json, time, urllib.request

CONFIG_PATH = r"C:\bot-config\config.txt"   # senhas ficam fora da pasta do bot

def ler_config(caminho=CONFIG_PATH):
    config = {}
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            if "=" in linha:
                chave, valor = linha.strip().split("=", 1)
                config[chave.strip()] = valor.strip()
    return config

cfg = ler_config()
APPID = cfg["SHOPEE_APPID"]
SECRET = cfg["SHOPEE_SECRET"]
URL = "https://open-api.affiliate.shopee.com.br/graphql"

consulta = """
{
  productOfferV2(keyword: "organizador", limit: 3) {
    nodes { productName price imageUrl offerLink commissionRate sales }
  }
}
"""

payload = json.dumps({"query": consulta})
timestamp = str(int(time.time()))
assinatura = hashlib.sha256((APPID + timestamp + payload + SECRET).encode()).hexdigest()

req = urllib.request.Request(URL, data=payload.encode(), method="POST", headers={
    "Content-Type": "application/json",
    "Authorization": f"SHA256 Credential={APPID}, Timestamp={timestamp}, Signature={assinatura}",
})

with urllib.request.urlopen(req) as resp:
    dados = json.loads(resp.read())

if "errors" in dados:
    print("ERRO:", dados["errors"])
else:
    for p in dados["data"]["productOfferV2"]["nodes"]:
        print(p["productName"])
        print("  Preço: R$", p["price"])
        print("  Comissão:", p["commissionRate"])
        print("  Link:", p["offerLink"])
        print()