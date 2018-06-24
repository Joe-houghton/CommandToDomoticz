#!/usr/bin/env python
__author__ = 'Joe Houghton'
import logging
import json
import requests

from collections import namedtuple


# CONFIG START

HTTP_PROXY_HOST = None
HTTP_PROXY_PORT = None

DOMOTICZ_USER = ''
DOMOTICZ_PASS = ''
DOMOTICZ_ADDRESS = 'http://192.168.0.1:8080'

#CONFIG END

class Domoticz:


    def __init__(self, address, user, password):
        self.address = address
        self.user = user
        self.password = password
        DomoticzDevice = namedtuple("DomoticzDevice", "name idx type")
        devicesAndScenes = []

    def __populateUsingURL(url, deviceType):
        requestUrl = DOMOTICZ_ADDRESS + url
        response = requests.get(requestUrl, auth=(user, password))
        if response.status_code != 200:
            print("Bad Request")
            return None
        jsonDevices = response.json()
        if "result" in jsonDevices:
            devices = jsonDevices["result"]
            for device in devices:
                tempDevice = DomoticzDevice(device["Name"], device["idx"], deviceType)
                devicesAndScenes.append(tempDevice)

    def __populateDevicesAndScenes():
        devicesAndScenes = []
        getAllSwitches = "/json.htm?type=command&param=getlightswitches"
        populateUsingURL(getAllSwitches, 0)
        getAllScenes = "/json.htm?type=scenes"
        populateUsingURL(getAllScenes, 1)

    def __doesDeviceExist(deviceName):
        deviceNameToTest = deviceName.lower()
        for device in devicesAndScenes:
            if device[0].lower() == deviceNameToTest :
                return device
        return None

    def __getTargetDevice(words):
        print("finding device...")
        wordsLength = len(words)
        targetDevice = ""
        for i in range(wordsLength - 2):
            if i > 0 :
                targetDevice += " "
            targetDevice += words[i + 2]
            returnDevice = doesDeviceExist(targetDevice)
            if returnDevice != None :
                return returnDevice

        print("No matches for " + targetDevice)
        return None # No matches


    def __sendCommand(command, deviceId, deviceType):
        # e.g. '/json.htm?type=command&param=switchscene&idx=1'
        url = ""
        param = ""

        if deviceType == 0:
            param = "switchlight"
        elif deviceType == 1:
            param = "switchscene"

        jsonString = '/json.htm?type=command&'
        switchCommand = '&switchcmd='
        seq = (address, jsonString, "param=", param, "&idx=", deviceId, switchCommand, command)
        blankString = ''
        url = blankString.join(seq)

        print(url, '\n')
        response = requests.get(url, auth=(user, password))
        if response.status_code != 200:
            print("Bad Send Request")
            return None


    def ProcessCommand(message):
        lines = message.split('\n')
        commandUnderstood = False
        for line in lines:
            words = line.split(' ')
            if len(words) > 2:
                if words[0] == '#command':
                    commandUnderstood = True
                    sendCommand(words[1], words[2], 0)
                elif words[0] == '#commandToScene':
                    commandUnderstood = True
                    sendCommand(words[1], words[2], 1)
                elif words[0] == '#commandByName':
                    print("Processing Command by Name")
                    commandUnderstood = True
                    targetDevice = getTargetDevice(words)
                    if targetDevice != None:
                        print("Target Device is " + targetDevice[0])
                        sendCommand(words[1], targetDevice[1], targetDevice[2])
                    else:
                        print("Cannot find device: ")

        return commandUnderstood

