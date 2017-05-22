import pandas as pd
import json
import httplib


def players_api(team_id):
    connection = httplib.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': 'ea0299f31f154fcaa9ea2eb42a1c6612', 'X-Response-Control': 'minified'}
    connection.request('GET', '/v1/teams/'+str(team_id)+'/players/', None, headers)
    responce = json.loads(connection.getresponse().read().decode('utf-8'))
    players = pd.DataFrame.from_dict(responce['players'])
    return players
