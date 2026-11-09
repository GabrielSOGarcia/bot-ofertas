// Conexão com o WhatsApp do chip (Baileys, igual a um WhatsApp Web ligado 24h).
// O postar_shopee.py manda os posts para cá (só por dentro do servidor, porta 3010) e
// este programa entrega no grupo/canal. O painel do Telegram pede o código de conexão.
//
//   GET  /status                  conectado? número? (o painel e o bot olham aqui)
//   POST /conectar  {numero}      pede o código para "Conectar com número de telefone"
//   POST /trocar    {numero}      (07/11) chip reserva: sai do chip atual e pede o código do novo
//   GET  /grupos                  grupos em que o chip está (para achar o id do grupo)
//   GET  /canal?convite=CODIGO    id do canal a partir do link de convite
//   GET  /canal/mensagens?jid=ID&qtd=40   (Bot B) últimas mensagens de um canal: views, reações, texto
//   POST /canal/seguir {jid}              segue um canal (alguns só mostram as mensagens a quem segue)
//   POST /enviar    {destinos, texto, imagem (base64)}
//   GET  /grupos/observados?horas=24      (06/11) o que os OUTROS grupos postaram, com reações
const http = require("http");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const pino = require("pino");
const QRCode = require("qrcode");
const {
  default: makeWASocket, useMultiFileAuthState, DisconnectReason, fetchLatestBaileysVersion, Browsers,
} = require("@whiskeysockets/baileys");

// ================= AJUSTES =================
const PORTA = 3010;
const PASTA_LOGIN = path.join(__dirname, "login");   // a "sessão" do WhatsApp (não apague: desconecta)
const ARQUIVO_QR = path.join(__dirname, "qr.png");
// ===========================================

const CONFIG_PATH = process.env.BOT_CONFIG || "C:\\bot-config\\config.txt";

function lerConfig() {
  const cfg = {};
  for (const linha of fs.readFileSync(CONFIG_PATH, "utf-8").split(/\r?\n/)) {
    const i = linha.indexOf("=");
    if (i > 0) cfg[linha.slice(0, i).trim()] = linha.slice(i + 1).trim();
  }
  return cfg;
}
const cfg = lerConfig();

// Aviso no painel do Telegram (o mesmo bot do painel, só para o Gabriel)
async function avisar(texto) {
  if (!cfg.PAINEL_TOKEN || !cfg.PAINEL_ADMIN) return;
  try {
    await fetch(`https://api.telegram.org/bot${cfg.PAINEL_TOKEN}/sendMessage`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: cfg.PAINEL_ADMIN, text: texto, parse_mode: "HTML" }),
    });
  } catch (e) {
    console.log("Não consegui avisar no painel:", e.message);
  }
}

async function mandarFotoNoPainel(buffer, legenda) {
  if (!cfg.PAINEL_TOKEN || !cfg.PAINEL_ADMIN) return;
  try {
    const form = new FormData();
    form.append("chat_id", cfg.PAINEL_ADMIN);
    form.append("caption", legenda);
    form.append("photo", new Blob([buffer], { type: "image/png" }), "qr.png");
    await fetch(`https://api.telegram.org/bot${cfg.PAINEL_TOKEN}/sendPhoto`, { method: "POST", body: form });
  } catch (e) {
    console.log("Não consegui mandar o QR no painel:", e.message);
  }
}

let sock = null;
const estado = { conectado: false, numero: null, deslogado: false, desde: null, erro: null,
                 caiuEm: null, quedasHoje: 0, diaQuedas: null, backupEm: null };
let pedidoConexao = null;   // { numero, ate } enquanto o Gabriel está conectando pelo painel
let qrAvisados = 0;
let trocando = false;       // /zaptrocar: saindo do chip atual de propósito (não é "desconectado pelo celular")
let avisouQueda = false;

// ---------- Segurança do chip (07/11) ----------
// Cópia da sessão (pasta login) a cada 6 h enquanto conectado. Se o servidor desligar no meio de uma
// gravação e o creds.json estragar, volta da cópia sozinho em vez de pedir conexão nova.
const PASTA_LOGIN_BACKUP = path.join(__dirname, "login_backup");
const MINUTOS_PARA_AVISAR_QUEDA = 10;

function credsBoas(pasta) {
  try {
    const c = JSON.parse(fs.readFileSync(path.join(pasta, "creds.json"), "utf-8"));
    return !!(c && c.me && c.noiseKey);
  } catch (e) {
    return false;
  }
}

function salvarSessao() {
  if (!estado.conectado || !credsBoas(PASTA_LOGIN)) return;
  const tmp = PASTA_LOGIN_BACKUP + "_tmp";
  try {
    fs.rmSync(tmp, { recursive: true, force: true });
    fs.cpSync(PASTA_LOGIN, tmp, { recursive: true });
    if (!credsBoas(tmp)) throw new Error("cópia saiu estragada");
    fs.rmSync(PASTA_LOGIN_BACKUP, { recursive: true, force: true });
    fs.renameSync(tmp, PASTA_LOGIN_BACKUP);
    estado.backupEm = new Date().toISOString();
  } catch (e) {
    console.log("Não consegui copiar a sessão:", e.message);
  }
}
setInterval(salvarSessao, 6 * 3600e3);

function restaurarSeEstragou() {
  const temArquivo = fs.existsSync(path.join(PASTA_LOGIN, "creds.json"));
  if (!temArquivo || credsBoas(PASTA_LOGIN) || !credsBoas(PASTA_LOGIN_BACKUP)) return false;
  fs.rmSync(PASTA_LOGIN, { recursive: true, force: true });
  fs.cpSync(PASTA_LOGIN_BACKUP, PASTA_LOGIN, { recursive: true });
  console.log("Sessão estragada: voltei da cópia");
  return true;
}

function apagarSessao() {
  fs.rmSync(PASTA_LOGIN, { recursive: true, force: true });
  fs.rmSync(PASTA_LOGIN_BACKUP, { recursive: true, force: true });   // sessão morta: a cópia também não serve
}

function explicarErro(codigo) {
  if (codigo === 403) return "o WhatsApp bloqueou ou restringiu o número";
  if (codigo === DisconnectReason.connectionReplaced) return "outro aparelho/programa abriu esta mesma sessão";
  if (codigo === DisconnectReason.badSession) return "a sessão estragou";
  if (codigo === DisconnectReason.timedOut || codigo === DisconnectReason.connectionLost ||
      codigo === DisconnectReason.connectionClosed)
    return "a internet do servidor oscilou";
  return `erro ${codigo || "?"}`;
}

// Queda longa: avisa no painel uma vez (os posts esperam sozinhos e voltam quando reconectar)
setInterval(async () => {
  if (estado.conectado || estado.deslogado || !estado.caiuEm || avisouQueda) return;
  const minutos = (Date.now() - Date.parse(estado.caiuEm)) / 60e3;
  if (minutos < MINUTOS_PARA_AVISAR_QUEDA) return;
  avisouQueda = true;
  await avisar(`🟠 WhatsApp fora do ar há ${Math.round(minutos)} min (${explicarErro(Number(estado.erro))}). ` +
    "Estou tentando voltar sozinho; os posts esperam e voltam juntos. Se passar de 1 hora ou o chip " +
    "tiver sido bloqueado: /zaptrocar 55DDDNÚMERO_DO_RESERVA");
}, 60e3);

async function conectar() {
  if (restaurarSeEstragou()) await avisar("🛟 A sessão do WhatsApp estragou e voltei da cópia de segurança.");
  const { state, saveCreds } = await useMultiFileAuthState(PASTA_LOGIN);
  // Sem login feito e sem o Gabriel pedindo pelo painel: fica quieto esperando o /zapconectar
  if (!state.creds.me && !(pedidoConexao && Date.now() < pedidoConexao.ate)) {
    sock = null;
    setTimeout(conectar, 5000);
    return;
  }
  let version;
  try {
    ({ version } = await fetchLatestBaileysVersion());
  } catch (e) {
    version = undefined;   // sem internet para olhar a versão: usa a que vem no Baileys
  }
  sock = makeWASocket({
    version, auth: state, logger: pino({ level: "silent" }),
    browser: Browsers.ubuntu("Chrome"), markOnlineOnConnect: false, syncFullHistory: false,
  });
  sock.ev.on("creds.update", saveCreds);
  // Bot B ao vivo: canal que o chip SEGUE manda cada post novo para cá (não depende de ler o histórico)
  sock.ev.on("messages.upsert", ({ messages }) => {
    for (const m of messages || []) {
      const jid = m.key && m.key.remoteJid;
      if (jid && jid.endsWith("@newsletter")) {
        guardarAoVivo(jid, m).catch((e) => console.log("Observador ao vivo falhou:", e.message));
      }
      if (jid && jid.endsWith("@g.us")) {
        guardarDoGrupo(jid, m).catch((e) => console.log("Observador de grupos falhou:", e.message));
      }
    }
  });
  // Reação em post de grupo (vem por aqui ou como reactionMessage no upsert; as duas contam 1 vez por pessoa)
  sock.ev.on("messages.reaction", (lista) => {
    for (const r of lista || []) {
      const jid = r.key && r.key.remoteJid;
      if (!jid || !jid.endsWith("@g.us") || !r.reaction) continue;
      const quem = r.reaction.key && (r.reaction.key.participant || r.reaction.key.remoteJid);
      registrarReacao(jid, r.key.id, quem, r.reaction.text);
    }
  });
  sock.ev.on("connection.update", async ({ connection, lastDisconnect, qr }) => {
    if (qr) {
      fs.writeFileSync(ARQUIVO_QR, await QRCode.toBuffer(qr, { width: 400 }));
      if (pedidoConexao && Date.now() < pedidoConexao.ate) {
        if (pedidoConexao.numero && !pedidoConexao.codigoPedido) {
          pedidoConexao.codigoPedido = true;
          try {
            const codigo = await sock.requestPairingCode(pedidoConexao.numero);
            await avisar(`📲 Código para conectar o WhatsApp: <code>${codigo}</code>\n\nNo celular do chip: ` +
              "WhatsApp → ⋮ → Aparelhos conectados → Conectar aparelho → Conectar com número de " +
              "telefone, e digite o código. Vale por uns 2 minutos.");
          } catch (e) {
            await avisar(`⚠️ Não consegui gerar o código (${e.message}). Mande /zapconectar sem número para receber o QR.`);
          }
        } else if (!pedidoConexao.numero && qrAvisados < 3) {
          qrAvisados += 1;   // o QR troca a cada ~20s: manda os 3 primeiros (abra no PC e escaneie com o chip)
          await mandarFotoNoPainel(fs.readFileSync(ARQUIVO_QR),
            "📷 Escaneie com o celular do chip: WhatsApp → ⋮ → Aparelhos conectados → Conectar aparelho");
        }
      }
    }
    if (connection === "open") {
      estado.conectado = true;
      estado.deslogado = false;
      estado.erro = null;
      estado.desde = new Date().toISOString();
      estado.numero = (sock.user && sock.user.id || "").split(":")[0].split("@")[0];
      fs.rmSync(ARQUIVO_QR, { force: true });
      if (pedidoConexao) {
        await avisar(`🟢 WhatsApp conectado (${estado.numero}). Os grupos continuam os mesmos: confira se este ` +
          "número é administrador nos dois grupos (/zapgrupos) e depois /zap");
      } else if (avisouQueda) {
        const minutos = Math.round((Date.now() - Date.parse(estado.caiuEm)) / 60e3);
        await avisar(`🟢 WhatsApp voltou depois de ${minutos} min. Os posts voltam sozinhos.`);
      }
      pedidoConexao = null;
      qrAvisados = 0;
      estado.caiuEm = null;
      avisouQueda = false;
      setTimeout(salvarSessao, 60e3);   // copia a sessão 1 min depois de conectar
      console.log("WhatsApp conectado:", estado.numero);
    }
    if (connection === "close") {
      const codigo = lastDisconnect && lastDisconnect.error && lastDisconnect.error.output
        ? lastDisconnect.error.output.statusCode : null;
      const estavaConectado = estado.conectado;
      estado.conectado = false;
      estado.erro = String(codigo || (lastDisconnect && lastDisconnect.error && lastDisconnect.error.message) || "");
      if (estavaConectado) {
        const hoje = new Date().toISOString().slice(0, 10);
        if (estado.diaQuedas !== hoje) { estado.diaQuedas = hoje; estado.quedasHoje = 0; }
        estado.quedasHoje += 1;
        estado.caiuEm = estado.caiuEm || new Date().toISOString();
      }
      if (codigo === DisconnectReason.loggedOut || codigo === 403) {
        // Desconectado pelo celular, número bloqueado ou troca de chip: não adianta tentar de novo sozinho
        estado.deslogado = true;
        apagarSessao();
        if (trocando) {
          trocando = false;
          console.log("Saí do chip antigo. Esperando o código do chip novo.");
        } else {
          await avisar(`🔴 O WhatsApp saiu da conta (${codigo === 403 ? explicarErro(403) : "desconectado pelo " +
            "celular ou o número teve problema"}). Os posts no WhatsApp pararam.\n\n` +
            "Mesmo chip: /zapconectar 55DDDNÚMERO\nChip reserva: /zaptrocar 55DDDNÚMERO_DO_RESERVA");
          console.log("Deslogado. Esperando /zapconectar.");
        }
        setTimeout(conectar, 5000);   // volta a esperar conexão nova (sem login)
        return;
      }
      if (estavaConectado) console.log("Conexão caiu (", estado.erro, "), reconectando...");
      setTimeout(conectar, codigo === DisconnectReason.restartRequired ? 1000 : 10000);
    }
  });
}

function lerCorpo(req) {
  return new Promise((ok, falha) => {
    let dados = "";
    req.on("data", (c) => { dados += c; if (dados.length > 20e6) req.destroy(); });
    req.on("end", () => { try { ok(dados ? JSON.parse(dados) : {}); } catch (e) { falha(e); } });
    req.on("error", falha);
  });
}

function responder(res, codigo, obj) {
  res.writeHead(codigo, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(obj));
}

const espera = (ms) => new Promise((ok) => setTimeout(ok, ms));

// ---------- Bot B: leitura de canais de outros afiliados (só leitura) ----------

// Tenta pelo id (seguindo o canal antes, se ainda não seguia) e depois pelo convite. Cada tentativa
// desiste em 25 s: o WhatsApp às vezes simplesmente não responde.
const comLimite = (promessa) => Promise.race([promessa, new Promise((_, no) =>
  setTimeout(() => no(new Error("sem resposta em 25 s")), 25000))]);

async function lerCanalMensagens(jid, convite, qtd, depurar) {
  const tentativas = [];
  if (jid) tentativas.push(["id", () => sock.newsletterFetchMessages("jid", jid, qtd)]);
  if (convite) tentativas.push(["convite", () => sock.newsletterFetchMessages("invite", convite, qtd)]);
  let lista = null;
  const falhas = [];
  for (let volta = 0; volta < 2 && !lista; volta++) {
    for (const [nome, fazer] of tentativas) {
      try {
        lista = await comLimite(fazer());
        break;
      } catch (e) {
        falhas.push(`${nome}: ${e.message}`);
      }
    }
    if (!lista && volta === 0 && jid) {
      try { await comLimite(sock.newsletterFollow(jid)); falhas.push("segui o canal"); }
      catch (e) { falhas.push(`seguir: ${e.message}`); }
    }
  }
  if (!lista) return { ok: false, erro: falhas.join(" | ") };
  const itens = lista.map((m) => {
    const msg = m.message || {};
    const texto = msg.conversation || (msg.extendedTextMessage && msg.extendedTextMessage.text) ||
      (msg.imageMessage && msg.imageMessage.caption) || (msg.videoMessage && msg.videoMessage.caption) || "";
    const reacoes = (m.reactions || []).reduce((s, r) => s + Number(r.count || 0), 0);
    const t = m.timestamp || m.t || (msg.messageContextInfo && msg.messageContextInfo.timestamp) || null;
    return { id: String(m.server_id || m.id || ""), views: Number(m.views || 0), reacoes,
             quando: t ? Number(t) : null, texto };
  });
  const extra = depurar && lista[0]
    ? { campos: Object.keys(lista[0]), msg_campos: Object.keys(lista[0].message || {}) } : undefined;
  return { ok: true, itens, extra };
}

// Observação 24 horas: de tempos em tempos lê todos os canais de bots/*/canais_observados.json,
// guarda a leitura em whatsapp/leituras.json (o /zapmaisvistos usa isso, sem esperar) e, no canal
// marcado como oficial (/zapoficial), avisa no painel de cada post NOVO (cupom, comissão, campanha).
const PASTA_BOTS = path.join(__dirname, "..", "bots");
const ARQUIVO_LEITURAS = path.join(__dirname, "leituras.json");
const INTERVALO_LEITURA_MIN = 20;

function canaisObservados() {
  const lista = [];
  let pastas = [];
  try { pastas = fs.readdirSync(PASTA_BOTS); } catch (e) { return lista; }
  for (const bot of pastas) {
    try {
      const dados = JSON.parse(fs.readFileSync(path.join(PASTA_BOTS, bot, "canais_observados.json"), "utf-8"));
      for (const c of dados.canais || []) if (!lista.some((x) => x.id === c.id)) lista.push(c);
    } catch (e) { /* esse bot não observa nada */ }
  }
  return lista;
}

function lerLeituras() {
  try { return JSON.parse(fs.readFileSync(ARQUIVO_LEITURAS, "utf-8")); } catch (e) { return {}; }
}

const escaparHtml = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// (08/11) Grupo com MENSAGENS TEMPORÁRIAS (e foto de "ver uma vez", documento com legenda, mensagem editada)
// manda o post "embrulhado": ephemeralMessage.message.imageMessage... Sem desembrulhar, o observador achava que
// não tinha texto nem foto e jogava fora (alguns grupos observados não apareciam).
function abrirMensagem(msg) {
  for (let i = 0; i < 5 && msg; i++) {
    const dentro = msg.ephemeralMessage || msg.viewOnceMessage || msg.viewOnceMessageV2 ||
      msg.viewOnceMessageV2Extension || msg.documentWithCaptionMessage || msg.editedMessage;
    if (!dentro || !dentro.message) break;
    msg = dentro.message;
  }
  return msg || {};
}

function textoDaMensagem(msg) {
  msg = abrirMensagem(msg);
  return msg.conversation || (msg.extendedTextMessage && msg.extendedTextMessage.text) ||
    (msg.imageMessage && msg.imageMessage.caption) || (msg.videoMessage && msg.videoMessage.caption) ||
    (msg.documentMessage && msg.documentMessage.caption) || "";
}

// Canal oficial: avisa no painel o post novo (cada id uma vez só, venha da leitura ou do ao vivo)
async function avisarSeOficial(canal, entrada, m) {
  if (!canal || !canal.oficial || !m.texto || !m.id) return;
  entrada.avisados = entrada.avisados || [];
  if (entrada.avisados.includes(m.id)) return;
  entrada.avisados = entrada.avisados.concat(m.id).slice(-200);
  await avisar(`📢 <b>${escaparHtml(canal.nome)}</b> postou:\n\n${escaparHtml(m.texto.slice(0, 900))}`);
}

async function guardarAoVivo(jid, m) {
  const canal = canaisObservados().find((c) => c.id === jid);
  if (!canal) return;                      // canal que o chip segue, mas ninguém pediu para observar
  const texto = textoDaMensagem(m.message);
  const item = { id: String((m.key && (m.key.server_id || m.key.id)) || ""), views: 0, reacoes: 0,
                 quando: Number(m.messageTimestamp || 0) || Math.floor(Date.now() / 1000), texto };
  const leituras = lerLeituras();
  const entrada = leituras[jid] || { nome: canal.nome };
  entrada.ao_vivo = (entrada.ao_vivo || []).filter((x) => x.id !== item.id).concat(item).slice(-100);
  entrada.ultimo_ao_vivo = Date.now();
  await avisarSeOficial(canal, entrada, item);
  leituras[jid] = entrada;
  fs.writeFileSync(ARQUIVO_LEITURAS, JSON.stringify(leituras));
  console.log("Observador ao vivo:", canal.nome, "-", texto.slice(0, 60).replace(/\n/g, " "));
}

async function observarUmaVez() {
  if (!estado.conectado) return;
  for (const canal of canaisObservados()) {
    const r = await lerCanalMensagens(canal.id, canal.convite, 30, false);
    const leituras = lerLeituras();      // lê de novo: o ao vivo pode ter gravado no meio tempo
    const anterior = leituras[canal.id] || {};
    if (!r.ok) {
      leituras[canal.id] = { ...anterior, nome: canal.nome, erro: r.erro, tentou: Date.now() };
      console.log("Observador:", canal.nome, "não leu:", r.erro);
    } else {
      const primeira = !anterior.mensagens;
      const entrada = { ...anterior, nome: canal.nome, quando: Date.now(), mensagens: r.itens, erro: null };
      // Na 1ª leitura só marca o que já existia (sem avisar); depois avisa o que for novo
      if (primeira) entrada.avisados = r.itens.map((m) => m.id).slice(-200);
      else for (const m of r.itens) await avisarSeOficial(canal, entrada, m);   // cada id avisa 1 vez só
      leituras[canal.id] = entrada;
      console.log("Observador:", canal.nome, "-", r.itens.length, "mensagens lidas");
    }
    fs.writeFileSync(ARQUIVO_LEITURAS, JSON.stringify(leituras));
    await espera(3000 + Math.random() * 4000);   // um canal de cada vez, devagar
  }
}

async function observarSempre() {
  try { await observarUmaVez(); } catch (e) { console.log("Observador falhou:", e.message); }
  setTimeout(observarSempre, INTERVALO_LEITURA_MIN * 60e3 * (0.8 + Math.random() * 0.4));
}
setTimeout(observarSempre, 60e3);   // 1 min depois de ligar (dá tempo de conectar)

// ---------- Observador de GRUPOS (06/11, Gabriel: "analisa tudo que os grupos postarem") ----------
// Os grupos de ofertas em que o chip está (de outros afiliados) mandam cada post para cá. Guarda tudo em
// whatsapp/grupos_observados.json: texto, links, preços, se tem foto/vídeo e as reações (contagem por emoji).
// Fica de fora: os NOSSOS grupos (bots/*/whatsapp_destinos.txt) e o que o próprio chip manda.
// Privacidade: não guarda quem postou nem o número de quem reagiu (só um código embaralhado para não contar
// a mesma pessoa 2 vezes). Só leitura: nunca manda nada nesses grupos.
const ARQUIVO_GRUPOS_OBS = path.join(__dirname, "grupos_observados.json");
const MAX_POSTS_POR_GRUPO = 3000;            // ~1 mês de um grupo que posta 100 por dia
let gruposObs = null;
let gruposObsMudou = false;
const nomesGrupos = {};

function carregarGruposObs() {
  if (!gruposObs) {
    try { gruposObs = JSON.parse(fs.readFileSync(ARQUIVO_GRUPOS_OBS, "utf-8")); } catch (e) { gruposObs = {}; }
  }
  return gruposObs;
}

function nossosGrupos() {
  const ids = new Set();
  let pastas = [];
  try { pastas = fs.readdirSync(PASTA_BOTS); } catch (e) { return ids; }
  for (const bot of pastas) {
    try {
      for (const l of fs.readFileSync(path.join(PASTA_BOTS, bot, "whatsapp_destinos.txt"), "utf-8").split(/\r?\n/)) {
        const id = l.split("#")[0].trim();
        if (id) ids.add(id);
      }
    } catch (e) { /* bot sem destino */ }
  }
  return ids;
}

async function nomeDoGrupo(jid) {
  if (!nomesGrupos[jid]) {
    try { nomesGrupos[jid] = (await sock.groupMetadata(jid)).subject || jid; } catch (e) { return jid; }
  }
  return nomesGrupos[jid];
}

const embaralhar = (s) => crypto.createHash("sha256").update(String(s)).digest("hex").slice(0, 12);

function dadosDaOferta(texto) {
  const links = texto.match(/https?:\/\/\S+/g) || [];
  const precos = (texto.match(/R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{1,2})?/g) || []).map((p) => p.replace(/\s/g, ""));
  return { links, precos, shopee: links.some((l) => /shopee|shope\.ee/i.test(l)) };
}

async function guardarDoGrupo(jid, m) {
  if (!m.key || m.key.fromMe) return;
  const msg = abrirMensagem(m.message);
  if (msg.reactionMessage) {
    const quem = m.key.participant || m.key.remoteJid;
    return registrarReacao(jid, msg.reactionMessage.key && msg.reactionMessage.key.id, quem, msg.reactionMessage.text);
  }
  if (nossosGrupos().has(jid)) return;
  const texto = textoDaMensagem(msg);
  const imagem = !!msg.imageMessage, video = !!msg.videoMessage;
  if (!texto && !imagem && !video) return;   // aviso de sistema, figurinha, áudio...
  const dados = carregarGruposObs();
  const g = dados[jid] || (dados[jid] = { posts: [] });
  g.nome = await nomeDoGrupo(jid);
  const id = m.key.id;
  if (g.posts.some((p) => p.id === id)) return;
  g.posts.push({ id, quando: Number(m.messageTimestamp || 0) || Math.floor(Date.now() / 1000),
                 texto: texto.slice(0, 2000), imagem, video, ...dadosDaOferta(texto), reacoes: {} });
  if (g.posts.length > MAX_POSTS_POR_GRUPO) g.posts = g.posts.slice(-MAX_POSTS_POR_GRUPO);
  gruposObsMudou = true;
}

function registrarReacao(jid, alvo, quem, emoji) {
  const g = carregarGruposObs()[jid];
  const p = g && g.posts.find((x) => x.id === alvo);
  if (!p || !quem) return;                   // reação em post que não foi guardado (ou dos nossos grupos)
  const chave = embaralhar(quem);
  if (emoji) p.reacoes[chave] = emoji; else delete p.reacoes[chave];   // texto vazio = tirou a reação
  gruposObsMudou = true;
}

setInterval(() => {                          // grava no disco a cada 30 s (não a cada mensagem)
  if (!gruposObsMudou) return;
  gruposObsMudou = false;
  const tmp = ARQUIVO_GRUPOS_OBS + ".tmp";
  fs.writeFileSync(tmp, JSON.stringify(gruposObs));
  fs.renameSync(tmp, ARQUIVO_GRUPOS_OBS);
}, 30e3);

function resumoGrupos(horas) {
  const desde = Date.now() / 1000 - horas * 3600;
  const saida = {};
  for (const [jid, g] of Object.entries(carregarGruposObs())) {
    const posts = g.posts.filter((p) => p.quando >= desde).map((p) => {
      const emojis = {};
      for (const e of Object.values(p.reacoes || {})) emojis[e] = (emojis[e] || 0) + 1;
      return { ...p, reacoes: Object.values(p.reacoes || {}).length, emojis };
    });
    saida[jid] = { nome: g.nome, total_guardado: g.posts.length, posts };
  }
  return saida;
}

http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://localhost");
  try {
    if (req.method === "GET" && url.pathname === "/status") {
      return responder(res, 200, { ...estado, qr: fs.existsSync(ARQUIVO_QR) });
    }
    if (req.method === "POST" && url.pathname === "/conectar") {
      const { numero } = await lerCorpo(req);
      if (estado.conectado) return responder(res, 200, { ok: true, ja: true, numero: estado.numero });
      pedidoConexao = { numero: numero ? String(numero).replace(/\D/g, "") : null, ate: Date.now() + 3 * 60e3 };
      qrAvisados = 0;
      // Recomeça a conexão para vir um QR novo (e o código, se mandou o número)
      try { sock && sock.end(undefined); } catch (e) { /* já estava fechada */ }
      return responder(res, 200, { ok: true });
    }
    if (req.method === "POST" && url.pathname === "/trocar") {
      // Chip reserva (07/11): sai da conta atual (se ainda estiver nela) e pede o código do número novo.
      // Os destinos (ids dos grupos) não mudam: o número novo só precisa ser admin nos grupos.
      const { numero } = await lerCorpo(req);
      const novo = String(numero || "").replace(/\D/g, "");
      if (novo.length < 12) return responder(res, 400, { ok: false, erro: "número inválido" });
      if (estado.conectado && estado.numero === novo) return responder(res, 200, { ok: true, ja: true, numero: novo });
      const antigo = estado.numero;
      pedidoConexao = { numero: novo, ate: Date.now() + 5 * 60e3 };
      qrAvisados = 0;
      if (sock && estado.conectado) {
        trocando = true;
        try { await sock.logout(); } catch (e) {
          apagarSessao();   // não deu para sair direito: apaga a sessão e recomeça do zero
          try { sock.end(undefined); } catch (e2) { /* já estava fechada */ }
        }
        setTimeout(() => { trocando = false; }, 60e3);
      } else {
        apagarSessao();
        try { sock && sock.end(undefined); } catch (e) { /* já estava fechada */ }
      }
      return responder(res, 200, { ok: true, antigo });
    }
    if (req.method === "GET" && url.pathname === "/grupos/observados") {
      // Funciona mesmo desconectado (é o que já foi guardado). ?horas=24 (máx. 24*60)
      const horas = Math.min(Number(url.searchParams.get("horas") || 24) || 24, 24 * 60);
      return responder(res, 200, { ok: true, grupos: resumoGrupos(horas) });
    }
    if (!estado.conectado) return responder(res, 503, { ok: false, erro: "WhatsApp desconectado" });
    if (req.method === "GET" && url.pathname === "/grupos") {
      const grupos = await sock.groupFetchAllParticipating();
      return responder(res, 200, Object.values(grupos).map((g) => ({
        id: g.id, nome: g.subject, pessoas: (g.participants || []).length,
      })));
    }
    if (req.method === "GET" && url.pathname === "/canal") {
      const convite = (url.searchParams.get("convite") || "").split("/").pop();
      const canal = await sock.newsletterMetadata("invite", convite);
      const nome = canal && (canal.name || (canal.thread_metadata && canal.thread_metadata.name &&
        canal.thread_metadata.name.text));
      return responder(res, 200, { id: canal && canal.id, nome });
    }
    if (req.method === "GET" && url.pathname === "/canal/mensagens") {
      // Bot B: lê as últimas mensagens de um canal (de qualquer pessoa) com visualizações e reações.
      // Só leitura; não manda nada. ?jid=ID@newsletter (ou ?convite=CODIGO) &qtd=40
      const jid = url.searchParams.get("jid");
      const convite = (url.searchParams.get("convite") || "").split("/").pop();
      const qtd = Math.min(parseInt(url.searchParams.get("qtd") || "40", 10) || 40, 100);
      const r = await lerCanalMensagens(jid, convite, qtd, !!url.searchParams.get("depurar"));
      if (!r.ok) return responder(res, 200, { ok: false, erro: r.erro });
      return responder(res, 200, { ok: true, mensagens: r.itens, extra: r.extra });
    }
    if (req.method === "GET" && url.pathname === "/canal/leituras") {
      // O que o observador já leu sozinho (atualiza a cada ~20 min): o painel mostra sem esperar
      return responder(res, 200, { ok: true, leituras: lerLeituras() });
    }
    if (req.method === "POST" && url.pathname === "/canal/seguir") {
      const { jid } = await lerCorpo(req);
      await sock.newsletterFollow(jid);
      return responder(res, 200, { ok: true });
    }
    if (req.method === "POST" && url.pathname === "/enviar") {
      const { destinos, texto, imagem } = await lerCorpo(req);
      const resultados = [];
      for (const jid of destinos || []) {
        try {
          const msg = imagem ? { image: Buffer.from(imagem, "base64"), caption: texto } : { text: texto };
          await sock.sendMessage(jid, msg);
          resultados.push({ jid, ok: true });
        } catch (e) {
          resultados.push({ jid, ok: false, erro: e.message });
        }
        await espera(1500 + Math.random() * 2500);   // não manda tudo no mesmo segundo
      }
      return responder(res, 200, { ok: resultados.some((r) => r.ok), resultados });
    }
    return responder(res, 404, { ok: false, erro: "caminho desconhecido" });
  } catch (e) {
    console.log("Erro em", url.pathname, ":", e.message);
    return responder(res, 500, { ok: false, erro: e.message });
  }
}).listen(PORTA, "127.0.0.1", () => console.log(`WhatsApp do bot ouvindo em 127.0.0.1:${PORTA}`));

conectar();
