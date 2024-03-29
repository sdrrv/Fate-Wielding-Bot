import discord
from discord.ext import commands
from discord.utils import find
import os
from controllers.controller import controller
from keep_alive import keep_alive
import json

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!fate ", intents=intents)
cont = controller(bot)

admins = cont.getAdmins()


@bot.event  # On Ready
async def on_ready():
    await bot.change_presence(activity=discord.Game("!fate help"))
    print(bot.user)
    print([i.name for i in bot.guilds])


@bot.event  # On Error
async def on_command_error(ctx, error):
    print("error")
    cont.debug(ctx)
    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.send("Command not found.Try `!fate help`")
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.channel.send(f"Sorry <@{ctx.message.author.id}>, you do not have permissions to do that!")
        return
    elif isinstance(error, commands.MemberNotFound):
        await ctx.channel.send(f"Member '`{error.argument}`' not found")
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("You're missing an argument there bud...\nTry `!fate help <command>`")
        return 
    await ctx.channel.send("**Something went wrong**... We are sorry. If you think this is a `bug` pls **report it**.")    
    raise error


@bot.event  # On new Server Enter
async def on_guild_join(guild):
    print(f"{guild.name}, Online")
    await cont.debugerLogGreen(f"**{guild.name}**, `Online`")
    with open("./models/leaderBoard.json", "r") as f:
        leaderBoard = json.load(f)

    leaderBoard[str(guild.id)] = {
        "games": {},
        "randomizers": {
            "ban": []
        }
    }

    with open("./models/leaderBoard.json", "w") as f:
        json.dump(leaderBoard, f, indent=4)

    general = find(lambda x: (x.name == 'general' or x.name ==
                              "geral"),  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(f"Hello there, `{guild.name}`!\nThank you for adding our bot, we hope you have as mutch fun using it, as we did coding it.\n"
                           + cont.help())


@bot.event
async def on_guild_remove(guild):
    print(f"{guild.name}, Offline")
    await cont.debugerLogRed(f"**{guild.name}**, `Offline`")
    with open("./models/leaderBoard.json", "r") as f:
        leaderBoard = json.load(f)

    leaderBoard.pop(str(guild.id))

    with open("./models/leaderBoard.json", "w") as f:
        json.dump(leaderBoard, f, indent=4)

#!--------------------------------------------------------------------------------------------------------------------------------------

@bot.command(name="about",
             brief="A little about the bot"
             )
async def about(ctx):
    cont.debug(ctx)
    await ctx.channel.send(cont.help())

#!-----------------------------------------------------------------------------------------------------------------------------------------

@bot.command(name="pull", hidden=True)
async def pull(ctx):
    if(ctx.author.id not in admins):
        return
    os.system("git pull https://github.com/sdrrv/Fate-Wielding-Bot.git")

#!-----------------------------------------------------------------------------------------------------------------------------------------

@bot.command(hidden=True)
async def load(ctx, name):
    if(ctx.author.id not in admins):
        return
    bot.load_extension(f"cogs.{name}")
    print(f"{name} Loaded!")


@bot.command(hidden=True)
async def unload(ctx, name):
    if(ctx.author.id not in admins):
        return
    bot.unload_extension(f"cogs.{name}")
    print(f"{name} UnLoaded!")


@bot.command(hidden=True)
async def reload(ctx, name):
    if(ctx.author.id not in admins):
        return
    bot.unload_extension(f"cogs.{name}")
    bot.load_extension(f"cogs.{name}")
    print(f"{name} ReLoaded!")

#!-----------------------------------------------------------------------------------------------------------------------------------------

for file in os.listdir("./cogs"):  # Will load all COGs
    if file.endswith(".py"):
        print("Load "+file)
        bot.load_extension(f"cogs.{ file[:-3] }")

keep_alive()
bot.run("ODAxNTgwNTg5OTAzOTA0Nzk5.YAiwGQ.A1EgBAnDHHuR4oJvkWrVDmVBU_0")  # Secret Stuff

#!-----------------------------------------------------------------------------------------------------------------------------------------
