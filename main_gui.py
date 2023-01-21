import pandas as pd
import time

from dash import Dash, dash_table, html, dcc, Input, Output, State, ctx
import plotly.express as px

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

list_tab_name = ['prediction', 'analysis']

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(
            label=list_tab_name[idx], value='tab'+str(idx+1),
            style={'width': '20%', 'border': '1px solid',  'font_family': 'cursive',},
            selected_style={'width': '20%', 'border': '1px solid', 'font_family': 'cursive',},

        ) for idx in range(0, len(list_tab_name))
    ], style={'margin-left': '10px'}),

    html.Div(id='tabs_content')
])


@app.callback(
    Output('tabs_content', 'children'),
    [Input('tabs', 'value')]
)
def make_tabs_content(tab):
    print('[INIT] make_tabs_content : ', tab)
    if tab == 'tab1':
        return tab1
    # elif tab == 'tab2':
    #     return tab2


########################################################################################################################

tab1_box1_btns = html.Div([
    html.Div([
        html.H5('line', style={'color': 'red'}),
        dcc.Dropdown(
            id='tab1_box1_ddn1', options=list_info_line, value=list_info_line[0],
            placeholder='select...', style={'height': '20px', 'width': '140px'}
        ),
    ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
    html.Div([
        html.H5('proc', style={'color': 'A0A0A0'}),
        dcc.Dropdown(
            id='tab1_box1_ddn2', options=list_info_line, value=list_info_line[0],
            placeholder='select...', style={'height': '20px', 'width': '140px'}
        ),
    ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),

    html.Div([
        html.Button(
            'dataload', id='tab1_box1_btn1_dataload', n_clicks=0,
            style={'height': '20px', 'width': '140px'}
        ),
    ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
    html.Div([
        html.Button(
            'predict', id='tab1_box1_btn2_predict', n_clicks=0,
            style={'height': '20px', 'width': '140px'}
        ),
    ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
], style={'position': 'relative'})

tab1_box1 = html.Div([
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
                'minWidth': '600px', 'width': '600px', 'maxWidth': '600px',
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
                'minWidth': '600px', 'width': '600px', 'maxWidth': '600px',
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
        html.Div(id='tab1_box1_data'),
        tab1_box1,
    ], style={
        'border': '1px solid', 'padding': '10px',
        'margin-left': '10px', 'margin-right': '10px', 'margin-bottom': '10px'

    })
])


@app.callback(
    Output('tab1_box1_table1', 'data'),
    Output('tab1_box1_data', 'children'),
    Input('tab1_box1_btn1_dataload', 'n_clicks'),
)
def make_tab1_box1_table1(btn):
    print('[INIT] make_tab1_box1_table1 : ', btn)
    if ctx.triggered_id == 'tab1_box1_btn1_dataload':
        print(' > [IF] tab1_box1_btn1_dataload')

        df_copper = pd.read_csv('collector/output_data/df_copper.csv')
        dict_data = df_copper.to_dict('records')
        print(dict_data)

    else:
        dict_data = None

    return dict_data, dict_data


@app.callback(
    Output('tab1_box1_table2', 'data'),
    Input('tab1_box1_btn2_predict', 'n_clicks'),
    State('tab1_box1_data', 'children'),
)
def make_tab1_box1_table2(btn, dict_data):
    print('[INIT] make_tab1_box1_table2 : ', btn, type(dict_data))
    if ctx.triggered_id == 'tab1_box1_btn2_predict':
        print(' > [IF] tab1_box1_btn2_predict : ', btn, type(dict_data))
        print(dict_data)
    else:
        dict_data = None

    return dict_data


########################################################################################################################

# tab2_box1_table1 = html.Div([
#     html.Button('show', id='tab2_box1_btn1', n_clicks=0, style=style_btn),
#     dash_table.DataTable(
#         id='tab1_box1_table1',
#         data=df_study.to_dict('records'),
#         columns=[{'name': idx, 'id': idx, 'deletable': True} for idx in df_study.columns],
#         filter_action='native',  # 'native', 'custom'
#         # filter_query='',
#         sort_action='native',  # 'native', 'custom'
#         sort_mode='multi',
#         # sort_by=['Date']
#         row_deletable=False,
#         # page_current=0,
#         # page_size=1000,
#         page_action='native',   # 'native', 'custom'
#         style_table=style_table,
#         style_cell=style_cell,
#     )
# ])
#
# tab2_box1_dnns = html.Div([
#     html.Div([
#         html.H1('line', style=style_txt_blue14),
#         dcc.Dropdown(id='tab2_box1_ddn1', options=list_info_line, value=list_info_line[0], placeholder='select...'),
#     ], style=style_ddn),
#     html.Div([
#         html.H1('Proc', style=style_txt_blue14),
#         dcc.Dropdown(id='tab2_box1_ddn2', options=list_info_proc, value=list_info_proc[0], placeholder='select...'),
#     ], style=style_ddn),
#     html.Div([
#         html.H1('lot_target', style=style_txt_blue14),
#         dcc.Dropdown(id='tab2_box1_ddn3', options=list_info_lot, value=list_info_lot[0], placeholder='select...'),
#     ], style=style_ddn),
#     html.Div([
#         html.H1('wf_target', style=style_txt_blue14),
#         dcc.Dropdown(id='tab2_box1_ddn4', options=list_info_wf, value=list_info_wf[0], placeholder='select...'),
#     ], style=style_ddn),
#     html.Div([
#         html.H1('lot_base', style=style_txt_blue14),
#         dcc.Dropdown(id='tab2_box1_ddn5', options=list_info_lot, value=list_info_lot[0], placeholder='select...'),
#     ], style=style_ddn),
#     html.Div([
#         html.H1('wf_base', style=style_txt_blue14),
#         dcc.Dropdown(id='tab2_box1_ddn6', options=list_info_wf, value=list_info_wf[0], placeholder='select...'),
#     ], style=style_ddn),
# ])

# tab2_box1_table2 = html.Div([
#     html.Button('show', id='tab2_box1_btn2', n_clicks=0, style=style_btn),
#     dash_table.DataTable(
#         id='tab2_box1_table2',
#         data=None,
#         columns=[{'name': idx, 'id': idx, 'deletable': True} for idx in df_study.columns],
#         editable=True,
#
#         filter_action='native',  # 'native', 'custom'
#         # filter_query='',
#         sort_action='native',  # 'native', 'custom'
#         sort_mode='multi',
#         # sort_by=['Date']
#         row_deletable=False,
#         # page_current=0,
#         # page_size=1000,
#         page_action='native',   # 'native', 'custom'
#         style_table=style_table,
#         style_cell=style_cell,
#     )
# ])
#
# tab2_box2 = html.Div([
#     html.Div([
#         html.H1('stepseq', style=style_txt_blue14),
#         dcc.Dropdown(id='tab2_box2_ddn', options=list_col_step, value=list_col_step[0], placeholder='select...'),
#     ], style=style_ddn),
#     html.Button('show', id='tab2_box2_btn1', n_clicks=0, style=style_btn),
#     dcc.Graph(id='tab2_box2_graph1'),
#     dcc.Graph(id='tab2_box2_graph2'),
# ])
#
# tab2 = html.Div([
#     html.H1('trace : top vs bottom wf'),
#     tab2_box1_table1,
#     tab2_box1_dnns,
#     tab2_box1_table2,
#     html.Br(),
#     tab2_box2,
# ])
#
#
# @app.callback(
#     Output('tab2_box1_table2', 'data'),
#     Input('tab2_box1_btn2', 'n_clicks'),
#     [State('tab2_box1_ddn{}'.format(num), 'value') for num in range(1, 7)]
# )
# def action(btn, dnn1, dnn2, dnn3, dnn4, dnn5, dnn6):
#     print('[RUN] action:', btn, dnn1, dnn2, dnn3, dnn4, dnn5, dnn6)
#
#     if btn == 0:
#         df_result = pd.DataFrame(columns=df_study.columns).to_dict('records')
#     else:
#         df_tmp = df_study.set_index('lot_wf')
#         lot_wf_end = str(dnn3) + '_' + str(dnn4)
#         lot_wf_start = str(dnn5) + '_' + str(dnn6)
#         df_end = df_tmp.loc[[lot_wf_end], :].reset_index()
#         df_start = df_tmp.loc[[lot_wf_start], :].reset_index()
#
#         df_diff = df_start.eq(df_end).drop(columns=['lot_wf', 'chip_x_pos', 'chip_y_pos', 'et']).T.reset_index()
#         df_diff = df_diff[df_diff[0] == False]
#         list_idx_diff = sorted(df_diff.index)
#
#         df_trace = pd.DataFrame(columns=df_tmp.columns).reset_index()
#         for _ in range(0, len(list_idx_diff)+1):
#             df_trace = pd.concat([df_trace, df_start], axis=0)
#
#         idx_row = 1
#         idx_start = 0
#         for idx_end in list_idx_diff:
#             df_trace.iloc[idx_row, idx_start:idx_end] = df_end.iloc[0, idx_start:idx_end]
#             idx_start = idx_end
#             idx_row += 1
#
#         df_result = df_trace.reset_index().to_dict('records')
#
#     return df_result
#
#
# @app.callback(
#     Output('tab2_box2_graph1', 'figure'),
#     Output('tab2_box2_graph2', 'figure'),
#     Input('tab2_box2_btn1', 'n_clicks'),
#     State('tab2_box2_ddn', 'value'),
# )
# def action(btn, step):
#     print('[RUN] action:', btn, step)
#
#     fig1 = px.scatter(
#         df_study,
#         x=step, y='et',
#         hover_name=None, log_x=False, size_max=None,
#         width=800, height=400
#     )
#
#     df_study_tmp = df_study[['chip_x_pos', 'chip_y_pos', step, 'et']]
#     df_study_tmp = df_study_tmp.groupby(['chip_x_pos', 'chip_y_pos', step]).agg({'et': ['median', 'count']})
#     df_study_tmp.to_csv('loc_flash/output_data/df_study_agg1.csv')
#     df_study_tmp.columns = ['et_med', 'et_cnt']
#     df_study_tmp = df_study_tmp.reset_index()
#     df_study_tmp.to_csv('loc_flash/output_data/df_study_agg2.csv')
#
#     fig2 = px.scatter(
#         df_study_tmp,
#         x='chip_x_pos', y='chip_y_pos', size='et_cnt', color='et_med',
#         hover_name=None, log_x=False, size_max=None,
#         labels={step: 'cnt_sample'},
#         width=800, height=400
#     )
#
#     return fig1, fig2


########################################################################################################################

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8082)
