import dash
from datetime import timedelta
from dash.dependencies import Input, Output, State
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from datetime import datetime as dt
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os,sys
BASH_DIR = os.path.abspath(os.path.dirname(os.getcwd()))
FUNC_DIR = (BASH_DIR+"/functions")
# OUTPUT_DIR = (BASH_DIR+"/outputs/")
sys.path.append(FUNC_DIR)
# import common_config,common_functions
# common_config.pd_display_setting()
# etiger_songpeng = common_config.etiger_stock_songpeng
# DB_Session = sessionmaker(bind=etiger_songpeng)
# sess = DB_Session()


app = dash.Dash(__name__)

app.layout =  html.Div(
    html.Div([
        html.H4('异动板块监控'),
        dbc.Col(html.Div(id="up_limit")),
        html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
        html.Div(id='output-state'),
        dcc.Interval(
            id='interval-component',
            interval=300*1000, # in milliseconds
            n_intervals=0
        )
    ])
)
def get_stock_price():
    sql_string = "SELECT * FROM etiger_member_xusongpeng.tdx_realtime_price where `trading_time`>'"\
                 +min(dt.strftime(dt.now()-timedelta(minutes=2),'%H:%M:%S'),'14:58:00')+"' " \
                 "order by `trading_time` ;"
    last_price = pd.read_sql_query(sql_string,etiger_songpeng)
    last_price.drop_duplicates(subset=['instrument_id'],
                               keep='last',inplace=True)
    last_price = last_price[last_price['close']>0]
    last_price = last_price[last_price['prev_close'] > 0]
    last_price['ratio'] = last_price['close']/last_price['prev_close']-1
    last_price = last_price[['instrument_id','close','ratio']]
    return last_price

def get_sw_winda():
    sql_string = "SELECT * FROM etiger_member_xusongpeng.sw_winda_table;"
    sw_winda = pd.read_sql_query(sql_string,etiger_songpeng)
    sw_winda = sw_winda[['InstrumentID','InstrumentName','SW3Name']]
    return sw_winda


def get_zhangting():
    sql_string = "SELECT * FROM etiger_member_xusongpeng.daily_zhangting;"
    zhangting = pd.read_sql_query(sql_string,etiger_songpeng)
    zhangting = zhangting.drop_duplicates(subset='InstrumentID',keep='last')
    # zhangting.columns
    zhangting = zhangting[[ 'InstrumentID','GaiNian', 'EventCategory', 'Remarks','Rating']]
    return zhangting

def daily_uplimit():
    last_price = get_stock_price()
    sw_winda = get_sw_winda()
    zhangting = get_zhangting()

    last_price = pd.merge(last_price, sw_winda, how='inner', left_on='instrument_id', right_on='InstrumentID')
    zhangting = pd.merge(zhangting,last_price,how='outer',left_on='InstrumentID',right_on='InstrumentID')
    zhangting = zhangting[['InstrumentID','InstrumentName','close','ratio','SW3Name','GaiNian','EventCategory','Remarks','Rating']]
    zhangting.rename(columns={'close':'Close','ratio':'PriceChangeClose','SW3Name':'IndustryName'},inplace=True)
    zhangting = zhangting[zhangting['PriceChangeClose']>=0.099]
    zhangting['PriceChangeClose'] =zhangting['PriceChangeClose'].round(4)
    zhangting = zhangting.sort_values(by=['GaiNian','IndustryName','EventCategory'])
    zhangting.reset_index(drop=True,inplace=True)
    zhangting['ID'] =zhangting.index
    zhangting['Date'] = dt.today().strftime('%Y-%m-%d')
    return zhangting


@app.callback(Output('up_limit', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_uplimit_table(n):
    data_table =daily_uplimit()
    data = data_table.to_dict('records')
    columns = [{"name": i, "id": i, } for i in (data_table.columns)]
    return [dash_table.DataTable(data=data, columns=columns,editable=True,hidden_columns=['InstrumentID','Close','Date','ID'],sort_action='native',
                                 export_format = 'xlsx',export_headers = 'display',merge_duplicate_headers = True,
                                 style_cell={'textAlign': 'left','whiteSpace': 'normal','height': 'auto',},
                                 page_action='native',
                                 page_current=0,
                                 page_size=20,
                                 )]

@app.callback(
    Output('output-state', 'children'),
    [Input('submit-button-state', 'n_clicks')],
    [State('up_limit', 'children')])
def update_columns(n_clicks, data):

    if n_clicks>0:
        contents = pd.DataFrame.from_dict(data[0]['props']['data'])
        contents.drop(columns='ID',inplace=True)
        insql = pd.read_sql_query('SELECT * FROM etiger_member_xusongpeng.daily_zhangting '
                                  'where `Date`="' + dt.today().strftime("%Y-%m-%d") + '";', etiger_songpeng)
        append_data = contents[~contents['InstrumentID'].isin(insql['InstrumentID'])]
        append_data.to_sql('daily_zhangting', etiger_songpeng, if_exists='append', index=False)
        update_data = contents[contents['InstrumentID'].isin(insql['InstrumentID'])]
        update_data.sort_values('InstrumentID',inplace=True)
        update_data.set_index('InstrumentID',inplace=True)
        insql = insql[insql['InstrumentID'].isin(update_data.index)]
        insql = insql[['InstrumentID','Date','InstrumentName','Close','PriceChangeClose','IndustryName','GaiNian','EventCategory','Remarks','Rating']]
        insql.set_index('InstrumentID',inplace=True)

        diff_cate = update_data[update_data['EventCategory'].str.strip() != insql['EventCategory'].str.strip()]
        diff_remarks = update_data[update_data['Remarks'].str.strip() != insql['Remarks'].str.strip()]
        diff_gainian = update_data[update_data['GaiNian'].str.strip() != insql['GaiNian'].str.strip()]
        diff_rating = update_data[update_data['Rating'].str.strip() != insql['Rating'].str.strip()]

        if len(diff_cate.index)>0:
            for item in diff_cate.index:
                if update_data.loc[item,'EventCategory'] is not None:
                    query = "update `etiger_member_xusongpeng`.`daily_zhangting` set `EventCategory`='"+update_data.loc[item,'EventCategory']+"' " \
                            "where `Date`='"+dt.today().strftime(
                        "%Y-%m-%d")+"' and `InstrumentID`='"+item+"';"
                    sess.execute(query)
                    sess.commit()
        if len(diff_remarks.index) > 0:
            for item in diff_remarks.index:
                if update_data.loc[item, 'Remarks'] is not None:
                    query = "update `etiger_member_xusongpeng`.`daily_zhangting` set `Remarks`='" + update_data.loc[
                        item, 'Remarks'] + "' where `Date`='" + dt.today().strftime(
                        "%Y-%m-%d") + "' and `InstrumentID`='" + item + "';"
                    sess.execute(query)
                    sess.commit()
        if len(diff_gainian.index) > 0:
            for item in diff_gainian.index:
                if update_data.loc[item, 'GaiNian'] is not None:
                    query = "update `etiger_member_xusongpeng`.`daily_zhangting` set `GaiNian`='" + update_data.loc[
                        item, 'GaiNian'] + "' where `Date`='" + dt.today().strftime(
                        "%Y-%m-%d") + "' and `InstrumentID`='" + item + "';"
                    sess.execute(query)
                    sess.commit()
        if len(diff_rating.index) > 0:
            for item in diff_rating.index:
                if update_data.loc[item, 'Rating'] is not None:
                    query = "update `etiger_member_xusongpeng`.`daily_zhangting` set `Rating`='" + update_data.loc[
                        item, 'Rating'] + "' where `Date`='" + dt.today().strftime(
                        "%Y-%m-%d") + "' and `InstrumentID`='" + item + "';"
                    sess.execute(query)
                    sess.commit()
        sess.close()

        return u''' The Button has been pressed {} times '''.format(n_clicks)


if __name__ == '__main__':
    app.run_server(debug=True,port=54789)
