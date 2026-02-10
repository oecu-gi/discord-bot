#!/bin/bash

while true; do
    echo "ボットを起動しています..."
    python3 main.py
    
    EXIT_CODE=$?
    echo "ボットが終了コード $EXIT_CODE で停止しました。"
    
    # 終了コードが0の場合は正常終了とみなしてループを抜ける
    if [ $EXIT_CODE -eq 0 ]; then
        echo "正常終了しました。再起動しません。"
        break
    fi
    
    echo "1秒後に再起動します..."
    sleep 1
done
