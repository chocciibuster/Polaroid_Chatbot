class Command(object):
    def __init__(self, command, cooldown = 10, prefix = "!", response = ""):

        self.prefix   = prefix
        self.command  = command
        self.response = response
        self.cooldown = cooldown
