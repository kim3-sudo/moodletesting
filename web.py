import requests
import json
import threading
import random
import re

usernames = json.loads(open("usernames.json", "r").read())
texts = json.loads(open('starwars.json', 'r').read())
discussions = json.loads(open("discussions.json", "r").read())
password = '%4B%65%6E%79%6F%6E%35%25' # A hex encoded password
siteurl = '192.168.122.61'

print('User\tToken\t\t\t\t\t\t\t\tID\tPreview')

def run():
    sampletext = random.choice(texts) # An escaped string for a message
    discussion = random.choice(discussions) # A discussion ID
    username = random.choice(usernames)
    queryuser = str(random.choice(list(range(3, 999))))
    token = requests.get('http://' + siteurl + '/login/token.php?username=' + username + '&password=' + password + '&service=moodle_mobile_app').json()["token"]
    idnum = re.findall(r'<KEY name=\"id\"><VALUE>\d+</VALUE>', requests.get('http://' + siteurl + '/webservice/rest/server.php?wstoken=' + token + '&wsfunction=core_user_get_users_by_field&field=id&values[0]=' + queryuser).text)[0][22:-8]
    postpreview = sampletext[0:20]
    requests.get('http://' + siteurl + '/webservice/rest/server.php?wstoken=' + token + '&wsfunction=mod_forum_add_discussion_post&postid=' + discussion + '&subject=Star+Wars&message=' + sampletext)
    unamepreview = username[0:4]
    print(f'{unamepreview}\t{token}\t{idnum}\t{postpreview}')
    
while True:
    numthreads = 50
    threads = []
    for i in range(numthreads):
        t = threading.Thread(target = run)
        t.daemon = True
        threads.append(t)
    for i in range(numthreads):
        threads[i].start()
    for i in range(numthreads):
        threads[i].join()