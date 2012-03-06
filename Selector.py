#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Database import *


class SortableTableWidgetItem(QTableWidgetItem):
    def __lt__(self, obj):
        return self.data(Qt.DisplayRole).toInt() < obj.data(Qt.DisplayRole).toInt()
    

class Selector(QDialog):
    def __init__(self, category, parent=None):
        super(Selector, self).__init__(parent)
        
        self.tableWidget = self.createTable(category)
        
        okButton = QPushButton("&OK")
        cancelButton = QPushButton("&Cancel")
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(okButton, QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(cancelButton, QDialogButtonBox.RejectRole)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        
        self.resize(self.tableWidget.sizeHint().width(), self.sizeHint().height())
        self.setWindowTitle(self.tr("Specify the ") + category)
        
    def retrieveData(self):
        conditions = QString("")
        for row in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(row, 0).checkState() == Qt.Checked:
                conditions += self.tableWidget.item(row, 1).text() + ", "
        
        return conditions
        
    def createTable(self, category):
        tableWidget = QTableWidget()
        tableWidget.setSortingEnabled(False)
        
        freqDict = db.getFrequency(category)
        tableWidget.setRowCount(len(freqDict))
        tableWidget.setColumnCount(3)
        row = 0
        for key in freqDict:
            cell0 = QTableWidgetItem()
            cell0.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            cell0.setCheckState(Qt.Unchecked)
            
            cell1 = QTableWidgetItem(key)
            cell1.setFlags(Qt.ItemIsEnabled)
            cell1.setTextAlignment(Qt.AlignCenter)
            
            cell2 = SortableTableWidgetItem(QString().setNum(freqDict[key]))
            cell2.setFlags(Qt.ItemIsEnabled)
            cell2.setTextAlignment(Qt.AlignCenter)
            
            tableWidget.setItem(row, 0, cell0)
            tableWidget.setItem(row, 1, cell1)
            tableWidget.setItem(row, 2, cell2)
            
            row += 1
        
        tableWidget.sortByColumn(2, Qt.DescendingOrder)
        
        labels = QStringList()
        labels << "" << category << self.tr("Frequency")
        tableWidget.setHorizontalHeaderLabels(labels)
        tableWidget.horizontalHeader().resizeSection(0, 32)
        tableWidget.horizontalHeader().resizeSection(2, 80)
        tableWidget.verticalHeader().hide()
        
        return tableWidget
        

class SingleSelector(Selector):
    def retrieveData(self):
        checkedCount = 0
        conditions = QString()
        for row in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(row, 0).checkState() == Qt.Checked:
                checkedCount += 1
                conditions += self.tableWidget.item(row, 1).text() + ", "

        if checkedCount != 1:
            QMessageBox.warning(self, self.tr("Invalid item count"), self.tr("Please specify exactly 1 item."))
            return
        else:
            if conditions.endsWith(", "):
                conditions.chop(2)
            return conditions

