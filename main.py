import discord
import os
from controllers.controller import controller
from keep_alive import keep_alive
import time

intents = discord.Intents.all()
cont = controller()
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print(client.user)

@client.event
async def on_message(message):
    if message.author == client.user:
        return 0
    elif message.content.startswith("!fate"):
        command = message.content.split(" ")[1:]

        print(message.guild.name)
        print(message.author)
        print(message.content)

        if (command[0]=="choose"):
            await message.channel.send(cont.choose(command[1:]))
        
        elif(command[0]=="help"):
            await message.channel.send(cont.help()) 
        
        elif(command[0]=="debug"): #for debugging stuff
            pass

        elif(command[0]=="roulette"):
            channel= message.author.voice.channel
            #-------------------------------------
            members= [i for i in channel.voice_states.keys()]
            to_kick= cont.choose(members)
            #-------------------------------------
            voice_client= await cont.join(channel)

            for memberid in members:
                if memberid == to_kick:
                    cont.play(voice_client,"shoot.wav")
                    while voice_client.is_playing():
                        time.sleep(.1)
                    await cont.disconnect_member(cont.get_member(message.guild,memberid))
                    break
                    
                cont.play(voice_client,"revolver_blank.wav")
                while voice_client.is_playing():
                    time.sleep(.1)
            await message.channel.send(cont.get_disconnect_phrase()+cont.get_member(message.guild,to_kick).name)
            time.sleep(3)
            await cont.leave(voice_client) #self disconnect






keep_alive()
client.run(os.getenv("TOKEN"))  #Secret Stuff
