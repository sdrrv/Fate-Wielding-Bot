from discord.ext import commands
import gtts
from controllers.controller import controller
import os
import asyncio
import discord


class Troll(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cont= controller(bot)
        self.languages = gtts.lang.tts_langs().keys()
        self.wordLimit = 100
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name="pussy", help="Just do !fate pussy and find out", brief="Wanna see some pussys?")
    async def cat(self,ctx):
        self.cont.debug(ctx)
        await self.cont.debugV2(ctx)
        await ctx.channel.send(self.cont.get_cat_photo())
        await ctx.channel.send("Here ya go ya perv have a pussy")
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
            await asyncio.sleep(0.1)
        await asyncio.sleep(1)
        await self.cont.leave(voice_client) #self disconnect
  
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
        guild = ctx.guild
        for memberID in self.cont.get_members_in_voice_channel(channel):
            member = self.cont.get_member(guild, memberID)
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
        guild = ctx.guild
        for memberID in self.cont.get_members_in_voice_channel(channel):
            member = self.cont.get_member(guild, memberID)
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
        await ctx.channel.send(f"<@{ctx.author.id}> couldn't take your sh*t anymore")
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
            await asyncio.sleep(.2)
        await asyncio.sleep(3)
        await self.cont.leave(voice_client) #self disconnect
    #!----------------------------------------------------------------------------------------------------------------------------  
    @commands.command(name = "say", brief = "The bot will say what you write in your voice chat", help = "Ex: !fate say hello")
    
    async def say(self, ctx,lang = "en",*,text):
        self.cont.debug(ctx)
        await self.cont.debugV2(ctx)
        if not ctx.author.voice:
            await ctx.channel.send("You must be in a voice channel to do that.")
            return 1
         
        if(len(text) >= self.wordLimit):
            await ctx.channel.send("Sorry, i cant say something that big.")
            return
        
        channel= ctx.author.voice.channel
        #-------------------------------------
        voice_client= await self.cont.join(channel)
        
        if(lang in self.languages):    
            serialNumber = await self.cont.generateTextToSpeetch(text, lang)
        else:
            serialNumber = await self.cont.generateTextToSpeetch(lang + " " + text, "en")
        
        self.cont.play(voice_client,"text2Speetch"+ str(serialNumber) + ".mp3")
        while voice_client.is_playing():
            await asyncio.sleep(.1)
        await asyncio.sleep(1)
        await self.cont.leave(voice_client) #self disconnect
        os.system("rm ./sounds/text2Speetch"+ str(serialNumber) + ".mp3")

def setup(bot):
    bot.add_cog(Troll(bot))
