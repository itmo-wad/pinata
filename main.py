from flask import Flask
from pymongo import MongoClient 

app = Flask(__name__)
client = MongoClient('localhost',27017)
db = client.pinata


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)