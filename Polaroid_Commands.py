class Command(object):
    def __init__(self, command, cooldown = 10, prefix = "!", response = ""):
        self.prefix   = ""
        self.command  = command
        self.response = response
        self.cooldown = cooldown

    def gnork(self, ScriptName, user):
        return Parent.IsOnUserCooldown(ScriptName, self.command, user)

    #def handleMessage(data):
        #pass
