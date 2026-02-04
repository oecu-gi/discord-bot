#!/bin/bash

while true; do
    echo "ボットを起動しています..."
    python3 main.py
    
    EXIT_CODE=$?
    echo "ボットが終了コード $EXIT_CODE で停止しました。"
    
    # 特定のエラーコードでループを停止したい場合は、ここにチェックを追加できます。
    # 現時点では、どのような終了でも再起動します。
    
    echo "1秒後に再起動します..."
    sleep 1
done
