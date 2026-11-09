# Bot de Ofertas Shopee

Bot que encontra ofertas na Shopee e publica automaticamente em canais do Telegram e grupos do WhatsApp, com link de afiliado. Roda 24h num servidor Linux e é controlado por um painel no próprio Telegram.

## Sobre o projeto

Comecei este projeto com uma ideia de renda extra usando links de afiliado da Shopee. Com a ajuda da IA, fui corrigindo, melhorando e aprimorando aos poucos, e hoje ele está como descrito abaixo. O projeto continua em andamento: a próxima etapa é levar o bot para o Mercado Livre.

## O que ele faz

- **Busca de ofertas**: consulta a API de afiliados da Shopee (GraphQL, requisições assinadas com SHA-256) por listas de palavras-chave de cada nicho e filtra por desconto mínimo, avaliação, marca e comissão.
- **Escolha do produto**: dá uma pontuação a cada candidato (desconto, comissão extra da loja, marca conhecida, variedade de categorias) e evita repetir produtos já postados.
- **Post pronto**: monta o texto com preço "de/por", cupom ativo, nome do produto limpo e foto. Opcionalmente usa o Google Gemini para escrever a chamada.
- **Vários bots com um só código**: cada nicho é uma pasta em `bots/` com um `nicho.py` que sobrescreve só o que muda (listas de produtos, marcas, canal).
- **WhatsApp**: um serviço em Node.js com [Baileys](https://github.com/WhiskeySockets/Baileys) mantém a conexão do número e entrega os posts nos grupos/canais. Só aceita pedidos de dentro do servidor (127.0.0.1).
- **Painel no Telegram**: um bot separado, que só obedece o administrador, liga e desliga os bots, muda ajustes sem reiniciar, recebe cupons, faz backup e roda uma verificação geral do sistema.
- **Relatório de vendas**: cada link é etiquetado (canal, tipo, palavra) para o relatório mostrar o que gera cliques e vendas.
- **Análise de concorrência**: lê (sem copiar) o que outros grupos e canais de ofertas postam e o que mais engaja, para sugerir produtos novos.

## Tecnologias

- Python 3 (biblioteca padrão + Pillow para as imagens)
- Node.js + Baileys (WhatsApp), pino, qrcode
- APIs: Shopee Affiliate Open API, Telegram Bot API, Google Gemini
- Linux + systemd (um serviço por bot: `bot-ofertas@NOME`)

## Estrutura

```
postar_shopee.py      programa principal (busca, escolha e publicação)
painel.py             painel de controle pelo Telegram
verificacao.py        checagem de tudo de que o bot depende
relatorio.py          relatório de vendas dos links de afiliado
cupons.py             leitura e gravação de cupons
concorrentes.py       observador de grupos de outros afiliados
observador.py         observador de canais do WhatsApp
analisar_grupos.py    cruza o que os outros postam com as nossas listas
testar_config.py      confere se as credenciais do config.txt funcionam
bots/<nicho>/nicho.py ajustes de cada bot (bots/_modelo é o modelo para um bot novo)
whatsapp/servidor.js  conexão com o WhatsApp (HTTP local na porta 3010)
servidor/             scripts de instalação e serviços systemd
```

## Como configurar

1. **Credenciais**: copie `config.example.txt` para um lugar **fora** da pasta do projeto (por exemplo `C:\bot-config\config.txt`, ou `~/bot-config/config.txt` no Linux) e preencha:
   - `TOKEN` e `CANAL`: bot do Telegram (criado no @BotFather) e o canal onde ele é administrador
   - `SHOPEE_APPID` e `SHOPEE_SECRET`: credenciais do programa de afiliados da Shopee
   - `PAINEL_TOKEN` e `PAINEL_ADMIN`: bot do painel e o seu ID de usuário do Telegram
   - `GEMINI_KEY` (opcional)

   Se o arquivo estiver em outro caminho, aponte a variável de ambiente `BOT_CONFIG` para ele.

2. **Dependências**
   ```bash
   pip install -r servidor/requirements.txt
   cd whatsapp && npm install
   ```

3. **Conferir as credenciais**
   ```bash
   python testar_config.py
   ```

4. **Rodar**
   ```bash
   python postar_shopee.py          # bot "casa"
   python postar_shopee.py geral    # outro bot (pasta bots/geral)
   python painel.py                 # painel no Telegram
   node whatsapp/servidor.js        # conexão com o WhatsApp
   ```

5. **Links dos grupos**: em `postar_shopee.py` e `bots/geral/nicho.py`, troque os links de exemplo em `GRUPOS` pelos convites dos seus grupos.

6. **Servidor 24h**: o passo a passo está em [`servidor/COMO_INSTALAR.txt`](servidor/COMO_INSTALAR.txt).

## Segurança

Nenhuma credencial fica no código: tudo é lido do `config.txt`, que fica fora do repositório. A sessão do WhatsApp, os históricos e os backups também ficam fora do Git (veja o `.gitignore`).
