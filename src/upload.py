import os
from werkzeug.utils import secure_filename
from flask import redirect, request, flash


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def update_avatar(db, username, app):
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'avatars', filename)
        file.save(path)
        flash('Successfully saved', 'success')
        db.users.update({"username": username}, {"$set": {"photo": path}})
        return redirect(request.url)
    else:
        flash('Wrong file\'s extension')
        return redirect(request.url)
    #return redirect('/cabinet')


def update_item_photo(photos, app):
    paths = []
    for file in photos:
        if file.filename == '' or not allowed_file(file.filename):
            paths.append("../static/default_item_photo.jpg")
        else:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], 'items_photo', filename)
            file.save(path)
            paths.append(path)
    return paths



