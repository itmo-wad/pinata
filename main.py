from flask import Flask, request, flash, render_template, send_from_directory
from pymongo import MongoClient 
from src.search import wl_search, wl_show

client = MongoClient('localhost',27017)
db = client.pinata
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static", "favicon.ico", mimetype="image/vnd.microsoft.icon")


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return wl_search(db)
    else:
        return render_template("index.html")
        
        
@app.route('/wishlist/<string:listid>', methods=["GET", "POST"])
def wihlist(listid):
    if request.method == "GET":
        return wl_show(db, listid)


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)