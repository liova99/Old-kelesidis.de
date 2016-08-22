# coding=utf-8
from flask import render_template, Blueprint, flash, request,redirect
from bokeh.embed import components

from ..my_func.leo_markt import *  # my functions
from ..my_func.my_plots import leo_markt_total_chart as lmtc # total income chart

leo_markt_blueprint = Blueprint("leo_markt", __name__)


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
        product_name = request.form.get("product_name")
        product_description = request.form.get("product_description")
        price = request.form.get("price")
        category = request.form.get("categories")
        print("category is " + category)
        availability = request.form.get("product_availability")
        print (availability)

        # check TODO
        product_name = is_valid_name(product_name)
        product_description = is_valid_text(product_description)
        price = is_valid_price(price)
        if category == "":
            category = "Not defined"
        if availability == "":
            availability = "1"

        if (price != False) and (product_description != False) and (product_name != False):
            add_product(product_name, product_description, price, category, availability )
            flash("%s was added" % product_name, "msg")
        else:
            return render_template("/leo_markt/add_product_error.html", title = title, categories = categories,
                           products_zip = products_zip, script = script, div = div)
    elif (request.method== "POST") and (request.form["add"] == "update_availability"):
        update_availability()
    elif (request.method == "POST") and (request.form['add'] == "add_category"):
        category_name = request.form.get("category_name")
        if is_valid_category(category_name) != False:
            add_category()
        else:
            return render_template("/leo_markt/edit_category_error.html", title = title, categories = categories,
                                   products_zip = products_zip, script = script, div = div)
    elif (request.method == "POST" ) and (request.form['add'] == "remove_category"):
        category_name = request.form.get("category_name")
        if is_valid_category(category_name) != False:
            remove_category()
        else:
            return render_template("/leo_markt/edit_category_error.html", title = title, categories = categories,
                                   products_zip = products_zip, script = script, div = div)
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


@leo_markt_blueprint.route("/leo_markt/how")
def how():
    title = "Inside Leo Markt"

    return render_template("/leo_markt/how.html", title = title)

# Get ajax Form:
@leo_markt_blueprint.route("/leo_markt_details", methods = ["GET", "POST"])
def leo_markt_details():
    if request.method == "POST":
        show_details_id = request.form.get("details_id")
        print(show_details_id)
        details = show_details(show_details_id)

        return details


# render this clone pages if user make an error in the input e.g. add negative price
@leo_markt_blueprint.route("/leo_markt/add_product_error", methods = ["GET", "POST"])
def add_product_error():

    return render_template("/leo_markt/add_product_error.html")


@leo_markt_blueprint.route("/leo_markt/edit_category_error", methods = ["GET", "POST"])
def add_category_error():

    return render_template("/leo_markt/edit_category_error.html")

