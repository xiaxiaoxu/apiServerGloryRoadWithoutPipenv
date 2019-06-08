#encoding=utf-8
#python3
import requests
import json
import os
import hashlib

m5 = hashlib.md5()
m5.update('wcx123wac'.encode(encoding = 'utf-8'))
pwd = m5.hexdigest()
print("pwd: %s" % pwd)


print("############login############")
data = json.dumps({'username': 'lily', 'password': pwd})
r = requests.post('http://localhost:5000/login/', data = data)

print("r.status_code: %s" % r.status_code)
print("r.text: %s" % r.text)
print("type(r.json()): %s" % type(r.json()))
print("str(r.json()): %s" % str(r.json()))
