import random
import discord
import os
from controllers.controller import controller
from keep_alive import keep_alive
import time

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
        
        elif(command[0]=="enter"):
            channel= message.author.voice.channel
            voice_client= await cont.join(channel)
            #-------------------------------------
            members= channel.voice_states.keys()
            to_kick= cont.choose(members)
            #-------------------------------------
            for memberid in members:
                if memberid == to_kick:
                    time.sleep(random.randint(1.0,2.0))
                    cont.play(voice_client,"shoot.wav")
                    while voice_client.is_playing():
                    time.sleep(.1)
                    
                cont.play(voice_client,"revolver_blank.wav")
                while voice_client.is_playing():
                    time.sleep(.1)
                
            await cont.leave(voice_client)






keep_alive()
client.run(os.getenv("TOKEN"))  #Secret Stuff
