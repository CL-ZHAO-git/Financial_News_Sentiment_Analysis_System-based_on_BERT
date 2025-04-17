import dash
import dash_table
import pandas as pd
import json
from datetime import datetime as dt
import dash_core_components as dcc                  # 交互式组件
import dash_html_components as html                 # 代码转html
import time
import dash_bootstrap_components as dbc
from datetime import date
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from mongodb import query_normal,reslut_to_pd,get_condition,query_condition,update_doc,query_wx,reslut_to_pd_wx
from cls_crawler import get_cls_data
from wall_crawler import get_wall_data
from wx_crawler import get_artical_data
import re
import os
import base64
skip=60
icon="http://etigerfund-public.oss-cn-shanghai.aliyuncs.com/img/etigerfund_icon.png"
app= dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "弈泰金融信息监控平台"

colunms=[
    {'name':"时间戳","id":'time_stamp','hideable':True},
    {'name':"时间","id":"time","editable":False},
    {'name':"新闻内容","id":"content","editable":False},
    {'name':"情感分类","id":"class","editable":False},
    {'name':"情感得分","id":"score","editable":False},
    {'name':"股票名称","id":"stock_name","editable":False},
    {'name':"股票代码","id":"stock_code","editable":False},
    {'name':"自定义情绪","id":"label","editable":True},
    {'name':"自定义分类","id":"label2","editable":True}
]

with open('./行业分类.json','r',encoding='utf8')as fp:
    SW_data = json.load(fp)

SW_list=list(SW_data.keys())
bk_name_list=[]
with open('./板块名称列表.txt', 'r') as f:
    for line in f.readlines():
        line = line.strip('\n')
        bk_name_list.append(line)

bk_options=[{'label': i, 'value': i}  for i in bk_name_list]




import threading
import time
res_data=[]
cls_url_expired=False
wall_url_expired=False
def thread_Timer():

    global res_data
    global wall_url_expired
    global cls_url_expired
    # 声明全局变量
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    res1,wall_url_expired = get_wall_data(start_time)
    res2,cls_url_expired= get_cls_data(start_time)
    res1.extend(res2)
    res_data=res1
    global t1
    # 创建并初始化线程
    t1 = threading.Timer(180, thread_Timer)
    # 启动线程
    t1.start()




    # 创建并初始化线程



app.layout = html.Div([
dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=icon, height="35px")),
                    dbc.Col(dbc.NavbarBrand("金融信息监控平台", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),

        ),
        dbc.Row(
    [dbc.Col(dbc.NavItem(dbc.NavLink("使用说明", href="https://gitee.com/zhao-chengliang/ET_Fin_News/tree/master",style={"color":"white"},external_link=True,target='_blank')))],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)


        #dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="dark",
    style={'height':"70px"},
    dark=True,
),


    html.Div(id = 'my-div'),

dcc.Tabs(id='tabs', value='tab1', children=[


        dcc.Tab(label='实时新闻', value="tab1",children=[
            dbc.Alert(id="news_alert" ,color="primary",is_open=False,duration=170000),
            dbc.Alert("数据每3分钟更新、仅显示个股相关新闻", color="light"),
        dbc.Modal(
            [
                dbc.ModalHeader("错误"),
                dbc.ModalBody(id='error_info'),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_error", className="ml-auto")
                ),
            ],
            id="news_error",
        ),
            dbc.Col(dash_table.DataTable(id='real_time_news',columns = colunms,editable=True,
                                  hidden_columns=['time_stamp'],
                                css=[{"selector": ".show-hide", "rule": "display: none"}],#sort_action='native',export_format='xlsx',
                                  export_headers='display',
                                merge_duplicate_headers=True,
                                style_cell_conditional=[
                                     {'if': {
                                                                                          'column_id': 'stock_code'},
                                                                                       'width': '5%'},
                                                                                      {'if': {
                                                                                          'column_id': 'stock_name'},
                                                                                       'width': '5%'},
                                    {'if': {
                                        'column_id': 'time'},
                                        'width': '10%'},
                                                                                  ],
                                 style_data={'textAlign': 'left', 'whiteSpace': 'normal', 'height': 'auto', },
                                 style_header={'textAlign': "center",'backgroundColor': 'rgb(230, 230, 230)',
                                        'fontWeight': 'bold'},


                                 ),style={'margin-top':"5px"})
            ]),

    dcc.Tab(label="历史新闻",value="tab2",children=[
        html.Div(),
dbc.Alert("查询完成！", id='query_complete',color="success",is_open=False,duration=2000,fade=True),
dbc.Modal(
            [
                dbc.ModalHeader("提示"),
                dbc.ModalBody("没有更多数据"),
                dbc.ModalFooter(
                    dbc.Button(
                        "好的", id="close", className="ml-auto"
                    )
                ),
            ],
            id="no_more_data",
            centered=True,
        is_open=False
        ),
dbc.Modal(
            [
                dbc.ModalHeader("自定义标签更新完成"),
                #dbc.ModalBody("没有更多数据"),
                dbc.ModalFooter(
                    dbc.Button(
                        "好的", id="close_1", className="ml-auto"
                    )
                ),
            ],
            id="update_complete",
            centered=True,
        is_open=False
        ),

dbc.Row(
       [


    dbc.Col(dcc.DatePickerSingle(
            id='my-date-picker-single',
            min_date_allowed=dt(2018, 8, 5 ),
            initial_visible_month=dt.today(),
            max_date_allowed=dt(2100, 9, 19),
             # for testing purpose
             date=None # Actual code，
            ,clearable=True
        ),width=4,lg=1),
           dbc.Col( dcc.Input(
            id="input_stock_name",
            type="text",
            style={'width':"100%",'height':"100%"},
            placeholder="请输入股票名称/代码",
            ),width=8,lg=2,md=15),
        dbc.Col(dcc.Dropdown(
        id='SW1',
        #style={"width":'30%'},
        options=[ {'label': i, 'value': i}  for i in SW_list],
        placeholder="请选择一级行业",
        value=None
    ),width=8,lg=2),
        dbc.Col(dcc.Dropdown(
        id='SW2',
        #style={"width":'30%'},
        placeholder="请选择二级行业",
        value=None
    ),width=8,lg=2),
        dbc.Col(dcc.Dropdown(
        id='SW3',
        #style={"width":'30%'},
        placeholder="请选择三级行业",
        value=None
    ),width=8,lg=2),
    dbc.Col(dcc.Dropdown(id="bankuai",
                 #style={"width": '%'},
                 placeholder="请输入并选择板块",
                 value=None
                 ),width=8,lg=2,md=10),
        dbc.Col(dbc.Button("查询", color="primary", id="query_button",className="mr-1",n_clicks=0)
                ,width=5,lg=1,md=10)]
    ,style={'margin-top':"20px",'margin-left':'10px','margin-bottom':'20px'})
           ,
        dbc.Col(dash_table.DataTable(id='result', editable=True, columns=colunms,
                                     hidden_columns=['time_stamp'],  # , sort_action='native',export_format='xlsx',
                                     merge_duplicate_headers=True,
                                    css=[{"selector": ".show-hide", "rule": "display: none"}],
                                     page_action='none',
                                    style_cell_conditional=[
                                    {'if': {'column_id': 'stock_code'},
                                    'width': '5%'},
                                     {'if': {'column_id': 'stock_name'},
                                         'width': '5%'},
                                        {'if': {
                                        'column_id': 'time'},
                                        'width': '5%'},

                                    ],


                                     style_data={
                                         'textAlign': 'left',
                                         'whiteSpace': 'normal',
                                         'height': 'auto',
                                     },
                                    style_header={'textAlign': "center",'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold' },
                                     )),
        dbc.Row([
        dbc.Col(dbc.Button("加载更多", color="primary", id="load_more",className="mr-1",n_clicks=0,style={'width':'80%'}),width=10,md=2),
        dbc.Col(dbc.Button("提交",  outline=True, color="success", id="submit",className="mr-1",n_clicks=0,style={'width':'40%'}),width=10,md=2)],justify="center",
        style={'margin-top':"20px"})
    ]),




    dcc.Tab(label="公众号",value="tab4",children=[
        dbc.Alert(id="wx_alert" ,color="primary",is_open=False,duration=4000),
        dbc.Modal(
            [
                dbc.ModalHeader("错误！"),
                dbc.ModalBody("微信公众号爬虫失效 或 暂无网络连接"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_wx_error", className="ml-auto")
                ),
            ],
            id="wx_error",
        ),
dcc.Dropdown(
    options=[
        {'label': '爱在冰川同学', 'value': '爱在冰川同学'},
        {'label': '财联社', 'value': '财联社'},
        {'label': '华创证券研究', 'value': '华创证券研究'},
         {'label': '巨潮资讯网', 'value': '巨潮资讯网'}
    ],
    value=[],
    id='account',

    multi=True),
dbc.Col(dbc.Button("登陆及爬取", color="primary", id="login",className="mr-1",n_clicks=0,style={'width':'80%'})),
dbc.Col(dash_table.DataTable(id='wx_public',columns = [{'name':"时间","id":"date"},{'name':"标题","id":"title",'presentation':'markdown'},{'name':"公众号","id":"account"}],
                                hidden_columns=['date_num'],

                                css=[{"selector": ".show-hide", "rule": "display: none"}],#sort_action='native',export_format='xlsx',
                                  export_headers='display',
                                merge_duplicate_headers=True,
                                 style_data={'textAlign': 'left', 'whiteSpace': 'normal', 'height': 'auto', },
                                 style_header={'textAlign': "center",'backgroundColor': 'rgb(230, 230, 230)',
                                        'fontWeight': 'bold'},
                                 ),style={'margin-top':"5px"}
        ),
            dbc.Modal(
            [
                dbc.ModalHeader("请扫码登陆"),
                dbc.ModalBody(html.Img(src="",id='QRcode_img')),
                dbc.ModalBody("扫码后请等稍候，数据在10s内更新"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-QR", className="ml-auto")
                ),
            ],
            id="QRcode_scan",
            size="sm",
        ),
     dbc.Col(dbc.Button("加载更多", color="primary", id="load_more_wx",className="mr-1",n_clicks=0))

    ])

])
    ,
        dcc.Store(id='query_year'),
        dcc.Store(id='query_year_2'),
        dcc.Store(id='query_skip_num'),
        dcc.Store(id="select_year"),
        dcc.Store(id="select_month"),
        dcc.Store(id="select_day"),
        dcc.Store(id="stock_name"),
        dcc.Store(id="stock_code"),
        html.Div(id='output-state'),

    dcc.Interval(
        id='interval-component',
        interval=180 * 1000,  # in milliseconds
        n_intervals=0
    )])




@app.callback(
              Output('real_time_news','data'),
              Output('news_alert','is_open'),
              Output('news_alert','children'),
              Output('news_error','is_open'),
              Output('error_info','children'),
              [Input('interval-component', 'n_intervals'),
               Input('close_error','n_clicks'),
               State('real_time_news','data')])
def update(n,n2,previous_pd):
    if n == 0:
        raise PreventUpdate
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print("更改id")
    print(changed_id)
    global res_data
    global wall_url_expired
    global cls_url_expired
    if 'interval-component' in changed_id:
        if wall_url_expired or cls_url_expired:
            return [],False,'',True,'爬虫失效 或网络故障，请联系管理员更新爬虫程序'
        if previous_pd==None:
            previous_pd=pd.DataFrame()
        else:
            previous_pd = pd.DataFrame(previous_pd)

        data,new_num=reslut_to_pd(res_data)

        if data.empty:
            message = '暂无新个股相关新闻'
        else:
            data = data.sort_values(by='time_stamp', ascending=False)
            message = '更新完成！ 共更新{}条数据'.format(new_num)
        data=pd.concat([data,previous_pd],ignore_index=True)
        data = data.to_dict('records')
        return data,True,message,False,''

    elif 'close_error' in changed_id:
        return previous_pd,False,'',False,''



@app.callback(
    Output('select_year','data'),
    Output('select_month','data'),
    Output('select_day','data'),

    [Input('my-date-picker-single', 'date')]

)
def select_date(date_value):
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        return date_object.year,date_object.month,date_object.day
    else:
        return None,None,None
@app.callback(
    Output("stock_name","data"),
    Output("stock_code","data"),
    [Input("input_stock_name","value")]
)
def input_stock(value):
    if value != None:
        pattern = re.compile('[0-9]+')
        match = pattern.findall(value)

        if match:#输入为代码
            return "",value
        else:
            return value,""
    else:
        return '',''

@app.callback(
    Output('result','data'),
    Output('query_skip_num',"data"),
    Output('query_year_2','data'),
    Output("no_more_data", "is_open"),
    Output("query_complete", "is_open"),

    [Input("query_button","n_clicks"),
     Input("load_more","n_clicks"),
     Input('close','n_clicks'),
     State("result","data"),
     State('select_year', 'data'),
     State('select_month', 'data'),
     State('select_day', 'data'),
     State("stock_name","data"),
     State("stock_code","data"),
     State('query_skip_num','data'),
     State('query_year_2','data'),
     State('SW1','value'),
     State('SW2','value'),
     State('SW3','value'),

     State('bankuai','value')
     ]
)

def query_data(click_1,click_2,n,previous_pd,query_year,month,day,name,code,global_skip_num,year,SW1,SW2,SW3,bk_name):


    global skip
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if click_1==0 and click_2 ==0:
        year=dt.today().year
        skip_num=0
        data_table, year,skip_num,no_more_data= query_normal(previous_pd, year, skip_num, skip)
        data = data_table.to_dict('records')
        skip_num=skip_num+skip

        return data,skip_num,year,no_more_data,False

    if "query_button" in changed_id:
        if query_year==None:#不指定日期
            print("sssss")
            year=dt.today().year
        else:
            year=query_year
        condition=get_condition(month,day,name,code,SW1,SW2,SW3,bk_name)
        print(year,condition)

        data_table,year,skip_num,no_more_data=query_condition(None,year,0,skip,condition)
        print("1",year)
        data = data_table.to_dict('records')
        skip_num = skip_num + skip
        print(skip_num)

        return data,skip_num,year,no_more_data,True
        # if query_year==None:
        #     year = dt.today().year
        #
        # if name=="" and code!="":
        #
    elif "load_more" in changed_id:
        condition=get_condition(month,day,name,code,SW1,SW2,SW3,bk_name)
        print(condition)
        if condition=={}:
            data_table, year,skip_num,no_more_data = query_normal(previous_pd, year, global_skip_num, skip)
            skip_num = skip_num+ skip
            data = data_table.to_dict('records')
            return data,skip_num,year,no_more_data,False
        else:
            print(year)
            print(global_skip_num)
            data_table,year,skip_num,no_more_data=query_condition(previous_pd,year,global_skip_num,skip,condition)
            skip_num = skip_num+ skip
            data = data_table.to_dict('records')
            print(year)
            return data, skip_num, year,no_more_data,False
    elif 'close' in changed_id:
        #print("is")
        return previous_pd, global_skip_num, year,False,False

@app.callback(
    Output('update_complete', 'is_open'),
    [Input("submit","n_clicks"),
     Input('close_1','n_clicks'),
    State('result', 'data'),
    ]
)
def update_data(n,n2,rows):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'submit' in changed_id:
        if n>0:
            df=pd.DataFrame(rows)
            for index in df.index:
                time_stamp=df.loc[index]["time_stamp"]
                label=df.loc[index]['label']
                label2 = df.loc[index]['label2']
                name=df.loc[index]["stock_name"]
                if label!="" or label2!='':
                    if len(name)>4:
                        name=name[:4]
                    update_doc(time_stamp,name,label,label2)
        return True
    elif 'close_1' in changed_id:
        return False
    else:
        return False


@app.callback(
    Output('SW2','options'),
    Output('SW3','options'),
    Output('SW2','value'),
    Output('SW3','value'),

    [Input('SW1','value'),
     Input('SW2', 'value'),
     State('SW1', 'value'),
     State("SW2",'options')
     ]
)
def select_SW(value1,value2,SW1_value,SW2_options):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'SW1' in changed_id:
        if value1!=None:
            SW2_list=list(SW_data[value1].keys())
            options=[ {'label': i, 'value': i}  for i in SW2_list]
            return options,[],None,None
        else:
            return [],[],None,None
    elif 'SW2' in changed_id:
        if value2 != None:
            SW3_list = SW_data[SW1_value][value2]
            options = [{'label': i, 'value': i} for i in SW3_list]
            return SW2_options,options,value2,None
        else:
            return SW2_options,[],None,None
    else:
        return [],[],None,None



@app.callback(
    Output("bankuai", "options"),
    [Input("bankuai", "search_value")],
)
def update_options(search_value):
    if not search_value:
        raise PreventUpdate
    return [o for o in bk_options if search_value in o["label"]]

@app.callback(
    Output("QRcode_scan", "is_open"),
    Output('QRcode_img','src'),
    [Input('login','n_clicks'),
     Input('close-QR','n_clicks'),]
)
def open_QR(n1,n2):
    src = './QRcode_images'
    num=len(os.listdir(src))
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if n1==0 and n2==0:
        return False,''
    else:
        if 'login' in changed_id :
            print("bbb")
            #time.sleep(2.5)
            while num==len(os.listdir(src)):
                print('等待',len(os.listdir(src)))
                time.sleep(0.3)
            print("图片就位")
            #src = './QRcode_images'
            files = os.listdir(src)
            files_path = [f'{src}/{file}' for file in files]
            files_path.sort(key=lambda fp: os.path.getctime(fp), reverse=True)
            newest_file = files_path[0]
            print(newest_file)
            encoded_image = base64.b64encode(open(newest_file, 'rb').read())
            src='data:image/png;base64,{}'.format(encoded_image.decode())
            print(src)
            return True,src
        else:
            return False,''



@app.callback(
    Output('wx_public','data'),
    Output('wx_alert','is_open'),
    Output('wx_alert','children'),
    Output('wx_error','is_open'),
    [Input('login','n_clicks'),
     Input('load_more_wx','n_clicks'),
     Input('close_wx_error','n_clicks'),
     State('wx_public','data'),
     State('account','value')]


)
def search(n1,n2,n3,previous_pd,nickname_list):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if n1==0 and n2 ==0:
        data,_=query_wx(None,0,30)
        #print(data)
        #print('第一次查询')
        #print(data)
        return data.to_dict('records'),False,"",False
    else:
        if 'login' in changed_id:
            print("aaa")
            previous_pd = pd.DataFrame(previous_pd)
            data,is_expired=get_artical_data(nickname_list)
            data,new_num=reslut_to_pd_wx(data)
            if data.empty:
                message='暂无新数据'
            else:
                message='更新完成！ 共更新{}条数据'.format(new_num)
            data=pd.concat([data,previous_pd], ignore_index=True,sort=False)
            data_ = data.to_dict('records')
            return data_,True,message,is_expired
        elif 'load_more_wx' in changed_id:
            data_table,_=query_wx(previous_pd,n2*30,30)
            return data_table.to_dict('records'),False,"",False
        elif 'close_wx_error' in changed_id:
            return previous_pd,False,"",False


if __name__ == '__main__':
    t1 = threading.Timer(180, thread_Timer)
    t1.start()
    app.run_server(host="127.0.0.1",port=35456)#,debug=True)
