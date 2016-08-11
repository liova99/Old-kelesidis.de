from flask import request
from config import mysql_connect

if request.method == "POST":
    product_name = request.form.get("product_name")
    product_description = request.form.get("product_description")
    price = request.form.get("price")
    category = request.form.get("categories")
    print("variables ready")
else:
    print ("pizdariki")

def import_categories():
    cur, conn = mysql_connect("leo_markt")

    cur.execute('SELECT name FROM category')
    cur.close()
    conn.close()
    categories = []
    for category in cur:
        categories.extend(category)
    return categories


def add_product():
    if request.method == "POST":
        cur, conn = mysql_connect("leo_markt")
        cur.execute('INSERT INTO products (name, description, price, category) VALUES ("%s","%s","%s","%s")'
                    % (product_name, product_description, price, category))
        conn.commit()
        print ("changes committed")
        cur.close()
        conn.close()
        print ("Connection closed")


