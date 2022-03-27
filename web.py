import requests
import json
import threading
import random
import re

usernames = json.loads(open("usernames.json", "r").read())
texts = json.loads(open('starwars.json', 'r').read())
#discussions = json.loads(open("discussions.json", "r").read())
password = '%4B%65%6E%79%6F%6E%35%25' # A hex encoded password
siteurl = '192.168.122.61'

print('User\tToken\t\t\t\t\t\t\t\tID\tPreview\t\t\t\t\tForum ID')

def run():
    sampletext = random.choice(texts) # An escaped string for a message
    username = random.choice(usernames)
    queryuser = str(random.choice(list(range(3, 999))))
    queryforum = str(random.choice([2, 6, 9, 10]))
    token = requests.get('http://' + siteurl + '/login/token.php?username=' + username + '&password=' + password + '&service=moodle_mobile_app').json()["token"]
    idnum = re.findall(r'<KEY name=\"id\"><VALUE>\d+</VALUE>', requests.get('http://' + siteurl + '/webservice/rest/server.php?wstoken=' + token + '&wsfunction=core_user_get_users_by_field&field=id&values[0]=' + queryuser).text)[0][22:-8]
    postpreview = sampletext[0:20]
    requesturi = 'http://' + siteurl + '/webservice/rest/server.php?wstoken=' + token + '&wsfunction=mod_forum_add_discussion&forumid=' + queryforum + '&subject=Star+Wars&message=' + sampletext
    unamepreview = username[0:4]
    requests.get(requesturi).text
    print(f'{unamepreview}\t{token}\t{idnum}\t{postpreview}\t{queryforum}')
    
while True:
    #run()
    #"""
    numthreads = 80
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