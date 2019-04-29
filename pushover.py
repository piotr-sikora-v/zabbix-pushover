#!/usr/bin/python3

import http.client, urllib
import argparse, sys, re

parser = argparse.ArgumentParser(description='Send Zabbix notification to Pushover enabled devices.')
parser.add_argument('appkey', type=str, help='Application Token/Key')
parser.add_argument('userkey', type=str, help='User Key')
parser.add_argument('subject', type=str, help='Subject')
parser.add_argument('message', help='Message')
parser.add_argument('--emergency', metavar=('retry', 'expire'), help="Set emergency mode with retry and expire time in seconds", default=False, required=False, nargs=2, type=int)



args = parser.parse_args()
app_token = args.appkey
user_key = args.userkey
subject = args.subject
message = args.message
emergency = args.emergency

prio = 0
s = None
retry = 0
expire = 0

for line in message.splitlines():
    x = re.findall("^Severity: ", line)
    if(x):
        s = line.split(": ")[1]
        print(s)

if(s == 'Not classified'):
    prio = -2
elif (s == 'Information'):
    prio = -1
elif (s == 'Warning'):
    prio = 0
elif (s == 'Average'):
    pior = 1
elif (s == 'High'):
    prio = 1
elif (s == 'Disaster'):
    if (emergency != False):
        prio = 2
    else:
        prio = 1


x = re.findall("^Resolved: ", subject)
if(x):
    prio = -1

if (emergency != False):
    retry = emergency[0]
    expire = emergency[1]



conn = http.client.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": app_token,
    "user": user_key,
    "message": message,
    "title": subject,
    "priority": prio,
    "html": 1,
    "retry": retry,
    "expire": expire,
  }), { "Content-type": "application/x-www-form-urlencoded" })


conn.getresponse()
#    "priority": 2,
#    "retry": 10,
#    "expire": 60,
