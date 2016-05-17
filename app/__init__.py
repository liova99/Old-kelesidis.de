from bokeh.embed import components
from flask import Flask, render_template, request, redirect, abort, url_for

#import MySQLdb

# Warning! the pass import must be first!!
from app.passwords import *
from config import connection


### Unused imports ###
#from flask.ext.sqlalchemy import SQLAlchemy
# import pandas as pd
# import datetime
# #import pygal
# # from bokeh.charts import Line, output_file
# from bokeh.models import HoverTool
# from bokeh.plotting import figure
# import pandas.io.data as web
# from bokeh.models.sources import ColumnDataSource
###           ###                 ###

app = Flask(__name__)

# @app.route('/static/')
# try:
#     def static():
#         pass
# except Exception as e:
#     e = render_template('index.html')
#
#
#     pass

@app.route('/', methods = ['GET', 'POST'])
def homepage():
    title = 'home'

    if request.method == 'POST':
        f= request.files['the_file']
        f.save('C:\Users\levan\Desktop')

    return render_template('index.html', title = title)

@app.route('/coutinho/')
def pandasPage():
    title = 'Liverpool YNWA'

    from my_func.my_plots import liverpool as lp

    l = lp()
    script, div = components(l)

    return render_template('football/en/epl/liverpool/coutinho.html',
                           title = title, script = script, div = div)

# @app.route('/charts/')
# def charts():
#     title = 'Charts'
#
#     from my_func.my_plots import HLevelLine as hl
#     p = hl()
#     script, div = components(p)
#
#     #########################################################
#
#     from my_func.my_plots import PygalLine as pgl
#
#     line_chart = pgl()
#     graph_data = line_chart.render_data_uri()
#
#
#     return render_template('charts.html', title = title, graph_data = graph_data, script = script, div = div,)





#create connection

#Once the connection is created,
#  we'll require a cursor to query our stored procedure.
# So, using conn connection, create a cursor.

#c = conn.cursor()

@app.route('/finance/', methods = ["GET", "POST"])
def finance():
    title = 'finance'

    from my_func.my_plots import finance, info

    if request.method == "POST":
        fin = str(request.form.get('chart'))
        c, conn = connection()

        #MySQL command, for str dont forget the "" ( " %s " )
        c.execute( 'INSERT INTO finance (search) VALUES( "%s" )' %fin )
        conn.commit()
        print ('Connected!!!')

    else:
        pass

    f = finance()
    info = info()
    info  = info.to_html(classes='info_table')

    script, div = components(f)

    return render_template('finance.html', title = title, script = script, div = div, info = info)


# with app.test_request_context():
#     print (url_for('static'  css/'))

#####   import views   ##########

#If you are wondering why the import statement is at the end
# and not at the beginning of the script as it is always done,
#  the reason is to avoid circular references,
#  because you are going to see that the views module
#  needs to import the app variable defined in this script.
#  Putting the import at the end avoids the circular import error.

from app import views

if __name__ == "__main__":
    app.run(debug=True)






