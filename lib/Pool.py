from Member import Member

class Pool:
    def __init__(self, members):
        self.members    = members
        self.goal       = 100000 * len(members)
        self.balance    = 0
        self.status     = 0

    def addMembers(self, members):
        pass

    def removeMembers(self, members):
        pass
