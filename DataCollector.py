#!/usr/bin/env python
# coding: utf-8

# In[72]:


__author__ = 'Zachary C Luscher'

import datetime
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import os
import datetime as DT
import pitools.pull as Pi
import pitools.push as push
import pitools.ril as r
from numpy import exp, array, random, dot
import schedule
import time
import math

#import xlrd
#import xlwt
#from xlwt import Workbook
#import xlutils
#from xlutils import copy

# _____________IMPORTS_______________

########################################################

#Plot Size for Debugging
plt.style.use('fivethirtyeight')

# Arbituary Email Array for Sending out Data
Email_value = np.zeros(shape=(365,4))


####### This Pulls Code and Formats it for Machine Learning#######


#########Making an Array of Datetimes in order to pull data from pitools#########
base = datetime.datetime.today()
date_list = [base - datetime.timedelta(days=x) for x in range(0, 730)]

# 0, 730 days to pull data
#Spliting up lists for day month year in order to parse as a string later  
year_list = []
month_list = []
day_list = []

# taking characters from the datetime array and adding them to the lists of days, months, years

for y in range(len(date_list)):
    num = len(date_list)-y-1
    date_list_temp = str(date_list[num])
    year = date_list_temp[0:4]
    year_list.append(year)

    date_list_temp = str(date_list[num])
    month = date_list_temp[5:7]
    month_list.append(month)

    date_list_temp = str(date_list[num])
    day = date_list_temp[8:10]
    day_list.append(day)  

# changing months from numbers to appropriate characters

for y in range(len(month_list)):
    if month_list[y-1] == '01':
        month_list[y-1] = 'jan'
    elif month_list[y-1] == '02':
        month_list[y-1] = 'feb'
    elif month_list[y-1] == '03':
        month_list[y-1] = 'mar'
    elif month_list[y-1] == '04':
        month_list[y-1] = 'apr'
    elif month_list[y-1] == '05':
        month_list[y-1] = 'may'
    elif month_list[y-1] == '06':
        month_list[y-1] = 'jun'
    elif month_list[y-1] == '07':
        month_list[y-1] = 'jul'
    elif month_list[y-1] == '08':
        month_list[y-1] = 'aug'
    elif month_list[y-1] == '09':
        month_list[y-1] = 'sep'
    elif month_list[y-1] == '10':
        month_list[y-1] = 'oct'
    elif month_list[y-1] == '11':
        month_list[y-1] = 'nov'
    else:
        month_list[y-1] = 'dec'

#This is an example format of what I pass throuh Pi.stream
#  str(day_list[1]) + '-' + str(month_list[1]) + '-' + str(year_list[1])


################################ Pulling Data with PiStream  ######################################

#PItagTotalizer()  ####need to have time pulled exactly from 6:00:00 AM to 6:00:00 AM everyday  then sum the list and divide by minutes in day 1440
# here are my PiTags! Sulfide, Carbonate, Acid Flow and Tonage Flow
d = {
    's':"AC_LECO_Assay_Surge_Tnk_Sulfide_Wt.%_Man_Hr",
    'c':"AC_LECO_Assay_Surge_Tnk_CO3_Wt.%_Man_Hr",
    'o1':"AC_Acdl_Acid_TTL_Disch_GPM_DCS_Cont",
    'o2':"L_SIMA_AC_Mill_RIL_Feed_Tons_Day",
    'R':"AC_LECO_Assay_Tnk_606_Disch_A/C_Feed_CO3_Sulfide_Ratio_Man_Hr",
    }

#Making a bunch of lists to use later for Data formatting    
q = 0
trainingO11 = []
trainingO22 = []
trainingS1 = []
trainingC1 = []
testS1 = []
testC1 = []

trainingO1 = []
trainingO2 = []
trainingS = []
trainingC = []
testS = []
testC = []

#For the entirity of the list of dates the data pulled will be in one day intervals

for y in range(len(day_list)-2):
    day1 = day_list[y]
    day2 = day_list[y+1]
    month1 = month_list[y]
    month2 = month_list[y+1]
    year1 = year_list[y]
    year2 = year_list[y+1]

#This is how day 1 and day2 are formated for Pi pulling

    date1 = str(day1) + '-' + str(month1) + '-' + str(year1) + ' 6:00:00'
    date2 = str(day2) + '-' + str(month2) + '-' + str(year2) + ' 6:00:00'

#example: date1: '12-nov-2018 6:00:00'
#         date2: '12-nov-2018 6:00:00'

    #setting time frame for pulling to the dates
    s = str(date1)
    e = str(date2)
    i = '1m'

    #Pulling the data
    dt = Pi.stream(d , s , e , i, show_status_bar= False).GetSummary()
    o1values = list(dt['o1'].values)
    o1value1 = sum(o1values)
    o1value = (o1value1*15.371/2000)  
    trainingO11.append(o1value)

    #The extra str and Pi,stream dont need to be here, not sure why I did that. Just leaving it for now.
    s = str(date1)
    e = str(date2)
    i = '1m'

    dt = Pi.stream(d , s , e , i, show_status_bar= False).GetSummary()
    o2values = list(dt['o2'].values)
    o2value2 = sum(o2values)
    o2value = (o2value2/1440)  
    trainingO22.append(o2value)

    s = str(date1)
    e = str(date2)
    i = '1m'

    dt = Pi.stream(d , s , e , i, show_status_bar= False).GetSummary()
    svalues = list(dt['s'].values)
    svalue1 = sum(svalues)
    svalue = (svalue1/1440)
    trainingS1.append(svalue)
    testS1.append(svalue)

    s = str(date1)
    e = str(date2)
    i = '1m'

    dt = Pi.stream(d , s , e , i, show_status_bar= False).GetSummary()
    cvalues = list(dt['c'].values)
    cvalue1 = sum(cvalues)
    cvalue = (cvalue1/1440)
    trainingC1.append(cvalue)
    testC1.append(cvalue)
    
    s = str(date1)
    e = str(date2)
    i = '1m'

    #just seeing how fast the data is collecting
    q += 1
    print(q)

###############################################################
#Getting rid of the Nan values and making sure each row is deleted in each list of data

nan_index = []
for v in range(0,len(testS1)):
    if not math.isnan(testS1[v]):
        nan_index.append(v) 
for v in range(0,len(nan_index)):
    trainingS.append(trainingS1[nan_index[v]])
for v in range(0,len(nan_index)):
    trainingC.append(trainingC1[nan_index[v]])
for v in range(0,len(nan_index)):
    trainingO1.append(trainingO11[nan_index[v]])
for v in range(0,len(nan_index)):
    trainingO2.append(trainingO22[nan_index[v]])
for v in range(0,len(nan_index)):
    testS.append(testS1[nan_index[v]])
for v in range(0,len(nan_index)):
    testC.append(testC1[nan_index[v]])

#################################################################    

#Need to eliminate Nan and inf and Zeros while keeping integrity of the lists.####   
#
#
#Replace the removed values with something negligble# <--- This doesn't work unless I have a totalized average

#This Finds the MAX and MIN in the TrainingS and TrainingC then orders them so the indices are lined up and deleted back to front
#Then it deletes the index of every list so they match, this could cause some problems with matching the graph precisly.

print(trainingS)
print(trainingC)

#Removes 10 mins and 10 maxs from the training data # first finds the mins and maxes for both Sulfides and Carbonates
for n in range(5):
    minposS = trainingS.index(min(trainingS))
    maxposS = trainingS.index(max(trainingS)) 
    minposC = trainingC.index(min(trainingC))
    maxposC = trainingC.index(max(trainingC))

#stores min max in list
    templist = []
    temp_list = []

    templist.append(minposS)
    templist.append(maxposS)
    templist.append(minposC)
    templist.append(maxposC)

#then orders the min max values so that they dont delineate the data.
#indcies of the maxyiest max is first then minniest min last
#finds index of max and puts it in new list hopefully in order
    max_index = templist.index(max(templist)) 
    temp_list.append(templist.pop(max_index))

    max_index = templist.index(max(templist)) 
    temp_list.append(templist.pop(max_index))

    max_index = templist.index(max(templist)) 
    temp_list.append(templist.pop(max_index))

    max_index = templist.index(max(templist)) 
    temp_list.append(templist.pop(max_index))

#This gets rid of duplicates and keeps them in order. have to do it twice to keep it nice. actually though, its weird
    temp_list = list(dict.fromkeys(temp_list))
    temp_list = list(dict.fromkeys(temp_list))

#debugging
    #print(temp_list)

#This finally removes mins and maxes starting with the largest index of the mins and maxs and goes to the smallest index
    for n in range(len(temp_list)):

#making sure all of the lists are the same and even.
        testC.remove(testC[temp_list[n-2]])
        testS.remove(testS[temp_list[n-2]])
        trainingO2.remove(trainingO2[temp_list[n-2]])
        trainingO1.remove(trainingO1[temp_list[n-2]])
        trainingS.remove(trainingS[temp_list[n-2]])
        trainingC.remove(trainingC[temp_list[n-2]])

#making sure we don't delete indexes we already deleted next time the loop runs
    temp_list.clear
    templist.clear
    #max_index.clear    

temp_list1 = []
q = 0

#This gets rid of the zeros in trainingO2 so be dont divide by zero!!! Make sure we delete the other rows of other lists so they are all lined up still
for n in range(len(trainingO2)):
    if trainingO2[n-1] == 0.0 :
        temp_list1.append(n-1)

        testC.remove(testC[n-1])
        #testC[n-1] = 1 
        testS.remove(testS[n-1])
        #testS[n-1] = 1

        trainingC.remove(trainingC[n-1])
        #trainingC[n-1] = 1
        trainingS.remove(trainingS[n-1])
        #trainingS[n-1] = 1
        trainingO1.remove(trainingO1[n-1])
        #trainingO1[n-1] = 30


for p in range(len(temp_list1)):
    trainingO2.remove(trainingO2[temp_list1[p]-q])
    #trainingO2[temp_list2[p]-q] = 10000
    q += 1


#finally combinging trainingO1 and trainingO2 into trainingO!!!!!!!
trainingO = []
for i in range(len(trainingO1)):
    trainingO.append((trainingO1[i])*2000/(trainingO2[i]))

#Opens Existing random.xls workbook and adds values into the columns of sheet1 appropriatly then saves
####### THIS DON"T WORK INVALID SYNTAX, MIHGT have to use pandas


df = pd.DataFrame({'a' : trainingO, 'b' : trainingS, 'c' : trainingC})
writer = pd.ExcelWriter('random.xlsx')
df.to_excel(writer,'Sheet1',index=False)
writer.save()
print(trainingO2)
print(df)


# In[ ]:




