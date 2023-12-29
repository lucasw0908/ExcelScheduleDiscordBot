import discord
from discord.ext import commands

class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name="Excel啦啦啦!!!")) 
        print(" * Discord bot : Started!")
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx: discord.ApplicationContext, err: discord.ApplicationCommandError):
        await ctx.send(f"```{err}```")
            
def setup(bot: commands.Bot):
    bot.add_cog(Main(bot))