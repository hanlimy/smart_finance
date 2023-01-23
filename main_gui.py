import pandas as pd
import time

from dash import Dash, dash_table, html, dcc, Input, Output, State, ctx
import plotly.express as px

df_copper = pd.read_csv('collector/output_data/df_copper.csv')
df_study = pd.read_csv('loc_flash/output_data/df_study.csv')
df_study_agg = pd.read_csv('loc_flash/output_data/df_study_agg2.csv')

list_info_line = ['LLLA', 'LLLB', 'LLLC']
list_info_proc = ['PPPA', 'PPPB', 'PPPC']


########################################################################################################################

app = Dash(__name__)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(
            label='Prediction', value='tab1',
            style={'width': '140px', 'height': '30px', 'border': '1px solid', 'font_family': 'AppleGothic'},
            selected_style={'width': '140px', 'height': '30px', 'border': '1px solid', 'font_family': 'AppleGothic'},
        ),
        dcc.Tab(
            label='Analysis', value='tab2',
            style={'width': '140px', 'height': '30px', 'border': '1px solid', 'font_family': 'AppleGothic'},
            selected_style={'width': '140px', 'height': '30px', 'border': '1px solid', 'font_family': 'AppleGothic'},
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
        html.Div('line', style={'color': 'black', 'fontSize': 14, 'font_family': 'Malgun Gothic'}),
        dcc.Dropdown(
            id='tab1_box1_ddn1', options=list_info_line, value=list_info_line[0],
            style={'height': '40px', 'width': '140px'})
    ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
    html.Div([
        html.Div('proc', style={'color': 'black', 'fontSize': 14, 'font_family': 'Malgun Gothic'}),
        dcc.Dropdown(
            id='tab1_box1_ddn2', options=list_info_line, value=list_info_line[0],
            style={'height': '40px', 'width': '140px'}),
    ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),

    html.Div([
        html.Button(
            'Load Data', id='tab1_box1_btn1_loaddata', n_clicks=0,
            style={'height': '40px', 'width': '140px'}
        )
    ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
    html.Div([
        html.Button(
            'Save Data', id='tab1_box1_btn2_savedata', n_clicks=0,
            style={'height': '40px', 'width': '140px'}
        ),
    ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
    html.Div([
        html.Button(
            'Show Predict', id='tab1_box1_btn3_predict', n_clicks=0,
            style={'height': '40px', 'width': '140px'}
        ),
    ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
])

tab1_box1 = html.Div([

    dcc.Store(id='tab1_box1_data'),

    html.Div([
        dash_table.DataTable(
            id='tab1_box1_table1',
            columns=[{'name': idx, 'id': idx, 'deletable': False} for idx in df_copper.columns],
            data=None,
            editable=True,

            filter_action='native',
            sort_action='native',
            sort_mode='multi',
            # sort_by=['Date']

            # page_size=20,
            # fixed_columns={'headers': True, 'data': 1},
            fixed_rows={'headers': True, 'data': 0},

            style_table={
                'overlflowX': 'scroll',
                'minHeight': '700px', 'height': '700px', 'maxHeight': '700px',
                'minWidth': '700px', 'width': '700px', 'maxWidth': '700px',

            },
            style_cell={
                'height': '80',
                # all three widths are needed
                'minHeight': '30px', 'width': '30px', 'maxHeight': '30px',
                # 'whiteSpace': 'normal',
                # 'textOverflow': 'ellipsis',
                'font_family': 'Malgun Gothic', 'fontSize': 10,
            }

        ),
    ], style={
        'display': 'inline-block', 'verticalAlign': 'top',
    }),

    html.Div([
        dash_table.DataTable(
            id='tab1_box1_table2',
            columns=[{'name': idx, 'id': idx, 'deletable': False} for idx in df_copper.columns],
            data=None,

            filter_action='native',
            sort_action='native',
            sort_mode='multi',
            # sort_by=['Date']

            # page_size=20,
            # fixed_columns={'headers': True, 'data': 1},
            fixed_rows={'headers': True, 'data': 0},
            style_table={
                'overlflowX': 'scroll',
                'minHeight': '700px', 'height': '700px', 'maxHeight': '700px',
                'minWidth': '700px', 'width': '700px', 'maxWidth': '700px',
            },
            style_cell={
                'height': '80',
                # all three widths are needed
                'minHeight': '30px', 'width': '30px', 'maxHeight': '30px',
                # 'whiteSpace': 'normal',
                # 'textOverflow': 'ellipsis',
                'font_family': 'Malgun Gothic', 'fontSize': 10,
            }

        ),
    ], style={
        'display': 'inline-block', 'margin-left': '20px', 'verticalAlign': 'top',
    }),
])

tab1 = html.Div([
    html.Div([
        tab1_box1_btns,
        html.Br(),
        tab1_box1,
    ], style={
        'border': '1px solid', 'padding': '10px',
        'height': '780px',
        'margin-left': '10px', 'margin-right': '10px', 'margin-bottom': '10px'

    })
])


@app.callback(
    Output('tab1_box1_table1', 'data'),
    Input('tab1_box1_btn1_loaddata', 'n_clicks'),
)
def make_tab1_box1_table1(btn):
    print('[INIT] make_tab1_box1_table1 : ', btn, ctx.triggered_id)
    if btn != 0:
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
    if btn != 0:
        print(' > [IF] tab1_box1_btn2_savedata : ', btn, ctx.triggered_id)
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
    if btn != 0:
        print(' > [IF] tab1_box1_btn3_predict : ', btn, type(dict_data))
        df_data = pd.DataFrame(dict_data)

    else:
        dict_data = None

    return dict_data


########################################################################################################################

tab2 = html.Div([
    html.Div([
    ], style={
        'border': '1px solid', 'padding': '10px',
        'height': '780px',
        'margin-left': '10px', 'margin-right': '10px', 'margin-bottom': '10px'

    })
])


########################################################################################################################

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8082)
