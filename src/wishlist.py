from flask import request, render_template, redirect
from pymongo import MongoClient 
import os
from datetime import datetime
import ast


def wl_create(db, username):
    list_id = username + "-" + os.urandom(3).hex()
    new_wl_list = []
    new_wl_list = ast.literal_eval(str(db.users.find_one({"username":username})["wishlists"]))
    while list_id in new_wl_list:
        list_id = username + "-" + os.urandom(3).hex()
        
    new_wl_list.append(list_id)    
    db.users.update({"username": username}, {"$set": {"wishlists": str(new_wl_list)}})
    
    wl_title = request.form["wl-title"]  
    wl_description = request.form["description"]
    item_names = request.form.getlist("item-title[]")
    links = request.form.getlist("item-link[]")
    photos = request.form.getlist("file[]")
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
    
    for i in range(len(items)):
        db.items.insert({"itemid": items[i], "title": item_names[i], "description": descriptions[i], "link": links[i],
                         "picture": "../static/pic/1.jpg", "reserved": "0", "date": str(datetime.now().date())})
         
    return list_id
