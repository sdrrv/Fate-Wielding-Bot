import random

from discord import channel
from models.models import models
import discord
import json
import requests
from gtts import gTTS

class controller:
    def __init__(self, bot):
        self.bot = bot
        self.model = models()
        self.admins = [201335861755772928, 608226067614007316,
                       363414378923687946, 540870123452628993]
        self.guilder = None
        self.channeler = None

    def getAdmins(self):
        return self.admins

    def choose(self, list):
        return random.choice(list)

    def choose_v2(self, list, amount):
        return " and ".join(random.sample(list, amount))

    def choose_num_between(self, int1, int2):
        return random.randint(int1, int2)

    def help(self):
        result = "This is just an alpha bot, still in development.\nCreated by: Sdrrv, Galbatorix, Doginainar, TheLittleDwarf, Fl4shKiller, Bkn, Gonxalor,ChiP.\nIST\n" + \
            ("-"*110)
        return result

    def join(self, channel):
        return channel.connect()

    def leave(self, voice_client):
        return voice_client.disconnect()

    def play(self, voice_client, music):
        audio = discord.FFmpegPCMAudio(source="./sounds/"+music)
        voice_client.play(source=audio, after=None)

    def stop(self, voice_client):
        voice_client.stop()

    def get_member(self, guild, id):
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

    def is_in_voice_channel(self, voice_channel, user):
        return user in voice_channel.members

    def debug(self, clx):
      if clx.guild:
        print(clx.guild.name)
      print(clx.message.author)
      print(clx.message.content)

    async def debugV2(self, ctx):
        if not self.guilder:
            self.guilder = self.bot.get_guild(412276518148898827)
            self.channeler = self.guilder.get_channel(809138565837488172)

        embed = discord.Embed(title=f"Server:`{ctx.guild.name}`", description=f"**Author:**`{ctx.message.author}`\n**Command:**`{ctx.message.content}`",
                              colour=discord.Colour.blue()
                              )

        await self.channeler.send(embed=embed)

    async def debugerLogGreen(self, text):
        if not self.guilder:
            self.guilder = self.bot.get_guild(412276518148898827)
            self.channeler = self.guilder.get_channel(809138565837488172)

        embed = discord.Embed(description=text, colour=discord.Colour.green())
        await self.channeler.send(embed=embed)

    async def debugerLogRed(self, text):
        if not self.guilder:
            self.guilder = self.bot.get_guild(412276518148898827)
            self.channeler = self.guilder.get_channel(809138565837488172)

        embed = discord.Embed(description=text, colour=discord.Colour.red())
        await self.channeler.send(embed=embed)

    def randIsBanned(self, member_id, guild_id):
        with open("./models/leaderBoard.json", "r") as f:
            leaderBoard = json.load(f)
        return member_id in leaderBoard[str(guild_id)]["randomizers"]["ban"]

    def randBan(self, member_id, guild_id):
        with open("./models/leaderBoard.json", "r") as f:
            leaderBoard = json.load(f)
        leaderBoard[str(guild_id)]["randomizers"]["ban"].append(member_id)
        with open("./models/leaderBoard.json", "w") as f:
            json.dump(leaderBoard, f, indent=4)

    def getRandBan(self, guild_id):
        with open("./models/leaderBoard.json", "r") as f:
            leaderBoard = json.load(f)
        return leaderBoard[str(guild_id)]["randomizers"]["ban"]

    def removeRandBan(self, member_id, guild_id):
        with open("./models/leaderBoard.json", "r") as f:
            leaderBoard = json.load(f)
        leaderBoard[str(guild_id)]["randomizers"]["ban"].remove(member_id)
        with open("./models/leaderBoard.json", "w") as f:
            json.dump(leaderBoard, f, indent=4)
    
    def generateTextToSpeetch(self, myText, language):
        obj = gTTS(text = myText, lang= language, slow= False)
        obj.save("./sounds/text2Speetch.mp3")
