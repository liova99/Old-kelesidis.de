# coding=utf-8
from flask import render_template, Blueprint, flash, request,redirect
from bokeh.embed import components

from ..my_func.leo_markt import *  # my functions
from ..my_func.my_plots import leo_markt_total_chart as lmtc # total income chart

leo_markt_blueprint = Blueprint("leo_markt", __name__)

# Get ajax Form:
@leo_markt_blueprint.route("/leo_markt_details", methods = ["GET", "POST"])
def leo_markt_details():
    if request.method == "POST":
        show_details_id = request.form.get("details_id")
        print(show_details_id)
        details = show_details(show_details_id)

        return details


@leo_markt_blueprint.route("/leo_markt/", methods = ["GET", "POST"])
def leo_martk():

    title = "Market DataBase Example"

    categories = import_categories()
    products_zip = show_products()

    # total income chart
    f = lmtc()
    script, div = components(f)

    # request.form[" form name"] == "form value"
    if (request.method == "POST") and (request.form["add"] == "add_product"):
        add_product()
        print ("product added")
    elif (request.method== "POST") and (request.form["add"] == "update_availability"):
        update_availability()
    elif (request.method == "POST") and (request.form['add'] == "add_category"):
        add_category()
    elif (request.method == "POST" ) and (request.form['add'] == "remove_category"):
         remove_category()
    elif (request.method == "POST" ) and (request.form['add'] == "refresh"):
        return render_template("/leo_markt/leo_markt.html", title = title, categories = categories,
                               products_zip = products_zip, script = script, div = div)
    elif (request.method == "POST" ) and (request.form['add'] == "delete_product"):
        delete_product()
    elif (request.method == "POST") and (request.form['add'] == "show_products"):
        print("show products")
        show_products()
    elif (request.method == "POST" ) and (request.form['add'] == "sell_product"):
        sell_product()
    else:
        print("nothing pressed")

    print("render Template")

    return render_template("/leo_markt/leo_markt.html", title = title, categories = categories,
                           products_zip = products_zip, script = script, div = div)
