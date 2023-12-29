import discord
from discord.ext import commands

from ..utils.excel import excel
from ..utils.storage import Storage
from ..utils.embed import EmbedMaker
from ..utils.module import FindAllFiles


class SlashBaseCommands(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emojis = None
               
               
    @commands.slash_command(name="暱稱設定", description="設定班表內使用的暱稱")
    async def nickname(self, ctx: discord.ApplicationContext, 暱稱: discord.Option(str, max_length=16)):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
            
        Storage.set_nickname({"id": ctx.author.id, "nickname": 暱稱})
        await ctx.respond(embed=EmbedMaker(status=True, emojis=self.emojis, description=f"_**暱稱[{暱稱}]設定完畢!**_"))
                
        
    @commands.slash_command(name="p", description="計算並設定倍率")
    async def p(
        self, 
        ctx: discord.ApplicationContext, 
        p1: discord.Option(float, min_value=0),
        p2: discord.Option(float, min_value=0),
        p3: discord.Option(float, min_value=0),
        p4: discord.Option(float, min_value=0),
        p5: discord.Option(float, min_value=0)
        ):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
            
        all_p = round(p1+1+(p2+p3+p4+p5)/5, 2)
        Storage.set_p({"id": ctx.author.id, "p": all_p})
        
        await ctx.respond(embed=EmbedMaker(status=True, emojis=self.emojis, description=f"_**您的倍率為: {all_p}!**_"))
        
        
    @commands.slash_command(name="查看目前班表", description="下載目前班表資訊")
    async def check_target_calendar(self, ctx: discord.ApplicationContext):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
            
        filepath, filename = excel.get_excel_file_information()
        excelfile = discord.File(filepath)
        await ctx.respond(embed=EmbedMaker(status=True, emojis=self.emojis, description=f'_**成功獲取班表"{filename}"**_'), file=excelfile)
        
        
    @commands.slash_command(name="排班", description="排定班表")
    async def set_calendar(
        self, 
        ctx: discord.ApplicationContext, 
        月份: discord.Option(int, min_value=1, max_value=12), 
        日期: discord.Option(int, min_value=1, max_value=31), 
        時間: discord.Option(int, min_value=0, max_value=23),
        時間2: discord.Option(int, min_value=0, max_value=23)
        ):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
        
        nickname = Storage.find("nickname", ctx.author.id)
        p = Storage.find("p", ctx.author.id)
        if nickname is None:
            await ctx.respond(embed=EmbedMaker(status=False, emojis=self.emojis, description=f"_**您尚未設定暱稱!**_"))
            return
        
        if p is None:
            await ctx.respond(embed=EmbedMaker(status=False, emojis=self.emojis, description=f"_**您尚未設定倍率!**_"))
            return
        
        excel.save_information(month=月份, date=日期, t1=時間, t2=時間2, nick=nickname, p=p)
        await ctx.respond(embed=EmbedMaker(status=True, emojis=self.emojis, description=f"_**設定完畢，{nickname}將於{月份}月{日期}日{時間}:00-{時間2}:00進行排班**_"))
            
            
    @commands.slash_command(name="移除排班", description="從班表移除排班")
    async def remove_calendar(
        self, 
        ctx: discord.ApplicationContext, 
        月份: discord.Option(int, min_value=1, max_value=12), 
        日期: discord.Option(int, min_value=1, max_value=31)
        ):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
        
        nickname = Storage.find("nickname", ctx.author.id)
        
        if nickname is None:
            await ctx.respond(embed=EmbedMaker(status=False, emojis=self.emojis, description=f"_**您尚未設定暱稱!**_"))
            return
        
        status = excel.remove_information(month=月份, date=日期, nick=nickname)
        if status:
            await ctx.respond(embed=EmbedMaker(status=status, emojis=self.emojis, description=f"_**已移除{nickname}於{月份}月{日期}日的排班**_"))
        else:
            await ctx.respond(embed=EmbedMaker(status=status, emojis=self.emojis, description=f"_**{nickname}於{月份}月{日期}日並沒有排班!**_"))
        
        
    @commands.slash_command(name="查看班表列表", description="查看班表列表")
    async def check_calendar_list(self, ctx: discord.ApplicationContext):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
            
        filelist = FindAllFiles("xlsx")
        embed = discord.Embed(title=f'**班表資訊{self.emojis["animation_search"]}**', description="_查看所有班表資訊_", color=discord.Color.blue())
        
        for index, f in enumerate(filelist):
            
            if f == excel.get_target_file_name():
                embed.add_field(name=f'**{self.emojis["animation_arrow"]}班表{index+1}:{f}**', value="", inline=False)
            
            else:
                embed.add_field(name=f"**班表{index+1}:{f}**", value="", inline=False)
            
        await ctx.respond(embed=embed)
        
        
    @commands.slash_command(name="查班", description="查詢自己在指定日期的排班")
    async def check(
        self, 
        ctx: discord.ApplicationContext, 
        月份: discord.Option(int, min_value=1, max_value=12), 
        日期: discord.Option(int, min_value=1, max_value=31)
        ):
        
        if not self.emojis:
            self.emojis: {str: str} = {e.name:str(e) for e in ctx.bot.emojis}
            
        nickname = Storage.find("nickname", ctx.author.id)
        p = Storage.find("p", ctx.author.id)
        
        if nickname is None:
            await ctx.respond(embed=EmbedMaker(status=False, emojis=self.emojis, description=f"_**您尚未設定暱稱!**_"))
            return
        
        if p is None:
            await ctx.respond(embed=EmbedMaker(status=False, emojis=self.emojis, description=f"_**您尚未設定倍率!**_"))
            return
            
        infomation = excel.get_information(month=月份, date=日期, nick=nickname)
        
        embed = discord.Embed(title=f'{nickname}的排班資訊{self.emojis["animation_search"]}' , color=discord.Color.blue())
        for info in infomation:
            embed.add_field(name="**倍率**", value=f'_{info["p"]}_', inline=True)
            embed.add_field(name="**日期**", value=f'_{info["month"]}/{info["date"]}_', inline=True)
            embed.add_field(name="**時間**", value=f'_{info["timerange"]}_', inline=True)
            
        await ctx.respond(embed=embed)
            
            
def setup(bot: commands.Bot):
    bot.add_cog(SlashBaseCommands(bot))