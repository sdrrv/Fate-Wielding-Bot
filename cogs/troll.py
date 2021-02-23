import discord
from discord.ext import commands
from discord.ext.commands.core import command
from controllers.controller import controller
import os
import time
import json

class Troll(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cont= controller(bot)
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name="pussy", help="Just do !fate pussy and find out", brief="Wanna see some pussys?")
    async def cat(self,ctx):
        self.cont.debug(ctx)
        await self.cont.debugV2(ctx)
        await ctx.channel.send(self.cont.get_cat_photo())
        await ctx.channel.send("Here ya go ya perv have a pussy")
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name = "deus", hidden=True)
    async def kamazaki(self,ctx):
        print(ctx.author.id)
        await ctx.channel.send(f"Louvem o nosso deus <@{184715371377328128}>")
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name = "cry",brief="Just tilt your friends when they throw a tantrum")
    async def cry(self,ctx):
        self.cont.debug(ctx)
        await self.cont.debugV2(ctx)
        if not ctx.author.voice:
            await ctx.channel.send("You must be in a voice channel to do that.")
            return 1
        channel= ctx.author.voice.channel
        voice_client= await self.cont.join(channel)
        await ctx.channel.send("You made me cry :(")
        x = "crys/"+self.cont.choose(os.listdir("./sounds/crys"))
        print(x)
        self.cont.play(voice_client,x)
        while voice_client.is_playing():
            time.sleep(.1)
        time.sleep(1)
        await self.cont.leave(voice_client) #self disconnect
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name = "execute", hidden=True)
    async def execute(self,ctx):
        if(ctx.author.id not in self.cont.getAdmins()):
            return
        print("Executed")
        with open("./models/leaderBoard.json","r") as f:
                leaderBoard = json.load(f)
        for guild in self.bot.guilds:
            leaderBoard[str(guild.id)]= {
            "games":{},
            "randomizers":{
                "ban":[]
                }
            }
        with open("./models/leaderBoard.json","w") as f:
            json.dump(leaderBoard, f, indent=4)

    @commands.command(name="news",hidden=True)
    async def news(self,ctx):
        if(ctx.author.id not in self.cont.getAdmins()):
            return
        for guild in self.bot.guilds:
            general = discord.utils.find(lambda x: (x.name == 'general' or x.name =="geral"),  guild.text_channels)
            if general and general.permissions_for(guild.me).send_messages:
                print(guild.name)
                await general.send("**NEWS**\nNow you can **ban** users from using `randomizer` commands, with the new:\n`!fate randBanUser`\n`!fate randUnbanUser`")

    @commands.command(name="info",hidden=True)
    async def info(self,ctx):
        if(ctx.author.id not in self.cont.getAdmins()):
            return
        guilds= [i.name for i in self.bot.guilds]
        await ctx.channel.send(guilds)
        await ctx.channel.send(len(guilds))

    @commands.command(name = "what", hidden = True)
    async def doyoumean(self, ctx):
        await ctx.channel.send("O afonso é gay")
    
    @commands.command(name = "mute", help = "This will mute everyone in the voice chat", brief = "Will mute everyone in the voice chat")
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx):
        channel = ctx.author.voice.channel
        for member in channel.members:
            await member.edit(mute = True) 

    @commands.command(name = "unmute", help = "This will unmute everyone in the voice chat", brief = "Will unmute everyone in the voice chat")
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx):
        channel = ctx.author.voice.channel
        for member in channel.members:
            await member.edit(mute = False)
        


def setup(bot):
    bot.add_cog(Troll(bot))
