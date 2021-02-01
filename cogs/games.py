import discord
from discord.ext import commands
from controllers.controller import controller
import os
import time

class Games(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cont= controller()

    @commands.command(name = "duel",brief="Duel, old west style",help="With this command you will be able to duel with one of your friends.\n Just type: (!fate duel @user)\nWhere the @user is the tag\n still in beta ;)")
    async def duel(self,ctx,user : discord.Member):
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
        print(response.content)
        if(response.content == "!no"):
            await ctx.channel.send("pussy")
            return
        embed = discord.Embed(title="READ RULES", description="How to play:\nIn `10` seconds the bot will start to play an old west music.\nIn a `random` amount of seconds **the music will stop**.\nWhen the music **stops** type in the chat `!bang`\n **The First to type wins**",
        colour = discord.Colour.blue()
        )
        embed.set_footer(text="**May the best gun slinger win**")
        voice_client=await self.cont.join(channel)
        await ctx.channel.send(embed=embed)
        time.sleep(8)
        self.cont.play(voice_client,"duelMusic.wav")
        time.sleep(self.cont.choose_num_between(2,30))
        self.cont.stop(voice_client)
        await ctx.channel.send("**BANG!**")
        print("BANG!")
        bang = await self.bot.wait_for("message",timeout=30,check=lambda i: ( (i.author == ctx.author or i.author == user ) and (i.content=="!bang")) )
        self.cont.play(voice_client,"shoot.wav")
        time.sleep(1)
        if(bang.author == ctx.author):
            print("Author Wins.")
            await self.cont.disconnect_member(user)
        else:
            await self.cont.disconnect_member(ctx.author)
        await ctx.channel.send(f"Nice Shoot <@{bang.author.id}>")
        await self.cont.leave(voice_client) #self disconnect
def setup(bot):
    bot.add_cog(Games(bot))