# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 10:03:50 2020

@author: 45220
"""
import pandas as pd
import numpy as np
import prettytable as pt
from tqdm import tqdm
from ReadData import utils
import re


def ReadTXT(filename):
    # Reading data from a TXT document
    txt_list = list()
    with open("./" + filename, encoding='utf-8') as f:
        while(True):
            eachline = f.readline()
            if (not eachline):
                break
            eachline = eachline.strip().split('\t')
            txt_list.append(eachline)
    # Items with more than 5 columns are excluded
    txt_list_subset = list()
    for i in txt_list:
        if (len(i) == 5):
            txt_list_subset.append(i)
    print("subset / total = {} / {}".format(len(txt_list_subset), len(txt_list)))
    return txt_list_subset


def ProcessTXT(txt_list_subset):
    '''
    input : .txt
    output: save data
    '''
    # crate dataframe
    df = pd.DataFrame(txt_list_subset[1:], columns=txt_list_subset[0])
    # interval type
    IntervalType = dict()
    for i in tqdm(df.index):
        loc = df.iloc[i, :]['loc'].lower()
        if (loc not in IntervalType):
            IntervalType[loc] = 0
        IntervalType[loc] += 1
    # Key: cited_id, Value: Informations of citation
    repcount_1 = 0
    Paper2CitationDict = dict()
    Paper2CountsDict = dict()
    Paper2Pubyear = dict()
    re_number = re.compile(r"\d+")
    for i in tqdm(df.index):
        eachline = df.iloc[i, :]
        cite_id = eachline['cite_id']
        cited_id = eachline['cited_id']
        cite_y = eachline['cite_y']
        cited_y = eachline['cited_y']
        loc = eachline['loc'].lower()
        if (re_number.findall(cite_y)):
            cite_y = max([int(k) for k in re_number.findall(cite_y)])
        else:
            # miss publication year
            continue
        # Key: cited_id
        if (cited_id not in Paper2CitationDict):
            Paper2CitationDict[cited_id] = dict()
            for it in IntervalType.keys():
                Paper2CitationDict[cited_id][it] = dict()
        if (cite_y not in Paper2CitationDict[cited_id][loc]):
            Paper2CitationDict[cited_id][loc][cite_y] = list()
        # Repeated reference of the same interval
        if (cite_id not in Paper2CitationDict[cited_id][loc][cite_y]):
            Paper2CitationDict[cited_id][loc][cite_y].append(cite_id)
        else:
            repcount_1 += 1  # 150229
        # Repeated references of different intervals
        # ... 
    # Counts --> Top n%
    for Id in tqdm(Paper2CitationDict):
        paper2countslist = list()
        for loc in Paper2CitationDict[Id]:
            for cite_y in Paper2CitationDict[Id][loc]:
                paper2countslist += Paper2CitationDict[Id][loc][cite_y]        
        Paper2CountsDict[Id] = len(list(set(paper2countslist)))
    # pubyear --> distribution
    for i in tqdm(df.index):
        eachline = df.iloc[i, :]
        cite_id = eachline['cite_id']
        cited_id = eachline['cited_id']
        cite_y = eachline['cite_y']
        cited_y = eachline['cited_y']
        if (re_number.findall(cite_y)):
            cite_y = max([int(k) for k in re_number.findall(cite_y)])
        if (re_number.findall(cited_y)):
            cited_y = max([int(k) for k in re_number.findall(cited_y)])
        if (cite_id not in Paper2Pubyear):
            Paper2Pubyear[cite_id] = cite_y
        if (cited_id not in Paper2Pubyear):
            Paper2Pubyear[cited_id] = cited_y
         
    # save
    utils.SaveJson(IntervalType, "IntervalType")             # plot the pie chart of citation interval
    utils.SaveJson(Paper2CitationDict, "Paper2CitationDict") # Citation details for building model 
    utils.SaveJson(Paper2CountsDict, "Paper2CountsDict")     # Selecting highly cited literature
    utils.SaveJson(Paper2Pubyear, "Paper2Pubyear")           # plot publication distributions


def main():
    txt_list_subset_Re = ReadTXT('allResearchA.txt')    
    txt_list_subset_Ot = ReadTXT('allOtherA.txt')
    txt_list_subset = txt_list_subset_Re + txt_list_subset_Ot[1:]
    ProcessTXT(txt_list_subset)