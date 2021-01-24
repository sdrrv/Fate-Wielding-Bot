import random
from models.commands import commands

class controller:
  def __init__(self):
        self.commands_dic= commands()

  def choose(self,list):
      return random.choice(list)

  def help(self):
    result="This is just an alpha bot, stil in development.\nCreated by: Sdrrv, Galbatorix, Doginainar, TheLittleDwarf, Fl4shKiller, Bkn, Gonxalor.\nIST\n"+("-"*30)
    commands=self.commands_dic.get_commands()
    for command in commands.keys():
      result+= "\n"+command+":::"+commands[command]
    return result