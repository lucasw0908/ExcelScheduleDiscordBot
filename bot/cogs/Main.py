import discord
from discord.ext import commands
from ..utils.embed import need_help

class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emojis = None

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name="Excel啦啦啦!!!")) 
        print(" * Discord bot : Started!")
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx: discord.ApplicationContext, err: discord.ApplicationCommandError):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
            
        await ctx.send(f"``` * {err}```")
        await ctx.send(embed=need_help(emojis=self.emojis))
            
def setup(bot: commands.Bot):
    bot.add_cog(Main(bot))