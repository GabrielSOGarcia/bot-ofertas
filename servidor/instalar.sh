#!/usr/bin/env bash
# Instala o bot como serviço no servidor (Oracle Linux ou Ubuntu). Rode de dentro da pasta do bot:
#   bash servidor/instalar.sh
set -e
cd "$(dirname "$0")/.."

echo "== Memória extra (swap) para a máquina pequena não travar =="
if ! swapon --show | grep -q .; then
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab > /dev/null
fi

echo "== Instalando Python e a biblioteca de imagem =="
if command -v dnf > /dev/null; then          # Oracle Linux
    sudo dnf install -y python3 python3-pip
    python3 -m pip install --user pillow
else                                          # Ubuntu / Debian
    sudo apt-get update -y
    sudo apt-get install -y python3 python3-pil
fi
python3 -c "import PIL; print('Pillow ok', PIL.__version__)"

echo "== Pasta das senhas (fora da pasta do bot) =="
mkdir -p ~/bot-config
chmod 700 ~/bot-config

echo "== Registrando o serviço (liga sozinho e volta se cair) =="
sed "s/USUARIO/$USER/g" servidor/bot-ofertas.service | sudo tee /etc/systemd/system/bot-ofertas.service > /dev/null
sudo systemctl daemon-reload
sudo systemctl enable bot-ofertas

echo
echo "Pronto. Falta só:"
echo "  1) copiar o config.txt para ~/bot-config/config.txt (do seu PC, com scp)"
echo "  2) conferir:  BOT_CONFIG=~/bot-config/config.txt python3 testar_config.py"
echo "  3) ligar:     sudo systemctl start bot-ofertas"
echo "  4) ver posts: journalctl -u bot-ofertas -f"
