import math
import discord
import dislash
from discord.ext import commands, tasks
from dislash import InteractionClient, Option, OptionType
import random
import time
import math

prefix = ">"
bot = commands.Bot(command_prefix=prefix)
inter_client = InteractionClient(bot)

# Wklej tutaj token bota
token = "token"

# Wklej tutaj ID serwera, na którym bedzie pies
idguild = 0

# Tutaj ID kanału kuwety - możesz go ustawić (z małą szansą powodzenia) /kuweta, ale możesz też tak
chanid = 0

'''
Wersja jak chcesz w config.json
Plik przygotowany w folderze.

import json
with open("config.json", "r") as conf:
    jcon = json.loads(conf.read())
    token = jcon['token']
    idguild = jcon['guiid']
    chanid = jcon['kuwetaid']
'''

lastused = 0
karmaperc = 100
emotional = 100
zmeczenie = 0

whencleaned = 0

sleeps = False

def IsSleeping():
    global sleeps
    global zmeczenie
    if(sleeps == True):
        return True
    elif(zmeczenie > 90):
        sleeps = False
        return False
    else:
        return False

def ChangeSleep():
    global sleeps
    global zmeczenie
    if(sleeps == False and zmeczenie > 70):
        sleeps = True
    else:
        sleeps = False

async def ChangeKarmaPercent(minus, plus):
    global karmaperc
    global emotional
    global zmeczenie
    if(karmaperc - minus > 0):
        karmaperc = karmaperc - minus
    karmaperc = karmaperc + plus

async def ChangeEmotionalPercent(minus, plus):
    global karmaperc
    global emotional
    global zmeczenie
    if(emotional - minus < 0):
        emotional = 0
    else:
        emotional = emotional - minus
    if(emotional + plus > 100):
        emotional = 100
    else:
        emotional = emotional + plus

async def ChangeZmeczeniePercent(minus, plus):
    global karmaperc
    global emotional
    global zmeczenie
    if(zmeczenie - minus < 0):
        zmeczenie = 0
    else:
        zmeczenie = zmeczenie - minus
    if(zmeczenie + plus > 100):
        zmeczenie = 100
    else:
        zmeczenie = zmeczenie + plus
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"Saturacja: {karmaperc}%, Emocja: {emotional}%, Zmęczenie: {zmeczenie}%"))

def LetEmotional():
    global emotional
    rand = random.randint(1, 30)
    if(emotional + 1 > rand):
        return True
    else:
        return False

def LetEat():
    global karmaperc
    if(karmaperc < 100):
        return True
    else:
        if(random.randint(1, 4) == 2):
            return True
        else:
            return False


@bot.event
async def on_ready():
    await ChangeKarmaPercent(0, 0)
    timer.start()

#@bot.event
#async def on_message(message):
    #if(":elon_musk:" in message.content):
    #    await message.channel.send("😡 HAU HAU HAU! HAU HAU!")
    #    await message.delete()

@inter_client.slash_command(
    description="daj głos",
)
async def glos(inter : dislash.Interaction):
    if(IsSleeping()):
        await inter.reply(":sleeping:")
    else:
        if(LetEmotional()):
            temp = ""
            for y in range(random.randint(2, 9)):
                temp = temp + "hau"
                te = random.randint(1, 8)
                if(te == 2):
                    temp = temp + ", "
                elif(te == 3):
                    temp = temp + ". "
                elif (te == 4):
                    temp = temp + "! "
                else:
                    temp = temp + " "
            await inter.reply(temp)
            await ChangeKarmaPercent(1, 0)
        else:
            await inter.reply(":cry:")

@inter_client.slash_command(
    description="pogłaszcz psa",
)
async def glask(inter : dislash.Interaction):
    rand = random.randint(1, 20)
    if(rand < 15):
        await inter.reply("🤩")
        await ChangeEmotionalPercent(0, 4)
    elif(rand < 10):
        await inter.reply("😋")
        await ChangeEmotionalPercent(0, 3)
    elif(rand < 5):
        await inter.reply("😍")
        await ChangeEmotionalPercent(0, 2)
    else:
        await inter.reply("🥰")
        await ChangeEmotionalPercent(0, 1)

@inter_client.slash_command(
    description="zdobądź statystyki bota",
)
async def staty(inter : dislash.Interaction):
    global karmaperc
    global emotional
    global zmeczenie
    await inter.reply(f"Saturacja: *{karmaperc}%*\nEmocje: *{emotional}%*\nZmeczenie: *{zmeczenie}%*")

@inter_client.slash_command(
    description="wyzwij pimpka!",
    options=[
        Option("wyzwisko", "Wyzwij go", OptionType.STRING)
    ]
)
async def wyzwij(inter : dislash.Interaction):
    if (IsSleeping()):
        await inter.reply(":sleeping:")
    else:
        rand = random.randint(1, 20)
        if (rand > 10):
            await inter.reply(f"😭")
            await ChangeEmotionalPercent(2, 0)
        else:
            await inter.reply("😢")
            await ChangeEmotionalPercent(1, 0)

@inter_client.slash_command(
    description="aport!",
)
async def aport(inter : dislash.Interaction):
    if (IsSleeping()):
        await inter.reply(":sleeping:")
    else:
        global emotional
        if(LetEmotional()):
            await inter.reply("https://tenor.com/view/good-girl-dog-with-stick-cool-run-gif-12436602")
            await ChangeEmotionalPercent(0, 3)
            await ChangeKarmaPercent(8, 0)
            await ChangeZmeczeniePercent(0, 5)
        else:
            await inter.reply("Pies nie ma ochoty aportować :(")

@inter_client.slash_command(
    description="nakarm psa",
)
async def nakarm(inter : dislash.Interaction):
    if (IsSleeping()):
        await inter.reply(":sleeping:")
    else:
        global karmaperc
        rand = random.randint(1, 20)
        if(LetEmotional()):
            if(LetEat()):
                if(rand > 15):
                    await inter.reply("🤩")
                    await ChangeKarmaPercent(0, 4)
                    await ChangeEmotionalPercent(0, 4)
                elif(rand > 10):
                    await inter.reply("😋")
                    await ChangeKarmaPercent(0, 3)
                    await ChangeEmotionalPercent(0, 3)
                elif(rand > 5):
                    await inter.reply("😍")
                    await ChangeKarmaPercent(0, 2)
                    await ChangeEmotionalPercent(0, 2)
                else:
                    await inter.reply("🥰")
                    await ChangeKarmaPercent(0, 1)
                    await ChangeEmotionalPercent(0, 1)
            else:
                await inter.reply("Przepełniony.")
                await ChangeEmotionalPercent(2, 0)
        else:
            await inter.reply(":cry:")

@inter_client.slash_command(
    description="naucz psa że tu jest kuweta",
)
async def kuweta(inter : dislash.Interaction):
    if (IsSleeping()):
        await inter.reply(":sleeping:")
    else:
        global chanid
        rand = random.randint(2100, 7890)
        if(rand == 2137):
            await inter.reply("*potrząsa głową*")
            chanid = inter.channel.id
        else:
            await inter.reply("?")

@inter_client.slash_command(
    description="zrób solidne kupsko.",
)
async def sraj(inter : dislash.Interaction):
    if (IsSleeping()):
        await inter.reply(":sleeping:")
    else:
        global karmaperc
        if(karmaperc >= 103):
            await inter.reply(":poop:")
            await ChangeKarmaPercent(3, 0)
        else:
            await inter.reply("*potrząsa głową (nie)*")

@inter_client.slash_command(
    description="uśpij psa (nie pistoletem comand.)"
)
async def uspij(inter : dislash.Interaction):
    global zmeczenie
    if(zmeczenie < 40):
        await inter.reply("*Psowi sie nie chce spac*")
    else:
        ChangeSleep()
        await inter.reply("*Dobranoc!*")

@inter_client.slash_command(
    description="umyj psa",
)
async def umyj(inter : dislash.Interaction):
    if (IsSleeping()):
        await inter.reply(":sleeping:")
    else:
        global whencleaned
        if(LetEmotional()):
            if(whencleaned - math.floor(time.time()) <= 2137):
                whencleaned = math.floor(time.time())
                await inter.reply("🥰")
                await ChangeEmotionalPercent(0, 2)
            else:
                await inter.reply("😠")
                await ChangeEmotionalPercent(1, 0)
        else:
            await inter.reply(":cry:")

i = 0

@tasks.loop(seconds=60)
async def timer():
    global i
    if (IsSleeping()):
        if(i == 5):
            await ChangeKarmaPercent(1, 0)
            await ChangeEmotionalPercent(0, 0)
            await ChangeZmeczeniePercent(5, 0)
            i = 0
        else:
            i = i + 1
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"Dobranoc!"))
    else:
        global karmaperc
        if(karmaperc > 100):
            if(chanid == 0):
                await random.choice(bot.get_guild(idguild).text_channels).send(":poop:")
                await ChangeKarmaPercent(3, 0)
            else:
                c = await bot.fetch_channel(chanid)
                await c.send(":poop:")
                await ChangeKarmaPercent(3, 0)
            await ChangeKarmaPercent(1, 0)
            await ChangeEmotionalPercent(1, 0)
            await ChangeZmeczeniePercent(0, 1)
        await ChangeKarmaPercent(1, 0)
        await ChangeEmotionalPercent(1, 0)
        await ChangeZmeczeniePercent(0, 1)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"/staty !"))
        ChangeSleep()

def RunSeq():
    if (token == "token"):
        #print("Czy nie zapomniales o tokenie?")
        SystemExit("Czy nie zapomniales o tokenie?")
    elif (idguild == 0):
        #print("Czy nie zapomniales o gildii?")
        SystemExit("Czy nie zapomniales o gildii?")
    else:
        bot.run(token)
        print("Pies żyje.")
RunSeq()