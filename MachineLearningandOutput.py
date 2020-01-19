#!/usr/bin/env python
# coding: utf-8

# In[78]:


import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import datetime
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
import os
import datetime as DT
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import pitools.pull as Pi
import pitools.push as push
import pitools.ril as r
from numpy import exp, array, random, dot
import schedule
import math

#def Value_Checker():
trainingO = []
trainingS = []
trainingC = []
testS = []
testC = []


#sheet1c0 = pd.read_excel('random.xlsx', sheetname=0, index_col=0)
#sheet1 = pd.read_excel("random.xlsx", sheetname=0)
df = pd.read_excel('random.xlsx')
a = df.loc[:,'a'].values.tolist()
b = df.loc[:,'b'].values.tolist()
c = df.loc[:,'c'].values.tolist()
#df = pandas.read_excel(open('your_xls_xlsx_filename','rb'), sheetname='Sheet 1')

trainingO = a
trainingS = b
trainingC = c
testS = trainingS
testC = trainingC

#Dividing trainingO by its max value to linearize it between 0 and 1
max_valueO = max(trainingO)
#redundant stupid naming stuff for debugging and testing data correctness later on
training_set_output11 = trainingO
training_set_output1 = [i /max_valueO for i in training_set_output11]

#convert to list of lists, This is the data that trains the computer Outputs
training_set_output = [[i] for i in training_set_output1]

#linearzing trainingC
max_valueC = max(trainingC)
inputs111 = trainingC
inputs11 = [i /max_valueC for i in inputs111]

#linearzing trainingS
max_valueS = max(trainingS)
inputs222 = trainingS
inputs22 = [i /max_valueS for i in inputs222]

training_inputs = []

#putting training C and training S into a list of two variable lists This is the data that trains the computer Inputs
#for i in range(0,len(inputs1),2):
for i in range(len(inputs11)):
    a = inputs11[i]
    b = inputs22[i]
    #c = inputs1[i+1]
    #d = inputs2[i+1]
    training_inputs.append([a,b])#,c,d])


#sigmoidal machine learning magic
class NeuralNetwork():
    def __init__(self):
        #sometimes changing the see to 2 or 3 helps with data accuracy
        #random.seed(5)
        self.synaptic_weights = [[-0.1280102 ],[-0.94814754]]#2 * random.random((2, 1)) - 1
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))
    def __sigmoid_derivative(self, x):
        return x * (1 - x)
    def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
        for iteration in range(number_of_training_iterations):
            output = self.think(training_set_inputs)
            error = training_set_outputs - output
            adjustment = dot(training_set_inputs.T, error * self.__sigmoid_derivative(output))
            self.synaptic_weights += adjustment
    def think(self, training_set_inputs):
        return self.__sigmoid(dot(training_set_inputs, self.synaptic_weights))

#runs the machine learning script sorta
if __name__ == "__main__":
    neural_network = NeuralNetwork()
    print("Random starting synaptic weights: ")
    print(neural_network.synaptic_weights)
    training_set_inputs = array(training_inputs)
    training_set_outputs = array(training_set_output)
    neural_network.train(training_set_inputs, training_set_outputs, 100000)
    print("New synaptic weights after training: ")
    print(neural_network.synaptic_weights)
    print("Considering new situation -> ?: ")
    #input_1 = input()
    #input_2 = input()
    #input_1 = float(input_1)
    #input_2 = float(input_2)

    '''training_inputs_test = []'''

#This is the data that goes into the computer to give the outputs
    #CO3 values #S values
    #

    max_valuetestC = max(testC)
    test111 = testC

    #sulfide values
    max_valuetestS = max(testS)
    test222 = testS

    test11 = [j / max_valuetestC for j in test111]

    test22 = [i / max_valuetestS for i in test222]

    for i in range(len(test111)):
        N = neural_network.think(array([test11[i],test22[i]]))
        print(max_valueO*N)

#######################TEST CUSTOM VALUES HERE!!!!!!!!!!!!!#####################
    customtest1 = 2.649438794046759
    customtest2 = 0.647856929128873
    customtest11 = 2.649438794046759/max_valuetestC
    customtest22 = 0.647856929128873/max_valuetestS

############Custom Prediction###################
    print()
    print('Custom Value Prediction:')
    C = neural_network.think(array([customtest11,customtest22]))
    customML = ((max_valueO*C)+70)*0.6
    customOG =(3500*(customtest1-0.9*customtest2)/100)+60
    print((customML+customOG)/2)

#values for YESTERDAY,
    todaysvalueC = max_valuetestC*test11[(len(test111)-1)]
    todaysvalueS = max_valuetestS*test22[(len(test222)-1)]
    todayvalueC = test11[(len(test111)-1)]
    todayvalueS = test22[(len(test222)-1)]


#Machine learning for values each day/today
    M = neural_network.think(array([todayvalueC,todayvalueS]))


    d = {
    's':"AC_LECO_Assay_Surge_Tnk_Sulfide_Wt.%_Man_Hr",
    'c':"AC_LECO_Assay_Surge_Tnk_CO3_Wt.%_Man_Hr",
    'o1':"AC_Acdl_Acid_TTL_Disch_GPM_DCS_Cont",
    'o2':"L_SIMA_AC_Mill_RIL_Feed_Tons_Day",
    'o3':"AC_Acdl_Mass_Feed_to_Acidulation_TPH_DCS_Cont"
    }

# This is pulling data for immediate real time 2 hour predictions in the plant
    s = '*-2h'
    e = '*'
    i = '1m'

    dt = Pi.stream(d , s , e , i, show_status_bar= False).GetSummary()
    j11 = list(dt['c'].values)
    j1 = sum(j11)
    j = (j1/len(j11))
    nowvaluej = j /max_valuetestC

    s = '*-2h'
    e = '*'
    i = '1m'

    dt = Pi.stream(d , s , e , i, show_status_bar= False).GetSummary()
    m11 = list(dt['s'].values)
    m1 = sum(m11)
    m = (m1/len(m11))
    nowvaluei = m /max_valuetestS

    s = '*-10m'
    e = '*'
    i = '1m'

    dt = Pi.stream(d , s , e , i, show_status_bar= False).GetSummary()
    k11 = list(dt['o1'].values)
    k1 = sum(k11)
    k = (k1/len(k11))

    s = '*-10m'
    e = '*'
    i = '1m'

    dt = Pi.stream(d , s , e , i, show_status_bar= False).GetSummary()
    l11 = list(dt['o3'].values)
    l1 = sum(l11)
    l = (l1/len(l11))

    print()

    print('Yesterdays Machine Learning Value Prediction: Acidulation, C, S')

#converting back into meaningful values after the sigmoid
    Todays_Machine_Learning_Prediction = (max_valueO*M+70)*0.6
    print(Todays_Machine_Learning_Prediction)
    print(todaysvalueC)
    print(todaysvalueS)
    print()
    print('Original formula Prediction: Accidulation:')
    Original_Formula =(3500*(todaysvalueC-0.9*todaysvalueS)/100)+60
    print(Original_Formula)
    print()
    print('Merged formula Prediction: Accidulation:')
    Merged_Formula_Prediction = (Original_Formula+Todays_Machine_Learning_Prediction)/2
    Merged_Formula_PredictionGPM = (l*((((Original_Formula + Todays_Machine_Learning_Prediction)/2))/(60*15.37)))

    print(Merged_Formula_Prediction)
    print()

#Predictionlist to put values into a array so that it can be sent out in email or CSV
    #TodaysPredictionlist = max_valueO*M
    #TodaysPrediction = TodaysPredictionlist[0]
######################                           YESTERDAY ACTUAL
    TodayActual = trainingO[len(trainingO)-1]
    TodayActualGPM = (l*((TodayActual))/(60*15.37))
    print('Yesterdays Actual Totalized Acidulation GPT:')
    print(TodayActual)

    #o1 G/minute o3 Tons/hour -----> GPT    Gallons*60/Tons

    Actual_GPT = (k*60*15.37)/l

#Nueral network Right NOW values going in
    RN = neural_network.think(array([nowvaluej,nowvaluei]))
    CurrentML = ((max_valueO*RN)+70)*0.6
    CurrentOG = (3500*(j-0.9*m)/100)+60

#THE REAAAAAAL TIIIIMMMMEE OUTPUT PREDICTION!!!!!!!!!!!
    CurrentPrediction = (CurrentML + CurrentOG)/2
    CurrentPredictionGPM = (l*((CurrentPrediction))/(60*15.37))
    print('Current Merged Formula Prediction Accidulation:')
    print(CurrentPrediction)
    print(CurrentPredictionGPM[0])
    print(j)
    print(m)
    print()
    #print('Current Machine Learning Prediction Accidulation:')


    print('Actual Current Gallons Per Ton:')
    print(Actual_GPT)

#Pushing the OUTPUT to a PITAG for record keeping and displaying
    """Uses API to grab most recent time to allwas keep time updated."""

    time_url = "http://worldtimeapi.org/api/timezone/America/Los_Angeles"
    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "dc63b79d-e386-436d-829a-b50a9b5b7788"
        }

    response = requests.request("GET", time_url, data=payload, headers=headers)
    time_now = datetime.datetime.now()


    z = push.stream()
#     time = z.getTime()
    from datetime import datetime as DT
    from datetime import timedelta
    yesterday = DT.today() - timedelta(days=1)
    time_now1 = time_now - timedelta(hours=7)

    z.PushSingleValue("AC_Acdl_Acid_ML_Pred_YTTL_Disch_GPM_AF" , Merged_Formula_PredictionGPM[0], yesterday)
    #z.PushSingleValue("T_TAIL_Feed_Rasp_Pi_Temperature_F_Man", TodayActual, yesterday)
    z.PushSingleValue("AC_Acdl_Acid_ML_Pred_RLT_Disch_GPTon_AF", Actual_GPT, time_now1)
    z.PushSingleValue("AC_Acdl_Acid_ML_Pred_TTL_Disch_GPM_AF" , CurrentPredictionGPM[0], time_now1)
    print(time_now1)
