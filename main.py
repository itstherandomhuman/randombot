# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import os
from discord.ext import commands
import discord
import random
import asyncio
import requests
import json
import keyfinder

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print("Ready")
    print(f"logged as {bot.user}")
    await bot.change_presence(activity=discord.Game(".bothelp for help with bot"))
    await bot.tree.sync()
    await asyncio.sleep(5*60*60)
    os.remove(os.environ["CONDITION"])
    await bot.close()

@bot.command(help = "Detailed help on bot.")
async def bothelp(ctx):
    embed = discord.Embed(
        title="RandomBot Help",
        description="here's a list of available commands:",
        color=discord.Color(0xA6BE22)
    )

    embed.add_field(name="spam", value="syntax: .spam {count} {text}. Count is how many times to spam and text is what you spam (of course).", inline=True)

    embed.add_field(name="hello", value="syntax: .wsg. You can say hello to the bot, but also test to see if it's online.", inline=True)

    embed.add_field(name="8ball", value="syntax: .8ball {question}. You may ask RandomBot a question, and it will return a magic 8 ball response.", inline=True)

    embed.add_field(name="rickroll", value="syntax: .rickroll. You get rickrolled (L Bozo).", inline=True)

    embed.add_field(name="/copypasta", value="syntax: /copypasta {listing} {timeframe}. timeframe can be week, month or all and listing is like top or random.", inline=True)

    await ctx.send(embed=embed)

@bot.command()
async def wsg(ctx):
    await ctx.send('wsg bbg')

@bot.command(name='8ball', help = "Magic 8 ball to ask questions.")
async def magic8ball(ctx, *, question):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    final = random.choice(responses)
    await ctx.reply(final)

@bot.command(help = "Spams messages.")
async def spam(ctx, count: int, *, message):
    if count > 100:
      await ctx.send("That's too big!")
    else:
      for i in range(count):
          await ctx.send(message)

@bot.command(help = "just an embed test")
async def embed(ctx):
    # Create an initial embed
    embed = discord.Embed(title="Original Embed", description="This is the original content.")
    message = await ctx.send(embed=embed)
    # After some time, edit the embed
    await asyncio.sleep(5)
    new_embed = discord.Embed(title="Updated Embed", description="This is the updated content.")
    await message.edit(embed=new_embed)

@bot.command(help = "Gets a copypasta.")
async def copypasta(interaction ,listing: str = None,  time: str = None):
    cookies = {
        '__stripe_mid': os.getenv("STRIPE"),
        'reddit_session': os.getenv("SESSION"),
        'csrf_token': os.getenv("CSRF"),
    }
    response = requests.get(
        f'https://www.reddit.com/r/copypasta/{listing}.json?limit=1&t={time}',
        cookies=cookies,
    )
    data = response.json()
    pasta = keyfinder.keyfind(data, "selftext")
    print(pasta)
    await interaction.send(pasta[0])
#funnies
@bot.command()
async def rickroll(ctx):
    embed = discord.Embed()
    embed.set_image(url='https://media1.tenor.com/m/x8v1oNUOmg4AAAAd/rickroll-roll.gif') 
    await ctx.send(embed=embed)
    
@bot.command()
async def literallyme(ctx):
    embed = discord.Embed()
    embed.set_image(url='https://media1.tenor.com/m/uSCuWHveNmEAAAAC/you-look-lonely-hologram.gif') 
    await ctx.send(embed=embed)

bot.run(os.getenv("TOKEN"))
