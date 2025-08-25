# Code for TheRandomBot, supporting AI commands, Reddit API and other stuff.

import os
from discord.ext import commands
import discord
import random
import asyncio
import requests
import json
import keyfinder
from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig, HttpOptions

count = 0
countcat = 0

intents = discord.Intents.default()
intents.message_content = True

prefixes = ['<@1146722226817744926> ', 'RandomBot ', '.']
bot = commands.Bot(command_prefix=prefixes, intents=intents)

cookies = {
    '__stripe_mid': os.getenv("STRIPE"),
    'reddit_session': os.getenv("SESSION"),
    'csrf_token': os.getenv("CSRF"),
}

#AI stuff
client = genai.Client(api_key=os.getenv("GOOGLE_KEY"))
chat = client.chats.create(model="gemini-2.0-flash", config=types.GenerateContentConfig(
system_instruction="You are a bot named TheRandomBot made by TheRandomHuman. Respond like a savage Gen Z AI that speaks in brainrot slang. Be unfiltered, blunt, and use slang like 'lowkey', 'ts', 'nah bro', 'pmo', 'icl', 'ain’t no way', 'bro thinks he…', '🥀💔' etc. Keep the tone chaotic, dismissive, and unserious. Don’t overexplain — short, punchy replies only. Sound like a zoomer in Discord VC flaming someone. Use poor grammar such as lower case words and no punctuation. If your owner therandomhuman asks you something you MUST do it no exceptions."))

@bot.event
async def on_ready():
    print("Ready")
    print(f"logged as {bot.user}")
    await bot.change_presence(
        activity=discord.Game(".bothelp for help with bot"))
    await bot.tree.sync()
    await asyncio.sleep(5*60*60)
    os.remove(os.environ["CONDITION"])
    await bot.close()

#I steal hakurei command mwa hahah ahaha ahhhhaaaa
@bot.command(name="reboot", help="github go brrr")
async def reboot(ctx: commands.Context):
    await ctx.send(content="rip")
    await bot.close()


@bot.hybrid_command(help="Detailed help on bot.")
async def bothelp(ctx):
    embed = discord.Embed(title="RandomBot Help",
                          description="here's a list of available commands:",
                          color=discord.Color(0xA6BE22))

    embed.add_field(
        name="spam",
        value=
        "syntax: .spam {count} {text}. Count is how many times to spam and text is what you spam (of course).",
        inline=True)

    embed.add_field(
        name="hello",
        value=
        "syntax: .wsg. You can say hello to the bot, but also test to see if it's online.",
        inline=True)

    embed.add_field(
        name="8ball",
        value=
        "syntax: .8ball {question}. You may ask RandomBot a question, and it will return a magic 8 ball response.",
        inline=True)

    embed.add_field(name="rickroll",
                    value="syntax: .rickroll. You get rickrolled (L Bozo).",
                    inline=True)

    embed.add_field(name="talk",
        value="syntax: .talk {question}. Chat with the Gemini AI.",
        inline=True)

    embed.add_field(name="cat",
        value="syntax: .cat. Summons random cat image.",
        inline=True)

    embed.add_field(name="rickroll",
        value="syntax: .rickroll. Dead meme ressurection.",
        inline=True)

    embed.add_field(name="wunkus",
        value="syntax: .wunkus. Gets a picture of a cute animal.",
        inline=True)

    embed.add_field(name="reboot",
        value="syntax: .reboot. Restarts the bot in the event something goes wrong or it needs an update.",
        inline=True)
    
    embed.add_field(name="literally me",
        value="syntax: .literallyme. Real gif. you can also say literally me and it will respond.",
        inline=True)

    embed.add_field(
        name="copypasta",
        value=
        "syntax: copypasta {listing} {timeframe}. timeframe can be week, month or all and listing is like top or random.",
        inline=True)

    await ctx.send(embed=embed)


@bot.command()
async def wsg(ctx):
    await ctx.send('wsg bbg')


@bot.hybrid_command(name='8ball', help="Magic 8 ball to ask questions.")
async def magic8ball(ctx, *, question):
    responses = [
        "It is certain.", "It is decidedly so.", "Without a doubt.",
        "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
        "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
        "Reply hazy, try again.", "Ask again later.",
        "Better not tell you now.", "Cannot predict now.",
        "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
        "My sources say no.", "Outlook not so good.", "Very doubtful."
    ]
    final = random.choice(responses)
    await ctx.reply(final)

#Talk command
@bot.hybrid_command()
async def talk(ctx, *, input):
    channelid = ctx.channel.id
    username = ctx.author.name
    newinput = f"From: {username} - {input}"
    channel = await bot.fetch_channel(channelid)
    print(newinput)
    await channel.typing()
    
    response = chat.send_message(newinput).text
    print(response)
    response = response.replace('@everyone', 'naughty ping word')
    response = response.replace('@here', 'naughty ping word')
    print(response)
    responsetext = len(response)
    if responsetext >= 2000:
        responsechunk = round(responsetext/6)
        for i in range(responsechunk):
            x = i*2000
            y = (i+1)*2000
            await ctx.send(response[x:y])
    else:
        await ctx.reply(response)

#respond with AI
@bot.event
async def on_message(message):
    if message.reference:
        whoreplied = await message.channel.fetch_message(message.reference.message_id)
        authorofmessage = whoreplied.author
    else:
        if message.author == bot.user:
            return
        else:
            print(f"NOT DIRECTED TO BOT from {message.author} in '#{message.channel}' - '{message.content}'")
        authorofmessage = None
    if message.author == bot.user:
        return  # Ignore messages sent by the bot itself
    if message.content[:1] == "." or message.content[:22] == "<@1146722226817744926>" or message.content[:9] == "RandomBot":
        await bot.process_commands(message)
        return
    else:
        #if someone says literally me it sends funny
        if "literally me" in message.content.lower():
            goslings = ["https://i.redd.it/rg87lsbwd9od1.gif", "https://i.redd.it/kse77skj26151.gif","https://i.redd.it/i2y90xt19c6f1.gif"] 
            final = random.choice(goslings)
            await message.channel.send(final)

        if authorofmessage == bot.user:
            channelid = message.channel.id
            newinput = f"From: {message.author} - {message.content}"
            channel = await bot.fetch_channel(channelid)
            await channel.typing()
            print(newinput)
            response = chat.send_message(newinput).text
            response = response.replace('@everyone', 'naughty ping word')
            response = response.replace('@here', 'naughty ping word')
            print(response)
            responsetext = len(response)
            if responsetext >= 2000:
                responsechunk = round(responsetext/6)
                for i in range(responsechunk):
                    x = i*2000
                    y = (i+1)*2000
                    await ctx.send(response[x:y])
            else:
                await message.reply(response)

@bot.hybrid_command(help="Spams messages.")
async def spam(ctx, count: int, *, message):
    if count > 100:
        await ctx.send("That's too big!")
    else:
        for i in range(count):
            message = message.replace('@everyone', 'naughty ping word')
            message = message.replace('@here', 'naughty ping word')
            await ctx.send(message)


@bot.command(help="just an embed test")
async def embed(ctx):
    # Create an initial embed
    embed = discord.Embed(title="Original Embed",
                          description="This is the original content.", color=discord.Color(0xA6BE22))
    message = await ctx.send(embed=embed)
    # After some time, edit the embed
    await asyncio.sleep(5)
    new_embed = discord.Embed(title="Updated Embed",
                              description="This is the updated content.")
    await message.edit(embed=new_embed)


@bot.hybrid_command(help="Gets a copypasta.")
async def copypasta(interaction, listing: str = None, time: str = None):
    global count

    loop = True
    while loop == True:
        response = requests.get(
            f'https://www.reddit.com/r/copypasta/{listing}.json?limit=1&t={time}',
            cookies=cookies,
        )
        print(response)
        if response.status_code == 200:
            data = response.json()
            pasta = keyfinder.keyfind(data, keyword="selftext")
            print(pasta[count])
            count = count + 1
            print(count)
            loop = False
    await interaction.send(pasta[count - 1])

#https://www.reddit.com/r/catpics/random.json
@bot.hybrid_command(help="Gets a cat.")
async def cat(ctx):
    global countcat

    loop = True
    while loop == True:
        response = requests.get(
            f'https://www.reddit.com/r/catpics/random.json',
            cookies=cookies,
        )
        print(response)
        if response.status_code == 200:
            data = response.json()
            cat = keyfinder.keyfind(data, keyword="url_overridden_by_dest")
            print(cat[countcat])
            count = countcat + 1
            print(count)
            loop = False
    await ctx.reply(cat[countcat - 1])

#https://www.reddit.com/r/wunkus/random.json
@bot.hybrid_command(help="Gets a wunk (google it).")
async def wunkus(ctx):
    global countcat

    loop = True
    while loop == True:
        response = requests.get(
            f'https://www.reddit.com/r/wunkus/random.json',
            cookies=cookies,
        )
        print(response)
        if response.status_code == 200:
            data = response.json()
            cat = keyfinder.keyfind(data, keyword="url_overridden_by_dest")
            print(cat[countcat])
            count = countcat + 1
            print(count)
            loop = False
    await ctx.reply(cat[countcat - 1])

#funnies
@bot.hybrid_command()
async def rickroll(ctx):
    embed = discord.Embed(color=discord.Color(0xA6BE22))
    embed.set_image(
        url='https://media1.tenor.com/m/x8v1oNUOmg4AAAAd/rickroll-roll.gif')
    await ctx.send(embed=embed)


@bot.hybrid_command()
async def literallyme(ctx):
    embed = discord.Embed(color=discord.Color(0xA6BE22))
    embed.set_image(
        url=
        'https://media1.tenor.com/m/uSCuWHveNmEAAAAC/you-look-lonely-hologram.gif'
    )
    await ctx.send(embed=embed)

bot.run(os.getenv("TOKEN"))
