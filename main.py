import os
from flask import Flask, request, flash, render_template, send_from_directory, redirect, url_for
from flask_login import LoginManager, login_required, logout_user, UserMixin, login_user, current_user
from pymongo import MongoClient
from src.search import wl_search, wl_show
from src.auth import login, reg

client = MongoClient('localhost', 27017)
db = client.pinata
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16).hex()
login_manager = LoginManager()
login_manager.init_app(app)


# The User Model for Flask-Login
class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password


# User Loader Function
@login_manager.user_loader
def load_user(username):
    user = db.users.find_one({'username': username})
    return User(username=user['username'], password=user['password'])


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


@app.route('/login', methods=['GET', 'POST'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('cabinet'))
    if request.method == 'POST':
        return login()
    return render_template('login.html')


# Add registration function
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('cabinet'))
    if request.method == 'POST':
        return reg()
    return render_template('register.html')


@app.route('/cabinet')
@login_required
def cabinet():
    return render_template('cabinet.html', username=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/invalid')
def invalid():
    return render_template('invalid.html')


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
