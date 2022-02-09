import discord
from discord import channel
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
    @commands.command(name = "what", hidden = True)
    async def doyoumean(self, ctx):
        await ctx.channel.send("O afonso é gay")
    
    @commands.command(name = "quem?", hidden = True)
    async def quem(self, ctx):
        await ctx.channel.send("**QUEM TE PERGUNTOU!?!?**")

    @commands.command(name = "bernas", hidden = True)
    async def bernas(self, ctx):
        await ctx.channel.send("O Bernardo Castiço tem um mamilo postiço")
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name = "mute", help = "This will mute everyone in the voice chat", brief = "Will mute everyone in the voice chat")
    @commands.has_permissions(ban_members=True)
    
    async def mute(self, ctx):
        if not ctx.author.voice:
            await ctx.channel.send("You must be in a voice channel to do that.")
            return 1
        self.cont.debug(ctx)
        await self.cont.debugV2(ctx)
        channel = ctx.author.voice.channel
        for member in channel.members:
            await member.edit(mute = True) 
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name = "unmute", help = "This will unmute everyone in the voice chat", brief = "Will unmute everyone in the voice chat")
    @commands.has_permissions(ban_members=True)
    
    async def unmute(self, ctx):
        if not ctx.author.voice:
            await ctx.channel.send("You must be in a voice channel to do that.")
            return 1
        self.cont.debug(ctx)
        await self.cont.debugV2(ctx)
        channel = ctx.author.voice.channel
        for member in channel.members:
            await member.edit(mute = False)
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name = "suicide", help = "Tired of talking? Give it a try ;)", brief = "Tired of talking? Give it a try ;)")
    
    async def suicide(self,ctx):
        if not ctx.author.voice:
            await ctx.channel.send("You must be in a voice channel to do that.")
            return 1
        self.cont.debug(ctx)
        self.cont.debugV2(ctx)
        await self.cont.disconnect_member(ctx.author)
        await ctx.channel.send(f"<@{ctx.author.id}> couldn't take your shit anymore")
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name = "yeahboi", help = "The longest Yeah boiiiiiiiiiii", brief = "The longest Yeah boiiiiiiiiiii")

    async def yeahboi(self, ctx):
        self.cont.debug(ctx)
        await self.cont.debugV2(ctx)
        if not ctx.author.voice:
            await ctx.channel.send("You must be in a voice channel to do that.")
            return 1
        channel= ctx.author.voice.channel
        #-------------------------------------
        voice_client= await self.cont.join(channel)
        self.cont.play(voice_client,"YeahBoiii.wav")
        while voice_client.is_playing():
            time.sleep(.2)
        time.sleep(3)
        await self.cont.leave(voice_client) #self disconnect
    #!----------------------------------------------------------------------------------------------------------------------------  

def setup(bot):
    bot.add_cog(Troll(bot))
