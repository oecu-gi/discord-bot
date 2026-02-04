#!/bin/bash

# スクリプトのディレクトリに移動
cd "$(dirname "$0")" || exit

echo "更新を確認しています..."
git fetch origin

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "更新が見つかりました。プルしています..."
    git pull
    
    # 必要に応じて依存関係を更新
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi
    
    echo "再起動をトリガーするためにボットプロセスを停止しています..."
    # python3 main.py プロセスを見つけて停止します。
    # 可能であれば他のpythonプロセスを停止しないように注意してください。
    # 完全なコマンドライン一致を見つけるために pkill -f を使用しています。
    pkill -f "python3 main.py"
    
    echo "更新が完了しました。"
else
    echo "更新は見つかりませんでした。"
fi
