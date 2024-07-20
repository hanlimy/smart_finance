from engine import make_stock_item_code

import pandas as pd

from dash import Dash, dash_table, html, dcc, Input, Output, State, ctx
import plotly.express as px
from datetime import datetime, date


def make_page(info_comm):
    print('-' * 100 + '\n[make_page]')

    if list(info_comm['item_code'].values())[0] is None:
        print(' > info_comm[code_stock_item] is Null... updating from files')
        info_comm = make_stock_item_code(info_comm)

    dict_df_src_item = dict()

    list_source = [src for src in info_comm['item_code'].keys()]
    print(' > list_source : {}'.format(list_source))

    for src in list_source:
        if src in ['Material']:
            continue

        df_index = pd.read_csv('{}/df_list_item_{}.csv'.format(info_comm['path_output'], src))
        df_src = pd.read_csv('{}/df_price_stock_{}.csv'.format(info_comm['path_output'], src))

        num_samples = 10
        list_item = df_index.loc[0:num_samples, 'Name'].values

        # print(' >> list_item : {}'.format(list_item))
        for item in list_item:
            # print('   >>> item : {}'.format(item))
            df_src_item = df_src[df_src['Item'] == item]
            dict_df_src_item.update({
                src + '_' + item: df_src_item
            })

    ####################################################################################################################

    app = Dash(__name__)
    app.config.suppress_callback_exceptions = True

    style_tab = {
        'height': '30px', 'width': '140px', 'border': '1px solid',
        'background': 'grey',
        # 'font_family': 'AppleGothic',
        'font-size': '14px', 'font-weight': 10, 'color': 'white', 'text-transform': 'uppercase',
        'align-items': 'center', 'justify-content': 'left',
    }
    style_tab_selected = {
        'height': '30px', 'width': '140px', 'border': '1px solid',
        # 'font_family': 'AppleGothic',
        'font-size': '14px', 'font-weight': 600, 'color': 'black', 'text-transform': 'uppercase',
        'align-items': 'center', 'justify-content': 'left',
    }

    app.layout = html.Div([
        dcc.Tabs(id='tabs', value=None, children=[
            dcc.Tab(label='compare', value='tab1', style=style_tab, selected_style=style_tab_selected),
            dcc.Tab(label='analysis', value='tab2', style=style_tab, selected_style=style_tab_selected, ),
        ], style={'margin-left': '10px'}),

        html.Div(id='tabs_content')
    ])

    @app.callback(
        Output('tabs_content', 'children'),
        [Input('tabs', 'value')]
    )
    def make_tabs_content(tab):
        print('-' * 100 + '\n[INIT] make_tabs_content : ', tab, ctx.triggered_id)
        if tab == 'tab1' and ctx.triggered_id == 'tabs':
            print(' > [IF] tabs : ', tab, ctx.triggered_id)
            return tab1
        elif tab == 'tab2' and ctx.triggered_id == 'tabs':
            print(' > [IF] tabs : ', tab, ctx.triggered_id)
            return tab2

    ####################################################################################################################

    tab1_area1 = html.Div([

        # tab1_area1_box1
        html.Div([
            html.Div('source', style={'color': 'black', 'fontSize': 14, 'font_family': 'Malgun Gothic'}),
            dcc.Dropdown(
                id='tab1_area1_ddn1_src', options=list_source, value=list_source[0],
                style={'height': '40px', 'width': '140px'})
        ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
        html.Div([
            html.Div('Item', style={'color': 'black', 'fontSize': 14, 'font_family': 'Malgun Gothic'}),
            html.Div(id='tab1_area1_ddn2_div'),
        ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
        html.Div([
            html.Button(
                'Load Data', id='tab1_area1_btn1_loaddata', n_clicks=0,
                style={'height': '40px', 'width': '80px'}
            )
        ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
        html.Div([
            html.Button(
                'Save Data', id='tab1_area1_btn2_savedata', n_clicks=0,
                style={'height': '40px', 'width': '80px'}
            ),
        ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
        html.Div([
            html.Div('column', style={'color': 'black', 'fontSize': 14, 'font_family': 'Malgun Gothic'}),
            html.Div(id='tab1_area1_ddn3_div'),
        ], style={'display': 'inline-block', 'verticalAlign': 'bottom', 'margin-left': '20px'}),

        # tab1_area1_box2
        html.Div([
            html.Div('source', style={'color': 'black', 'fontSize': 14, 'font_family': 'Malgun Gothic'}),
            dcc.Dropdown(
                id='tab1_area1_ddn4_src', options=list_source, value=list_source[0],
                style={'height': '40px', 'width': '140px'})
        ], style={'display': 'inline-block', 'verticalAlign': 'bottom', 'margin-left': '120px'}),
        html.Div([
            html.Div('Item', style={'color': 'black', 'fontSize': 14, 'font_family': 'Malgun Gothic'}),
            html.Div(id='tab1_area1_ddn5_div'),
        ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
        html.Div([
            html.Button(
                'Load Data', id='tab1_area1_btn3_loaddata', n_clicks=0,
                style={'height': '40px', 'width': '80px'}
            )
        ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
        html.Div([
            html.Button(
                'Save Data', id='tab1_area1_btn4_savedata', n_clicks=0,
                style={'height': '40px', 'width': '80px'}
            ),
        ], style={'display': 'inline-block', 'verticalAlign': 'bottom'}),
        html.Div([
            html.Div('column', style={'color': 'black', 'fontSize': 14, 'font_family': 'Malgun Gothic'}),
            html.Div(id='tab1_area1_ddn6_div'),
        ], style={'display': 'inline-block', 'verticalAlign': 'bottom', 'margin-left': '20px'}),
    ])

    # ---------------------------------------------------------------------------------------------------------------- #
    
    tab1 = html.Div([
        tab1_area1,

        # tab1_area2
        html.Div([
            html.Div(
                id='tab1_area2_div1', children=[],
                style={'display': 'inline-block', 'verticalAlign': 'top'}
            ),
            dcc.Store(id='tab1_area2_data_table1'),
            html.Div(
                id='tab1_area2_div2', children=[],
                style={'display': 'inline-block', 'verticalAlign': 'top', 'margin-left': '20px'}
            ),
            dcc.Store(id='tab1_area2_data_table2'),
        ]),

        html.Br(),

        # tab1_area3
        html.Div([
            dcc.DatePickerSingle(
                id='tab1_area3_date',
                min_date_allowed=date(2021, 1, 1),
                max_date_allowed=date(2023, 12, 31),
                initial_visible_month=date(2023, 1, 1),
                placeholder=datetime.now().strftime('%Y-%m-%d'),
                display_format='YYYY-MM-DD',
            ),
            html.Button(
                'Show Graph',
                id='tab1_area3_btn1_showgraph', n_clicks=0,
                style={'height': '40px', 'width': '80px'}
            ),
        ], style={'display': 'inline-block', 'verticalAlign': 'bottom', 'margin-top': '20px'}),

        # tab1_area4
        html.Div([
            html.Div([
                   dcc.Graph(
                       id='tab1_area4_graph1',
                       style={'height': '400px', 'width': '600px'})
                ], style={'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div([
                dcc.Graph(
                    id='tab1_area4_graph2',
                    style={'height': '400px', 'width': '600px'})
            ], style={'display': 'inline-block', 'verticalAlign': 'top'}),
        ]),

        # tab1_area5
        html.Div([
            html.Div([
                dcc.Graph(
                    id='tab1_area5_graph1',
                    style={'height': '400px', 'width': '600px'})
            ], style={'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div([
                dcc.Graph(
                    id='tab1_area5_graph2',
                    style={'height': '400px', 'width': '600px'})
            ], style={'display': 'inline-block', 'verticalAlign': 'top'}),
        ]),

    ], style={
        'border': '1px solid', 'padding': '10px',
        'margin-left': '10px', 'margin-right': '10px', 'margin-bottom': '10px',
    })

    # ---------------------------------------------------------------------------------------------------------------- #

    @app.callback(
        Output('tab1_area1_ddn2_div', 'children'),
        Input('tab1_area1_ddn1_src', 'value'),
    )
    def make_tab1_area1_ddn2_div(src):
        print('[INIT] make_tab1_area1_ddn2_div : ', src, ctx.triggered_id)
        if src is not None:
            print(' > [IF] tab1_area1_ddn1_src : ', src, ctx.triggered_id)

            list_item = list(info_comm['item_code'][src].keys())
            ddn = dcc.Dropdown(
                id='tab1_area1_ddn2_item', options=list_item, value=list_item[0],
                style={'height': '40px', 'width': '140px'}
            ),
        else:
            print(' > [ELSE] tab1_area1_ddn1_src : ', src, ctx.triggered_id)
            ddn = dcc.Dropdown(style={'height': '40px', 'width': '140px'}),

        return ddn

    @app.callback(
        Output('tab1_area2_div1', 'children'),
        Output('tab1_area1_ddn3_div', 'children'),
        Input('tab1_area1_btn1_loaddata', 'n_clicks'),
        State('tab1_area1_ddn1_src', 'value'),
        State('tab1_area1_ddn2_item', 'value'),
    )
    def make_tab1_area2_table1(btn, src, item):
        print('[INIT] make_tab1_area2_table1 : ', btn, ctx.triggered_id)

        if btn != 0 and ctx.triggered_id == 'tab1_area1_btn1_loaddata':
            print(' > [IF] tab1_area1_btn1_loaddata : ', btn, ctx.triggered_id)
            key = src + '_' + item
            data_table = dash_table.DataTable(
                id='tab1_area2_table1',
                columns=[{'name': idx, 'id': idx, 'deletable': False} for idx in dict_df_src_item[key].columns],
                data=dict_df_src_item[key].to_dict('records'),
                editable=True,

                fixed_rows={'headers': True, 'data': 0},
                filter_action='native',
                sort_action='native',
                sort_mode='multi',

                style_table={
                    'overlflowX': 'scroll',
                    'minHeight': '200px', 'height': '200px', 'maxHeight': '300px',
                    'minWidth': '700px', 'width': '700px', 'maxWidth': '700px',
                },
                style_cell={
                    'height': '80',
                    'minHeight': '30px', 'width': '30px', 'maxHeight': '30px',
                    'font_family': 'Malgun Gothic', 'fontSize': 10,
                }
            )
            print(' > data_table :', data_table)

            list_col = [col for col in dict_df_src_item[key].columns if col not in ['Item', 'Date']]
            ddn = dcc.Dropdown(
                id='tab1_area1_ddn3_col', options=list_col, value=list_col[0],
                style={'height': '40px', 'width': '140px'}
            ),

        else:
            print(' > [ELSE] tab1_area1_btn1_loaddata : ', btn, ctx.triggered_id)
            data_table = None
            ddn = dcc.Dropdown(style={'height': '40px', 'width': '140px'})

        return data_table, ddn

    @app.callback(
        Output('tab1_area1_ddn5_div', 'children'),
        Input('tab1_area1_ddn4_src', 'value'),
    )
    def make_tab1_area1_ddn5_div(src):
        print('[INIT] make_tab1_area1_ddn5_div : ', src, ctx.triggered_id)

        if src is not None:
            print(' > [IF] tab1_area1_ddn4_src : ', src, ctx.triggered_id)

            list_item = list(info_comm['item_code'][src].keys())
            ddn = dcc.Dropdown(
                id='tab1_area1_ddn5_item', options=list_item, value=list_item[0],
                style={'height': '40px', 'width': '140px'}
            ),
        else:
            print(' > [ELSE] tab1_area1_ddn4_src : ', src, ctx.triggered_id)

            ddn = dcc.Dropdown(style={'height': '40px', 'width': '140px'}),

        return ddn

    @app.callback(
        Output('tab1_area2_div2', 'children'),
        Output('tab1_area1_ddn6_div', 'children'),
        Input('tab1_area1_btn3_loaddata', 'n_clicks'),
        State('tab1_area1_ddn4_src', 'value'),
        State('tab1_area1_ddn5_item', 'value'),
    )
    def make_tab1_area2_table2(btn, src, item):
        print('[INIT] make_tab1_area2_table2 : ', btn, ctx.triggered_id)

        if btn != 0 and ctx.triggered_id == 'tab1_area1_btn3_loaddata':
            print(' > [IF] tab1_area1_btn3_loaddata : ', btn, ctx.triggered_id)
            key = src + '_' + item
            data_table = dash_table.DataTable(
                id='tab1_area2_table2',
                columns=[{'name': idx, 'id': idx, 'deletable': False} for idx in dict_df_src_item[key].columns],
                data=dict_df_src_item[key].to_dict('records'),
                editable=True,

                fixed_rows={'headers': True, 'data': 0},
                filter_action='native',
                sort_action='native',
                sort_mode='multi',

                style_table={
                    'overlflowX': 'scroll',
                    'minHeight': '200px', 'height': '200px', 'maxHeight': '300px',
                    'minWidth': '700px', 'width': '700px', 'maxWidth': '700px',
                },
                style_cell={
                    'height': '80',
                    'minHeight': '30px', 'width': '30px', 'maxHeight': '30px',
                    'font_family': 'Malgun Gothic', 'fontSize': 10,
                }
            )
            print(' > data_table :', data_table)

            list_col = [col for col in dict_df_src_item[key].columns if col not in ['Item', 'Date']]
            ddn = dcc.Dropdown(
                id='tab1_area1_ddn6_col', options=list_col, value=list_col[0],
                style={'height': '40px', 'width': '140px'}
            ),

        else:
            print(' > [ELSE] tab1_area1_btn3_loaddata : ', btn, ctx.triggered_id)

            data_table = None
            ddn = dcc.Dropdown(style={'height': '40px', 'width': '140px'})

        return data_table, ddn

    @app.callback(
        Output('tab1_area4_graph1', 'figure'),
        Output('tab1_area4_graph2', 'figure'),
        Output('tab1_area5_graph1', 'figure'),
        Output('tab1_area5_graph2', 'figure'),

        Input('tab1_area3_btn1_showgraph', 'n_clicks'),
        State('tab1_area1_ddn1_src', 'value'),
        State('tab1_area1_ddn2_item', 'value'),
        State('tab1_area1_ddn4_src', 'value'),
        State('tab1_area1_ddn5_item', 'value'),
        State('tab1_area3_date', 'date'),

        State('tab1_area2_table1', 'data'),
        State('tab1_area1_ddn3_col', 'value'),
        State('tab1_area2_table2', 'data'),
        State('tab1_area1_ddn6_col', 'value'),
    )
    def make_tab1_area45_graph(btn, src1, item1, src2, item2, date_target, dict_table1, col1, dict_table2, col2):
        print('[INIT] make_tab1_area45_graph : ', btn, ctx.triggered_id)
        if btn != 0 and ctx.triggered_id == 'tab1_area3_btn1_showgraph':
            print(' > [IF] tab1_area3_btn1_showgraph : ', btn, ctx.triggered_id)

            df_1 = pd.DataFrame(dict_table1).set_index('Date')
            df_2 = pd.DataFrame(dict_table2).set_index('Date')
            list_same_date = sorted(set(df_1.index) & set(df_2.index))
            df_1 = df_1.loc[list_same_date]
            df_2 = df_2.loc[list_same_date]

            # graph 1
            df_comp_all = pd.DataFrame()
            for item in info_comm['item_code'][src1].keys():
                df_tmp = dict_df_src_item[src1+'_'+item].set_index('Date')
                base_num = df_tmp.loc[df_tmp.index[0], col1]
                df_tmp_tr = df_tmp[[col1]].apply(lambda x: x / base_num - 1)
                df_tmp_tr = df_tmp_tr.rename(columns={col1: item})
                if len(df_comp_all.columns) == 0:
                    df_comp_all = df_tmp_tr.copy()
                else:
                    df_comp_all = pd.merge(df_comp_all, df_tmp_tr, on='Date', how='outer')

            df_comp_all = df_comp_all.reset_index()
            lineplot_all = px.line(df_comp_all, x='Date', y=df_comp_all.columns, line_shape='spline', render_mode='svg')

            # graph 2 : treemap
            df_treemap = pd.DataFrame()
            print(' > graph 2 treemap | date_target : {}'.format(date_target))
            for item in info_comm['item_code'][src1].keys():
                df_tmp = dict_df_src_item[src1+'_'+item]
                df_tmp = df_tmp[df_tmp['Date'] == date_target]
                df_treemap = pd.concat([df_treemap, df_tmp], axis=0)

            treemap = px.treemap(
                df_treemap,
                path=[px.Constant(src1), 'Item'],
                values='Volume',
                # color='Close',
                # hover_data=['Change']
            )

            # graph 3: corr map
            df_sum = pd.merge(df_1.drop(columns=['Item']), df_2.drop(columns=['Item']), on='Date', how='inner')
            df_corr = df_sum.corr()
            heatmap = px.imshow(df_corr, color_continuous_scale='Blues', origin='lower')
            # fig = px.colors.sequential.swatches_continuous()

            # graph 4: line graph
            base_num_1 = df_1.loc[df_1.index[0], col1]
            df_1_tr = df_1[[col1]].apply(lambda x: x/base_num_1-1)
            base_num_2 = df_2.loc[df_2.index[0], col2]
            df_2_tr = df_2[[col2]].apply(lambda x: x/base_num_2-1)

            col1_new = src1 + '_' + item1 + '_' + col1
            col2_new = src2 + '_' + item2 + '_' + col2
            df_1_tr = df_1_tr.rename(columns={col1: col1_new})
            df_2_tr = df_2_tr.rename(columns={col2: col2_new})
            df_comp = pd.merge(df_1_tr, df_2_tr, on='Date', how='inner').reset_index()

            lineplot = px.line(df_comp, x='Date', y=df_comp.columns, line_shape='spline', render_mode='svg')

        else:
            print(' > [ELSE] tab1_area3_btn1_showgraph : ', btn, ctx.triggered_id)

            lineplot_all = None
            treemap = None
            heatmap = None
            lineplot = None

        return lineplot_all, treemap, heatmap, lineplot
    
    ####################################################################################################################

    tab2 = html.Div([
        html.Div([
        ], style={
            'border': '1px solid', 'padding': '10px',
            'height': '780px',
            'margin-left': '10px', 'margin-right': '10px', 'margin-bottom': '10px',
            # 'border-radius': '4px',
        })
    ])

    ####################################################################################################################

    app.run_server(debug=False, host='0.0.0.0', port=8080)
