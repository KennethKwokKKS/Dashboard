import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd



# use css outside
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


# go to __name__ to run the server
# call css 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    #json thing

    # buttom item and value
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],

    # left A,A,A O,O,O value
    "Amount": [4, 1, 2, 2, 4, 5],

    # right 
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

# positioning setting 
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")



fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)






app.layout = html.Div(children=[
    html.H1(
        children='Hello Crypyto Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
        
        ),       # name title // HTML element


        html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure=fig            # fig  = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    )
])



if __name__ == '__main__':
    app.run_server(debug=True)            
    ##   WARNING: This is a development server. Do not use it in a production deployment.
    ##   Use a production WSGI server instead.