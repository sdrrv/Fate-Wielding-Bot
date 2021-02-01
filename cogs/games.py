import discord
from discord.ext import commands
from discord.ext.commands.core import command
from controllers.controller import controller
import os
import time

class Games(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cont= controller()

    @commands.command(name = "duel")
    async def duel(self,ctx,user : discord.User):
        self.cont.debug(ctx)
        if not ctx.author.voice:
            await ctx.channel.send("You must be in a voice channel to do that.")
            return 
        channel= ctx.author.voice.channel
        if (ctx.author == user):
            await ctx.channel.send("You can't start a duel with your self... Moron")
            return
        elif not(self.cont.is_in_voice_channel(channel,ctx.author) and self.cont.is_in_voice_channel(channel,user)):
            await ctx.channel.send("You both must be in the same voice channel... It's almost **High noon**")
            return
        await ctx.channel.send(f"<@{user.id}> you have been challanged for a duel! Do you accept?\nWrite `!yes` or `!no`, you have `50`sec")
        response = await self.bot.wait_for("message",timeout=50.0 ,check=lambda message: (message.author == user) and ((message.content=="!yes")or(message.content=="!no")))
        print(response)
        if(response.content == "!no"):
            await ctx.channel.send("pussy")
            return
        embed = discord.Embed(title="READ RULES", description="How to play:\nIn `10` seconds the bot will start to play an old west music.\nIn a `random` amount of seconds **a bell will ring**.\nWhen you ear the **bell** type in the chat `!bang`\n **The Fist to type wins**",
        colour = discord.Colour.blue()
        )
        embed.set_footer(text="**May the best gun slinger win**")
        voice_client=await self.cont.join(channel)
        await ctx.channel.send(embed=embed)
        time.sleep(8)
        await self.cont.play(voice_client,"duelMusic.wav")
        time.sleep(self.cont.choose_num_between(2,30))
        #await self.cont.stop(voice_client)
        await self.cont.play(voice_client,"duelBel.wav")

def setup(bot):
    bot.add_cog(Games(bot))