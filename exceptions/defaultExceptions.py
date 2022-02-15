class defaultException(Exception):
    def __init__(self):
        super().__init__("**Something went wrong**... We are sorry. If you think this is a `bug` pls **report it**.")