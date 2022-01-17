#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import numpy as np
import seaborn as sn

import matplotlib.pyplot as plt


# In[20]:


#create cards <labels> for 13x13 range matrix
ranks = ['2','3','4','5','6','7','8','9','T','J','Q','K','A'][::-1]
suits = ["s","o"]
labels = np.empty(shape=(13,13),dtype="<U16")
for i, c1 in enumerate(ranks):
    for j, c2 in enumerate(ranks):
        if i < j:            
            hand= c1+c2+"s"
            labels[i][j]=hand
        elif i > j:                    
            hand= c2+c1+"o"
            labels[i][j]=hand
        elif i == j:
            hand= c1+c2            
            labels[i][j]=hand
        else:
            continue

#create a global dict <idxmap> mapping hand as a string to tuple of numbers between 0 and 12

idxmap = {}
for i, c1 in enumerate(ranks):
    for j, c2 in enumerate(ranks):
        if i < j:            
            for s in suits:
                hand = c1+c2+s
                if s == "s":
                    idxmap [hand] = (i,j)
                    
                else:
                    idxmap [hand] = (j,i)
                   
        elif i == j:
            hand = c1+c2
            idxmap [hand] = (i,j)
            
        else:
            continue


# In[16]:


class Range:
    """
    Get a starting range as a string in Flopzilla format and display visualization
    """
    def __init__(self, str_, title = ""):
        self.str_ = str_
        self.label = title
        self.weights, self.hands = self.string2list(self.str_)
        self.matrix = self.list2matrix(self.weights,self.hands)    
    
    def string2list(self, r):        
        range_list = r.replace(" ", "").split(",")
        weights = list()
        hands = list()
        for rge in range_list:
            weights_pattern = re.compile(r"\d+\.\d")        
            if weights_pattern.search(rge) is not None:
                weights.append(float(weights_pattern.search(rge).group()))
                hand_pattern = re.compile(r"\][23456789TJQKA][23456789TJQKA](o|s)?")
                hands.append(str(hand_pattern.search(rge).group()[1:]))
            else:                
                weights.append(100.0)
                hand_pattern = re.compile(r"[23456789TJQKA][23456789TJQKA](o|s)?")
                hands.append(str(hand_pattern.search(rge).group()))
                
        return weights, hands

    def list2matrix(self, weights, hands):
        matrix = np.zeros(shape=(13,13), dtype=np.float64)
        for ix, val in enumerate(hands): 
            hand_idx = idxmap[val]
            matrix[hand_idx[0]][hand_idx[1]]+= weights[ix]/100
        return matrix
    
    def displayRange(self): 
        plt.rcParams['figure.figsize'] = (10.0, 10.0)
        g = sn.heatmap(self.matrix,annot=labels,cmap="YlOrBr",vmin=-0, vmax=1.0, fmt = '',linewidths=.5,square=True)#           
        #g.set(xticklabels=ranks)
        #g.set(yticklabels=ranks)
        g.set(xticklabels=[])
        g.set(yticklabels=[])       
        
        g.xaxis.tick_top()
        g.title.set_position([.5, 1.1])
        plt.title(self.label)
        #plt.yticks(rotation=0)
        plt.show()

