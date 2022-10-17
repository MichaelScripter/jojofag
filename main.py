import discord
from discord.ext import commands
import sqlite3
import random
from config import *
from database import database_object
from database import exec
import PIL
from PIL import Image
from functs import *
import time
import json

commandse = {
    "Аррест": {
        "Description":"Отправка юзера в тюрьму",
        "Args": "<юзер>",
    },
    "Ударить": {
        "Description":"Избиение юзера",
        "Args": "<юзер>",
    },
    "ЯТебяПоАйпиВычислю": {
        "Description":"Генерация фейкового айпи",
        "Args":"<юзер>"
    },
    "Стрела": {
        "Description":"Получить рандомний стенд",
        "Args":""
    },
    "Рока": {
        "Description":"Удалить стенд",
        "Args":"<имястенда>"
    },
    "Шансы": {
        "Description":"Шансы на стендов",
        "Args":""
    },
    "Стенди": {
        "Description":"Ваши стенди",
        "Args":""
    },
    "Героин": {
        "Description":"Героин реал",
        "Args":""
    },
    "Повестка": {
        "Description":"Мобилизация.",
        "Args":"<юзер>"
    },
    "Яйцо": {
        "Description":"Как",
        "Args":"<юзер>"
    },
    "Негр": {
        "Description":"бля поч я стал негром",
        "Args":"<юзер>"
    },
    "Расстрел": {
        "Description":"Расстрелать юзера",
        "Args":"<юзер>"
    },
    "Виебать": {
        "Description":"Чел ты...",
        "Args":"<юзер>"
    },
    "Респект": {
        "Description":"😎",
        "Args":"<юзер>"
    },
    "ИзбивФурри": {
        "Description":"Чел ты крутой",
        "Args":""
    }
}

arrow_countdown = {}

def add_arrow_countdown(user):
    arrow_countdown[user.id] = time.time()

def check_arrow_countdown(user):
    if user.id in arrow_countdown:
        if time.time() - arrow_countdown[user.id] > 5*60:
            arrow_countdown.pop(user.id)
            return True
    else:
        return True
    return False

roka_countdown = {}

def add_roka_countdown(user):
    roka_countdown[user.id] = time.time()

def check_roka_countdown(user):
    if user.id in roka_countdown:
        if time.time() - roka_countdown[user.id] > 5*60:
            roka_countdown.pop(user.id)
            return True
    else:
        return True
    return False

add_chance(["Death Thirteen", "Judgement", "Hanged Man", "Emperor"], 40)
add_chance(["Hierophant Green", "Tower of Gray", "Cream", "Anubis"], 30)
add_chance(["Magician's Red", "Hermit Purple", "Silver Chariot", "Bastet"], 25)
add_chance(["The World", "Star Platinum"], 5)

sys_random = random.SystemRandom()

data = database_object("accounts")

def create_acc(user):
    id = str(user.id)
    data = exec("SELECT * FROM accounts WHERE id = ?", [id])
    if data.fetchone() is None:
        values = (
            (str(id), json.dumps([]), json.dumps([]), 0)
        )
        exec("INSERT INTO accounts(id, countdowns, stands, money) VALUES(?, ?, ?, ?)", values)

def gif_embed(title, link):
    embed = discord.Embed(description=title, color=discord.Color.from_rgb(186, 252, 3).value)
    embed.set_image(url=link)
    return embed

def embed(title, desc):
    embed = discord.Embed(title=title, description=desc, color=discord.Color.from_rgb(186, 252, 3).value)
    return embed

client = commands.Bot(command_prefix=".", help_command=None)

@client.command(name="Аррест", aliases=["аррест"])
async def command(ctx, first: discord.User=None):
    if first is None:
        await ctx.send(embed=embed("Помощь", "Аррест"+" "+commandse["Аррест"]["Args"]))
    else:
        await ctx.send(embed=gif_embed(f"{first.mention} вы были арестованы", sys_random.choice(arrest_images)))

@client.command(name="Ударить", aliases=["ударить"])
async def command(ctx, first: discord.User=None):
    if first is None:
        await ctx.send(embed=embed("Помощь", "Ударить"+" "+commandse["Ударить"]["Args"]))
    else:
        rand = sys_random.choice(beat_images)
        data = beat_data[rand]
        file = Image.open(f"assets/{rand}")
        add_avatar(file, first, data[0], data[1])
        add_avatar(file, ctx.author, data[2], data[3])
        file.save("real.png")
        await ctx.send(file=discord.File("real.png"), embed=gif_embed(f"{first.mention} ты был избит {ctx.author.mention}", "attachment://real.png"))

@client.command(name="Респект", aliases=["респект"])
async def command(ctx, first: discord.User=None):
    if first is None:
        await ctx.send(embed=embed("Помощь", "Респект"+" "+commandse["Респект"]["Args"]))
    else:
        await ctx.send(embed=gif_embed(f"{first.mention} респект<:chupep_ochki:1029327559646773258>", "https://media.tenor.com/Z2FddVYN14IAAAAS/repete-jojo.gif"))

@client.command(name="Стрела", aliases=["стрела"])
async def command(ctx):
    if check_arrow_countdown(ctx.author):
        add_arrow_countdown(ctx.author)
        dataj = json.loads(data.get(ctx.author, "stands").fetchone()[0])
        if len(dataj) < 10:
            stand = generate_stand()
            dataj.append(stand)
            data.set(ctx.author, "stands", json.dumps(dataj))
            await ctx.send(embed=embed("Стенд", f"Ты получил **{stand}**"))
        else:
            await ctx.send(embed=embed("Стенд", f"Вы можете иметь только 10 стендов"))
    else:
        await ctx.send("Вы можете использовать эту команду раз в 5 минут")

@client.command(name="Рока", aliases=["рока"])
async def command(ctx, *, first=None):
    if first is None:
        await ctx.send(embed=embed("Помощь", "Рока"+" "+commandse["Рока"]["Args"]))
    else:
        if check_roka_countdown(ctx.author):
            dataj = json.loads(data.get(ctx.author, "stands").fetchone()[0])
            if first in dataj:
                dataj.remove(first)
                data.set(ctx.author, "stands", json.dumps(dataj))
                add_roka_countdown(ctx.author)
                await ctx.send(embed=embed("Стенд", f"У тебя больше нету **{first}**"))
            else:
                await ctx.send(embed=embed("Стенд", f"Стенда не существует или нету в инвентаре"))
        else:
            await ctx.send("Вы можете использовать эту команду раз в 5 минут")

@client.command(name="Стенди", aliases=["стенди"])
async def command(ctx):
    dataj = json.loads(data.get(ctx.author, "stands").fetchone()[0])
    stre = ""
    counter = 0
    for r in dataj:
        counter+=1
        stre = stre + f"{counter}. **{r}** \n\n"
    await ctx.send(embed=embed("Стенди", stre))

@client.command(name="Шансы", aliases=["шансы"])
async def command(ctx):
    stre = ""
    for chance in chances:
        stre = stre + "**" + str(chance[1] - chance[0]) + "%" + "**" + ": " + ", ".join(chances[chance]) + "\n\n"
    await ctx.send(embed = embed("Шансы", stre))

@client.command(name="ЯТебяПоАйпиВычислю")
async def command(ctx, first: discord.User=None):
    if first is None:
        await ctx.send(embed=embed("Помощь", "ЯТебяПоАйпиВычислю"+" "+commandse["ЯТебяПоАйпиВычислю"]["Args"]))
    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    await ctx.send(embed=embed("Айпи", f"{first.mention} твой айпи {ip}"))

@client.command(name="Героин", aliases=["героин"])
async def command(ctx):
    await ctx.send(embed=gif_embed(f"{ctx.author.mention} попробовал героин", "https://media.tenor.com/15qFC090J3AAAAAS/jotaro-falls.gif"))

@client.command(name="Хелп", aliases=["команди", "хелп", "Команди"])
async def command(ctx, first: discord.User=None):
    stre = ""
    for command, info in commandse.items():
        stre = stre + "**."+ command + "** " + info["Args"] + "\n" + " ? " + info["Description"] + "\n" + "\n"
    stre = stre + "\n! Создатель бота <@770297312793854033> !"
    await ctx.send(embed=embed("Хелп", stre))

@client.command(name="Повестка", aliases=["повестка"])
async def command(ctx, first: discord.User=None):
    if first is None:
        await ctx.send(embed=embed("Помощь", "Повестка"+" "+commandse["Повестка"]["Args"]))
    else:
        await ctx.send(embed=gif_embed(f"{first.mention} был мобилизован {ctx.author.mention}", "https://media.tenor.com/peykjsShSugAAAAS/kakyoin-shades.gif"))

@client.command(name="Расстрел", aliases=["расстрел"])
async def command(ctx, first: discord.User=None):
    if first is None:
        await ctx.send(embed=embed("Помощь", "Расстрел"+" "+commandse["Расстрел"]["Args"]))
    else:
        await ctx.send(embed=gif_embed(f"{first.mention} был застрелен", "https://media.tenor.com/ZYhuTmctmeIAAAAS/hol-horse.gif"))

@client.command(name="Виебать", aliases=["виебать"])
async def command(ctx, first: discord.User=None):
    if first is None:
        await ctx.send(embed=embed("Помощь", "Виебать"+" "+commandse["Виебать"]["Args"]))
    else:
        await ctx.send("<:che:1000868299623628911>")

@client.command(name="ИзбивФурри", aliases=["избивФурри"])
async def command(ctx):
    file = Image.open("assets/jotarobeatsfurry.png")
    add_avatar(file, ctx.author, (335, 92), (113, 113))
    file.save("ez.png")
    await ctx.send(file=discord.File("ez.png"), embed=gif_embed(f"{ctx.author.mention} крут", "attachment://ez.png"))

@client.command(name="Яйцо", aliases=["яйцо"])
async def command(ctx, first: discord.User=None):
    if first is None:
        await ctx.send(embed=embed("Помощь", "Яйцо"+" "+commandse["Яйцо"]["Args"]))
    else:
        image = Image.open("assets/egg.png")
        mask = Image.open("assets/eggmask.png")
        img = Image.open(requests.get(first.avatar_url, stream=True).raw)
        img = img.resize((220, 220))
        image.paste(img, (0, 0), mask)
        image.save("egg.png")
        await ctx.send(file=discord.File("egg.png"), embed=gif_embed(f"{ctx.author.mention} непон", "attachment://egg.png"))

@client.command(name="Негр", aliases=["негр"])
async def command(ctx, first: discord.User=None):
    if first is None:
        await ctx.send(embed=embed("Помощь", "Негр"+" "+commandse["Негр"]["Args"]))
    else:
        img = Image.open(requests.get(first.avatar_url, stream=True).raw)
        img = img.convert("RGB")
        img = img.resize((220, 220))
        layer = Image.new('RGB', img.size, (255, 255, 255))
        img = Image.blend(img, layer, 0.35)
        layer = Image.new('RGB', img.size, (124, 79, 49))
        output = Image.blend(img, layer, 0.7)
        output.save("black.png")
        await ctx.send(file=discord.File("black.png"), embed=gif_embed(f"{ctx.author.mention} чо за..", "attachment://black.png"))

@client.command(name="Ночной-Чат")
async def command(ctx):
    if ctx.author.id == 770297312793854033 or ctx.message.author.guild_permissions.administrator:
        await ctx.channel.edit(name="ночной-чат")

@client.command(name="Утренний-Чат")
async def command(ctx):
    if ctx.author.id == 770297312793854033 or ctx.message.author.guild_permissions.administrator:
        await ctx.channel.edit(name="утренний-чат")

@client.command(name="Вечерний-Чат")
async def command(ctx):
    if ctx.author.id == 770297312793854033 or ctx.message.author.guild_permissions.administrator:
        await ctx.channel.edit(name="вечерний-чат")

@client.command(name="Дневной-Чат")
async def command(ctx):
    if ctx.author.id == 770297312793854033 or ctx.message.author.guild_permissions.administrator:
        await ctx.channel.edit(name="дневной-чат")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="ЮБА"))

@client.event
async def on_message(message):
    create_acc(message.author)
    await client.process_commands(message)

client.run(token)
