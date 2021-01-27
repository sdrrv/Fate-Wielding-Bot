import random
from models.commands import commands
import discord

class controller:
  def __init__(self):
        self.commands_dic = commands()

  def choose(self, list):
      return random.choice(list)

  def help(self):
    result = "This is just an alpha bot, stil in development.\nCreated by: Sdrrv, Galbatorix, Doginainar, TheLittleDwarf, Fl4shKiller, Bkn, Gonxalor,ChiP.\nIST\n"+("-"*110)
    return result
  
  def join(self, channel):
    return channel.connect()

  def leave(self, voice_client):
    return voice_client.disconnect()

  def play(self, voice_client,music):
    audio = discord.FFmpegPCMAudio(source="./sounds/"+music)
    voice_client.play(source=audio, after=None)
  
  def get_member(self, guild,id):
      return guild.get_member(id)
  
  def disconnect_member(self, member):
    return member.move_to(None)

  def get_disconnect_phrase(self):
      return random.choice(self.commands_dic.get_disconnect_phrases())
  
  def debug(self, clx):
        print(clx.guild.name)
        print(clx.message.author)
        print(clx.message.content)
