from app import app

from flask import Flask, render_template, request, url_for, flash, redirect
import matplotlib.pyplot as plt 
import _thread as thread
from DaoGroups import DAOGroups
from twitter import *
from settings import connection
from utils import *
import datetime
import time
from externalComms import *


def restartMonitor():
     daoGroup = DAOGroups(connection())
     daoGroup.disableMonitor()

restartMonitor()


@app.route('/monitor/groups/')
def showallMonitorGroups():
    daoGroup = DAOGroups(connection())
    groups = daoGroup.getAllGroups()
    keepRunningMonitor = daoGroup.keepRunningMonitor()
    autorunToggle=""
    if bool(keepRunningMonitor[0][0]):
        autorunToggle = "checked"
    del daoGroup
    return render_template('monitor.html', groupList=groups, isAutorunEnabled=autorunToggle)


@app.route('/monitor/groups/auto', methods = ['POST'])
def handleAutorun():    
    daoGroup = DAOGroups(connection())
    keepRunningMonitor = daoGroup.keepRunningMonitor()

    if bool(keepRunningMonitor[0][0]):
        daoGroup.disableMonitor()
        return "Automonitor mode disabled"
    else:
        daoGroup.enableMonitor()
        thread.start_new_thread(initDaemon, ())
        return "Automonitor mode enabled"
        


@app.route('/monitor/groups/create', methods = ['POST'])
def createMonitorGroup():
    
    daoGroup = DAOGroups(connection())
    daoGroup.insertGroup(request.form.get('groupName'), request.form.get('groupDescription'), request.form.get('groupInterval') )
    del daoGroup
    return redirect('/monitor/groups/')


@app.route('/monitor/groups/<int:groupID>/auto', methods=['POST'])
def autorunMonitorForGroup(groupID):
    daoGroup = DAOGroups(connection())
    print()
    if daoGroup.isMonitorEnabledForGroup(groupID)[0][0] == 1: 
        daoGroup.disableMonitorForGroup(groupID)
        return "Autorun Disabled"
    else: 
        daoGroup.enableMonitorForGroup(groupID)
        return "Autorun Enabled"
    

@app.route('/monitor/groups/<int:groupID>/')
def showSpecificMonitorGroup(groupID):
    
    daoGroup = DAOGroups(connection())
    groupInfo = daoGroup.getGroupInfo(groupID)
    resultList = list(daoGroup.getGroupMonitorizeResults(groupID))
    for x in range(len(resultList)):
        resultList[x] =  list(resultList[x])
        rulesForResultList = daoGroup.getRulesForResult(resultList[x][4],groupID )
        resultList[x].insert(11,rulesForResultList)
        
    del daoGroup

    if groupInfo[0][7] == 1:
        autorunEnabled = "checked"
    else: 
        autorunEnabled = ""

    return render_template('group.html',  groupID=str(groupID),autorunEnabled = autorunEnabled, groupName=groupInfo[0][1],groupDescription=groupInfo[0][2], resultList=resultList, lastTimeScanned=timeElapsedString(groupInfo[0][6]))


@app.route('/monitor/groups/<int:groupID>/users/')
def showUsersFromMonitorGroup(groupID):

    daoGroup = DAOGroups(connection())
    userList = daoGroup.getGroupUsers(groupID)
    groupInfo = daoGroup.getGroupInfo(groupID)
    del daoGroup

    if groupInfo[0][7] == 1:
        autorunEnabled = "checked"
    else: 
        autorunEnabled = ""

    return render_template('usersGroup.html',autorunEnabled = autorunEnabled, userList=userList, groupName=groupInfo[0][1], groupDescription=groupInfo[0][2],  groupID=str(groupID) , lastTimeScanned=timeElapsedString(groupInfo[0][6]))


@app.route('/monitor/groups/<int:groupID>/users/add', methods = ['POST'])
def addUserToMonitorGroup(groupID):
    daoGroups = DAOGroups(connection())
    userID, photoURL = getTwitterInfoFromUser(request.form.get('username'))
    if userID != -1:
        daoGroups.insertUser(userID, groupID, request.form.get('username'), photoURL)
    del daoGroups
    return redirect('/monitor/groups/'+ str(groupID) + '/users/')


@app.route('/monitor/groups/<int:groupID>/rules/')
def showRulesFromMonitorGroup(groupID):
    ruleType = ['none', 'Search Text','Scan Images','Search Regex']
    daoGroups = DAOGroups(connection())
    rulesList = daoGroups.getGroupMonitorizeRules(groupID)
    groupInfo = daoGroups.getGroupInfo(groupID)

    if groupInfo[0][7] == 1:
        autorunEnabled = "checked"
    else: 
        autorunEnabled = ""


    del daoGroups
    return render_template('rulesGroup.html', autorunEnabled = autorunEnabled, rulesList=rulesList, groupName=groupInfo[0][1], groupDescription=groupInfo[0][2], groupID=str(groupID), ruleType=ruleType, lastTimeScanned=timeElapsedString(groupInfo[0][6])  )

    

@app.route('/monitor/groups/<int:groupID>/rules/add',  methods = ['POST'])
def addRuleToMonitorGroup(groupID):
    daoGroups = DAOGroups(connection())

    if request.form.get('ruleSelect') == 'text':
        ruleTypeID = 1
        searchText = request.form.get('searchString')
        daoGroups.insertRule(groupID,ruleTypeID, searchText, 1 )

    elif request.form.get('ruleSelect') == 'image':
        imageScanRulesList = {'Guns' : 'weapon_moderation', 'Porn' : 'porn_moderation', 'Drugs' : 'drug_moderation', 'Gore' : 'gore_moderation', 'Money' : 'money_moderation' , 'Nudity' : 'suggestive_nudity_moderation', 'Hate' : 'hate_sign_moderation' }
        ruleTypeID = 2
        imageScanRule = request.form.get('scanType')
        try:
            imageScanRule = imageScanRulesList[imageScanRule]
        except: 
            imageScanRule = 'NOTFOUND'

        if 'NOTFOUND' not in imageScanRule:
            daoGroups.insertRule(groupID,ruleTypeID, imageScanRule, 1 )
            
    elif request.form.get('ruleSelect') == 'regex':
        ruleTypeID = 3
        searchText = request.form.get('searchString')
        daoGroups.insertRule(groupID,ruleTypeID, searchText, 1 )
    return redirect('/monitor/groups/'+ str(groupID) + '/rules/')



@app.route('/monitor/groups/<int:groupID>/run',  methods = ['POST'])
def runMonitorGroup(groupID):
    if request.form.get('autorun') == "on":
        setNewExecutionTimeForGroup(groupID)
    else:
        #monitorizeUserFromGroup(groupID)
        thread.start_new_thread(monitorizeUserFromGroup,(groupID,))
    return redirect('/monitor/groups/'+ str(groupID) + '/')




@app.route('/monitor/groups/<int:groupID>/settings',  methods = ['POST'])
def addSettings(groupID):
    daoGroups = DAOGroups(connection())
    slackToken = request.form.get('slackToken')
    slackGroupId = request.form.get('slackGroupID')

    daoGroups.insertGroupSetting(groupID, slackToken, slackGroupId)
    post_message_to_slack("Test", slackGroupId, slackToken )
    
    return redirect('/monitor/groups/'+ str(groupID) + '/settings')


@app.route('/monitor/groups/<int:groupID>/settings',  methods = ['GET'])
def getSettings(groupID):
    daoGroups = DAOGroups(connection())
    groupInfo = daoGroups.getGroupInfo(groupID)
    del daoGroups

    if groupInfo[0][7] == 1:
        autorunEnabled = "checked"
    else: 
        autorunEnabled = ""

    return render_template('settingsGroup.html',autorunEnabled =autorunEnabled, groupName=groupInfo[0][1], groupDescription=groupInfo[0][2], groupID=str(groupID),  lastTimeScanned=timeElapsedString(groupInfo[0][6])  )

def monitorizeUserFromGroup(ids):
    daoGroups = DAOGroups(connection())
    usersFromGroup = daoGroups.getGroupUsers(ids)
    rulesFromGroup = daoGroups.getGroupMonitorizeRules(ids)
    groupSettings = daoGroups.getGroupSettings( ids)
    if len(groupSettings) >= 0:
        sendToSlack = True
        slackToken = groupSettings[0][1]
        slackID = groupSettings[0][2]
    else:
        sendToSlack = False
        slackToken = None
        slackID = None
    

    for user in usersFromGroup:
        try:
            userTweets = getLastTweetsFromUser(user[0],user[2])
        except Exception as ex: 
            print(ex)
            return None
        if len(userTweets) != 0:
            #print(userTweets)
            daoGroups.setTweetCursorFromUser(userTweets[0].id, user[0], ids)
           
            for tweet in userTweets:
                checkTweet( rulesFromGroup, tweet, daoGroups, user, sendToSlack, slackToken, slackID)
    daoGroups.setLastTimeScan(ids)



def setNewExecutionTimeForGroup(id, daoGroups):
    executionInterval = daoGroups.getGroupExecutionInterval(id)
    timeNow =  datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
    time_change = datetime.timedelta(minutes=executionInterval[0][0])
    time_change = time_change + timeNow
    time_change = datetime.datetime.strptime(str(time_change), '%Y-%m-%d %H:%M:%S.%f')
    print(time_change)
    daoGroups.setNextTimeScan( id, time_change)
    



def initDaemon():
    daoGroups = DAOGroups(connection())
    keepRunning = daoGroups.keepRunningMonitor()

    while keepRunning[0][0] == 1:
        allGroups = daoGroups.getGroupstoRun()
        for group in allGroups:
            monitorizeUserFromGroup(group[0])
            setNewExecutionTimeForGroup(group[0], daoGroups)
        time.sleep(20)
        keepRunning = daoGroups.keepRunningMonitor()
    del daoGroups

