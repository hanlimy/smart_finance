import pandas as pd

from dash import Dash, dash_table, html, dcc, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

df_iris = px.data.iris()
list_col_iris = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

list_file_mat = ['gold', 'silver', 'oil']
box_df_material = dict()
for mat in list_file_mat:
    box_df_material[mat] = pd.read_csv('smart_collector/output_data/df_{}.csv'.format(mat))
df_copper = pd.read_csv('smart_collector/output_data/df_copper.csv')

list_info_line = ['LLLA', 'LLLB', 'LLLC']
list_info_proc = ['PPPA', 'PPPB', 'PPPC']
list_info_lot = ['BZZ001', 'BZZ002', 'BZZ003']
list_info_wf = ['0' + str(wf) if wf < 10 else wf for wf in range(1, 25)]

########################################################################################################################

app = Dash(__name__)
app.config.suppress_callback_exceptions = True

style_tab = {'height': 20, 'width': 100}
style_ddn = {'width': 140, 'display': 'inline-block'}
style_btn = {'height': 20, 'width': 100, 'display': 'inline-block'}
style_txt_b14 = {'color': 'blue', 'fontSize': 14}
style_table = {'height': '600px', 'overflowX': 'scroll'}
style_cell = {'height': '90', 'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'whiteSpace': 'normal'},

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='prediction', value='tab1', style=style_tab, selected_style=style_tab),
        dcc.Tab(label='analysis', value='tab2', style=style_tab, selected_style=style_tab),
        dcc.Tab(label='ex_price1', value='tab3', style=style_tab, selected_style=style_tab),
        dcc.Tab(label='ex_price2', value='tab4', style=style_tab, selected_style=style_tab),
        dcc.Tab(label='ex_iris', value='tab5', style=style_tab, selected_style=style_tab),
    ]),
    html.Div(id='tabs_content')
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
    elif tab == 'tab3':
        return tab3
    elif tab == 'tab4':
        return tab4
    elif tab == 'tab5':
        return tab5


########################################################################################################################


tab1_box1_dnns = html.Div([
    html.Div([
        html.H1('line', style=style_txt_b14),
        dcc.Dropdown(id='tab1_box1_ddn1', options=list_info_line, value=list_info_line[0], placeholder='select...'),
    ], style=style_ddn),
    html.Div([
        html.H1('Proc', style=style_txt_b14),
        dcc.Dropdown(id='tab1_box1_ddn2', options=list_info_wf, value=list_info_wf[0], placeholder='select...'),
    ], style=style_ddn),
    html.Div([
        html.H1('lot_target', style=style_txt_b14),
        dcc.Dropdown(id='tab1_box1_ddn3', options=list_info_lot, value=list_info_lot[0], placeholder='select...'),
    ], style=style_ddn),
    html.Div([
        html.H1('wf_target', style=style_txt_b14),
        dcc.Dropdown(id='tab1_box1_ddn4', options=list_info_wf, value=list_info_wf[0], placeholder='select...'),
    ], style=style_ddn),
    html.Div([
        html.H1('lot_base', style=style_txt_b14),
        dcc.Dropdown(id='tab1_box1_ddn5', options=list_info_lot, value=list_info_lot[0], placeholder='select...'),
    ], style=style_ddn),
    html.Div([
        html.H1('wf_base', style=style_txt_b14),
        dcc.Dropdown(id='tab1_box1_ddn6', options=list_info_wf, value=list_info_wf[0], placeholder='select...'),
    ], style=style_ddn),
])

tab1_box1_table = html.Div([
    html.Button('show', id='tab1_box1_btn1', n_clicks=0, style=style_btn),
    dash_table.DataTable(
        id='tab1_box1_table',
        columns=[{'name': idx, 'id': idx, 'deletable': True} for idx in df_copper.columns],
        data=df_copper.to_dict('records'),
        style_table=style_table,
        style_cell=style_cell,
        # page_current=0,
        # page_size=1000,
        # page_action='custom',
        filter_action='native',
        # filter_query='',
        sort_action='native',
        sort_mode='multi',
        # sort_by=['Date']
    )
])

tab1 = html.Div([
    html.Div([
        html.H1('prediction'),
        tab1_box1_dnns,
        html.Br(),
        tab1_box1_table,
    ])
])


@app.callback(
    Output('tab1_box1_table', 'children'),
    Input('tab1_box1_btn1', 'value'),
    [State('tab1_box1_ddn{}'.format(num), 'value') for num in range(1, 7)]
)
def action_update_graph(btn, dnn1, dnn2, dnn3, dnn4, dnn5, dnn6):

    return tab1_box1_table


########################################################################################################################

tab2_box1_dnns = html.Div([
    html.Div([
        html.H1('line', style=style_txt_b14),
        dcc.Dropdown(id='tab2_box1_ddn1', options=list_info_line, value=list_info_line[0], placeholder='select...'),
    ], style=style_ddn),
    html.Div([
        html.H1('Proc', style=style_txt_b14),
        dcc.Dropdown(id='tab2_box1_ddn2', options=list_info_wf, value=list_info_wf[0], placeholder='select...'),
    ], style=style_ddn),
    html.Div([
        html.H1('lot_target', style=style_txt_b14),
        dcc.Dropdown(id='tab2_box1_ddn3', options=list_info_lot, value=list_info_lot[0], placeholder='select...'),
    ], style=style_ddn),
    html.Div([
        html.H1('wf_target', style=style_txt_b14),
        dcc.Dropdown(id='tab2_box1_ddn4', options=list_info_wf, value=list_info_wf[0], placeholder='select...'),
    ], style=style_ddn),
    html.Div([
        html.H1('lot_base', style=style_txt_b14),
        dcc.Dropdown(id='tab2_box1_ddn5', options=list_info_lot, value=list_info_lot[0], placeholder='select...'),
    ], style=style_ddn),
    html.Div([
        html.H1('wf_base', style=style_txt_b14),
        dcc.Dropdown(id='tab2_box1_ddn6', options=list_info_wf, value=list_info_wf[0], placeholder='select...'),
    ], style=style_ddn),
])

tab2_box1 = html.Div([
    html.H1('analysis'),
    html.Div(id='tab2_box1_dnns', children=[tab2_box1_dnns]),
    html.Br(),
    html.Button('show', id='tab1_box1_btn1', n_clicks=0, style=style_btn),
    html.Br(),
    html.Div([tab1_box1_table])
])

tab2_box2 = html.Div([
    html.Button('show', id='tab2_box2_btn_show', n_clicks=0, style=style_btn),
    dcc.Graph(id='tab2_box2_graph')
])

tab2 = html.Div([
    html.H1('trace : top vs bottom wf'),
    tab2_box1,
    html.Br(),
    tab2_box2,
])


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


########################################################################################################################

tab3_box1 = html.Div([
    dcc.Dropdown(id='tab3_box1_ddn_material', options=list_file_mat, value=list_file_mat[0], placeholder='select...',
                 style=style_ddn),
    dcc.Graph(id='tab3_box1_graph')
])

tab3_box2 = html.Div([
    html.Button('show', id='tab3_box2_btn_show', n_clicks=0, style=style_btn),
    dcc.Graph(id='tab3_box2_graph')
])

tab3 = html.Div([
    html.H1('trace : top vs bottom wf'),
    tab3_box1,
    html.Br(),
    tab3_box2,
])


@app.callback(
    Output('tab3_box1_graph', 'figure'),
    Input('tab3_box1_ddn_material', 'value'),
)
def action_update_graph(material):
    val_x = 'Date'
    df_tmp = box_df_material[material]
    val_y = list(df_tmp.columns)
    fig = px.line(df_tmp, x=val_x, y=val_y, width=1000, height=700)
    fig.update_layout(title_text=material, title_font_size=30)
    return fig


@app.callback(
    Output('tab3_box2_graph', 'figure'),
    Input('tab3_box2_btn_show', 'n_clicks'),
)
def action_update_graph(btn):
    val_x = 'Date'
    val_y = list(df_copper.columns)
    fig = px.line(df_copper, x=val_x, y=val_y, width=1000, height=700)
    fig.update_layout(title_text='copper', title_font_size=30)
    return fig


########################################################################################################################

tab4_box1 = html.Div([
    dcc.Dropdown(id='tab4_box1_ddn_material', options=list_file_mat, value=list_file_mat[0], placeholder='select...',
                 style=style_ddn),
    dcc.Graph(id='tab4_box1_graph')
])

tab4_box2 = html.Div([
    html.Button('show', id='tab4_box2_btn_show', n_clicks=0, style=style_btn),
    dcc.Graph(id='tab4_box2_graph')
])

tab4 = html.Div([
    html.H1('trace : top vs bottom wf'),
    tab4_box1,
    html.Br(),
    tab4_box2,
])


@app.callback(
    Output('tab4_box1_graph', 'figure'),
    Input('tab4_box1_ddn_material', 'value'),
)
def action_update_graph(material):
    val_x = 'Date'
    df_tmp = box_df_material[material]
    val_y = list(df_tmp.columns)
    fig = px.line(df_tmp, x=val_x, y=val_y, width=1000, height=700)
    fig.update_layout(title_text=material, title_font_size=30)
    return fig


@app.callback(
    Output('tab4_box2_graph', 'figure'),
    Input('tab4_box2_btn_show', 'n_clicks'),
)
def action_update_graph(btn):
    val_x = 'Date'
    val_y = list(df_copper.columns)
    fig = px.line(df_copper, x=val_x, y=val_y, width=1000, height=700)
    fig.update_layout(title_text='copper', title_font_size=30)
    return fig


########################################################################################################################

tab5_box1 = html.Div([
    html.H1('iris : scatter plot for the iris data'),
    html.Div([
        html.H1('X-variable', style=style_txt_b14),
        dcc.Dropdown(id='tab5_box1_x', options=list_col_iris, value=list_col_iris[0], placeholder='Select X'),
    ], style=style_ddn),
    html.Div([
        html.H1('Y-variable', style=style_txt_b14),
        dcc.Dropdown(id='tab5_box1_y', options=list_col_iris, value=list_col_iris[1], placeholder='Select Y'),
    ], style=style_ddn)
])

tab5_box2 = html.Div([dcc.Graph(id='tab5_box2_graph')])

tab5 = html.Div([
    tab5_box1,
    html.Br(),
    tab5_box2,
])


@app.callback(
    Output('tab5_box2_graph', 'figure'),
    Input('tab5_box1_x', 'value'),
    Input('tab5_box1_y', 'value')
)
def action_update_graph(xvar, yvar):
    fig = px.scatter(df_iris, x=xvar, y=yvar, color='species', width=1000, height=700)
    fig.update_layout(title_text='Scatter plot of ' + xvar + ' vs ' + yvar, title_font_size=30)
    return fig


########################################################################################################################

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8888)
