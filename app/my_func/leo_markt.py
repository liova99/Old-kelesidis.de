# coding=utf-8
from pandas import json

from flask import request, flash, render_template  # , redirect, url_for
from config import mysql_connect
import pandas as pd

# ====== info =================
# request.form.get("input name")
# The chart is in my_plots.py

# TODO make a Rename category func.


def is_valid_price(num):

    if len(num) == 1:
        return num
    elif num.strip():
        if (num[-1] == ".") or (num[-1] == ","):
            num = num[:-2]
            print(num)

        if (num[-2] == ",") or (num[-2] == "."):
            num = num[:] + "0"
            print(num + " type 458.5 or 458,5")

        if ("," in num) or ("." in num):

            if (num[-3] == ",") and ("." in num):
                num = num.replace(",", "X").replace(".", "").replace("X", ".")
                print(num + " type 12.356,23")

            elif (num[-3] == ".") and ("," in num):
                num = num.replace(",", "")
                print(num + " type 25,569.25")

            elif (num[-3] == ".") and (num.count(".") > 1):
                num = num.replace(".", "")
                num = num[:-2] + "." + num[-2:]
                print(num + " type 50.845.55")

            elif (num[-3] == ",") and (num.count(",") > 1):
                num = num.replace(",", "")
                num = num[:-2] + "." + num[-2:]
                print(num, " Type 50,585,50")

            elif (num[-3] == ".") or (num[-3] == ","):
                num = num.replace(",", ".")
                print(num + " type 455,55 or 45.55")

            elif (num[-3] != ",") or (num[-3] != "."):
                # num = num.replace(",", "").replace(".", "")
                flash("Check your price number, price format is 4999,99, max price is 99999,99", "price_error")
                print(num + " type 455.589 or 455,585")
                return False

        try:
            if float(num) > 99999.99:
                flash("Check your price number, price format is 4999,99. Max price is 99999,99", "price_error")
                return False
            elif float(num) < 0:
                flash("You are so negative! price format is 4999,99 Max price is 99999,99", "price_error")
                return False
            else:
                return num
        except ValueError:
            flash("Check your price number, price format is 4999,99. Max price is 99999,99", "price_error")
            return False
    else:
        flash("Add a Price. Price format is 4999,99. Max price is 99999,99", "price_error")
        return False


def is_valid_name(name):

    if name.strip():
        if (len(name) <= 32) and (len(name) >= 2):
            return name.strip(" ")
        else:
            flash("Name must be max 32 characters and min 2.", "name_error")
            return False
    else:
        flash("Name is required.", "name_error")
        return False


def is_valid_text(text):

    if text.strip():
        if (len(text) < 255) or (len(text) > 2):
            return text
        else:
            flash("Description must be max 255 characters", "error_text")
            return False


def is_valid_category(name):

    if name.strip():
        if (len(name) <= 32) and (len(name) >= 2):
            return name.strip(" ")
        else:
            flash("Category Name must be max 32 characters and min 2.", "category_error")
            return False
    flash("Your input is empty. Category Name must be max 32 characters and min 2.", "category_error")
    return False


def import_categories():
    cur, conn = mysql_connect("leo_markt")
    cur.execute('SELECT name FROM category')
    cur.close()
    conn.close()
    categories = []
    for category in cur:
        categories.extend(category)  # cursor return a tuple from MySQL so i put it out of tuple with extend
    return categories


def add_product(product_name, product_description, price, category, availability):

    if request.method == "POST":

        cur, conn = mysql_connect("leo_markt")
        cur.execute("""INSERT INTO products (name, description, price, category, availability) VALUES (%s,%s,%s,%s,%s)""",
                    (product_name, product_description, price, category, availability))
        conn.commit()
        print ("changes committed")
        cur.close()
        conn.close()
        print ("Connection closed")
        return True


def update_availability():

    product_id = request.form.get("update_availability_id")
    update_availability_qty = request.form.get("update_availability_qty")
    current_qty = request.form.get("current_qty")
    product_to_update = request.form.get("product_to_update")
    new_qty = int(current_qty) + int(update_availability_qty)

    cur, conn = mysql_connect("leo_markt")
    cur.execute(""" UPDATE products SET availability = availability + %s WHERE id= %s """, (update_availability_qty, product_id))
    conn.commit()

    cur.close()
    conn.close()

    if new_qty == 1:
        flash(""" Done!
        You have now 1 %s """ % product_to_update, "msg")
    else:
        flash(""" Done!
        you have now %s %s' s """ % (new_qty, product_to_update), "msg")


def add_category():

    def category_exists():
        if request.method == "POST":
            categories = import_categories()
            categories_lower = [category.lower() for category in categories]
            new_category = request.form.get("category_name").lower()
            print (new_category)
            if new_category in categories_lower:
                return False

    # TODO "to be or not to be" , to.title() or not.title()
    title = "Market DataBase Example"  # html page title
    categories = import_categories()
    new_category = request.form.get("category_name").title()

    # TODO: check if input is empty
    # TODO replace return render_template with return redirect
    if (request.method == "POST") and (category_exists() == False):
            flash("%s category already exists" % new_category, "msg")
            return render_template("/leo_markt/leo_markt.html", title =title, categories = categories)

    else:
        cur, conn = mysql_connect("leo_markt")
        cur.execute("""INSERT INTO category (name) VALUES (%s) """, (new_category,))
        conn.commit()
        print ("changes committed")
        cur.close()
        conn.close()
        print ("Connection closed")
        flash("%s category added" % new_category, "msg")
        # TODO make auto refresh and update the category list (Ajax/js)


def remove_category():

    if request.method == "POST":
        selected_category = request.form.get("categories_to_remove")
        cur, conn = mysql_connect("leo_markt")
        cur.execute("""DELETE FROM category WHERE name = %s """, (selected_category,))
        conn.commit()
        print("category Deledet")
        cur.close()
        conn.close()
        print("connection closed")
        flash("%s category was removed" % selected_category, "msg")


def show_products():

    cur, conn = mysql_connect("leo_markt")
    selected_category = request.form.get("category_to_show")

    if selected_category == "":
        flash("Please select a category ", "msg")

    if (request.method == "POST") and (request.form['add'] == "show_products"):
        df = pd.read_sql(""" SELECT * FROM products where category = '%s' """ % selected_category, con = conn)
    elif (request.method == "POST") and (request.form['add'] == "refresh"):
        print("refresh pushed")
        df = pd.read_sql(""" SELECT * FROM products """, con = conn)
    else:
        df = pd.read_sql(""" SELECT * FROM products """, con = conn)

    df = df.set_index('id')

    pr_id = df.index.tolist()
    pr_names = df.name.tolist()
    # pr_descriptions = df.description.tolist()
    pr_prices = df.price.tolist()
    # change format from 1,000.00 to 1.000,00
    pr_prices = ['{:,.2f} €'.format(i).replace(",", "X").replace(".", ",").replace("X", ".") for i in pr_prices]
    pr_prices = [i.decode('utf-8') for i in pr_prices]  # euro symbol not in ASCII
    pr_alailability = df.availability.tolist()
    pr_categories = df.category.tolist()

    products_zip = zip(pr_id, pr_names, pr_prices, pr_alailability, pr_categories)
    cur.close()
    conn.close()
    return products_zip


def sell_product():
    if request.method == "POST":
        product_to_sell_id = request.form.get("sell_product_id")
        print (product_to_sell_id)
        product_to_sell = request.form.get("sell_product")

        cur, conn = mysql_connect("leo_markt")
        cur.execute("""  UPDATE products SET availability = availability - 1 where id = %s  """, (product_to_sell_id,))
        cur.execute("""INSERT INTO sold (id,name,description,price,category)
         select id,name,description, price, category from products where id= %s """, (product_to_sell_id,))
        conn.commit()
        cur.close()
        conn.close()
        flash("%s Sold" % product_to_sell, "msg")


def show_details(show_details_id):
        cur, conn = mysql_connect("leo_markt")

        cur.execute(""" SELECT name, description, price, category, availability FROM products WHERE id = %s """,
                    (show_details_id,))

        # cur returns a tuple, use for looop to extract data and add to variables

        # items = cur.fetchall()
        # items_list = [
        #     items[0][0],
        #     items[0][1],
        #     '{:,.2f}€'.format(items[0][2]).replace(",", "X").replace(".", ",").replace("X", "."),
        #     items[0][3],
        #     items[0][4]
        # ]
        #
        for i in cur:
            items_dict = {
                "name": i[0],
                "description": i[1],
                "price": '{:,.2f}'.format(i[2]).replace(",", "X").replace(".", ",").replace("X", ".") + "€",
                # price = price.decode('utf-8')
                "category": i[3],
                "availability": i[4]
            }

            show_details_json = json.dumps(items_dict)

            cur.close()
            conn.close()

            return show_details_json


def delete_product():
    if request.method == "POST":
        product_to_delete = request.form.get("product_to_delete")
        product_to_delete_id = request.form.get("product_to_delete_id")

        cur, conn = mysql_connect("leo_markt")
        cur.execute(""" DELETE FROM products WHERE id = %s """, (product_to_delete_id,))
        conn.commit()
        cur.close()
        conn.close()
        flash("%s was deleted" % product_to_delete, "msg")
