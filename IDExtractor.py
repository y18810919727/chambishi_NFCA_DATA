# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     IDExtractor
   Description :
   Author :       yzl
   date：          18-6-16
-------------------------------------------------
   Change Activity:
                   18-6-16:
-------------------------------------------------
"""
import pandas as pd
ID_name = "IDtoName.xls"


def get_used_id_list(file_name):
    id_table = pd.read_excel(file_name, sheetname='Sheet1')
    no_used_list =['不要','不管','没用','没数据']
    res = []
    for rowid in id_table.index:
        row = id_table.loc[rowid]
        sym = True
        for no_used_str in no_used_list:
            if str(row.values[2]).find(no_used_str) is not -1:
                sym=False
        if sym is False:
            continue
        res.append(str(row['Index']))
    return res


