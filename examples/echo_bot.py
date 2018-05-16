# -*- coding: utf-8 -*-

import os
from flask import Flask, request, jsonify
import pymongo
import numpy
import konlpy

connection = pymongo.MongoClient("localhost", 27017)

db = connection.testDB
collectionInfo = db.collection_names()
print(collectionInfo)
collection  = db.testCollection
app = Flask(__name__)

@app.route('/')
def main():
    return 'Welcome to echo bot server!'

@app.route('/keyboard')
def Keyboard():
    dataSend = {
        "type": "buttons",
        "buttons": ["시작하기", "도움말"]
    }

    return jsonify(dataSend)


@app.route('/message', methods=['POST'])
def Message():
    dataReceive = request.get_json()
    content = dataReceive['content']
    echo = "Echo : " + content
    dataSend = {
        "message" : {
            "text" : echo
        }
    }
    print(echo)
    collection.insert({"message" : echo})
    docs = collection.find()
    for doc in docs:
        print(doc)
    return jsonify(dataSend)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)