# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 11:38:57 2020

@author: 45220
"""
from ReadData import utils
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

IntervalType = utils.ReadJson("IntervalType")
Paper2CitationDict = utils.ReadJson("Paper2CitationDict")
Paper2CountsDict = utils.ReadJson("Paper2CountsDict")
Paper2Pubyear = utils.ReadJson("Paper2Pubyear")

def PieIntervalType(IntervalType):
    '''
    Multiple citation in the same interval are counted once
    The citations in different intervals are calculated separately
    '''
    interval_name = list()
    interval_count = list()
    others = ['case', 'experiment', 'limitation', 'literature', 'background']
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
    PubDistribution = dict()
    for Id in Paper2Pubyear:
        pubyear = Paper2Pubyear[Id]
        if (pubyear not in PubDistribution):
            PubDistribution[pubyear] = 0 
        PubDistribution[pubyear] += 1
    # 1980-2011 obey power law
    ValidYear = np.arange(1980, 2011)
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
    left, bottom, width, height = 0.1,0.1, 1, 1
    ax1 = fig.add_axes([left,bottom,width,height])
    ax1.plot(X, Y, marker='s', c='r')
    ax1.set_yticks(np.arange(0, 25001, 5000))
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Publications per year")
    ax1.yaxis.get_major_formatter().set_powerlimits((0, 1))
    #
    left, bottom, width, height = 0.25, 0.55, 0.5, 0.5
    ax2 = fig.add_axes([left,bottom,width,height])
    ax2.plot(X, Y_cumulative, marker='o', c='r')
    ax2.set_ylabel("log(N(t))")
    # The first three do not participate in linear fitting
    Initiator = 3  
    model = linear_model.LinearRegression()
    model.fit(np.array(X[Initiator:]).reshape(-1, 1), Y_cumulative[Initiator:])
    Y_cumulative_predict = model.predict(np.array(X[Initiator:]).reshape(-1, 1))
    ax2.plot(X[Initiator:], Y_cumulative_predict, linestyle='--', c='black')
    ax2.set_yticks(np.arange(6, 14, 1))

'''
<Quantifying long-term scientific impact>
we replicated their analysis using 5-year citation history to 
predict future citations. We used 1973 Physical Review papers 
published in 1980 that acquired  at least 10 citations in the 
first 5 years. 
'''
for Paper2CitationDict




'''
Figure S2: a 5-year span collect the same number of citations are found to
have widely different long-term impacts. (different citaion interval)
'''

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