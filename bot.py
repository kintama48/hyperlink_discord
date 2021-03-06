import asyncio
import json
import os
import platform
import sys

import discord
import psycopg2
from discord.ext import commands
from discord.ext.commands import Bot

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = discord.Intents.default()
bot = Bot(command_prefix=config["bot_prefix"], intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    # status_task.start()


@bot.event
async def on_command_completion(ctx):  # command executed successfully
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    print(
        f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})")


bot.remove_command("help")
if __name__ == "__main__":  # loading the features of the bot
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0x8233FF
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission `" + ", ".join(
                error.missing_perms) + "` to execute this command!",
            color=0xFF3387
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            color=0xFF5733
        )
        await context.send(embed=embed)
    raise error


@bot.event
async def on_message(message):  # executed when a message is sent by someone
    if message.author == bot.user or message.author.bot:
        return
    words = asyncio.gather(await get_words())
    for i in words:
        lst = i.split("<>")
        word = lst[0]
        link = lst[1]
        if i in message.content:
            embed = discord.Embed(color=0x18a324,
                                  description=f"{message.author} just mentioned the term '{word}'."
                                              f" To educate yourself and read about it. [Click here]({link}).")
            await message.channel.send(embed=embed)


async def get_words():
    db = psycopg2.connect(host="ec2-44-195-201-3.compute-1.amazonaws.com",
                          database="d3bjgaf44oicgk",
                          password="b1696d318ff8248df9aabf877f63ea752bc031be899b0408b935da4cb730d1c9",
                          port=5432, user="qygylrtrevsqcy")
    cur = db.cursor()
    cur.execute("SELECT * FROM public.term_link_db;")
    return cur.fetchall()[0]


bot.run(config["token"])

# https://discord.com/api/oauth2/authorize?client_id=882693617255350292&permissions=533113207808&scope=bot