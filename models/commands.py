class commands:
    def __init__(self):
        self.Dg = {
            "choose":"!fate choose S S2 S3 - This will choose randomly between S,S2 and S3"
        }

        self.disconnect_phrases=[""]
    
    def get_commands(self):
        return self.Dg
    
    def disconnect_phrases(self):
        return self.disconnect_phrases