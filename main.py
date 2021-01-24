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
    elif message.content.startswith("!choose"):
        await message.channel.send(cont.choose(message.content.split(" ")[1:]))
        print(message.author)
    elif message.content.startswith("!fate"):
        command = message.content.split(" ")[1:]

        if (command[0]=="choose"):
            await message.channel.send(cont.choose(command[1:]))
        
        elif(command[0]=="help"):
            await message.channel.send(cont.help())






keep_alive()
client.run(os.getenv("TOKEN"))  #Secret Stuff
