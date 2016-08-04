from flask import Blueprint, render_template, request
from bokeh.embed import components

# MySQL connection
# Warning! the password import must be above the connection import!!
from app.passwords import *
from config import mysql_connect

finance_blueprint = Blueprint('finance_blueprint', __name__)

# finance_data() need an argument, so: defaults={'fin': 'TSLA'}
# <string:selected_company> now we can add the company name on the link e.g. : http://kelesidis.de/historical_data/AAPL
@finance_blueprint.route('/historical_data/', defaults={'selected_company': 'TSLA'}, methods = ['GET', 'POST'])
@finance_blueprint.route('/historical_data/<string:selected_company>', methods = ['GET', 'POST'])
def finance_data(selected_company):
    title = 'Historical Stock Prices'

    from ..my_func.my_plots import finance, info

    if (request.method == "POST") or (selected_company != 'TSLA'):
        #selected_company = str(request.form.get('chart'))
        cur, conn = mysql_connect('test')

        # MySQL command, for str don't forget the "" ( " %s " )
        # | finance is the db table, (search) is the column name |
        cur.execute( 'INSERT INTO finance (search) VALUES( "%s" )' % selected_company)
        conn.commit()
        print ( 'Connected!!!' )
        cur.close()
        conn.close()
        print ('connection closed')
    else:
        pass


    f = finance(selected_company)
    info = info(selected_company)
    info  = info.to_html(classes='info_table')

    script, div = components(f)

    return render_template('finance.html', title = title, script = script, div = div, info = info)
