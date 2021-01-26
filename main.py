import discord
from discord.ext import commands
import os
from controllers.controller import controller
from keep_alive import keep_alive
import time

intents = discord.Intents.all()
cont = controller()
bot = commands.Bot(command_prefix="!fate ",intents = intents)


@bot.command(name="nuke")
async def hi(ctx):
    await ctx.channel.send("Nuke those Bitches")


@bot.event
async def on_ready():
    print(bot.user)
#----------------------------------------------------
@bot.command(name="roulette")
async def roulette(ctx):
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


@bot.command(name="choose")
async def choose(ctx,*args):
  await ctx.channel.send(cont.choose(args))



keep_alive()
bot.run(os.getenv("TOKEN"))  #Secret Stuff
