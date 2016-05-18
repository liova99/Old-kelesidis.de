from flask import Flask, render_template, request, Blueprint
from bokeh.embed import components


#define blueprint
football_blueprint = Blueprint('football', __name__ )

@football_blueprint.route('/coutinho/')
def coutinho():
    title = 'Liverpool YNWA'

    from app.my_func.my_plots import coutinho

    l = coutinho()
    script, div = components(l)

    return render_template('football/en/epl/liverpool/coutinho.html',
                           title = title, script = script, div = div)