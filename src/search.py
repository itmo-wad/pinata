from flask import request, render_template, flash, redirect, abort
from pymongo import MongoClient 

def wl_search(db):
    list_id = request.form["search"]
    if not db.wishlists.find_one({"listid":list_id}):
        #flash("Invalid wishlist ID")
        return render_template("index.html")
    return redirect('wishlist/'+list_id)
    
    
def wl_show(db, list_id):  
    if not db.wishlists.find_one({"listid":list_id}):
        abort(404)
    return render_template("wishlist.html", id = list_id,
                            title = db.wishlists.find_one({"listid":list_id})['title'], 
                            owner = db.wishlists.find_one({"listid":list_id})['owner'],
                            description = db.wishlists.find_one({"listid":list_id})['description'],
                            items = db.wishlists.find_one({"listid":list_id})['items'])
    