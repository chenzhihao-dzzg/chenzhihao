#输入两个基金的估值代码，和比较日期（可选，默认值为今天），返回两个组合的相似度。
#相似度定义：取两只产品重复的持仓，计算占股票市值比的较小值，再求和
#若输入的日期无持仓数据，则往前取一天，直至有持仓数据。
#输入变量需带引号
#例如similar_1('169101','169104','20191208')。similar_1('169101','169104')。

# -*- coding: utf-8 -*-
import cx_Oracle
import pandas as pd
import datetime as dt
import time

#连接数据库
RISK_DB_RO_USER = 'riskadm'
RISK_DB_RO_PASS = 'Y*iaciej123456'
RISK_DB_RO_INST = 'zgriskd'
RISK_DB_RO_HOST = '172.17.7.80'
PORT1           = 1521
dsn = cx_Oracle.makedsn(RISK_DB_RO_HOST, PORT1, RISK_DB_RO_INST)
conn = cx_Oracle.connect("riskadm", "Y*iaciej123456", dsn)



def similar_1(vc_fund_code_1,vc_fund_code_2,l_date=str(dt.date.today().strftime('%Y%m%d'))):
    
    #sql代码
    sql_stock_1="""select * from view_vw_fm_risk_vstock where VC_FUND_CODE='"""+vc_fund_code_1+"""' and l_date="""+l_date
    sql_stock_2="""select * from view_vw_fm_risk_vstock where VC_FUND_CODE='"""+vc_fund_code_2+"""' and l_date="""+l_date
    
    #若若输入的日期无持仓数据，则往前取一天，直至有持仓数据。
    while pd.read_sql(sql_stock_1,conn).empty or pd.read_sql(sql_stock_2,conn).empty:
        date_year=time.strptime(l_date, '%Y%m%d').tm_year
        date_month=time.strptime(l_date, '%Y%m%d').tm_mon
        date_day=time.strptime(l_date, '%Y%m%d').tm_mday
        l_date_num=dt.date(date_year,date_month,date_day)
        l_date_num+= dt.timedelta(-1)
        l_date=str(l_date_num.strftime('%Y%m%d'))
        sql_stock_1="""select * from view_vw_fm_risk_vstock where VC_FUND_CODE='"""+vc_fund_code_1+"""' and l_date="""+l_date
        sql_stock_2="""select * from view_vw_fm_risk_vstock where VC_FUND_CODE='"""+vc_fund_code_2+"""' and l_date="""+l_date
    
    #持仓数据
    stock_1=pd.read_sql(sql_stock_1,conn)
    stock_2=pd.read_sql(sql_stock_2,conn)

    #计算单只股票市值/股票总市值，得到占比
    stock_1['SHARE_PCT_VALUE']=stock_1[stock_1['VC_STOCKTYPE_NAME']=="股票"]['CURRENCY_VALUE']/sum(stock_1[stock_1['VC_STOCKTYPE_NAME']=="股票"]['CURRENCY_VALUE'])
    stock_2['SHARE_PCT_VALUE']=stock_2[stock_2['VC_STOCKTYPE_NAME']=="股票"]['CURRENCY_VALUE']/sum(stock_2[stock_2['VC_STOCKTYPE_NAME']=="股票"]['CURRENCY_VALUE'])
    
    #取两只产品重复的持仓，计算占股票市值比的较小值，再求和
    test_merge=pd.merge(stock_1,stock_2,on=['WIND_CODE'],how='inner')
    test_merge['PCT_MIN']=test_merge[['SHARE_PCT_VALUE_x','SHARE_PCT_VALUE_y']].min(axis=1)
    sml_1=sum(test_merge['PCT_MIN'])
    return sml_1