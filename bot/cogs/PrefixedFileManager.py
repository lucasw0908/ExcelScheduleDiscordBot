import discord
from discord.ext import commands

from ..utils.excel import excel
from ..utils.embed import EmbedMaker

class PrefixedFileManager(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emojis = None
        
          
    @commands.command()
    @commands.has_role("管理員")
    async def create(self, ctx: discord.ApplicationContext, *, name):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
            
        excel.create_new_file(name)
        await ctx.send(embed=EmbedMaker(status=True, emojis=self.emojis, description=f'_**班表"{name}"已建立**_'))
        
    
    @commands.command()
    @commands.has_role("管理員")
    async def change(self, ctx: discord.ApplicationContext, *, name):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
            
        success, oldname = excel.change_target_file(name)
        if oldname==name:
            await ctx.send(embed=EmbedMaker(status=False, emojis=self.emojis, description=f'_**班表已經是"{name}"了喔!**_'))
        elif success:
            await ctx.send(embed=EmbedMaker(status=True, emojis=self.emojis, description=f'_**已將班表從"{oldname}"變更至"{name}"**_'))
        else:
            await ctx.send(embed=EmbedMaker(status=False, emojis=self.emojis, description=f'_**在將班表變更至"{name}"時發生了錯誤**_'))
            
            
def setup(bot: commands.Bot):
    bot.add_cog(PrefixedFileManager(bot))