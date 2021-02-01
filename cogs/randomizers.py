import discord
from discord.ext import commands
from discord.ext.commands.core import command
from controllers.controller import controller
import os
import time

class Randomizers(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cont= controller()
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name="choose", help="!fate choose S S1 S2 ... Sn, it will choose between all the Ss given", brief="Will chooose one between all arguments given")
    async def choose(self,ctx,*args):
        self.cont.debug(ctx)
        await ctx.channel.send(self.cont.choose(args))
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name="nuke", help="This will kick a random number os members in a voice chat.\nYou must be in a voice chat to use.",brief="Will nuke some of the members in a voice chat.")
    @commands.has_permissions(ban_members=True)
    async def nuke(self,ctx):
        self.cont.debug(ctx)
        if not ctx.author.voice:
            await ctx.channel.send("You must be in a voice channel to do that.")
            return 1
        channel= ctx.author.voice.channel
        #-------------------------------------
        members= [i for i in channel.members]
        if len(members)<=1:
            await ctx.channel.send(f"You seem to be alone <@{ctx.author.id}>... no one to nuke")
            return 1
        num_to_kick=self.cont.choose_num_between(1,len(members))
        to_kick=self.cont.choose_v2(members,num_to_kick)
        #-------------------------------------
        voice_client= await self.cont.join(channel)
        self.cont.play(voice_client,"explosion.wav")
        time.sleep(2)

        result= self.cont.get_bombed_phrase()

        for member in to_kick:
                await self.cont.disconnect_member(member)
                result+= f", <@{member.id}>"
        
        await ctx.channel.send(result)
        
        while voice_client.is_playing():
            time.sleep(.1)
        time.sleep(1)
        await self.cont.leave(voice_client) #self disconnect
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name = "roulette", help="!fate roulette - it will enter the voice channel of the user and kick one person Russian Roulette style\nYou must be in a voice channel to use.", brief="Will kick one user inside your voice channel, Russian Roulette style")
    async def roulette(self,ctx):
        self.cont.debug(ctx)
        if not ctx.author.voice:
            await ctx.channel.send("You must be in a voice channel to do that.")
            return 1
        channel= ctx.author.voice.channel
        #-------------------------------------
        members= [i for i in channel.members]
        to_kick= self.cont.choose(members)
        #-------------------------------------
        voice_client= await self.cont.join(channel)

        for member in members:
            if member == to_kick:
                self.cont.play(voice_client,"shoot.wav")
                while voice_client.is_playing():
                    time.sleep(.1)
                await self.cont.disconnect_member(member)
                break

            self.cont.play(voice_client,"revolver_blank.wav")
            while voice_client.is_playing():
                time.sleep(.1)

        await ctx.channel.send(self.cont.get_disconnect_phrase()+f"<@{to_kick.id}>")
        time.sleep(3)
        await self.cont.leave(voice_client) #self disconnect


def setup(bot):
    bot.add_cog(Randomizers(bot))
