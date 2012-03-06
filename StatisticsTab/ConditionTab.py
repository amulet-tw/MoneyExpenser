#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Selector import *


class ConditionTab(QWidget):
    def __init__(self, category, parent=None):
        super(ConditionTab, self).__init__(parent)
        
        self.category = category
        allButton = QRadioButton(self.tr("&All"))
        allButton.setChecked(True)
        self.customButton = QRadioButton(self.tr("C&ustom"))
        self.lineEdit = QLineEdit()
        self.lineEdit.setEnabled(False)
        self.editButton = QPushButton(self.tr("&Edit"))
        self.editButton.setEnabled(False)
        self.editButton.clicked.connect(self.listConditions)
        editLayout = QHBoxLayout()
        editLayout.addWidget(self.lineEdit)
        editLayout.addWidget(self.editButton)
        layout = QVBoxLayout()
        layout.addWidget(allButton)
        layout.addWidget(self.customButton)
        layout.addLayout(editLayout)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        
        self.customButton.toggled.connect(self.toggleEditable)
        
    def listConditions(self):
        dialog = Selector(self.category)
        if dialog.exec_() == QDialog.Accepted:
            self.lineEdit.setText(dialog.retrieveData())
        
    def retrieveCondition(self):
        if self.customButton.isChecked():
            condition = self.lineEdit.text()
            if condition.endsWith(","):
                condition += " "
            return condition
        else:
            return QString()
        
    def toggleEditable(self, toggled):
        self.lineEdit.setEnabled(toggled)
        self.editButton.setEnabled(toggled)
        
