import os
import codecs
import json

from Pool import Pool
from Member import Member

def sendMessage (msg):
    Parent.SendStreamMessage(msg)

def sendUsrMessage (username, msg):
    mention = "@" + username
    sendMessage(mention + " " + msg)

def Log(x):
    Parent.Log(ScriptName, x)

def nameStartsWith (name, x):
    if name[0] == x:
        return True
    return False

def formatMember (mem):
    if mem[0] == "@":
        return mem[1:]
    return mem

def getMemberListFromData (data):

    memberArray = [Member(data.UserName)]
    argc = data.GetParamCount()

    for i in range(1, argc):
        mem = data.GetParam(i)
        if not nameStartsWith(mem, "@"):
            return []
        memberArray.append(Member(formatMember(mem)))

    return memberArray

def usersInAnyPool (memberList, pools):

    # optimize later
    for pool in pools:
        for poolmem in pool.members:
            for member in memberList:
                if member.username == poolmem.username:
                    return True
    return False

def findPoolByUsername (username, file):
    pools = readPoolsFromFile(file)

    for pool in pools:
        for mem in pool.members:
            if mem.username == username:
                return pool
    return None

def overwritePoolfileWithList (list, file):
    with open(file, 'wb') as f:
        for element in list:
            pickle.dump(element, f)

def deletePoolByUsername (username, file):

    sendUsrMessage("jambuzzed", "knobi")

    pools = readPoolsFromFile(file)

    def filt (pool):
        for mem in pool.members:
            if mem.username == username:
                return False
        return True

    writeList = filter(filt, pools)

    sendUsrMessage("jambuzzed", "knobi2")

    overwritePoolfileWithList(writeList, file)
