# Code for TheRandomBot, supporting AI commands, Reddit API and other stuff.

import os
from discord.ext import commands
import discord
import random
import asyncio
import requests
import json
import keyfinder
import google.generativeai as genai

count = 0
countcat = 0

intents = discord.Intents.default()
intents.message_content = True

prefixes = ['@TheRandomBot ', 'RandomBot ', '.']
bot = commands.Bot(command_prefix=prefixes, intents=intents)

cookies = {
    '__stripe_mid': os.getenv("STRIPE"),
    'reddit_session': os.getenv("SESSION"),
    'csrf_token': os.getenv("CSRF"),
}

GOOGLE_API_KEY = os.getenv('GOOGLE_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

#specify the model
model = genai.GenerativeModel('gemini-1.5-pro', system_instruction = 'You are a friendly bot who can respond to anything in a quick, easy to understand manner and your response should be as short as possible. Your responses are formatted in the markdown system as if you were writing in a discord chat. Your creator is TheRandomHuman. Whenever you are asked a question that requires you to make a decision, you have to make a decision. You do not need to annouce who youre responding to you.', safety_settings={'HATE': 'BLOCK_NONE', 'HARASSMENT': 'BLOCK_NONE', 'SEXUAL' : 'BLOCK_NONE', 'DANGEROUS' : 'BLOCK_NONE'})
#start a chat
chat = model.start_chat()

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
        value="syntax: .talk. Chat with the Gemini AI.",
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
    await channel.typing()
    response = chat.send_message(newinput, safety_settings={'HATE': 'BLOCK_NONE', 'HARASSMENT': 'BLOCK_NONE', 'SEXUAL' : 'BLOCK_NONE', 'DANGEROUS' : 'BLOCK_NONE'}).text
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
        await ctx.send(response)

#respond with AI
@bot.event
async def on_message(message):
    if message.reference:
        whoreplied = await message.channel.fetch_message(message.reference.message_id)
        authorofmessage = whoreplied.author
    else:
        print("Message not directed to anyone.")
        authorofmessage = None
    if message.author == bot.user:
        return  # Ignore messages sent by the bot itself
    if message.content[:1] == ".":
        await bot.process_commands(message)
        return
    else:
        #if someone says literally me it sends funny
        if "literally me" in message.content.lower():
            goslings = ["https://media1.tenor.com/m/Qu9da9ZPlnsAAAAd/blade-runner2049-literally-me.gif", "https://media1.tenor.com/m/AWH8Uy6PMuoAAAAd/nubv.gif", "https://media1.tenor.com/m/iVL9VpBhrlQAAAAd/blade-runner2049-snow.gif"] 
            final = random.choice(goslings)
            await message.channel.send(final)
            
        if authorofmessage == bot.user:
            channelid = message.channel.id
            username = authorofmessage
            newinput = f"From: {username} - {message}"
            channel = await bot.fetch_channel(channelid)
            await channel.typing()
            response = chat.send_message(newinput, safety_settings={'HATE': 'BLOCK_NONE', 'HARASSMENT': 'BLOCK_NONE', 'SEXUAL' : 'BLOCK_NONE', 'DANGEROUS' : 'BLOCK_NONE'}).text
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
