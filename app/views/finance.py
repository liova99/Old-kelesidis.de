from flask import Blueprint, render_template, request
from bokeh.embed import components

# MySQL connection
# Warning! the password import must be above the connection import!!
from app.passwords import *
from config import connection

finance_blueprint = Blueprint('finance_blueprint', __name__)


@finance_blueprint.route('/historical_data/', methods = ['GET', 'POST'])
def finance_data():
    title = 'finance'

    from ..my_func.my_plots import finance, info

    if request.method == "POST":
        fin = str(request.form.get('chart'))
        c, conn = connection()

        # MySQL command, for str don't forget the "" ( " %s " )
        c.execute( 'INSERT INTO finance (search) VALUES( "%s" )' %fin )
        conn.commit()
        print ( 'Connected!!!' )

    else:
        pass

    f = finance()
    info = info()
    info  = info.to_html(classes='info_table')

    script, div = components(f)

    return render_template('finance.html', title = title, script = script, div = div, info = info)
