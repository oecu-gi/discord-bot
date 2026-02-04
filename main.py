import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        # Cogを再帰的に読み込む
        for root, dirs, files in os.walk('cogs'):
            # __init__.pyが存在する場合、そのディレクトリをパッケージとして読み込む
            if '__init__.py' in files:
                path = root.replace(os.path.sep, '.').replace('/', '.')
                # current directory "." check (though technically root starts with cogs)
                if path.startswith('.'):
                    path = path[1:]
                
                try:
                    await self.load_extension(path)
                    print(f'パッケージを読み込みました: {path}')
                except commands.errors.ExtensionAlreadyLoaded:
                    pass
                except Exception as e:
                    print(f'パッケージ {path} の読み込みに失敗しました: {e}')
                
                # パッケージとして読み込んだディレクトリ内の個別ファイルは無視する
                continue

            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    path = os.path.join(root, file)
                    module = path.replace('.py', '').replace(os.path.sep, '.').replace('/', '.')
                    
                    try:
                        await self.load_extension(module)
                        print(f'拡張機能を読み込みました: {module}')
                    except commands.errors.NoEntryPointError:
                        pass
                    except commands.errors.ExtensionAlreadyLoaded:
                        pass
                    except Exception as e:
                        print(f'拡張機能 {module} の読み込みに失敗しました: {e}')


        # コマンドを同期
        await self.tree.sync()
        print("コマンドが同期されました。")

    async def on_ready(self):
        print(f'{self.user} としてログインしました (ID: {self.user.id})')

if __name__ == '__main__':
    if not TOKEN:
        print("エラー: .envファイルにDISCORD_TOKENが設定されていません。")
        exit(1)
    
    bot = MyBot()
    try:
        bot.run(TOKEN)
    except discord.errors.PrivilegedIntentsRequired:
        print("\n\033[31m[ERROR] Privileged Intents Required\033[0m")
        print("Discord Developer Portalで 'Privileged Gateway Intents' の 'Presence Intent' と 'Server Members Intent' を有効にしてください。")
        print("URL: https://discord.com/developers/applications")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
