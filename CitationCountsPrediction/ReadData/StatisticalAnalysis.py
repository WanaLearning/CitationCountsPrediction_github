# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 11:38:57 2020

@author: 45220
"""
from ReadData import utils
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
import random

# read data
IntervalType = utils.ReadJson("IntervalType")
Paper2CitationDict = utils.ReadJson("Paper2CitationDict")
Paper2CountsDict = utils.ReadJson("Paper2CountsDict")
Paper2Pubyear = utils.ReadJson("Paper2Pubyear")
# intervals are merged into others
interval_name, others = utils.LocType()

#%%
def PieIntervalType(IntervalType, others):
    '''
    Multiple citation in the same interval are counted once
    The citations in different intervals are calculated separately
    '''
    interval_name = list()
    interval_count = list()
    
    others_count = 0
    for it in IntervalType.keys():
        if (it not in others):
            interval_name.append(it)
            interval_count.append(IntervalType[it])
        else:
            others_count += IntervalType[it] 
    interval_name.append('others')
    interval_count.append(others_count)    
    plt.pie(interval_count, labels=interval_name, autopct='%1.2f%%')
    plt.axis('equal')


def ExplosiveGrowthofPublications(Paper2Pubyear):
    '''
    Explosive Growth of Publications
    Figure S1: The number of papers published each year in the PR corpus. 
    Inset: cumulative number of papers N(t) published up to year t
    '''
    # 1980-2011 obey power law
    ValidYear = np.arange(1980, 2011)  
    
    PubDistribution = dict()
    for Id in Paper2Pubyear:
        pubyear = Paper2Pubyear[Id]
        if (pubyear not in PubDistribution):
            PubDistribution[pubyear] = 0 
        PubDistribution[pubyear] += 1
    # 
    X = list()
    Y = list()
    for year in ValidYear:
        X.append(year)
        Y.append(PubDistribution[year])
    Y_cumulative = list()
    for i, _ in enumerate(Y):
        Y_cumulative.append(np.log(sum(Y[:i+1])))
    # 
    fig = plt.figure()
    left, bottom, width, height = 0.1, 0.1, 1, 1
    ax1 = fig.add_axes([left, bottom, width, height])
    ax1.plot(X, Y, marker='s', c='r')
    ax1.set_yticks(np.arange(0, 25001, 5000))
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Publications per year")
    ax1.yaxis.get_major_formatter().set_powerlimits((0, 1))
    #
    left, bottom, width, height = 0.25, 0.55, 0.5, 0.5
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.plot(X, Y_cumulative, marker='o', c='r')
    ax2.set_ylabel("log(N(t))")
    # The first three do not participate in linear fitting
    Initiator = 3  
    model = linear_model.LinearRegression()
    model.fit(np.array(X[Initiator:]).reshape(-1, 1), Y_cumulative[Initiator:])
    Y_cumulative_predict = model.predict(np.array(X[Initiator:]).reshape(-1, 1))
    ax2.plot(X[Initiator:], Y_cumulative_predict, linestyle='--', c='black')
    ax2.set_yticks(np.arange(6, 14, 1))
#%%

def FilteredPaper(Paper2CountsDict, TargetedYear=1995, threshold=10):
    '''
    <Quantifying long-term scientific impact>
    we replicated their analysis using 5-year citation history to 
    predict future citations. We used 1973 Physical Review papers 
    published in 1980 that acquired  at least 10 citations in the 
    first 5 years. 
    '''
    
    TargetedSet = list()     # Time requirement              1995 
    TargetedSubSet = list() # Number of citations threshold 10
    for Id in Paper2CountsDict:
        if (Paper2Pubyear[Id] == TargetedYear):
            TargetedSet.append(Id)
            if (Paper2CountsDict[Id] >= threshold):
                TargetedSubSet.append(Id)
    print("{} / {}".format(len(TargetedSubSet), len(TargetedSet)))
    return TargetedSubSet


def CharacterizingCitationDynamics():
    '''
     Yearly citation ci (t) for 54 randomly selected papers published 
     between 1990 and 2000 in the corpus. The color code corresponds to 
     each papers’publication year
    '''
    # 1990-2000 random pick SIZE papers
    size = 5                          # Number of samples per year
    Fig1Span = np.arange(1990, 2000)  # The year span of the sample set
    Fig1SampleSet = list()            # Sample taken
    threshold = 30                    # Highly cited threshold
    num = 0                           # Total number of samples greater than threshold
    for year in Fig1Span:
        TargetedSubSet = FilteredPaper(Paper2CountsDict, TargetedYear=year, threshold=threshold)
        temp_num = len(TargetedSubSet)
        if (temp_num < size):
            # All included
            Fig1SampleSet = Fig1SampleSet + TargetedSubSet
        else:
            # Random sampling SIZE papers
            Fig1SampleSet = Fig1SampleSet + random.sample(TargetedSubSet, size)
        num += temp_num
    print("Ramdom Sampling: {} / {}".format(len(Fig1SampleSet), num))
    # plot with Fig1SampleSet
    EndYear = 2021
    fig = plt.figure(figsize=(15, 8))
    left1, bottom1, width1, height1 = 0.1, 0.1, 1, 1
    ax1 = fig.add_axes([left1, bottom1, width1, height1])
    left2, bottom2, width2, height2 = 0.15, 0.55, 0.5, 0.5
    ax2 = fig.add_axes([left2, bottom2, width2, height2])
    cm = plt.cm.get_cmap('rainbow')
    for Id in Fig1SampleSet:
        pubyear = Paper2Pubyear[Id]
        span = EndYear - pubyear
        Y = utils.CoarseGrainedReference(Id, span, Paper2Pubyear, Paper2CitationDict)
        # Change to ratio %
        Y_ratio = np.array(Y) / sum(Y)
        # cumulative ratio
        Y_ratio_cumulative = list()
        for i, j in enumerate(Y_ratio):
            Y_ratio_cumulative.append(sum(Y_ratio[:i+1]))
        c = (pubyear-Fig1Span[0]) / (Fig1Span[-1]-Fig1Span[0])
        ax1.plot(np.arange(pubyear, EndYear), Y_ratio_cumulative, c=cm(c), marker='o')
        ax2.plot(np.arange(pubyear, EndYear), Y_ratio, c=cm(c), marker='s')
    # colorbar
    colorbar_x = (Fig1Span-Fig1Span[0]) / (Fig1Span[-1]-Fig1Span[0])
    colorbar_y = [-1] * len(Fig1Span)
    ax2c = ax2.scatter(Fig1Span, colorbar_y, c=colorbar_x, cmap=cm)    
    fc = fig.colorbar(ax2c, ax=ax2)
    fc.set_ticks(colorbar_x)
    fc.set_ticklabels(Fig1Span)
    #
    ax1.set_xticks(np.arange(Fig1Span[0], EndYear, 5))
    ax2.set_xticks(np.arange(Fig1Span[0], EndYear, 5))
    ax1.set_xlabel('Year')
    ax2.set_ylim([-0.01, 0.4])
    ax2.set_xlabel('Year')


def DifferentLongTermImpacts():
    '''
    Figure S2: a SPAN-year span collect the same number of citations (threshold) are found to
    have widely different long-term impacts. (different citaion interval)
    '''
    threshold = 5                     # Filter papers 
    Fig1Span = np.arange(2000, 2010)  # The year span of the sample set
    Fig1SampleSet = list()            # Sample taken
    for year in Fig1Span:
        TargetedSubSet = FilteredPaper(Paper2CountsDict, TargetedYear=year, threshold=threshold)
        Fig1SampleSet = Fig1SampleSet + TargetedSubSet
    print("pubyear in {}-{}, the cumulative citaions >= {}, has {} papers".format(Fig1Span[0], Fig1Span[-1], 
                         threshold, len(Fig1SampleSet)))
    
    if (False):
        # 出版后span年的引文积累量
        span = 5                          
        YearSpanDict = dict()
        for Id in Fig1SampleSet:
            totalcount = Paper2CountsDict[Id]
            Y = utils.CoarseGrainedReference(Id, span, Paper2Pubyear, Paper2CitationDict)
            YearSpanDict[Id] = (sum(Y), totalcount)
        # a SPAN2-year span, obtain threshold2 papers
        threshold2 = np.arange(5, 6, 5)  # 挑选在span年处累计引文满足threshold2的画图
        span2 = 5                        # 出版后span + span2年的引文积累量 (灰色区域)
        Fig2SampleSet = list()
        for Id in YearSpanDict:
            if (YearSpanDict[Id][0] in threshold2):
                Fig2SampleSet.append(Id)
        print("cumulative = {} in {} year, has {} papers".format(threshold2, span, len(Fig2SampleSet)))        
        # plot
        plt.figure(figsize=(8, 6))    
        cm = plt.cm.get_cmap('Dark2')
        for Id in Fig2SampleSet:
            Y = utils.CoarseGrainedReference(Id, span + span2, Paper2Pubyear, Paper2CitationDict)
            # Y_cumulative
            Y_cumulative = list()
            for i, _ in enumerate(Y):
                Y_cumulative.append(sum(Y[:i+1]))
            #Y_process = np.log(np.array(Y_cumulative) + 1)
            c = (YearSpanDict[Id][0] - threshold2[0]) / (threshold2[-1] - threshold2[0])
            plt.plot(np.arange(0, span + span2), Y_cumulative, marker='s', c=cm(c))
        # fill gray        
        plt.fill_between(np.arange(span-1, span + span2), [90]*(span2+1), color='lightgray')
        plt.xticks(np.arange(0, span + span2))
        plt.yticks(np.arange(0, 100, 10))
        plt.xlabel('Year')
        plt.ylabel('C(t)')
        # legend
        for i in threshold2:
            c = (i - threshold2[0]) / (threshold2[-1] - threshold2[0])
            plt.plot(0, -1,c=cm(c), label='{}'.format(i), marker='s')
        plt.legend(frameon=False)
    else:
        # 出版后span年的引文积累量
        span = 5                          
        YearSpanDict = dict()
        for Id in Fig1SampleSet:
            totalcount = Paper2CountsDict[Id]
            Y = utils.CoarseGrainedReference(Id, span, Paper2Pubyear, Paper2CitationDict)
            YearSpanDict[Id] = (sum(Y), totalcount)    
        # a SPAN-year span, obtain threshold2 papers
        threshold2 = [5]                # 挑选在span年处累计引文满足threshold2的画图
        Fig2SampleSet = list()
        for Id in YearSpanDict:
            if (YearSpanDict[Id][0] in threshold2):
                Fig2SampleSet.append(Id)
        print("cumulative = {} in {} year, has {} papers".format(threshold2, span, len(Fig2SampleSet)))        
        span2 = 5                   # 出版后span + span2年的引文积累量 (灰色区域)
        # 'introduction', 'method', 'result', 'conclusion', 'others'
        temp = list()
        A = list()
        B = list()
        for Id in Fig2SampleSet:
            total_count = Paper2CountsDict[Id]
            Y = utils.FineGrainedReference(Id, span, Paper2Pubyear, Paper2CitationDict)
            Y_ratio = utils.IntervalRatio(Y)
            Y_1 = utils.CoarseGrainedReference(Id, span, Paper2Pubyear, Paper2CitationDict)
            Y_2= utils.CoarseGrainedReference(Id, span + span2, Paper2Pubyear, Paper2CitationDict)
            # full info
            temp.append((Y_ratio, sum(Y_1), sum(Y_2), total_count))
            # correlation
            A.append(Y_ratio)   # span年时的引用区间比率
            B.append(sum(Y_2))  # span + span2年后的引文数目
            
        utils.MultiCorCoef(A, B)
        
        
        #utils.CorrelationCoefficient([list(np.array(A)[:, 1]), B])
        
'''
Figure S3: Empirical validation of preferential attachment. (different citaion interval)
'''

'''
Figure S4: Empirical validation of the lognormal decay. (different citaion interval)
'''

'''
Figure S7 varying the (λ, µ, σ, ...) parameters, indicating that
model an account for a wide range of citation patterns
'''

'''
Figure S9: Simulating individual citation histories
'''