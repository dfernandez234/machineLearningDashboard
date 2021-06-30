import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import nationalInfo, statesInfo, predictions


PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/nationalInfo':
        return nationalInfo.layout
    if pathname == '/apps/statesInfo':
        return statesInfo.layout
    if pathname == '/apps/predictions':
        return predictions.layout
    if pathname == '/':
        content = html.Div([
            dbc.NavbarSimple(
                brand="CancerStats",
                brand_href="#",
                color="#0f0f0f",
                dark=True,
            ),

            dbc.Jumbotron(
            [
                html.H1("About this Project", className="display-3"),
                html.P(children=["This project presents a data dashboard of Cancer data in Mexico ", html.Br(), "and display the results of applying Neural Networks for forecasting."],className="lead"),
                html.Hr(className="my-2"),

                html.P(children = ["Data Science in Mexico is slowly picking up on different industries, "
                       "unfortunately in Mexico all data related with Healthcare", 
                       html.Br(), "is distributed by the government and not very available for everybody. "]),
                
                html.P(children = ["This project compiles, analyzes and studies national cancer data in "
                        "Mexico to make it available with data visualization techniques. ", html.Br(), "And forecast cancer mortality rates using LSTM neural networks."]),

                html.Hr(className="my-2"),
                html.P(dbc.Button("Click Here to check the Dashboard. ", outline=True, color="danger", className="mr-1", href="/apps/nationalInfo"), className="lead"),
            ]),

            dbc.CardDeck(
            [
                dbc.Card(children=[
                    dbc.CardImg(src="https://lh3.googleusercontent.com/3rYo7s4NOX7meK7F3SVmCBqqdiPfThPGLxgLskzSoteNWnxy6w3gB18J8eSEk92atFeQ8W-GUNkxiRIqsBFGT5RLwNzWJVaFVsv4kAfNRxaoYsTBxs2VKU-Rgy5SIyRxgDM-ODkcYA=w2400", top=True),
                    dbc.CardBody(children=[
                            html.H5("What is Cancer?", className="card-title"),
                            html.P(
                                "Cancer is the name given to a collection of related diseases. "
                                "In all types of cancer, some of the body’s cells begin to divide without stopping and spread into surrounding tissues.",
                                className="card-text",
                            ),
                            html.P(
                                "Cancer is the second leading cause of death worldwide, in 2018 it accounted for an estimated 9.6 million deaths.",
                                className="card-text",
                            ),
                            dbc.Button("MORE", outline=True, color="danger", className="mr-1", href="https://www.cancer.gov/about-cancer/understanding/what-is-cancer"),
                        ]
                    )
                ]),
                dbc.Card(children=[
                    dbc.CardImg(src="https://lh3.googleusercontent.com/9TtcSguUzkcqMjOH01ncafornOVb_4D5PWG6Bs5PW7d9Tfo6M-P1opo0kWl5VHMl4DL_XnMze6ybrh1-pPyjocqZ9SIt2-xtHZRgFWR2id4Gk0Q5-cUvcDciSPvEsD7fpK397-cmGQ=w2400", top=True),
                    dbc.CardBody(children=[
                            html.H5("What is Data Analysis?", className="card-title"),
                            html.P(
                                "Data Analysis? It is a process of inspecting, cleansing, transforming, and modeling data so that we can "
                                "derive some useful information from the data and use it for future predictions.",
                                className="card-text",
                            ),
                            dbc.Button("MORE", outline=True, color="danger", className="mr-1", href="https://towardsdatascience.com/understanding-data-analysis-step-by-step-48e604cb882"),
                        ]
                    )
                ]),
                dbc.Card(children=[
                    dbc.CardImg(src="https://lh3.googleusercontent.com/vCBdE5lXuUyNQcGLSvxLe0iyT-noboht1TJjfnHSX61gOCi45s0drRUJobpKImxoN7qrRN-JE_3PIvruwta46-1MvoS4dRNxASpihGpH5XbrXXFqcd0SLtO0lSsXd1-1fhziMo_QgA=w2400", top=True),
                    dbc.CardBody(children=[
                            html.H5("Methodology.", className="card-title"),
                            html.P(
                                "Long Short-Term Memory (LSTM) networks are a type of recurrent neural network capable of learning order dependence in sequence prediction problems.",
                                className="card-text",
                            ),
                            dbc.Button("MORE", outline=True, color="danger", className="mr-1", href="https://towardsdatascience.com/illustrated-guide-to-lstms-and-gru-s-a-step-by-step-explanation-44e9eb85bf21"),
                        ]
                    )
                ]),

                html.Div(children=[
                    html.Ul(children=[
                        html.Li(children=[
                            html.P("👋", className="wavy")
                        ],className="WavyLi"),
                        html.Li(children=[
                            html.A("GitHub", href="#",className="footerLink")
                        ],className="footerLi"),
                        html.Li(children=[
                            html.A("David Fernandez", href="#",className="footerLink")
                        ],className="footerLi"),

                    ],className="footerUl")
                ], className = "c_footer")

            ])
        ], className="index_container")
        return content
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug = True)