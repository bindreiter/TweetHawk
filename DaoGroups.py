import MySQLdb
class DAOGroups:
    def __init__(self, connectionPool):
        self.connectionPool = connectionPool
        self.cursor = connectionPool.cursor()

    
    def getGroupUsers(self, groupID):
        
        try:
            self.cursor.execute("SELECT userID, username, lastTweetCursor, profilePicURL FROM monitorizeUsers WHERE groupID = %s", (str(groupID),))
        except Exception as ex:
            print(ex)
        return  self.cursor.fetchall()
    
    def getAllGroups(self):
        try:
            self.cursor.execute("SELECT id, name, description, nUsers, nRules, nResults  FROM monitorizeGroups")
        except Exception as ex:
            print(ex)
        return  self.cursor.fetchall()
    
    def getGroupstoRun(self):
        try:
            self.cursor.execute("SELECT id , nextTimeScan FROM monitorizegroups WHERE nextTimeScan <= CURRENT_TIMESTAMP AND autorun = 1")
        except Exception as ex:
            print(ex)
        return  self.cursor.fetchall()

    def keepRunningMonitor(self):
        try:
            self.cursor.execute("SELECT autorunMonitor FROM settings")
        except Exception as ex:
            print(ex)
        return  self.cursor.fetchall()

    def getGroupExecutionInterval(self, groupID):
        try:
            self.cursor.execute("SELECT looptime FROM monitorizeGroups WHERE monitorizeGroups.ID = %s", (str(groupID),))
        except Exception as ex:
            print(ex)
        return  self.cursor.fetchall()

    
    def getGroupInfo(self, groupID):
        try:
            self.cursor.execute("SELECT id, name, description, nUsers, nRules, nResults, lastTimeScanned, autorun  FROM monitorizeGroups WHERE  ID = %s", (groupID,))
        except Exception as ex:
            print(ex)
        return  self.cursor.fetchall()

    
    def groupExists(self, groupID):
        try:
            self.cursor.execute("SELECT id  FROM monitorizeGroups WHERE ID = %s", (str(groupID),))
        except Exception as ex:
            print(ex)
        return  self.cursor.fetchall()


    def getGroupMonitorizeRules(self, groupID):
        
        try:
            self.cursor.execute("SELECT type, rule, ID, groupID FROM  monitorizeRules WHERE groupID = %s", (str(groupID), ))

        except Exception as ex:
            print(ex)
        return  self.cursor.fetchall()
    

    def getGroupMonitorizeResults(self, groupID):
        try:
            self.cursor.execute("SELECT * FROM monitorizeResults INNER JOIN monitorizeUsers ON monitorizeUsers.userID=monitorizeResults.userID WHERE monitorizeResults.groupID = %s AND monitorizeUsers.groupID = %s group by monitorizeResults.tweetID order by monitorizeResults.tweetID DESC", (str(groupID),str(groupID)))
        except Exception as ex:
            print(ex)
        return  self.cursor.fetchall()
    
    
    def setTweetCursorFromUser(self,lastTweetCursor, userID,  groupID):
        try:
            self.cursor.execute("UPDATE monitorizeUsers SET lastTweetCursor = %s  WHERE userID = %s AND groupID = %s", ( str(lastTweetCursor), userID , groupID ))
            self.connectionPool.commit()
        except Exception as ex:
            print(ex)



    def insertRule(self, groupID, typeR, rule, priority):
        try:
            self.cursor.execute("INSERT INTO  monitorizeRules (groupID, type, rule, priority ) VALUES (%s, %s, %s, %s)", ( groupID, typeR, str(rule), priority ))
            self.connectionPool.commit()
        except Exception as ex:
            print(ex)

    
    def setLastTimeScan(self, id):
        try:
            self.cursor.execute("UPDATE monitorizeGroups SET lastTimeScanned = CURRENT_TIMESTAMP()  WHERE ID = %s", ( str(id),))
            self.connectionPool.commit()
        except Exception as ex:
            print(ex)

    def setNextTimeScan(self, id, date):
        try:
            self.cursor.execute("UPDATE monitorizeGroups SET nextTimeScan = %s  WHERE ID = %s", (date , str(id)))
            self.connectionPool.commit()
        except Exception as ex:
            print(ex)

    def insertResult(self, userID, groupID, ruleID, tweetID, tweet):

        try:
            self.cursor.execute("INSERT INTO  monitorizeResults ( userID, groupID, ruleID, tweetID, tweet, new ) VALUES (%s, %s, %s, %s, %s, 1)", (  userID, groupID, ruleID, str(tweetID), str(tweet) ))
            self.connectionPool.commit()
        except Exception as ex:
            print(ex)
    
    def insertUser(self, userID, groupID, username, photoURL):
        try:
            self.cursor.execute("INSERT INTO  monitorizeUsers ( userID, groupID, username, lasttweetcursor, profilePicURL) VALUES (%s, %s, %s, 404, %s)", (  userID, groupID, str(username), photoURL))
            self.connectionPool.commit()
        except Exception as ex:
            print(ex)

    def insertGroup(self,name, description, loop):
        
        try:
            self.cursor.execute("INSERT INTO  monitorizeGroups ( name, description, looptime ) VALUES ( %s, %s, %s )", (str(name), str(description), loop))
            self.connectionPool.commit()
        except Exception as ex:
            print(ex)


    def getGroupSettings(self, groupID):
        try:
            self.cursor.execute("SELECT `groupID`, `slackToken`, `slackgroupID` FROM `monitorizegroupsettings` WHERE groupId = %s", (str(groupID),))
        except Exception as ex:
            print(ex)
        return  self.cursor.fetchall()

    def insertGroupSetting(self,groupID, slackToken, slackGroupId):
        
        try:
            self.cursor.execute("DELETE FROM `monitorizegroupsettings` where groupID=%s", (str(groupID),))
            self.cursor.execute("INSERT INTO `monitorizegroupsettings`(`groupID`, `slackToken`, `slackgroupID`) VALUES (%s,%s,%s)", (str(groupID), str(slackToken), str(slackGroupId)))
            self.connectionPool.commit()
        except Exception as ex:
            print(ex)

    def updateGroupSetting(self,groupID, slackToken, slackGroupId):
        
        try:
            self.cursor.execute("UPDATE `monitorizegroupsettings` SET `slackToken`=%s,`slackgroupID`=%s WHERE groupId = %s", (str(slackToken), str(slackGroupId), str(groupID), ))
            self.connectionPool.commit()
        except Exception as ex:
            print(ex)
    

    def enableMonitor(self):
        try:
            self.cursor.execute("UPDATE settings SET autorunMonitor = 1")
            self.connectionPool.commit()
        except Exception as ex:
            print(ex)
    
    def disableMonitor(self):
        try:
            self.cursor.execute("UPDATE settings SET autorunMonitor = 0 where 1")
            self.connectionPool.commit()
        except Exception as ex:
            print(ex)

    
    def enableMonitorForGroup(self, groupID):
        try:
            self.cursor.execute("UPDATE monitorizegroups SET autorun = 1 where ID = %s", (groupID,))
            self.connectionPool.commit()
        except Exception as ex:
            print(ex)
    
    def disableMonitorForGroup(self, groupID):
        try:
            self.cursor.execute("UPDATE monitorizegroups SET autorun = 0 where ID = %s", (groupID,))
            self.connectionPool.commit()
        except Exception as ex:
            print(ex)

    def isMonitorEnabledForGroup(self,groupID):
        try:
            self.cursor.execute("SELECT autorun FROM monitorizegroups where ID = %s", (groupID,))
            
        except Exception as ex:
            print(ex)
        return self.cursor.fetchall()

    def getRulesForResult(self, tweetID, groupID):
        try:
            self.cursor.execute("SELECT monitorizerules.rule FROM monitorizeresults JOIN monitorizerules on monitorizerules.ID = monitorizeresults.ruleID WHERE monitorizeresults.tweetID = %s AND monitorizeresults.groupID = %s", (str(tweetID),str(groupID)))
        except Exception as ex:
            print(ex)
        return  self.cursor.fetchall()


