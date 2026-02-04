import discord
from discord import app_commands
import sys
import os
from .group import admin_group, is_admin_or_specific_role

@admin_group.command(name="restart", description="ボットを再起動します。")
@is_admin_or_specific_role()
async def restart(interaction: discord.Interaction):
    """ボットを再起動します。"""
    await interaction.response.send_message("ボットを再起動しています...", ephemeral=True)
    print("/admin restart 経由で再起動しています...")
    sys.exit(0) # ループを通常通り継続させるために 0 で終了
