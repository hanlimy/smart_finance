import pandas as pd
import time

from dash import Dash, dash_table, html, dcc, Input, Output, State, ctx
import plotly.express as px

dcc.Markdown('''
    # This is a heading
    This is some **bold** text.
''', style={'font-family': 'Verdana'})

df_iris = px.data.iris()
list_col_iris = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

list_file_mat = ['gold', 'silver', 'oil']
box_df_material = dict()
for mat in list_file_mat:
    box_df_material[mat] = pd.read_csv('collector/output_data/df_{}.csv'.format(mat))
df_copper = pd.read_csv('collector/output_data/df_copper.csv')

df_study = pd.read_csv('loc_flash/output_data/df_study.csv')
df_study_agg = pd.read_csv('loc_flash/output_data/df_study_agg2.csv')
list_col_step = [step for step in df_study.columns if step not in ['lot_wf', 'et', 'chip_x_pos', 'chip_y_pos']]

list_info_line = ['LLLA', 'LLLB', 'LLLC']
list_info_proc = ['PPPA', 'PPPB', 'PPPC']
list_info_lot = sorted(set([str(lot_wf).split('_')[0] for lot_wf in df_study['lot_wf']]))
list_info_wf = ['0' + str(wf) if wf < 10 else wf for wf in range(1, 25)]


########################################################################################################################

app = Dash(__name__)
app.config.suppress_callback_exceptions = True

style_tab = {'height': 20, 'width': 100}
style_btn = {'height': 20, 'width': 100, 'display': 'inline-block'}
style_txt_blue14 = {'color': 'blue', 'fontSize': 14}

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(
            label='prediction', value='tab1',
            style={'width': '20%', 'height': '50px', 'border': '1px solid', 'font_family': 'AppleGothic'},
            selected_style={'width': '20%', 'height': '50px', 'border': '1px solid', 'font_family': 'AppleGothic'},
        ),
        dcc.Tab(
            label='analysis', value='tab2',
            style={'width': '20%', 'height': '50px', 'border': '1px solid', 'font_family': 'AppleGothic'},
            selected_style={'width': '20%', 'height': '50px', 'border': '1px solid', 'font_family': 'AppleGothic'},
        ),
    ], style={'margin-left': '10px'}),

    html.Div(id='tabs_content')
])


@app.callback(
    Output('tabs_content', 'children'),
    [Input('tabs', 'value')]
)
def make_tabs_content(tab):
    print('-' * 100 + '\n[INIT] make_tabs_content : ', tab)
    if tab == 'tab1':
        return tab1
    elif tab == 'tab2':
        return tab2


########################################################################################################################

tab1_box1_btns = html.Div([
    html.Div([
        html.H5('라인', style={'color': 'red', 'font_family': 'Malgun Gothic'}),
        dcc.Dropdown(
            id='tab1_box1_ddn1', options=list_info_line, value=list_info_line[0],
            placeholder='select...', style={'height': '20px', 'width': '140px'}
        ),
    ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
    html.Div([
        html.H5('디스플레이', style={'color': 'A0A0A0', 'font_family': 'Malgun Gothic'}),
        dcc.Dropdown(
            id='tab1_box1_ddn2', options=list_info_line, value=list_info_line[0],
            placeholder='select...', style={'height': '20px', 'width': '140px'}
        ),
    ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),

    html.Div([
        html.Button(
            'dataload', id='tab1_box1_btn1_loaddata', n_clicks=0,
            style={'height': '20px', 'width': '140px'}
        ),
    ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
    html.Div([
        html.Button(
            'savedata', id='tab1_box1_btn2_savedata', n_clicks=0,
            style={'height': '20px', 'width': '140px'}
        ),
    ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
    html.Div([
        html.Button(
            'predict', id='tab1_box1_btn3_predict', n_clicks=0,
            style={'height': '20px', 'width': '140px'}
        ),
    ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
], style={'position': 'relative'})

tab1_box1 = html.Div([

    dcc.Store(id='tab1_box1_data'),

    html.Div([
        dash_table.DataTable(
            id='tab1_box1_table1',
            columns=[{'name': idx, 'id': idx, 'deletable': True} for idx in df_copper.columns],
            data=None,
            editable=True,

            filter_action='native',
            sort_action='native',
            sort_mode='multi',
            # sort_by=['Date']

            page_size=20,
            fixed_columns={'headers': True, 'data': 1},
            # fixed_rows={'headers': True, 'data': 1},
            style_table={
                # 'overlflowX': 'scroll',
                'minWidth': '600px', 'width': '700px', 'maxWidth': '700px',
            },
            style_cell={
                'height': '90',
                # all three widths are needed
                'minWidth': '40px', 'width': '60px', 'maxWidth': '100px',
                # 'whiteSpace': 'normal',
                # 'textOverflow': 'ellipsis',
            }

        ),
    ], style={
        'display': 'inline-block', 'margin-top': '20px',
        'verticalAlign': 'top',
    }),

    html.Div([
        dash_table.DataTable(
            id='tab1_box1_table2',
            columns=[{'name': idx, 'id': idx, 'deletable': True} for idx in df_copper.columns],
            data=None,

            filter_action='native',
            sort_action='native',
            sort_mode='multi',
            # sort_by=['Date']

            page_size=20,
            fixed_columns={'headers': True, 'data': 1},
            # fixed_rows={'headers': True, 'data': 1},
            style_table={
                # 'overlflowX': 'scroll',
                'minWidth': '600px', 'width': '700px', 'maxWidth': '700px',
            },
            style_cell={
                'height': '90',
                # all three widths are needed
                'minWidth': '40px', 'width': '60px', 'maxWidth': '100px',
                # 'whiteSpace': 'normal',
                # 'textOverflow': 'ellipsis',
            }

        ),
    ], style={
        'display': 'inline-block', 'margin-top': '20px', 'margin-left': '20px',
        'verticalAlign': 'top',
    }),
])

tab1 = html.Div([
    html.Div([
        tab1_box1_btns,
        html.Br(),

        tab1_box1,
    ], style={
        'border': '1px solid', 'padding': '10px',
        'margin-left': '10px', 'margin-right': '10px', 'margin-bottom': '10px'

    })
])


@app.callback(
    Output('tab1_box1_table1', 'data'),
    Input('tab1_box1_btn1_loaddata', 'n_clicks'),
)
def make_tab1_box1_table1(btn):
    print('[INIT] make_tab1_box1_table1 : ', btn, ctx.triggered_id)
    if ctx.triggered_id == 'tab1_box1_btn1_loaddata':
        print(' > [IF] tab1_box1_btn1_loaddata : ', btn, ctx.triggered_id)
        dict_data = df_copper.to_dict('records')
    else:
        dict_data = None

    return dict_data


@app.callback(
    Output('tab1_box1_data', 'data'),
    Input('tab1_box1_btn2_savedata', 'n_clicks'),
    State('tab1_box1_table1', 'data'),
)
def make_tab1_box1_data(btn, dict_data):
    print('[INIT] make_tab1_box1_data : ', btn, ctx.triggered_id)
    if ctx.triggered_id == 'tab1_box1_btn2_savedata':
        print(' > [IF] tab1_box1_btn2_savedata : ', btn, ctx.triggered_id)
        print(dict_data)
    else:
        dict_data = None

    return dict_data


@app.callback(
    Output('tab1_box1_table2', 'data'),
    Input('tab1_box1_btn3_predict', 'n_clicks'),
    State('tab1_box1_data', 'data'),
)
def make_tab1_box1_table2(btn, dict_data):
    print('[INIT] make_tab1_box1_table2 : ', btn, ctx.triggered_id)
    if ctx.triggered_id == 'tab1_box1_btn3_predict':
        print(' > [IF] tab1_box1_btn3_predict : ', btn, type(dict_data))
        print(dict_data)
        df_data = pd.DataFrame(dict_data)
        print(df_data)
    else:
        dict_data = None

    return dict_data


########################################################################################################################

tab2 = html.Div([
    html.H1('trace : top vs bottom wf'),
])


########################################################################################################################

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8082)
