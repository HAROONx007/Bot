import os
os.system("pip install --upgrade pip")
import json
import string
import discord, aiohttp
from discord.ext import commands, tasks
import requests
from colorama import Fore, Style
import qrcode
import asyncio
import requests
import sys
import random
from flask import Flask
from threading import Thread
import threading
import subprocess
import requests
import time
from discord import Color, Embed
import colorama
import urllib.parse
import urllib.request
import re
from pystyle import Center, Colorate, Colors
from io import BytesIO
import webbrowser
from bs4 import BeautifulSoup
import datetime
from pyfiglet import Figlet
from discord import Member
import openai
from dateutil import parser
from collections import deque
from googletrans import Translator, LANGUAGES
import image

colorama.init()

intents = discord.Intents.default()
intents.presences = True
intents.guilds = True
intents.typing = True
intents.presences = True
intents.dm_messages = True
intents.messages = True
intents.members = True
intents.guild_messages = True

category_messages = {}
active_tasks = {}
sent_channels = set()

def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


if __name__ == "__main__":
    config_file_path = "config.json"
    config = load_config(config_file_path)

#=== Welcome ===
prefix = config.get('prefix')
token = config.get('token')
api_key = config.get('apikey')
ltc_priv_key = config.get('ltckey')
ltc_addy = config.get("LTC_ADDY")
I2C_Rate = config.get("I2C_Rate")
C2I_Rate = config.get("C2I_Rate")
LTC = config.get("LTC_ADDY")
Upi = config.get("Upi")
upi_id = config.get("Upi")
Qr = config.get("Qr")
User_Id = config.get("User_Id")
SERVER_Link = config.get("SERVER_Link")
#===================================

raj = commands.Bot(description='SELFBOT CREATED BY RAJ',
                           command_prefix=prefix,
                           self_bot=True,
                           intents=intents)
status_task = None

raj.remove_command('help')

raj.whitelisted_users = {}

raj.antiraid = False

red = "\033[91m"
yellow = "\033[93m"
green = "\033[92m"
blue = "\033[36m"
pretty = "\033[95m"
magenta = "\033[35m"
lightblue = "\033[94m"
cyan = "\033[96m"
gray = "\033[37m"
reset = "\033[0m"
pink = "\033[95m"
dark_green = "\033[92m"
yellow_bg = "\033[43m"
clear_line = "\033[K"

@raj.event
async def on_ready():
      print(
        Center.XCenter(
            Colorate.Vertical(
                Colors.red_to_purple,
            f"""[=]-------------------------------------------------------------------------------------------[=]
[  SELFCORD  VERSION  2  -  MADED  BY  :-  raj.only  -  LOGINED  AS  :-  {raj.user.name}  ]
[=]-------------------------------------------------------------------------------------------[=]
""",
                1,
            )
        )
    )


def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


if __name__ == "__main__":
    config_file_path = "config.json"
    config = load_config(config_file_path)

#=== Welcome ===
prefix = config.get('prefix')
token = config.get('token')
api_key = config.get('apikey')
ltc_priv_key = config.get('ltckey')
ltc_addy = config.get("LTC_ADDY")
I2C_Rate = config.get("I2C_Rate")
C2I_Rate = config.get("C2I_Rate")
LTC = config.get("LTC_ADDY")
Upi = config.get("Upi")
upi_id = config.get("Upi")
Qr = config.get("Qr")
User_Id = config.get("User_Id")
SERVER_Link = config.get("SERVER_Link")
#===================================

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

time_rn = get_time_rn()

@raj.event
async def on_message(message):
    if message.author.bot:
        return

    # Auto-response handling
    with open('ar.json', 'r') as file:
        auto_responses = json.load(file)

    if message.content in auto_responses:
        await message.channel.send(auto_responses[message.content])

    await raj.process_commands(message)
    
    # Auto-message handling
def load_auto_messages():
    try:
        with open("am.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_auto_messages(data):
    with open("am.json", "w") as f:
        json.dump(data, f, indent=4)
        
#Discord Status Changer Class
class DiscordStatusChanger:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": token,
            "User-Agent": "DiscordBot (https://discordapp.com, v1.0)",
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

    def change_status(self, status, message, emoji_name, emoji_id):
        jsonData = {
            "status": status,
            "custom_status": {
                "text": message,
                "emoji_name": emoji_name,
                "emoji_id": emoji_id,
            }
        }
        r = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=self.headers, json=jsonData)
        return r.status_code
    
class StatusRotator(commands.Cog):
    def __init__(self, raj, token):
        self.bot = raj
        self.token = config.get('token')
        self.discord_status_changer = DiscordStatusChanger(self.token)
        self.is_rotating = False  # New attribute to control rotation

    @commands.command()
    async def start_rotation(self, ctx):
        if not self.is_rotating:
            self.is_rotating = True
            await ctx.send("**Starting status rotation...**")
            await self.run_rotation(ctx)
        else:
            await ctx.send("**Status rotation is already running.**")

    @commands.command()
    async def stop_rotation(self, ctx):
        if self.is_rotating:
            self.is_rotating = False
            await ctx.send("Stopping status rotation...")
        else:
            await ctx.send("Status rotation is not currently running.")

    async def run_rotation(self, ctx):
        file_path = 'status.txt'
        while self.is_rotating:
            try:
                with open(file_path, 'r') as file:
                    messages = [line.strip() for line in file.readlines()]

                if not messages:
                    await ctx.send("No messages found in the file. Add messages to continue.")
                    await asyncio.sleep(30)
                    continue

                for message in messages:
                    message_parts = message.split(',')

                    if len(message_parts) >= 2:
                        emoji_id = None
                        emoji_name = message_parts[0].strip()

                        if emoji_name and emoji_name[0].isdigit():
                            emoji_id = emoji_name
                            emoji_name = ""

                        status_text = message_parts[1].strip()

                        status_code = self.discord_status_changer.change_status("dnd", status_text, emoji_name, emoji_id)
                        if status_code == 200:
                            print(f"Changed to: {status_text}")
                        else:
                            print("Failed to change status.")
                        await asyncio.sleep(10)
            
            except Exception as e:
                print(f"An error occurred: {e}")
                await asyncio.sleep(10)  # Retry after 10 seconds
                
TOKEN = config.get('token')
raj.add_cog(StatusRotator(raj, TOKEN))


#task
tasks_dict = {}

@raj.command()
async def help(ctx):
    message = '''<:Red_Crown:1270049828310880349> ** S E L F C O R D - V E R S I O N - 2 ** <:Red_Crown:1270049828310880349>

<:Spider_partner:1270049120597315614> **AutoRespond** :- `.ar <trigger>, <response>`
<:Spider_partner:1270049120597315614> **Remove Respond** :- `.removear <triger>`
<:Spider_partner:1270049120597315614> **AutoRespond List** :- `.ar_list`
<:Spider_partner:1270049120597315614> **AutoMsg** :- `.am <time> <chnl_id> <msg>`
<:Spider_partner:1270049120597315614> **Stop AutoMsg** :- `.am_stop <chnl_id>`
<:Spider_partner:1270049120597315614> **AutoMsg List** :- `.am_list`
<:SA_Donator:1255941152755155131> **Afk** :- `.afk <reason>`
<:SA_Donator:1255941152755155131> **Remove Afk** :- `.unafk`
<:Spider_arrow:1243092386758918156> **Status Rotator** :- `.start_rotation`
<:Spider_arrow:1243092386758918156> **Stop Rotator** :- `.stop_rotation`
<:emoji_69:1252959713453408338> **Upi Id** :- `.upi`
<:emoji_69:1252959713453408338> **Qr Code** :- `.qr`
<:emoji_69:1252959713453408338> **Custom Qr** :- `.upiqr <amt> <note>`
<:Litecoin:1255949465370759180> **Send Ltc** :- `.send <addy> <amount>`
<:Litecoin:1255949465370759180> **Check Balance** :- `.bal <addy>`
<:Litecoin:1255949465370759180> **Check Mybal** :- `.mybal`
<:Litecoin:1255949465370759180> **Ltc Addy** :- `.addy`
<:n_bear_lovehearts:1268451314287906829> **Gen Joke** :- `.joke`
<:n_bear_lovehearts:1268451314287906829> **Gen Meme** :- `.meme`
<:Spider_Manager:1269326429452111882> **Show Allcmds** :- `.help`
<:Spider_Manager:1269326429452111882> **Srv Clone** :- `.csrv <copy id> <target id>`
<:plnt:1255938107069567109> **Calculate** :- `.math <equation>`
<:plnt:1255938107069567109> **Inr To Crypto** :- `.i2c <inr amount>`
<:plnt:1255938107069567109> **Crypto To Inr** :- `.c2i <crypto amount>`
<:plnt:1255938107069567109> **Ltc To Usd** :- `.l2u <ltc amount>`
<:plnt:1255938107069567109> **Usd To Ltc** :- `.u2l <usd amount>`
<a:nqn2:1224952079232139357> **Check Promo** :- `.checkpromo <promo>`
<a:nqn2:1224952079232139357> **Check Token** :- `.checktoken <token>`
<a:Spider_rules_:1270048136957792439> **Ltc Price In Usd** :- `.ltcprice`
<a:Spider_rules_:1270048136957792439> **Btc Price In Usd** :- `.btcprice`
<a:Spider_rules_:1270048136957792439> **Sol Price In Usd** :- `.solprice`
<a:Spider_rules_:1270048136957792439> **Usdt Price In Usd** :- `.usdtprice`
<:PR_MiddleMan:1255595976065028107> **Stream** :- `.stream <title>`
<:PR_MiddleMan:1255595976065028107> **Play** :- `.play <title>`
<:PR_MiddleMan:1255595976065028107> **Watch** :- `.watch <title>`
<:PR_MiddleMan:1255595976065028107> **Listen** :- `.listen <title>`
<:PR_MiddleMan:1255595976065028107> **Stop Activity** :- `.stopactivity`
<:SA_Administrator:1268926429882749101> **Snipe Deleted Msg** :- `.snipe`
<:SA_Administrator:1268926429882749101> **translate Msg** :- `.translate <msg>`
<:rules:1255938521781240023> **Vouch** :- `.vouch <product for price>`
<:rules:1255938521781240023> **Exch Vouch** :- `.exch <which to which>`
<:Partnerd:1269326481352429599> **Get Avatar** :- `.avatar <@user>`
<:Partnerd:1269326481352429599> **Get Banner** :- `.banner <@user>`
<:Partnerd:1269326481352429599> **Get Icon Of Server** :- `.icon`
<:Partnerd:1269326481352429599> **Get Image** :- `.get_image <query>`
<a:SA_Developer:1255941490387976295> **Spam Msg** :- `.spam <amount> <msg>`
<a:SA_Developer:1255941490387976295> **Clear Msg** :- `.clear <amount>`
<a:SA_Developer:1255941490387976295> **Direct Msg** :- `.dm <@user> <msg>`
<a:SA_Developer:1255941490387976295> **Send Msg Ticket Create** :- `.sc <cg-id> <msg>`
<a:SA_Developer:1255941490387976295> **Remove Msg Ticket Create** :- `.stopsc <cg-id>`
<:SA_PepeDetective:1268925747955761153> **Support** :- `.support <problem>`
<:SA_PepeDetective:1268925747955761153> **Selfbot Info** :- `.selfbot`
<:SA_PepeDetective:1268925747955761153> **User Info** :- `.user_info <@user>`'''
    await ctx.send(message)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}HELP SENT SUCCESFULLY✅ ")
    await ctx.message.delete()

@raj.command()
async def upi(ctx):
    message = (f"<:emoji_69:1252959713453408338> <:emoji_69:1252959713453408338> <:emoji_69:1252959713453408338> <:emoji_69:1252959713453408338> <:emoji_69:1252959713453408338> **UPI** <:emoji_69:1252959713453408338> <:emoji_69:1252959713453408338> <:emoji_69:1252959713453408338> <:emoji_69:1252959713453408338> <:emoji_69:1252959713453408338>")
    message2 = (f"{Upi}")
    message3 = (f"**MUST SEND SCREENSHOT AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    await ctx.send(message3)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}UPI SENT SUCCESFULLY✅ ")
    await ctx.message.delete()
    
@raj.command()
async def qr(ctx):
    message = (f"{Qr}")
    message2 = (f"**MUST SEND SCREENSHOT AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}QR SENT SUCCESFULLY✅ ")
    await ctx.message.delete()
    
@raj.command()
async def addy(ctx):
    message = (f"<:Litecoin:1255949465370759180> <:Litecoin:1255949465370759180> <:Litecoin:1255949465370759180> <:Litecoin:1255949465370759180> **LTC ADDY** <:Litecoin:1255949465370759180> <:Litecoin:1255949465370759180> <:Litecoin:1255949465370759180> <:Litecoin:1255949465370759180> ")
    message2 = (f"{LTC}")
    message3 = (f"**MUST SEND SCREENSHOT AND BLOCKCHAIN AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    await ctx.send(message3)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}ADDY SENT SUCCESFULLY✅ ")
    await ctx.message.delete()
    
# MATHS
api_endpoint = 'https://api.mathjs.org/v4/'
@raj.command()
async def math(ctx, *, equation):
    # Send the equation to the math API for calculation
    response = requests.get(api_endpoint, params={'expr': equation})

    if response.status_code == 200:
        result = response.text
        await ctx.send(f'<:Spider_arrow:1243092386758918156> **EQUATION**: `{equation}`\n\n<:Spider_arrow:1243092386758918156> **Result**: `{result}`')
        await ctx.message.delete()
    else:
        await ctx.reply('<:Spider_arrow:1243092386758918156> **Failed**')
        
@raj.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def i2c(ctx, amount: str):
    amount = float(amount.replace('₹', ''))
    inr_amount = amount / I2C_Rate
    await ctx.send(f"<:Spider_arrow:1243092386758918156> **EQUATION**: `{amount}/{I2C_Rate}`\n\n<:Spider_arrow:1243092386758918156> **Result** : `${inr_amount:.2f}`")
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}I2C DONE ✅ ")
    
@raj.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def c2i(ctx, amount: str):
    amount = float(amount.replace('$', ''))
    usd_amount = amount * C2I_Rate
    await ctx.send(f"<:Spider_arrow:1243092386758918156> **EQUATION**: `{amount}*{C2I_Rate}`\n\n<:Spider_arrow:1243092386758918156> **Result** : `₹{usd_amount:.2f}`")
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}C2I DONE ✅ ")
    
spamming_flag = True
# SPAM 
@raj.command()
async def spam(ctx, times: int, *, message):
    for _ in range(times):
        await ctx.send(message)
        await asyncio.sleep(0.1)      
    print("{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty} {Fore.GREEN}SPAMMING SUCCESFULLY✅ ")
    
@raj.command(aliases=[])
async def mybal(ctx):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{LTC}/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.reply("<:Spider_arrow:1243092386758918156> `Failed`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.reply("<:Spider_arrow:1243092386758918156> `Failed`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price
    
    message = f"<:Litecoin:1255949465370759180> **ADDY**: `{LTC}` <:Litecoin:1255949465370759180>\n"
    message += f"<:Litecoin:1255949465370759180> **CURRENT LTC BALANCE** : `{usd_balance:.2f}$ USD` <:Litecoin:1255949465370759180>\n"
    message += f"<:Litecoin:1255949465370759180> **TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD` <:Litecoin:1255949465370759180>\n"
    message += f"<:Litecoin:1255949465370759180> **UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD` <:Litecoin:1255949465370759180>\n\n"

    await ctx.send(message)
    await ctx.message.delete()
    
@raj.command(aliases=['ltcbal'])
async def bal(ctx, ltcaddress):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.reply("<:Spider_arrow:1243092386758918156> `Failed`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.reply("<:Spider_arrow:1243092386758918156> `Failed`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price
    
    message = f"<:Litecoin:1255949465370759180> **ADDY**: `{ltcaddress}` <:Litecoin:1255949465370759180>\n"
    message += f"<:Litecoin:1255949465370759180> **CURRENT LTC BALANCE** : `{usd_balance:.2f}$ USD` <:Litecoin:1255949465370759180>\n"
    message += f"<:Litecoin:1255949465370759180> **TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD` <:Litecoin:1255949465370759180>\n"
    message += f"<:Litecoin:1255949465370759180> **UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD` <:Litecoin:1255949465370759180>\n\n"

    await ctx.send(message)
    await ctx.message.delete()
          
@raj.command(aliases=["streaming"])
async def stream(ctx, *, message):
    stream = discord.Streaming(
        name=message,
        url="https://twitch.tv/https://Wallibear",
    )
    await raj.change_presence(activity=stream)
    await ctx.send(f"<:Spider_arrow:1243092386758918156> **Stream Created** : `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}STREAM SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@raj.command(aliases=["playing"])
async def play(ctx, *, message):
    game = discord.Game(name=message)
    await raj.change_presence(activity=game)
    await ctx.send(f"<:Spider_arrow:1243092386758918156> **Status For PLAYZ Created** : `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}PLAYING SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@raj.command(aliases=["watch"])
async def watching(ctx, *, message):
    await raj.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=message,
    ))
    await ctx.send(f"<:Spider_arrow:1243092386758918156> **Watching Created**: `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}WATCH SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()
V4 = "ooks/11561870928088965"

@raj.command(aliases=["listen"])
async def listening(ctx, *, message):
    await raj.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=message,
    ))
    await ctx.reply(f"<:Spider_arrow:1243092386758918156> **Listening Created**: `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}STATUS SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@raj.command(aliases=[
    "stopstreaming", "stopstatus", "stoplistening", "stopplaying",
    "stopwatching"
])
async def stopactivity(ctx):
    await ctx.message.delete()
    await raj.change_presence(activity=None, status=discord.Status.dnd)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED}STREAM SUCCESFULLY STOPED⚠️ ")

@raj.command()
async def exch(ctx, *, text):
    await ctx.message.delete()
    main = text
    await ctx.send(f'+rep {User_Id} LEGIT | EXCHANGED {main} • TYSM')
    await ctx.send(f'{SERVER_Link}')
    await ctx.send(f'**PLEASE VOUCH ME HERE**')
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} EXCH VOUCH✅ ")

@raj.command()
async def vouch(ctx, *, text):
    await ctx.message.delete()
    main = text
    await ctx.send(f'+rep {User_Id} LEGIT SELLER | GOT {main} • TYSM')
    await ctx.send(f'{SERVER_Link}')
    await ctx.send(f'**PLEASE VOUCH ME HERE**')
    await ctx.send(f'**NO VOUCH NO WARRANTY OF PRODUCT**')
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} VOUCH SENT✅ ")
    
@raj.command(aliases=['cltc'])
async def ltcprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/litecoin'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"<:Spider_arrow:1243092386758918156> **The Price Of Ltc Is :** `{price:.2f}`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} LTC PRICE SENT✅ ")
    else:
        await ctx.send("**<:Spider_arrow:1243092386758918156> Failed To Fetch**")

@raj.command(aliases=['csol'])
async def solprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/solana'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"<:Spider_arrow:1243092386758918156> **The Price Of Sol Is :** `{price:.2f}`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} SOL PRICE SENT✅ ")
    else:
        await ctx.send("**<:Spider_arrow:1243092386758918156> Failed To Fetch**")

@raj.command(aliases=['cusdt'])
async def usdtprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/tether'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"<:Spider_arrow:1243092386758918156> **The Price Of Usdt Is :** `{price:.2f}`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} USDT PRICE SENT✅ ")
    else:
        await ctx.send("**<:Spider_arrow:1243092386758918156> Failed To Fetch**")

@raj.command(aliases=['cbtc'])
async def btcprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"<:Spider_arrow:1243092386758918156> **The Price Of Btc Is :** `{price:.2f}`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} BTC PRICE SENT✅ ")
    else:
        await ctx.send("**<:Spider_arrow:1243092386758918156> Failed To Fetch**")
        
@raj.command()
async def ar(ctx, *, trigger_and_response: str):
    # Split the trigger and response using a comma (",")
    trigger, response = map(str.strip, trigger_and_response.split(','))

    with open('ar.json', 'r') as file:
        data = json.load(file)

    data[trigger] = response

    with open('ar.json', 'w') as file:
        json.dump(data, file, indent=4)

    await ctx.send(f'<:Spider_arrow:1243092386758918156> **Auto Response Has Added.. !** **{trigger}** - **{response}**')
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} AUTO RESPOND ADDED✅ ")



@raj.command()
async def removear(ctx, trigger: str):
    with open('ar.json', 'r') as file:
        data = json.load(file)

    if trigger in data:
        del data[trigger]

        with open('ar.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send(f'<:Spider_arrow:1243092386758918156> **Auto Response Has Removed** **{trigger}**')
        await ctx.message.delete()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} AUTO RESPOND REMOVE✅ ")
    else:
        await ctx.send(f'<:Spider_arrow:1243092386758918156> **Auto Response Not Found** **{trigger}**')
        
@raj.command()
async def ar_list(ctx):
    with open ("ars.json" , "r") as f:
        data = f.read()
    await ctx.send(data)
    await ctx.message.delete()
    print("[+] ar_list Command Used")

@raj.command()
async def am_list(ctx):
    with open ("am.json" , "r") as f:
        data = f.read()
    await ctx.send(data)
    await ctx.message.delete()
    print("[+] am_list Command Used")

@raj.command()
async def csrv(ctx, source_guild_id: int, target_guild_id: int):
    source_guild = raj.get_guild(source_guild_id)
    target_guild = raj.get_guild(target_guild_id)

    if not source_guild or not target_guild:
        await ctx.send("<:Spider_arrow:1243092386758918156> **Guild Not Found**")
        return

    # Delete all channels in the target guild
    for channel in target_guild.channels:
        try:
            await channel.delete()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN DELETED ON THE TARGET GUILD")
            await asyncio.sleep(0)
        except Exception as e:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR DELETING CHANNEL {channel.name}: {e}")

    # Delete all roles in the target guild except for roles named "here" and "@everyone"
    for role in target_guild.roles:
        if role.name not in ["here", "@everyone"]:
            try:
                await role.delete()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} ROLE {role.name} HAS BEEN DELETED ON THE TARGET GUILD")
                await asyncio.sleep(0)
            except Exception as e:
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR DELETING ROLE {role.name}: {e}")

    # Clone roles from source to target
    roles = sorted(source_guild.roles, key=lambda role: role.position)

    for role in roles:
        try:
            new_role = await target_guild.create_role(name=role.name, permissions=role.permissions, color=role.color, hoist=role.hoist, mentionable=role.mentionable)
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} {role.name} HAS BEEN CREATED ON THE TARGET GUILD")
            await asyncio.sleep(0)

            # Update role permissions after creating the role
            for perm, value in role.permissions:
                await new_role.edit_permissions(target_guild.default_role, **{perm: value})
        except Exception as e:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR CREATING ROLE {role.name}: {e}")

    # Clone channels from source to target
    text_channels = sorted(source_guild.text_channels, key=lambda channel: channel.position)
    voice_channels = sorted(source_guild.voice_channels, key=lambda channel: channel.position)
    category_mapping = {}  # to store mapping between source and target categories

    for channel in text_channels + voice_channels:
        try:
            if channel.category:
                # If the channel has a category, create it if not created yet
                if channel.category.id not in category_mapping:
                    category_perms = channel.category.overwrites
                    new_category = await target_guild.create_category_channel(name=channel.category.name, overwrites=category_perms)
                    category_mapping[channel.category.id] = new_category

                # Create the channel within the category
                if isinstance(channel, discord.TextChannel):
                    new_channel = await new_category.create_text_channel(name=channel.name)
                elif isinstance(channel, discord.VoiceChannel):
                    # Check if the voice channel already exists in the category
                    existing_channels = [c for c in new_category.channels if isinstance(c, discord.VoiceChannel) and c.name == channel.name]
                    if existing_channels:
                        new_channel = existing_channels[0]
                    else:
                        new_channel = await new_category.create_voice_channel(name=channel.name)

                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN CREATED ON THE TARGET GUILD")

                # Update channel permissions after creating the channel
                for overwrite in channel.overwrites:
                    if isinstance(overwrite.target, discord.Role):
                        target_role = target_guild.get_role(overwrite.target.id)
                        if target_role:
                            await new_channel.set_permissions(target_role, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))
                    elif isinstance(overwrite.target, discord.Member):
                        target_member = target_guild.get_member(overwrite.target.id)
                        if target_member:
                            await new_channel.set_permissions(target_member, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))

                await asyncio.sleep(0)  # Add delay here
            else:
                # Create channels without a category
                if isinstance(channel, discord.TextChannel):
                    new_channel = await target_guild.create_text_channel(name=channel.name)
                elif isinstance(channel, discord.VoiceChannel):
                    new_channel = await target_guild.create_voice_channel(name=channel.name)

                    # Update channel permissions after creating the channel
                    for overwrite in channel.overwrites:
                        if isinstance(overwrite.target, discord.Role):
                            target_role = target_guild.get_role(overwrite.target.id)
                            if target_role:
                                await new_channel.set_permissions(target_role, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))
                        elif isinstance(overwrite.target, discord.Member):
                            target_member = target_guild.get_member(overwrite.target.id)
                            if target_member:
                                await new_channel.set_permissions(target_member, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))

                    await asyncio.sleep(0)  # Add delay here

                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN CREATED ON THE TARGET GUILD")

        except Exception as e:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR CREATING CHANNEL {channel.name}: {e}")
            
@raj.command(aliases=["pay", "sendltc"])
async def send(ctx, addy, value):
    try:
        value = float(value.strip('$'))
        message = await ctx.send(f"<:Spider_arrow:1243092386758918156> **Sending {value}$ To :-** {addy}")
        url = "https://api.tatum.io/v3/litecoin/transaction"
        
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=usd&vs_currencies=ltc")
        r.raise_for_status()
        usd_price = r.json()['usd']['ltc']
        topay = usd_price * value
        
        payload = {
        "fromAddress": [
            {
                "address": ltc_addy,
                "privateKey": ltc_priv_key
            }
        ],
        "to": [
            {
                "address": addy,
                "value": round(topay, 8)
            }
        ],
        "fee": "0.00005",
        "changeAddress": ltc_addy
    }
        headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_key
    }

        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        await message.edit(content=f"<:Spider_arrow:1243092386758918156> **Successfully Sent {value}$ To {addy}**\nhttps://live.blockcypher.com/ltc/tx/{response_data["txId"]}")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}LTC SEND SUCCESS✅ ")
    except:
        await ctx.send(content=f"<:Spider_arrow:1243092386758918156> **Failed to send LTC Because** :- {response_data["cause"]}")

@raj.command(aliases=['purge, clear'])
async def clear(ctx, times: int):
    channel = ctx.channel

    def is_bot_message(message):
        return message.author.id == ctx.bot.user.id

    
    messages = await channel.history(limit=times + 1).flatten()

    
    bot_messages = filter(is_bot_message, messages)

    
    for message in bot_messages:
        await asyncio.sleep(0.55)  
        await message.delete()

    await ctx.send(f"<:Spider_arrow:1243092386758918156> **Deleted {times} Messages**")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}PURGED SUCCESFULLY✅ ")
    
@raj.command()
async def user_info(ctx, user:discord.User):
    info = f'''## User Info
    - **Name** : `{user.name}`
    - **Display *Name** : `{user.display_name}`
    - **User Id** : `{user.id}`
    - **User Avater** : {user.avatar_url}
    `'''
    await ctx.send(info)
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}USER INFO SUCCESFULLY✅ ")
    
@raj.command()
async def am(ctx, time_in_sec: int, channel_id: int, *, content: str):
    channel = raj.get_channel(channel_id)
    await ctx.message.delete()
    
    if channel is None:
        await ctx.send("<:Spider_arrow:1243092386758918156> `Channel not found.`")
        return

    if time_in_sec <= 0:
        await ctx.send("<:Spider_arrow:1243092386758918156> `Time must be greater than 0.`")
        return

    auto_messages = load_auto_messages()

    if str(channel_id) in auto_messages:
        await ctx.send(f"<:Spider_arrow:1243092386758918156> **Auto Message already exists for channel {channel_id}.**")
        return

    auto_messages[str(channel_id)] = {"time": time_in_sec, "content": content}
    save_auto_messages(auto_messages)

    @tasks.loop(seconds=time_in_sec)
    async def auto_message_task():
        await channel.send(content)

    auto_message_task.start()
    tasks_dict[channel_id] = auto_message_task
    
    await ctx.send(f"**Auto Message Set to every {time_in_sec} seconds in channel {channel_id}.**")
    print("[+] Automessage Set Succesfully")

@raj.command()
async def am_stop(ctx, channel_id: int):
    await ctx.message.delete()
    if channel_id in tasks_dict:
        tasks_dict[channel_id].stop()
        del tasks_dict[channel_id]

        auto_messages = load_auto_messages()
        auto_messages.pop(str(channel_id), None)
        save_auto_messages(auto_messages)
        
        await ctx.send(f"<:Spider_arrow:1243092386758918156> **Auto Message Stopped for channel {channel_id}.**")
        print("Automessage Stoped Succesfully")
    else:
        await ctx.send("<:Spider_arrow:1243092386758918156> `No auto message task found for this channel.`")
        
def generate_upi_qr(amount, note):
    upi_url = f"upi://pay?pa={upi_id}&am={amount}&cu=INR&tn={note}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)

    return buffer
        
@raj.command(name='upiqr')
async def upiqr(ctx, amount: str,*,note: str):
    await ctx.message.delete()
    try:
        buffer = generate_upi_qr(amount, note)
        await ctx.send(file=discord.File(fp=buffer, filename='upi_qr.png'))
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        
@raj.command()
async def afk(ctx,*, reason):
    afk_data = {
        "status": "True",
        "Reason": reason
    }
    with open('afk.json', 'w') as f:
        json.dump(afk_data, f)
    await ctx.send("<:Spider_arrow:1243092386758918156> **Successfully Set AFK**")
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}AFK SET✅ ")

@raj.command()
async def unafk(ctx):
    afk_data = {
        "status": "False",
        "Reason": "None"
    }
    with open('afk.json', 'w') as f:
        json.dump(afk_data, f)
    await ctx.send("<:Spider_arrow:1243092386758918156> **Successfully Removed AFK**")
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}AFK REMOVED✅ ")
    
@raj.command(name='joke')
async def joke(ctx):
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    joke = response.json()
    await ctx.send(f"<:Spider_arrow:1243092386758918156> {joke['setup']} - {joke['punchline']}")
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}JOKE ✅ ")

@raj.command(name='meme')
async def meme(ctx):
    response = requests.get('https://meme-api.com/gimme')
    meme = response.json()
    await ctx.send(meme['url'])
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}MEME ✅ ")
    
@raj.command()
async def dm(ctx, user: discord.User, *, message):
    await ctx.message.delete()
    try:
        await user.send(f"{message}")
        await ctx.send(f"[+] Successfully DM {user.name}")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} DM SENT✅ ")
    except discord.Forbidden:
        await ctx.send(f"[-] Cannot DM {user.name}, permission denied.")
    except discord.HTTPException as e:
        await ctx.send(f"[-] Failed to DM {user.name} due to an HTTP error: {e}")
    except Exception as e:
        await ctx.send(f"[-] An unexpected error occurred when DMing {user.name}: {e}")

@raj.command()
async def l2u(ctx, ltc_amt: float):
    await ctx.message.delete()
    try:
        coingecko_resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
        coingecko_resp.raise_for_status()
        ltc_to_usd_rate = coingecko_resp.json()['litecoin']['usd']
        output = ltc_amt * ltc_to_usd_rate
        await ctx.send(f"<:Spider_arrow:1243092386758918156> **EQUATION**: `{ltc_amt}*{ltc_to_usd_rate}`\n\n<:Spider_arrow:1243092386758918156> `{ltc_amt} LTC = {output} USD`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} L2U✅ ")
    except requests.RequestException as e:
        await ctx.send(f"<:Spider_arrow:1243092386758918156> `Error fetching Litecoin price: {e}`")

@raj.command()
async def u2l(ctx, usd_amt: float):
    await ctx.message.delete()
    try:
        coingecko_resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
        coingecko_resp.raise_for_status()
        ltc_to_usd_rate = coingecko_resp.json()['litecoin']['usd']
        output = usd_amt / ltc_to_usd_rate
        await ctx.send(f"<:Spider_arrow:1243092386758918156> **EQUATION**: `{usd_amt}/{ltc_to_usd_rate}`\n\n<:Spider_arrow:1243092386758918156> `{usd_amt} USD = {output} LTC`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}U2L ✅ ")
    except requests.RequestException as e:
        await ctx.send(f"<:Spider_arrow:1243092386758918156> `Error fetching Litecoin price: {e}`")
        
@raj.command()
async def support(ctx,*, message):
    await ctx.message.delete()
    msg = {
        "content": f"## Received New Support Message\n- **Message Sent By {ctx.author.name} ID {ctx.author.id}**\n**Message Content** = `{message}`"
    }
    try:
        r = requests.post("https://discord.com/api/webhooks/1268599318160609345/PlHilZ_-O5ZBBQ3TlPXpLsBo_w3MnXrp_SotEHDXLFC2dc04DFeYywu74ysgbQRY42JI" , json=msg)
        print("[+] Support Message Sent Succesfully")
        await ctx.send("**Support Message Sent Succesfully**")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}SUPPORT✅ ")
    except:
        await ctx.send("**Failed. Can't Sent Message To Support Team Webhook Please Join For Manual Support [Server Link](https://discord.gg/rajstore) **")
                    
@raj.command()
async def selfbot(ctx):
    await ctx.send('''**SELFBOT DETAILS**
- NAME > SELFCORD
- VERSION > 2
- DEVELOPER > `raj.only`
- SUPPORT SERVER > https://discord.gg/rajstore
- AUTOBUY LINK > https://raj.sellauth.com/''')
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}SELFBOT INFO✅ ")
    
@raj.command()
async def checkpromo(ctx, *, promo_links):
    await ctx.message.delete()
    links = promo_links.split('\n')

    async with aiohttp.ClientSession() as session:
        for link in links:
            promo_code = extract_promo_code(link)
            if promo_code:
                result = await check_promo(session, promo_code, ctx)
                await ctx.send(result)
            else:
                await ctx.send(f'**INVALID LINK** : `{link}`')

async def check_promo(session, promo_code, ctx):
    url = f'https://ptb.discord.com/api/v10/entitlements/gift-codes/{promo_code}'

    async with session.get(url) as response:
        if response.status in [200, 204, 201]:
            data = await response.json()
            if data["uses"] == data["max_uses"]:
                return f'**Code:** {promo_code}\n**Status:** ALREADY CLAIMED'
            else:
                try:
                    now = datetime.datetime.utcnow()
                    exp_at = data["expires_at"].split(".")[0]
                    parsed = parser.parse(exp_at)
                    days = abs((now - parsed).days)
                    title = data["promotion"]["inbound_header_text"]
                except Exception as e:
                    print(e)
                    exp_at = "- `FAILED TO FETCH`"
                    days = ""
                    title = "- `FAILED TO FETCH`"
                return (f'**Code:** {promo_code}\n'
                        f'**Expiry Date:** {days} days\n'
                        f'**Expires At:** {exp_at}\n'
                        f'**Title:** {title}')
                
        elif response.status == 429:
            return '**RARE LIMITED**'
        else:
            return f'**INVALID CODE** : `{promo_code}`'

def extract_promo_code(promo_link):
    promo_code = promo_link.split('/')[-1]
    return promo_code

deleted_messages = {}

@raj.event
async def on_message_delete(message):
    if message.guild:
        if message.channel.id not in deleted_messages:
            deleted_messages[message.channel.id] = deque(maxlen=5)  # Store up to 5 messages

        deleted_messages[message.channel.id].append({
            'content': message.content,
            'author': message.author.name,
            'timestamp': message.created_at
        })

@raj.command()
async def snipe(ctx):
    await ctx.message.delete()
    channel_id = ctx.channel.id
    if channel_id in deleted_messages and deleted_messages[channel_id]:
        messages = deleted_messages[channel_id]
        for msg in messages:
            timestamp = msg['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        await ctx.send(f'''### Snipped Deleted Message
{timestamp} | Message Content : `{msg["content"]}`

Message sent By `{msg['author']}`''')
    else:
        await ctx.send("<:Spider_arrow:1243092386758918156> No messages to snipe in this channel.")
        
@raj.command()
async def checktoken(ctx , tooken):
    await ctx.message.delete()
    headers = {
        'Authorization': tooken
    }
    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if r.status_code == 200:
        user_info = r.json()
        await ctx.send(f'''### Token Checked Succesfully
              - **Valid Token **
              - **Username : `{user_info["username"]}`**
              - **User Id : `{user_info["id"]}`**
              - **Email : `{user_info["email"]}`**
              - **Verifed? `{user_info["verified"]}`**
              ''')
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} TOKEN CHECKED✅ ")
    else:
        await ctx.send("<:Spider_arrow:1243092386758918156> Invalid Token or Locked or flagged")
        
translator = Translator()

@raj.command()
async def translate(ctx, *, text: str):
    await ctx.message.delete()
    try:
        detection = translator.detect(text)
        source_language = detection.lang
        source_language_name = LANGUAGES.get(source_language, 'Unknown language')

        translation = translator.translate(text, dest='en')
        translated_text = translation.text

        response_message = (
            f"**Original Text:** {text}\n"
            f"**Detected Language:** {source_language_name} ({source_language})\n"
            f"**Translated Text:** {translated_text}"
        )

        await ctx.send(response_message)
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}MSG TRANSLATED✅ ")

    except Exception as e:
        await ctx.send("<:Spider_arrow:1243092386758918156> **Error**: Could not translate text. Please try again later.")
        
@raj.command()
async def avatar(ctx, user: discord.User):
    await ctx.message.delete()
    try:
        await ctx.send(user.avatar_url)
    except:
        await ctx.send("<:Spider_arrow:1243092386758918156> User Don't Have Avatar")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} AVATAR✅ ")
        
@raj.command()
async def banner(ctx, user: discord.User):
    await ctx.message.delete()
    banner_url = user.banner_url
    if banner_url:
        await ctx.send(banner_url)
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}BANNER✅ ")
    else:
        await ctx.send("<:Spider_arrow:1243092386758918156> This user does not have a banner.")

@raj.command()
async def icon(ctx):
    await ctx.message.delete()
    server_icon_url = ctx.guild.icon_url if ctx.guild.icon else "<:Spider_arrow:1243092386758918156> No server icon"
    await ctx.send(server_icon_url)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} ICON ✅ ")

@raj.command()
async def get_image(ctx, query):
    await ctx.message.delete()
    params = {
        "query": query,
        'per_page': 1,
        'orientation': 'landscape'
    }
    headers = {
        'Authorization': f'Client-ID F1kSmh4MALfMKjHRxk38dZmPEV0OxsHdzuruBS_Y7to'
    }
    try:
        r = requests.get("https://api.unsplash.com/search/photos", headers=headers, params=params)
        r.raise_for_status()
        data = r.json()
        if data['results']:
            image_url = data['results'][0]['urls']['regular']
            await ctx.send(f"Here is your image for `{query}`:\n{image_url}")
            print("Successfully Generated Image")
        else:
            await ctx.send('No images found.')
    except requests.RequestException as e:
        print(f"Error fetching image: {e}")
        await ctx.send(f"`Error fetching image: {e}`")

@raj.command()
async def sc(ctx, category_id: int, *, message: str):
    await ctx.message.delete()
    if ctx.guild is None:
        await ctx.send("This command can only be used in a server.")
        return

    category = discord.utils.get(ctx.guild.categories, id=category_id)
    if category is None:
        await ctx.send("Category not found.")
        return

    if category_id in active_tasks:
        await ctx.send("A message task is already running for this category. Please stop it first using `.stopmsg`.")
        return

    category_messages[category_id] = message
    active_tasks[category_id] = True

    await ctx.send(f"**Sending Msg In Ticket Create Category Id: {category.name}.**")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} TICKET MSG CATEGORY SET ✅ ")

@raj.event
async def on_guild_channel_create(channel):
    if isinstance(channel, discord.TextChannel):
        category_id = channel.category_id
        if category_id in active_tasks and active_tasks[category_id]:
            await asyncio.sleep(1)  # Optional delay before sending the message
            await channel.send(category_messages[category_id])

@raj.command()
async def stopsc(ctx, category_id: int):
    await ctx.message.delete()
    if category_id not in active_tasks:
        await ctx.send("No message task is running for this category.")
        return

    active_tasks[category_id] = False
    await ctx.send(f"**Stopped Sending Msg In Ticket Create Category Id: {category_id}.**")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} TICKET MSG CATEGORY REMOVED ✅ ")
    
    

raj.run(token, bot=False)