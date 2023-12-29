import discord
from discord.ext import commands

from ..utils.excel import excel
from ..utils.storage import p_storage, nickname_storage
from ..utils.embed import EmbedMaker, need_help
from ..utils.module import FindAllFiles
from ..utils.input import get_date

class PrefixedBaseCommands(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emojis = None
               
               
    @commands.command()
    async def nick(self, ctx: discord.ApplicationContext, *, nickname):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
            
        nickname_storage.nickname = {"id": ctx.author.id, "nickname": nickname}
        await ctx.send(embed=EmbedMaker(status=True, emojis=self.emojis, description=f"_**nickname[{nickname}]設定完畢!**_"))
                
        
    @commands.command()
    async def p(self, ctx: discord.ApplicationContext, p1, p2, p3, p4, p5):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
        
        all_p = round(p1+1+(p2+p3+p4+p5)/5, 2)
        p_storage.p = {"id": ctx.author.id, "p": all_p}
        
        await ctx.send(embed=EmbedMaker(status=True, emojis=self.emojis, description=f"_**您的倍率為: {all_p}!**_"))
        
        
    @commands.command()
    async def download(self, ctx: discord.ApplicationContext):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
            
        filepath, filename = excel.get_information()
        excelfile = discord.File(filepath)
        await ctx.send(embed=EmbedMaker(status=True, emojis=self.emojis, description=f'_**成功獲取班表"{filename}"**_'), file=excelfile)
        
        
    @commands.command()
    async def c(
        self, 
        ctx: discord.ApplicationContext, 
        month: int, 
        date: int, 
        time: int,
        time2: int
        ):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
        
        nickname = nickname_storage.find(ctx.author.id)
        p = p_storage.find(ctx.author.id)
        
        if nickname is None:
            await ctx.respond(embed=EmbedMaker(status=False, emojis=self.emojis, description=f"_**您尚未設定暱稱!**_"))
            return
        
        if p is None:
            await ctx.respond(embed=EmbedMaker(status=False, emojis=self.emojis, description=f"_**您尚未設定倍率!**_"))
            return
        
        excel.save_information(month=month, date=date-1, t1=time, t2=time2, nick=nickname)
        await ctx.send(embed=EmbedMaker(status=True, emojis=self.emojis, description=f"_**設定完畢，{nickname}將於{month}月{date}日{time}:00-{time2}:00進行排班**_"))
            
            
    @commands.command()
    async def remove(self, ctx: discord.ApplicationContext, *, message):
        
        nickname = nickname_storage.find(ctx.author.id)
        
        if nickname is None:
            await ctx.send(embed=EmbedMaker(status=False, emojis=self.emojis, description=f"_**您尚未設定暱稱!**_"))
            return
        
        month, date = get_date(message)
        
        if month is None or date is None:
            await ctx.send(embed=need_help(self.emojis))
            return
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
        
        status = excel.remove_information(month=month, date=date, nick=nickname)
        if status:
            await ctx.send(embed=EmbedMaker(status=status, emojis=self.emojis, description=f"_**已移除{nickname}於{month}月{date}日的排班**_"))
        else:
            await ctx.send(embed=EmbedMaker(status=status, emojis=self.emojis, description=f"_**{nickname}於{month}月{date}日並沒有排班!**_"))
        
        
    @commands.command()
    async def list(self, ctx: discord.ApplicationContext):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
            
        filelist = FindAllFiles("xlsx")
        embed = discord.Embed(title=f'**班表資訊**{self.emojis["animation_search"]}', description="_查看所有班表資訊_", color=discord.Color.blue())
        
        for index, f in enumerate(filelist):
            
            if f == excel.get_target_file_name():
                embed.add_field(name=f'**{self.emojis["animation_arrow"]}班表{index+1}:{f}**', value="", inline=False)
            
            else:
                embed.add_field(name=f"**班表{index+1}:{f}**", value="", inline=False)
            
        await ctx.send(embed=embed)
        
        
    @commands.command()
    async def check(self, ctx: discord.ApplicationContext, *, message):
                    
        nickname = nickname_storage.find(ctx.author.id)
        p = p_storage.find(ctx.author.id)
        
        if nickname is None:
            await ctx.respond(embed=EmbedMaker(status=False, emojis=self.emojis, description=f"_**您尚未設定暱稱!**_"))
            return
        
        if p is None:
            await ctx.respond(embed=EmbedMaker(status=False, emojis=self.emojis, description=f"_**您尚未設定倍率!**_"))
            return
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
        
        month, date = get_date(message)
            
        if month is None or date is None:
            await ctx.send(embed=need_help(self.emojis))
            return

        infomation = excel.get_information(month=month, date=date, nick=nickname)

        embed = discord.Embed(title=f'{nickname}的排班資訊{self.emojis["animation_search"]}' , color=discord.Color.blue())
        for info in infomation:
            embed.add_field(name="**倍率**", value=f'_{info["p"]}_', inline=True)
            embed.add_field(name="**date**", value=f'_{info["month"]}/{info["date"]}_', inline=True)
            embed.add_field(name="**時間**", value=f'_{info["timerange"]}_', inline=True)
            
        await ctx.send(embed=embed)
            
            
def setup(bot: commands.Bot):
    bot.add_cog(PrefixedBaseCommands(bot))