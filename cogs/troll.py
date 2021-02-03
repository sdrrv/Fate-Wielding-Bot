import discord
from discord.ext import commands
from discord.ext.commands.core import command
from controllers.controller import controller
import os
import time

class Troll(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cont= controller()
    
    @commands.command(name="pussy", help="Just do !fate pussy and find out", brief="Wanna see some pussys?")
    async def cat(self,ctx):
        self.cont.debug(ctx)
        await ctx.channel.send(self.cont.get_cat_photo())
        await ctx.channel.send("Here ya go ya perv have a pussy")
    
    @commands.command(name = "deus", hidden=True)
    async def kamazaki(self,ctx):
        print(ctx.author.id)
        await ctx.channel.send(f"Louvem o nosso deus <@{184715371377328128}>")
    
    @commands.command(name = "cry", hidden=True)
    async def cry(self,ctx):
        self.cont.debug(ctx)
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


def setup(bot):
    bot.add_cog(Troll(bot))
