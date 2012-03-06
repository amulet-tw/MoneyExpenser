#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from AddRecordDialog import *
from TableView import *

class GeneralTab(QWidget):
    def __init__(self, parent=None):
        super(GeneralTab, self).__init__(parent)
        self.parent = parent
        
        self.createLayout()
        self.addButton.clicked.connect(self.addRecord)
        self.removeButton.clicked.connect(self.removeRecord)
        QTimer.singleShot(0, self.updateTable)
        
    def updateTable(self):
        date = self.calendar.selectedDate()
        count, sum = self.tableView.updateContent(1, date, None, None, None)
        msg = date.toString("MMM dd, yyyy") + ":   " + QString().setNum(count) + self.tr(" item(s). Total $") + QString().setNum(sum)
        self.parent.setStatusBarMessage(msg)
        
    def addRecord(self):
        dialog = AddRecordDialog(self.calendar.selectedDate(), self)
        if dialog.exec_() == QDialog.Accepted:
            date, title, cost, tags, comment = dialog.retrieveData()
            db.addRecord(date, title, cost, tags, comment)
            self.updateTable()
        
    def removeRecord(self):
        if len(self.tableView.selectedIndexes()) == 0:
            QMessageBox.warning(self, self.tr("No item selected"), self.tr("Please select an item first."))
            return
        
        reply = QMessageBox.warning(self, self.tr("Removing record"), self.tr("Are you sure?"), QMessageBox.Ok | QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            if self.tableView.removeRecord():
                self.parent.setStatusBarMessage(self.tr("Record removed."))
            else:
                self.parent.setStatusBarMessage(self.tr("Error occured."))
        else:
            self.parent.setStatusBarMessage(self.tr("Canceled."))
        
    def createLayout(self):
        self.profileGroupBox = QGroupBox(self.tr("Profile:"))
        self.calendar = QCalendarWidget()
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.calendar)
        leftLayout.addStretch()
        self.profileGroupBox.setLayout(leftLayout)
        
        self.tableView = TableView()
        self.addButton = QPushButton(self.tr("&Add"))
        self.removeButton = QPushButton(self.tr("&Remove Row"))
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.removeButton)
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.tableView)
        rightLayout.addLayout(buttonLayout)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.profileGroupBox)
        mainLayout.addLayout(rightLayout, 1)
        
        self.setLayout(mainLayout)
        
        self.calendar.selectionChanged.connect(self.updateTable)
        
    def setTitle(self, profileName):
        if profileName.isEmpty():
            profileName = "(empty)"
        self.profileGroupBox.setTitle(self.tr("Profile: %s" % profileName))
        
    # patch for statusbar msg disappearing
    def enterEvent(self, event):
        if event.type() == QEvent.Enter:
            if self.parent.statusBar().currentMessage().isEmpty():
                self.updateTable()
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = GeneralTab()
    widget.show()
    app.exec_()
