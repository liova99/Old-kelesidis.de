# coding=utf-8
from flask import render_template, Blueprint, flash, request,redirect

from ..my_func.leo_markt import *  # my functions

leo_markt_blueprint = Blueprint("leo_markt", __name__)

# Get ajax Form:
@leo_markt_blueprint.route("/leo_markt_details", methods = ["GET", "POST"])
def leo_markt_details():
    if request.method == "POST":
        show_details_id = request.form.get("details_id")
        print(show_details_id)
        details = show_details(show_details_id)
        # product_id = {"tweets" :[
        #               {"content" : "hello"},
        #               {"message" : "jsajdjd"} ]
        #               }
        # # product_id =  request.form.get("show_details_id")
        # print (product_id)

        @leo_markt_blueprint.context_processor
        def utility_processor():
            details = leo_markt_details()
            return dict(details = details)

        return details #json.dumps(detailes)

@leo_markt_blueprint.route("/leo_markt/", methods = ["GET", "POST"])
def leo_martk():

    title = "Market DataBase Example"

    categories = import_categories()
    products_zip = show_products()

    if (request.method == "POST") and (request.form["add"] == "add_product"):
        add_product()
        print ("added")
    elif (request.method == "POST") and (request.form['add'] == "add_category"):
        add_category()
    elif (request.method == "POST" ) and (request.form['add'] == "remove_category"):
         remove_category()
    elif (request.method == "POST" ) and (request.form['add'] == "refresh"):
        return render_template("/leo_markt/leo_markt.html", title = title, categories = categories,
                               products_zip = products_zip)
    elif (request.method == "POST" ) and (request.form['add'] == "delete_product"):
        delete_product()
    elif (request.method == "POST") and (request.form['add'] == "show_products"):
        print("show products")
        show_products()
    elif (request.method == "POST" ) and (request.form['add'] == "sell_product"):
        sell_product()
    # elif (request.method == "POST") and (request.form['add'] == "show_details"):
    #     show_details_json = show_details()
    #     return show_details_json




            # # show_details()
        # details_name, details_description, details_price, details_category, details_availability =  show_details()
        # return render_template("/leo_markt/leo_markt.html", title = title, categories = categories,
        #                        products_zip = products_zip, details_name = details_name,
        #                        details_description = details_description,
        #                        details_price = details_price, details_category = details_category,
        #                        details_availability = details_availability)

    else:
        print("nothing pressed")

    print("returnet here")
    return render_template("/leo_markt/leo_markt.html", title = title, categories = categories,
                           products_zip = products_zip)
