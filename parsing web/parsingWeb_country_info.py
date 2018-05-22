
# coding: utf-8

# In[ ]:


import pandas
import requests
import csv
import json
import xmltodict


url = "http://apis.data.go.kr/1262000/CountryBasicService/getCountryBasicList"

code_list = []
with open("isoCode.csv", 'r') as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        code = row[0].split(',')
        code_list.append(code[0])

code_list = code_list[1:]

for n in range(len(code_list)):
    payload = {'serviceKey': '24C%2FxddyRCTiVMSQN7xGhrvODlbKHfrGG%2Bg4ryyKXO8GGVjexQKYpkSH7PHU6MamZZ9qa07Dq9h25bAohPX3Jg%3D%3D','isoCode1':code_list[n]}
    payload_str = "&".join("%s=%s" % (k,v) for k,v in payload.items())

    resp = requests.get(url,params = payload_str)

    xmlString = resp.text
     
    jsonString = json.dumps(xmltodict.parse(xmlString,encoding= 'utf-8'), indent=2, ensure_ascii=False)
 
    with open("output2.json", 'a',encoding='utf-8') as f:
        f.write(jsonString)


# In[ ]:


#-*- coding: utf-8 -*-
import json
import xmltodict
 
xmlString = resp.text
     
jsonString = json.dumps(xmltodict.parse(xmlString,encoding= 'utf-8'), indent=2,ensure_ascii=False)

print(jsonString)
 
with open("output2.json", 'w',encoding='utf-8') as f:
    f.write(jsonString)

