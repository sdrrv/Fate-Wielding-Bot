import discord
from discord import client
from discord.ext import commands
from discord.utils import find
import os
from controllers.controller import controller
from keep_alive import keep_alive
import time

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
        await ctx.channel.send("Command not found.")
        return 1
    raise error

@bot.event #On new Server Enter
async def on_guild_join(guild):
    print(f"{guild.name}, you have a new bot now")
    general = find(lambda x: (x.name == 'general' or x.name =="geral"),  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(f"Hello there, {guild.name}!\nThank you for adding our bot, we hope you have as mutch fun using it, as we did coding it.\n"\
          + cont.help())

#--------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name = "roulette",
help="!fate roulette - it will enter the voice channel of the user and kick one person Russian Roulette style\nYou must be in a voice channel to use.",
brief="will kick one user inside your voice channel, Russian Roulette style"
)
async def roulette(ctx):
  cont.debug(ctx)
  if not ctx.author.voice:
      await ctx.channel.send("You must be in a voice channel to do that.")
      return 1
  channel= ctx.author.voice.channel
  #-------------------------------------
  members= [i for i in channel.members]
  to_kick= cont.choose(members)
  #-------------------------------------
  voice_client= await cont.join(channel)

  for member in members:
      if member == to_kick:
        cont.play(voice_client,"shoot.wav")
        while voice_client.is_playing():
          time.sleep(.1)
        await cont.disconnect_member(member)
        break

      cont.play(voice_client,"revolver_blank.wav")
      while voice_client.is_playing():
        time.sleep(.1)

  await ctx.channel.send(cont.get_disconnect_phrase()+f"<@{to_kick.id}>")
  time.sleep(3)
  await cont.leave(voice_client) #self disconnect
#--------------------------------------------------------------------------------------------------------------------------------------

@bot.command(name="about",
brief="A little about the bot"
)
async def about(ctx):
    cont.debug(ctx)
    await ctx.channel.send(cont.help())
#-----------------------------------------------------------------------------------------------------------------------------------------


@bot.command(hidden=True)
async def load(ctx, name):
  bot.load_extension(f"cogs.{name}")
  print(f"{name} Loaded!")

@bot.command(hidden=True)
async def unload(ctx, name):
  bot.unload_extension(f"cogs.{name}")
  print(f"{name} UnLoaded!")

@bot.command(hidden=True)
async def reload(ctx,name):
  bot.unload_extension(f"cogs.{name}")
  bot.load_extension(f"cogs.{name}")
  print(f"{name} ReLoaded!")


for file in os.listdir("./cogs"): #Will load all COGs
      if file.endswith(".py"):
            print("Load "+file)
            bot.load_extension(f"cogs.{ file[:-3] }")


keep_alive()
bot.run(os.getenv("TOKEN"))  #Secret Stuff
