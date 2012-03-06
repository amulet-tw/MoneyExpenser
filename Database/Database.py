#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtSql import *
from QueryModel import *


def parseConditions(string, category):
    condition = QString()
    if string == None:
        return condition
    
    list = string.split(", ", QString.SkipEmptyParts, Qt.CaseInsensitive)
    if not list.isEmpty():
        condition += " AND ( " + category + " LIKE '%" + list[0].trimmed() + "%'"
        for item in list[1:]:
            condition += " OR " + category + " LIKE '%" + item.trimmed() + "%'"
        condition += " )"
    
    return condition


class Database():
    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.connected = False
        self.profilePath = QString()
        
    def connectTo(self, profilePath):
        if profilePath.isEmpty():
            return False
        self.db.setDatabaseName(profilePath)
        
        if not self.db.open():
            self.connected = False
            self.profilePath.clear()
            return self.connected
        
        self.connected = True
        self.profilePath = profilePath
        
        query = QSqlQuery(self.db)
        # Initial the database. Won't overwrite the existing one.
        query.exec_("CREATE DATABASE MoneyExpenser")
        query.exec_("CREATE TABLE Log (ID INTEGER PRIMARY KEY, " # 'AUTO_INCREMENT'ed in sqlite
                                       "Date DATE, "
                                       "Title TEXT, "
                                       "Cost INTEGER, "
                                       "Tags TEXT, "
                                       "Comment TEXT)")
        
        return self.connected
        
    def convertToUTF8(self, query):
        return QTextCodec.codecForName("UTF-8").toUnicode(query.toUtf8())
        
    def addRecord(self, date, title, cost, tags, comment):
        query = QSqlQuery(self.db)
        return query.exec_(self.convertToUTF8("INSERT INTO Log VALUES(null, '" + date + "', '" + title + "', " + cost + ", '" + tags + "', '" + comment + "')"))
        
    def removeRecord(self, primeKey):
        query = QSqlQuery(self.db)
        return query.exec_("DELETE FROM Log WHERE ID = " + primeKey)
        
    def getFrequency(self, category):
        query = QSqlQuery(self.db)
        query.exec_("SELECT DISTINCT " + category + " FROM Log")
        
        items = []
        while query.next():
            item = QTextCodec.codecForName("UTF-8").toUnicode(query.value(0).toString().toUtf8())
            if not item.isEmpty() and not item.contains(", "):
                items.append(item)
        
        dic = {}
        freq = []
        for item in items:
            query.exec_("SELECT COUNT(*) FROM Log WHERE " + category + " LIKE '%" + item + "%'")
            while query.next():
                f = query.value(0).toInt()[0]
                freq.append(f)
                dic[item] = f
        
        freq.sort()
        freq.reverse()
        
        freqDict = {}
        for f in freq[:15]:
            for key in dic:
                if dic[key] == f and key not in freqDict:
                    freqDict[key] = f
                    break
        
        return freqDict
        
    def getModelAndStatistics(self, parent, dateCount, date1, date2, title, tags):
        '''query (int, QDate, QDate, QString, QString), return (model, count, sum)'''
        
        filter = QString()
        if dateCount == 1:
            filter += "Date = " + date1.toString('"yyyy-MM-dd"')
        elif dateCount == 2:
            filter += "( Date BETWEEN " + date1.toString('"yyyy-MM-dd"') + " AND " + date2.toString('"yyyy-MM-dd"') + " )"
        
        filter += parseConditions(title, "Title")
        filter += parseConditions(tags, "Tags")
        
        model = QueryModel()
        model.setQuery("SELECT * FROM Log WHERE ( " + filter + " ) ORDER BY Date", self.db)
        
        query = QSqlQuery(self.db)
        query.exec_("SELECT COUNT(*), SUM(Cost) FROM Log WHERE ( " + filter + " )")
        query.next()
        count, status = query.value(0).toInt()
        sum, status = query.value(1).toInt()
        
        return model, count, sum
        

db = Database()

