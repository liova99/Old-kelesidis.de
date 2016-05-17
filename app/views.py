#import thr app from init:
#app = Flask(__name__)
from app import app

from bokeh.embed import components
from flask import Flask, render_template, request



@app.route('/charts/')
def charts():
    title = 'Charts'

    from my_func.my_plots import HLevelLine as hl
    p = hl()
    script, div = components(p)

    #########################################################

    from my_func.my_plots import PygalLine as pgl

    line_chart = pgl()
    graph_data = line_chart.render_data_uri()


    return render_template('charts.html', title = title, graph_data = graph_data, script = script, div = div,)
