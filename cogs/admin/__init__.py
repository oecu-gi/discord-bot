from discord.ext import commands
from . import group, reload, restart
import importlib

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 既にコマンドが登録された admin_group を管理下に置く
        # モジュール変数から直接参照することで、リロード後の最新オブジェクトを取得
        self.bot.tree.add_command(group.admin_group)

    async def cog_unload(self):
        # Cogアンロード時にコマンドを削除しないと、リロード時にエラーになったり重複したりする可能性がある
        self.bot.tree.remove_command(group.admin_group.name)

async def setup(bot):
    # ホットリロード用: setup呼び出し時にモジュールを再読み込みする
    # これにより、Cogのリロードコマンド実行時にサブモジュールの変更も反映される
    
    # 1. まずGroup定義を持つモジュールをリロード (新しいadmin_groupオブジェクトを作成)
    importlib.reload(group)
    # 2. その後にコマンド実装を持つモジュールをリロード (新しいadmin_groupにコマンドを登録)
    importlib.reload(reload)
    importlib.reload(restart)
    
    await bot.add_cog(Admin(bot))
