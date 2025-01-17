#!/usr/bin/env python
# coding: utf-8

# In[190]:


#!/usr/bin/env python
# coding: utf-8

import string
import re

import datetime
import numpy as np
import pandas as pd
import json
import dash_bio as dashbio
import dash_table
from dash import no_update
from dash.dependencies import Input, Output, ALL, State
import dash_html_components as html
import dash_core_components as dcc
from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc

import plotly.express as px
import dash
import plotly.graph_objects as go
import plotly.tools as tls

from collections import Counter


# In[66]:




# In[3]:


with open("Neighborhoods.geojson") as f:
    neigh_geojson = json.load(f)
    
with open("Police_Districts.geojson") as f1:
    dist_geojson = json.load(f1)


df=pd.read_pickle('cleaned_df.pickle')


neig=pd.read_pickle('neis.pickle')
dist=pd.read_pickle('dist.pickle')

subdf=df[(df.Year>=2014)&(df.Year)<=2020]

def intro():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H3("Baltimore Crime Data Analysis"),
            intro_tabone(),
            intro_tabtwo()
#             dcc.Tabs(id='tabs-example', value='tab-1', children=[
#                 dcc.Tab(label='Introduction', value='tab-1'),
#                 dcc.Tab(label='Control Board', value='tab-2')]),
#             html.Div(id='tabs-example-content'),
            #             html.H3("Welcome to the Clinical Analytics Dashboard"),
            #                 html.Blockquote(
            #                     id="intro",
            #                     children=["Rejection hurts. Yes but yet, I've met nobody who has not been rejected.\
            #                     It is a part of life and instead of drowning in the sorrow and somberness of being rejected, we can make it fun and try to try to analyze it.",
            #                             ]
            #                 ),
#             html.Div(children=[
#                      'This is the Dashboard analyzing the time-sapce pattern of the crime data in Baltimore for the job talk of Research Data Scientist.']),
#             html.Br(),
#             html.H4('Instructions'),
#             html.Div(children=[
#                 html.P("This dashboard enables multiple ways for you to interact with the plots. Every plot can be zoomed and selected, along with hovering tooltips. Despite these basics, it also supports the following interactions:"),
#                 html.Li(
#                     'Subsetting the dataset by selecting the time range, the weekdays, and the hours.'),
#                 html.Li(
#                     'Showing specific data entries by clicking on the Heatmap.'),
#                 html.Div('Other interaction options are detailed in the corresponding part')])
            #                 html.Li(
            #                     'Change the Solver of the Temporal Process and the number of days to prdict.'),
            #                 html.Li('Change the metric to rank the important terms, and the number of topics to model.')])
        ]
    )


# In[229]:


def intro_tabone():
    return html.Div(children=[
         html.Blockquote(children=["This dashboard is the visual deliverale for the job talk of the Research Data Scientist at \
         National Police Foundation.",'This web application is handcrafted by ',
                                html.A("Yukun", href='#contact_info')]),
        html.Br(),
            html.H4('Instructions'),
            html.Div(children=[
                html.P("Every plot can be zoomed and selected, along with hovering tooltips. Despite these basics, each\
                section will have its own interactions. \
                Despite these basics, it also supports other kinds of user inputs and interactions. Pleaase put your mouse on the ",style={"display":"inline"}),
                        html.I(className="fas fa-question-circle fa-lg", style={"display":"inline"}),
                html.P(' icon aside the title of each section to get more information. For this section, I render a way to find the space-time pattern of crimes.',style={"display":"inline"}),
                 html.Li(
                        'Adding spatial or temporal features into the pattern mining below'),
                    html.Li('Showing the map at specific time by changing the values of the sliders'),
                html.Li('Clicking on the tiles in the parallel cord plot to automatically change the silder and the map')
            ])

        
        
    ])

# def intro_tabtwo():
#     return html.Div(children=[
#         html.Div('In this tab. I will illustrate how to use this visualization tool.')
        
#     ])


# In[ ]:





# In[208]:


def intro_tabtwo():
    return html.Div(
        id="control-card",
        children=[

            html.Div(children=[

                html.Div(className='columns', children=[html.Strong("Select Granularity of Spatial Attributes"),
                                                              dcc.Checklist(
                    id='space_grand',
                    options=[
                        {'label': 'District', 'value': 'New_District'},
                        {'label': 'Neighborhood', 'value': 'Neighborhood_New'},
                        {'label': 'Street', 'value': 'Location'}
                    ],
                    value=['Neighborhood_New']
                ),
                    html.Br(),
                    html.Strong("Select Granularity of Temporal Attributes"),
                    dcc.Dropdown(
                    id='time_grand',
                    options=[
                        {'label': 'Month', 'value': 'month'},
                        {'label': 'Day', 'value': 'day'},
                        {'label': 'Day of Week', 'value': 'dayofweek'},
                        {'label': 'Weekday or Weekend',
                         'value': 'weekday'},
                        {'label': 'Hour', 'value': 'hour'},
#                         {'label': 'Minute', 'value': 'minute'},
                        {'label': 'Time of Day', 'value': 'period'},
                        {'label':'Quarter','value':'quarter'}

                    ],
                    value=['month', 'dayofweek', 'period'],
                    multi=True
                ),
                    html.Br(),
                    html.Strong("Select the Type of Crime(s)"),
                    dcc.Dropdown(
                    id='crime_type',
                    options=[{'label':i.title(),'value':i}for i in df.Description.unique()],
                    value=['SHOOTING'],
                    multi=True
                )])


            ])

        ]
    )


# In[17]:


def year_slider():
    return html.Div(children=[
                html.Strong("Select the Time Range for Analysis"),
                html.Div(style={"width": "100%", "height": "100%",
                         "display": "inline-block", "position": "relative"},
        className='columns', children=[dcc.RangeSlider(
                    id='year_slider',
                    updatemode='mouseup',  # don't let it update till mouse released
                    min=1963,
                    max=2020,
                    step=None,
                    marks={2016: {'label':'2016',"style": {"transform": "rotate(45deg)"}},
                           2018:  {'label':'2018',"style": {"transform": "rotate(45deg)"}},
                           2020:  {'label':'2020',"style": {"transform": "rotate(45deg)"}},
                           2015:  {'label':'2015',"style": {"transform": "rotate(45deg)"}},
                           2017:  {'label':'2017',"style": {"transform": "rotate(45deg)"}},
                           2019:  {'label':'2019',"style": {"transform": "rotate(45deg)"}},
                           2014:  {'label':'2014',"style": {"transform": "rotate(45deg)"}},
                           2011:  {'label':'2011',"style": {"transform": "rotate(45deg)"}},
                           2009:  {'label':'2009',"style": {"transform": "rotate(45deg)"}},
                           1975:  {'label':'1975',"style": {"transform": "rotate(45deg)"}},
                           2012:  {'label':'2012',"style": {"transform": "rotate(45deg)"}},
                           2013:  {'label':'2013',"style": {"transform": "rotate(45deg)"}},
                           1980:  {'label':'1980',"style": {"transform": "rotate(45deg)"}},
                           1973:  {'label':'1973',"style": {"transform": "rotate(45deg)"}},
                           2008:  {'label':'2008',"style": {"transform": "rotate(45deg)"}},
                           1978:  {'label':'1978',"style": {"transform": "rotate(45deg)"}},
                           1988:  {'label':'1988',"style": {"transform": "rotate(45deg)"}},
                           1977:  {'label':'1977',"style": {"transform": "rotate(45deg)"}},
                           1995:  {'label':'1995',"style": {"transform": "rotate(45deg)"}},
                           2001:  {'label':'2001',"style": {"transform": "rotate(45deg)"}},
                           2000:  {'label':'2000',"style": {"transform": "rotate(45deg)"}},
                           2007:  {'label':'2007',"style": {"transform": "rotate(45deg)"}},
                           1969:  {'label':'1969',"style": {"transform": "rotate(45deg)"}},
                           1982:  {'label':'1982',"style": {"transform": "rotate(45deg)"}},
                           1963:  {'label':'1963',"style": {"transform": "rotate(45deg)"}},
                           1981: {'label': '1981',"style": {"transform": "rotate(45deg)"}},
                           1999: {'label': '1999',"style": {"transform": "rotate(45deg)"}},
                           2003:  {'label':'2003',"style": {"transform": "rotate(45deg)"}},
                           2010:  {'label':'2010',"style": {"transform": "rotate(45deg)"}},
                           2004:  {'label':'2004',"style": {"transform": "rotate(45deg)"}},
                           1998:  {'label':'1998',"style": {"transform": "rotate(45deg)"}},
                           1993:  {'label':'1993',"style": {"transform": "rotate(45deg)"}},
                           1985: {'label': '1985',"style": {"transform": "rotate(45deg)"}},
                           2006:  {'label':'2006',"style": {"transform": "rotate(45deg)"}}},
                    value=[2014, 2020],
#                     vertical=True,
#                     verticalHeight=600
                )])])


# In[18]:


slider_map={'{"index":1,"type":"slider"}':'Month',
'{"index":2,"type":"slider"}':'Day',
'{"index":3,"type":"slider"}':'DayofWeek',
'{"index":4,"type":"slider"}':'WeekDay',
'{"index":5,"type":"slider"}':'Quarter',
'{"index":6,"type":"slider"}':'Hour',
'{"index":7,"type":"slider"}':'Period'}

# {"index":1,"type":"slider"}


# In[19]:


def make_sliders(time):
    sliders = []
    for t in time:
        if t == 'month':
            sliders.append(dcc.Slider(
                id={'type':'slider','index':1},
                updatemode='mouseup',  # don't let it update till mouse released
                min=1,
                max=12,
                marks={1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                       7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'},
                step=1,
                value=1
            ))
        elif t == 'day':
            sliders.append(dcc.Slider(
                id={'type':'slider','index':2},
                updatemode='mouseup',  # don't let it update till mouse released
                min=1,
                max=31,
                marks={i: str(i) for i in range(1, 32)},
                step=1,
                value=1
            ))
        elif t == 'dayofweek':
            sliders.append(dcc.Slider(
                id={'type':'slider','index':3},
                updatemode='mouseup',  # don't let it update till mouse released
                min=0,
                max=6,
                marks={0: "Monday", 1: 'Tue', 2: 'Wed',
                       3: 'Thur', 4: 'Fri', 5: 'Sat', 6: 'Sun'},
                step=1,
                value=0
            ))
        elif t == 'weekday':
            sliders.append(dcc.Slider(
                id={'type':'slider','index':4},
                updatemode='mouseup',  # don't let it update till mouse released
                min=1,
                max=2,
                marks={1: 'Weekdays', 2: 'Weekends'},
                step=1,
                value=1
            ))
        elif t == 'quarter':
            sliders.append(dcc.Slider(
                id={'type':'slider','index':5},
                updatemode='mouseup',  # don't let it update till mouse released
                min=1,
                max=4,
                marks={1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'},
                step=1,
                value=1
            ))
        elif t == 'hour':
            sliders.append(dcc.Slider(
                id={'type':'slider','index':6},
                updatemode='mouseup',  # don't let it update till mouse released
                min=0,
                max=23,
                marks={0: '12 AM', 1: '1 AM', 2: '2 AM', 3: '3 AM', 4: '4 AM', 5: '5 AM', 6: '6 AM', 7: '7 AM',
                       8: '8 AM', 9: '9 AM', 10: '10 AM', 11: '11 AM', 12: '12 PM', 13: '1 PM', 14: '2 PM', 15: '3 PM',
                       16: '4 PM', 17: '5 PM', 18: '6 PM', 19: '7 PM', 20: '8 PM', 21: '9 PM', 22: '10 PM', 23: '11 PM'},
                step=1,
                value=1
            ))
        elif t == 'period':
            sliders.append(dcc.Slider(
                id={'type':'slider','index':7},
                updatemode='mouseup',  # don't let it update till mouse released
                min=1,
                max=6,
                marks={1: 'Late Night',
                       2: 'Early Morning',
                       3: 'Morning',
                       4: 'Noon',
                       5: 'Evening',
                       6: 'Night'},
                step=1,
                value=1
            ))
    return sliders


# In[235]:


def para_html():
    return html.Div(id='para', className="columns pretty_container", children=[
        html.Div(style={"display": "inline-flex"}, children=[html.H5('Parallel Coordinates of the Crime Acticity'),
                                                             html.Div(children=[
                                                                 html.I(
                                                                     className="fas fa-question-circle fa-lg", id="target"),
                                                                 dbc.Tooltip("How do we read this? Bascially, each ploly line represents a combination of space-time patterns, and the color indicates the frequency of this pattern.\
                                Each variable in the data set is represented by a column of rectangles, \
                                where each rectangle corresponds to a discrete value taken on by that variable.\
                                     The relative heights of the rectangles reflect the relative\
                                          frequency of occurrence of the corresponding value. ", target="target",
                                                                             style={"max-width": "400px", "padding": ".25rem .5rem", "color": "#fff", "text-align": "center", "background-color": "#000", "border-radius": ".25rem"}),
                                                             ],
                    className="p-5 text-muted"
                    )
                                                            ]),

        html.Div("This plot is automatically generated based on the spaial/temporal features you selected to add.\
                        Each tile is the most frequent space-time pattern of crime activities. You can change the number\
                        below to show the patterns that is more frequent than X% of other patterns, a.k.a. the top (100-X)% pattern." ,
                 style={'margin': "10px"}),
        html.Div(children=[
            html.Strong('Please select the quantile number here:'),
            html.Br(),
                    html.Div(dcc.Input(
            id="dtrue", type="number",
            debounce=True, placeholder="Debounce True",value=98
        ))
        ], style={'text-align': 'center'})
,
        html.Div(id='quant', children=[], style={'display':'None'}),
        html.Br(style={'margin':'10px'}),
        dcc.Loading(dcc.Graph(id='paco'))])


# In[22]:


def subset_df(crime, space, year, time):
    
    #filter crime
    new_df=df[df.Description.isin(crime)]
    
    #filter year
    new_df=new_df[(new_df.Year>=year[0])&(new_df.Year<=year[-1])]
    
    grouping_attr=space+list(time.keys())
    
    grouping_attr.extend(['Description','Total Incidents'])  
    
    print(grouping_attr)
    subdf=new_df.loc[:,grouping_attr]
    
    return subdf


def make_paco(df, quant):
    col=list(df.columns)
    col.remove('Total Incidents')
    col_group=col
    
    newdf=df.groupby(col_group).count().reset_index().sort_values('Total Incidents')
    
    num=newdf['Total Incidents'].quantile(quant)
    
    newdf=newdf[newdf['Total Incidents']>num]
    
    fig=px.parallel_categories(newdf, dimensions=col, color='Total Incidents')
    
    return fig, fig.data[0]['dimensions']
    
    
    


# In[230]:


def pattern_html():
    return html.Div(id='', className='columns pretty_container', children=[
        html.Div(style={"display": "inline-flex"}, children=[
            html.H5("Maximal Frequent Pattern Mining",
                    style={'margin-left': '10px'}),
            html.Div(children=[
                html.I(
                    className="fas fa-question-circle fa-lg", id="target2"),
                dbc.Tooltip("How can we interact with this? 1) Filter the size of the pattern--Larger pattern will include more dimensions; \n 2)\
                                Selecting how many patterns you want to see in the bar chart below;\n.", target="target2",
                            style={"max-width": "400px", "padding": ".25rem .5rem", "color": "#fff", "text-align": "center", "background-color": "#000", "border-radius": ".25rem"}),
            ],
                className="p-5 text-muted"
            )]),

        html.P(
            children="An frequent itemset/pattern is defined as a set of attributes whose support is greater than or equal to a Minimum Support threshold. \
            Support is the frequency of occurrence of an itemset. Here I used the FPMax algorithm to generate the patterns.\
                    The support threshold is 0.001. The maximal size of the pattern is set as 6.",
            style={'margin': '10px'}
        ),
        html.Div(
            id="select model",
            style={"text-align": "center"},
            className="six columns", children=[html.Strong('Filter the Patterns'),
                                               dcc.Checklist(
                id='len_picker',
                options=[
                    {'label': 'Two',
                     'value': 2},
                    {'label': 'Three',
                     'value': 3},
                    {'label': 'Four',
                     'value': 4},
                    {'label': 'Five',
                     'value': 5},
                    {'label': 'Six',
                     'value': 6},
                ],
                value=[2,3,4,5,6],
                labelStyle={'display': 'inline-block'}
            )

            ]),
        html.Div(
            id="select_bum",
            style={"text-align": "center"},
            className="six columns", children=[html.Strong('Select Number of Patterns to Show'),
                                               dcc.Slider(
                id='numslider',
                min=1,
                max=100,
                step=1,
                value=15,
                updatemode='drag'
            )
            ]),
        html.Br(),
        html.Br(),
        html.Div(className='columns', children=dcc.Loading(
            dcc.Graph(id='pattern_bar'))
        )


    ]
    )


# In[212]:


from mlxtend.frequent_patterns import fpmax

def pattern(df, crime):
    
    if len(crime)==1:
        df=df.drop(columns=['Total Incidents','Description'])
        rules=fpmax(pd.get_dummies(df.astype('category')), min_support=0.001, max_len=6,use_colnames=True)
    else:
        df=df.drop(columns=['Total Incidents'])
        rules=fpmax(pd.get_dummies(df.astype('category')), min_support=0.001, max_len=6,use_colnames=True)
    
    rules['len']=rules.itemsets.apply(len)
    rules['itemsets']=rules.itemsets.apply(list)
#     rules.sort_values('support', ascending=False)
    rules=rules.sort_values('support', ascending=False).reset_index()
    
    return rules


# In[213]:


def filter_df(newdf,times):
#     print(times)
#     print(newdf)
    for t in times.items():
        if t[0]=='Weekday':
            real_val={1:'Weekday',2:'Weekend'}[t[1]]
            newdf=newdf[newdf[t[0]]==real_val]
        elif t[0]=='Period':
            real_val={1: 'Late Night',
                       2: 'Early Morning',
                       3: 'Morning',
                       4: 'Noon',
                       5: 'Evening',
                       6: 'Night'}[t[1]]
            newdf=newdf[newdf[t[0]]==real_val]
            
        else:
            newdf=newdf[newdf[t[0]]==t[1]]
#             print(newdf)
    return newdf
    


# In[255]:


def season_html():
    return html.Div(id='season', className='columns pretty_container',children=[
        html.Div(style={"display": "inline-flex"}, children=[
            html.H5("Detecting Seasonality",
                    style={'margin-left': '10px'}),
            html.Div(children=[
                html.I(
                    className="fas fa-question-circle fa-lg",id="target3"),
                dbc.Tooltip("How can we interact with this? 1) Selecting the tab by changing the seasonality detection approcah; \n 2)\
                                Selecting the time interval of the input data;\n 3)\
                                    Selecting the type of crime to model.", target="target3",
                            style={"max-width": "400px", "padding": ".25rem .5rem", "color": "#fff", "text-align": "center", "background-color": "#000", "border-radius": ".25rem"}),
            ],
                className="p-5 text-muted"
            )]),

        html.P("I have explored three ways to find and test the seasonality of a data. \
        Fourier transform as a way to explore all possible seasonalities Seasonal ARIMA to model one seasonality in the data \
            In addtion, I also presented modelling multiple seasonalites in the data using Facebook's Prophet.",
            style={'margin': '10px'}
        ),
        html.Div(children=[ 
            dcc.Tabs(id='stabsexample', value='stab1', children=[
                dcc.Tab(label='Fourier', value='stab1'),
                dcc.Tab(label='SARIMA', value='stab2'),
                 dcc.Tab(label='Prophet by Faebook', value='stab3')]),
        html.Div(id='stabcontent')])

        
    ]
    ) 


# In[256]:


def stab1():
    return html.Div(children=[
        html.Div(children=[
            html.Strong('Please select the type of crime to model'),
            dcc.Dropdown(
            id='scrime',
            options=[{'label': i.title(), 'value': i}
                     for i in df.Description.unique()],
            value='SHOOTING'
        )], style={'text-align': 'center'},
                className='six columns')
        
        ,
        
        html.Div(children=[
            html.Strong('Please select the type of time series to generate'),
            dcc.RadioItems(
            options=[
                {'label': 'Construct Hourly Time Series', 'value': 'hourly'},
                {'label': 'Construct Daily Time Series', 'value': 'daily'},
                {'label': 'Construct Monthly Time Series', 'value': 'monthly'}
            ],
            value='hourly',
                id='speriod'
        )
        
        ], style={'text-align': 'center'},
                className='six columns'),


        html.Div(className='six columns', children=[
                 dcc.Loading(dcc.Graph(id='stab1_line'))]),
        html.Div(className='six columns',id='stab1_df', children=[
        html.H4('Prominent Frequncies',style={'text-align': 'center'}),
        dash_table.DataTable(
                id='stab1_table',page_size= 15)])



    ])


# In[249]:


def ftt_result(crime, period):
    
    # sdf=df[(df.Year>=2014)&(df.Year)<=2020]
    
    sdf=subdf[subdf.Description==crime]
    
    if period=='hourly':
        
        signal=sdf.resample('H', on='Datetime').sum()['Total Incidents']
        fft_outputft, power, freq, peaks, peak_freq, peak_power= get_fftt(signal)
        
        output = pd.DataFrame()
        output['index'] = peaks
        output['freq (1/hour)'] = peak_freq
        output['amplitude'] = peak_power
        output['period (hour)'] = 1 / peak_freq
#         output['fft'] = fft_output[peaks]
        output['peak']='peak'
        output = output.sort_values('amplitude', ascending=False)
        
        fft_df=pd.DataFrame()
        fft_df['freq']=freq
        fft_df['power']=power

        f=px.line(fft_df, x='freq',y='power', title='All Frequencies and Their Amplitute')
        f.add_trace(px.scatter(output, x='freq (1/hour)', y='amplitude', color='peak',template='ggplot2').data[0])
        f.update_layout(margin={"l":0,"b":0},legend=dict(
            orientation="h"))

 

    elif period=='daily':
        
        signal=sdf.resample('D', on='Datetime').sum()['Total Incidents']
        fft_outputft, power, freq, peaks, peak_freq, peak_power= get_fftt(signal)
        
        output = pd.DataFrame()
        output['index'] = peaks
        output['freq (1/day)'] = peak_freq
        output['amplitude'] = peak_power
        output['period (day)'] = 1 / peak_freq
#         output['fft'] = fft_output[peaks]
        output['peak']='peak'
        output = output.sort_values('amplitude', ascending=False)
                
        fft_df=pd.DataFrame()
        fft_df['freq']=freq
        fft_df['power']=power

        f=px.line(fft_df, x='freq',y='power', title='All Frequencies and Their Amplitute')
        f.add_trace(px.scatter(output, x='freq (1/day)', y='amplitude', color='peak',template='ggplot2').data[0])
        f.update_layout(margin={"l":0,"b":0},legend=dict(
            orientation="h"))


        
    else:
        signal=sdf.resample('M', on='Datetime').sum()['Total Incidents']
        fft_outputft, power, freq, peaks, peak_freq, peak_power= get_fftt(signal)        
        
        output = pd.DataFrame()
        output['index'] = peaks
        output['freq (1/month)'] = peak_freq
        output['amplitude'] = peak_power
        output['period (month)'] = 1 / peak_freq
#         output['fft'] = fft_output[peaks]
        output['peak']='peak'
        output = output.sort_values('amplitude', ascending=False)  
        
        fft_df=pd.DataFrame()
        fft_df['freq']=freq
        fft_df['power']=power

        f=px.line(fft_df, x='freq',y='power', title='All Frequencies and Their Amplitute')
        f.add_trace(px.scatter(output, x='freq (1/month)', y='amplitude', color='peak',template='ggplot2').data[0])
        f.update_layout(margin={"l":0,"b":0},legend=dict(
            orientation="h"))


    
    return f, output


# In[29]:


from scipy import fft
from scipy import signal as sig
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

def get_fftt(signal):
    fft_output = fft.fft(signal)
    power = np.abs(fft_output)
    freq = fft.fftfreq(len(signal))
    
    mask = freq >= 0
    freq = freq[mask]
    power = power[mask]
    
    peaks = sig.find_peaks(power[freq >=0], prominence=200)[0]
# peaks = power[freq >=0]
    peak_freq =  freq[peaks]
    peak_power = power[peaks]
    
    
    return fft_output, power, freq, peaks, peak_freq, peak_power


def sarima_html():
    return html.Div(style={'text-align': 'center'},children=[
        
            html.Div(children=[
            html.Strong('Please select the type of crime to model'),
            dcc.Dropdown(
            id='sacrime',
            options=[{'label': i.title(), 'value': i}
                     for i in df.Description.unique()],
            value='SHOOTING'
        )], style={'text-align': 'center'},
                className='six columns')
        
        ,
        
        html.Div(children=[
            html.Strong('Please select the type of time series to generate'),
            dcc.RadioItems(
            options=[
                {'label': 'Construct Daily Time Series', 'value': 'daily'},
                {'label': 'Construct Monthly Time Series', 'value': 'monthly'},
                {'label': 'Construct Quarterly Time Series', 'value': 'quarterly'}
            ],
            value='quarterly',
                id='saperiod'
        )
        
        ], style={'text-align': 'center'},
                className='six columns'),
        
        html.Div(className='six columns', children=[
            html.Strong('Decomposition of the Time Series'),
                 dcc.Loading(dcc.Graph(id='stab2_decom'))]),
        html.Div(className='six columns', children=[
                     html.Strong('Model Comparison of Seasonal/Non-Seasonal Models'),
        dash_table.DataTable(
                id='stab2_par',page_size= 15)]),
        html.Br(),
        html.Br(),
        html.Div(className='columns', children=[
                     html.Strong('Model Performance on the Testing Set'),
        dcc.Loading(dcc.Graph(id='pred'))]),
        
        html.Div(className='six columns', children=[
                     html.Strong('Seasonal Model Coef.'),
        dash_table.DataTable(
                id='seco',page_size= 15)]),
        html.Div(className='six columns', children=[html.Strong('None-Seasonal Model Coef.'),
        dash_table.DataTable(
            
                id='noseco',page_size= 15)])


    ])


# In[241]:


def sarima_result(crime, period):
    
    sdf=subdf[subdf.Description==crime]
    
    # sdf=df[df.Description==crime]
    
    if period=='monthly':
        signal=sdf.resample('M', on='Datetime').sum()['Total Incidents']
        decom_fig=decom(signal)
        pra_df,se_co,nose_co,result_df=srima_fit(signal,12)
        
    elif period=='daily':
        signal=sdf.resample('D', on='Datetime').sum()['Total Incidents']
        decom_fig=decom(signal)
        pra_df,se_co,nose_co,result_df=srima_fit(signal,365)
    else:
        signal=sdf.resample('Q', on='Datetime').sum()['Total Incidents']
        decom_fig=decom(signal)
        pra_df,se_co,nose_co,result_df=srima_fit(signal,4)
        
    
    return decom_fig, pra_df, se_co, nose_co, result_df
    


# In[33]:


from statsmodels.tsa.seasonal import seasonal_decompose
def decom(signal):
    result = seasonal_decompose(signal)
    fig = result.plot()
    n_fig=tls.mpl_to_plotly(fig)
    
    return n_fig


# In[251]:


import pmdarima as pm
def srima_fit(signal, m):
    
    
    seasonal_model = pm.auto_arima(signal, start_p=1, start_q=1,
                           max_p=3, max_q=3,m=m,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
    
    non_seasonal_model = pm.auto_arima(signal, start_p=1, start_q=1,
                           max_p=3, max_q=3,
                           start_P=0, seasonal=False,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
    
    se_pra=seasonal_model.get_params()
    se_pra['aic']=seasonal_model.aic()
    
    nose_pra=non_seasonal_model.get_params()
    nose_pra['aic']=non_seasonal_model.aic()
    
    pra_df=pd.DataFrame([se_pra,nose_pra])
    
    se_co=pd.read_html(seasonal_model.summary().tables[1].as_html(), header=0, index_col=0)[0]
    nose_co=pd.read_html(non_seasonal_model.summary().tables[1].as_html(), header=0, index_col=0)[0]
    
    
    train=signal[:int(0.8*(len(signal)))]
    test=signal[int(0.8*(len(signal))):]
    
    
    seasonal_model.fit(train)
    se_forecast = seasonal_model.predict(n_periods=len(test))
    
    non_seasonal_model.fit(train)
    nose_forecast = non_seasonal_model.predict(n_periods=len(test))
    
    future_forecast1 = pd.DataFrame(se_forecast,index = test.index,columns=['SesonalPrediction'])
    future_forecast2 = pd.DataFrame(nose_forecast,index = test.index,columns=['NonseaPrediction'])
    
    
    result_df=pd.concat([test,future_forecast1,future_forecast2],axis=1)
    
    return pra_df,se_co.reset_index(),nose_co.reset_index(),result_df


# In[177]:


from prophet import Prophet
def pro(crime,period):
    
    
    # sdf=df[(df.Year>=2014)&(df.Year)<=2020]
    sdf=subdf[subdf.Description==crime]
    # sdf=df[df.Description==crime]
    
    signal=sdf.resample('D', on='Datetime').sum()['Total Incidents']
    
    df=signal.reset_index().rename(columns={'Datetime':'ds','Total Incidents': 'y'})
    
    
    if 'weekly' in period:
    
        m = Prophet(weekly_seasonality=True)
    else:
        m = Prophet(weekly_seasonality=False)
    
    if 'monthly' in period:
        m.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    if 'quarterly' in period:
        m.add_seasonality(name='quarterly', period=91.3125, fourier_order=10)


    m.fit(df)

    future = m.make_future_dataframe(periods=20)
    
    forecast = m.predict(future)
    
    fig = m.plot_components(forecast)
    
    return [tls.mpl_to_plotly(fig)]
    
    


# In[258]:


def pro_html():
     return html.Div(children=[
        html.Div(children=[dcc.Dropdown(
            id='pcrime',
            options=[{'label': i.title(), 'value': i}
                     for i in df.Description.unique()],
            value='SHOOTING'
        ),
            dcc.Dropdown(
            options=[
                {'label': 'Add Daily Seasonality', 'value': 'daily'},
                {'label': 'Add Monthly Seasonality', 'value': 'monthly'},
                {'label': 'Add Quarterly Seasonality', 'value': 'quarterly'}
            ],
            value=['quarterly'],
                id='pperiod',
                multi=True
                
        )]),

        
        html.Div(className='columns', children=[
        dcc.Graph(id='pro')])



    ])


# In[ ]:





# In[263]:


from causalimpact import CausalImpact
import splot
import io
import base64, pickle



def ci(crime, time):
    print(time+'******************************')
    print(pd.to_datetime(time))
    print('---***')
    print(pd.to_datetime(time)==pd.to_datetime('2019/11/20'))

    if ((crime=='SHOOTING') & (pd.to_datetime(time)==pd.to_datetime('2019/11/20'))):
        print('default')


        with open('rep.pkl', 'rb') as f:  # Overwrites any existing file.
            report=pickle.load(f)   
        
        src=app.get_asset_url ('output.png')

        return [report, src]
    
    else:
        sdf=subdf[subdf.Description==crime]
        # sdf=df[(df.Year>=2014)&(df.Year<=2020)&(df.Description==crime)]
        
        signal=sdf.resample('D', on='Datetime').sum()['Total Incidents']
        
        
        post=signal[signal.index>pd.to_datetime(time)]
        pre=signal[signal.index<pd.to_datetime(time)]
        
        ci = CausalImpact(signal, [pre.index[0],pre.index[-1]], [post.index[0],post.index[-1]],nseasons=[{'period': 7}, {'period': 30}])
    
        fig=splot.plot(ci)
        
        report=ci.summary(output='report')
        
        buf = io.BytesIO() # in-memory files
        fig.savefig(buf, format = "png") # save to the above file object
        data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
        plt.close()
    
    
    return [report,"data:image/png;base64,{}".format(data)]
    


# In[264]:


from datetime import datetime as dt
 

def ci_html():
    return html.Div(className='columns pretty_container', children=[
        
                html.Div(style={"display": "inline-flex"}, children=[
            html.H5("Policy Evaluation",
                    style={'margin-left': '10px'}),
            html.Div(children=[
                html.I(
                    className="fas fa-question-circle fa-lg",id="target5"),
                dbc.Tooltip("How can we interact with this? 1) Selecting the type of crime to model; \n 2)\
                                Selecting the policy execution date;.", target="target5",
                            style={"max-width": "400px", "padding": ".25rem .5rem", "color": "#fff", "text-align": "center", "background-color": "#000", "border-radius": ".25rem"}),
            ],
                className="p-5 text-muted"
            )]),

        html.P("In this section, I will present the result of Bayesian structural time series, similar to Interrupted Time Series Analysis. You will see the pre-post intervention plots and a summary report.",
            style={'margin': '10px'}
        ),
        


#                 html.P(
#                     children="A Temporal Process is a kind of random process whose realization consists of discrete events \
#                     localized in time. Compared with \
#                     traditional Time-Seris, each data entry was allocated in different time interval. The scattering nature of receiving\
#                     an email fits better with a Temporal Process Analysis. \n \
#                     A very popular kind of termporal process is the Hawkes process, which could be consider\
#                     as an 'auto-regression' type of process. Here I used the Hawkes Process to simulate the events.\
#                     You can select the Kernal and the days to forecast below.👇",
#                     style={'margin': '10px'}
#                 ),
             html.Div(children=[
                 html.Strong('Select the Type of Crime'),dcc.Dropdown(
            id='cicrime',
            options=[{'label': i.title(), 'value': i}
                     for i in df.Description.unique()],
            value='SHOOTING'
        )],style={'text-align': 'center'},className='six columns'),
        
            html.Div(children=[
                 html.Strong('Select the Date of Policy Execution'),
    dcc.DatePickerSingle(
        id='poli_date',
        min_date_allowed=dt(2014, 1, 1),
        max_date_allowed=dt(2020, 1, 1),
        date=dt(2019, 11, 20)
    )],
                     style={'text-align': 'center'},className='six columns'),

                html.Br(),
                html.Div(className='columns',style={'text-align': 'center'}, children=html.Img(id='static', src='out.png')),
                html.Div(className='columns mini_container',style={'text-align': 'center'}, id='rep',children=[

                    ]
                    )
                               ])


# In[266]:


# %tb
# app = dash.Dash(__name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css",
#                                                     "https://dash-gallery.plotly.host/dash-oil-and-gas/assets/styles.css?m=1590087908.0"])
app = dash.Dash(__name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css",
                                                 "https://dash-gallery.plotly.host/dash-oil-and-gas/assets/styles.css?m=1590087908.0",
                                                "https://use.fontawesome.com/releases/v5.10.2/css/all.css"])
server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    id="app-container",
    children=[html.Div(id="left-column ",
                       style={},
                       className="four columns pretty_container",
                       children=intro()
                       ),
              html.Div(
        id="right-column",
        className="eight columns",
        style={},
        children=[html.Div(
            [
                html.Div(
                    [html.H6(),
                     html.P("No. of Years Selected"),
                     html.Strong(id="years_selected")],
                    id="days",
                    className="mini_container",
                ),
                html.Div(
                    [html.H6(), html.P(
                        "No. of Incidents in the Period"),
                     html.Strong(id="total")],

                    className="mini_container",
                ),
                html.Div(
                    [html.H6(), html.P(
                        "The Dimension You Selected"),
                     html.Strong(id="click_pa")],

                    className="mini_container",
                )
            ],
            id="info-container",
            className="row container-display",
        ),
            year_slider(),
            html.Div(
            className='mini_container',
            children=[
                dcc.Loading(dcc.Graph(id='map'))]),
            html.Div(id='sliders'),
            html.Div(id='test')





        ]),

        para_html(),
        dcc.Store(id='pacodata'),
        dcc.Store(id='clickpaco'),
        html.Div(id='test_click'),
              
        pattern_html(),
        season_html(),
            ci_html(),
        html.Div(id='contact_info', style={'text-align': 'center'}, className='pretty_container twelve columns', children=[
                'Thanks for playing with it! You can contact me via my ',
                html.A(
                    'LinkedIn', href='https://www.linkedin.com/in/yukun-yang-1044ab157/', target="_blank"),
                ', or ',
                html.A('Personal Website',
                    href='http://www.yukunyang.info', target="_blank"),
                '. You can also Email me at ',
                html.A('contact@yukunyang.info',
                    href='mailto:contact@yukunyang.info', target="_blank")
            ])


    ])

    
@app.callback([
    Output('static', 'src'),
              Output('rep', 'children'),

],
              [Input('cicrime', 'value'),
              Input('poli_date', 'date')])

def render_ci(crime, date):
    
    rep,src=ci(crime,date)
    
    
    return [src,rep]

@app.callback(Output('stabcontent', 'children'),
              [Input('stabsexample', 'value')])
def render_content(tab):
#     return tab
    if tab == 'stab1':
        return stab1()
    elif tab=='stab2': 
        return sarima_html()
    else:
        return pro_html()

@app.callback([
    Output('pro', 'figure')
],
              [Input('pcrime', 'value'),
              Input('pperiod', 'value')])

def render_pro(crime, period):
    

    return pro(crime,period)
    
    
    
    
@app.callback([
    Output('stab1_line', 'figure'),
              Output('stab1_table', 'data'),
Output('stab1_table', 'columns')
],
              [Input('scrime', 'value'),
              Input('speriod', 'value')])

def render_ftt(crime, period):
    
    f,t=ftt_result(crime, period)
    
    colums=[{"name": i, "id": i} for i in t.columns]
    data=t.to_dict('records')
    return f,data,colums


@app.callback([
    Output('stab2_decom', 'figure'),
              Output('stab2_par', 'data'),
                Output('stab2_par', 'columns'),
    Output('pred', 'figure'),
                  Output('seco', 'data'),
                Output('seco', 'columns'),
    
                  Output('noseco', 'data'),
                Output('noseco', 'columns'),
],
              [Input('sacrime', 'value'),
              Input('saperiod', 'value')])

def render_sari(crime, period):
    
    decom_fig, pra_df, se_co, nose_co, result_df=sarima_result(crime,period)
    pra_df=pra_df.astype('str')[['order','seasonal_order','aic']]
    pra_dfcolums=[{"name": i, "id": i} for i in pra_df.columns]
    pra_dfdata=pra_df.to_dict('records')
    
    se_cocolums=[{"name": i, "id": i} for i in se_co.columns]
    se_codata=se_co.astype('str').to_dict('records')
    
    nose_cocolums=[{"name": i, "id": i} for i in nose_co.columns]
    nose_codata=nose_co.astype('str').to_dict('records')
    
    fig=px.line(result_df.astype('float'), template='seaborn')
    
#     return decom_fig,pra_dfdata,pra_dfcolums,fig,se_codata,se_cocolums,nose_codata,nose_cocolums
    return decom_fig, pra_dfdata,pra_dfcolums, fig,se_codata,se_cocolums,nose_codata,nose_cocolums



@app.callback(Output("click_pa", 'children'),
              [Input('clickpaco', 'data')])
def change_pattern(clickpaco):
    found = False
    if clickpaco == None:
        return no_update
    return_s=''
    for k, v in clickpaco.items():
        s='{}->{} || '.format(k,v)
        return_s=return_s+s
    return return_s
    if found == False:
        return no_update

@app.callback(Output({"index": 7, "type": "slider"}, 'value'),
              [Input('clickpaco', 'data')])
def change_silder(clickpaco):
    found = False
    if clickpaco == None:
        return no_update
    for k, v in clickpaco.items():
        if k == 'Period':
            return {'Late Night': 1,
                    'Early Morning': 2,
                    'Morning': 3,
                    'Noon': 4,
                    'Evening': 5,
                    'Night': 6}[v]
    if found == False:
        return no_update

@app.callback(Output({"index": 6, "type": "slider"}, 'value'),
              [Input('clickpaco', 'data')])
def change_silder(clickpaco):
    found = False
    if clickpaco == None:
        return no_update
    for k, v in clickpaco.items():
        if k == 'Hour':
            return v
    if found == False:
        return no_update

@app.callback(Output({"index": 5, "type": "slider"}, 'value'),
              [Input('clickpaco', 'data')])
def change_silder(clickpaco):
    found = False
    if clickpaco == None:
        return no_update
    for k, v in clickpaco.items():
        if k == 'Quarter':
            return v
    if found == False:
        return no_update

@app.callback(Output({"index": 3, "type": "slider"}, 'value'),
              [Input('clickpaco', 'data')])
def change_silder(clickpaco):
    found = False
    if clickpaco == None:
        return no_update
    for k, v in clickpaco.items():
        if k == 'DayofWeek':
            return v
    if found == False:
        return no_update


@app.callback(Output({"index": 4, "type": "slider"}, 'value'),
              [Input('clickpaco', 'data')])
def change_dow(clickpaco):
    found = False
    if clickpaco == None:
        return no_update
    for k, v in clickpaco.items():
        if k == 'WeekDay':
            #             print('found weekday')
            if v == 'Weekday':
                return 1
            else:
                return 2
#             return v.map({'Weekday':0,'Weekend':1})
    if found == False:
        return no_update


@app.callback(Output({"index": 2, "type": "slider"}, 'value'),
              [Input('clickpaco', 'data')])
def change_day(clickpaco):
    found = False
    if clickpaco == None:
        return no_update
    for k, v in clickpaco.items():
        if k == 'Day':
            return v
    if found == False:
        return no_update

@app.callback(Output({"index": 1, "type": "slider"}, 'value'),
              [Input('clickpaco', 'data')])
def change_month(clickpaco):
    found = False
    if clickpaco == None:
        return no_update
    for k, v in clickpaco.items():
        if k == 'Month':
            return v
    if found == False:
        return no_update


@app.callback(Output('clickpaco', 'data'),
              [Input('paco', 'clickData')],
              [State('pacodata', 'data')])
def save_click_data(clickData, pacodata):
    if clickData == None:
        return no_update
    else:
        df_id = clickData['points'][0]['pointNumber']

        rule = {}

        for i in pacodata:
            rule[i['label']] = i['values'][df_id]

        return rule


@app.callback(Output('quant', 'children'),
              [Input('dtrue', 'value')
               ])
def render_perc(tval):
    percent = float(tval)/100.0

    return percent


@app.callback(Output('sliders', 'children'),
              [Input('time_grand', 'value')
               ])
def render_sliders(time):

    return html.Div(children=make_sliders(time))


@app.callback([Output('pattern_bar', 'figure')],
              [Input({'type': 'slider', 'index': ALL}, 'value'),
               Input('year_slider', 'value'),
               Input('crime_type', 'value'),
               Input('space_grand', 'value'),
              Input('numslider','value'),
              Input('len_picker','value')])

def update_bar(values, year, crime, space, numshow, lenpick):
    time = {}
    for key, value in dash.callback_context.inputs.items():
        if 'index' in key:
            time[slider_map[key.replace('.value', '')]] = value

    subdf = subset_df(crime, space, year, time)
    
    rules=pattern(subdf, crime)
    
    
    
    rules=rules[rules['len'].isin(lenpick)]
    
    rules=rules.reset_index()
    
    rules=rules[:numshow]
    bar=px.bar(rules, y='support',color='len', hover_data=['itemsets']).update_layout(xaxis={'categoryorder':'total ascending'})

    
    return [bar]
    
    


@app.callback([Output('map', 'figure')],
              [Input({'type': 'slider', 'index': ALL}, 'value'),
               Input('year_slider', 'value'),
               Input('crime_type', 'value'),
               Input('space_grand', 'value')])
def update_map(values, year, crime, space):
    time = {}
#     year=[]
    for key, value in dash.callback_context.inputs.items():
        if 'index' in key:
            time[slider_map[key.replace('.value', '')]] = value

    subdf = subset_df(crime, space, year, time)

    col = list(subdf.columns)
    col.remove('Total Incidents')
    col_group = col

    newdf=subdf.groupby(col_group).count().reset_index().sort_values('Total Incidents')

#     for t in time.items():
#             newdf=newdf[newdf[t[0]]==t[1]]
    if 'Neighborhood_New' in space:
        single_dimension=pd.merge(neig,filter_df(newdf, time), left_on='Neighborhood_New',right_on='Neighborhood_New', how='left').fillna(0)

#         single_dimension=single_dimension[['Neighborhood_New','Total Incidents']]

        mapf=px.choropleth_mapbox(data_frame=single_dimension,hover_data=single_dimension.columns, color='Total Incidents',locations='Neighborhood_New', geojson=neigh_geojson,featureidkey="properties.Name",
                               center={"lat": 39.30, "lon": -76.61},
                               mapbox_style="carto-positron", zoom=10)
        mapf.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return [mapf]
    else:
        single_dimension=pd.merge(dist,filter_df(newdf, time), left_on='New_District',right_on='New_District', how='left').fillna(0)

#         single_dimension=single_dimension[['New_District','Total Incidents']]

        mapf=px.choropleth_mapbox(data_frame=single_dimension, hover_data=single_dimension.columns, color='Total Incidents',locations='New_District', geojson=dist_geojson,featureidkey="properties.dist_name",
                               center={"lat": 39.30, "lon": -76.61},
                               mapbox_style="carto-positron", zoom=10)
        mapf.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return [mapf]

@app.callback([Output('paco', 'figure'),
               Output('pacodata', 'data'),
               Output('years_selected','children'),
               Output('total','children')
               ],
              [Input({'type': 'slider', 'index': ALL}, 'value'),
               Input('year_slider', 'value'),
               Input('crime_type', 'value'),
               Input('space_grand', 'value'),
               Input('dtrue', 'value')])

def changein_sliders(values, year, crime, space, quant):
    time = {}
#     year=[]
    for key, value in dash.callback_context.inputs.items():
        if 'index' in key:
            time[slider_map[key.replace('.value', '')]] = value

    subdf = subset_df(crime, space, year, time)
    
    total=subdf['Total Incidents'].sum()

    paco, pacodata = make_paco(subdf, quant/100.0)

    return paco, pacodata, year[-1]-year[0],total


# @app.callback([Output('test_click', 'children')],
#                 [Input('pacodata', 'data')])

# def see_click(click):
#     return str(click)


if __name__ == '__main__':

    app.run_server(debug=True, port=8100)







