#!/bin/bash
# Instala o programa do WhatsApp (whatsapp/servidor.js) como servico: liga sozinho e volta se cair.
# Rodar no servidor:  bash ~/bot-ofertas/servidor/instalar_whatsapp.sh
set -e
command -v git >/dev/null || sudo dnf install -y git   # o Baileys baixa uma peca pelo git
cd ~/bot-ofertas/whatsapp
npm install --omit=dev --no-audit --no-fund
sudo cp ~/bot-ofertas/servidor/whatsapp.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now whatsapp
sudo systemctl restart painel
echo
echo "Pronto: WhatsApp instalado. No painel: /zapconectar 55DDDNUMERO (o numero do chip)"
