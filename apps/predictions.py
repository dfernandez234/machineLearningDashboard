import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import json
import plotly.graph_objects as go
import os
from os.path import dirname
from apps import DataDictionaries
from apps import PredictedValues

state = PredictedValues.statesDF()

from app import app

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

#assets
layout = html.Div([
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
                        html.Img(src='https://dl.dropboxusercontent.com/s/0f9pgtqxw8nw64n/globe-2-48.png?dl=0'),
                        html.Span()
                    ], className='button')
                ]),
                html.Li(children=[
                    html.Button(children=[
                        html.Img(src='https://dl.dropboxusercontent.com/s/ae910zfp11n17az/pie-chart-5-48.png?dl=0'),
                        html.Span()
                    ], className='button')
                ]),
                html.Li(children=[
                    html.Button(children=[
                        html.Img(src='https://dl.dropboxusercontent.com/s/nkj5hau236vfqu6/line-48.png?dl=0'),
                        html.Span()
                    ], className='button')
                ]),
                html.Li(children=[
                    html.Button(children=[
                        html.Img(src='https://dl.dropboxusercontent.com/s/tbgis3cno0li7zc/combo-48.png?dl=0'),
                        html.Span()
                    ], className='button')
                ])
            ],style={"list-style-type":"none", "margin":0 , "padding":0 })
        ],className='chartSidebar'),



        #sidebarControl
        html.Div([
            dbc.Nav(
                [
                    html.Ul(children=[
                        html.H5("Control Menu"),
                        html.Li(children=[
                            html.P("Indicator"),
                            html.Hr(),
                            dcc.RadioItems(id='indicator_checklist_pred',
                                options=[
                                    {'label': 'Incidence', 'value': 1},
                                    {'label': 'Mortality', 'value': 2},
                                ],
                                value = 2,
                                labelStyle={'display': 'inline-block',"padding-left": "5px"},
                                inputStyle={"margin-left": "0px", "margin-right": "0px"}
                            )  
                        ]),
                        html.Br(),
                        html.Li(children=[
                            html.P("States"),
                            html.Hr(),
                            dcc.Dropdown(id='state_dropdown_pred',
                                options=[{'label': i, 'value': j} for i, j in zip(state['state'].unique(), state['code'].unique())],
                                value="00",
                                style={"color":"white"}
                            )
                        ]),
                    ],style={"list-style-type":"none", "margin":0 , "padding":0 })
                ],
                vertical=True,
                pills=True,
            ),
        ],className='controlSidebar'),

        html.Div(id="page-content", children=[
            dbc.Row([
                html.Div(
                    children = [
                        html.H5(id='title_monthly',children=[]),
                        html.Hr(className="hrSlider"),
                        dcc.Graph(id="monthly_trend"),
                    ],className = "create_container1 twelve columns")
            ]),
            dbc.Row([
                html.Div(
                    children = [
                        html.H5(id='title_daily',children=[]),
                        html.Hr(className="hrSlider"),
                        dcc.Graph(id="daily_trend"),
                    ],className = "create_container1 twelve columns")
            ]),
        ],className='main-content_large')
    ],className='mainContainer'),
],className='mainDiv')


@app.callback(
    [Output('monthly_trend', 'figure'), Output('daily_trend', 'figure'),
    Output(component_id='title_monthly', component_property='children'),
    Output(component_id='title_daily', component_property='children')],
    [Input(component_id='indicator_checklist_pred', component_property='value'),
    Input(component_id='state_dropdown_pred', component_property='value')])

def getTendency(indicator, state):
    tendency = PredictedValues.read_result(indicator, state)

    daily_original, daily_predicted = PredictedValues.get_daily(tendency)
    monthly_original, monthly_predicted = PredictedValues.get_monthly(tendency)

    if state == '00':
        title_m = f'National {DataDictionaries.getIndic(indicator)} monthly predicted values.'
        title_d = f'National {DataDictionaries.getIndic(indicator)} daily predicted values.'

    else:
        title_m = f'{DataDictionaries.getStateKey(state)[0][0]} {DataDictionaries.getIndic(indicator)} monthly predicted values.'
        title_d = f'{DataDictionaries.getStateKey(state)[0][0]} {DataDictionaries.getIndic(indicator)} daily predicted values.'

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=monthly_original['day'], y=monthly_original['toll'], name = 'Original', mode='lines',line=dict(color='royalblue', width=3.5)))
    fig1.add_trace(go.Scatter(x=monthly_predicted['day'], y=monthly_predicted['toll'], name = 'Predicted',mode='lines',line=dict(color='crimson', width=3.5)))
    fig1.update_layout(title='Cancer Deaths',xaxis_title='Month',yaxis_title='Cancer Deaths')
    fig1.update_layout(margin={"r":0,"t":15,"l":0,"b":0},height=450,paper_bgcolor="#1A1A1A",font_color="white",plot_bgcolor = '#1A1A1A',font_size=16,title='')

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=daily_original['day'], y=daily_original['toll'], name = 'Original', mode='lines',line=dict(color='royalblue', width=3.5)))
    fig2.add_trace(go.Scatter(x=daily_predicted['day'], y=daily_predicted['toll'], name = 'Predicted', mode='lines',line=dict(color='crimson', width=3.5)))
    fig2.update_layout(title='Cancer Deaths',xaxis_title='Month',yaxis_title='Cancer Deaths')
    fig2.update_layout(margin={"r":0,"t":15,"l":0,"b":0},height=450,paper_bgcolor="#1A1A1A",font_color="white",plot_bgcolor = '#1A1A1A',font_size=16,title='')



    return fig1, fig2, title_m, title_d


