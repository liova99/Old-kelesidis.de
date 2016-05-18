# -*- coding: utf-8 -*-

import pandas as pd
import pandas.io.data as web
import datetime
import pygal
from bokeh.charts import Line
from bokeh.models import HoverTool
from bokeh.plotting import figure
from bokeh.models.sources import ColumnDataSource as cds
#import the different color background
from bokeh.models import BoxAnnotation as ba

from flask import request

# Add the data here

sample = pd.read_table('http://128.199.61.9/static/data/sample.txt')

###############################################

######## Charts #############

def PygalLine():

    line_chart = pygal.Line(width=600, height=450)
    line_chart.title = 'Pygal Line Chart'
    line_chart.x_labels = map(str, range(1880, 1887))
    ys = [i for i in sample.columns[1:]]

    # make a for loop to create all the lines
    for month in ys:
        line_chart.add(month, sample[month].tolist())

    return line_chart

def HLevelLine():
    # sample = pd.read_table('http://128.199.61.9/static/data/sample.txt')

    # Use the Sample Data

    # Make a list with the months
    ys = [month for month in sample.columns[1:]]

    TOOLS = 'pan,wheel_zoom,hover,crosshair,resize,reset'
    TOOLTIPS = [("Year", "$~x"),
                ("Temp", "$y")]

    #make our line configurations
    #import from df, x= the Year column, y = the ys list we created above
    p = Line(sample, x='Year', y=ys, title="Hight Level Bokeh Line Chart", legend="bottom_left",
             ylabel='Temp',  tools=TOOLS ,width=600, height=450, responsive = True)


    #hover tool configuration
    p_hover = p.select(HoverTool)
    p_hover.tooltips = TOOLTIPS

    p.logo = None

    return p

###### END Charts ###########

############ finance ################

#import companies names for finance()
def table_companies():
    # import companies, set and sort index, use only needed colums
    companies = pd.read_csv('http://128.199.61.9/static/data/companies.csv')
    companies = companies.set_index(['Symbol'])
    companies = companies.sort_index()
    companies = companies[['Name', 'IPOyear', 'Sector', 'Industry']]
    return companies

#import info table for finance()
def info():
    if request.method == "POST":
        # 'chart' is the name of <input> tag in html file
        inf = request.form.get('chart')
    else:
        inf = 'CRME'

    companies = table_companies()
    pd.options.display.max_colwidth = 150
    info = pd.DataFrame(companies.loc[inf])

    return info


def finance():
    chart = 'CRME'

    if request.method == "POST":
        chart = request.form.get('chart')

    start = datetime.datetime(2010, 3, 1)
    end = datetime.datetime(2016, 4, 1)

    # df = web.get_data_yahoo( 'TSLA', start, end, interval='w' )
    df = web.get_data_yahoo(chart, start)

    # convert the dates for the hover tool
    dates = pd.Series(df.index)

    dates = dates.dt.strftime('%d-%m-%Y').tolist()

    # Hover tools configuration,
    # Make a list of strings for every value(the hover tool accepts only str)
    # open_p and close the _p is beqause open and close is  funcs in python
    open_p = [str(i) for i in df.Open]
    high = [str(i) for i in df.High]
    low = [str(i) for i in df.Low]
    close_p = [str(i) for i in df.Close]
    vol = [str(i) for i in df.Volume]
    adj = [str(i) for i in df['Adj Close']]


    TOOLS = 'pan,wheel_zoom,box_zoom,hover,crosshair,resize,reset'

    source1 = cds({"Date": dates, "Open": open_p, "High": high,
                                "Low": low, "Close": close_p, "Volume": vol, "Adj": adj})

    source2 = cds({"Date": dates, "Open": open_p, "High": high,
                                "Low": low, "Close": close_p, "Volume": vol, "Adj": adj})


    TOOLTIPS = [("Date", "@Date"), ("Open", "@Open"), ("High", "@High"),
                ("Low", "@Low"), ("Close", "@Close"), ("Volume", "@Volume"), ("Adj Close*", "@Adj")]


    # Make the figure configuration
    f = figure(height=270, x_axis_type="datetime", tools=TOOLS, responsive = True)

    #Add title and label
    f.title = 'Historical Prices for ' + chart+ " from 1.03.2010 until yesterday"
    f.xaxis.axis_label = 'Date'
    f.yaxis.axis_label = 'Open Prices'

    #make line and circle plots
    f.line(df.index, df.Open, source=source2, color='blue')
    f.circle(df.index, df.Open, source=source1, color='navy', size=0.5, alpha=0.8)

    # other hover tool conf
    p_hover = f.select(HoverTool)
    p_hover.tooltips = TOOLTIPS


    return f

########## END Finance ##############


######## Liverpool ################

#/notebooks/Liverpool/coutinho_beter_import_v0.3.ipynb

def coutinho():

    # read the csv, #Add columns name, delede 2 unnamed colums, parse dates,
    # set index, dayfirst True because pandas can read the 5.1.16 as 1.5.16
    df = pd.read_excel('http://128.199.61.9/static/data/liverpool/coutinho.xlsx',
                       names=['Com', 'Date', 'HT', 'Score', 'AT', 'NaN', 'NaN', 'Min', 'Rating'])
    df.Date = pd.to_datetime(df.Date, dayfirst=True)

    df = df.drop('NaN', 1)
    df = df.set_index('Date')

    # Combine HT,Score,AT columns:
    # make a new column Game and assign the HT,Score,AT columns values,
    # new clm Name. The ' ' is for space, and the map func make the int to str
    df['Game'] = df.HT + ' ' + df.Score.map(str) + ' ' + df.AT

    # delete not needed columns
    df = df.drop(['HT', 'Score', 'AT'], axis=1)

    # change the columns order
    df = df[['Com', 'Game', 'Min', 'Rating']]

    # Because in some games there is no player Rating, we must to separate the data,
    # so we will make 2 df, "df_cp" for the complete line in plot and
    # "df_na" for the "Rating Not Available" line in our plot

    df_cp = df[df.Rating.notnull()]
    df_na = df[df.Rating.isnull()]

    # i will fill N/A with 4.7, because othervise the plot will have from 0-6 empty place
    df_na = df_na.fillna(4.7)

    ###### Hover tool Base config #####

    #Now our data is ready, next step is to prepare the data for the Hover Tool

    #the dates: convert to series, change format to ( '%d-%m-%y' ) and ad the data to a list,
    #so we will make 2 list, dates_cp and dates_na one for each df (df_cp & df_na)
    dates_cp = pd.Series(df_cp.index)
    dates_cp = dates_cp.dt.strftime('%d-%m-%y').tolist()

    dates_na = pd.Series(df_na.index)
    dates_na = dates_na.dt.strftime('%d-%m-%y').tolist()

    #Now we will make list for the other data.( hover tool works better with strings)

    # make lists for hover tool with rating,
    compe_cp = [i for i in df_cp.Com]
    game_cp = [i for i in df_cp.Game]
    min_cp = [i for i in df_cp.Min]

    # make list for hover tool N/A
    compe_na = [i for i in df_na.Com]
    game_na = [i for i in df_na.Game]
    min_na = [i for i in df_na.Min]
    rating_na = ['Rating N/A' for i in range(len(df_na))]
    # !! Wall time: 500 µs !! #

    # define 2 func for each of our df's to loop throught the competitions and make a list with links to the
    # photos for every competition with the correct order.

    #http://128.199.61.9/static/img/Liverpool_competition_ico/

    def photo_links_cp():
        epl = 'http://128.199.61.9/static/img/Liverpool_competition_ico/epl.png'
        iuc = 'http://128.199.61.9/static/img/Liverpool_competition_ico/iuc.png'
        links = []
        for i in df_cp.Com:
            if i == 'EPL':
                links.append(epl)
            elif i == 'IUC':
                links.append(iuc)
            else:
                print ('you miss something')#for debug
        return links
    img_cp = photo_links_cp()

    def photo_links_na():
        links = []
        epl = 'http://128.199.61.9/static/img/Liverpool_competition_ico/epl.png'
        iuc = 'http://128.199.61.9/static/img/Liverpool_competition_ico/iuc.png'
        int_fri = 'http://128.199.61.9/static/img/Liverpool_competition_ico/fifa.jpg'
        ecc = 'http://128.199.61.9/static/img/Liverpool_competition_ico/ecc.jpg'
        efc = 'http://128.199.61.9/static/img/Liverpool_competition_ico/fa.png'
        for i in df_na.Com:
            if i == 'EPL':
                links.append(epl)
            elif i == 'IUC':
                links.append(iuc)
            elif i == 'IF':
                links.append(int_fri)
            elif i == 'ECC':
                links.append(ecc)
            elif i == 'EFC':
                links.append(efc)
        return links
    img_na = photo_links_na()

    #tools that we add to our plot:

    TOOLS = 'pan,wheel_zoom,hover,crosshair,resize,reset'

    #Create the ColumnDataSource's for each df and eventually for each line plot
    source_cp = cds(
        {"Date": dates_cp, 'Comp': compe_cp, 'Game': game_cp, 'Min': min_cp, 'Rating': df_cp.Rating, 'Img': img_cp})

    source_na = cds(
        {"Date": dates_na, 'Comp': compe_na, 'Game': game_na, 'Min': min_na, 'Rating': rating_na, 'Img': img_na})

    # To add img to Hover Tool, we can add custom html to the ToolTips

    TOOLTIPS = """
            <div >

                <div >
                    <span style="font-size: 15px; ">Date: </span>
                    <span style="font-size: 15px; ">@Date</span> <br>
                    <span style="font-size: 15px;  ">Game: </span>
                    <span style="font-size: 15px;">@Game </span><br>
                    <span style="font-size: 15px;  ">Minutes Played: </span>
                    <span style="font-size: 15px;">@Min </span><br>
                    <span style="font-size: 15px;  ">Rating: </span>
                    <span style="font-size: 15px;">@Rating </span>
                </div>

                    <div>
                        <img
                            src="@Img" height="64" alt="@Img" width="64"
                            style="float: right; margin: none; position:releative"
                            border="2">
                        </img>
                    </div>

            </div>
        """

    ###### Hover tool Base config END #####

    #######   Chart   ###########

    #make figure,( the tools links to the TOOLS we create earlier, as the source with source_cp / _na )
    #responsive = True, make the plot to be responsive in web pages, when minimize maximize etc.
    p_lfc = figure(x_axis_type='datetime', width=800, height=450, tools=TOOLS, responsive = True)

    # df_cp line
    p_lfc.line(df_cp.index, df_cp.Rating, color='DodgerBlue', source=source_cp)
    p_lfc.circle(df_cp.index, df_cp.Rating, size=5, color='DodgerBlue', source=source_cp)

    # df_na line
    p_lfc.line(df_na.index, df_na.Rating, color='red', legend='Rating N/A', line_dash=[5, 5], source=source_na)
    p_lfc.circle(df_na.index, df_na.Rating, size=7, color='red', legend='Rating N/A', source=source_na)

    # Fill the chart background with different colors with the BoxAnnotation

    high_box = ba(plot=p_lfc, bottom=7.49, fill_alpha=0.1, fill_color='#00ff00')
    mid_box = ba(plot=p_lfc, bottom=6.49, fill_alpha=0.1, top=7.49, fill_color='yellow')
    low_box = ba(plot=p_lfc, top=6.49, fill_alpha=0.1, fill_color='red')

    p_lfc.renderers.extend([high_box, mid_box, low_box])

    # If we want we can configure the legend like this:
    # p.legend.location = (40,150) #x,y pixels from botom left corner of screen!
    p_lfc.legend.location = "top_left"

    #Last Hover Tool Configs.( uncomment p_hover.mode to change hover mode ;) )
    hover_lfc = p_lfc.select(HoverTool)
    # p_hover.mode = 'vline'
    hover_lfc.tooltips = TOOLTIPS

    return p_lfc

####### END Liverpool #################




























