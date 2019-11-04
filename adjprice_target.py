# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 13:42:16 2019

@author: chenzhihao
"""
#输入变量origin_data：dataframe格式，需要指标：交易日TRADE_DT，未复权收盘价S_DQ_CLOSE，复权因子S_DQ_ADJFACTOR。指标名称为可选参数。
#输入变量target_date：目标复权日期，格式为20191029
#返回一个增加后复权价格和定点复权价格的dataframe

import pandas as pd
import numpy as np
def get_adjprice(origin_data,
                 target_date, 
                 trade_dt='TRADE_DT',
                 close_col_name='S_DQ_CLOSE', 
                 adjust_col_name='S_DQ_ADJFACTOR'):
    data=origin_data.copy()

    #后复权价格
    data['adjprice_back']=data[close_col_name]*data[adjust_col_name]
    
    #读取定点复权日的复券因子,先判断该日是否有交易数据
    if data[data[trade_dt]==target_date][adjust_col_name].empty:
        print('目标日期无交易数据')
        return()
    else:
        #定点复权价格
        target_adjfactor=data[data[trade_dt]==target_date][adjust_col_name].values[0]
        data['adjprice_target']=data['adjprice_back']/target_adjfactor
        return data
   
    
    



