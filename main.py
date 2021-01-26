import discord
from discord.ext import commands
import os
from controllers.controller import controller
from keep_alive import keep_alive
import time

intents = discord.Intents.all()
cont = controller()
bot = commands.Bot(command_prefix="!fate ",intents = intents)

@bot.event
async def on_ready():
    print(bot.user)
    print([i.name for i in bot.guilds])
#----------------------------------------------------
@bot.command(name="roulette",
help="!fate roulette - it will enter the voice channel of the user and kick one person Russian Roulette style\nYou must be in a voice channel to use.",
brief="will kick one user inside your voice channel, Roussian Roulette style"
)
async def roulette(ctx):
  cont.debug(ctx)
  channel= ctx.author.voice.channel
  #-------------------------------------
  members= [i for i in channel.voice_states.keys()]
  to_kick= cont.choose(members)
  #-------------------------------------
  voice_client= await cont.join(channel)

  for memberid in members:
      if memberid == to_kick:
        cont.play(voice_client,"shoot.wav")
        while voice_client.is_playing():
          time.sleep(.1)
        await cont.disconnect_member(cont.get_member(ctx.guild,memberid))
        break

      cont.play(voice_client,"revolver_blank.wav")
      while voice_client.is_playing():
        time.sleep(.1)

  await ctx.channel.send(cont.get_disconnect_phrase()+cont.get_member(ctx.guild,to_kick).name)
  time.sleep(3)
  await cont.leave(voice_client) #self disconnect


@bot.command(name="choose",
help="!fate choose S S1 S2 ... Sn, it will choose between all the Ss given",
brief="Will chooose one between all arguments given"
)
async def choose(ctx,*args):
  cont.debug(ctx)
  await ctx.channel.send(cont.choose(args))

@bot.command(name="nuke")
async def nuke(ctx):
    cont.debug(ctx)
    await ctx.channel.send("Nuke those Bitches")

@bot.command(name="about",
brief="A little about the bot"
)
async def about(ctx):
    cont.debug(ctx)
    await ctx.channel.send(cont.help)


keep_alive()
bot.run(os.getenv("TOKEN"))  #Secret Stuff
