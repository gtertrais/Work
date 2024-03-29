#!/usr/bin/env python3
from datetime import date
import sys
import argparse
import requests
import random
import json
from io import StringIO
import urllib.request
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


def getUserInfo(header, user):
    r = requests.get(API_URL + "user/" + user, headers=header)
    if r.status_code == 200:
        data = json.loads(r.text)
        print(json.dumps(data, indent=2, sort_keys=False))
        return 0
    return 1


def autoLike(header):
    r = requests.get(API_URL + "user/recs", headers=header)
    currentTime = datetime.now()
    if r.status_code == 200:
        data = json.loads(r.text)
        with open("profile.csv", "a") as outfile:
            for profile in data["results"]:
                like_r = requests.get(API_URL + "like/" + profile["_id"], headers=header) if profile["gender"] == 1 and int(profile["birth_date"][0:4]) > 1985 else requests.get(
                    API_URL + "pass/" + profile["_id"], headers=header)
                if like_r.status_code == 200:
                    if profile["name"] == "Tinder Team":
                        print("[!] You ran out of likes")
                        return 1
                    age = int(str(date.today().year -
                                  int(profile["birth_date"][0:4])))
                    gender = ""
                    i = 0
                    if profile["gender"] == 0:
                        gender = "male"
                        if age <= 35:
                            imagePath = '/male_18-35/'
                        if age > 35 and age <= 55:
                            imagePath = '/male_36-55/'
                        elif age > 55:
                            imagePath = '/male_56+/'
                    elif profile["gender"] == 1:
                        gender = "female"
                        if age <= 35:
                            imagePath = '/female_18-35/'
                        if age > 35 and age <= 55:
                            imagePath = '/female_36-55/'
                        elif age > 55:
                            print(age)
                            imagePath = '/female_56+/'
                    else:
                        print('coucou')
                    message = profile["name"]+' '+gender+' '+str(age) + \
                        " years old"+' - ' + \
                        str(len(profile["photos"]))+' photo(s)'
                    print(message)
                    for photo in profile["photos"]:
                        photo = profile["photos"][i]["url"]
                        randomVal = random.randint(10000, 99999)
                        print("Downloading photo " + str(i+1))
                        urllib.request.urlretrieve(
                            photo, "./images"+imagePath+str(profile["gender"])+'-'+profile["name"]+'-'+str(age)+'_'+str(i+1)+str(randomVal)+'.jpg')
                        i = i + 1
                    line = profile["name"]+" ," + gender + "," + \
                        str(age) + ','+str(currentTime) + \
                        ',' + str(len(profile["photos"]))
                    outfile.write(line + "\n")
                    s = StringIO(line)
                else:
                    print("[!] Cannot like: " + profile["name"])
            print("==== DONE ====")
        return 0
    else:
        print("[!] Cannot like anyone.")
    return 1


# Parse arguments
parser = argparse.ArgumentParser(
    description='Automatically like Tinder profiles !')
parser.add_argument("user", metavar="user",
                    help="Get information about this user", action="store", nargs='?')
args = parser.parse_args()

# General infos
API_URL = "https://api.gotinder.com/"

# You can get this token by sniffing your phone's traffic
TINDER_TOKEN = os.getenv("TINDER_TOKEN")

# Tinder requests
if TINDER_TOKEN == "":
    print("[!] You must specify a TINDER_TOKEN")
    sys.exit(1)
header = {"Content-Type": "application/json", "X-Auth-Token": TINDER_TOKEN}

ret = 0
if args.user:
    ret = getUserInfo(header, args.user)
else:
    ret = autoLike(header)
sys.exit(ret)
