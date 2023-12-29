import discord
from .command_list import command_list

class EmbedMaker():
    def __new__(self, status: bool, emojis: {str: str}, description: str):
        self.embed = discord.Embed(description=description)
        
        if status:
            self.embed.title = f'**設定成功{emojis["animation_yes"]}**'
            self.embed.color = discord.Color.green()
        else:
            self.embed.title = f'**設定失敗{emojis["animation_no"]}**'
            self.embed.color = discord.Color.red()
            
        return self.embed
    
def need_help(emojis: {str: str}):
    return EmbedMaker(status=False, emojis=emojis, description=f'**輸入資料有誤，如需幫助請使用%help**')

def help():
    embed = discord.Embed(title=f'指令列表⚙️', description="_所有指令的名稱與說明_", color=discord.Color.purple())
    embed.add_field(name="_*表示管理員專用指令(使用時不用把它打出來)_", value="", inline=False)
    for key in command_list.keys():
        embed.add_field(name=f"**%{key}**", value=f"_**{command_list[key]}**_", inline=False)
        
    return embed