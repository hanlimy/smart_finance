from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

df = px.data.iris()
fig = px.scatter(df, x="sepal_length", y="sepal_width", color="species")
app = Dash(__name__)

# app layout: using by html, dcc module
app.layout = html.Div(children=[

    # make HTML by Dash HTML Components module
    html.H1(children='headline 1'),
    html.Div(children='Div'),

    # ploty graph rendering by dash.core.component(dcc)
    dcc.Graph(id='graph1', figure=fig),
])

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=False, host='0.0.0.0', port=8888)





