import os
from flask import Flask, request, flash, render_template, send_from_directory, redirect, url_for
from flask_login import LoginManager, login_required, logout_user, UserMixin, login_user, current_user
from pymongo import MongoClient
from src.search import wl_search, wl_show, wl_cabinet
from src.auth import login, reg
from src.wishlist import wl_create, wl_edit, add_new_list_id, wl_update, wl_delete
from src.upload import update_avatar


client = MongoClient('localhost', 27017)
db = client.pinata
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16).hex()
login_manager = LoginManager()
login_manager.init_app(app)
app.config['UPLOAD_FOLDER'] = 'upload'


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
        if current_user.is_authenticated:
            return render_template("index.html", link="Cabinet")
        else:
            return render_template("index.html", link="Sign in")


@app.route('/wishlist/<string:list_id>', methods=["GET", "POST"])
def wishlist(list_id):
    if request.method == "GET":
        if current_user.is_authenticated:
            return wl_show(db, list_id, 'Cabinet')
        else:
            return wl_show(db, list_id, 'Sing in')


@app.route('/login', methods=['GET', 'POST'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('cabinet'))
    if request.method == 'POST':
        return login()
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('cabinet'))
    if request.method == 'POST':
        return reg()
    return render_template('register.html')


@app.route('/cabinet', methods=['GET', 'POST'])
@login_required
def cabinet():
    if request.method == "POST":
        if request.form['search']:
            return wl_search(db)
        else:
            return update_avatar(db, current_user.username, app)
    else:
        return wl_cabinet(db, current_user.username)
    

@app.route('/create', methods=["GET", "POST"])
@login_required
def create():
    if request.method == "GET":
        return render_template('create_wl.html')
    else:
        list_id = add_new_list_id(current_user.username, db)
        wl_create(db, current_user.username, list_id, app)
        return redirect('/wishlist/' + list_id)


@app.route('/edit/<string:list_id>', methods=["GET", "POST"])
@login_required
def edit(list_id):
    if db.wishlists.find_one({"listid": list_id, "owner": current_user.username}):
        if request.method == "GET":
            return wl_edit(list_id, db)
        if request.method == "POST":
            return wl_update(list_id, db, current_user.username, app)
    else:
        return render_template('invalid.html')

@app.route('/delete/<string:list_id>', methods=["GET", "POST"])
@login_required
def delete(list_id):
    if db.wishlists.find_one({"listid": list_id, "owner": current_user.username}):
        if request.method == "GET":
            return render_template('delete.html', title=db.wishlists.find_one({"listid": list_id})["title"])
        if request.method == "POST":
            return wl_delete(list_id, db, current_user.username)
    else:
        return render_template('invalid.html') #redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.errorhandler(401)
def not_in(e):
    return redirect('/')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/upload/<path:filename>')
def send_from_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/bootstrap/<path:filename>')
def send_bootstrap(filename):
    return send_from_directory('bootstrap', filename)


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=False)
