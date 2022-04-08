import dbl
import discord
from discord.ext import commands
import os

class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjgwMTU4MDU4OTkwMzkwNDc5OSIsImJvdCI6dHJ1ZSwiaWF0IjoxNjE4ODI5OTgzfQ.g4s4HudaT44xRO-uxXUFycYoBuJt_GRQJL_6FiJyc70" # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True) # Autopost will post your guild count every 30 minutes

    async def on_guild_post(self):
        print("Server count posted successfully")

def setup(bot):
    bot.add_cog(TopGG(bot))
