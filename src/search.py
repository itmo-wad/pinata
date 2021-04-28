from flask import request, render_template, flash
from pymongo import MongoClient 

def wl_search(db):
    id = request.form["search"]
    if not db.wishlists.find_one({"listid":id}):
        #flash("Invalid wishlist ID")
        return render_template("index.html")
    return render_template("wishlist.html", id = id,
                            title = db.wishlists.find_one({"listid":id})['title'], 
                            owner = db.wishlists.find_one({"listid":id})['owner'],
                            description = db.wishlists.find_one({"listid":id})['description'],
                            items = db.wishlists.find_one({"listid":id})['items'])
    