#!/bin/bash

# 実行中のrab.pyプロセスを終了する
pkill -f /home/ubuntu/web/rab.py

# Pythonスクリプトをバックグラウンドで再実行する
nohup python3 -u /home/ubuntu/web/rab.py > /home/ubuntu/web/rab.log 2>&1 &
python3 /home/ubuntu/web/time.py > /home/ubuntu/web/time.log 2>&1
