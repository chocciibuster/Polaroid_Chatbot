from Member import Member
import json

class Pool:
    def __init__(self, members):
        self.members = members
        self.goal    = 100000 * len(members)
        self.balance = 0
        self.status  = "Spenden werden gesammelt"


    def printMembers(self):
        str = ""

        if len(self.members) == 1:
            str = self.members[0].username + " ist Mitglied des Pools."

        else:
            for member in self.members:

                if member == self.members[len(self.members) - 1]:
                    str += " und " + member.username
                elif member == self.members[len(self.members) - 2]:
                    str += " " + member.username
                else:
                    str += " " + member.username + ","

            str += " sind Mitglieder des Pools."

        print(str)


    def addMembers(self, members):
        pass

    def removeMembers(self, members):
        pass
