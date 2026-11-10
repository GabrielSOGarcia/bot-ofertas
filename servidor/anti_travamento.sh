#!/bin/bash
# Anti-travamento (10/11/2026): a VM micro tem só ~500 MB de RAM e travava de vez (3x no dia 10/11) quando
# a memória acabava e o disco virava "memória" (swap lento). Isto faz 3 coisas:
#  1) zram: um swap COMPRIMIDO dentro da própria RAM (bem mais rápido que o disco): a máquina aguenta o aperto
#  2) teto de memória por serviço: um bot que inchar é reiniciado sozinho, sem derrubar o servidor inteiro
#  3) vigia: se a memória ficar no limite por 1 minuto, reinicia o bot que mais usa (antes de travar tudo)
# Rodar uma vez no servidor:  bash ~/bot-ofertas/servidor/anti_travamento.sh   (pode rodar de novo: não duplica)
set -e

echo "== 1) zram (swap comprimido na RAM)"
sudo tee /etc/systemd/system/zram-swap.service >/dev/null <<'EOF'
[Unit]
Description=Swap comprimido na RAM (zram) - anti-travamento do bot
After=local-fs.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/sh -c 'modprobe zram num_devices=1; swapoff /dev/zram0 2>/dev/null; echo 1 > /sys/block/zram0/reset; (echo lz4 > /sys/block/zram0/comp_algorithm) 2>/dev/null; echo 350M > /sys/block/zram0/disksize && mkswap /dev/zram0 >/dev/null && swapon -p 100 /dev/zram0'
ExecStop=/bin/sh -c 'swapoff /dev/zram0; echo 1 > /sys/block/zram0/reset'

[Install]
WantedBy=multi-user.target
EOF
echo "vm.swappiness=100" | sudo tee /etc/sysctl.d/90-bot-ofertas.conf >/dev/null
sudo sysctl -q -p /etc/sysctl.d/90-bot-ofertas.conf

echo "== 2) teto de memória por serviço"
sudo mkdir -p /etc/systemd/system/bot-ofertas@.service.d /etc/systemd/system/whatsapp.service.d \
              /etc/systemd/system/painel.service.d
printf '[Service]\nMemoryHigh=120M\nMemoryMax=190M\n' | sudo tee /etc/systemd/system/bot-ofertas@.service.d/memoria.conf >/dev/null
printf '[Service]\nMemoryHigh=240M\nMemoryMax=320M\n' | sudo tee /etc/systemd/system/whatsapp.service.d/memoria.conf >/dev/null
printf '[Service]\nMemoryHigh=70M\nMemoryMax=110M\n'  | sudo tee /etc/systemd/system/painel.service.d/memoria.conf >/dev/null

echo "== 3) vigia da memória"
sudo tee /usr/local/bin/vigia-memoria.sh >/dev/null <<'EOF'
#!/bin/bash
# A cada 20 s: se sobrar menos de 30 MB livres E a pressão de memória estiver alta, conta; 3 seguidas (~1 min)
# reinicia o bot (python) que mais usa memória. O WhatsApp e o painel não são mexidos.
seguidas=0
while true; do
  livre=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
  pressao=$(awk -F'avg10=' '/^full/ {split($2,a," "); print int(a[1])}' /proc/pressure/memory 2>/dev/null || echo 0)
  if [ "${livre:-999}" -lt 30 ] && [ "${pressao:-0}" -ge 20 ]; then
    seguidas=$((seguidas+1))
  else
    seguidas=0
  fi
  if [ "$seguidas" -ge 3 ]; then
    maior=""; maior_mem=0
    for u in $(systemctl list-units --plain --no-legend 'bot-ofertas@*.service' | awk '{print $1}'); do
      m=$(systemctl show -p MemoryCurrent --value "$u" 2>/dev/null)
      [[ "$m" =~ ^[0-9]+$ ]] && [ "$m" -gt "$maior_mem" ] && maior=$u && maior_mem=$m
    done
    if [ -n "$maior" ]; then
      logger -t vigia-memoria "memória no limite (livre ${livre} MB, pressão ${pressao}): reiniciando $maior"
      systemctl restart "$maior"
    fi
    seguidas=0
    sleep 60
  fi
  sleep 20
done
EOF
sudo chmod +x /usr/local/bin/vigia-memoria.sh
sudo tee /etc/systemd/system/vigia-memoria.service >/dev/null <<'EOF'
[Unit]
Description=Vigia de memória do bot de ofertas (reinicia o bot que incha antes do servidor travar)

[Service]
ExecStart=/usr/local/bin/vigia-memoria.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now zram-swap.service vigia-memoria.service
sudo systemctl restart painel whatsapp 'bot-ofertas@*'
sleep 5
echo "== pronto"
swapon --show
free -m
systemctl is-active zram-swap vigia-memoria painel whatsapp bot-ofertas@casa bot-ofertas@geral bot-ofertas@perfume
