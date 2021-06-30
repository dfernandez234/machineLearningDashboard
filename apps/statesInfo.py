import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go
import os
from os.path import dirname
from dash.exceptions import PreventUpdate
from apps import DataDictionaries
from apps import DataDictionariesStates

canc = DataDictionaries.cancerDF()
state = DataDictionaries.statesDF()

# Connect to main app.py file
from app import app


#assets
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

layout = html.Div([
    dcc.Store(id='memory-output-state'),


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
                        html.Img(src='https://lh3.googleusercontent.com/DTKhadZ9kIVfsWVY9jJHrYMBik78Iu0kDJQJsr-VdSNSNqT6Hj7E462nUNkxxTH0qBxIQrs1au1nyiEXaLfwVIA8ardOgy232yhN9wsJFtaYB-vfYCeBcPJUj9d1RUa8zbANhubt7A=s48-p-k'),
                        html.Span(),
                        html.A("",href='/apps/nationalInfo')
                    ], className='button', id='chart1_button_states')
                ]),
                html.Li(children=[
                    html.Button(children=[
                        html.Img(src='https://lh3.googleusercontent.com/SykyJQT_7lviHR43H0kW_IHC6jcEq7y_61ruWbcweUYq88dNjQvPzpza8ZYkYUgDV1zXPWIko_KXwPfRqn-tI9K15f8gEKmUvO9QTb_MUADOM6bCx1qirBqWKettOAdMK7d_Jw6X8g=s48-p-k'),
                        html.Span()
                    ], className='button', id='chart2_button_states')
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
                            dcc.RadioItems(id='sex_states',
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
                            dcc.RadioItems(id='indicator-checklist-states',
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
                                id='age_range_states',
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
                            dcc.Dropdown(id='cancer_states',
                                options=[{'label': i, 'value': j} for i, j in zip(canc['organ'].unique(), canc['ICD'].unique())],
                                multi=True,
                                value="C999",
                                style={"color":"white"}
                            )
                        ]),

                        html.Li(children=[
                            html.P("States"),
                            html.Hr(),
                            dcc.Dropdown(id='state_dropdown',
                                options=[{'label': i, 'value': j} for i, j in zip(state['state'].unique(), state['code'].unique())],
                                value="01",
                                style={"color":"white"}
                            )
                        ]),
    

                        html.Li(children=[
                            html.Table([
                                html.Tr([html.Td(['Cancer Sites: ']), html.Td(id='cancer_table_states')]),
                                html.Tr([html.Td(['Age Group: ']), html.Td(id='age_table_states')]),
                                html.Tr([html.Td(['Gender: ']), html.Td(id='gender_table_states')]),
                                html.Tr([html.Td(['State: ']), html.Td(id='table_states')])
                             ]),
                        ])
                    ],style={"list-style-type":"none", "margin":0 , "padding":0 })
                ],
                vertical=True,
                pills=True,
            ),
        ],className='controlSidebar'),
        html.Div(id="page-content", children=[
            html.Div(className='output_container', children=[
                html.Div([
                    dbc.Row([
                        dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6(
                                    children = "Total Cases",
                                    style = {
                                        "textAlign": "center",
                                        "color": "white",
                                        "fontSize": 23
                                    }),
                                html.P(id='total_state_big',children=[],
                                    style = {
                                        "textAlign": "center",
                                        "color": "#dd1e35",
                                        "fontSize": 23
                                    }),
                            ]),
                        ],style={"width": "250px", "right":"0"})]),

                        dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6(
                                    children = "Most Affected Municipality",
                                    style = {
                                        "textAlign": "center",
                                        "color": "white",
                                        "fontSize": 23
                                    }),
                                html.P(id='most_mun_big',children=[],
                                    style = {
                                        "textAlign": "center",
                                        "color": "green",
                                        "fontSize": 23
                                    }),
                                html.P(id='most_mun_small',children=[],
                                    style = {
                                        "textAlign": "center",
                                        "color": "green",
                                        "fontSize": 20,
                                        "margin-top": "-18px"
                                    })
                            ]),
                        ],style={"width": "350px", 'height': '150px',"left":"0"})])
                    ]),

                    dbc.Row([
                        dbc.Col(
                            html.Div(children = [
                                #MAP State
                                html.Div(children = [
                                    html.H6("Drag the Slider to pick the Year"),
                                    html.Br(),
                                    html.Br(),
                                    dcc.Slider(id='year_slider_states',
                                        min=2010,
                                        max=2019,
                                        marks={x: {'label': str(x)} for x in range(2010,2020)},
                                        value=2012,
                                    ),
                                    html.Hr(className="hrSlider"),
                                    html.H5(id='title-states',children=[]),
                                    dcc.Loading(children=[dcc.Graph(id="choropleth-states")], color="#ff3b14", type="cube"),
                                ],className = "create_container1 twelve columns")
                            ],className = "row flex-display")),
                        
                        dbc.Col(
                            html.Div(children = [
                                html.Div(children = [
                                    html.H6("Pick a Graph from the Dropdown"),
                                    html.Br(),
                                    dcc.Dropdown(id = 'graph_picker',
                                        options=[
                                            {'label': 'Table', 'value': 'TBL'},
                                            {'label': 'Bar Chart', 'value': 'BAR'},
                                            {'label': 'Pie Chart', 'value': 'PIE'},
                                        ],
                                        value='BAR',
                                        clearable=False
                                    ),  
                                    html.Hr(className="hrSlider"),
                                    dcc.Loading(children=[
                                    dbc.Row([
                                        dbc.Col([
                                            html.H5(id='title_chart_states',children=[]),
                                        ]),
                                        dbc.Col([
                                            html.Br(),
                                            html.Div([
                                                html.Button("Download Data", id="btn_xlxs_state", className = "downloadButton"),
                                                dcc.Download(id="download-dataframe-states")
                                            ], id="hide_button"),
                                        ])
                                    ]),
                                    html.Br(),
                                    dcc.Graph(id="custom_chart_states")], color="#ff3b14", type="cube"),
                                ],className = "create_container1 twelve columns")
                            ],className = "row flex-display")),
                    ]),

                    html.Hr(className="hrSlider"),

                    dcc.Loading(children=[
                    html.Div([
                        dbc.Row([
                            html.Div(
                                children = [
                                html.H5(id='title_chart_comp',children=[]),
                                html.Hr(className="hrSlider"),
                                dcc.Graph(id="chart_comp"),
                            ],className = "create_container1 twelve columns")
                        ]),
                        html.Hr(className="hrSlider"),
                    ])], color="#ff3b14", type="cube"),

                    html.Br(), 
                ])
            ])            
        ],className='main-content_large')
    ],className='mainContainer'),
],className='mainDiv')

    
#get values
@app.callback([Output(component_id='title-states', component_property='children'),
            Output(component_id='cancer_table_states', component_property='children'),
            Output(component_id='age_table_states', component_property='children'),
            Output(component_id='gender_table_states', component_property='children'),
            Output(component_id='table_states', component_property='children'),
            Output('choropleth-states', 'figure'),
            Output(component_id='total_state_big', component_property='children'),
            Output(component_id='most_mun_big', component_property='children'),
            Output(component_id='most_mun_small', component_property='children'),
            Output(component_id='title_chart_states', component_property='children'),
            Output('custom_chart_states', 'figure'),
            Output('hide_button','style'),
            Output('memory-output-state', 'data')],

    [Input(component_id='sex_states', component_property='value'),
        Input(component_id='age_range_states', component_property='value'),
        Input(component_id='cancer_states', component_property='value'),
        Input(component_id='state_dropdown', component_property='value'),
        Input(component_id='year_slider_states', component_property='value'),
        Input(component_id='graph_picker', component_property='value'),
        Input(component_id='indicator-checklist-states', component_property='value')])   

def get_values(gender, age, icd, state, year, graph, indicator):

    title = f"age-standardized {DataDictionaries.getIndic(indicator)} rates ({DataDictionaries.getStateKey(state)[0][0]}) in {year}"

    styleButton = {'display': 'none'}

    data = dict()

    if(icd == 'C999' or 'C999' in icd):
        cancer_sites = "All Sites"
    else:
        cancer_sites = DataDictionaries.getCancerKey(icd)

    age_range_out = f"{age[0]} - {age[1]}"
    
    gender_out = DataDictionaries.getSex(gender)

    state_out = DataDictionaries.getStateKey(state)

    if(gender == 3):
        dff = DataDictionariesStates.solveQueryBothSexesState(year, icd, age, state, indicator)
    else:
        dff = DataDictionariesStates.solveQueryState(year, gender, icd, age, state, indicator)
    

    #load polygons
    stateToLoad = DataDictionaries.getStateKey(state)[0][0].replace(" ", "")
    
    pPath = os.getcwd()+ f'/geoData/muns/{stateToLoad}.json'
    with open(pPath, encoding="utf8") as f:
        counties = json.load(f)

    fig = go.Figure(px.choropleth_mapbox(dff, geojson=counties, featureidkey='properties.mun_code',
                           locations='unique_values', color='counts',
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=6, center = {"lat":DataDictionaries.getStateKey(state)[0][1] , "lon": DataDictionaries.getStateKey(state)[0][2]},
                           opacity=1,
                           labels={'counts':'Deceased'},
                           hover_name="unique_values"))         
    
    accesstoken = "pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw"
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=accesstoken)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},height=500)
    fig.update_layout(coloraxis=dict(colorbar_thickness=30, colorbar_bgcolor='#1A1A1A',colorbar_tickfont_color='#fff',colorbar_title_font_color='#fff',colorbar_xanchor="right"))

    dff = dff.sort_values(by=['counts'], ascending=False)

    total_big_ret = f"{dff['counts'].sum()}"

    mostMun = f"{DataDictionariesStates.getMunKey(int(dff.iloc[0]['unique_values']))[0][2]}"
    mustMunCases = f"{dff.iloc[0]['counts']} cases"

    if graph == 'TBL':
        styleButton = {'display': 'block'}
        df = DataDictionariesStates.generate_report_state(year, age, state, indicator)
        data = df.to_dict('index')
        rowOddColor = '#0f0f0f'
        rowEvenColor = '#2c2b2b'
        titleChart = f'{year} {DataDictionaries.getIndic(indicator)} cases by Site'
        chart = go.Figure(data=[go.Table(
            header=dict(
                        values=['ICD', 'Organ', 'Male Cases', 'Female Cases', 'Total Cases'],
                        fill_color='rgb(8, 81, 156)',
                        align='center',
                        font=dict(color='white', size=17)),

            cells=dict(values=[df[k].tolist() for k in df.columns[:]],
                        fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*df.shape[0]],
                        align='center',
                        font=dict(color='white', size=15)))
            ])

        chart.update_layout(margin={"r":0,"t":0,"l":0,"b":0},height=650,paper_bgcolor="#1A1A1A",plot_bgcolor = '#1A1A1A',showlegend=False)

    if graph == 'BAR':
        df = DataDictionariesStates.generate_report_state(year, age, state, indicator)
        df = df.sort_values('Total Cases')
        titleChart = f'{year} {DataDictionaries.getIndic(indicator)}'
        chart = go.Figure()
        chart.add_trace(go.Bar(
            y=df['Organ'],
            x=df['Male Cases'],
            name='Male Cases',
            orientation='h',
            marker=dict(
            color='rgba(47, 35, 219, 0.6)',
            line=dict(color='rgba(47, 35, 219, 1.0)', width=3)
            )
        ))
        chart.add_trace(go.Bar(
            y=df['Organ'],
            x=df['Female Cases'],
            name='Female Cases',
            orientation='h',
            marker=dict(
                color='rgba(246, 78, 139, 0.6)',
                line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
                )
        ))

        chart.update_layout(barmode='stack')
        chart.update_layout(title='',xaxis_title='Deaths',yaxis_title='Cancer Site')
        chart.update_layout(margin={"r":0,"t":50,"l":0,"b":0},height=650,paper_bgcolor="#1A1A1A",font_color="white",font_size=16,plot_bgcolor = '#1A1A1A',title='')

    if graph == 'PIE':

        titleChart = f'Most common {DataDictionaries.getIndic(indicator)} sites'
        dff = DataDictionariesStates.generate_report_suburst_state(year,age,state, indicator)
        chart = px.sunburst(dff, path=['Gender', 'Organ', 'counts'], values='counts',color='counts', hover_data=['counts'],
                color_continuous_scale='RdBu',
                color_continuous_midpoint=np.average(dff['counts'], weights=dff['counts']))
        chart.update_layout(margin={"r":0,"t":0,"l":0,"b":0},height=550,paper_bgcolor="#1A1A1A",font_color="white")
        chart.update_layout(coloraxis=dict(colorbar_thickness=30, colorbar_bgcolor='#1A1A1A',colorbar_tickfont_color='#fff',colorbar_title_font_color='#fff',colorbar_xanchor="right"))
        chart.update_layout(font=dict(size=16), title='')

    return title, cancer_sites, age_range_out, gender_out, state_out[0][0], fig, total_big_ret, mostMun, mustMunCases, titleChart, chart, styleButton, data
 

#download callback
@app.callback(
    Output("download-dataframe-states", "data"),
    [Input("btn_xlxs_state", "n_clicks"), Input('memory-output-state', 'data')],prevent_initial_call=True)

def DownloadBtn(btn_xlxs, data):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if data is None:
        raise PreventUpdate
    else:
        dff = pd.DataFrame.from_dict(data, orient='index')
        if 'btn_xlxs' in changed_id:
            return dcc.send_data_frame(dff.to_csv, "mydf.csv")




@app.callback(
    [Output(component_id='title_chart_comp', component_property='children'),
            Output('chart_comp', 'figure')],
    [Input(component_id='year_slider_states', component_property='value'),
    Input(component_id='state_dropdown', component_property='value'),
    Input(component_id='indicator-checklist-states', component_property='value')])

def compChart(year, state, indicator):
    title = f"Year Count of total {DataDictionaries.getIndic(indicator)} Cases: {DataDictionaries.getStateKey(state)[0][0]}"
    comp = DataDictionariesStates.generate_report_resid(year, state, indicator)
    comp = comp.sort_values('unique_values')
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=month, y=comp['counts'], mode='lines+markers',line=dict(color='crimson', width=4),marker=dict(color='orange',size=10,line=dict(color='black',width=2))))
    fig.update_layout(title='',xaxis_title='Month',yaxis_title=f'{DataDictionaries.getIndic(indicator)}')
    fig.update_layout(margin={"r":0,"t":5,"l":0,"b":0},height=450,paper_bgcolor="#1A1A1A",font_color="white",plot_bgcolor = '#1A1A1A',font_size=16,title='')

    return title, fig
    