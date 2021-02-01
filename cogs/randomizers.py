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



def setup(bot):
    bot.add_cog(Randomizers(bot))