from flask import request, render_template, flash, redirect, abort
import ast


def wl_search(db):
    list_id = request.form["search"]
    if not db.wishlists.find_one({"listid": list_id}):
        flash("Invalid wishlist ID")
        return redirect(request.url)
    return redirect('wishlist/' + list_id)


def wl_show(db, list_id, link):
    if not db.wishlists.find_one({"listid": list_id}):
        abort(404)

    username = db.wishlists.find_one({"listid": list_id})['owner']
    avatar = '../' + db.users.find_one({"username": username})['photo']
    items = ast.literal_eval(str(db.wishlists.find_one({"listid": list_id})["items"]))
    items_dic = []
    for i in range(len(items)):
        items_dic.append(db.items.find_one({"itemid": items[i]}))

    return render_template("wishlist.html", id=list_id,
                           title=db.wishlists.find_one({"listid": list_id})['title'],
                           photo=avatar, owner=username,
                           description=db.wishlists.find_one({"listid": list_id})['description'],
                           items=items_dic, go_back_link=link)


def wl_cabinet(db, username):
    avatar = db.users.find_one({"username": username})['photo']
    wishlists = ast.literal_eval(str(db.users.find_one({"username": username})["wishlists"]))
    wishlists_dic = []
    for i in range(len(wishlists)):
        wishlists_dic.append(db.wishlists.find_one({"listid": wishlists[i]}))

    return render_template('cabinet.html', username=username, photo=avatar, wishlists=wishlists_dic)
