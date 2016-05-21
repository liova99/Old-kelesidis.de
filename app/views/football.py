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

    from ..api.football_data_org import players_api

    players = players_api(64)
    names = players.name


    def team_atendance(team_id):
        global Team
        global Full
        cur, conn = mysql_connect('football_15_16')
        cur.execute(('SELECT Team, Full FROM attendance_epl_s15 WHERE id=%d') % team_id)
        cur.close()
        conn.close()
        for (Team, Full) in cur:
            return Team, Full


    team, full = team_atendance(5)

    # team_atendance(5)
    # team = Team
    # full = Full
    photo = ""

    return render_template('football/en/epl/liverpool/liverpool.html', title = title,
                           names = names, team = team, full = full, photo = photo)


@football_blueprint.route('/coutinho/')
def coutinho():
    title = 'Liverpool YNWA'

    from app.my_func.my_plots import coutinho

    l = coutinho()
    script, div = components(l)

    return render_template('football/en/epl/liverpool/coutinho.html',
                           title = title, script = script, div = div)