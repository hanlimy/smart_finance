from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

df = px.data.iris()
list_col = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']


app = Dash(__name__)
app.config.suppress_callback_exceptions = True


style_tab = {'height': 20, 'width': 100}
style_dropdown = {'width': '20%', 'display': 'inline-block'}
style_txt_b14 = {'color': 'blue', 'fontSize': 14}

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='Tab 1', value='tab1', style=style_tab, selected_style=style_tab),
        dcc.Tab(label='Tab 2', value='tab2', style=style_tab, selected_style=style_tab),
    ]),
    html.Div(id='tabs_content')
])

tab1_box1 = html.Div([
    html.H1('callback practice : scatter plot for the iris data'),
    html.Div([
        html.H1('X-variable', style=style_txt_b14),
        dcc.Dropdown(id='tab1_box1_x', options=list_col, value=list_col[0], placeholder='Select X'),
    ], style=style_dropdown),
    html.Div([
        html.H1('Y-variable', style=style_txt_b14),
        dcc.Dropdown(id='tab1_box1_y', options=list_col, value=list_col[1], placeholder='Select Y'),
    ], style=style_dropdown)
])

tab1_box2 = html.Div([dcc.Graph(id='tab1_box2_graph')])

tab1_box3 = html.Div([
    html.Div('Example Div', style=style_txt_b14),
    html.P('Example P', className='my-class', id='my-p-element')
], style={'marginBottom': 50, 'marginTop': 25})

tab1 = html.Div([
    tab1_box1,
    html.Br(),
    html.Br(),
    tab1_box2,
    tab1_box3,
])


tab2 = html.H1('Tab 2 inside')


@app.callback(
    Output('tabs_content', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab1':
        return tab1
    elif tab == 'tab2':
        return tab2


@app.callback(
    Output('tab1_box2_graph', 'figure'),
    Input('tab1_box1_x', 'value'),
    Input('tab1_box1_y', 'value')
)
def action_update_graph(xvar, yvar):
    fig = px.scatter(df, x=xvar, y=yvar, color='species', width=1000, height=700)
    fig.update_layout(title_text='Scatter plot of ' + xvar + ' vs ' + yvar, title_font_size=30)
    return fig



# app.layout = html.Div(children=[
#     html.H1(children='callback practice : scatter plot for the iris data'),
#     html.Div([
#         'X-variable',
#         dcc.Dropdown(id='xvar_name', options=col_names, value=col_names[0], placeholder='Select X-axis col'),
#         ], style={'width': '30%', 'display': 'inline-block'}),
#     html.Div([
#         'Y-variable',
#         dcc.Dropdown(id='yvar_name', options=col_names, value=col_names[1], placeholder='Select Y-axis col'),
#         ], style={'width': '30%', 'display': 'inline-block'}),
#     html.Br(),
#     html.Br(),
#     html.Div([dcc.Graph(id='update_graph')])
# ])
#
#
# @app.callback(
#     Output('update_graph', 'figure'),
#     Input('xvar_name', 'value'),
#     Input('yvar_name', 'value')
# )
# def action_update_graph(xvar, yvar):
#     fig = px.scatter(df, x=xvar, y=yvar, color='species', width=1000, height=700)
#     fig.update_layout(title_text='Scatter plot of ' + xvar + ' vs ' + yvar, title_font_size=30)
#     return fig


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8888)
