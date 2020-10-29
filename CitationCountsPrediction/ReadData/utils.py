# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 11:24:56 2020

@author: 45220
"""
import json
import math
import numpy as np
import prettytable as pt

#%%
def SaveJson(file, filename):
    with open("./" + filename, 'w') as f:
        json.dump(file, f)

        
def ReadJson(filename):
    with open('./' + filename, 'r') as f:
        file = json.load(f)
    return file


#%%
def LocType():
    IntervalType = ReadJson("IntervalType")
    others = ['case', 'experiment', 'limitation', 'literature', 'background']
    interval_name = list()
    for it in IntervalType.keys():
        if (it not in others):
            interval_name.append(it)
    interval_name.append('others')
    return interval_name, others

#%%
# c(t)
def FineGrainedReference(Id, span, Paper2Pubyear, Paper2CitationDict):
    '''
        Y: 从pubyear开始连续span年的细粒度引用
           每个元素是tuple, 反应在每个区间的被引用频次
           如果重复rep_num引用, 则使用 1 / rep_num计算
    '''
    interval_name, others = LocType()
    pubyear = Paper2Pubyear[Id]
    Y = list()
    for year in np.arange(pubyear, pubyear + span):
        year = "{}".format(year)
        # yearly loc2paperid 
        temp = dict()
        for it in interval_name:
            temp[it] = list()
        for loc in Paper2CitationDict[Id]:
            if (year in Paper2CitationDict[Id][loc]):
                if (loc in others):
                    temp['others'] = temp['others'] + Paper2CitationDict[Id][loc][year]
                else:
                    temp[loc] = temp[loc] + Paper2CitationDict[Id][loc][year]    
        # yearly SET()
        set_temp = list()
        for it in interval_name:    
            set_temp = set_temp + temp[it]
        set_temp = list(set(set_temp))
        #
        temp_count = dict()
        for it in interval_name:
            temp_count[it] = 0 
        for i in set_temp:
            rep_num = 0  # 区间重复数 
            rep_interval = list()
            for it in interval_name:
                if (i in temp[it]):
                    rep_num += 1
                    rep_interval.append(it)
            # 计数, 1 / rep_num
            for rit in rep_interval:
                temp_count[rit] += 1 / rep_num
        # dict 2 list
        score = list()
        for it in interval_name:
            score.append(temp_count[it])
        Y.append(score)
    return Y
    

def CoarseGrainedReference(Id, span, Paper2Pubyear, Paper2CitationDict):
    Y_FineGrained = FineGrainedReference(Id, span, Paper2Pubyear, Paper2CitationDict)
    Y_CoarseGrained = list()
    for y in Y_FineGrained:
        Y_CoarseGrained.append(math.ceil(sum(y)))
    return Y_CoarseGrained


def IntervalRatio(Y):
    # ['introduction', 'method', 'result', 'conclusion', 'others']
    Y = np.array(Y)
    Y = list(Y.sum(axis=0) / sum(Y.sum(axis=0)))
    Y = [round(y, 4) for y in Y]
    return Y

#%%   
def CorrelationCoefficient(c):
    c = np.array(c)
    return np.corrcoef(c)[0, 1]
    

def MultiCorCoef(A, B):
    '''
    A 是 论证区间比率列表 row: 文章, colum: 区间类比数目
    B 是 span+span2年份的引文数目
    '''
    cor_list = list()
    for i in range(np.array(A).shape[-1]):
        C = list(np.array(A)[:, i])
        D = [C, B]
        cor = CorrelationCoefficient(D)
        cor_list.append(round(cor, 5))
    tb = pt.PrettyTable()
    interval_name,_ = LocType()
    tb.field_names  = interval_name
    tb.add_row(cor_list)
    print(tb)