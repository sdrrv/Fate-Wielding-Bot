import discord
from discord.ext import commands
from controllers.controller import controller
import random
import asyncio


class Randomizers(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cont= controller(bot)
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name="choose", help="!fate choose S S1 S2 ... Sn, it will choose between all the Ss given", brief="Will chooose one between all arguments given")
    async def choose(self,ctx,*args):
        self.cont.debug(ctx)
        await self.cont.debugV2(ctx)
        if (len(args)==0):
            await ctx.channel.send("I cant choose from an empy list.\nDo `!fate help choose` for more information")
            return 
        await ctx.channel.send(self.cont.choose(args))
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name="choose+", brief="Similar to the choose command, but will choose more than one arg",help="Chooses multiple arguments.\nThe number of arguments choosen is given by the '<amountToChoose>', witch is the first argument\nEx:\nInput: !fate choose+ 2 Peter David Adam\nOutput: ['Adam','Peter']")
    async def chooseV2(self,ctx,amountToChoose: int,*args):
        self.cont.debug(ctx)
        await self.cont.debugV2(ctx)
        if (amountToChoose>len(args)):
            await ctx.channel.send("You can't choose more than the arguments given.")
            return
        elif(amountToChoose<=0):
            await ctx.channel.send("The number must be positive.")
            return
        await ctx.channel.send(self.cont.choose_v2(args,amountToChoose))

     #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name="nuke", help="This will kick a random number os members in a voice chat.\nYou must be in a voice chat to use.\nIn compliance with the rules, this command is an admin only command. ",brief="Will nuke some of the members in a voice chat. (Ban Perm Needed)")
    @commands.has_permissions(ban_members=True)
    async def nuke(self,ctx):
        self.cont.debug(ctx)
        await self.cont.debugV2(ctx)
        if self.cont.randIsBanned(ctx.author.id,ctx.guild.id):
            await ctx.channel.send("You were **banned** from using this command.\nOnly an **admin** can **unban** you using the `!fate randUnbanUser` command")
            return
        elif not ctx.author.voice:
            await ctx.channel.send("You must be in a voice channel to do that.")
            return 1
        channel= ctx.author.voice.channel
        #-------------------------------------
        membersId= self.cont.get_members_in_voice_channel(channel) 
        if len(membersId)<=1:
            await ctx.channel.send(f"You seem to be alone <@{ctx.author.id}>... no one to nuke")
            return 1
        num_to_kick=self.cont.choose_num_between(1,len(membersId))
        to_kick=random.sample(membersId, num_to_kick)
        #-------------------------------------
        voice_client= await self.cont.join(channel)
        self.cont.play(voice_client,"WTF BOOM Sound Byte.wav")
        await asyncio.sleep(2.8)

        result= self.cont.get_bombed_phrase()

        guild = ctx.guild
        for memberId in to_kick:
                await self.cont.disconnect_member(self.cont.get_member(guild, memberId))
                result+= f", <@{memberId}>"
        
        await ctx.channel.send(result)
        
        while voice_client.is_playing():
            await asyncio.sleep(.1)
        await asyncio.sleep(1)
        await self.cont.leave(voice_client) #self disconnect
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name = "roulette", help="!fate roulette - it will enter the voice channel of the user and kick one person Russian Roulette style\nYou must be in a voice channel to use.", brief="Will kick one user inside your voice channel, Russian Roulette style")
    #@commands.has_permissions(move_members=True) for debug still
    async def roulette(self,ctx):
        self.cont.debug(ctx)
        await self.cont.debugV2(ctx)
        if self.cont.randIsBanned(ctx.author.id,ctx.guild.id):
            await ctx.channel.send("You were **banned** from using this command.\nOnly an **admin** can **unban** you using the `!fate randUnbanUser` command")
            return
        elif not ctx.author.voice:
            await ctx.channel.send("You must be in a voice channel to do that.")
            return 1
        channel= ctx.author.voice.channel
        #-------------------------------------
        voice_states = list(self.cont.get_voice_states_in_voice_channel(channel))
        to_kick= self.cont.choose(voice_states)
        #-------------------------------------
        voice_client= await self.cont.join(channel)
        
        try:
            guild = ctx.guild
            for memberId in voice_states:
                if memberId == 801580589903904799:
                    continue
                
                if memberId == to_kick:
                    self.cont.play(voice_client,"shoot.wav")
                    while voice_client.is_playing():
                        await asyncio.sleep(.1)
                    await self.cont.disconnect_member(self.cont.get_member(guild, memberId))
                    break
                
            self.cont.play(voice_client,"revolver_blank.wav")
            while voice_client.is_playing():
                await asyncio.sleep(.1)

        except Exception as e:
            await self.cont.leave(voice_client) #self disconnect
            raise defaultException 
        
        await ctx.channel.send(self.cont.get_disconnect_phrase()+f"<@{to_kick}>")
        await asyncio.sleep(3)
        await self.cont.leave(voice_client) #self disconnect

    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name="randBanUser",brief="Ban a user from using a randomizer command.**(Admin Command)**")
    @commands.has_permissions(administrator=True)
    async def randBanUser(self,ctx,member: discord.Member):
        self.cont.debug(ctx)
        await self.cont.debugV2(ctx)
        if not self.cont.randIsBanned(member.id,ctx.guild.id):
            self.cont.randBan(member.id,ctx.guild.id)
            await ctx.channel.send(f"The user <@{member.id}>, was **Banned** from using `randomizer` commands")
            return
        await ctx.channel.send(f"The user <@{member.id}>, was already **Banned** from using `randomizer` commands")
    #!----------------------------------------------------------------------------------------------------------------------------
    @commands.command(name="randUnbanUser",brief="UnBan a user from using a randomizer command.**(Admin Command)**")
    @commands.has_permissions(administrator=True)
    async def randUnbanUser(self,ctx,member: discord.Member):
        self.cont.debug(ctx)
        await self.cont.debugV2(ctx)
        if self.cont.randIsBanned(member.id,ctx.guild.id):
            self.cont.removeRandBan(member.id,ctx.guild.id)
            await ctx.channel.send(f"The user <@{member.id}>, was **UnBanned** from using `randomizer` commands")
            return
        await ctx.channel.send(f"The user <@{member.id}>, was not **Banned** from using `randomizer` commands")
    

def setup(bot):
    bot.add_cog(Randomizers(bot))
