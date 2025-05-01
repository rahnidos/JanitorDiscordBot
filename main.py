import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
import asyncio
from datetime import datetime, timedelta, timezone


load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
LANGUAGE = os.getenv('BOT_LANGUAGE', 'en') 


def load_language(language_code):
    with open(f'lang/{language_code}.json', 'r', encoding='utf-8') as file:
        return json.load(file)
    

messages = load_language(LANGUAGE)

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    async def setup_hook(self):
        self.loop.create_task(schedule_daily_task())

bot = MyBot(command_prefix='!', intents=intents)

async def delete_old_images():
    await bot.wait_until_ready()
    channels = json.loads(os.getenv("CHANNELS", "[]"))  
    three_days_ago = datetime.now(timezone.utc) - timedelta(days=3)

    for channel_id in channels:
        channel = bot.get_channel(int(channel_id))
        if channel:
            async for message in channel.history(limit=None):
                if message.attachments and message.created_at < three_days_ago:
                    try:
                        await message.delete()
                        await asyncio.sleep(1)  
                    except discord.errors.HTTPException as e:
                        print(f"Can't delete message {e}")

async def schedule_daily_task():
    while True:
        now = datetime.now()
        target_time = now.replace(hour=12, minute=0, second=0, microsecond=0)
        if now > target_time:
            target_time += timedelta(days=1)
        await asyncio.sleep((target_time - now).total_seconds())
        await delete_old_images()

@bot.event
async def on_ready():
    print(messages["ready_message"].format(bot_name=bot.user))

@bot.command()
async def hello(ctx):
    await ctx.send(messages["hello_message"])

@bot.command()
async def clean(ctx):
    await delete_old_images() 
    await ctx.send(messages["clean_over"])

bot.run(TOKEN)