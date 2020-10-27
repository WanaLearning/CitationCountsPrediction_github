# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 11:24:56 2020

@author: 45220
"""
import json


def SaveJson(file, filename):
    with open("./" + filename, 'w') as f:
        json.dump(file, f)

        
def ReadJson(filename):
    with open('./' + filename, 'r') as f:
        file = json.load(f)
    return file
