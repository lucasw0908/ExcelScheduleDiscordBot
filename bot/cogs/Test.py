import discord
from discord.ext import commands
from ..utils.storage import p_storage, nickname_storage

class Test(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emojis = None

    @commands.slash_command(name="test", description="test")
    async def test(self, ctx: discord.ApplicationContext):
        
        nickname_storage.nickname = {"id": ctx.author.id, "nickname": "000"}
        p_storage.p = {"id": ctx.author.id, "p": 1.87}
        
        await ctx.respond("test")
            
def setup(bot: commands.Bot):
    bot.add_cog(Test(bot))