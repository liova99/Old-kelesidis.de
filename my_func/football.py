import pandas as pd
from flask import url_for

def coutinhno():
    df = pd.read_pickle( '../static/data/liverpool/liv_players.pkl')
    print (df.head())

coutinhno()
