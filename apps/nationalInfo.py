import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go
import os
from os.path import dirname
from apps import DataDictionaries
import re

canc = DataDictionaries.cancerDF()
state = DataDictionaries.statesDF()

from app import app

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

#assets
layout = html.Div([
    dcc.Store(id='memory-output'),

    html.Div(children=[
        html.Div(children=[
            html.A(children=[
                html.Img(src='https://lh3.googleusercontent.com/ECbLDQsLxhea8DIQKT4_BrUPmpPT5xNXYGvEMqWUxp2CZfbV0bHsADAOvZ9rVYVUUE8YO7UiZeDeXsXl3JWrXlr6xpNvtQX4spW16IIlm1VBGkK6At_-cWNpiXM7FpS5RYTjxoV5mw=w2400?source=screenshot.guru', className="nav_logo")
            ],href="/apps/nationalInfo")
        ], className="logo"),

        html.Div([
                dbc.DropdownMenu(
                    [
                        dbc.DropdownMenuItem(dbc.NavLink('National', href='/apps/nationalInfo')),
                        dbc.DropdownMenuItem(dbc.NavLink('States', href='/apps/statesInfo')),
                        dbc.DropdownMenuItem(dbc.NavLink('Prediction', href='/apps/predictions')),
                    ],
                    label="View",
                ),
                html.P(id="item-clicks", className="mt-3"),
            ], className = "drop_links"),
    ], className="topNav"),

    dbc.Container([
        #sidebarChartPicker
        dbc.Container(children=[
            html.Ul(children=[
                html.Li(children=[
                    html.Button(children=[
                        html.Img(src='https://lh3.googleusercontent.com/wYaZ9uMqzpQbiuHDTqwMXLscL48ISDtCgDXL9uitX7PQDeJXejv05VsUo2NchWPo-sT1xrLPKhkTJ0damwL8Og45TV5OaUTmSFodIQnTQDYP-b7Y7b0ZZlM-f3PO6XF8QxUGOVpS0A=s48-p-k'),
                        html.Span()
                    ], className='button', id='chart1_button')
                ]),
                html.Li(children=[
                    html.Button(children=[
                        html.Img(src='https://lh3.googleusercontent.com/SJbgCiIHcr9qwhV2K-w1Y3_IgNZYckDG1qX3n2D21FT_3Mff49DTqUQ17vmkz5ohnXCffUJiXpZiU70atZ54nujypY_TEWY4ZVDWKzuSIg36oFoB9VZEqTZKmFbRnco8ri7_ZLFZFg=s48-p-k'),
                        html.Span()
                    ], className='button', id='chart2_button')
                ]),
                html.Li(children=[
                    html.Button(children=[
                        html.Img(src='https://lh3.googleusercontent.com/ZF0tz3pjPtoE7gji9qUKlv2p8n2kcLAhzQO03GfzjdsDmq6qa0KvxZIUCCuhKJIKLBGIgVWJ-ihlDiA_WzBA37jelca-Irr_oq-9xip8zYIQcfPv6JFOWm9bObDk7M0UZuEAdnwlRg=s48-p-k'),
                        html.Span()
                    ], className='button', id='chart3_button')
                ]),
                html.Li(children=[
                    html.Button(children=[
                        html.Img(src='https://lh3.googleusercontent.com/SykyJQT_7lviHR43H0kW_IHC6jcEq7y_61ruWbcweUYq88dNjQvPzpza8ZYkYUgDV1zXPWIko_KXwPfRqn-tI9K15f8gEKmUvO9QTb_MUADOM6bCx1qirBqWKettOAdMK7d_Jw6X8g=s48-p-k'),
                        html.Span()
                    ], className='button', id='chart4_button')
                ])
            ],style={"list-style-type":"none", "margin":0 , "padding":0 })
        ],className='chartSidebar', id = 'chartSidebar'),



        #sidebarControl
        html.Div([
            dbc.Nav(
                [
                    html.Ul(children=[
                        html.H5("Control Menu"),
                        html.Br(),
                        html.Li(children=[
                            html.P("Sex"),
                            html.Hr(),
                            dcc.RadioItems(id='sex-checklist',
                                options=[
                                    {'label': 'Male', 'value': 1},
                                    {'label': 'Female', 'value': 2},
                                    {'label': 'Both', 'value': 3},
                                ],
                                value = 1,
                                labelStyle={'display': 'inline-block',"padding-left": "5px"},
                                inputStyle={"margin-left": "0px", "margin-right": "0px"}
                            )  
                        ]),

                        html.Li(children=[
                            html.P("Indicator"),
                            html.Hr(),
                            dcc.RadioItems(id='indicator-checklist',
                                options=[
                                    {'label': 'Incidence', 'value': 1},
                                    {'label': 'Mortality', 'value': 2},
                                ],
                                value = 1,
                                labelStyle={'display': 'inline-block',"padding-left": "5px"},
                                inputStyle={"margin-left": "0px", "margin-right": "0px"}
                            )  
                        ]),

                        html.Li(children=[
                            html.P("Age Group"),
                            html.Hr(),
                            html.Br(),
                            html.Br(),
                            dcc.RangeSlider(
                                id='age-range-slider',
                                min=0,
                                max=90,
                                step=5,
                                value=[0, 90],
                                allowCross=False,
                                marks={
                                    0: {'label': '0'},
                                    45: {'label': '45'},
                                    90: {'label': '90'}
                                },
                                tooltip={'always_visible':False, 'placement':'bottom'}
                            )
                        ]),
                        html.Li(children=[
                            html.P("Cancer Sites"),
                            html.Hr(),
                            dcc.Dropdown(id='cancer-dropdown',
                                options=[{'label': i, 'value': j} for i, j in zip(canc['organ'].unique(), canc['ICD'].unique())],
                                multi=True,
                                value="C999",
                                style={"color":"white"}
                            )
                        ]),

                        html.Li(children=[
                            html.Table([
                                html.Tr([html.Td(['Cancer Sites: ']), html.Td(id='cancer_table')]),
                                html.Tr([html.Td(['Age Group: ']), html.Td(id='age_table')]),
                                html.Tr([html.Td(['Gender: ']), html.Td(id='gender_table')])
                             ]),
                        ]),

                    ],style={"list-style-type":"none", "margin":0 , "padding":0 })
                ],
                vertical=True,
                pills=True,
            ),
        ],className='controlSidebar', id='mainControlSidebar'),

        #sidebarControlTable
        html.Div([
            dbc.Nav(
                [
                    html.Ul(children=[
                        html.H5("Control Menu"),
                        html.Br(),
                        html.Li(children=[
                            html.P("Year"),
                            html.Hr(),
                            dcc.Slider(id='year_slider_table',
                                min=2010,
                                max=2019,
                                marks={                                
                                    2010: {'label': '2010'},
                                    2015: {'label': '2015'},
                                    2019: {'label': '2019'}
                                },
                                value=2012,
                            )
                        ]),

                        html.Li(children=[
                            html.P("Indicator"),
                            html.Hr(),
                            dcc.RadioItems(id='indicator_checklist_table',
                                options=[
                                    {'label': 'Incidence', 'value': 1},
                                    {'label': 'Mortality', 'value': 2},
                                ],
                                value = 1,
                                labelStyle={'display': 'inline-block',"padding-left": "5px"},
                                inputStyle={"margin-left": "0px", "margin-right": "0px"}
                            )  
                        ]),

                        html.Li(children=[
                            html.P("Age Group"),
                            html.Hr(),
                            dcc.RangeSlider(
                                id='age-range-table',
                                min=0,
                                max=90,
                                step=5,
                                value=[0, 90],
                                allowCross=False,
                                marks={
                                    0: {'label': '0'},
                                    45: {'label': '45'},
                                    90: {'label': '90'}
                                },
                                tooltip={'always_visible':False, 'placement':'bottom'}
                            )
                        ]),
                        
                        html.Li(children=[
                            html.Br(),
                            html.Div(
                                [
                                    html.Button("Download Data", id="btn_xlxs", className = "downloadButton"),
                                    dcc.Download(id="download-dataframe-xlxs"),
                                ]
                            )
                        ])

                     ],style={"list-style-type":"none", "margin":0 , "padding":0 },id="table_list")
                ],
                vertical=True,
                pills=True,
            ),
        ],className='controlSidebar', id='controlTable'),

        #sidebarControlPie
        html.Div([
            dbc.Nav(
                [
                    html.Ul(children=[
                        html.H5("Control Menu"),
                        html.Br(),
                        html.Li(children=[
                            html.P("Year"),
                            html.Hr(),
                            dcc.Slider(id='year_slider_pie',
                                min=2010,
                                max=2019,
                                marks={                                
                                    2010: {'label': '2010'},
                                    2015: {'label': '2015'},
                                    2019: {'label': '2019'}
                                },
                                value=2012,
                            )
                        ]),
                        html.Li(children=[
                            html.P("Indicator"),
                            html.Hr(),
                            dcc.RadioItems(id='indicator_checklist_pie',
                                options=[
                                    {'label': 'Incidence', 'value': 1},
                                    {'label': 'Mortality', 'value': 2},
                                ],
                                value = 1,
                                labelStyle={'display': 'inline-block',"padding-left": "5px"},
                                inputStyle={"margin-left": "0px", "margin-right": "0px"}
                            )  
                        ]),
                        html.Li(children=[
                            html.P("Age Group"),
                            html.Hr(),
                            html.Br(),
                            html.Br(),
                            dcc.RangeSlider(
                                id='age-range-pie',
                                min=0,
                                max=90,
                                step=5,
                                value=[0, 90],
                                allowCross=False,
                                marks={
                                    0: {'label': '0'},
                                    45: {'label': '45'},
                                    90: {'label': '90'}
                                },
                                tooltip={'always_visible':False, 'placement':'bottom'}
                            )
                        ]),

                     ],style={"list-style-type":"none", "margin":0 , "padding":0 })
                ],
                vertical=True,
                pills=True,
            ),
        ],className='controlSidebar', id='controlSidebar_pie'),
        
        #sidebarControlLines
        html.Div([
            dbc.Nav(
                [
                    html.Ul(children=[
                        html.H5("Control Menu"),
                        html.Br(),
                        html.Li(children=[
                            html.P("Year"),
                            html.Hr(),
                            dcc.Slider(id='year_slider_line',
                                min=2010,
                                max=2019,
                                marks={                                
                                    2010: {'label': '2010'},
                                    2015: {'label': '2015'},
                                    2019: {'label': '2019'}
                                },
                                value=2012,
                            )
                        ]),
                        html.Li(children=[
                            html.P("Indicator"),
                            html.Hr(),
                            dcc.RadioItems(id='indicator_checklist_line',
                                options=[
                                    {'label': 'Incidence', 'value': 1},
                                    {'label': 'Mortality', 'value': 2},
                                ],
                                value = 1,
                                labelStyle={'display': 'inline-block',"padding-left": "5px"},
                                inputStyle={"margin-left": "0px", "margin-right": "0px"}
                            )  
                        ]),
                        html.Li(children=[
                            html.P("Age Group"),
                            html.Hr(),
                            html.Br(),
                            html.Br(),
                            dcc.RangeSlider(
                                id='age-range-line',
                                min=0,
                                max=90,
                                step=5,
                                value=[0, 90],
                                allowCross=False,
                                marks={
                                    0: {'label': '0'},
                                    45: {'label': '45'},
                                    90: {'label': '90'}
                                },
                                tooltip={'always_visible':False, 'placement':'bottom'}
                            )
                        ]),

                        html.Li(children=[
                            html.P("Cancer Sites"),
                            html.Hr(),
                            dcc.Dropdown(id='cancer-dropdown-line',
                                options=[{'label': i, 'value': j} for i, j in zip(canc['organ'].unique(), canc['ICD'].unique())],
                                multi=True,
                                value="C34",
                                style={"color":"white"}
                            )
                        ]),


                    ],style={"list-style-type":"none", "margin":0 , "padding":0 })
                ],
                vertical=True,
                pills=True,
            ),
        ],className='controlSidebar', id='controlSidebar_line'),

     
        html.Div(id="page-content", children=[
            dcc.Tabs(
            id="tabs-with-classes",
            value='tab-1',
            parent_className='custom-tabs',
            className='custom-tabs-container',
            children=[
                dcc.Tab(
                    label='Map View',
                    value='tab-1',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                        html.Div([
                            dbc.Row([
                                dbc.Col(
                                    html.Div(className='output_container', children=[
                                        html.Div(children = [
                                        #MAP Mex
                                        html.Div(
                                                children = [
                                                    html.H6("Drag the Slider to pick the Year"),
                                                    html.Br(),
                                                    dcc.Slider(id='year-slider',
                                                        min=2010,
                                                        max=2019,
                                                        marks={x: {'label': str(x)} for x in range(2010,2020)},
                                                        value=2012,
                                                    ),
                                                    html.Hr(className="hrSlider"),
                                                    html.H5(id='title',children=[]),
                                                    dcc.Loading(children=[dcc.Graph(id="choropleth")], color="#ff3b14",type="cube",fullscreen=True,style={"background-color":"#0f0f0f"}),
                                            ],className = "create_container1 twelve columns")
                                        ],className = "row flex-display"),
                                    ])
                                ,width=10),
                                dbc.Col([
                                    dbc.Row(dbc.Col(children=[
                                        html.Br(),
                                        #html.Div([
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.H6(
                                                    children = "Total Cases",
                                                    style = {
                                                        "textAlign": "center",
                                                        "color": "white",
                                                        "fontSize": 23
                                                    }),
                                                html.P(id='total_big',children=[],
                                                    style = {
                                                        "textAlign": "center",
                                                        "color": "orange",
                                                        "fontSize": 23
                                                    }),
                                            ]),
                                        ],style={"width": "14.3rem"},),html.Br() 
                                    ])),
                                    dbc.Row(dbc.Col(children=[
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.H6(
                                                    children = "Most Affected State",
                                                    style = {
                                                        "textAlign": "center",
                                                        "color": "white",
                                                        "fontSize": 23
                                                    }),
                                                    html.P(id='most_state_big',children=[],
                                                        style = {
                                                            "textAlign": "center",
                                                            "color": "#dd1e35",
                                                            "fontSize": 23
                                                        }),
                                                    html.P(id='most_state_small',children=[],
                                                        style = {
                                                            "textAlign": "center",
                                                            "color": "#dd1e35",
                                                            "fontSize": 20,
                                                            "margin-top": "-18px"
                                                        })
                                                    ]),
                                        ],style={"width": "14.3rem"},),html.Br()                                    
                                    ])),
                                    dbc.Row(dbc.Col(children=[
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.H6(
                                                    children = "Least Affected Sate",
                                                    style = {
                                                        "textAlign": "center",
                                                        "color": "white",
                                                        "fontSize": 23
                                                    }),
                                                html.P(id='least_state_big',children=[],
                                                    style = {
                                                        "textAlign": "center",
                                                        "color": "green",
                                                        "fontSize": 23
                                                    }),
                                                html.P(id='least_state_small',children=[],
                                                    style = {
                                                        "textAlign": "center",
                                                        "color": "green",
                                                        "fontSize": 20,
                                                        "margin-top": "-18px"
                                                    })
                                            ]),
                                        ],style={"width": "14.3rem"},),html.Br()                              
                                    ])),
                                    dbc.Row(dbc.Col(children=[
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.H6(
                                                    children = "Rate",
                                                    style = {
                                                        "textAlign": "center",
                                                        "color": "white",
                                                        "fontSize": 23
                                                    }),
                                                html.P(id='rate_big',children=[],
                                                    style = {
                                                        "textAlign": "center",
                                                        "color": "#e55467",
                                                        "fontSize": 23
                                                    }),
                                                html.P(id='rate_small',children=[],
                                                    style = {
                                                        "textAlign": "center",
                                                        "color": "#e55467",
                                                        "fontSize": 20,
                                                        "margin-top": "-18px"
                                                    })
                                            ]),
                                        ],style={"width": "14.3rem"},)                    
                                    ]))
                                ],width=2),
                            ]),
                        ])
                    ]
                ),
                dcc.Tab(
                    label='Statistics View',
                    value='tab-2',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                        html.Div(className='output_container', children=[
                            html.Div([
                                dbc.Row([
                                        html.Div(
                                            children = [
                                                html.H5(id='title_chart_bars',children=[]),
                                                html.Hr(className="hrSlider"),
                                                dcc.Graph(id="chart_bars"),
                                            ],className = "create_container1 twelve columns"),
                                        html.Div(
                                        children = [
                                            html.H5(id='title_chart_table',children=[]),
                                            dcc.Graph(id="chart_table"),
                                        ],className = "create_container1 twelve columns"),
                                    ]),
                                html.Hr(className="hrSlider"),
                            ],id='table'),

                            html.Div([
                                dbc.Row([
                                    html.Div(
                                        children = [
                                            html.H5(id='title_chart_pie',children=[]),
                                            html.Hr(className="hrSlider"),
                                            dcc.Graph(id="chart_pie"),
                                        ],className = "create_container1 twelve columns"),
                                    ]),
                                html.Hr(className="hrSlider"),
                            ],id='pie'),

                            html.Div([
                                dbc.Row([
                                    html.Div(
                                        children = [
                                            html.H5(id='title_chart_line',children=[]),
                                            html.Hr(className="hrSlider"),
                                            dcc.Graph(id="chart_line"),
                                        ],className = "create_container1 twelve columns")
                                    ]),
                                html.Hr(className="hrSlider"),
                            ],id='line'),

                          ])
                    ])
            ]),html.Div(id='tabs-content-classes'),
        ],className='main-content_large')
    ],className='mainContainer'),
],className='mainDiv')



#callbacks refering button clicks
@app.callback([Output('chartSidebar', 'style'),Output('mainControlSidebar', 'style'),
                Output('controlTable','style'),
                Output('controlSidebar_pie','style'),
                Output('controlSidebar_line','style'),
                Output('table','style'),
                Output('pie','style'),
                Output('line','style'),],

              [Input('chart1_button', 'n_clicks'),
              Input('chart2_button', 'n_clicks'),
              Input('chart3_button', 'n_clicks'),
              Input('chart4_button', 'n_clicks'),
              Input('tabs-with-classes', 'value')])


def displayClick(n_clicks, btn2, btn3, btn4, tab):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if tab == 'tab-1':
        chart_style = {'display': 'none'}
        control1 = {'display': 'block'}

        table = {'display': 'none'}
        pie = {'display': 'none'}
        line = {'display': 'none'}
        
        tableDiv = {'display': 'none'}
        pieDiv = {'display': 'none'}
        lineDiv = {'display': 'none'}
        
        return chart_style, control1, table,pie,line, tableDiv, pieDiv, lineDiv

    if tab == 'tab-2':
        chart_style = {'display': 'block'}
        control1 = {'display': 'none'}
        
        table = {'display': 'block'}
        pie = {'display': 'none'}
        line = {'display': 'none'}
        
        tableDiv = {'display': 'block'}
        pieDiv = {'display': 'none'}
        lineDiv = {'display': 'none'}

        if 'chart2_button' in changed_id:
            table = {'display': 'none'}
            pie = {'display': 'block'}
            line = {'display': 'none'}

            tableDiv = {'display': 'none'}
            pieDiv = {'display': 'block'}
            lineDiv = {'display': 'none'}


        if 'chart3_button' in changed_id:
            table = {'display': 'none'}
            pie = {'display': 'none'}
            line = {'display': 'block'}

            tableDiv = {'display': 'none'}
            pieDiv = {'display': 'none'}
            lineDiv = {'display': 'block'}

        if 'chart1_button' in changed_id or 'chart4_button' in changed_id:
            table = {'display': 'block'}
            pie = {'display': 'none'}
            line = {'display': 'none'}

            tableDiv = {'display': 'block'}
            pieDiv = {'display': 'none'}
            lineDiv = {'display': 'none'}
        
        return chart_style, control1, table,pie,line, tableDiv, pieDiv, lineDiv, 



#get values
@app.callback([Output(component_id='title', component_property='children'),
    Output(component_id='cancer_table', component_property='children'),
    Output(component_id='age_table', component_property='children'),
    Output(component_id='gender_table', component_property='children'),
    Output('choropleth', 'figure'),
    Output(component_id='total_big', component_property='children'),
    Output(component_id='most_state_big', component_property='children'),
    Output(component_id='most_state_small', component_property='children'),
    Output(component_id='least_state_big', component_property='children'),
    Output(component_id='least_state_small', component_property='children'),
    Output(component_id='rate_big', component_property='children'),
    Output(component_id='rate_small', component_property='children')],

    [Input(component_id='year-slider', component_property='value'),
        Input(component_id='sex-checklist', component_property='value'),
        Input(component_id='cancer-dropdown', component_property='value'),
        Input(component_id='age-range-slider', component_property='value'),
        Input(component_id='indicator-checklist', component_property='value')])

def get_values(year_chosen, gender_chosen, icd_chosen, age_range,indicator):

    title = f"age-standardized {DataDictionaries.getIndic(indicator)} rates (Mexico) in {year_chosen}"

    if(icd_chosen == 'C999' or 'C999' in icd_chosen):
        cancer_sites = "All Sites"
    else:
        cancer_sites = DataDictionaries.getCancerKey(icd_chosen)

    age_range_out = f"{age_range[0]} - {age_range[1]}"
        
    gender_out = DataDictionaries.getSex(gender_chosen)

    # GENERATE MAP

    if(gender_chosen == 3):
        dff = DataDictionaries.solveQueryBothSexes(year_chosen, icd_chosen, age_range, indicator)
    else:
        dff = DataDictionaries.solveQuery(year_chosen, gender_chosen, icd_chosen, age_range, indicator)

    #load polygons
    pPath = os.getcwd()+ r'/geoData/newStates.json'
    with open(pPath, encoding="utf8") as f:
        counties = json.load(f)

    fig = go.Figure(px.choropleth_mapbox(dff, geojson=counties, featureidkey='properties.state_code',
        locations='unique_values', color='counts',
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        zoom=4.6, center = {"lat":23.634501 , "lon": -102.552784},
        opacity=1,
        labels={'counts':f'{DataDictionaries.getIndic(indicator)}'},
        hover_name="unique_values"))         
        
    accesstoken = "pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw"
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=accesstoken)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},height=750)
    fig.update_layout(coloraxis=dict(colorbar_thickness=30, colorbar_bgcolor='#1A1A1A',colorbar_tickfont_color='#fff',colorbar_title_font_color='#fff',colorbar_xanchor="right"))

    dff = dff.sort_values(by=['counts'])
    total_big_ret = f"{dff['counts'].sum()}"

    mast = dff.iloc[-1,0]
    most_state_big_ret = f"{DataDictionaries.getStateKey(mast)[0][0]}"

    mast_s = dff.iloc[-1,1]
    most_state_small_ret = f"{mast_s} cases"

    lst = dff.iloc[0,0]
    least_state_big_ret = f"{DataDictionaries.getStateKey(lst)[0][0]}"

    lst_s = dff.iloc[0,1]
    least_state_small_ret = f"{lst_s} cases"


    rate_big_res = (dff['counts'].sum()/DataDictionaries.getPopulationNational(year_chosen))*100000
    rate_big_ret = str(round(rate_big_res, 2))
    rate_small_ret = f"{rate_big_ret} deaths per 100,000 population"

    return title, cancer_sites, age_range_out, gender_out, fig, total_big_ret, most_state_big_ret, most_state_small_ret, least_state_big_ret, least_state_small_ret, rate_big_ret, rate_small_ret


#Table chart

#callbacks refering button clicks
@app.callback([Output(component_id='title_chart_table', component_property='children'),
                Output('chart_table', 'figure'), 
                Output(component_id='title_chart_bars', component_property='children'),
                Output('chart_bars', 'figure'),
                Output('memory-output', 'data')],

              [Input(component_id='year_slider_table', component_property='value'),
              Input(component_id='age-range-table', component_property='value'),
              Input(component_id='indicator_checklist_table', component_property='value')])

def displayTable(year,age,indicator):
    rowOddColor = '#0f0f0f'
    rowEvenColor = '#2c2b2b'
    title = f'{year} {DataDictionaries.getIndic(indicator)} sites'
    df = DataDictionaries.generate_report(year, age, indicator)
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['ICD', 'Organ', 'Male Cases', 'Female Cases', 'Total Cases', f'{DataDictionaries.getIndic(indicator)} Rate per 100,000'],
            fill_color='rgb(8, 81, 156)',
            align='center',
            font=dict(color='white', size=17)),

        cells=dict(values=[df[k].tolist() for k in df.columns[:]],
            fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*df.shape[0]],
            align='center',
            font=dict(color='white', size=15)))
        ])

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},height=150,paper_bgcolor="#1A1A1A",plot_bgcolor = '#1A1A1A',showlegend=False),

    df = df.sort_values('Total Cases')
    title2 = f'{year} {DataDictionaries.getIndic(indicator)} National Cases'
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        y=df['Organ'],
        x=df['Male Cases'],
        name='Male Cases',
        orientation='h',
        marker=dict(
        color='rgba(47, 35, 219, 0.6)',
        line=dict(color='rgba(47, 35, 219, 1.0)', width=3)
        )
    ))
    fig2.add_trace(go.Bar(
        y=df['Organ'],
        x=df['Female Cases'],
        name='Female Cases',
        orientation='h',
        marker=dict(
            color='rgba(246, 78, 139, 0.6)',
            line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
            )
    ))

    fig2.update_layout(barmode='stack')
    fig2.update_layout(title='',xaxis_title=f'{DataDictionaries.getIndic(indicator)}',yaxis_title='Cancer Site')
    fig2.update_layout(margin={"r":0,"t":50,"l":0,"b":0},height=650,paper_bgcolor="#1A1A1A",font_color="white",font_size=16,plot_bgcolor = '#1A1A1A',title='')
        
    report = df.to_dict('index')
    return title, fig, title2, fig2, report


#download callback
@app.callback(
    Output("download-dataframe-xlxs", "data"),
    [Input("btn_xlxs", "n_clicks"), Input('memory-output', 'data')],prevent_initial_call=True)

def DownloadBtn(btn_xlxs, data):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if data is None:
        raise PreventUpdate
    else:
        dff = pd.DataFrame.from_dict(data, orient='index')
        if 'btn_xlxs' in changed_id:
            return dcc.send_data_frame(dff.to_csv, "mydf.csv")


#Pie

@app.callback([Output(component_id='title_chart_pie', component_property='children'),
                Output('chart_pie', 'figure')],

              [Input(component_id='year_slider_pie', component_property='value'),
              Input(component_id='age-range-pie', component_property='value'),
              Input(component_id='indicator_checklist_pie', component_property='value')])

def displayPie(year,age, indicator):
    title = f'{year} {DataDictionaries.getIndic(indicator)} Most Common Sites'
    dff = DataDictionaries.generate_report_suburst(year,age,indicator)
    fig = px.sunburst(dff, path=['Gender', 'Organ', 'counts'], values='counts',color='counts', hover_data=['counts'],
            color_continuous_scale='RdBu',
            color_continuous_midpoint=np.average(dff['counts'], weights=dff['counts']))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},height=750,paper_bgcolor="#1A1A1A",font_color="white")
    fig.update_layout(coloraxis=dict(colorbar_thickness=30, colorbar_bgcolor='#1A1A1A',colorbar_tickfont_color='#fff',colorbar_title_font_color='#fff',colorbar_xanchor="right"))
    fig.update_layout(font=dict(size=16), title='')

    return title, fig



#line
@app.callback([Output(component_id='title_chart_line', component_property='children'),
                Output('chart_line', 'figure')],

              [Input(component_id='year_slider_line', component_property='value'),
              Input(component_id='age-range-line', component_property='value'),
              Input(component_id='cancer-dropdown-line', component_property='value'),
              Input(component_id='indicator_checklist_line', component_property='value')])

def displayLine(year,age,cancer,indicator):
    dff = DataDictionaries.generate_report(year, age,indicator)
    dff = dff.sort_values('Total Cases', ascending=False)
    colors = ['lightgoldenrodyellow', 'mistyrose', 'lightpink','darkmagenta','firebrick','steelblue','snow','gold','crimson','mediumseagreen']
    title = f'{year} {DataDictionaries.getIndic(indicator)} Monthly National Cases'
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
    dfL = DataDictionaries.generate_time_series(year,age,indicator)
    fig = go.Figure()

    i = 0
    if isinstance(cancer, list):
        for site in cancer:
            fig.add_trace(go.Scatter(x=month, y=dfL[site], mode='lines+markers',name=DataDictionaries.getCancerKey(site),line=dict(color=colors[i], width=4),marker=dict(color='orange',size=10,line=dict(color='black',width=2))))
            i = i+1
    else:
        fig.add_trace(go.Scatter(x=month, y=dfL['C34'], mode='lines+markers',name=DataDictionaries.getCancerKey('C34'),line=dict(color='green', width=4),marker=dict(color='orange',size=10,line=dict(color='black',width=2))))


    
    # Create and style traces
    #for i in range (0,10,1):
    #    site = dff.iloc[i]['ICD']
    #    fig.add_trace(go.Scatter(x=month, y=dfL[site], mode='lines+markers',name=DataDictionaries.getCancerKey(site),line=dict(color=colors[i], width=4),marker=dict(color='orange',size=10,line=dict(color='black',width=2))))

    fig.update_layout(title='Cancer Deaths',xaxis_title='Month',yaxis_title='Cancer Deaths')
    fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0},height=750,paper_bgcolor="#1A1A1A",font_color="white",plot_bgcolor = '#1A1A1A',font_size=16,title='')

    return title, fig



