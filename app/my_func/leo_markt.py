# coding=utf-8
from pandas import json

from flask import request, flash, render_template,redirect, url_for
from config import mysql_connect
import pandas as pd

# TODO make a Rename category func.

def import_categories():
    cur, conn = mysql_connect("leo_markt")
    cur.execute('SELECT name FROM category')
    cur.close()
    conn.close()
    categories = []
    for category in cur:
        categories.extend(category)  # cursor return a tuple from MySQL so i put it out of tuple with extend
    return categories


def add_product():
    # TODO user input checks, unicode error, negative price flash("You are so negative...")

    if request.method == "POST":
        product_name = request.form.get("product_name")
        product_description = request.form.get("product_description")
        price = request.form.get("price")
        category = request.form.get("categories")
        availability = request.form.get("product_availability")

        cur, conn = mysql_connect("leo_markt")
        cur.execute("""INSERT INTO products (name, description, price, category, availability) VALUES (%s,%s,%s,%s,%s)""",
                    (product_name, product_description, price, category, availability))
        conn.commit()
        print ("changes committed")
        cur.close()
        conn.close()
        print ("Connection closed")
        flash("%s was added" % product_name)


def add_category():

    # from app.views import leo_markt
    # leo_markt = leo_markt
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
            flash("%s category already exists" % new_category)
            return render_template("/leo_markt/leo_markt.html", title =title, categories = categories)

    else:
        cur, conn = mysql_connect("leo_markt")
        cur.execute("""INSERT INTO category (name) VALUES (%s) """, (new_category,))
        conn.commit()
        print ("changes committed")
        cur.close()
        conn.close()
        print ("Connection closed")
        flash("%s category added" % new_category)
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
        flash("%s category was removed" % selected_category)


def show_products():

    cur, conn = mysql_connect("leo_markt")
    selected_category = request.form.get("category_to_show")

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
    pr_descriptions = df.description.tolist()
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
        #cur.execute("""DELETE FROM products where id=%s """, (product_to_sell_id,))
        conn.commit()
        cur.close()
        conn.close()
        flash("%s Sold" % product_to_sell)


def show_details(show_details_id):
    # if (request.method == "POST") and (request.form['add'] == "show_details"):
        # show_details_id = request.form.get("show_details_id")
        # show_details = request.form.get("show_details")

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
        flash("%s was deleted" % product_to_delete)

