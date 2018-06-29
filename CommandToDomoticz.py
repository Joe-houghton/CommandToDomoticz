#!/usr/bin/env python
__author__ = 'Joe Houghton'
import logging
import json
import requests

from collections import namedtuple

# CONFIG START

DOMOTICZ_USER = ''
DOMOTICZ_PASS = ''
DOMOTICZ_ADDRESS = 'http://192.168.0.1:8080'

#CONFIG END



DomoticzDevice = namedtuple("DomoticzDevice", "name idx type")


class Domoticz:
    
    
    def __init__(self, address, user, password):
        self.address = address
        self.user = user
        self.password = password       
        self.devicesAndScenes = []

    def __populateUsingURL(self, url, deviceType):
        requestUrl = self.address + url
        print("RequestUrl: " + requestUrl)
        response = requests.get(requestUrl, auth=(self.user,self. password))
        if response.status_code != 200:
            print("Bad Request")
            return None
        jsonDevices = response.json()
        if "result" in jsonDevices:
            devices = jsonDevices["result"]
            for device in devices:
                tempDevice = DomoticzDevice(device["Name"], device["idx"], deviceType)
                self.devicesAndScenes.append(tempDevice)

    def __populateDevicesAndScenes(self):
        self.devicesAndScenes = []
        getAllSwitches = "/json.htm?type=command&param=getlightswitches"
        self.__populateUsingURL(getAllSwitches, 0)
        getAllScenes = "/json.htm?type=scenes"
        self.__populateUsingURL(getAllScenes, 1)

    def __doesDeviceExist(self, deviceName):
        deviceNameToTest = deviceName.lower()
        for device in self.devicesAndScenes:
            if device[0].lower() == deviceNameToTest :
                return device
        return None

    def __getTargetDevice(self, words):
        print("finding device...")
        wordsLength = len(words)
        targetDevice = ""
        for i in range(wordsLength - 2):
            if i > 0 :
                targetDevice += " "
            targetDevice += words[i + 2]
            returnDevice = self.__doesDeviceExist(targetDevice)
            if returnDevice != None :
                return returnDevice

        print("No matches for " + targetDevice)
        return None # No matches


    def __sendCommand(self, command, deviceId, deviceType):
        # e.g. '/json.htm?type=command&param=switchscene&idx=1'
        url = ""
        param = ""
            
        if deviceType == 0:
            param = "switchlight"
        elif deviceType == 1:
            param = "switchscene"

        jsonString = '/json.htm?type=command&'
        switchCommand = '&switchcmd='
        seq = (self.address, jsonString, "param=", param, "&idx=", deviceId, switchCommand, command)
        blankString = ''
        url = blankString.join(seq)

        print(url, '\n')
        response = requests.get(url, auth=(self.user, self.password))
        if response.status_code != 200:
            print("Bad Send Request")
            return None
                

    def ProcessCommand(self, message):
        print("Processing Domoticz Command")
        self.__populateDevicesAndScenes()
        lines = message.split('\n')
        commandUnderstood = False
        for line in lines:
            words = line.split(' ')
            if len(words) > 2:
                if words[0] == '#command':
                    commandUnderstood = True
                    self.__sendCommand(words[1], words[2], 0)
                elif words[0] == '#commandToScene':
                    commandUnderstood = True
                    self.__sendCommand(words[1], words[2], 1)
                elif words[0] == '#commandByName':
                    print("Processing Command by Name")
                    commandUnderstood = True
                    targetDevice = self.__getTargetDevice(words)
                    if targetDevice != None:
                        print("Target Device is " + targetDevice[0])
                        self.__sendCommand(words[1], targetDevice[1], targetDevice[2])
                    else:
                        print("Cannot find device: ")
            
        return commandUnderstood


    def PrintObject(self):
        print("\nAddress: " + self.address)
        print("\nUsername: " + self.user)
        print("\nPassword: " + self.password)



def main():
    domoticz = Domoticz(DOMOTICZ_ADDRESS, DOMOTICZ_USER, DOMOTICZ_PASS)
    domoticz.PrintObject()
    while True:
        userInput = input("Please enter a Command: \n")
        domoticz.ProcessCommand(userInput)
    #domoticz.ProcessCommand("#commandByName On lamp")    


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
