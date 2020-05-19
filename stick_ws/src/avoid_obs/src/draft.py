#!/usr/bin/env python
from itertools import *
from operator import itemgetter
import numpy as np
#range_mask=[False,True,True,True,True,False,True,True,True,False,False,True,True]
THRESHOLD=1
scan_filter=[4,4,55,66,7,8,9,13,2,7,0,9,9,0,0,9,8]
counter=0
for i in range(len(scan_filter)):
    if(scan_filter[i]<50):
        counter+=1
print(counter)
range_angels = np.arange(len(scan_filter))
ranges = np.array(scan_filter)
range_mask = (ranges > THRESHOLD)
    
#print(range_mask)    
for j in range(1,len(range_mask)-1):
        
    if ((range_mask[j]==False) and (range_mask[j-1]==True) and (range_mask[j+1]==True)):
        range_mask[j]=True
print(range_mask)


ranges = list(range_angels[range_mask])
print(ranges)
gap_list=[]
for k, g in groupby(enumerate(ranges), lambda (i,x):i-x):
    gap_list.append(map(itemgetter(1), g))


print(gap_list)  


for index in range(len(gap_list)-1):

    if (abs(gap_list[index][-1]-gap_list[index+1][0])<=3):
        range_mask[gap_list[index][-1]+1]=True
        range_mask[gap_list[index][-1]+2]=True


ranges = list(range_angels[range_mask])
gap_list_final=[]
for k, g in groupby(enumerate(ranges), lambda (i,x):i-x):
    gap_list_final.append(map(itemgetter(1), g))

gap_list_final.sort(key=len)
print(gap_list_final)
largest_gap = gap_list_final[-1]
print(largest_gap)
