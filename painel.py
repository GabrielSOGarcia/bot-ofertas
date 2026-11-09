# Painel de controle pelo Telegram: um bot separado (criado no BotFather) que só obedece o Gabriel.
# Liga, desliga e mostra os bots do servidor (um serviço bot-ofertas@NOME para cada pasta em bots/),
# muda ajustes sem reiniciar e recebe cupons: cole o texto do cupom e a IA salva no cupons.txt.
# Precisa no config.txt: PAINEL_TOKEN (do BotFather) e PAINEL_ADMIN (seu número de usuário: o painel
# mostra ele na primeira mensagem que você mandar). GEMINI_KEY é usada para ler os cupons.
import html, json, os, re, subprocess, time, urllib.error, urllib.parse, urllib.request
from datetime import date, timedelta
import cupons
import observador
import concorrentes
import verificacao

# ================= AJUSTES (mexa só aqui) =================
GEMINI_MODELO = "gemini-3.5-flash-lite"   # o mesmo do postar_shopee.py
LINHAS_LOG = 25                           # linhas do /log
SERVICO = "bot-ofertas@{}"                # nome do serviço de cada bot no servidor
WHATSAPP_URL = "http://127.0.0.1:3010"    # programa do WhatsApp (whatsapp/servidor.js)
CONFIG_PATH = os.environ.get("BOT_CONFIG", r"C:\bot-config\config.txt")   # senhas fora da pasta do bot
# ===========================================================

PASTA = os.path.dirname(os.path.abspath(__file__))
PASTA_BOTS = os.path.join(PASTA, "bots")
ARQUIVO_CUPONS = os.path.join(PASTA, "cupons.txt")

def ler_config(caminho=CONFIG_PATH):
    config = {}
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            if "=" in linha:
                chave, valor = linha.strip().split("=", 1)
                config[chave.strip()] = valor.strip()
    return config

cfg = ler_config()

def telegram(metodo, campos, timeout=30):
    req = urllib.request.Request(f"https://api.telegram.org/bot{cfg['PAINEL_TOKEN']}/{metodo}",
                                 data=urllib.parse.urlencode(campos).encode())
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())["result"]

def responder(chat, texto):
    # Telegram aceita até 4096 letras por mensagem: corta em pedaços se passar
    for i in range(0, len(texto), 4000):
        try:
            telegram("sendMessage", {"chat_id": chat, "text": texto[i:i + 4000], "parse_mode": "HTML",
                                     "link_preview_options": '{"is_disabled": true}'})
        except Exception as e:
            print("Não consegui responder:", type(e).__name__)

# ---------- Bots e serviços ----------

def bots():
    if not os.path.isdir(PASTA_BOTS):
        return []
    return sorted(n for n in os.listdir(PASTA_BOTS)
                  if os.path.isdir(os.path.join(PASTA_BOTS, n)) and not n.startswith(("_", ".")))

def qual_bot(args):
    # "/ligar casa" -> casa. Com um bot só, nem precisa dizer o nome.
    lista = bots()
    if args and args[0].lower() in lista:
        return args[0].lower(), args[1:]
    if len(lista) == 1:
        return lista[0], args
    raise ValueError("Qual bot? Escreva o nome depois do comando: " + ", ".join(lista))

def sistema(*comando, sudo=True):
    try:
        r = subprocess.run((["sudo", "-n"] if sudo else []) + list(comando),
                           capture_output=True, text=True, timeout=60)
        return (r.stdout + r.stderr).strip()
    except FileNotFoundError:
        return "(esse comando só funciona no servidor)"
    except subprocess.TimeoutExpired:
        return "(demorou demais para responder)"

def ligado(bot):
    return sistema("systemctl", "is-active", SERVICO.format(bot), sudo=False) == "active"

def arquivo_do_bot(bot, nome):
    return os.path.join(PASTA_BOTS, bot, nome)

def ler_status(bot):
    try:
        with open(arquivo_do_bot(bot, "status.json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}

def ler_ajustes(bot):
    ajustes = {}
    try:
        with open(arquivo_do_bot(bot, "ajustes.txt"), encoding="utf-8") as f:
            for linha in f:
                if "=" in linha:
                    chave, valor = linha.strip().split("=", 1)
                    ajustes[chave.strip()] = valor.strip()
    except FileNotFoundError:
        pass
    return ajustes

def gravar_ajustes(bot, novos):
    ajustes = dict(ler_ajustes(bot), **{k: str(v) for k, v in novos.items()})
    with open(arquivo_do_bot(bot, "ajustes.txt"), "w", encoding="utf-8") as f:
        f.write("".join(f"{k}={v}\n" for k, v in sorted(ajustes.items())))

def dois_numeros(args, minimo, maximo, nome):
    try:
        a, b = int(args[0]), int(args[1])
    except (IndexError, ValueError):
        raise ValueError(f"Mande dois números. Ex.: {nome}")
    if not (minimo <= a <= maximo and minimo <= b <= maximo):
        raise ValueError(f"Os números vão de {minimo} a {maximo}.")
    return a, b

# ---------- Comandos ----------

AJUDA = """<b>Painel dos bots</b>
(com um bot só, não precisa escrever o nome dele)

<b>Ligar e desligar</b>
/status: como estão os bots
/ligar casa | /parar casa | /reiniciar casa
/log casa: últimas linhas do que o bot fez
/postar casa: posta um produto agora

<b>Ajustes</b> (valem no próximo post, sem reiniciar)
/ajustes casa: mostra os números em uso
/intervalo casa 6 15: minutos entre posts
/pico casa 3 6: minutos entre posts no pico
/horariopico casa 18 20: horas do pico
/horario casa 8 24: posta das 8h até meia-noite
/comissao casa 6 4: mínimo de 6% ou R$ 4 por venda
/caro casa 3 4: 1 produto caro a cada 3 ou 4 posts
/caropico casa 2 3: o mesmo, no horário de pico
/desconto casa 10: desconto mínimo em %
/padrao casa: volta tudo para o padrão

<b>Cupons</b> (valem para todos os bots da Shopee)
Cole ou encaminhe o texto do cupom aqui e eu salvo.
/cupons: lista os cupons valendo
/cupom OFERTAS10 10% 49 50 11/11: código, desconto (10% ou 70 para R$ 70), compra mínima, limite, validade
/validade OFERTAS10 11/11: muda a validade
/apagar OFERTAS10: tira o cupom
/alerta: manda o alerta de cupom agora em todos os bots

<b>WhatsApp</b>
/zap: conexão, destinos e posts de hoje
/zapconectar 5511900000000: código para conectar o chip (sem número: QR Code)
/zaptrocar 5511900000000: troca para o chip RESERVA (sai do atual; os grupos continuam os mesmos)
/backup: faz o backup agora (sozinho ele faz todo dia às 4h e guarda 7 dias)
/zapgrupos: grupos do chip, com o id de cada um
/zapcanal LINK: id do canal pelo link de convite
/zapdestino casa ID | /zaptirar casa ID: onde o bot posta
/zapligar casa | /zappausar casa: liga ou pausa os posts no WhatsApp
/zapritmo casa 15 40: no máximo 15 por dia, pelo menos 40 min entre eles (999 = sem limite, modo teste)
/zapintervalo casa 8 20: cada post sai entre 8 e 20 min depois do anterior (/zapintervalo casa 5 0 desliga)
Lojas: qualquer uma. Abaixo de R$ 200: nota 4,5+ e 1000+ vendas. De R$ 200 para cima: nota 4,7+, marca e 100+ vendas.
Preferência: Oficial > Indicada > comum com marca > comum
/lojaindicada casa liga|desliga: aceita (ou não) Loja Indicada
/lojacomum casa liga|desliga: aceita (ou não) loja comum
/telegrampausar casa: o Telegram para de receber posts (só o WhatsApp, no ritmo dele)
/telegramligar casa: o Telegram volta a receber os posts
/destaque LINK: o bot posta ESSE produto na próxima vez (pode mandar vários links; campanhas da Shopee)
/destaques: mostra a fila; /tirardestaque ID: tira um
/zapzerar casa: zera a contagem de posts de hoje no WhatsApp
/zapconvite casa: manda já a mensagem "Bom dia/Boa tarde/Boa noite + link do grupo"
/postados casa 15: últimos posts e se alguma oferta repetiu (/repetidos faz o mesmo)
/verificar casa: confere tudo (servidor, Shopee, Google, Telegram, painel, WhatsApp, canais observados).
O bot faz isso sozinho todo dia ao começar a postar e manda o resultado aqui.
<b>Bot B (olha canais de outros afiliados no WhatsApp)</b>
/zapobservar LINK: passa a observar esse canal (link do tipo whatsapp.com/channel/...)
/zapoficial LINK: o canal OFICIAL da Shopee (Criadores e Afiliados): aviso aqui cada post novo, 24 h
/zapmaisvistos: os posts que mais engajam nos canais observados (visualizações e reações)
/zapobservados: lista os canais; /zapnaoobservar ID: tira um

<b>Outros grupos</b> (o chip guarda tudo que os grupos dos outros afiliados postam, com as reações)
/concorrentes 24: cada grupo nas últimas 24 h (posts, reações, ♀/♂, os mais reagidos)
/concorrentestop 7: os 15 mais reagidos de todos os grupos em 7 dias
/copiar casa 1 2: copia as ofertas dos canais e grupos observados com o NOSSO link (1 a cada 2 posts; 0 2 desliga).
O Casa pega o que é de casa, o Geral o resto. Passa pelos filtros (peça, nota, preço único, TV, medida, IA)

<b>Campanhas</b> (11.11, Black Friday, 12.12: liga sozinho; na véspera, esquenta)
/campanha casa: mostra | /campanha casa 11.11: liga já (teste) | /campanha casa desligada | /campanha casa auto"""

def cmd_status(args):
    lista = bots()
    if not lista:
        return "Nenhum bot na pasta bots/."
    texto = "<b>Bots</b>\n\n"
    for bot in lista:
        st = ler_status(bot)
        texto += f"{'🟢 ligado' if ligado(bot) else '🔴 desligado'}: <b>{html.escape(bot)}</b>\n"
        if st:
            texto += f"Posts hoje: {st.get('posts_hoje', 0)}"
            if st.get("ultimo"):
                texto += f" | último às {st.get('ultimo_em')}: {html.escape(st['ultimo'])}"
            texto += f"\nÚltima volta do bot: {st.get('visto_em', '?')}\n"
        texto += "\n"
    validos = cupons.ler(ARQUIVO_CUPONS)
    return texto + f"🎟️ Cupons valendo: {len(validos)}"

def cmd_servico(acao):
    def comando(args):
        bot, _ = qual_bot(args)
        servico = SERVICO.format(bot)
        # enable/disable: continua ligado (ou desligado) mesmo se o servidor reiniciar
        saida = sistema("systemctl", {"ligar": "enable", "parar": "disable"}.get(acao, "restart"),
                        *(["--now"] if acao != "reiniciar" else []), servico)
        time.sleep(3)
        estado = "🟢 ligado" if ligado(bot) else "🔴 desligado"
        return f"<b>{html.escape(bot)}</b>: {estado}" + (f"\n<pre>{html.escape(saida[-1500:])}</pre>" if saida else "")
    return comando

def cmd_log(args):
    bot, resto = qual_bot(args)
    linhas = min(int(resto[0]), 100) if resto and resto[0].isdigit() else LINHAS_LOG
    saida = sistema("journalctl", "-u", SERVICO.format(bot), "-n", str(linhas), "--no-pager", "-o", "cat")
    # Corta DEPOIS de escapar (as aspas viravam &#x27; e o texto passava do limite do Telegram,
    # aí a mensagem quebrava no meio do <pre> e não chegava nada) e só em fim de linha
    texto = html.escape(saida, quote=False)
    if len(texto) > 3500:
        texto = texto[-3500:].split("\n", 1)[-1]
    return f"<b>Log do {html.escape(bot)}</b>\n<pre>{texto or '(vazio)'}</pre>"

def cmd_postar(args):
    bot, _ = qual_bot(args)
    open(arquivo_do_bot(bot, "postar_agora"), "w").close()
    aviso = "" if ligado(bot) else "\n⚠️ Ele está desligado: vai postar quando ligar (/ligar)."
    return f"Pedido feito: o <b>{html.escape(bot)}</b> posta em até 10 segundos.{aviso}"

def cmd_ajustes(args):
    bot, _ = qual_bot(args)
    em_uso = ler_status(bot).get("ajustes", {})
    mudados = ler_ajustes(bot)
    if not em_uso:
        return "Ainda não tenho os números desse bot (ele precisa rodar uma vez)."
    texto = f"<b>Ajustes do {html.escape(bot)}</b> (✏️ = mudado pelo painel)\n"
    for chave, valor in em_uso.items():
        texto += f"{'✏️ ' if chave in mudados else ''}{chave} = {mudados.get(chave, valor)}\n"
    return texto

def cmd_ajuste(chaves, minimo, maximo, exemplo):
    def comando(args):
        bot, resto = qual_bot(args)
        a, b = dois_numeros(resto, minimo, maximo, exemplo)
        if chaves[0].endswith("_MIN") and a > b:
            raise ValueError("O primeiro número tem que ser menor que o segundo.")
        gravar_ajustes(bot, dict(zip(chaves, (a, b))))
        return f"✅ {html.escape(bot)}: {chaves[0]} = {a}, {chaves[1]} = {b}. Vale no próximo post."
    return comando

def cmd_zapintervalo(args):
    # (07/11) Cada post no WhatsApp sai entre MIN e MAX minutos depois do anterior (sorteado).
    # /zapintervalo casa 8 20 | /zapintervalo casa 5 0 = desliga (volta a espalhar os do dia)
    bot, resto = qual_bot(args)
    a, b = dois_numeros(resto, 0, 240, "/zapintervalo casa 8 20")
    if b == 0:
        gravar_ajustes(bot, {"WHATSAPP_INTERVALO": max(a, 1), "WHATSAPP_INTERVALO_MAX": 0})
        return (f"✅ {html.escape(bot)}: faixa desligada. Volta a espalhar os posts do dia, "
                f"com pelo menos {max(a, 1)} min entre eles.")
    if not 1 <= a < b:
        raise ValueError("O mínimo tem que ser de 1 para cima e menor que o máximo. Ex.: /zapintervalo casa 8 20")
    gravar_ajustes(bot, {"WHATSAPP_INTERVALO": a, "WHATSAPP_INTERVALO_MAX": b})
    media = (a + b) / 2
    return (f"✅ {html.escape(bot)}: no WhatsApp, cada post sai entre {a} e {b} min depois do anterior "
            f"(média {media:.0f} min, uns {int(16 * 60 / media)} posts das 8h à meia-noite). Vale a partir do próximo.")

def cmd_horario(chaves, exemplo):
    def comando(args):
        bot, resto = qual_bot(args)
        a, b = dois_numeros(resto, 0, 24, exemplo)
        if a >= b:
            raise ValueError("A hora de começar tem que ser antes da hora de parar (ex.: 8 24).")
        gravar_ajustes(bot, dict(zip(chaves, (a, b))))
        return f"✅ {html.escape(bot)}: das {a}h às {b}h. Vale no próximo post."
    return comando

def cmd_desconto(args):
    bot, resto = qual_bot(args)
    if not resto or not resto[0].isdigit() or not 0 <= int(resto[0]) <= 90:
        raise ValueError("Mande um número de 0 a 90. Ex.: /desconto casa 10")
    gravar_ajustes(bot, {"DESCONTO_MINIMO": int(resto[0])})
    return f"✅ {html.escape(bot)}: desconto mínimo {resto[0]}%. Vale no próximo post."

def cmd_padrao(args):
    bot, _ = qual_bot(args)
    try:
        os.remove(arquivo_do_bot(bot, "ajustes.txt"))
    except FileNotFoundError:
        pass
    return f"✅ {html.escape(bot)}: tudo de volta ao padrão. Vale no próximo post."

def texto_cupom(c):
    return (f"🎟️ <code>{html.escape(c['codigo'])}</code> | {html.escape(c['descricao'])} | "
            f"até {c['validade']:%d/%m}")

def salvar_novos(novos):
    lista = cupons.salvar(ARQUIVO_CUPONS, cupons.adicionar(cupons.ler(ARQUIVO_CUPONS), novos))
    texto = "✅ Salvei:\n" + "\n".join(texto_cupom(c) for c in novos)
    texto += f"\n\nCupons valendo agora: {len(lista)}. Para mandar o alerta já: /alerta"
    if any(c["validade"] == date.today() for c in novos):
        texto += "\n⏰ Os que vencem hoje: se a data estiver errada, use /validade CÓDIGO 11/11"
    return texto

def cmd_cupons(args):
    lista = cupons.salvar(ARQUIVO_CUPONS, cupons.ler(ARQUIVO_CUPONS))   # já tira os vencidos
    if not lista:
        return "Nenhum cupom valendo. Cole o texto de um cupom aqui para salvar."
    return "<b>Cupons valendo</b>\n" + "\n".join(texto_cupom(c) for c in lista)

def cmd_cupom(args):
    if len(args) < 2:
        raise ValueError("Ex.: /cupom OFERTAS10 10% 49 50 11/11 (código, desconto, mínimo, limite, validade)")
    datas = [a for a in args[2:] if "/" in a]
    numeros = [a for a in args[2:] if "/" not in a]
    c = cupons.novo(args[0], args[1], numeros[0] if numeros else None,
                    numeros[1] if len(numeros) > 1 else None, datas[0] if datas else None)
    if not c:
        raise ValueError("Não entendi. Código só com letras e números, desconto tipo 10% ou 70.")
    return salvar_novos([c])

def cmd_validade(args):
    if len(args) < 2 or not cupons.ler_data(args[1]):
        raise ValueError("Ex.: /validade OFERTAS10 11/11")
    lista = cupons.ler(ARQUIVO_CUPONS)
    achou = [c for c in lista if c["codigo"] == args[0].upper()]
    if not achou:
        raise ValueError(f"Não achei o cupom {args[0].upper()}. Veja em /cupons")
    achou[0]["validade"] = cupons.ler_data(args[1])
    cupons.salvar(ARQUIVO_CUPONS, lista)
    return "✅ " + texto_cupom(achou[0])

def cmd_apagar(args):
    if not args:
        raise ValueError("Ex.: /apagar OFERTAS10")
    lista = cupons.ler(ARQUIVO_CUPONS)
    resto = [c for c in lista if c["codigo"] != args[0].upper()]
    if len(resto) == len(lista):
        raise ValueError(f"Não achei o cupom {args[0].upper()}. Veja em /cupons")
    cupons.salvar(ARQUIVO_CUPONS, resto)
    return f"✅ Cupom {html.escape(args[0].upper())} apagado."

def cmd_alerta(args):
    if not cupons.ler(ARQUIVO_CUPONS):
        return "Nenhum cupom valendo para mandar."
    for bot in bots():
        open(arquivo_do_bot(bot, "mandar_cupons"), "w").close()
    return "✅ Os bots mandam o alerta de cupom na próxima volta (dentro do horário de postar)."

# ---------- WhatsApp (programa whatsapp/servidor.js) ----------

def zap(caminho, dados=None, timeout=30):
    corpo = json.dumps(dados).encode() if dados is not None else None
    req = urllib.request.Request(WHATSAPP_URL + caminho, data=corpo, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}")
    except (urllib.error.URLError, OSError):
        raise ValueError("O programa do WhatsApp não está rodando. No servidor: sudo systemctl start whatsapp")

# ---------- Segurança do chip: backup de todo dia (07/11) ----------
# Um .tar.gz por dia com a sessão do WhatsApp (cópia), os arquivos de cada bot (histórico, destinos,
# ajustes, contagens), os grupos/canais observados e os cupons. Fica FORA da pasta do bot (não vai para
# o GitHub) e guarda os últimos 7 dias. Tem a sessão do chip: trate como senha.
PASTA_BACKUP = os.environ.get("BOT_BACKUP", os.path.join(os.path.expanduser("~"), "backups-bot"))
BACKUP_DIAS = 7
BACKUP_HORA = 4                     # faz o do dia a partir das 4h (bots parados)
FORA_DO_BACKUP = {"node_modules", "login", "login_backup_tmp", "qr.png", "__pycache__"}

def nome_backup(dia):
    return os.path.join(PASTA_BACKUP, f"bot_{dia:%Y-%m-%d}.tar.gz")

def fazer_backup(dia=None):
    import tarfile
    dia = dia or date.today()
    os.makedirs(PASTA_BACKUP, exist_ok=True)
    destino = nome_backup(dia)
    tmp = destino + ".tmp"
    filtro = lambda info: None if os.path.basename(info.name) in FORA_DO_BACKUP else info
    with tarfile.open(tmp, "w:gz") as tar:
        for nome in ("bots", "whatsapp"):
            if os.path.isdir(os.path.join(PASTA, nome)):
                tar.add(os.path.join(PASTA, nome), arcname=nome, filter=filtro)
        for nome in os.listdir(PASTA):   # cupons, destaques e outros dados soltos (o código não precisa)
            if nome.endswith((".txt", ".json")) and os.path.isfile(os.path.join(PASTA, nome)):
                tar.add(os.path.join(PASTA, nome), arcname=nome)
    os.replace(tmp, destino)
    antigos = sorted(n for n in os.listdir(PASTA_BACKUP) if n.startswith("bot_") and n.endswith(".tar.gz"))
    for n in antigos[:-BACKUP_DIAS]:
        os.remove(os.path.join(PASTA_BACKUP, n))
    return destino

def backup_do_dia(agora=None):
    # Chamado a cada volta do painel: faz o backup de hoje uma vez, depois das 4h
    from datetime import datetime
    agora = agora or datetime.now()
    if agora.hour < BACKUP_HORA or os.path.exists(nome_backup(agora.date())):
        return None
    try:
        return fazer_backup(agora.date())
    except Exception as e:
        print("Backup falhou:", type(e).__name__, e)
        if cfg.get("PAINEL_ADMIN"):
            responder(cfg["PAINEL_ADMIN"], f"⚠️ O backup de hoje falhou ({html.escape(type(e).__name__)}). "
                                           "Tento de novo daqui a pouco; para forçar: /backup")
        return None

def ultimo_backup():
    try:
        lista = sorted(n for n in os.listdir(PASTA_BACKUP) if n.startswith("bot_") and n.endswith(".tar.gz"))
    except OSError:
        return None
    return lista[-1] if lista else None

def quando(iso):
    from datetime import datetime
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone().strftime("%d/%m %H:%M")
    except (AttributeError, ValueError):
        return "ainda não"

def texto_seguranca(st):
    ult = ultimo_backup()
    linhas = [f"🛟 Cópia da sessão: {quando(st.get('backupEm'))} | backup: "
              f"{ult[4:14] if ult else 'ainda não'} (/backup)"]
    if st.get("quedasHoje") and st.get("diaQuedas") == date.today().isoformat():
        linhas.append(f"Quedas hoje: {st['quedasHoje']}")
    if not st.get("conectado") and st.get("caiuEm"):
        linhas.append(f"Fora do ar desde {quando(st['caiuEm'])}")
    return "\n".join(linhas)

def cmd_backup(args):
    destino = fazer_backup()
    tamanho = os.path.getsize(destino) / 1e6
    nome = os.path.basename(destino)
    return (f"🛟 Backup feito: <code>{html.escape(nome)}</code> ({tamanho:.1f} MB). Guardo os últimos "
            f"{BACKUP_DIAS} dias no servidor.\n\nPara baixar no PC (fica junto do config, porque tem a sessão do chip):\n"
            f"<code>cd C:\\bot-config; mkdir -Force backups; scp -i SUA_CHAVE.key "
            f"USUARIO@IP_DO_SERVIDOR:~/backups-bot/{html.escape(nome)} backups\\</code>")

def destinos(bot):
    try:
        with open(arquivo_do_bot(bot, "whatsapp_destinos.txt"), encoding="utf-8") as f:
            return [l.strip() for l in f if l.split("#")[0].strip()]
    except FileNotFoundError:
        return []

def cmd_zap(args):
    st = zap("/status")
    if st.get("conectado"):
        texto = f"🟢 WhatsApp conectado: {html.escape(st.get('numero') or '')}\n\n"
    else:
        texto = "🔴 WhatsApp desconectado. Para conectar: /zapconectar 55DDDNÚMERO (o número do chip)\n" \
                "Chip reserva: /zaptrocar 55DDDNÚMERO\n\n"
    texto += texto_seguranca(st) + "\n\n"
    for bot in bots():
        pausa = arquivo_do_bot(bot, "whatsapp_pausado")
        try:
            with open(arquivo_do_bot(bot, "whatsapp_contagem.json"), encoding="utf-8") as f:
                cont = json.load(f)
        except (OSError, ValueError):
            cont = {}
        hoje = cont.get("posts", 0) if cont.get("dia") == date.today().isoformat() else 0
        ajustes = dict(ler_status(bot).get("ajustes", {}), **ler_ajustes(bot))
        texto += f"<b>{html.escape(bot)}</b>: {'⏸️ pausado' if os.path.exists(pausa) else '▶️ ligado'} | " \
                 f"hoje {hoje}/{ajustes.get('WHATSAPP_MAX_DIA', '?')} | " \
                 f"intervalo mín. {ajustes.get('WHATSAPP_INTERVALO', '?')} min\n"
        if os.path.exists(pausa):
            with open(pausa, encoding="utf-8") as f:
                texto += f"Motivo: {html.escape(f.read()[:300])}\n"
        lista = destinos(bot)
        texto += ("Destinos:\n" + "\n".join(f"• <code>{html.escape(d)}</code>" for d in lista)
                  if lista else "Sem destino ainda: /zapgrupos e depois /zapdestino") + "\n\n"
    return texto

def cmd_zaptrocar(args):
    # Chip reserva (07/11): sai do chip atual e pede o código do número novo. Os grupos não mudam.
    numero = re.sub(r"\D", "", "".join(args))
    if len(numero) < 12:
        raise ValueError("Mande o número do chip reserva com 55 e DDD. Ex.: /zaptrocar 5511900000000")
    r = zap("/trocar", {"numero": numero})
    if not r.get("ok"):
        raise ValueError(r.get("erro") or "O programa do WhatsApp não aceitou a troca.")
    if r.get("ja"):
        return "🟢 Esse número já é o que está conectado."
    return ("🔄 Trocando de chip. O código do chip novo chega aqui em alguns segundos: no celular do RESERVA, "
            "WhatsApp → ⋮ → Aparelhos conectados → Conectar aparelho → Conectar com número de telefone.\n\n"
            "Depois: confira se o número novo é administrador nos dois grupos (/zapgrupos) e mande "
            "/zapligar casa e /zapligar geral se estiverem pausados.")

def cmd_zapconectar(args):
    numero = re.sub(r"\D", "", "".join(args))
    r = zap("/conectar", {"numero": numero or None})
    if r.get("ja"):
        return f"🟢 Já está conectado ({html.escape(r.get('numero') or '')})."
    if numero:
        return "⏳ Pedindo o código de conexão... chega aqui em alguns segundos."
    return "⏳ O QR Code chega aqui em alguns segundos (abra no PC e escaneie com o celular do chip)."

def cmd_zapgrupos(args):
    grupos = zap("/grupos")
    if isinstance(grupos, dict):
        raise ValueError(grupos.get("erro") or "Não consegui ler os grupos.")
    if not grupos:
        return "O chip não está em nenhum grupo. Adicione o número do chip no grupo (como administrador)."
    return "<b>Grupos do chip</b> (toque no id para copiar)\n\n" + "\n".join(
        f"{html.escape(g['nome'] or '?')} ({g['pessoas']} pessoas)\n<code>{html.escape(g['id'])}</code>"
        for g in grupos) + "\n\nPara postar num grupo: /zapdestino casa ID"

# ---------- Concorrentes: o que os outros grupos de ofertas postam (06/11, concorrentes.py) ----------

def _grupos_observados(horas):
    r = zap(f"/grupos/observados?horas={horas}", timeout=60)
    if not r.get("ok"):
        raise ValueError(r.get("erro") or "não consegui ler os grupos observados")
    return r["grupos"]

def cmd_concorrentes(args):
    # /concorrentes [horas]: cada grupo, quanto postou, o que mais reagiu e a proporção mulher/homem
    horas = int(args[0]) if args and args[0].isdigit() else 24
    grupos = _grupos_observados(horas)
    if not grupos:
        return ("Ainda não guardei nada. O chip precisa estar nos grupos dos outros afiliados; o que eles "
                "postarem a partir de agora fica guardado.")
    blocos = []
    for g in sorted(grupos.values(), key=lambda g: -len(g["posts"])):
        posts = g["posts"]
        if not posts:
            continue
        pub = [concorrentes.publico(p["texto"]) for p in posts]
        reacoes = sum(p["reacoes"] for p in posts)
        top = sorted(posts, key=lambda p: -p["reacoes"])[:3]
        linhas = "\n".join(f"  {concorrentes.publico(p['texto']) or '•'} {html.escape(concorrentes.titulo(p['texto'])[:60])}"
                           f" {html.escape(concorrentes.preco_final(p))} ❤️{p['reacoes']}" for p in top)
        blocos.append(f"<b>{html.escape(g['nome'] or '?')}</b>: {len(posts)} posts, {reacoes} reações, "
                      f"{sum(1 for x in pub if x == '♀')} ♀ / {sum(1 for x in pub if x == '♂')} ♂ "
                      f"(guardados no total: {g['total_guardado']})\n{linhas}")
    return (f"<b>Outros grupos (últimas {horas} h)</b>\n\n" + "\n\n".join(blocos or ["Nada nesse período."])
            + "\n\nMais reagidos de todos: /concorrentestop 7")

def cmd_concorrentestop(args):
    # /concorrentestop [dias]: os 15 posts com mais reações somando todos os grupos
    dias = int(args[0]) if args and args[0].isdigit() else 7
    todos = [(p, g["nome"]) for g in _grupos_observados(dias * 24).values() for p in g["posts"]]
    todos.sort(key=lambda x: -x[0]["reacoes"])
    if not todos:
        return "Ainda não guardei nada dos outros grupos."
    linhas = []
    for i, (p, nome) in enumerate(todos[:15], 1):
        emojis = " ".join(f"{e}{n}" for e, n in sorted(p["emojis"].items(), key=lambda x: -x[1])[:3])
        linhas.append(f"{i}. {concorrentes.publico(p['texto']) or '•'} <b>{html.escape(concorrentes.titulo(p['texto'])[:65])}</b>"
                      f" {html.escape(concorrentes.preco_final(p))}\n   {emojis or 'sem reação'} | {html.escape(nome or '?')}")
    return f"<b>Mais reagidos nos outros grupos ({dias} dias)</b>\n♀ mulher, ♂ homem, • geral\n\n" + "\n".join(linhas)

def cmd_zapcanal(args):
    if not args:
        raise ValueError("Mande o link do canal. Ex.: /zapcanal https://whatsapp.com/channel/XXXX")
    if "chat.whatsapp.com" in args[0]:
        raise ValueError("Esse link é de GRUPO (chat.whatsapp.com), não de canal. Para grupo: coloque o "
                         "chip no grupo como admin e mande /zapgrupos para pegar o ID. Link de canal "
                         "é whatsapp.com/channel/...")
    r = zap(f"/canal?convite={urllib.parse.quote(args[0].rstrip('/').split('/')[-1])}")
    if not r.get("id"):
        raise ValueError(r.get("erro") or "Não achei o canal por esse link.")
    return f"Canal: {html.escape(r.get('nome') or '?')}\n<code>{html.escape(r['id'])}</code>\n\n" \
           f"Para postar nele: /zapdestino casa {html.escape(r['id'])}"

# ---------- Bot B: observa canais de outros afiliados no WhatsApp (observador.py) ----------

def _canais(bot):
    caminho = arquivo_do_bot(bot, observador.ARQUIVO)
    return caminho, observador.carregar(caminho)

def _ler_canal(canal, quantas=50):
    # canal = {"id": ..., "convite": ...}: o servidor tenta pelo id (seguindo o canal) e pelo convite
    caminho = f"/canal/mensagens?jid={urllib.parse.quote(canal['id'])}&qtd={quantas}"
    if canal.get("convite"):
        caminho += f"&convite={urllib.parse.quote(canal['convite'])}"
    r = zap(caminho, timeout=120)
    if not r.get("ok"):
        raise ValueError(r.get("erro") or "não consegui ler o canal")
    return r

def _leituras():
    # O programa do WhatsApp lê todos os canais sozinho a cada ~20 min (24 h por dia) e guarda aqui
    try:
        r = zap("/canal/leituras")
        return r.get("leituras", {}) if r.get("ok") else {}
    except ValueError:
        return {}

def _mensagens_do_canal(canal):
    # Usa a leitura automática se for recente (menos de 3 h); senão lê na hora
    lido = _leituras().get(canal["id"], {})
    if lido.get("mensagens") and time.time() - (lido.get("quando") or 0) / 1000 < 3 * 3600:
        return lido["mensagens"]
    if lido.get("ao_vivo"):                    # posts recebidos ao vivo (canal seguido pelo chip)
        return lido["ao_vivo"]
    return _ler_canal(canal)["mensagens"]

def _cmd_observar(oficial):
    def comando(args):
        bot, resto = qual_bot(args)
        if not resto:
            raise ValueError("Mande o link do canal. Ex.: /zapobservar https://whatsapp.com/channel/XXXX")
        convite = resto[0].rstrip('/').split('/')[-1]
        r = zap(f"/canal?convite={urllib.parse.quote(convite)}")
        if not r.get("id"):
            raise ValueError(r.get("erro") or "Não achei o canal por esse link.")
        caminho, dados = _canais(bot)
        novo = observador.adicionar_canal(dados, r["id"], r.get("nome"), convite, oficial)
        observador.salvar(caminho, dados)
        nome = html.escape(r.get("nome") or "?")
        try:
            lidas = _ler_canal({"id": r["id"], "convite": convite}, 20)["mensagens"]
            teste = f"Li {len(lidas)} mensagens, {sum(1 for m in lidas if m['views'])} com visualizações."
            if lidas and not any(m["views"] for m in lidas):
                teste += " (sem visualizações: pode ser preciso seguir o canal)"
        except ValueError as e:
            teste = f"Salvei, mas não consegui ler as mensagens agora: {html.escape(str(e))}"
        papel = ("⭐ Canal OFICIAL da Shopee: aviso aqui cada post novo dele, 24 h por dia.\n"
                 if oficial else "Leio ele sozinho a cada ~20 min, 24 h por dia.\n")
        return (f"👀 {'Passei a observar' if novo else 'Já observava'}: <b>{nome}</b>\n{teste}\n{papel}"
                f"\nVeja o que mais engaja: /zapmaisvistos")
    return comando

cmd_zapobservar = _cmd_observar(False)
cmd_zapoficial = _cmd_observar(True)

def cmd_zapobservados(args):
    bot, _ = qual_bot(args)
    _, dados = _canais(bot)
    if not dados["canais"]:
        return "Nenhum canal observado ainda. Mande /zapobservar LINK_DO_CANAL"
    leituras = _leituras()
    linhas = []
    for c in dados["canais"]:
        lido = leituras.get(c["id"], {})
        if lido.get("ao_vivo"):
            horas = (time.time() - lido.get("ultimo_ao_vivo", 0) / 1000) / 3600
            estado = f"📡 ao vivo: {len(lido['ao_vivo'])} posts recebidos, o último há {horas:.1f} h"
        elif lido.get("mensagens"):
            minutos = int((time.time() - (lido.get("quando") or 0) / 1000) / 60)
            estado = f"lido há {minutos} min, {len(lido['mensagens'])} mensagens"
        elif lido.get("erro"):
            estado = ("esperando o 1º post ao vivo. Siga o canal no celular do chip (abra o link e toque "
                      "em Seguir). Histórico: " + html.escape(str(lido["erro"])[:100]))
        else:
            estado = "ainda não lido (a 1ª leitura sai em até uns 20 min)"
        linhas.append(f"• {'⭐ ' if c.get('oficial') else ''}{html.escape(c['nome'])}\n"
                      f"  {estado}\n  <code>{html.escape(c['id'])}</code>")
    return "<b>Canais que o Bot B observa (24 h)</b>\n" + "\n".join(linhas) + "\n\nPara tirar: /zapnaoobservar ID"

def cmd_zapnaoobservar(args):
    bot, resto = qual_bot(args)
    caminho, dados = _canais(bot)
    if not resto or not observador.tirar_canal(dados, resto[0]):
        raise ValueError("Não achei esse id. Veja /zapobservados")
    observador.salvar(caminho, dados)
    return "✅ Tirei da observação."

def cmd_zapmaisvistos(args):
    if any("whatsapp.com/channel" in a for a in args):     # mandou um link aqui: é para observar esse canal
        return cmd_zapobservar(args)
    bot, _ = qual_bot(args)
    _, dados = _canais(bot)
    if not dados["canais"]:
        return "Nenhum canal observado ainda. Mande /zapobservar LINK_DO_CANAL"
    todos, avisos = [], []
    for c in dados["canais"]:
        try:
            todos += observador.ranquear(_mensagens_do_canal(c), c["nome"])
        except ValueError as e:
            avisos.append(f"{html.escape(c['nome'])}: {html.escape(str(e))}")
    top = observador.melhores(todos, 10)
    if not top:
        return "Não achei posts de oferta com visualizações." + ("\n" + "\n".join(avisos) if avisos else "")
    linhas = []
    for i, r in enumerate(top, 1):
        linhas.append(f"{i}. <b>{html.escape(r['titulo'][:70])}</b>"
                      + (f" | R$ {r['preco']}" if r["preco"] else "")
                      + f"\n   👁 {r['views']} | ❤️ {r['reacoes']} | nota {r['nota']}x a média "
                        f"({html.escape(', '.join(sorted(r['canais'])))})")
    return ("<b>O que mais engaja nos canais observados</b>\n(nota = visualizações ÷ média do canal)\n\n"
            + "\n".join(linhas) + ("\n\n" + "\n".join(avisos) if avisos else ""))

# ---------- Destaques: produto exato para o bot postar (destaques.txt na pasta do bot) ----------

def ids_do_link(link):
    # shopee.com.br/product/SHOP/ITEM, ...-i.SHOP.ITEM e link curto (s.shopee.com.br, shope.ee: abre e vê aonde leva)
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

def _destaques(bot):
    caminho = arquivo_do_bot(bot, "destaques.txt")
    try:
        with open(caminho, encoding="utf-8") as f:
            return caminho, [l.rstrip("\n").split("\t") for l in f if l.count("\t") >= 2]
    except FileNotFoundError:
        return caminho, []

def cmd_destaque(args):
    bot, resto = qual_bot(args)
    links = [a for a in resto if "shopee" in a or "shope.ee" in a]
    if not links:
        raise ValueError("Mande o link do produto. Ex.: /destaque https://shopee.com.br/product/1648122739/22699055699 "
                         "(pode mandar vários links de uma vez)")
    caminho, fila = _destaques(bot)
    na_fila = {d[0] for d in fila}
    entraram, falharam = 0, []
    for link in links:
        ids = ids_do_link(link)
        if not ids:
            falharam.append(link)
            continue
        loja, item = ids
        if item not in na_fila:
            fila.append([item, loja, link])
            na_fila.add(item)
            entraram += 1
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("".join("\t".join(d) + "\n" for d in fila))
    texto = (f"⭐ {html.escape(bot)}: {entraram} produto(s) na fila de destaque ({len(fila)} no total). "
             "Saem na frente da busca normal, um por vez de WhatsApp.")
    if falharam:
        texto += "\nNão entendi estes links (mande o link completo shopee.com.br/product/...):\n" + \
                 "\n".join(html.escape(l) for l in falharam)
    return texto

def cmd_destaques(args):
    bot, _ = qual_bot(args)
    _, fila = _destaques(bot)
    if not fila:
        return "Fila de destaque vazia. Para colocar: /destaque LINK"
    return "<b>Fila de destaque</b> (sai nesta ordem)\n" + "\n".join(
        f"{i}. <code>{html.escape(d[0])}</code> {html.escape(d[2][:80])}" for i, d in enumerate(fila, 1)) + \
        "\n\nPara tirar: /tirardestaque ID"

def cmd_campanha(args):
    # /campanha casa: mostra | /campanha casa 11.11: liga agora (teste) | desligada: não liga nem na data | auto
    bot, resto = qual_bot(args)
    caminho = arquivo_do_bot(bot, "campanha")
    if resto:
        valor = " ".join(resto).strip()
        if valor.lower() == "auto":
            if os.path.exists(caminho):
                os.remove(caminho)
            feito = "volta para as datas (11.11, Black Friday, 12.12)."
        else:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write("desligada" if valor.lower() == "desligada" else valor.upper())
            feito = ("desligada (não liga nem nas datas)." if valor.lower() == "desligada"
                     else f"<b>{html.escape(valor.upper())}</b> ligada AGORA (selo nos posts, mais posts e caros). "
                          f"Para voltar ao normal: /campanha {html.escape(bot)} auto")
        return f"✅ {html.escape(bot)}: campanha {feito} Vale na próxima rodada."
    try:
        with open(caminho, encoding="utf-8") as f:
            manual = f.read().strip()
    except OSError:
        manual = ""
    agora = ler_status(bot).get("campanha")
    return (f"<b>Campanha do {html.escape(bot)}</b>\nAgora: {html.escape(agora or 'nenhuma')}\n"
            f"Modo: {'manual (' + html.escape(manual) + ')' if manual else 'automático pelas datas'}\n\n"
            "Datas: 11.11, Black Friday (sexta a segunda) e 12.12. Na véspera, esquenta (aviso no grupo).\n"
            "No dia: 30% mais posts, caro a cada 2-3, cupom a cada 10-15 e selo 🛍️ nos posts.\n"
            f"/campanha {html.escape(bot)} 11.11 (liga já) | desligada | auto")

def cmd_zapconvite(args):
    # Pede ao bot a mensagem "Bom dia/Boa tarde/Boa noite + link do grupo" agora (sai em até 10 s)
    bot, _ = qual_bot(args)
    open(arquivo_do_bot(bot, "mandar_grupos"), "w").close()
    aviso = "" if ligado(bot) else "\n⚠️ Ele está desligado: manda quando ligar (/ligar)."
    return f"Pedido feito: o <b>{html.escape(bot)}</b> manda a mensagem do grupo em até 10 segundos.{aviso}"

def cmd_zapzerar(args):
    # Zera a contagem de posts de hoje no WhatsApp (ex.: o modo teste já gastou o máximo do dia)
    bot, _ = qual_bot(args)
    caminho = arquivo_do_bot(bot, "whatsapp_contagem.json")
    try:
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
    except (OSError, ValueError):
        dados = {}
    antes = dados.get("posts", 0)
    dados.update(dia=date.today().isoformat(), posts=0)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f)
    return f"✅ {html.escape(bot)}: contagem de hoje zerada ({antes} → 0). O máximo do dia vale do zero a partir de agora."

def cmd_postados(args):
    # Últimos posts e se algo repetiu: mesmo item (postados.txt) ou mesmo nome (historico.txt)
    bot, resto = qual_bot(args)
    quantos = min(int(resto[0]), 50) if resto and resto[0].isdigit() else 15
    def ler(nome):
        try:
            with open(arquivo_do_bot(bot, nome), encoding="utf-8") as f:
                return [l.rstrip("\n") for l in f if l.strip()]
        except FileNotFoundError:
            return []
    ids, hist = ler("postados.txt"), ler("historico.txt")
    nomes = [l.split("\t", 1)[-1] for l in hist]
    chave = lambda n: " ".join(n.lower().split())
    ids_rep = sorted({i for i in ids if ids.count(i) > 1})
    nomes_rep = list({chave(n): n for n in nomes if sum(chave(x) == chave(n) for x in nomes) > 1}.values())
    linhas = [f"<b>Últimos {min(quantos, len(nomes))} posts do {html.escape(bot)}</b> "
              f"(total: {len(nomes)} posts, {len(set(ids))} itens diferentes)"]
    linhas += [f"{i}. {html.escape(n[:70])}" for i, n in enumerate(nomes[-quantos:][::-1], 1)]
    if not ids_rep and not nomes_rep:
        linhas.append("\n✅ Nenhuma oferta repetida.")
    else:
        linhas.append("\n⚠️ <b>Repetidos</b>")
        linhas += [f"• mesmo item {html.escape(i)} ({ids.count(i)}x)" for i in ids_rep]
        linhas += [f"• {html.escape(n[:70])} ({sum(chave(x) == chave(n) for x in nomes)}x)" for n in nomes_rep]
    return "\n".join(linhas)

def cmd_tirardestaque(args):
    bot, resto = qual_bot(args)
    caminho, fila = _destaques(bot)
    sobra = [d for d in fila if not resto or d[0] != resto[0]]
    if not resto or len(sobra) == len(fila):
        raise ValueError("Mande o ID que aparece em /destaques")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("".join("\t".join(d) + "\n" for d in sobra))
    return "✅ Tirei da fila de destaque."

def cmd_loja_comum(args):
    bot, resto = qual_bot(args)
    if not resto or resto[0].lower() not in ("liga", "desliga"):
        raise ValueError("Use: /lojacomum casa liga (aceita loja comum, com a régua de nota e vendas) "
                         "ou /lojacomum casa desliga (só Oficial e Indicada)")
    liga = resto[0].lower() == "liga"
    gravar_ajustes(bot, {"LOJA_COMUM_MARCA": 1 if liga else 0})
    return (f"✅ {html.escape(bot)}: loja comum " +
            ("aceita (com a régua de nota e vendas, depois da Oficial e da Indicada)."
             if liga else "não é mais aceita (só Oficial e Indicada).") + " Vale no próximo post.")

def cmd_loja_indicada(args):
    bot, resto = qual_bot(args)
    if not resto or resto[0].lower() not in ("liga", "desliga"):
        raise ValueError("Use: /lojaindicada casa liga (aceita Loja Indicada nota 4,8+ e 1000+ vendas) "
                         "ou /lojaindicada casa desliga (só Loja Oficial)")
    liga = resto[0].lower() == "liga"
    gravar_ajustes(bot, {"LOJA_INDICADA": 1 if liga else 0})
    return (f"✅ {html.escape(bot)}: " + ("aceita Loja Indicada (com a régua de nota e vendas, depois da Oficial)."
                                          if liga else "só Loja Oficial.") + " Vale no próximo post.")

def cmd_verificar(args):
    bot, _ = qual_bot(args)
    resultados = verificacao.verificar(cfg, os.path.join(PASTA_BOTS, bot), WHATSAPP_URL)
    return verificacao.resumo(resultados, bot, time.strftime("%d/%m %H:%M"))

def cmd_zapdestino(adicionar):
    def comando(args):
        bot, resto = qual_bot(args)
        if not resto or not re.fullmatch(r"[\w.-]+@(g\.us|newsletter)", resto[0]):
            raise ValueError("Mande o id do grupo (termina em @g.us) ou do canal (@newsletter). Veja /zapgrupos")
        lista = [d for d in destinos(bot) if d.split("#")[0].strip() != resto[0]]
        if adicionar:
            lista.append(resto[0])
        with open(arquivo_do_bot(bot, "whatsapp_destinos.txt"), "w", encoding="utf-8") as f:
            f.write("".join(d + "\n" for d in lista))
        return f"✅ {html.escape(bot)}: {'vai postar' if adicionar else 'não posta mais'} em " \
               f"<code>{html.escape(resto[0])}</code>. Veja em /zap"
    return comando

def cmd_zappausa(pausar):
    def comando(args):
        bot, _ = qual_bot(args)
        pausa = arquivo_do_bot(bot, "whatsapp_pausado")
        if pausar:
            with open(pausa, "w", encoding="utf-8") as f:
                f.write("pausado pelo painel")
            return f"⏸️ {html.escape(bot)}: WhatsApp pausado (o Telegram continua)."
        if os.path.exists(pausa):
            os.remove(pausa)
        return f"▶️ {html.escape(bot)}: WhatsApp ligado. Sai no próximo post que for a vez dele."
    return comando

def cmd_telegram_postar(ligar):
    def comando(args):
        bot, _ = qual_bot(args)
        gravar_ajustes(bot, {"TELEGRAM_POSTAR": 1 if ligar else 0})
        if ligar:
            return (f"▶️ {html.escape(bot)}: o Telegram volta a receber os posts (junto com o WhatsApp). "
                    f"Vale no próximo post.")
        return (f"⏸️ {html.escape(bot)}: o Telegram não recebe mais posts. Só o WhatsApp, no ritmo dele "
                f"(/zapritmo). Para voltar: /telegramligar {html.escape(bot)}")
    return comando

COMANDOS = {
    "/zapobservar": cmd_zapobservar, "/zapobservados": cmd_zapobservados,
    "/verificar": cmd_verificar,
    "/zapoficial": cmd_zapoficial, "/zapofc": cmd_zapoficial,
    "/zapnaoobservar": cmd_zapnaoobservar, "/zapmaisvistos": cmd_zapmaisvistos,
    "/telegramligar": cmd_telegram_postar(True), "/telegrampausar": cmd_telegram_postar(False),
    "/start": lambda a: AJUDA, "/ajuda": lambda a: AJUDA, "/status": cmd_status,
    "/ligar": cmd_servico("ligar"), "/parar": cmd_servico("parar"), "/reiniciar": cmd_servico("reiniciar"),
    "/log": cmd_log, "/postar": cmd_postar, "/ajustes": cmd_ajustes,
    "/intervalo": cmd_ajuste(["INTERVALO_MIN", "INTERVALO_MAX"], 1, 240, "/intervalo casa 6 15"),
    "/pico": cmd_ajuste(["PICO_MIN", "PICO_MAX"], 1, 240, "/pico casa 3 6"),
    "/horariopico": cmd_horario(["PICO_INICIO", "PICO_FIM"], "/horariopico casa 18 20"),
    "/horario": cmd_horario(["HORA_INICIO", "HORA_FIM"], "/horario casa 8 24"),
    "/comissao": cmd_ajuste(["COMISSAO_MINIMA", "VALOR_COMISSAO_MINIMO"], 0, 100, "/comissao casa 6 4"),
    "/caro": cmd_ajuste(["CARO_A_CADA_MIN", "CARO_A_CADA_MAX"], 1, 20, "/caro casa 3 4"),
    "/caropico": cmd_ajuste(["CARO_PICO_MIN", "CARO_PICO_MAX"], 1, 20, "/caropico casa 2 3"),
    "/desconto": cmd_desconto, "/padrao": cmd_padrao,
    "/cupons": cmd_cupons, "/cupom": cmd_cupom, "/validade": cmd_validade, "/apagar": cmd_apagar,
    "/alerta": cmd_alerta,
    "/zap": cmd_zap, "/zapconectar": cmd_zapconectar, "/zapgrupos": cmd_zapgrupos, "/zapcanal": cmd_zapcanal,
    "/zaptrocar": cmd_zaptrocar, "/backup": cmd_backup,
    "/zapdestino": cmd_zapdestino(True), "/zaptirar": cmd_zapdestino(False),
    "/zapligar": cmd_zappausa(False), "/zappausar": cmd_zappausa(True),
    "/zapritmo": cmd_ajuste(["WHATSAPP_MAX_DIA", "WHATSAPP_INTERVALO"], 1, 999, "/zapritmo casa 15 40"),
    "/zapintervalo": cmd_zapintervalo,
    "/lojaindicada": cmd_loja_indicada, "/lojacomum": cmd_loja_comum,
    "/zapzerar": cmd_zapzerar, "/zapconvite": cmd_zapconvite,
    "/concorrentes": cmd_concorrentes, "/concorrentestop": cmd_concorrentestop,
    "/campanha": cmd_campanha,
    "/copiar": cmd_ajuste(["COPIAR_OFERTAS", "COPIADOS_A_CADA"], 0, 10, "/copiar casa 1 2 (1 = liga, 1 copiada a cada 2 posts; 0 2 = desliga)"),
    "/postados": cmd_postados, "/repetidos": cmd_postados,
    "/destaque": cmd_destaque, "/destaques": cmd_destaques, "/tirardestaque": cmd_tirardestaque,
}

# ---------- Cupom colado: a IA lê o texto ----------

def chamar_gemini(pedido):
    chave = cfg.get("GEMINI_KEY")
    if not chave:
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODELO}:generateContent"
    corpo = json.dumps({"contents": [{"parts": [{"text": pedido}]}],
                        "generationConfig": {"temperature": 0, "responseMimeType": "application/json"}}).encode()
    req = urllib.request.Request(url, data=corpo, method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": chave})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("IA indisponível:", type(e).__name__)
        return None

def ler_cupons_do_texto(texto):
    hoje = date.today()
    pedido = (
        "Extraia os cupons de desconto da Shopee deste texto (post do canal de afiliados da Shopee). "
        f"Hoje é {hoje:%d/%m/%Y}. Só códigos que a pessoa digita no carrinho; ignore links e campanhas "
        "sem código. Responda só em JSON, assim: {\"cupons\": [{\"codigo\": \"OFERTAS10\", "
        "\"tipo\": \"porcentagem\" ou \"reais\", \"valor\": 10, \"minimo\": 49 (compra mínima em R$, 0 se "
        "não tiver), \"limite\": 50 (desconto máximo em R$, ou null), \"validade\": \"dd/mm/aaaa\" "
        "(ou \"\" se o texto não disser), \"descricao\": \"resumo curto, ex.: 10% OFF acima de R$ 49, "
        "limitado a R$ 50\"}]}\n\nTexto:\n" + texto[:4000])
    resposta = chamar_gemini(pedido)
    if not resposta:
        return None
    try:
        dados = json.loads(resposta.strip().strip("`").removeprefix("json").strip())
    except ValueError:
        return None
    achados = []
    for item in dados.get("cupons") or []:
        if not isinstance(item, dict):
            continue
        valor = item.get("valor")
        desconto = f"{valor}%" if item.get("tipo") == "porcentagem" else str(valor)
        validade = cupons.ler_data(item.get("validade") or "", hoje)
        if validade and validade > hoje + timedelta(days=60):   # data estranha: vale só hoje
            validade = None
        c = cupons.novo(item.get("codigo"), desconto, item.get("minimo"), item.get("limite"),
                        validade or hoje, item.get("descricao"))
        # O código tem que estar no texto de verdade (a IA não pode inventar)
        if c and c["codigo"] in texto.upper():
            achados.append(c)
    return achados

def cupom_colado(texto):
    if not cfg.get("GEMINI_KEY"):
        return "Sem GEMINI_KEY no config.txt não consigo ler o texto. Use /cupom OFERTAS10 10% 49 50 11/11"
    achados = ler_cupons_do_texto(texto)
    if achados is None:
        return "A IA não respondeu agora. Tente de novo daqui a pouco ou use /cupom OFERTAS10 10% 49 50 11/11"
    if not achados:
        return "Não achei código de cupom nesse texto. Se tiver, use /cupom OFERTAS10 10% 49 50 11/11"
    return salvar_novos(achados)

# ---------- Loop principal ----------

def tratar(msg):
    usuario = str((msg.get("from") or {}).get("id", ""))
    chat = msg["chat"]["id"]
    if not cfg.get("PAINEL_ADMIN"):
        # Primeiro uso: mostra o número para o Gabriel colocar no config.txt (não obedece ninguém ainda)
        responder(chat, f"Seu número de usuário é <code>{usuario}</code>. Coloque a linha "
                        f"PAINEL_ADMIN={usuario} no config.txt e reinicie o painel.")
        return
    if usuario != cfg["PAINEL_ADMIN"] or msg["chat"].get("type") != "private":
        return   # qualquer outra pessoa: ignora em silêncio
    texto = (msg.get("text") or msg.get("caption") or "").strip()
    if not texto:
        return
    if texto.startswith("/"):
        partes = texto.split()
        comando = partes[0].split("@")[0].lower()
        funcao = COMANDOS.get(comando)
        if not funcao:
            responder(chat, "Não conheço esse comando. Veja a lista em /ajuda")
            return
        try:
            resposta = funcao(partes[1:])
        except ValueError as e:
            resposta = f"⚠️ {html.escape(str(e))}"
        except Exception as e:
            resposta = f"⚠️ Deu erro: {html.escape(type(e).__name__)}"
            print("Erro no comando", comando, ":", repr(e))
        responder(chat, resposta)
    else:
        responder(chat, "Lendo o cupom...")
        responder(chat, cupom_colado(texto))

def main():
    # Pula as mensagens que chegaram com o painel desligado (não executa /parar velho de novo)
    offset = None
    try:
        antigas = telegram("getUpdates", {"offset": -1, "timeout": 0})
        if antigas:
            offset = antigas[-1]["update_id"] + 1
    except Exception as e:
        print("Telegram não respondeu no começo:", type(e).__name__)
    if cfg.get("PAINEL_ADMIN"):
        responder(cfg["PAINEL_ADMIN"], "🟢 Painel ligado. Mande /status ou /ajuda")
    print("Painel rodando. Para parar: Ctrl+C")
    while True:
        try:
            campos = {"timeout": 50, "allowed_updates": '["message"]'}
            if offset:
                campos["offset"] = offset
            for update in telegram("getUpdates", campos, timeout=70):
                offset = update["update_id"] + 1
                if "message" in update:
                    tratar(update["message"])
            backup_do_dia()
        except urllib.error.HTTPError as e:
            print("Telegram recusou:", e.code)
            time.sleep(30 if e.code != 409 else 60)   # 409 = outro painel rodando com o mesmo token
        except Exception as e:
            print("Falha falando com o Telegram:", type(e).__name__)
            time.sleep(10)

if __name__ == "__main__":
    main()
