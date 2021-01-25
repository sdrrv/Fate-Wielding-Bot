class commands:
    def __init__(self):
        self.Dg = {
            "choose" : " !fate choose S S2 S3 - This will choose randomly between S,S2 and S3",
            "roulette" : " !fate roulette - This will disconnect a random user, like a Roussian Roulette"
        }

        self.disconnect_phrases=["See ya later ","Smell ya later ","And don´t come back you filthy pig ","You are better dead ","Right up your ass "]
    
    def get_commands(self):
        return self.Dg
    
    def get_disconnect_phrases(self):
        return self.disconnect_phrases