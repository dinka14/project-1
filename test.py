import json

j = '[{"EnvID": 103,"OS": "centos7","Uptime": "7101","Remote display state": "stopped","Remote display":{"mode": "off","address": "0.0.0.0"},"Autostart": "on"}]'
string = j[1:len(j)-1]
j = json.loads(string)
print j["Remote display"]["address"]
try:
    if j["Remote display"]["mode"]:
        print 'true'
except KeyError:
    print 'exception'

count = 0
while True:
    print j
    try:
        if j["Remote display"]["port"]:
            print 'port', j["Remote display"]["port"]
            break
    except KeyError:
        print 'exception'
    j.update({'Remote display': {u"mode": "off", u"address": "0.0.0.0", u"port": "1234"}})

