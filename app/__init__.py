#=========== Unused imports ==========================
# from flask.ext.sqlalchemy import SQLAlchemy
# import pandas as pd
# import datetime
# #import pygal
# # from bokeh.charts import Line, output_file
# from bokeh.models import HoverTool
# from bokeh.plotting import figure
# import pandas.io.data as web
# from bokeh.models.sources import ColumnDataSource
#=====================================================

from bokeh.embed import components
from flask import Flask, render_template, request



# MySQL connection
# Warning! the password import must be above the connection import!!
from app.passwords import *
from config import connection

# Blueprints import
from app.views.charts import charts_blueprint
from app.views.finance import finance_blueprint
from app.views.football import football_blueprint


app = Flask(__name__)


#Blueprints registers
app.register_blueprint(charts_blueprint)
app.register_blueprint(football_blueprint)
app.register_blueprint(finance_blueprint)


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


if __name__ == "__main__":
    app.run(debug=True)


#========================== INFO =====================================
#  The foloving info is when we don't use blueprints we must import
#  our views in the bottom.
#=====================================================================
#  If you are wondering why the import statement is at the end
#  and not at the beginning of the script as it is always done,
#  the reason is to avoid circular references,
#  because you are going to see that the views module
#  needs to import the app variable defined in this script.
#  Putting the import at the end avoids the circular import error.
#=========================END INFO ===================================

#======== url_for, link test==========
# with app.test_request_context():
#     print (url_for('static'  css/'))
#====================================

