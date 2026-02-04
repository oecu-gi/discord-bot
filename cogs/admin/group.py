import discord
from discord import app_commands
import functools

# ここで1つだけ Group インスタンスを作る
admin_group = app_commands.Group(name="admin", description="管理者コマンド")

def is_admin_or_specific_role():
    """
    管理者権限を持っているか、特定のロール(ID: 1468589563323744338)を持っているユーザーのみ実行可能にするチェック
    """
    def predicate(interaction: discord.Interaction) -> bool:
        # 管理者権限チェック
        if interaction.user.guild_permissions.administrator:
            return True
        
        # 特定のロールチェック
        # interaction.user は Member または User。Memberの場合のみroles属性がある。
        if isinstance(interaction.user, discord.Member):
            role_id = 1468589563323744338
            if any(role.id == role_id for role in interaction.user.roles):
                return True
        
        return False

    return app_commands.check(predicate)
