import requests
import random
import os
import time
import string
import xml.etree.ElementTree as ET
import datetime
import json

version = "v1.0.6"

try:
    os.system('title RotMG Daily Login Claimer ' + str(version))
except Exception as e:
    print('failed setting window title', e)

def parseTime(time):
    print([int(s) for s in time.split() if s.isdigit()])
    result = [int(s) for s in time.split() if s.isdigit()][0]

    if "PM" in time.upper():
        result += 12
    return result % 24

if not os.path.exists("./config.json"):
    print("First time setup detected!\nPlease modify config.json to your liking & re-run the program\n")
    try:
        with open("./config.json", "w") as f:
            json.dump(
                {
                    "time": "02",
                    "account_list": [
                        {"username": "xyz", "password": "xyz"},
                        {"username": "xyz", "password": "xyz"},
                    ],
                },
                f,
                indent=4,
            )
        quit()
    except Exception as e:
        print("Error creating file: ./config.json")
else:
    try:
        with open("./config.json", "r") as f:
            global config
            config = json.loads(f.read())
    except:
        print("Error opening file: ./config.json")

try:
    HOUR = parseTime(config["time"])
    print("Script will run daily at " + str(HOUR) + ":00:00\n")
except Exception as e:
    HOUR = 2
    print("Error decoding time in config.json", e)
    print("Please enter a number 0-24. Defaulting to 2 AM")

try:
    ACCOUNT_LIST = config["account_list"]
except Exception as e:
    print("Error decoding account_list in config.json", e)
    print("Please enter in the format: \{'username': 'xyz', 'password': 'xyz'\}", e)
    quit()

def headerFetch():
    try:
        headersURL = "https://lullaby.cafe/loginclaimer/headers.json"
        headerResponse = requests.get(headersURL)
        return json.loads(headerResponse.text)
    except Exception as e:
        print("failed to load header data, defaulting to preset", e)
        return {
            "User-Agent": "UnityPlayer/2021.3.5f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)",
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Unity-Version": "2021.3.5f1"
        }

def generateClientToken():
    try:
        clientToken = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(40))
        print('client token:', clientToken + "\n")
        return clientToken
    except Exception as e:
        print("client token generation failed", e)
        print("retrying in 30 seconds...")
        time.sleep(30)
        generateClientToken()

def generateAccessToken(username, password, clientToken):
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
        verifyRequest = requests.post(verifyURL, data=payload1, headers=HEADERS)
        accessToken = ET.fromstring(verifyRequest.text).find('AccessToken').text
        print('access token: ' + accessToken + "\n")
        return ET.fromstring(verifyRequest.text).find("AccessToken").text
    except Exception as e:
        print("access token failed to generate", e)
        print("retrying in 30 seconds...")
        time.sleep(30)
        return generateAccessToken(username, password, clientToken)


def loadCharacterList(accessToken, clientToken):
    try:
        payload2 = {
          'doLogin': 'true',
          'accessToken': accessToken,
          'game_net': 'Unity',
          'play_platform': 'Unity',
          'game_net_user_id': ''
        }
        characterURL = 'https://www.realmofthemadgod.com/char/list'
        characterRequest = requests.post(characterURL, data=payload2, headers=HEADERS)
        ingameUsername = ET.fromstring(characterRequest.text).find('.//Account/Name').text
        print(ingameUsername, 'successfully logged in')
    except Exception as e:
        print("character list failed to load", e)
        print("retrying in 30 seconds...")
        time.sleep(30)
        loadCharacterList(accessToken, clientToken)

def fetchCalendar(accessToken, clientToken):
    try:
        payload3 = {
          'accessToken': accessToken,
          'game_net': 'Unity',
          'play_platform': 'Unity',
          'game_net_user_id': ''
        }

        calendarURL = 'https://www.realmofthemadgod.com/dailyLogin/fetchCalendar'
        calendarRequest = requests.post(calendarURL, data=payload3, headers=HEADERS)
        unlockedDays = ET.fromstring(calendarRequest.text).find(".//Unlockable").get("days")
        consecutiveDays = ET.fromstring(calendarRequest.text).find(".//Consecutive").get("days")
        print('Unlocked daily logins:', unlockedDays)
        print('Consecutive daily logins:', consecutiveDays)
        try:
            currentTime = datetime.datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
            print("Latest login time (UTC):", currentTime)
            print("------------------------\n")
        except Exception as e:
            print("time failed to display", e)
    except Exception as e:
        print("calendar failed to load", e)
        print("retrying in 30 seconds...")
        time.sleep(30)
        fetchCalendar(accessToken, clientToken)

while True:
    HEADERS = headerFetch()
    for account in ACCOUNT_LIST:
        clientToken = generateClientToken()
        accessToken = generateAccessToken(account["username"], account["password"], clientToken)
        loadCharacterList(accessToken, clientToken)
        fetchCalendar(accessToken, clientToken)
    print("waiting until " + str(HOUR) + ":00:00", "before running again")

    # sleep until HOUR
    t = datetime.datetime.today()
    future = datetime.datetime(t.year, t.month, t.day, HOUR, 0)
    if t.hour >= HOUR:
        future += datetime.timedelta(days=1)
    time.sleep((future - t).total_seconds())