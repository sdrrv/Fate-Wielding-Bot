import discord
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
    print(bot.user)
    print([i.name for i in bot.guilds])
@bot.event #On Error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.send("Command not found.")
    raise error
@bot.event #On new Server Enter
async def on_guild_join(guild):
    print(f"{guild.name}, you have a new bot now")
    general = find(lambda x: (x.name == 'general' or x.name =="geral"),  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(f"Hello there, {guild.name}!\nThank you for adding our bot, we hope you have as mutch fun using it, as we did coding it.\n"\
          + cont.help())

#--------------------------------------------------------------------------------------------------------------------------------------

@bot.command(name = "deus")
async def kamazaki(ctx):
  print(ctx.author.id)
  await ctx.channel.send(f"Louvem o nosso deus <@{184715371377328128}>")

@bot.command(name = "cry")
async def cry(ctx):
  cont.debug(ctx)
  if not ctx.author.voice:
      await ctx.channel.send("You must be in a voice channel to do that.")
      return 1
  channel= ctx.author.voice.channel
  voice_client= await cont.join(channel)
  await ctx.channel.send("You made me cry :(")
  x = "crys/"+cont.choose(os.listdir("./sounds/crys"))
  print(x)
  cont.play(voice_client,x)
  while voice_client.is_playing():
     time.sleep(.1)
  time.sleep(1)
  await cont.leave(voice_client) #self disconnect


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
@bot .command(name="pussy",
help="Just do !fate pussy and find out",
brief="Wanna see some pussys?"
)
async def cat(ctx):
  await ctx.channel.send(cont.get_cat_photo())
  await ctx.channel.send("Here ya perv have a pussy")
#--------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name="choose",
help="!fate choose S S1 S2 ... Sn, it will choose between all the Ss given",
brief="Will chooose one between all arguments given"
)
async def choose(ctx,*args):
  cont.debug(ctx)
  await ctx.channel.send(cont.choose(args))
#--------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name="nuke", 
help="This will kick a random number os members in a voice chat.\nYou must be in a voice chat to use.",
brief="Will nuke some of the members in a voice chat."
)
@commands.has_permissions(ban_members=True)
async def nuke(ctx):
  cont.debug(ctx)
  if not ctx.author.voice:
      await ctx.channel.send("You must be in a voice channel to do that.")
      return 1
  channel= ctx.author.voice.channel
  #-------------------------------------
  members= [i for i in channel.members]
  if len(members)<=1:
      await ctx.channel.send(f"You seem to be alone <@{ctx.author.id}>... no one to nuke")
      return 1
  num_to_kick=cont.choose_num_between(1,len(members))
  to_kick=cont.choose_v2(members,num_to_kick)
  #-------------------------------------
  voice_client= await cont.join(channel)
  cont.play(voice_client,"felix.wav")
  time.sleep(2)

  result= cont.get_bombed_phrase()

  for member in to_kick:
        await cont.disconnect_member(member)
        result+= f", <@{member.id}>"
  
  await ctx.channel.send(result)
  
  while voice_client.is_playing():
    time.sleep(.1)
  time.sleep(1)
  await cont.leave(voice_client) #self disconnect

@nuke.error
async def nuke_error(ctx, error):
    print("ERROR")
    cont.debug(ctx)
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.send(f"Sorry <@{ctx.message.author.id}>, you do not have permissions to do that!")

#----------------------------------------------------------------------------------------------------------------------------------------

@bot.command(name="about",
brief="A little about the bot"
)
async def about(ctx):
    cont.debug(ctx)
    await ctx.channel.send(cont.help())
#-----------------------------------------------------------------------------------------------------------------------------------------

keep_alive()
bot.run(os.getenv("TOKEN"))  #Secret Stuff
