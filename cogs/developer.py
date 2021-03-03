import discord
from discord.ext import commands
from controllers.controller import controller
import os
import time
import json


class Developer(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cont= controller(bot)

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
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name="news",hidden=True)
    async def news(self,ctx):
        if(ctx.author.id not in self.cont.getAdmins()):
            return
        for guild in self.bot.guilds:
            general = discord.utils.find(lambda x: (x.name == 'general' or x.name =="geral"),  guild.text_channels)
            if general and general.permissions_for(guild.me).send_messages:
                print(guild.name)
                await general.send("**HypeTrain**\nWe have reatched the `50` server mark.\nIf you can go to [https://top.gg/bot/801580589903904799] vote and give suggestions!(new command ideas).")
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name="info",hidden=True)
    async def info(self,ctx):
        if(ctx.author.id not in self.cont.getAdmins()):
            return
        guilds= [i.name for i in self.bot.guilds]
        await ctx.channel.send(guilds)
        await ctx.channel.send(len(guilds))
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name= "ping", brief="Get the ping of the bot")
    async def ping(self,ctx):
        await ctx.channel.send( f"**PONG!!** - `{round(self.bot.latency,2)}`ms " )
    #!----------------------------------------------------------------------------------------------------------------------------

def setup(bot):
    bot.add_cog(Developer(bot))
