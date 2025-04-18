import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json


load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
LANGUAGE = os.getenv('BOT_LANGUAGE', 'en') 


def load_language(language_code):
    with open(f'lang/{language_code}.json', 'r', encoding='utf-8') as file:
        return json.load(file)
    

messages = load_language(LANGUAGE)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(messages["ready_message"].format(bot_name=bot.user))

@bot.command()
async def hello(ctx):
    await ctx.send(messages["hello_message"])

bot.run(TOKEN)