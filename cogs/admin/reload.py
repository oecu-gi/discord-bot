import discord
from discord.ext import commands
import os
from .group import admin_group, is_admin_or_specific_role

# 共有グループにコマンドを登録する
@admin_group.command(name="reload", description="全てのCogをリロードし、コマンドツリーを同期します。")
@is_admin_or_specific_role()
async def reload(interaction: discord.Interaction):
    """全てのCogをリロードし、コマンドツリーを同期します。"""
    # botインスタンスを取得
    bot = interaction.client
    
    await interaction.response.defer(ephemeral=True)
    
    results = ["🚀 リロード処理を開始します..."]
    msg = await interaction.followup.send("\n".join(results), wait=True)
    
    async def update_msg(text):
        results.append(text)
        await msg.edit(content="\n".join(results))

    await update_msg("🔄 Cogの再読み込みを開始します...")
    # Cogをリロード
    for root, dirs, files in os.walk('cogs'):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                path = os.path.join(root, file)
                module = path.replace('.py', '').replace(os.path.sep, '.').replace('/', '.')
                
                try:
                    await bot.reload_extension(module)
                    await update_msg(f"✅ 再読み込み完了: `{module}`")
                except commands.errors.ExtensionNotLoaded:
                    try:
                        await bot.load_extension(module)
                        await update_msg(f"🆕 読み込み完了: `{module}`")
                    except commands.errors.NoEntryPointError:
                            pass # Cogではない
                    except Exception as e:
                        await update_msg(f"❌ `{module}` の再読み込みに失敗しました: {e}")
                except commands.errors.NoEntryPointError:
                    pass # Cogではない
                except Exception as e:
                    await update_msg(f"❌ `{module}` の再読み込みに失敗しました: {e}")

    # コマンドを同期
    await update_msg("🔄 コマンドの同期を開始します...")
    try:
        # 同期前のコマンドを取得
        old_commands = await bot.tree.fetch_commands()
        old_cmd_names = {cmd.name for cmd in old_commands}

        # 同期実行
        new_commands = await bot.tree.sync()
        new_cmd_names = {cmd.name for cmd in new_commands}

        await update_msg("🔄 グローバルコマンドが同期されました")

        # 差分比較
        added = new_cmd_names - old_cmd_names
        removed = old_cmd_names - new_cmd_names

        if added:
            await update_msg(f"🆕 追加されたコマンド: {', '.join(added)}")
        if removed:
            await update_msg(f"🗑️ 削除されたコマンド: {', '.join(removed)}")
        if not added and not removed:
            await update_msg("✨ コマンドに変更はありませんでした")
    except Exception as e:
        await update_msg(f"❌ コマンドの同期に失敗しました: {e}")
