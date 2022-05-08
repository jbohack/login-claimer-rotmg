import requests
import random
import time
import string
import xml.etree.ElementTree as ET

username = input('username to rotmg account: ')
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
        print('access token:\n' + accessToken)
    except Exception as e:
        print("access token failed to generate", e)
def fetchCalendar():
    try:
        payload2 = {
          'accessToken': accessToken,
          'game_net': 'Unity',
          'play_platform': 'Unity',
          'game_net_user_id': ''
        }

        calendarURL = 'https://www.realmofthemadgod.com/dailyLogin/fetchCalendar'
        calendarRequest = requests.post(calendarURL, data=payload2, headers=headers)
        print('respone:\n' + calendarRequest.text)
    except Exception as e:
        print("calendar failed to claim", e)
while True:
    generateAccessToken()
    fetchCalendar()
    print("\nWAITING 24 HOURS TO FETCH AGAIN\n")
    time.sleep(86400)