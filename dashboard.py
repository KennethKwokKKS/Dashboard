import dash
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
import dash_table
from datetime import datetime
import pandas as pd

from functions import historical

# APPLICATION DEFINITION
app = dash.Dash()

# LAYOUT
app.layout = html.Div([

    # SECTION 1
    html.Div([
        # TITLE
        html.Div([
            html.Div([
                html.Img(src=app.get_asset_url('logo-1.jpg'),
                         id='corona-image',
                         style={
                         "height": "60px",
                         "width": "auto",
                         "margin-bottom": "25px",
                         "border": "0px",
                         "border-radius": "15px"
                         },
                         )
            ],
                className="one-third column",
            ),
            html.Div([
                html.Div([
                    html.H3("Cryptocurrency",
                            style={"margin-bottom": "0px", 'color': 'white', 'font': "30px"}),
                    html.H5(" Market Movements",
                            style={"margin-top": "0px", 'color': '#33c3f0'}),
                ])
            ], className="one-half column", id="title"),

            html.Div([
                html.H6('Last Updated: ' + str((datetime.today().date()).strftime("%B %d, %Y")) + '  00:01 (UTC)',
                        style={'color': 'orange'}),

            ], className="one-third column", id='title1'),

        ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),




        # COIN SELECTION
        html.Div([
            dcc.Dropdown(
                id='coin_symbol',
                options=[
                 {'label': 'Bitcoin', 'value': 'bitcoin'},
                 {'label': 'Ethereum', 'value': 'ethereum'},
                 {'label': 'Cardano', 'value': 'cardano'},
                 {'label': 'Uniswap', 'value': 'uniswap'}],
                value='bitcoin',
                multi=False)
        ]),
        # DATE SELECTION
        html.Div([
            dcc.DatePickerRange(id='my_date_picker',
                                min_date_allowed=str(
                                    datetime(2012, 1, 1).date()),
                                max_date_allowed=str(
                                    datetime.today().date()),
                                start_date=str(
                                    datetime(2020, 10, 12).date()),
                                end_date=str(datetime.today().date())
                                )
        ])
    ], style={}),



    # SECTION 2
    html.Div([
        # TIMESERIES PLOTTING
        html.Div([
            dcc.Graph(figure={},
                      id='timeseries1',
                      )
        ], style={'margin': '0%',
                  'padding': '1%',
                  'width': '100%',
                  'height': '100%',
                  'display': 'inline-block'}),
        # HISTOGRAM PRICE CHANGE PLOTTING
        html.Div([
            dcc.Graph(figure={},
                      id='histogram1',
                      )
        ], style={'margin': '0%',
                  'padding': '1%',
                  'width': '31%',
                  'height': '100%',
                  'display': 'inline-block'}),

        # HISTOGRAM VOLUME CHANGE PLOTTING
        html.Div([
            dcc.Graph(figure={},
                      id='histogram2',
                      )
        ], style={'margin': '0%',
                  'padding': '1%',
                  'width': '31%',
                  'height': '100%',
                  'display': 'inline-block'}),

        # VOLUME PRICE CORRELATION
        html.Div([
            dcc.Graph(figure={},
                      id='scatter1',
                      )
        ], style={'margin': '0%',
                  'padding': '1%',
                  'width': '31%',
                  'height': '100%',
                  'display': 'inline-block'}),

    ])



])

# TIMESERIES


@ app.callback(
    Output('timeseries1', 'figure'),
    [Input('coin_symbol', 'value'),
     Input('my_date_picker', 'start_date'),
     Input('my_date_picker', 'end_date')])
def update_graph(value, start_date, end_date):

    df = historical(str(value), str(start_date), str(end_date))

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=df.index, y=df['usd'], name="USD"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df.index, y=df['volume'], name="Volume"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="<b>Price Volume</b> Timeseries"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="date")

    # Set y-axes titles
    fig.update_yaxes(title_text="USD", secondary_y=False)
    fig.update_yaxes(title_text="Volume", secondary_y=True)

    return fig

# PRICE CHANGE HISTOGRAM


@ app.callback(
    Output('histogram1', 'figure'),
    [Input('coin_symbol', 'value'),
     Input('my_date_picker', 'start_date'),
     Input('my_date_picker', 'end_date')])
def update_graph(value, start_date, end_date):

    df = historical(str(value), str(start_date), str(end_date))
    df = df.pct_change().dropna()

    fig = px.histogram(df, x=df['usd'])

    fig.update_layout(
        title_text="<b>Percentage Change Price</b> Histogram")

    return fig

# VOLUME CHANGE HISTOGRAM


@ app.callback(
    Output('histogram2', 'figure'),
    [Input('coin_symbol', 'value'),
     Input('my_date_picker', 'start_date'),
     Input('my_date_picker', 'end_date')])
def update_graph(value, start_date, end_date):

    df = historical(str(value), str(start_date), str(end_date))
    # df = df.pct_change().dropna()

    fig = px.histogram(df, x=df['year'])

    fig.update_layout(
        title_text="<b>Percentage Change Volume</b> Histogram")

    return fig


# VOLUME PRICE CORRELATION
@ app.callback(
    Output('scatter1', 'figure'),
    [Input('coin_symbol', 'value'),
     Input('my_date_picker', 'start_date'),
     Input('my_date_picker', 'end_date')])
def update_graph(value, start_date, end_date):

    df = historical(str(value), str(start_date), str(end_date))
    df['year'] = df.index.year

    fig = px.scatter(df, x="volume", y="usd", color="year",
                     size='market_cap')

    fig.update_layout(
        title_text="<b>Volume Price Correlation</b> Scatter")

    return fig


# SERVER START MODULE
if __name__ == '__main__':
    app.run_server(debug=False)
