import json, os, urllib.error, urllib.request

GEMINI_MODELO = "gemini-3.5-flash-lite"   # o mesmo do postar_shopee.py
CONFIG_PATH = os.environ.get("BOT_CONFIG", r"C:\bot-config\config.txt")   # senhas fora da pasta do bot

def ler_config(caminho=CONFIG_PATH):
    config = {}
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if "=" in linha:
                chave, valor = linha.split("=", 1)
                config[chave.strip()] = valor.strip()
    return config

cfg = ler_config()
for chave in ["TOKEN", "CANAL", "SHOPEE_APPID", "SHOPEE_SECRET", "GEMINI_KEY"]:
    print(chave, "OK" if cfg.get(chave) else "FALTANDO")
# Painel do Telegram (painel.py): PAINEL_ADMIN o próprio painel mostra na primeira mensagem
for chave in ["PAINEL_TOKEN", "PAINEL_ADMIN"]:
    print(chave, "OK" if cfg.get(chave) else "FALTANDO (só precisa para o painel)")

# Chave do Gemini: testa de verdade com uma pergunta curtinha (a chave nunca aparece na tela)
if cfg.get("GEMINI_KEY"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODELO}:generateContent"
    corpo = json.dumps({"contents": [{"parts": [{"text": "Responda só: OK"}]}]}).encode()
    req = urllib.request.Request(url, data=corpo, method="POST",
                                 headers={"Content-Type": "application/json",
                                          "x-goog-api-key": cfg["GEMINI_KEY"]})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            dados = json.loads(resp.read())
        print("Teste do Gemini OK. Resposta:", dados["candidates"][0]["content"]["parts"][0]["text"].strip())
    except urllib.error.HTTPError as e:
        print(f"Teste do Gemini FALHOU (erro {e.code}): 400/403 = chave errada, 404 = modelo, 429 = limite, "
              "500/503 = Google sobrecarregado, tente de novo daqui a pouco")
    except Exception as e:
        print(f"Teste do Gemini FALHOU ({type(e).__name__}): confira a internet")