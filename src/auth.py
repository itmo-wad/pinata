from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, logout_user, UserMixin, login_user, current_user
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.pinata

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(username):
    user = db.users.find_one({'username': username})
    return User(username=user['username'], password=user['password'])


def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username.isalnum():
        if db.users.find_one({'username': username}):
            l_user = db.users.find_one({'username': username})
            if check_password_hash(l_user['password'], password):
                user = User(username=username, password=password)
                login_user(user)
                return redirect('/cabinet')
            else:
                flash('Wrong password!')
                return redirect(request.url)
        else:
            if password == "" or username == "":
                flash('Not all fields are filled in!')
                return redirect(request.url)
            else:
                flash('The user is not registered')
                return redirect(request.url)
    else:
        flash('Username should consist only of letters or numbers')
        return redirect(request.url)

def reg():
    username = request.form.get('username')
    password_1 = request.form.get('password1')
    password_2 = request.form.get('password2')
    if username.isalnum():
        if db.users.find_one({'username': username}):
            flash('Login is already taken. Try again')
            return redirect(request.url)
        if password_1 != password_2:
            flash("Passwords don't match!")
            return redirect(request.url)
        if password_1 == "" or password_2 == "" or username == "":
            flash('Not all fields are filled in!')
            return redirect(request.url)
        else:
            password = generate_password_hash(password_1)
            db.users.insert({'username': username, 'password': password, 'photo': '../static/avatar.jpg', 'wishlists': []})
            return redirect('/login')
    else:
        flash('Username should consist only of letters or numbers')
        return redirect(request.url)


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
