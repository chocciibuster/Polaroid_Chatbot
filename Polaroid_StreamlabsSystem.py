#!/usr/bin/env python
# -*- coding: utf-8 -*-

#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
import types


class Command(object):
    def __init__(self, command, cooldown = 10, messageHandler = None, prefix = "!", response = ""):
        self.prefix   = ""
        self.command  = command
        self.response = response
        self.cooldown = cooldown

        if messageHandler is not None:
            self.handleMessage = types.MethodType(messageHandler, self)

    def IsOnUserCooldown(self, ScriptName, user):
        return Parent.IsOnUserCooldown(ScriptName, self.command, user)

    def handleMessage(self, data):
        Parent.SendStreamMessage("Hallo, ich bin der " + self.command + " Command. Nice to beep you")


sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from Settings_Module import MySettings
from Polaroid_Function import *

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName  = "Polaroids"
Website     = "https://twitch.tv/jambuzzed"
Description = "Managing&Creating Polaroid Pools"
Creator     = "Jam&0xBebop"
Version     = "1.0.0.0"

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = MySettings()

#Konstante#
MAX_POOL_MEMBERS = 5
MAX_POOLS = 5
POOLFILE = "schnib.pkl"

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

#-------------------------------------------------------------------------------

def polCreationHandler (self, data):

    owner = data.UserName
    argc  = data.GetParamCount()

    if getPoolCount(POOLFILE) >= MAX_POOLS:
        sendUsrMessage(owner, "Die maximale Anzahl an Polaroid-Pools wurde bereits erreicht :( Bitte hab ein bisschen Geduld.")
        return

    if (argc > MAX_POOL_MEMBERS):
        sendUsrMessage(owner, "Maximale Anzahl der zusätzlichen Hühnchen ist " + str(MAX_POOL_MEMBERS-1))
        return

    allPools   = readPoolsFromFile(POOLFILE)
    memberList = getMemberListFromData(data)

    if not memberList: # if list is empty
        sendUsrMessage(owner, "Eines deiner Hühnchen konnte ich nicht finden. Hühnchen müssen mit einem @ aufgelistet werden!")
        return

    if usersInAnyPool(memberList, allPools):
        sendUsrMessage(owner, "Eines deiner Hühnchen ist bereits in einem anderen Pool.")
        return

    newPool = Pool(memberList)
    appendPoolToFile(newPool, POOLFILE)

    sendUsrMessage(owner, "Euer pool wurde erfolgreich angelegt! <3")

#-------------------------------------------------------------------------------
def polSubmitHandler (self, data):
    pass
#-------------------------------------------------------------------------------
def polStatusHandler (self, data):
    pass

def polDeleteHandler (self, data):
    argc = data.GetParamCount()

    if data.UserName != "jambuzzed":
        return

    if argc != 2:
        return

    usr  = data.GetParam(1)
    #pool = findPoolByUsername(usr, POOLFILE)
    sendUsrMessage("jambuzzed", "usri: " + usr)
    allPools = readPoolsFromFile(POOLFILE)


    deletePoolByUsername(usr, POOLFILE)

    sendUsrMessage("jambuzzed", "ye pool was delet")

global polCreationCommand
global polSubmitCommand
global polStatusCommand
polCreationCommand  = Command("!polaroid", messageHandler=polCreationHandler)
polSubmitCommand    = Command("!submit")                             # eventuell neues Command, wenn wir nen cooleren Namen finden :D
polStatusCommand    = Command("!pstatus")
polDeleteCommand    = Command("!deletepool", messageHandler=polDeleteHandler)

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)

    #   Create commands
    ScriptSettings.Response = "Overwritten pong! ^_^"
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):

    if not data.IsChatMessage:
        return

    commandStr = data.GetParam(0).lower()

    global command

    # change to loop over list of possible commands later
    if commandStr == polCreationCommand.command:
        command = polCreationCommand
    elif commandStr == polSubmitCommand.command:
        command = polSubmitCommand
    elif commandStr == polStatusCommand.command:
        command = polStatusCommand
    elif commandStr == polDeleteCommand.command:
        command = polDeleteCommand
    else:
        return

    if command.IsOnUserCooldown(ScriptName, data.User):
        Parent.SendStreamMessage("Bitte warte noch einen Moment.")
        return

    command.handleMessage(data)

    Parent.AddUserCooldown(ScriptName,\
                           command.command,\
                           data.User,\
                           ScriptSettings.Cooldown)



    '''
    if command == polCreationCommand.command:
        if polCreationCommand.IsOnUserCooldown(ScriptName, data.User):
            Parent.SendStreamMessage("Time Remaining " + str(Parent.GetUserCooldownDuration(ScriptName, command, data.User)))
            return

        Parent.AddUserCooldown(ScriptName, command, data.User, ScriptSettings.Cooldown)  # Put the command on cooldown


    elif command == polSubmitCommand.command:
        return

    elif command == polStatusCommand.command:
        return
    '''

    '''
    if data.IsChatMessage():
        if data.GetParam(0).lower() == polCreationCommand.command || data.GetParam(0).lower() == polSubmitCommand.command || data.GetParam(0).lower() == polStatusCommand.command:
            if Parent.IsOnUserCooldown(ScriptName,data.GetParam(0),data.User):
                Parent.SendStreamMessage("Time Remaining " + str(Parent.GetUserCooldownDuration(ScriptName,"!bork",data.User)))

    #   Check if the propper command is used, the command is not on cooldown and the user has permission to use the command
    if data.GetParam(0).lower() == "!bork" and not Parent.IsOnUserCooldown(ScriptName,"!bork",data.User) and Parent.HasPermission(data.User,ScriptSettings.Permission,ScriptSettings.Info):
        Parent.BroadcastWsEvent("EVENT_MINE","{'show':false}")
        Parent.SendStreamMessage(ScriptSettings.Response)    # Send your message to chat
        Parent.AddUserCooldown(ScriptName,"!bork",data.User,ScriptSettings.Cooldown)  # Put the command on cooldown
    '''
    #Parent.Log(ScriptName, "0): " + data.GetParam(0) + "1) " + data.GetParam(1))

    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters)
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):

    if "$myparameter" in parseString:
        return parseString.replace("$myparameter","I am a cat!")

    return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
#def ReloadSettings(jsonData):
    ## Execute json reloading here
    #ScriptSettings.__dict__ = json.loads(jsonData)
    #ScriptSettings.Save(SettingsFile)
    #return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return
