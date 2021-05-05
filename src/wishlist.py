from flask import request, render_template
from pymongo import MongoClient 
import os
from datetime import datetime
import ast
from src.upload import update_item_photo


def add_new_list_id(username, db):
    list_id = username + "-" + os.urandom(3).hex()
    new_wl_list = ast.literal_eval(str(db.users.find_one({"username": username})["wishlists"]))
    while list_id in new_wl_list:
        list_id = username + "-" + os.urandom(3).hex()

    new_wl_list.append(list_id)
    db.users.update({"username": username}, {"$set": {"wishlists": str(new_wl_list)}})
    return list_id


def wl_create(db, username, list_id, app):
    wl_title = request.form["wl-title"]  
    wl_description = request.form["description"]
    item_names = request.form.getlist("item-title[]")
    links = request.form.getlist("item-link[]")
    descriptions = request.form.getlist("item-descr[]")
    
    items = []
    item_id = list_id + "-" + os.urandom(3).hex()
    for i in range(len(item_names)):
        if i > 0:
            while item_id in items:
                item_id = list_id + "-" + os.urandom(3).hex()
        items.append(item_id) 
    
    db.wishlists.insert({"listid": list_id, "title": wl_title, "owner": username, "description": wl_description,
                         "items": str(items)})

    if 'file[]' not in request.files:
        paths = []
        for i in range(len(items)):
            paths.append("../static/default_item_photo.jpg")
    else:
        photos = request.files.getlist("file[]")
        paths = update_item_photo(photos, app)

    for i in range(len(items)):
        db.items.insert({"itemid": items[i], "title": item_names[i], "description": descriptions[i], "link": links[i],
                         "picture": paths[i], "reserved": "0", "date": str(datetime.now().date())})


def wl_edit(list_id, db):
    items = ast.literal_eval(str(db.wishlists.find_one({"listid": list_id})["items"]))
    items_dic = []
    for i in range(len(items)):
        items_dic.append(db.items.find_one({"itemid": items[i]}))

    return render_template("edit_wl.html", id=list_id,
                           title=db.wishlists.find_one({"listid": list_id})['title'],
                           description=db.wishlists.find_one({"listid": list_id})['description'],
                           items=items_dic)
