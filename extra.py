# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 11:13:44 2023

@author: Michael P Mariani PhD

################### COPYRIGHT ######################
#Copyright (c) 2023, Mariani Systems LLC
#  All rights reserved.
#
#This source code is licensed under the license found in the
#LICENSE file in the root directory of this source tree. 
####################################################

"""

#Extra stuff for the QBS APP

#Now double check if matching faculty time is good
    
#appsAvailDf.iloc[:,2:9]
#facTime
#check time conflict:
        
#print(appsFacAlumDf.columns)
#print(appsAvailDf.columns)
#print(facAlumAvailDf.columns)

#print([facAlumAvailDf["Your name"], facAlumAvailDf['availMore5']])

#load times and dates txt file to be used as
#the first output column in the final .xlsx

#outDateTimeDf=pd.read_csv('G:/My Drive/mariani_systems_2022/'\
#                 'qbs_app_project/times_and_dates.txt',\
#                 sep=' ',\
#                 header=None)
#outDateTimeDf = outDateTimeDf.fillna('')
#outDateTimeDf[3] = outDateTimeDf[0].map(str) + \
#outDateTimeDf[1].map(str) + outDateTimeDf[2].map(str) 
#outDateTimeDf = outDateTimeDf[3]


####################### PLOTS #####################################
###################################################################

# function to add value labels
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i],ha='center')
        
##################### AC plot1 ####################################

import matplotlib.pyplot as plt

#xAxis = facAlumAvailDf["Your name"]
#yAxis = facAlumAvailDf['availMore5']
#plt.bar(xAxis, yAxis)
#plt.title('Available for more than 5?')
#plt.xlabel('Faculty or Alumni')
#plt.ylabel('Is available (bool)')
#plt.show()

summaryDf = pd.read_excel(inputPath,
                           sheet_name=3)
summaryDf.columns = summaryDf.columns.map(str)
        
#xAxis = facAlumAvailDf["Alums"]
#yAxis = facAlumAvailDf['#']
#plt.bar(xAxis, yAxis)
#plt.title('Alums Counts')
#plt.xlabel('Alum')
#plt.ylabel('Count')
#plt.show()
summaryDf = summaryDf.dropna()
xAxis = summaryDf['AC']
yAxis = pd.to_numeric(summaryDf['#_2'],errors='coerce')
plotDf = pd.DataFrame({'Alum': xAxis, 'Count': yAxis})
#plotDf = pd.DataFrame([[xAxis],[yAxis]],
 #                     columns=['Alum',"Count"])
#plotDf.plot.bar()
plt.bar(plotDf['Alum'],plotDf['Count'])
plt.xticks(rotation=45)
plt.title('Alums Counts')
plt.xlabel('Alum')
plt.ylabel('Count')
plt.gcf().subplots_adjust(bottom=0.50)
#ax = sns.countplot(x="Count", data=plotDf)
#for p in ax.patches:
#   ax.annotate('{:.1f}'.format(p.get_height()), (p.get_x()+0.25, p.get_height()+0.01))
addlabels(plotDf['Alum'],plotDf['Count'])
sns.despine(top=True, right=True, left=False, bottom=False)
#for container in ax1.containers:
#    ax1.bar_label(container, label_type='center', rotation=90, color='white')
plt.savefig('Alum_Counts.png')
plt.show()

##################### Faculty plot ####################################


##################### Plotting 3 ####################################