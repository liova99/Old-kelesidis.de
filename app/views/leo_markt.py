from flask import render_template, Blueprint, flash, request

leo_markt_blueprint = Blueprint("leo_markt", __name__)


@leo_markt_blueprint.route("/leo_markt/", methods = ["GET", "POST"])
def leo_martk():

    from ..my_func.leo_markt import import_categories
    from ..my_func.leo_markt import add_product

    title = "Market DataBase Example"

    categories = import_categories()

    if (request.method == "POST") and (request.form["add"] == "add_product"):
        add_product()
        print ("added")
    else:
        print("pizdets")


    return render_template("/leo_markt/leo_markt.html", title =title, categories = categories)
