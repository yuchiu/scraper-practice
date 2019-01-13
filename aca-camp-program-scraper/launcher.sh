#!/bin/bash
sudo systemctl start redis
sudo systemctl start mongodb

pip3 install -r requirements.txt

python3 apps/main.py &
python3 apps/data-fetcher/fetcher.py &
python3 apps/data-deduper/deduper.py &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)