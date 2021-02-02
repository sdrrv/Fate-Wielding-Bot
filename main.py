import discord
from discord.ext import commands
from discord.utils import find
import os
from controllers.controller import controller
from keep_alive import keep_alive

intents = discord.Intents.all()
cont = controller()
bot = commands.Bot(command_prefix="!fate ",intents = intents)

@bot.event #On Ready
async def on_ready():
    await bot.change_presence(activity=discord.Game("!fate help"))
    print(bot.user)
    print([i.name for i in bot.guilds])

@bot.event #On Error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.send("Command not found.Try `!fate help`")
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.channel.send(f"Sorry <@{ctx.message.author.id}>, you do not have permissions to do that!")
        return
    #elif isinstance(error, commands.TimeoutError):
      #  await ctx.channel.send("You took to long to respond.** Time Out **")
      #  return

    raise error

@bot.event #On new Server Enter
async def on_guild_join(guild):
    print(f"{guild.name}, you have a new bot now")
    general = find(lambda x: (x.name == 'general' or x.name =="geral"),  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(f"Hello there, {guild.name}!\nThank you for adding our bot, we hope you have as mutch fun using it, as we did coding it.\n"\
          + cont.help())
#!--------------------------------------------------------------------------------------------------------------------------------------

@bot.command(name="about",
brief="A little about the bot"
)
async def about(ctx):
    cont.debug(ctx)
    await ctx.channel.send(cont.help())

#!-----------------------------------------------------------------------------------------------------------------------------------------

@bot.command(hidden=True)
async def load(ctx, name):
  if(ctx.author.id!=201335861755772928):
        return
  bot.load_extension(f"cogs.{name}")
  print(f"{name} Loaded!")

@bot.command(hidden=True)
async def unload(ctx, name):
  if(ctx.author.id!=201335861755772928):
        return
  bot.unload_extension(f"cogs.{name}")
  print(f"{name} UnLoaded!")

@bot.command(hidden=True)
async def reload(ctx,name):
  if(ctx.author.id!=201335861755772928):
        return 
  bot.unload_extension(f"cogs.{name}")
  bot.load_extension(f"cogs.{name}")
  print(f"{name} ReLoaded!")


for file in os.listdir("./cogs"): #Will load all COGs
      if file.endswith(".py"):
            print("Load "+file)
            bot.load_extension(f"cogs.{ file[:-3] }")

#!-----------------------------------------------------------------------------------------------------------------------------------------
keep_alive()
bot.run(os.getenv("TOKEN"))  #Secret Stuff

