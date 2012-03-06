#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Database import *


class TableView(QTableView):
    def __init__(self, parent=None):
        super(TableView, self).__init__(parent)
        
        self.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.dateCount = 1
        self.date1 = QDate()
        self.date2 = QDate()
        self.title = QString()
        self.tags = QString()
        
    def updateContent(self, dateCount, date1, date2, title, tags):
        self.model, count, sum = db.getModelAndStatistics(self, dateCount, date1, date2, title, tags)
        
        labels = QStringList()
        labels << self.tr("ID") << self.tr("Date") << self.tr("Title") << self.tr("Cost") << self.tr("Tags") << self.tr("Comment")
        for order in range(6):
            self.model.setHeaderData(order, Qt.Horizontal, QVariant(QObject.tr(self.model, labels[order])))
        
        self.setModel(self.model)
        self.hideColumn(0)
        
        self.dateCount = dateCount
        self.date1 = date1
        self.date2 = date2
        self.title = title
        self.tags = tags
        return count, sum
        
    def removeRecord(self):
        status = True
        indices = self.selectedIndexes()
        for index in indices:
            status &= db.removeRecord(self.model.getPrimeKey(index))
        
        if status:
            self.updateContent(self.dateCount, self.date1, self.date2, self.title, self.tags)
        
        return status
