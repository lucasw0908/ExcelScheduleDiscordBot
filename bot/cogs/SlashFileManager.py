import discord
from discord.ext import commands

from ..utils.excel import excel
from ..utils.module import FindAllFiles
from ..utils.embed import EmbedMaker

class SlashFileManager(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emojis = None
        
        
    def choice(ctx: discord.AutocompleteContext):
        choice_list = FindAllFiles("xlsx")
        return choice_list
        
        
    @commands.slash_command(name="創建班表", description="創建一個新的班表")
    @commands.has_role("管理員")
    async def create_calendar(self, ctx: discord.ApplicationContext, name: discord.Option(str, max_length=16)):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
            
        excel.create_new_file(name)
        await ctx.respond(embed=EmbedMaker(status=True, emojis=self.emojis, description=f'_**班表"{name}"已建立**_'))
        
    
    @commands.slash_command(name="變更班表", description="變更目前班表")
    @commands.has_role("管理員")
    async def change_calendar(self, ctx: discord.ApplicationContext, name: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(choice))):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
            
        success, oldname = excel.change_target_file(name)
        if oldname==name:
            await ctx.respond(embed=EmbedMaker(status=False, emojis=self.emojis, description=f'_**班表已經是"{name}"了喔!**_'))
        elif success:
            await ctx.respond(embed=EmbedMaker(status=True, emojis=self.emojis, description=f'_**已將班表從"{oldname}"變更至"{name}"**_'))
        else:
            await ctx.respond(embed=EmbedMaker(status=False, emojis=self.emojis, description=f'_**在將班表變更至"{name}"時發生了錯誤**_'))
            
            
def setup(bot: commands.Bot):
    bot.add_cog(SlashFileManager(bot))