import discord
from discord.ext import commands
from pathlib import Path
import threading
import os

from .config import TOKEN
from .utils.help import Help

class DiscordBotSync(commands.Bot):
    """The discord bot object."""
    
    def __init__(self, **options) -> None:
        super().__init__(self, **options)
        self.command_prefix = commands.when_mentioned_or("%")
        self.help_command = Help()
      
    def load(self) -> None:
        """Load all cogs."""

        for cog in [p.stem for p in Path(os.path.abspath(os.path.dirname(__file__))).glob("./cogs/*.py")]:
            try:
                self.load_extension(f"bot.cogs.{cog}")
                print(f" * Discrod bot : Loaded {cog}")
            except Exception as e:
                print(f" * Discrod bot : Loaded {cog} fail!")
                print(e)
            
        print(f" * Discrod bot : Loading completed!")
        
    def run_in_thread(self) -> None:
        def _run():
            self.load()
            self.run(TOKEN)
        self.bot_run_func = threading.Thread(target=_run, daemon=True)
        self.bot_run_func.start()
        
bot = DiscordBotSync(intents=discord.Intents.all())