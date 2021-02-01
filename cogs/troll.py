import discord
from discord.ext import commands
from controllers import controller


class Troll(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cont= controller()
    
    @commands.command(name="pussy", help="Just do !fate pussy and find out", brief="Wanna see some pussys?")
    async def cat(self,ctx):
        await ctx.channel.send(self.cont.get_cat_photo())
        await ctx.channel.send("Here ya perv have a pussy")


def setup(bot):
    bot.add_cog(Troll(bot))