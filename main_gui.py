from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

df = px.data.iris()
col_names = ['s_len', 's_wid', 'p_len', 'p_wid']
app = Dash(__name__)


app.layout = html.Div(children=[
    html.H1(children='callback practice'),
    html.Div([
        'X-var:',
        dcc.Dropdown(id='xvar_name', value=col_names[0], placeholder='Select X-axis col'),
        ], style={'width': '30%', 'display': 'inline-block'}),
    html.Div([
        'Y-var:',
        dcc.Dropdown(id='yvar_name', value=col_names[1], placeholder='Select X-axis col'),
        ], style={'width': '30%', 'display': 'inline-block'}),
    html.Br(),
    html.Br(),
    html.Div([dcc.Graph(id='update_graph')])
])


@app.callback(
    Output('update_graph', 'figure'),
    Input('xvar_name', 'value'),
    Input('yvar_name', 'value')
)
def action_update_graph(xvar, yvar):
    fig = px.scatter(df, x=xvar, y=yvar, color='species', width=1000, height=700)
    fig.update_layout(title_text='Scatter plot of ' + xvar + ' vs ' + yvar, title_font_size=30)
    return fig


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8888)
