import random
from models.models import models
import discord
import json
import requests

class controller:
  def __init__(self):
        self.model = models()

  def choose(self, list):
      return random.choice(list)

  def choose_v2(self,list,amount):
        return random.sample(list,amount)

  def choose_num_between(self,int1,int2):
      return random.randint(int1,int2)

  def help(self):
    result = "This is just an alpha bot, still in development.\nCreated by: Sdrrv, Galbatorix, Doginainar, TheLittleDwarf, Fl4shKiller, Bkn, Gonxalor,ChiP.\nIST\n"+("-"*110)
    return result
  
  def join(self, channel):
    try:
      return channel.connect()
    except Exception as e:
      print("Bot Already Connected.")
      #raise e

  def leave(self, voice_client):
    return voice_client.disconnect()

  def play(self, voice_client,music):
    audio = discord.FFmpegPCMAudio(source="./sounds/"+music)
    voice_client.play(source=audio, after=None)
  
  def stop(self,voice_client):
    voice_client.stop()

  def get_member(self, guild,id):
      return guild.get_member(id)
  
  def disconnect_member(self, member):
    return member.move_to(None)

  def get_disconnect_phrase(self):
      return random.choice(self.model.get_disconnect_phrases())
  
  def get_bombed_phrase(self):
        return random.choice(self.model.get_bombed_phrases())

  def get_cat_photo(self):
        request = requests.get("https://api.thecatapi.com/v1/images/search")
        data = json.loads(request.text)
        return data[0]["url"]
  
  def is_in_voice_channel(self,voice_channel,user):
        return user in voice_channel.members
        

  def debug(self, clx):
        print(clx.guild.name)
        print(clx.message.author)
        print(clx.message.content)
