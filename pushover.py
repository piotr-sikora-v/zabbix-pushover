#!/usr/bin/python3

import http.client, urllib
import argparse, sys

parser = argparse.ArgumentParser(description='Send Zabbix notification to Pushover enabled devices.')
parser.add_argument('appkey', type=str, help='Application Token/Key')
parser.add_argument('userkey', type=str, help='User Key')
parser.add_argument('subject', type=str, help='Subject')
parser.add_argument('message', help='Message')
parser.add_argument('--emergency', metavar=('retry', 'expire'), help="set emergency mode with retry and expire time in seconds", default=False, required=False, nargs=2, type=int)



args = parser.parse_args()
app_token = args.appkey
user_key = args.userkey
subject = args.subject
message = args.message

conn = http.client.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": app_token,
    "user": user_key,
    "message": message,
    "html": 1,
  }), { "Content-type": "application/x-www-form-urlencoded" })
print(conn.getresponse())
#    "priority": 2,
#    "retry": 10,
#    "expire": 60,
