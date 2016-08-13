from flask import render_template, Blueprint, flash, request,redirect

leo_markt_blueprint = Blueprint("leo_markt", __name__)


@leo_markt_blueprint.route("/leo_markt/", methods = ["GET", "POST"])
def leo_martk():

    from ..my_func.leo_markt import (import_categories, add_product, add_category, remove_category)


    title = "Market DataBase Example"

    categories = import_categories()

    if (request.method == "POST") and (request.form["add"] == "add_product"):
        add_product()
        print ("added")
    elif (request.method == "POST") and (request.form['add'] == "add_category"):
        add_category()
    elif (request.method == "POST" ) and (request.form['add'] == "remove_category"):
         remove_category()
    elif (request.method == "POST" ) and (request.form['add'] == "refresh"):
        return render_template("/leo_markt/leo_markt.html", title =title, categories = categories)
    else:
        print("nothing hapend")

    return render_template("/leo_markt/leo_markt.html", title =title, categories = categories)
