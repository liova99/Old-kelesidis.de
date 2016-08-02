# link for this page http://kelesidis.de/charts/, just to test bokeh and pygal

#import thr app from init:
#app = Flask(__name__)
#from app import app
from bokeh.embed import components
from flask import Flask, render_template, request, Blueprint

#define blueprint
charts_blueprint = Blueprint('charts', __name__ )
#=============================== INFO ============================================
# To create a blueprint object, we import the Blueprint() class                  #
# and initialize it with the arguments name and import_name.                     #
# Usually import_name will just be __name__,                                     #
# which is a special Python variable containing the name of the current module.  #
#============================== END INFO =========================================


@charts_blueprint.route('/charts/')
def charts():
    title = 'Charts'

    from app.my_func.my_plots import HLevelLine as hl
    p = hl()
    script, div = components(p)

    #########################################################

    from app.my_func.my_plots import PygalLine as pgl

    line_chart = pgl()
    graph_data = line_chart.render_data_uri()


    return render_template('charts.html', title = title, graph_data = graph_data, script = script, div = div,)
