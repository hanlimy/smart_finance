import pandas as pd

from dash import Dash, dash_table, html, dcc, Input, Output, State, ctx
import plotly.express as px


def make_page(info_comm):
    print('[make_page]')

    dict_src_item = dict()

    list_source = [src for src in info_comm.keys() if 'src' in src]
    for src in list_source:
        for item in info_comm[src]:
            dict_src_item.update({
                src + '_' + item: pd.read_csv('output_data/df_{}_{}.csv'.format(src, item))
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
        dcc.Tabs(id='tabs', value='tab1', children=[
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
        print('-' * 100 + '\n[INIT] make_tabs_content : ', tab)
        if tab == 'tab1':
            return tab1
        elif tab == 'tab2':
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
            html.Div('item', style={'color': 'black', 'fontSize': 14, 'font_family': 'Malgun Gothic'}),
            html.Div(id='tab1_area1_ddn2_empty'),
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
            html.Div(id='tab1_area1_ddn3_empty'),
        ], style={'display': 'inline-block', 'verticalAlign': 'bottom', 'margin-left': '80px'}),

        # tab1_area1_box2
        html.Div([
            html.Div('source', style={'color': 'black', 'fontSize': 14, 'font_family': 'Malgun Gothic'}),
            dcc.Dropdown(
                id='tab1_area1_ddn4_src', options=list_source, value=list_source[0],
                style={'height': '40px', 'width': '140px'})
        ], style={'display': 'inline-block', 'verticalAlign': 'bottom', 'margin-left': '120px'}),
        html.Div([
            html.Div('item', style={'color': 'black', 'fontSize': 14, 'font_family': 'Malgun Gothic'}),
            html.Div(id='tab1_area1_ddn5_empty'),
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
            html.Div(id='tab1_area1_ddn6_empty'),
        ], style={'display': 'inline-block', 'verticalAlign': 'bottom', 'margin-left': '80px'}),
    ])
    
    tab1 = html.Div([
        tab1_area1,

        # tab1_area2
        html.Div([
            html.Div(
                id='tab1_area2_empty1', children=[],
                style={'display': 'inline-block', 'verticalAlign': 'top'}
            ),
            dcc.Store(id='tab1_area2_data_table1'),
            html.Div(
                id='tab1_area2_empty2', children=[],
                style={'display': 'inline-block', 'verticalAlign': 'top', 'margin-left': '20px'}
            ),
            dcc.Store(id='tab1_area2_data_table2'),
        ]),

        html.Br(),

        # tab1_area3
        html.Div([
            html.Button(
                'Show Graph', id='tab1_area3_btn1_showgraph', n_clicks=0,
                style={'height': '40px', 'width': '80px'}
            )
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
        Output('tab1_area1_ddn2_empty', 'children'),
        Input('tab1_area1_ddn1_src', 'value'),
    )
    def make_tab1_area1_ddn2_empty(val):
        print('[INIT] make_tab1_area1_ddn2_empty : ', val, ctx.triggered_id)
        if val is not None:
            print(' > [IF] tab1_area1_ddn1_src : ', val, ctx.triggered_id)

            list_item = list(info_comm[val].keys())
            ddn = dcc.Dropdown(
                id='tab1_area1_ddn2_item', options=list_item, value=list_item[0],
                style={'height': '40px', 'width': '140px'}
            ),
        else:
            ddn = dcc.Dropdown(style={'height': '40px', 'width': '140px'}),

        return ddn

    @app.callback(
        Output('tab1_area2_empty1', 'children'),
        Output('tab1_area1_ddn3_empty', 'children'),
        Input('tab1_area1_btn1_loaddata', 'n_clicks'),
        State('tab1_area1_ddn1_src', 'value'),
        State('tab1_area1_ddn2_item', 'value'),
    )
    def make_tab1_area2_table1(btn, src, mat):
        print('[INIT] make_tab1_area2_table1 : ', btn, ctx.triggered_id)
        if btn != 0:
            print(' > [IF] tab1_area1_btn1_loaddata : ', btn, ctx.triggered_id)
            key = src + '_' + mat
            data_table = dash_table.DataTable(
                id='tab1_area2_table1',
                columns=[{'name': idx, 'id': idx, 'deletable': False} for idx in dict_src_item[key].columns],
                data=dict_src_item[key].to_dict('records'),
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

            list_col = [col for col in dict_src_item[key].columns if col not in ['Date']]
            ddn = dcc.Dropdown(
                id='tab1_area1_ddn3_col', options=list_col, value=list_col[0],
                style={'height': '40px', 'width': '140px'}
            ),

        else:
            data_table = None
            ddn = dcc.Dropdown(style={'height': '40px', 'width': '140px'})

        return data_table, ddn

    @app.callback(
        Output('tab1_area2_data_table1', 'data'),
        Input('tab1_area1_btn2_savedata', 'n_clicks'),
        State('tab1_area2_table1', 'data'),
    )
    def make_tab1_area2_data_table1(btn, data_table):
        print('[INIT] make_tab1_area2_data_table1 : ', btn, ctx.triggered_id)
        if btn != 0:
            print(' > [IF] tab1_area1_btn2_savedata : ', btn, ctx.triggered_id)
        else:
            data_table = None

        return data_table

    @app.callback(
        Output('tab1_area1_ddn5_empty', 'children'),
        Input('tab1_area1_ddn4_src', 'value'),
    )
    def make_tab1_area1_ddn5_empty(val):
        print('[INIT] make_tab1_area1_ddn5_empty : ', val, ctx.triggered_id)
        if val is not None:
            print(' > [IF] tab1_area1_ddn4_src : ', val, ctx.triggered_id)

            list_item = list(info_comm[val].keys())
            ddn = dcc.Dropdown(
                id='tab1_area1_ddn5_item', options=list_item, value=list_item[0],
                style={'height': '40px', 'width': '140px'}
            ),
        else:
            ddn = dcc.Dropdown(style={'height': '40px', 'width': '140px'}),

        return ddn

    @app.callback(
        Output('tab1_area2_empty2', 'children'),
        Output('tab1_area1_ddn6_empty', 'children'),
        Input('tab1_area1_btn3_loaddata', 'n_clicks'),
        State('tab1_area1_ddn4_src', 'value'),
        State('tab1_area1_ddn5_item', 'value'),
    )
    def make_tab1_area2_table2(btn, src, mat):
        print('[INIT] make_tab1_area2_table2 : ', btn, ctx.triggered_id)
        if btn != 0:
            print(' > [IF] tab1_area1_btn3_loaddata : ', btn, ctx.triggered_id)
            key = src + '_' + mat
            data_table = dash_table.DataTable(
                id='tab1_area2_table2',
                columns=[{'name': idx, 'id': idx, 'deletable': False} for idx in dict_src_item[key].columns],
                data=dict_src_item[key].to_dict('records'),
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

            list_col = [col for col in dict_src_item[key].columns if col not in ['Date']]
            ddn = dcc.Dropdown(
                id='tab1_area1_ddn6_col', options=list_col, value=list_col[0],
                style={'height': '40px', 'width': '140px'}
            ),

        else:
            data_table = None
            ddn = dcc.Dropdown(style={'height': '40px', 'width': '140px'})

        return data_table, ddn

    @app.callback(
        Output('tab1_area2_data_table2', 'data'),
        Input('tab1_area1_btn4_savedata', 'n_clicks'),
        State('tab1_area2_table2', 'data'),
    )
    def make_tab1_area2_data_table2(btn, data_table):
        print('[INIT] make_tab1_area2_data_table2 : ', btn, ctx.triggered_id)
        if btn != 0:
            print(' > [IF] tab1_area1_btn4_savedata : ', btn, ctx.triggered_id)
        else:
            data_table = None

        return data_table

    @app.callback(
        Output('tab1_area4_graph1', 'figure'),
        Output('tab1_area4_graph2', 'figure'),
        Output('tab1_area5_graph1', 'figure'),
        Output('tab1_area5_graph2', 'figure'),
        Input('tab1_area3_btn1_showgraph', 'n_clicks'),
        State('tab1_area2_data_table1', 'data'),
        State('tab1_area1_ddn3_col', 'value'),
        State('tab1_area2_data_table2', 'data'),
        State('tab1_area1_ddn6_col', 'value'),
    )
    def make_tab1_area4_graph(btn, dict_table1, col1, dict_table2, col2):
        print('[INIT] make_tab1_area4_graph : ', btn, ctx.triggered_id)
        if btn != 0:
            print(' > [IF] tab1_area3_btn1_showgraph : ', btn, ctx.triggered_id)

            df_1 = pd.DataFrame(dict_table1).set_index('Date')
            df_2 = pd.DataFrame(dict_table2).set_index('Date')
            print(' > shape original | df_1 : {} | df_2 : {}'.format(df_1.shape, df_2.shape))

            list_same_date = sorted(set(df_1.index) & set(df_2.index))
            print(' > list_same_date : ', list_same_date)

            df_1 = df_1.loc[list_same_date]
            df_2 = df_2.loc[list_same_date]
            print(' > shape common | df_1 : {} | df_2 : {}'.format(df_1.shape, df_2.shape))

            df_sum = pd.merge(df_1, df_2, on='Date', how='inner')
            df_corr = df_sum.corr()
            heatmap = px.imshow(df_corr, color_continuous_scale='Blues', origin='lower')
            # fig = px.colors.sequential.swatches_continuous()

            # df = px.data.gapminder()
            df_comp = pd.merge(df_1[[col1]], df_2[[col2]], on='Date', how='inner')
            df_comp = df_comp.reset_index()

            lineplot = px.line(df_comp, x='Date', y=df_comp.columns, line_shape='spline', render_mode='svg')

            df_pop = px.data.gapminder().query('year == 2007')
            treemap = px.treemap(
                df_pop,
                path=[px.Constant('world'), 'continent', 'country'], values='pop',
                color='lifeExp', hover_data=['iso_alpha']
            )

        else:
            heatmap = None
            lineplot = None
            treemap = None

        return heatmap, lineplot, treemap, treemap
    
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
