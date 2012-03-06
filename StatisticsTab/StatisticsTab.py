#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ConditionTab import *
from TableView import *


class StatisticsTab(QWidget):
    def __init__(self, parent=None):
        super(StatisticsTab, self).__init__(parent)
        self.parent = parent
        
        self.createLayout()
        
    def updateTable(self):
        date1 = self.fromDateEdit.date()
        date2 = self.toDateEdit.date()
        if date1 > date2:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Invalid date range."))
            return
        
        title = self.titleTab.retrieveCondition()
        tags = self.tagTab.retrieveCondition()
        
        count, sum = self.tableView.updateContent(2, date1, date2, title, tags)
        countString = QString().setNum(count)
        self.cntLabel.setText(countString + self.tr(" item(s)"))
        self.sumLabel.setText(self.tr("$") + QString().setNum(sum))
        self.parent.setStatusBarMessage(self.tr("Query done. " + countString + " item(s) matched."))
        
    def changeDateRangeMonth(self):
        today = QDate.currentDate()
        self.fromDateEdit.setDate(QDate(today.year(), today.month(), 1))
        self.toDateEdit.setDate(today)
        
    def createLayout(self):
        dateGroup = QGroupBox(self.tr("Date range"))
        
        self.thisMonthButton = QRadioButton(self.tr("This &month"), dateGroup)
        self.customButton = QRadioButton(self.tr("&Custom"), dateGroup)
        
        self.fromDateEdit = QDateEdit()
        self.fromDateEdit.setDisplayFormat("MMM dd, yyyy")
        self.fromDateEdit.setCalendarPopup(True)
        self.toDateEdit = QDateEdit()
        self.toDateEdit.setDisplayFormat("MMM dd, yyyy")
        self.toDateEdit.setCalendarPopup(True)
        dateEditLayout = QFormLayout()
        dateEditLayout.addRow(self.tr("F&rom"), self.fromDateEdit)
        dateEditLayout.addRow(self.tr("T&o"), self.toDateEdit)
        
        dateLayout = QVBoxLayout()
        dateLayout.addWidget(self.thisMonthButton)
        dateLayout.addWidget(self.customButton)
        dateLayout.addLayout(dateEditLayout)
        dateGroup.setLayout(dateLayout)
        
        self.thisMonthButton.setChecked(True)
        self.changeDateRangeMonth()
        self.thisMonthButton.toggled.connect(self.changeDateRangeMonth)
        self.thisMonthButton.toggled.connect(self.thisMonthButton.setChecked)
        self.fromDateEdit.dateChanged.connect(self.customButton.click)
        self.toDateEdit.dateChanged.connect(self.customButton.click)
        
        titleGroup = QGroupBox(self.tr("T&itle"))
        self.titleTab = ConditionTab(QString("Title"))
        titleLayout = QVBoxLayout()
        titleLayout.addWidget(self.titleTab)
        titleGroup.setLayout(titleLayout)
        
        tagGroup = QGroupBox(self.tr("&Tag"))
        self.tagTab = ConditionTab(QString("Tags"))
        tagLayout = QVBoxLayout()
        tagLayout.addWidget(self.tagTab)
        tagGroup.setLayout(tagLayout)
        
        self.calcButton = QPushButton(self.tr("&GO!"))
        self.calcButton.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.calcButton.clicked.connect(self.updateTable)
        
        resultGroup = QGroupBox(self.tr("Result"))
        cntLabel = QLabel(self.tr("Count:"))
        sumLabel = QLabel(self.tr("  Sum:"))
        self.cntLabel = QLabel()
        self.sumLabel = QLabel()
        self.cntLabel.setAlignment(Qt.AlignLeft)
        self.sumLabel.setAlignment(Qt.AlignLeft)
        
        resultLayout = QGridLayout()
        resultLayout.addWidget(cntLabel, 0, 0)
        resultLayout.addWidget(sumLabel, 1, 0)
        resultLayout.addWidget(self.cntLabel, 0, 1)
        resultLayout.addWidget(self.sumLabel, 1, 1)
        resultGroup.setLayout(resultLayout)
        
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(dateGroup)
        leftLayout.addWidget(titleGroup)
        leftLayout.addWidget(tagGroup)
        leftLayout.addWidget(self.calcButton)
        leftLayout.addStretch()
        leftLayout.addWidget(resultGroup)
        
        self.tableView = TableView()
        
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addWidget(self.tableView, 1)
        self.setLayout(mainLayout)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = StatisticsTab()
    widget.show()
    app.exec_()

