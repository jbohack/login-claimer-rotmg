import requests
import random
import os
import time
import string
import xml.etree.ElementTree as ET
import pwinput

try:
    os.system('title RotMG Daily Login Claimer')
except Exception as e:
    print('failed setting window title', e)

username = input('username to rotmg account: ')
password = pwinput.pwinput('password to rotmg account: ')

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
        print('access token:\n' + accessToken)
    except Exception as e:
        print("access token failed to generate", e)
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
        print('response:\n' + characterRequest.text)
    except Exception as e:
        print("character list failed to load", e)
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
        print('response:\n' + calendarRequest.text)
        print("\nWAITING 24 HOURS TO FETCH AGAIN\n")
        time.sleep(86400 + randomCooldown)
    except Exception as e:
        print("calendar failed to load", e)
while True:
    randomCooldown = random.randrange(600, 1800)
    generateAccessToken()
    loadCharacterList()
    fetchCalendar()
