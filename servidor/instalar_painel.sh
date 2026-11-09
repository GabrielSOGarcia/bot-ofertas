#!/bin/bash
# Troca o serviço antigo (bot-ofertas) pelos novos: um por bot (bot-ofertas@casa, ...) e o painel.
# Rodar no servidor:  bash ~/bot-ofertas/servidor/instalar_painel.sh
set -e
cd ~/bot-ofertas
sudo timedatectl set-timezone America/Sao_Paulo
sudo cp servidor/bot-ofertas@.service servidor/painel.service /etc/systemd/system/
sudo systemctl disable --now bot-ofertas 2>/dev/null || true
sudo systemctl daemon-reload
sudo systemctl enable --now painel
echo
echo "Pronto: o painel está ligado. No Telegram, mande /status para o bot do painel."
echo "O bot Casa continua desligado: ligue pelo painel com /ligar casa"
