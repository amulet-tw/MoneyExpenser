#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *


class QueryModel(QSqlQueryModel):
    def data(self, index, role):
        value = QSqlQueryModel.data(self, index, role)
        if value.isValid() and role == Qt.DisplayRole:
            if index.column() == 3:
                return QVariant(value.toString().prepend(self.tr("$")))
        
        if role == Qt.TextColorRole:
            if index.column() == 2:
                return QVariant(QColor(Qt.blue))
            elif index.column() == 3:
                return QVariant(QColor(Qt.red))
        
        if role == Qt.TextAlignmentRole:
            if index.column() != 5:
                return QVariant(Qt.AlignCenter)
        
        return value
        
    def getPrimeKey(self, index):
        primeKeyIndex = index.sibling(index.row(), 0)
        id = self.data(primeKeyIndex, Qt.EditRole).toString()
        return id

