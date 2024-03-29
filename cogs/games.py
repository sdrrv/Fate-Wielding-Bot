import discord
from discord.ext import commands
from controllers.controller import controller
import os
import asyncio
from exceptions.defaultExceptions import defaultException
class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cont = controller(bot)

    @commands.command(name="duel", brief="Duel, old west style", help="With this command you will be able to duel with one of your friends.\n Just type: (!fate duel @user)\nWhere the @user is the tag\n still in beta ;)")
    async def duel(self, ctx, user: discord.Member):
        self.cont.debug(ctx)
        await self.cont.debugV2(ctx)
        if not ctx.author.voice:
            await ctx.channel.send("You must be in a voice channel to do that.")
            return
        
        channel = ctx.author.voice.channel

        if (ctx.author == user):
            await ctx.channel.send("You can't start a duel with your self... Moron")
            return
        elif not(self.cont.is_in_voice_channel(channel, ctx.author) and self.cont.is_in_voice_channel(channel, user)):
            await ctx.channel.send("You both must be in the same voice channel... It's almost **High noon**")
            return
        await ctx.channel.send(f"<@{user.id}> you have been challanged for a duel! Do you accept?\nWrite `!yes` or `!no`, you have `50`sec")

        try:
            response = await self.bot.wait_for("message", timeout=50.0, check=lambda message: (message.author == user) and ((message.content == "!yes") or (message.content == "!no")))
        except Exception:
            await ctx.channel.send(f"Opps... You dind't respond in time <@{user.id}>")
            return

        print(response.content)
        if(response.content == "!no"):
            await ctx.channel.send(f"<@{user.id}> pussy.")
            return
        embed = discord.Embed(title="READ RULES", description="How to play:\nIn `10` seconds the bot will start to play an old west music.\nIn a `random` amount of seconds **the music will stop**.\nWhen the music **stops** type in the chat `!bang`\n **The First to type wins**",
                              colour=discord.Colour.blue()
                              )
        embed.set_footer(text="**May the best gun slinger win**")
        voice_client = await self.cont.join(channel)
        await ctx.channel.send(embed=embed)
        asyncio.sleep(8)
        self.cont.play(voice_client, "duelMusic.wav")
        asyncio.sleep(self.cont.choose_num_between(4, 30))
        self.cont.stop(voice_client)
        await ctx.channel.send("**BANG!**")
        print("BANG!")
        #! On the works... Causing Some Problems here.
        try:
            bang = await self.bot.wait_for("message", timeout=10, check=lambda i: ((i.author == ctx.author or i.author == user) and (i.content == "!bang")))
        except Exception:
            await ctx.channel.send(f"No Shoots... <@{user.id}>, <@{ctx.author.id}> you peace loving freaks.")
            await self.cont.leave(voice_client)  # self disconnect
            return

        self.cont.play(voice_client, "shoot.wav")
        asyncio.sleep(1)
        if(bang.author == ctx.author):
            print("Author Wins.")
            await self.cont.disconnect_member(user)
        else:
            await self.cont.disconnect_member(ctx.author)
        await ctx.channel.send(f"Nice Shoot <@{bang.author.id}>")
        await self.cont.leave(voice_client)  # self disconnect
    #!----------------------------------------------------------------------------------------------------------------------------
    
    @commands.command(name="silence", brief="Will kick all the users in the chat that aren't muted.", hidden=False)
    async def silence(self, ctx):
        self.cont.debug(ctx)
        await self.cont.debugV2(ctx)
        if not ctx.author.voice:
            await ctx.channel.send("You must be in a voice channel to do that.")
            return

        embed = discord.Embed(title="READ RULES", description="How to play:\nIn `10` seconds the **ghost of all the kicked members will join the voice chat**. \n**He will say some ghost stuff**, idk... the guy likes to talk...\nWhen he **stops talking ** all the members in the chat who **are not muted will be kicked**\n `SILENCE YOURSELF IF YOU DO NOT WANT TO DIE`",

                              colour=discord.Colour.red()
                              )
        embed.set_footer(text="I'm coming in...SILENCE!!!")
        await ctx.channel.send(embed=embed)

        try: # Will enter the voice channel
            channel = ctx.author.voice.channel
            voice_client = await self.cont.join(channel)
        except Exception as e:
            raise defaultException
        
        await asyncio.sleep(8)

        x = "ghost/"+self.cont.choose(os.listdir("./sounds/ghost"))
        self.cont.play(voice_client,x)
        while voice_client.is_playing():
            await asyncio.sleep(.1)
        
        print(x)
        try:
            guild = ctx.guild
            voice_states = self.cont.get_voice_states_in_voice_channel(channel)
            for memberId in voice_states:
                if memberId == 801580589903904799:
                    continue
                if not voice_states[memberId].self_mute and not voice_states[memberId].mute:
                    await self.cont.disconnect_member(self.cont.get_member(guild, memberId))
    
        except Exception as e:
            await self.cont.leave(voice_client) #self disconnect
            raise defaultException 


        await asyncio.sleep(1)
        await self.cont.leave(voice_client) #self disconnect

    #!----------------------------------------------------------------------------------------------------------------------------


def setup(bot):
    bot.add_cog(Games(bot))
