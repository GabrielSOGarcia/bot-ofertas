# Verificação geral: confere tudo de que o bot depende e devolve uma lista (ok, nome, detalhe).
# Roda sozinha todo dia quando o bot começa a postar (e depois de cada reinício), e a qualquer hora
# pelo painel (/verificar). Se o programa do WhatsApp estiver parado, tenta ligar de novo sozinha.
import hashlib, html, json, os, shutil, subprocess, time, urllib.error, urllib.parse, urllib.request

GEMINI_MODELO = "gemini-3.5-flash-lite"
LEITURA_VELHA_HORAS = 3        # canal observado sem leitura nova há mais que isso = problema

def _pegar(url, dados=None, cabecalhos=None, timeout=20):
    req = urllib.request.Request(url, data=dados, headers=cabecalhos or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read() or b"{}")

def _tentar(nome, funcao):
    # Roda uma conferência: qualquer erro vira "falhou" com o motivo curto, nunca derruba as outras
    try:
        ok, detalhe = funcao()
    except urllib.error.HTTPError as e:
        ok, detalhe = False, f"erro {e.code}"
    except Exception as e:
        ok, detalhe = False, f"{type(e).__name__}: {str(e)[:120]}"
    return (ok, nome, detalhe)

def _servico_ativo(nome):
    try:
        r = subprocess.run(["systemctl", "is-active", nome], capture_output=True, text=True, timeout=10)
        return r.stdout.strip() == "active"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None            # não é o servidor (ex.: testando no PC): não conta

def _religar(nome):
    try:
        subprocess.run(["sudo", "-n", "systemctl", "restart", nome], capture_output=True, timeout=60)
        time.sleep(15)
        return _servico_ativo(nome)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def verificar(cfg, pasta_bot, whatsapp_url="http://127.0.0.1:3010"):
    resultados = []

    def servidor():
        livre = shutil.disk_usage(pasta_bot)
        pct = 100 * livre.free / livre.total
        memoria = ""
        try:
            with open("/proc/meminfo") as f:
                info = {l.split(":")[0]: int(l.split()[1]) for l in f}
            memoria = f", memória livre {info['MemAvailable'] // 1024} MB"
        except (OSError, KeyError, ValueError):
            pass
        return pct > 10, f"disco livre {pct:.0f}%{memoria}"
    resultados.append(_tentar("Servidor", servidor))

    # Shopee: busca mínima assinada, igual à do bot
    def shopee():
        consulta = '{ productOfferV2(keyword: "panela", limit: 1) { nodes { itemId } } }'
        payload = json.dumps({"query": consulta})
        ts = str(int(time.time()))
        assinatura = hashlib.sha256((cfg["SHOPEE_APPID"] + ts + payload + cfg["SHOPEE_SECRET"]).encode()).hexdigest()
        dados = _pegar("https://open-api.affiliate.shopee.com.br/graphql", payload.encode(),
                       {"Content-Type": "application/json",
                        "Authorization": f"SHA256 Credential={cfg['SHOPEE_APPID']}, Timestamp={ts}, Signature={assinatura}"})
        if "errors" in dados:
            texto = str(dados["errors"])
            if "10030" in texto or "10000" in texto:
                return True, "responde, mas está instável agora (limite/erro passageiro)"
            return False, texto[:150]
        return True, "responde"
    resultados.append(_tentar("Shopee (busca de produtos)", shopee))

    def gemini():
        if not cfg.get("GEMINI_KEY"):
            return True, "sem chave (o bot segue sem IA)"
        corpo = json.dumps({"contents": [{"parts": [{"text": "Responda só: ok"}]}],
                            "generationConfig": {"maxOutputTokens": 8}}).encode()
        _pegar(f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODELO}:generateContent", corpo,
               {"Content-Type": "application/json", "x-goog-api-key": cfg["GEMINI_KEY"]})
        return True, "responde"
    resultados.append(_tentar("Google (IA Gemini)", gemini))

    def telegram_canal():
        base = f"https://api.telegram.org/bot{cfg['TOKEN']}"
        eu = _pegar(f"{base}/getMe")["result"]["username"]
        canal = _pegar(f"{base}/getChat?chat_id={urllib.parse.quote(cfg['CANAL'])}")["result"].get("title", "?")
        return True, f"@{eu} no canal \"{canal}\""
    resultados.append(_tentar("Telegram (canal)", telegram_canal))

    def painel():
        eu = _pegar(f"https://api.telegram.org/bot{cfg['PAINEL_TOKEN']}/getMe")["result"]["username"]
        ativo = _servico_ativo("painel")
        if ativo is False:
            return False, f"@{eu} existe, mas o serviço do painel está parado"
        return True, f"@{eu} funcionando"
    resultados.append(_tentar("Painel", painel))

    # Rodízio e memória do bot: tudo fica em arquivo, então depois de travar/reiniciar ele continua de
    # onde parou e não repete produto. Aqui mostra que esses arquivos estão lá e fazem sentido.
    def rodizio():
        def linhas(nome):
            try:
                with open(os.path.join(pasta_bot, nome), encoding="utf-8") as f:
                    return [l.rstrip("\n") for l in f if l.strip()]
            except OSError:
                return None
        ciclo, postados, historico = linhas("ciclo.txt"), linhas("postados.txt"), linhas("historico.txt")
        if postados is None and historico is None:
            if ciclo is None:   # bot novo (ex.: o Geral no 1º dia): a memória nasce no 1º post
                return True, "bot novo: a memória (postados/histórico) começa no 1º post"
            return False, "não achei a memória do bot (postados/histórico): ele pode repetir produtos"
        texto = (f"continua de onde parou: {len(ciclo or [])} buscas já tiveram a vez nesta volta, "
                 f"{len(set(postados or []))} produtos já postados (não repetem)")
        if historico:
            ultimo = historico[-1].split("\t")[-1][:50]
            quando = time.strftime("%d/%m %H:%M", time.localtime(os.path.getmtime(os.path.join(pasta_bot, "historico.txt"))))
            texto += f"; último: {ultimo} ({quando})"
        return True, texto
    resultados.append(_tentar("Rodízio", rodizio))

    # WhatsApp: se o programa não responde, tenta ligar de novo uma vez
    def whatsapp():
        try:
            st = _pegar(whatsapp_url + "/status", timeout=10)
        except (urllib.error.URLError, OSError):
            if _religar("whatsapp") is None:
                return False, "o programa não responde"
            try:
                st = _pegar(whatsapp_url + "/status", timeout=10)
                texto = " (estava parado, religuei sozinho)"
            except (urllib.error.URLError, OSError):
                return False, "o programa estava parado e não consegui religar: sudo systemctl status whatsapp"
        else:
            texto = ""
        if not st.get("conectado"):
            return False, "programa ligado, mas o chip está DESCONECTADO: /zapconectar" + texto
        pausa = os.path.join(pasta_bot, "whatsapp_pausado")
        if os.path.exists(pausa):
            try:
                motivo = open(pausa, encoding="utf-8").read()[:120]
            except OSError:
                motivo = "?"
            return False, f"conectado, mas os posts estão PAUSADOS ({motivo}): /zapligar" + texto
        try:
            destinos = [l for l in open(os.path.join(pasta_bot, "whatsapp_destinos.txt"), encoding="utf-8")
                        if l.split("#")[0].strip()]
        except OSError:
            destinos = []
        if not destinos:
            return False, "conectado, mas sem grupo/canal para postar: /zapdestino" + texto
        return True, f"conectado ({st.get('numero')}), {len(destinos)} destino(s)" + texto
    resultados.append(_tentar("WhatsApp (posts)", whatsapp))

    # Observação dos canais (Bot B): cada canal precisa ter sido lido há pouco tempo e sem erro
    def observacao(canal, leituras):
        def conferir():
            lido = leituras.get(canal["id"])
            if not lido:
                return None, "ainda sem nenhuma leitura (esperando a 1ª)"   # None = esperando (⏳), não é erro
            if lido.get("mensagens") and time.time() - (lido.get("quando") or 0) / 1000 < LEITURA_VELHA_HORAS * 3600:
                minutos = (time.time() - lido["quando"] / 1000) / 60
                return True, f"lido há {minutos:.0f} min, {len(lido['mensagens'])} mensagens"
            if lido.get("ao_vivo") and time.time() - lido.get("ultimo_ao_vivo", 0) / 1000 < 24 * 3600:
                horas = (time.time() - lido["ultimo_ao_vivo"] / 1000) / 3600
                return True, f"recebendo ao vivo, último post há {horas:.1f} h"
            if lido.get("ao_vivo"):
                return False, "nenhum post ao vivo há mais de 24 h (o chip ainda segue o canal?)"
            if lido.get("erro"):
                return None, ("esperando o 1º post ao vivo: siga o canal no celular do chip "
                               "(o histórico não abre: " + str(lido["erro"])[:60] + ")")
            return False, f"sem leitura nova há mais de {LEITURA_VELHA_HORAS} h"
        return conferir
    # (09/11) Os canais observados valem para todos os bots (a soma das listas de bots/*/)
    try:
        import observador
        canais = observador.carregar_todos(os.path.dirname(os.path.abspath(pasta_bot)))["canais"]
    except Exception:
        canais = []
    # E os grupos dos outros afiliados em que o chip está (o programa do WhatsApp guarda o que eles postam)
    def grupos():
        caminho = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(pasta_bot))), "whatsapp",
                               "grupos_observados.json")
        dados = json.load(open(caminho, encoding="utf-8"))
        desde = time.time() - 24 * 3600
        ativos = {(g.get("nome") or j) for j, g in dados.items()
                  if any((p.get("quando") or 0) >= desde for p in g.get("posts") or [])}
        posts = sum(1 for g in dados.values() for p in g.get("posts") or [] if (p.get("quando") or 0) >= desde)
        if not ativos:
            return False, "nenhum post dos grupos dos outros nas últimas 24 h"
        return True, f"{len(ativos)} grupos, {posts} posts nas últimas 24 h ({', '.join(sorted(ativos))[:150]})"
    resultados.append(_tentar("Observando grupos", grupos))
    if canais:
        try:
            leituras = _pegar(whatsapp_url + "/canal/leituras", timeout=10).get("leituras", {})
        except Exception:
            leituras = {}
        for canal in canais:
            resultados.append(_tentar(("⭐ " if canal.get("oficial") else "") + "Observando: " + canal["nome"][:40],
                                      observacao(canal, leituras)))
    return resultados

def resumo(resultados, bot, quando=None):
    # ✅ ok | ⏳ esperando (ainda não leu, nada quebrado) | ❌ só quando deu erro de verdade (09/11, Gabriel)
    falhas = [r for r in resultados if r[0] is False]
    esperando = [r for r in resultados if r[0] is None]
    cabeca = (f"✅ <b>{html.escape(bot)}</b>: verificação geral, tudo certo" if not falhas else
              f"⚠️ <b>{html.escape(bot)}</b>: verificação geral, {len(falhas)} problema(s)")
    if esperando:
        cabeca += f", {len(esperando)} esperando"
    if quando:
        cabeca += f" ({quando})"
    icone = {True: "✅", None: "⏳", False: "❌"}
    linhas = [f"{icone.get(ok, '❌')} {html.escape(nome)}: {html.escape(detalhe)}" for ok, nome, detalhe in resultados]
    return cabeca + "\n\n" + "\n".join(linhas)
