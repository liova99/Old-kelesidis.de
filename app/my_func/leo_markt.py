# coding=utf-8

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
    # TODO user input checks, unicode error, negative price
    if request.method == "POST":
        product_name = request.form.get("product_name")
        product_description = request.form.get("product_description")
        price = request.form.get("price")
        category = request.form.get("categories")

        cur, conn = mysql_connect("leo_markt")
        cur.execute("""INSERT INTO products (name, description, price, category) VALUES (%s,%s,%s,%s)""",
                    (product_name, product_description, price, category))
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

    # TODO "to be or not to be" to.title() or not.title()
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

    if (request.method == "POST") and (request.form['add'] == "show_products") :
        df = pd.read_sql(""" SELECT * FROM products where category = '%s' """ % selected_category, con = conn)
    elif (request.method == "POST") and (request.form['add'] == "refresh"):
        print("refresh pushed")
        df = pd.read_sql(""" SELECT * FROM products """, con = conn)
    else:
        df = pd.read_sql(""" SELECT * FROM products """, con = conn)

    df = df.set_index('id')
    pr_names = df.name.tolist()
    pr_descriptions = df.description.tolist()
    pr_prices = df.price.tolist()
    # change format from 1,000.00 to 1.000,00
    pr_prices = ['{:,.2f}€'.format(i).replace(",", "X").replace(".", ",").replace("X", ".")  for i in pr_prices]
    pr_prices = [i.decode('utf-8') for i in pr_prices]  # euro symbol not in ASCII
    pr_categories = df.category.tolist()

    products_zip = zip(pr_names, pr_descriptions, pr_prices, pr_categories)
    cur.close()
    conn.close()
    return products_zip


def delete_product():
    if request.method == "POST":
        product_to_delete = request.form.get("product_to_delete")
        cur, conn = mysql_connect("leo_markt")
        cur.execute(""" DELETE FROM products WHERE name = %s """, (product_to_delete,))
        conn.commit()
        cur.close()
        conn.close()
        flash("%s was deleted" % product_to_delete)

