# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     clean
   Description :
   Author :       yzl
   date：          18-6-15
-------------------------------------------------
   Change Activity:
                   18-6-15:
-------------------------------------------------
"""
import pandas as pd
import sys
import IDExtractor as ide
import pdb
import time
#time.strptime(dt, "%Y-%m-%d %H:%M:%S")
used_index=[]
def run(file_name, filter=False):
    print(filter)
    data = pd.read_csv(file_name,sep=';')
    res = data[data.ValueID == 1]
    res.rename(columns={'RealValue':'1'},inplace=True)
    res.drop(res.columns[[0,3,4]],axis=1,inplace=True)
    id_list = ide.get_used_id_list(ide.ID_name)
    #print(res)
    res.set_index('Timestamp', inplace=True)
    #print(res)

    for i in range(2,58):
        if str(i) not in id_list:
            continue
        if len(data[data.ValueID == i]) is 0:
            continue

        tmp_data = data[data.ValueID == i].iloc[:,1:3].values
        tmp_data = pd.DataFrame(tmp_data,columns=['Timestamp', str(i)])
        tmp_data.set_index('Timestamp',inplace=True)
        #print(tmp_data)
        cur_num = len(res.columns)
        #res.insert(cur_num,str(i), tmp_data)
        res = res.join(tmp_data,on='Timestamp',how='outer',sort='Timestamp')
        #print(res)
        #res = res.join(tmp_data)
        #res[str(i)] = tmp_data
    #print(res)
    delete_list = []
    #print(res)
    res.reset_index(inplace=True)
    # delete datas with 0 feeding flow
    if filter:
        for id in res.index:
            l = id-10
            r = id+10
            if l<0 or r>=len(res):
                delete_list.append(id)
                continue
            min_num = 1e9
            for i in range(l,r):
                num = abs(float(res.loc[i,'16']))
                min_num = min(min_num,num)
            if min_num < 20:
                delete_list.append(id)

    new_data = res.drop(delete_list)
    print("size of the original :"+str(len(res)))
    print("size of result :"+str(len(new_data)))
    new_data.to_csv("res_"+file_name)





if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("choose a csv file")
    else:
        file_name = sys.argv[1]
        filter = False 
        if len(sys.argv) is 3:
            if sys.argv[2] == 'filter':
                filter = True
        run(file_name, filter)
