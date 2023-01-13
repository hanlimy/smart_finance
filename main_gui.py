import pandas as pd

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go

df = px.data.iris()
list_col = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

list_mat = ['gold', 'silver', 'oil']

box_df_material = dict()
for mat in list_mat:
    box_df_material[mat] = pd.read_csv('smart_collector/output_data/df_{}.csv'.format(mat))

df_copper = pd.read_csv('smart_collector/output_data/df_copper.csv')

app = Dash(__name__)
app.config.suppress_callback_exceptions = True

style_tab = {'height': 20, 'width': 100}
style_ddn = {'width': '20%', 'display': 'inline-block'}
style_btn = {'hieght': 20, 'width': 10, 'display': 'inline-block'}
style_txt_b14 = {'color': 'blue', 'fontSize': 14}

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab2', children=[
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
    ], style=style_ddn),
    html.Div([
        html.H1('Y-variable', style=style_txt_b14),
        dcc.Dropdown(id='tab1_box1_y', options=list_col, value=list_col[1], placeholder='Select Y'),
    ], style=style_ddn)
])

tab1_box2 = html.Div([dcc.Graph(id='tab1_box2_graph')])

tab1 = html.Div([
    tab1_box1,
    html.Br(),
    tab1_box2,
])

tab2_box1 = html.Div([
    dcc.Dropdown(id='tab2_box1_ddn_material', options=list_mat, value=list_mat[0], placeholder='Select Material',
                 style=style_ddn),
    dcc.Graph(id='tab2_box1_graph')
])

tab2_box2 = html.Div([
    html.Button('show', id='tab2_box2_btn_show', n_clicks=0, style=style_btn),
    dcc.Graph(id='tab2_box2_graph')
])

tab2 = html.Div([
    html.H1('practice 2: price in 2021~2022'),
    tab2_box1,
    html.Br(),
    tab2_box2,
])


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


@app.callback(
    Output('tab2_box1_graph', 'figure'),
    Input('tab2_box1_ddn_material', 'value'),
)
def action_update_graph(material):
    val_x = 'Date'
    df_tmp = box_df_material[material]
    val_y = list(df_tmp.columns)
    fig = px.line(df_tmp, x=val_x, y=val_y, width=1000, height=700)
    fig.update_layout(title_text=material, title_font_size=30)
    return fig


@app.callback(
    Output('tab2_box2_graph', 'figure'),
    Input('tab2_box2_btn_show', 'n_clicks'),
)
def action_update_graph(btn):
    val_x = 'Date'
    val_y = list(df_copper.columns)
    fig = px.line(df_copper, x=val_x, y=val_y, width=1000, height=700)
    fig.update_layout(title_text='copper', title_font_size=30)
    return fig


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8888)
