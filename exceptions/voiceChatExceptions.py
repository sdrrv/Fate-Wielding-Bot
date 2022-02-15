class UserNotInTheVoiceChatException(Exception):
    def __init__(self):
        super().__init__("You must be in a voice channel to do that.")