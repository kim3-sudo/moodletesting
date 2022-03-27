import requests
import threading
import random
import json

usernames = json.loads(open("usernames.json", "r").read())
password = '%4B%65%6E%79%6F%6E%35%25' # A hex encoded password
siteurl = '192.168.122.61'

def run():
    username = random.choice(usernames)
    token = requests.get('http://' + siteurl + '/login/token.php?username=' + username + '&password=' + password + '&service=moodle_mobile_app').json()["token"]
    print(f'{token}')

while True:
    #run()
    #"""
    numthreads = 200
    threads = []
    for i in range(numthreads):
        t = threading.Thread(target = run)
        t.daemon = True
        threads.append(t)
    for i in range(numthreads):
        threads[i].start()
    for i in range(numthreads):
        threads[i].join()
    #"""