from flask import Blueprint, render_template, request
from bokeh.embed import components

# MySQL connection
# Warning! the password import must be above the connection import!!
from app.passwords import *
from config import mysql_connect

finance_blueprint = Blueprint('finance_blueprint', __name__)

# finance_data() need an argument, so: defaults={'fin': 'TSLA'}
# <string:fin> now we can add the company name on the link : http://127.0.0.1:5000/historical_data/AAPL
@finance_blueprint.route('/historical_data/', defaults={'fin': 'TSLA'}, methods = ['GET', 'POST'])
@finance_blueprint.route('/historical_data/<string:fin>', methods = ['GET', 'POST'])
def finance_data(fin ):
    title = 'finance'

    from ..my_func.my_plots import finance, info





    if (request.method == "POST") or (fin != 'TSLA'):
        #fin = str(request.form.get('chart'))
        cur, conn = mysql_connect('test')

        # MySQL command, for str don't forget the "" ( " %s " )
        # | finance is the db table, (search) is the column name |
        cur.execute( 'INSERT INTO finance (search) VALUES( "%s" )' %fin )
        conn.commit()
        print ( 'Connected!!!' )
        cur.close()
        conn.close()
        print ('connection closed')
    else:
        pass


    f = finance(fin)
    info = info(fin)
    info  = info.to_html(classes='info_table')

    script, div = components(f)

    return render_template('finance.html/', title = title, script = script, div = div, info = info)
