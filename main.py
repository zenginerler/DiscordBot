import discord
import os
import random
import requests
import json
from replit import db
from discord.ext import commands
from keep_alive import keep_alive

client = commands.Bot(command_prefix = '>')


@client.event
async def on_ready(): # makes the bot work/online
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('with Fire'))
    print(client.user.name, 'is online!')


@client.command()
async def ping(ctx):
    """Prints the latency of a Bot"""
    await ctx.send(f'My current latency: {round(client.latency * 1000)}ms')


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=2):
    """Clears the message above"""
    await ctx.channel.purge(limit=amount)


@client.command(aliases=['askme', 'yesNo'])
async def eightBall(ctx, *, question):
    """Allows author to play a 8ball game"""
    responses = ["It is certain.",
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
                "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command(aliases=['f', 'F'])
async def payRespect(ctx):
    """Pays respect"""
    await ctx.send(f'{ctx.author.name} has paid their respect!')


@client.command(aliases=['flip', 'coin'])
async def flipACoin(ctx):
    """Flips a coin"""
    outcomes = ['Tails', 'Heads']
    await ctx.send(f'{ctx.author.name} flipped a coin! \nCoin: **{random.choice(outcomes)}**')


@client.command(aliases=['kitty'])
async def cat(ctx):
    """Sends a random cat image"""
    image = get_cat()
    await ctx.send(image)


@client.command(aliases=['inspireMe'])
async def quote(ctx):
    """Prints a random quote"""
    quote = get_quote()
    await ctx.send(quote)


@client.command(aliases=['define', 'urban'])
async def urbanDictionary(ctx, *, word):
    """Searches a definition for a given word"""
    if word == "Yavuz" or word == "yavuz":
        definition = "Greatest abi ever!" 
    else:
        definition = get_definition(word)
    await ctx.send(f'The most popular definition for **{word}** in Urban Dictionary: \n\n{definition}')


@client.command(aliases=['helpMe'])
async def helpMessage(ctx):
    """Shows the command prefix and possible commands"""
    await ctx.send('Command Prefix: **>** \nPossible Commands: **askme, quote/inspireMe, flip, define/urban, cat, F, ping, helpMe**')


def get_cat():
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    json_data = json.loads(response.text)
    return json_data[0]['url']


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote 


def get_definition(word):
    response = requests.get(f'https://api.urbandictionary.com/v0/define?term={word}')
    json_data = json.loads(response.text)
    try:
        result = json_data['list'][0]['definition']
    except Exception:
        result = 'Try again please!'
    return result


# this is a datbase function that is being tested!
def update_something(new_data):
    if "test_key" in db.keys():
        retrieved_data = db["test_key"]
        retrieved_data.append(new_data)
        db["test_key"] = retrieved_data
    else:
        db["test_key"] = [new_data]



keep_alive()
client.run(os.getenv('TOKEN'))