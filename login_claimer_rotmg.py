import requests
import random
import os
import time
import string
import xml.etree.ElementTree as ET
import pwinput
from datetime import datetime

version = "v1.0.5"

try:
    os.system('title RotMG Daily Login Claimer ' + str(version))
except Exception as e:
    print('failed setting window title', e)

username = input('username to rotmg account: ')

try:
    password = pwinput.pwinput('password to rotmg account: ')
except Exception as e:
    print('failed to use custom input', e)
    password = input('password to rotmg account: ')

headers = {
    'User-Agent': 'UnityPlayer/2020.3.30f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)',
    'Accept': '*/*',
    'Accept-Encoding': 'deflate, gzip',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Unity-Version': '2020.3.30f1'
}

try:
    clientToken = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(40))
    print('client token:', clientToken)
except Exception as e:
    print("client token generation failed", e)
def generateAccessToken():
    try:
        payload1 = {
          'guid': username,
          'password': password,
          'clientToken': clientToken,
          'game_net': 'Unity',
          'play_platform': 'Unity',
          'game_net_user_id': ''
        }

        verifyURL = 'https://www.realmofthemadgod.com/account/verify'
        verifyRequest = requests.post(verifyURL, data=payload1, headers=headers)
        global accessToken
        accessToken = ET.fromstring(verifyRequest.text).find('AccessToken').text
        print('access token: ' + accessToken)
    except Exception as e:
        print("access token failed to generate", e)
        print("retrying in 30 seconds...")
        time.sleep(30)
        generateAccessToken()
def loadCharacterList():
    try:
        payload2 = {
          'doLogin': 'true',
          'accessToken': accessToken,
          'game_net': 'Unity',
          'play_platform': 'Unity',
          'game_net_user_id': ''
        }
        characterURL = 'https://www.realmofthemadgod.com/char/list'
        characterRequest = requests.post(characterURL, data=payload2, headers=headers)
        ingameUsername = ET.fromstring(characterRequest.text).find('.//Account/Name').text
        print(ingameUsername, 'successfully logged in')
    except Exception as e:
        print("character list failed to load", e)
        print("retrying in 30 seconds...")
        time.sleep(30)
        loadCharacterList()
def fetchCalendar():
    try:
        payload3 = {
          'accessToken': accessToken,
          'game_net': 'Unity',
          'play_platform': 'Unity',
          'game_net_user_id': ''
        }

        calendarURL = 'https://www.realmofthemadgod.com/dailyLogin/fetchCalendar'
        calendarRequest = requests.post(calendarURL, data=payload3, headers=headers)
        unlockedDays = ET.fromstring(calendarRequest.text).find(".//Unlockable").get("days")
        consecutiveDays = ET.fromstring(calendarRequest.text).find(".//Consecutive").get("days")
        print('Unlocked daily logins:', unlockedDays)
        print('Consecutive daily logins:', consecutiveDays)
        try:
            currentTime = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
            print("Latest login time (UTC):", currentTime)
        except Exception as e:
            print("time failed to display", e)
        print("\nWAITING 24 HOURS TO FETCH AGAIN\n")
        time.sleep(86400)
    except Exception as e:
        print("calendar failed to load", e)
        print("retrying in 30 seconds...")
        time.sleep(30)
        fetchCalendar()
def programRun():
    generateAccessToken()
    loadCharacterList()
    fetchCalendar()
while True:
    programRun()