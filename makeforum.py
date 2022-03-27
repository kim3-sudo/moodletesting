import requests
siteurl = '192.168.122.61'
for i in range(1000):
    requests.post('http://' + siteurl + '/webservice/rest/server.php?wstoken=107f5d1ad1b8a4bc3400ab0d30291c10&wsfunction=mod_forum_add_discussion&forumid=2&subject=Star+Wars+Parent&message=Parent+discussion+for+the+Star+Wars+bot').text