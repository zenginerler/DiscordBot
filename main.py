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
    await ctx.send(f'My current latency: {round(client.latency * 1000)}ms')


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)


@client.command(aliases=['askme'])
async def yesNo(ctx, *, question):
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


@client.command(aliases=['inspireMe'])
async def quote(ctx):
    quote = get_quote()
    await ctx.send(quote)


@client.command()
async def test1(ctx):
    await ctx.send('This function is under development')


@client.command()
async def test2(ctx):
    await ctx.send('This function is under development')


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote 


# this is a function that is being tested!
def update_something(new_data):
    if "test_key" in db.keys():
        retrieved_data = db["test_key"]
        retrieved_data.append(new_data)
        db["test_key"] = retrieved_data
    else:
        db["test_key"] = [new_data]



keep_alive()
client.run(os.getenv('TOKEN'))