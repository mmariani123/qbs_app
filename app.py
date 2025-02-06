
####### for running in local web browser ###############
import nest_asyncio
nest_asyncio.apply()
########################################################

####### for functions ##################################
import os
import pandas as pd
import numpy as np
import xlsxwriter
########################################################

################### For Shiny ##########################
import urllib.request
from pathlib import Path

import duckdb
from query import query_output_server, query_output_ui
from shiny import App, reactive, ui
#######################################################

app_dir = Path(__file__).parent
db_file = app_dir / "weather.db"


def load_csv(con, csv_name, table_name):
    csv_url = f"https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2022/2022-12-20/{csv_name}.csv"
    local_file_path = app_dir / f"{csv_name}.csv"
    urllib.request.urlretrieve(csv_url, local_file_path)
    con.sql(
        f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{local_file_path}')"
    )


if not Path.exists(db_file):
    con = duckdb.connect(str(db_file), read_only=False)
    load_csv(con, "weather_forecasts", "weather")
    load_csv(con, "cities", "cities")
    con.close()

con = duckdb.connect(str(db_file), read_only=True)

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_action_button("add_query", "Upload schedule file", class_="btn btn-primary"),
        ui.input_action_button(
            "get_matches", "Get Matches!", class_="btn btn-secondary"
        ),
        ui.input_action_button(
            "show_meta", "Dowload Results", class_="btn btn-secondary"
        ),
        ui.markdown(
            """
            This App is for matching QBS applicants with desired faculty and alumni
            """
            #This app lets you explore a dataset using SQL and duckdb.
            #The data is stored in an on-disk [duckdb](https://duckdb.org/) database,
            #which leads to extremely fast queries.
        ),
    ),
    ui.tags.div(
        query_output_ui("initial_query", remove_id="initial_query"),
        id="module_container",
    ),
    #title="DuckDB query explorer",
    title="QBS App for Krissy",
    class_="bslib-page-dashboard",
)


def server(input, output, session):
    
    
    ##################### INPUTS ###################################
    
    inputPath='input_mm.xlsx'
    appsFacAlumDf = pd.read_excel(inputPath,
                               sheet_name=0)
    appsFacAlumDf.columns = appsFacAlumDf.columns.map(str)

    facDesiredCounts = appsFacAlumDf["AC"].value_counts()
    Num1DesiredCounts = appsFacAlumDf["1"].value_counts()
    Num2DesiredCounts = appsFacAlumDf["2"].value_counts()

    appsAvailDf = pd.read_excel(inputPath,
                          sheet_name=1)
    
    facAlumAvailDf = pd.read_excel(inputPath,
                              sheet_name=2)
    
    summaryDf = pd.read_excel(inputPath,
                              sheet_name=3)
    
    ####################### MAIN ALGORITHM ##########################
    
    #Applicant times:
    appTimesAll = ['Before8',
                '9-10am',
                '10-11am',
                '11-12pm',
                '12-1pm',
                '1-2pm',
                '2-3pm',
                '3-4pm',
                '4-5pm',
                'After5']

    #Faculty times
    facTimesAll = ['Before8',
                'Morning',
                'Afternoon',
                'After8']
    
    ################### Go through appplicants
    #print(len(appsFacAlumDf["Student"]))
    #56 applicants total

    apps = appsFacAlumDf["Student"].sample(frac=1)
    #print(apps)

    #Let's start by creating the final
    #output matching 3d array and
    #randomly shuffling the applicant pool

    allFacultyQuestion = [
    'Christian Darab',
    'Josh Levy',
    'Rob Frost',
    'Student Gr #1',
    'David Chen',
    'Brock Christianson',
    'Meghan Muse	',
    'Ronnie Zipkin',
    'Diane Gilbert-Diamond',
    'Jiang Gui',
    'Carly Bobak',
    'Possible Student group',
    'Diane Gilbert-Diamond',
    'Alfredo',
    'Tor Tosteson',
    'Jeremiah Brown',
    'Student Gr. #2',
    'Elle Palmer',
    'George Price',
    'David Qian',
    'Soroush Vosoughi',
    'Britt Goods	',
    'Aaron McKenna',
    'Student Gr. #3',
    'Jennifer Franks',
    'Yuka Moroishi',
    'Catherine Pollack',
    'Anne Hoen']
    			
    allFaculty = [
    'Aaron McKenna',
    'jiang gui',
    'Lucas Salas',
    'Rob Frost',
    'Joshua Levy',
    'Jennifer Emond',
    'Annie Hoen',
    'Erika',
    'Ben Ross',
    'Eugene Demidenko',
    'Britt Goods',
    'Wesley Marrero',
    'Scott',
    'Kenneth Hoehn',
    'Li Song',
    'Megan Romano',
    'Caitlin Howe',
    'Mike Passarelli',
    'Alfredo',
    'Siming Zhao',
    'Nick Jacobson',
    'todd mackenzie',
    'Tor Tosteson',
    'Daniel Schultz',
    'Michael Whitfield',
    'jay dunlap',
    'Brock Christensen',
    'Ramesh Yapalparvi',
    "James O'Malley",
    'Diane Gilbert-Diamond',
    'Margie Ackerman',
    'Jiwon Lee',
    'Jeremiah Brown', 
    'Carly Bobak',
    'Ben Ross']

    allAlum = [
    'Yuka Moroishi',
    'David Qian',
    'Iben Sullivan (Ricket)',
    'Sara Lundgren',
    'Christiaan Rees',
    'Catherine Pollack']

    allFacAlum = allFaculty + allAlum

    allTimes = ['8:00-8:30',
    '8:30-9:00',
    '9:00-9:30',
    '9:30-10:00',
    '10:00-10:30',
    '10:30-11:00',
    '11:00-11:30',
    '11:30-12:00',
    '12:00-12:30',
    '12:30-1:00',
    '1:00-1:30',
    '1:30-2:00',
    '2:00-2:30',
    '2:30-3:00',
    '3:00-3:30',
    '3:30-4:00',
    '4:00-4:30',
    '4:30-5:00']

    allDays = [
        'Monday, January 16',
        'Tuesday, January 17',
        'Wednesday, January 18',
        'Thursday, January 19',
    	'Friday, January 20']

    len(allFacAlum) #41
    len(allTimes) #18
    len(allDays) #5
    #18*5=90
    
    ###########################################################################

    #Ben Ross was included twice in input sheet

    allAvailFacTimes = facAlumAvailDf.drop(facAlumAvailDf.columns[[1,2,3,4,10,11,12,13,14,15]],axis=1)
    allAvailFacTimes = pd.melt(allAvailFacTimes, 
                               id_vars='Your name', 
                               value_vars=allAvailFacTimes.columns[1:],
                               var_name="day",
                               value_name="time")
    allAvailFacTimes.replace('morning', '8:00-8:30, 8:30-9:00, 9:00-9:30, 9:30-10:00, 10:00-10:30, 10:30-11:00, 11:00-11:30, 11:30-12:00', inplace=True)
    allAvailFacTimes.replace('afternoon','12:00-12:30, 12:30-1:00, 1:00-1:30, 1:30-2:00, 2:00-2:30, 2:30-3:00, 3:00-3:30, 3:30-4:00, 4:00-4:30, 4:30-5:00', inplace=True)
    allAvailFacTimes.replace('morning, afternoon','8:00-8:30, 8:30-9:00, 9:00-9:30, 9:30-10:00, 10:00-10:30, 10:30-11:00, 11:00-11:30, 11:30-12:00, 12:00-12:30, 12:30-1:00, 1:00-1:30, 1:30-2:00, 2:00-2:30, 2:30-3:00, 3:00-3:30, 3:30-4:00, 4:00-4:30, 4:30-5:00', inplace=True)

    newTimesFrame = allAvailFacTimes.time.str.split(", ", expand = True)
    allAvailFacTimes = pd.concat([allAvailFacTimes, newTimesFrame], axis=1)
    allAvailFacTimes = allAvailFacTimes.drop(columns='time')
    allAvailFacTimes = pd.melt(allAvailFacTimes, 
                               id_vars=['Your name','day'], 
                               value_vars=allAvailFacTimes.columns[2:],
                               var_name="slot",
                               value_name="time")
    allAvailFacTimes = allAvailFacTimes.drop(columns='slot')
    allAvailFacTimes.loc[:,"applicant"] = "open"
    allAvailFacTimes.columns.values[0] = 'faculty'
    #Drop rows with NA in time:
    allAvailFacTimes.dropna(inplace=True)

    finalDf = allAvailFacTimes.copy()

    finalDf['ofaculty'] = pd.Categorical(finalDf.faculty, 
                                         ordered=True, 
                                         categories=facAlumAvailDf['Your name'])

    finalDf['oday'] = pd.Categorical(finalDf.day, 
                                         ordered=True, 
                                         categories=allDays)

    finalDf['otime'] = pd.Categorical(finalDf.time, 
                                         ordered=True, 
                                         categories=allTimes)

    finalDf = finalDf.sort_values(by=['ofaculty','oday'])

    finalDf.drop('ofaculty', axis=1, inplace=True)
    finalDf.drop('oday', axis=1, inplace=True)
    finalDf.drop('otime', axis=1, inplace=True)

    finalDf.reset_index(inplace=True, drop=True)

    appsPoints = dict.fromkeys(apps.array,0)

    facs = allAvailFacTimes['faculty'].values
    facsAssignNums = dict.fromkeys(facs,0)
    
    ################### Search for faculty 1 ################################
    #########################################################################
    #########################################################################
    #########################################################################
    #########################################################################

    #print("\n\n\n\n\n fac 1 \n\n\n\n\n ")

    facTimes1 = []
    for i in appsPoints.keys():
        #print(i)
        fac1 = appsFacAlumDf.loc[(appsFacAlumDf['Student'] == i),\
                                 ["1"]].iloc[0,0]
        
        #If fac1 isn't listed (is na) or is not included in faculty list
        #select their fac2 as fac1
        if((pd.isna(fac1)) | (facsAssignNums.get(fac1) is None)):
            fac1 = appsFacAlumDf.loc[(appsFacAlumDf['Student'] == i),\
                                     ["2"]].iloc[0,0]
        
        #If fac already has 5, move on
        if(facsAssignNums[fac1]>=5):
            continue
        
        appTimes = appsAvailDf.drop(appsAvailDf\
                                    .columns[[1,7,8,9,10,11,12]],axis=1)\
                                    .loc[(appsAvailDf['Your Name'] == i)]
        
        facTimes = facAlumAvailDf.drop(facAlumAvailDf\
                                       .columns[[1,2,3,4,10,11,12,13,14,15]],
                                       axis=1)\
                                    .loc[(facAlumAvailDf['Your name'] == fac1)]
        
        #Check if first faculty is even available
        if(not facTimes.empty):
            #now suset days and check first available:
            #print(appTimes)
            #print(facTimes)
            #replace morning and afternoon with list of times above
            #in faculty avail df to do precise matching
            facTimes.replace('morning',
            '8:00-8:30, 8:30-9:00, 9:00-9:30, 9:30-10:00, 10:00-10:30, \
            10:30-11:00, 11:00-11:30, 11:30-12:00', 
            inplace=True)
            
            facTimes.replace('afternoon',
            '12:00-12:30, 12:30-1:00, 1:00-1:30, 1:30-2:00, 2:00-2:30, \
            2:30-3:00, 3:00-3:30, 3:30-4:00, 4:00-4:30, 4:30-5:00', 
            inplace=True)
            
            facTimes.replace('morning, afternoon',
            '8:00-8:30, 8:30-9:00, 9:00-9:30, 9:30-10:00, 10:00-10:30, \
            10:30-11:00, 11:00-11:30, 11:30-12:00, 12:00-12:30, 12:30-1:00, \
            1:00-1:30, 1:30-2:00, 2:00-2:30, 2:30-3:00, 3:00-3:30, 3:30-4:00, \
            4:00-4:30, 4:30-5:00', 
            inplace=True)
            
            #Also can add After5 here ...
            for column in facTimes.columns[1:]:
                #print(facTimes[column])
                #print(appTimes[column])
                if(not facTimes[column].isnull().values.any()):
                    print('hi')
                    if(not appTimes.isnull().values.any()):
                        print('yo')
                        facTimesSplit = facTimes[column].str.split(', ')
                        appTimesSplit = appTimes[column].str.split(', ')
                    
                        facTimesSplit = facTimesSplit.tolist()[0]
                        #Breakup applicant times into half hours:
                        
                        #appTimesSplit = re.sub('8-9am', '8:00-8:30, 8:30-9:00', appTimesSplit)
                        #appTimesSplit = re.sub['9-10am', '9:00-9:30, 9:30-10:00' appTimesSplit]
                        #appTimesSplit = re.sub['10:00-10:30, 10:30-11:00' for "10-11am" in appTimesSplit]
                        #appTimesSplit = re.sub['11:00-11:30, 11:30-12:00' for "11-12pm" in appTimesSplit]
                        #appTimesSplit = re.sub['12:00-12:30, 12:30-1:00' for "12-1pm" in appTimesSplit]
                        #appTimesSplit = re.sub['1:00-1:30, 1:30-2:00' for "1-2pm" in appTimesSplit]
                        #appTimesSplit = re.sub['2:00-2:30, 2:30-3:00' for "2-3pm" in appTimesSplit]
                        #appTimesSplit = re.sub['3:00-3:30, 3:30-4:00' for "3-4pm" in appTimesSplit]
                        #appTimesSplit = re.sub['4:00-4:30, 4:30-5:00' for "4-5pm" in appTimesSplit]
                        
                        appTimesSplit = appTimesSplit.tolist()[0]
                        appTimesSplit = [sub.replace('8-9am', '8:00-8:30, 8:30-9:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('9-10am', '9:00-9:30, 9:30-10:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('10-11am', '10:00-10:30, 10:30-11:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('11-12pm', '11:00-11:30, 11:30-12:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('12-1pm', '12:00-12:30, 12:30-1:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('1-2pm', '1:00-1:30, 1:30-2:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('2-3pm', '2:00-2:30, 2:30-3:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('3-4pm', '3:00-3:30, 3:30-4:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('4-5pm', '4:00-4:30, 4:30-5:00') for sub in appTimesSplit]
                        
                        appTimesSplit = [i.split(', ') for i in appTimesSplit] 
                        #flatten the above list:
                        appTimesSplit = [item for sublist in appTimesSplit for item in sublist]
                        #appTimesSplit.loc[appTimesSplit=="8-9am"] = '8:00-8:30, 8:30-9:00'
                        #appTimesSplit.loc[appTimesSplit=="9-10am"] = '9:00-9:30, 9:30-10:00'
                        #appTimesSplit.loc[appTimesSplit=="10-11am"] = '10:00-10:30, 10:30-11:00'
                        #appTimesSplit.loc[appTimesSplit=="11-12pm"] = '11:00-11:30, 11:30-12:00'
                        #appTimesSplit.loc[appTimesSplit=="12-1pm"] = '12:00-12:30, 12:30-1:00'
                        #appTimesSplit.loc[appTimesSplit=="1-2pm"] = '1:00-1:30, 1:30-2:00'
                        #appTimesSplit.loc[appTimesSplit=="2-3pm"] = '2:00-2:30, 2:30-3:00'
                        #appTimesSplit.loc[appTimesSplit=="3-4pm"] = '3:00-3:30, 3:30-4:00'
                        #appTimesSplit.loc[appTimesSplit=="4-5pm"] = '4:00-4:30, 4:30-5:00'
                    
                        #look for intersection and take first instance of intersection
                        olap = list(set(facTimesSplit) & set(appTimesSplit))
                        #print(olap)
                        if(bool(olap)==True):
                            print('sup')
                            #Check if slot is already assigned in final sheet,
                            #if not, Assign the first available overlap to the final sheet
                            for check in range(len(olap)):
                                #exit()
    ############## major if case here ###########################################                            
                                #check present time slot:
                                checkPresent = (finalDf[(finalDf['faculty']==fac1) & (finalDf['time']==olap[check]) & (finalDf['day']==column)]['applicant'].to_string(index=False) == 'open') & (appsPoints[i] < 2)
                                #get row index of current time slot
                                currentIndex = finalDf.index[(finalDf['faculty']==fac1) & (finalDf['time']==olap[check]) & (finalDf['day']==column)].values[0]
                                #check 1/2 hour after 8 and 1/2 hour before 5:
                                checkBefore = (not ((finalDf.iloc[currentIndex]['applicant'] == '8:00-8:30') & (finalDf.iloc[currentIndex+1]['applicant'] != 'open')))
                                checkAfter = (not ((finalDf.iloc[currentIndex]['applicant'] == '4:30-5:00') & (finalDf.iloc[currentIndex-1]['applicant'] != 'open')))
                                checkInBetween = ((finalDf.iloc[currentIndex]['applicant'] != '8:00-8:30') & (finalDf.iloc[currentIndex]['applicant'] != '4:30-5:00') & (finalDf.iloc[currentIndex-1]['applicant'] == 'open') & (finalDf.iloc[currentIndex+1]['applicant'] == 'open'))
                                if((checkPresent) & (checkBefore) & (checkAfter) & (checkInBetween)):
                                    print('assigning')
                                    #exit()
                                    #print(olap[check])
                                    finalDf.loc[(finalDf['faculty']==fac1) &\
                                            (finalDf['time']==olap[check]) &\
                                            (finalDf['day']==column),
                                            ['applicant']] = i
                                    appsPoints[i]+=1
                                    facsAssignNums[fac1]+=1
                                    selectDf = finalDf.loc[(finalDf['faculty']==fac1) &\
                                            (finalDf['time']==olap[check]) &\
                                            (finalDf['day']==column) &\
                                            (finalDf['applicant']==i)]
                                    print(selectDf['applicant'].to_string(index=False) + ',\t' +\
                                            selectDf['faculty'].to_string(index=False) + ',\t' +\
                                            selectDf['day'].to_string(index=False) + ',\t' +\
                                            selectDf['time'].to_string(index=False))
                                    vals = selectDf.astype(str).values.flatten().tolist()
                                    stringOut = ';\t'.join(map(str,vals))
                                    facTimes1.append(stringOut)
                                    break
                            else:
                                continue
                            break
                             
                                #for check in range(len(olap)):
                                #    if(any(finalDf['faculty'].str.match(fac1)) & any((finalDf['time'].str.match(olap[check]))) & any((finalDf['day'].str.match(column))) & any((finalDf['applicant']==i))):
                                #        #print('already assigned')
                                #        next
                                #    else:
                                #        print(olap[check])
                                #        finalDf.loc[(finalDf['faculty']==fac1) &\
                                #            (finalDf['time']==olap[check]) &\
                                #            (finalDf['day']==column),
                                #            ['applicant']] = i
                                #        appsPoints[i]+=1
                                #        break

    #Output fac1 matches file:
    if os.path.exists("fac1.txt"):
        os.remove("fac1.txt")

    with open('fac1.txt', 'w') as f1:
        f1.write('\n'.join([str(x) for x in facTimes1]))
    f1.close()    
    
########################### Search for faculty 2 ###########################
############################################################################
############################################################################
############################################################################
############################################################################

#print("\n\n\n\n\n fac 2 \n\n\n\n\n ")

    facTimes2 = []
    for i in appsPoints.keys():
        #print(i)
        #selected = [appsFacAlumDf['Student'==i,'1'],appsFacAlumDf['Student'==i,"2"]]
        #appsList.append(appsFacAlumDf.loc[(appsFacAlumDf['Student'] == i),["1","2"]])
        #Find first faculty:
        fac2 = appsFacAlumDf.loc[(appsFacAlumDf['Student'] == i),["2"]].iloc[0,0]
    
        #If fac1 isn't listed (is na) or is not included in faculty list
        #select their fac2 as fac3 or just skip
        if((pd.isna(fac2)) | (facsAssignNums.get(fac2) is None)):
            #fac2 = appsFacAlumDf.loc[(appsFacAlumDf['Student'] == i),["3"]].iloc[0,0]
            continue
    
        #If fac already has 5, move on
        if(facsAssignNums[fac2]>=5):
            continue
    
        appTimes = appsAvailDf.drop(appsAvailDf.columns[[1,7,8,9,10,11,12]],axis=1).loc[(appsAvailDf['Your Name'] == i)]
        facTimes = facAlumAvailDf.drop(facAlumAvailDf.columns[[1,2,3,4,10,11,12,13,14,15]],axis=1).loc[(facAlumAvailDf['Your name'] == fac2)]
        #Check if first faculty is even available
        if(not facTimes.empty):
            #now suset days and check first available:
            #print(appTimes)
            #print(facTimes)
            #replace morning and afternoon with list of times above
            #in faculty avail df to do precise matching
            facTimes.replace('morning', '8:00-8:30, 8:30-9:00, 9:00-9:30, 9:30-10:00, 10:00-10:30, 10:30-11:00, 11:00-11:30, 11:30-12:00', inplace=True)
            facTimes.replace('afternoon','12:00-12:30, 12:30-1:00, 1:00-1:30, 1:30-2:00, 2:00-2:30, 2:30-3:00, 3:00-3:30, 3:30-4:00, 4:00-4:30, 4:30-5:00', inplace=True)
            facTimes.replace('morning, afternoon','8:00-8:30, 8:30-9:00, 9:00-9:30, 9:30-10:00, 10:00-10:30, 10:30-11:00, 11:00-11:30, 11:30-12:00, 12:00-12:30, 12:30-1:00, 1:00-1:30, 1:30-2:00, 2:00-2:30, 2:30-3:00, 3:00-3:30, 3:30-4:00, 4:00-4:30, 4:30-5:00', inplace=True)
            #Also can add After5 here ...
            for column in facTimes.columns[1:]:
                #print(facTimes[column])
                #print(appTimes[column])
                if(not facTimes[column].isnull().values.any()):
                    #check if app time is NA
                    if(not appTimes.isnull().values.any()):
                        facTimesSplit = facTimes[column].str.split(', ')
                        appTimesSplit = appTimes[column].str.split(', ')
                
                        facTimesSplit = facTimesSplit.tolist()[0]
                        #Breakup applicant times into half hours:
                    
                        appTimesSplit = appTimesSplit.tolist()[0]
                        appTimesSplit = [sub.replace('8-9am', '8:00-8:30, 8:30-9:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('9-10am', '9:00-9:30, 9:30-10:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('10-11am', '10:00-10:30, 10:30-11:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('11-12pm', '11:00-11:30, 11:30-12:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('12-1pm', '12:00-12:30, 12:30-1:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('1-2pm', '1:00-1:30, 1:30-2:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('2-3pm', '2:00-2:30, 2:30-3:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('3-4pm', '3:00-3:30, 3:30-4:00') for sub in appTimesSplit]
                        appTimesSplit = [sub.replace('4-5pm', '4:00-4:30, 4:30-5:00') for sub in appTimesSplit]
                    
                        appTimesSplit = [i.split(', ') for i in appTimesSplit] 
                        #flatten the above list:
                        appTimesSplit = [item for sublist in appTimesSplit for item in sublist]
                
                        #look for intersection and take first instance of intersection
                        olap = list(set(facTimesSplit) & set(appTimesSplit))
                        #print(olap)
                        if(bool(olap)==True):
                            #Check if slot is already assigned in final sheet,
                            #if not, Assign the first available overlap to the final sheet
                            for check in range(len(olap)):
                                #exit()
############## major if case here ###########################################                            

                                #check present time slot:
                                checkPresent = (finalDf[(finalDf['faculty']==fac2) & (finalDf['time']==olap[check]) & (finalDf['day']==column)]['applicant'].to_string(index=False) == 'open') & (appsPoints[i] < 2)
                                #get row index of current time slot
                                currentIndex = finalDf.index[(finalDf['faculty']==fac2) & (finalDf['time']==olap[check]) & (finalDf['day']==column)][0]
                                #check 1/2 hour after 8 and 1/2 hour before 5:
                                checkBefore = (not ((finalDf.iloc[currentIndex]['applicant'] == '8:00-8:30') & \
                                    (finalDf.iloc[currentIndex+1]['applicant'] != 'open')))
                                checkAfter = (not ((finalDf.iloc[currentIndex]['applicant'] == '4:30-5:00') & \
                                    (finalDf.iloc[currentIndex-1]['applicant'] != 'open')))
                                checkInBetween = ((finalDf.iloc[currentIndex]['applicant'] != '8:00-8:30') & \
                                              (finalDf.iloc[currentIndex]['applicant'] != '4:30-5:00') & \
                                              (finalDf.iloc[currentIndex-1]['applicant'] == 'open') & \
                                              (finalDf.iloc[currentIndex+1]['applicant'] == 'open'))
                                
                                if((checkPresent) & (checkBefore) & (checkAfter) & (checkInBetween)):
                                    print('assigning')
                                    #exit()
                                    #print(olap[check])
                                    finalDf.loc[(finalDf['faculty']==fac2) &\
                                        (finalDf['time']==olap[check]) &\
                                        (finalDf['day']==column),
                                        ['applicant']] = i
                                    appsPoints[i]+=1
                                    facsAssignNums[fac2]+=1
                                    selectDf = finalDf.loc[(finalDf['faculty']==fac2) &\
                                        (finalDf['time']==olap[check]) &\
                                        (finalDf['day']==column) &\
                                        (finalDf['applicant']==i)]
                                    print(selectDf['applicant'].to_string(index=False) + ',\t' +\
                                        selectDf['faculty'].to_string(index=False) + ',\t' +\
                                        selectDf['day'].to_string(index=False) + ',\t' +\
                                        selectDf['time'].to_string(index=False))
                                    vals = selectDf.astype(str).values.flatten().tolist()
                                    stringOut = ';\t'.join(map(str,vals))
                                    facTimes2.append(stringOut)
                                    break
                        else:
                            continue
                        break

    #Output fac2 matches file:
        if os.path.exists("fac2.txt"):
            os.remove("fac2.txt")
    
    with open('fac2.txt', 'w') as f2:
        f2.write('\n'.join([str(x) for x in facTimes2]))
        f2.close()  
    
######### write out applicant points file and fac #s files ############
#######################################################################
#######################################################################
#######################################################################
#######################################################################

    dfp = pd.DataFrame(data=appsPoints, index=[0])
    #Transpose:
    dfp = (dfp.T)
    dfpIndex = dfp.index
    dfp.insert(0,"applicant",dfpIndex)
    dfp.columns.values[1] = 'points'
    dfp.to_excel('apps_points.xlsx',index=False)

    dfa = pd.DataFrame(data=facsAssignNums, index=[0])
    #Transpose:
    dfa = (dfa.T)
    dfaIndex = dfa.index
    dfa.insert(0,"faculty",dfaIndex)
    dfa.columns.values[1] = 'assigns'
    dfa.to_excel('fac_num_assigned.xlsx',index=False)    
    
    ################ Assigning remaining slots randomly ###################
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################

    #remember to prioritize faculty over alumni
    facSubs = finalDf[~finalDf['faculty'].isin(allAlum)]['faculty'].unique()
    alumSubs = finalDf[finalDf['faculty'].isin(allAlum)]['faculty'].unique()
    allSubs = facSubs.tolist()+alumSubs.tolist()
    allJobs = (np.repeat('fac',len(facSubs)).tolist()+np.repeat('alum',len(alumSubs)).tolist())

    alumFacCheck = pd.DataFrame()
    alumFacCheck['faculty']=allSubs
    alumFacCheck['job']=allJobs
    alumFacCheck['status']=np.repeat(0,alumFacCheck.shape[0])
                                 
    assignRandom = True
    if(assignRandom==True):
        #reindex row #s:
            finalDf.reset_index(inplace=True, drop=True)                            
            #Now loop through and fill in missing
            for i in appsPoints.keys():
                print("assigning random to " + i)
                #print(len(finalDf[finalDf['applicant']==i]))
                #if no 2 points, choose random faculty/alum for the candidate
                while(appsPoints[i]<2):
                    checkPresent = False
                    checkBefore = False
                    checkAfter = False
                    checkInBetween = False
                    #pic random row in assignment df:
                    randomRow = finalDf.sample()
                    #print(randomRow['faculty'])
                    #check if faculty:
                    if(((alumFacCheck.loc[alumFacCheck['faculty']==randomRow.faculty.values[0],'job'].values[0]=='fac') &\
                                (alumFacCheck.loc[alumFacCheck['faculty']==randomRow.faculty.values[0],'status'].values[0]==0)) |\
                               ((all(alumFacCheck.loc[alumFacCheck['job']=='fac'].status==1) & \
                                 (alumFacCheck.loc[alumFacCheck['faculty']==randomRow.faculty.values[0],'job'].values[0]=='alum')))):
                                
                        #check present time slot:
                        checkPresent = (randomRow['applicant'].to_string(index=False)=='open')
                                    
                        #get row index of current time slot
                        currentIndex = randomRow.index[0]
            
                        #check fac #s alreads assigned:
                        selFac = finalDf.iloc[currentIndex]['faculty']
                
                        #assign the faculty over alum:
                        alumFacCheck.loc[alumFacCheck['faculty']==selFac,'status'] = 1
                
                        if(facsAssignNums[selFac]>=5):
                            continue
            
                        #check if index is first or last
                        if(currentIndex==len(finalDf.index)-1):
                            checkBefore = (finalDf.iloc[currentIndex-1]['applicant'] != 'open')
                            checkAfter = True
                            checkInBetween = True
                        elif(currentIndex==0):
                            checkAfter = (finalDf.iloc[currentIndex+1]['applicant'] != 'open')
                            checkBefore = True
                            checkInBetween = True
                        else:
                            #check 1/2 hour after 8 and 1/2 hour before 5:
                            checkBefore = (not ((finalDf.iloc[currentIndex]['applicant'] == '8:00-8:30') & (finalDf.iloc[currentIndex+1]['applicant'] != 'open')))
                            checkAfter = (not ((finalDf.iloc[currentIndex]['applicant'] == '4:30-5:00') & (finalDf.iloc[currentIndex-1]['applicant'] != 'open')))
                            checkInBetween = ((finalDf.iloc[currentIndex]['applicant'] != '8:00-8:30') & (finalDf.iloc[currentIndex]['applicant'] != '4:30-5:00') & (finalDf.iloc[currentIndex-1]['applicant'] == 'open') & (finalDf.iloc[currentIndex+1]['applicant'] == 'open'))
                            #print(checkPresent + checkBefore + checkAfter + checkInBetween)
                        if((checkPresent) & (checkBefore) & (checkAfter) & (checkInBetween)):
                            #print('assigning random')
                            finalDf.iloc[currentIndex]["applicant"] = i 
                            appsPoints[i]+=1
                            facsAssignNums[selFac]+=1
                            alumFacCheck.loc[alumFacCheck['faculty']==selFac,'status'] = 1
                    
                            #Reset faculty over alum priority check:
                            alumFacCheck['faculty']=allSubs
                            alumFacCheck['job']=allJobs
                            alumFacCheck['status']=np.repeat(0,alumFacCheck.shape[0])
                    
                            #print(appsPoints[i])
                            #print(appsPoints)

    print(alumFacCheck)   
    
################### Final formatting and output #######################
#######################################################################
#######################################################################
#######################################################################
#######################################################################

    finalDups = finalDf.duplicated()

    finalDf = finalDf.drop_duplicates(finalDf.columns).reset_index(drop=True)
    
    finalDfM  = finalDf.loc[finalDf["day"]==allDays[0]]
    finalDfM = finalDfM.drop_duplicates(finalDfM.columns).reset_index(drop=True)

    finalDfT  = finalDf.loc[finalDf["day"]==allDays[1]] 
    finalDfT = finalDfT.drop_duplicates(finalDfT.columns).reset_index(drop=True)

    finalDfW  = finalDf.loc[finalDf["day"]==allDays[2]]
    finalDfW = finalDfW.drop_duplicates(finalDfW.columns).reset_index(drop=True)

    finalDfTh = finalDf.loc[finalDf["day"]==allDays[3]] 
    finalDfTh = finalDfTh.drop_duplicates(finalDfTh.columns).reset_index(drop=True)

    finalDfF  = finalDf.loc[finalDf["day"]==allDays[4]] 
    finalDfF = finalDfF.drop_duplicates(finalDfF.columns).reset_index(drop=True)

    #Need to remove blank time spot for a couple places:
    finalDfW.drop([4], axis=0, inplace=True)
    finalDfF.drop([6], axis=0, inplace=True)

    mTimes = finalDfM['time']
    finalDfMCast  = (finalDfM.pivot(index=['time'], 
                                         columns='faculty',
                                         values='applicant').reset_index(drop=True))
    finalDfMCast.insert(0,'time',mTimes.unique())
    tTimes = finalDfT['time']
    finalDfTCast  = (finalDfT.pivot(index=['time','day'], 
                                         columns='faculty',
                                         values='applicant').reset_index(drop=True))
    finalDfTCast.insert(0,'time',tTimes.unique())
    wTimes = finalDfW['time']
    finalDfWCast  = (finalDfW.pivot(index=['time','day'], 
                                         columns='faculty',
                                         values='applicant').reset_index(drop=True))
    finalDfWCast.insert(0,'time',wTimes.unique())
    thTimes = finalDfTh['time']
    finalDfThCast = (finalDfTh.pivot(index=['time','day'], 
                                         columns='faculty',
                                         values='applicant').reset_index(drop=True))
    finalDfThCast.insert(0,'time',thTimes.unique())
    fTimes = finalDfF['time']
    finalDfFCast  = (finalDfF.pivot(index=['time','day'], 
                                         columns='faculty',
                                         values='applicant').reset_index(drop=True))
    finalDfFCast.insert(0,'time',fTimes.unique())

    finalDfMCast.fillna("", inplace=True)
    finalDfTCast.fillna("", inplace=True)
    finalDfWCast.fillna("", inplace=True)
    finalDfThCast.fillna("", inplace=True)
    finalDfFCast.fillna("", inplace=True)

    finalDfMCast.replace('open', "", inplace=True)
    finalDfTCast.replace('open', "", inplace=True)
    finalDfWCast.replace('open', "", inplace=True)
    finalDfThCast.replace('open', "", inplace=True)
    finalDfFCast.replace('open', "", inplace=True)

    #unique(finalDfM["time"])
    #unique(finalDfT["time"])
    #unique(finalDfW["time"])
    #unique(finalDfTh["time"])
    #unique(finalDfF["time"])

    #finalDfMCast.insert(0,finalDfM inplace=TRUE

    #Order by time column:
    finalDfMCast['otime'] = pd.Categorical(finalDfMCast.time, 
                                       ordered=True, 
                                       categories=allTimes)
    finalDfMCast = finalDfMCast.sort_values('otime')
    finalDfMCast.drop('otime',axis=1,inplace=True)

    finalDfTCast['otime'] = pd.Categorical(finalDfTCast.time, 
                                       ordered=True, 
                                       categories=allTimes)
    finalDfTCast = finalDfTCast.sort_values('otime')
    finalDfTCast.drop('otime',axis=1,inplace=True)

    finalDfWCast['otime'] = pd.Categorical(finalDfWCast.time, 
                                       ordered=True, 
                                       categories=allTimes)
    finalDfWCast = finalDfWCast.sort_values('otime')
    finalDfWCast.drop('otime',axis=1,inplace=True)

    finalDfThCast['otime'] = pd.Categorical(finalDfThCast.time, 
                                       ordered=True, 
                                       categories=allTimes)
    finalDfThCast = finalDfThCast.sort_values('otime')
    finalDfThCast.drop('otime',axis=1,inplace=True)

    finalDfFCast['otime'] = pd.Categorical(finalDfFCast.time, 
                                       ordered=True, 
                                       categories=allTimes)
    finalDfFCast = finalDfFCast.sort_values('otime')
    finalDfFCast.drop('otime',axis=1,inplace=True)

    #Now row bind the casted table and output to file
    dfList=[finalDfMCast,
            finalDfTCast,
            finalDfWCast,
            finalDfThCast,
            finalDfFCast]

################# paste points to the applicant ##################
################# paste job and assign num to faculty/alum #######

    #Write to excel:
    writer = pd.ExcelWriter("final_match_output.xlsx",engine='xlsxwriter') 
    startRow = 2
    headerRow = 0
    workbook=writer.book
    count = 0
    for dataFrame in dfList:
        dataFrame.style.set_properties(**{'background-color': 'blue'}, subset=['A'])
        dataFrame.to_excel(writer, 
                           sheet_name='output', 
                           startrow=startRow, 
                           startcol=0,
                           index=False)
        bold = workbook.add_format({'bold': True})
        worksheet = writer.sheets['output']
        worksheet.write(headerRow, 0, allDays[count],bold)
        #worksheet.conditional_format('B2:B8', {'type': '3_color_scale'})
        startRow+=22
        headerRow+=22
        count+=1
    writer.close()   
    
######################### Server Action ##################################
##########################################################################
##########################################################################

    mod_counter = reactive.value(0)

    query_output_server("initial_query", con=con, remove_id="initial_query")

    @reactive.effect
    @reactive.event(input.add_query)
    def _():
        counter = mod_counter.get() + 1
        mod_counter.set(counter)
        id = "query_" + str(counter)
        ui.insert_ui(
            selector="#module_container",
            where="afterBegin",
            ui=query_output_ui(id, remove_id=id),
        )
        query_output_server(id, con=con, remove_id=id)

    @reactive.effect
    @reactive.event(input.show_meta)
    def _():
        counter = mod_counter.get() + 1
        mod_counter.set(counter)
        id = "query_" + str(counter)
        ui.insert_ui(
            selector="#module_container",
            where="afterBegin",
            ui=query_output_ui(
                id, qry="SELECT * from information_schema.columns", remove_id=id
            ),
        )
        query_output_server(id, con=con, remove_id=id)


app = App(app_ui, server)

######### For running the App in local browser ###########################
app.run()
##########################################################################
