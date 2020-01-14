from discord.errors import Forbidden
from discord import Game, ChannelType
import discord, requests, json, os
from discord.ext.commands import Bot

try:
    with open(os.getcwd() + "/app/data-store/bot-details.json", 'r') as f:
        data = f.read()
    bot_details = json.loads(data)
    if bot_details['token'] == "":
        raise ValueError("ValueError: You must have a token to run the bot/app.")
    if not isinstance(bot_details['token'], str):
        raise TypeError("TypeError: The token must be in a string format.")
except Exception as e:
    print(e)
    exit()

bot = Bot(bot_details['prefix'])
bot.remove_command("help")

@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.message.channel.send("Pong!")

@bot.command(pass_context=True, aliases=['m'])
async def mention(ctx):
    await ctx.message.channel.send(f"<@{ctx.message.author.id}>")

async def test(ctx, param):
    await ctx.channel.send(str(param))

@bot.event
async def on_message(ctx):
    with open(os.getcwd() + "/app/data-store/data.json", 'r') as f:
        data = f.read()
    data = json.loads(data)
    for i in data['cmds']:
        if ctx.author.id != "532185354036445195":
            if i['title'] == ctx.content or ctx.content in i['aliases']:
                with open(os.getcwd() + "/app/data-store/data-reference.json", 'r') as f:
                    data = f.read()
                data = json.loads(data)
                for j in data['elements']:
                    if j['id'] == i['id']:
                        await test(ctx, j['commands'])

@bot.event
async def on_ready():
    game = discord.Game("with the API")
    await bot.change_presence(activity=game)
    print('Bot_Ready: True')

def begin():
    bot.run(bot_details['token'])

begin()
