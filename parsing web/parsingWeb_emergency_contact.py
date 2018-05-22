
# coding: utf-8

# In[12]:


# coding: utf-8
import pandas
import requests
import csv
import json
import xmltodict

url = "http://apis.data.go.kr/1262000/ContactService/getContactList"
sKey = '24C%2FxddyRCTiVMSQN7xGhrvODlbKHfrGG%2Bg4ryyKXO8GGVjexQKYpkSH7PHU6MamZZ9qa07Dq9h25bAohPX3Jg%3D%3D'

code_list = []
with open("isoCode.csv", 'r') as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        code = row[0].split(',')
        code_list.append(code[0])

code_list = code_list[1:]

for iso in code_list:
    payload = {'serviceKey': sKey,'isoCode1':iso}
    payload_str = "&".join("%s=%s" % (k,v) for k,v in payload.items())

    resp = requests.get(url,params = payload_str)
    xmlString = resp.text
    jsonString = json.dumps(xmltodict.parse(xmlString,encoding= 'utf-8'), indent=2, ensure_ascii=False)

    with open("emergency_contact.json", 'a',encoding='utf-8') as f:
        f.write(jsonString)


