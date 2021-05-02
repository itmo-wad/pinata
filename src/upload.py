import os
from werkzeug.utils import secure_filename
from flask import redirect, request, flash


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def update_avatar(db, username):
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/upload/avatars', filename))
        flash('Successfully saved', 'success')
        avatar = "../static/upload/avatars/" + filename
        db.users.update({"username": username}, {"$set": {"photo": avatar}})
        return redirect(request.url)
    else:
        flash('Wrong file\'s extension')
        return redirect(request.url)
    #return redirect('/cabinet')


#def update_item_photo(db):


