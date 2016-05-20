from flask import Flask, render_template, request, Blueprint
from bokeh.embed import components
#Temp imports for the API
import httplib
import json
import pandas as pd

# MySQL connection
# Warning! the password import must be above the connection import!!
from app.passwords import *
from config import mysql_connect

#define blueprint
football_blueprint = Blueprint('football', __name__ )




@football_blueprint.route('/liverpool/')
def liverpool():
    title = 'Liverpool YNWA'

    connection = httplib.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'ea0299f31f154fcaa9ea2eb42a1c6612', 'X-Response-Control': 'minified'}
    connection.request('GET', '/v1/teams/64/players/', None, headers)
    responce = json.loads(connection.getresponse().read().decode('utf-8'))

    players = pd.DataFrame.from_dict(responce['players'])
    names = players.name


    def team_atendance(team_id):
        global Team
        global Full
        cur, conn = mysql_connect('football_15_16')
        cur.execute(('SELECT Team, Full FROM attendance_epl_s15 WHERE id=%d') % team_id)
        for (Team, Full) in cur:
            return Team, Full


    team_atendance(5)
    team = Team
    full = Full


    return render_template('football/en/epl/liverpool/liverpool.html', title = title,
                           names = names, team = team, full = full)


@football_blueprint.route('/coutinho/')
def coutinho():
    title = 'Liverpool YNWA'

    from app.my_func.my_plots import coutinho

    l = coutinho()
    script, div = components(l)

    return render_template('football/en/epl/liverpool/coutinho.html',
                           title = title, script = script, div = div)