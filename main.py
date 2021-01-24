import discord
import os
from controllers.controller import controller
from keep_alive import keep_alive

cont = controller()
client = discord.Client()


@client.event
async def on_ready():
    print(client.user)


@client.event
async def on_message(message):
    if message.author == client.user:
        return 0
    if message.content.startswith("!choose"):
        print("#-" * 30)
        await message.channel.send(cont.choose(message.content.split(" ")[1:]))
        print(message.author)
        print(message.content)
        print("#-" * 30)

@client.event
async def on_message(message):
    if message.author == client.user:
        return 0
    if message.content.startswith("!Fate"):
        await message.channel.send("Something will be added where soon ;)")


keep_alive()
client.run(os.getenv("TOKEN"))  #Secret Stuff
