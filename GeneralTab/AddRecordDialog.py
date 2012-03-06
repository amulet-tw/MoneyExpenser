#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Selector import *


class AddRecordDialog(QDialog):
    def __init__(self, initialDate, parent=None):
        super(AddRecordDialog, self).__init__(parent)
        
        self.setWindowTitle(self.tr('Add a new record'))
        
        dateLabel = QLabel('&Date:')
        self.dateEdit = QDateEdit()
        dateLabel.setBuddy(self.dateEdit)
        self.dateEdit.setDisplayFormat('MMM dd, yyyy')
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(initialDate)
        
        titleLabel = QLabel('&Title:')
        self.titleEdit = QLineEdit()
        titleLabel.setBuddy(self.titleEdit)
        self.titleEditButton = QPushButton(self.tr('&Edit'))
        self.titleEditButton.setFocusPolicy(Qt.NoFocus)
        self.titleEditButton.clicked.connect(self.listTitle)
        hLayout1 = QHBoxLayout()
        hLayout1.addWidget(self.titleEdit)
        hLayout1.addWidget(self.titleEditButton)
        
        costLabel = QLabel('Co&st:')
        self.costSpin = QSpinBox()
        costLabel.setBuddy(self.costSpin)
        self.costSpin.setSingleStep(10)
        self.costSpin.setRange(0, 100000)
        
        tagLabel = QLabel('Ta&gs:')
        self.tagEdit = QLineEdit()
        tagLabel.setBuddy(self.tagEdit)
        self.tagEditButton = QPushButton(self.tr('E&dit'))
        self.tagEditButton.setFocusPolicy(Qt.NoFocus)
        self.tagEditButton.clicked.connect(self.listTags)
        hLayout2 = QHBoxLayout()
        hLayout2.addWidget(self.tagEdit)
        hLayout2.addWidget(self.tagEditButton)
        
        commentLabel = QLabel('Co&mment:')
        self.commentEdit = QLineEdit()
        commentLabel.setBuddy(self.commentEdit)
        
        okButton = QPushButton('&OK')
        cancelButton = QPushButton('&Cancel')
        okButton.setFocusPolicy(Qt.NoFocus)
        cancelButton.setFocusPolicy(Qt.NoFocus)
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(okButton, QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(cancelButton, QDialogButtonBox.RejectRole)
        
        # QFormLayout should be a more elegant choice
        # but shortcut key will get fucked
        layout = QGridLayout()
        layout.addWidget(dateLabel, 0, 0, Qt.AlignRight)
        layout.addWidget(self.dateEdit, 0, 1)
        layout.addWidget(titleLabel, 1, 0, Qt.AlignRight)
        layout.addLayout(hLayout1, 1, 1)
        layout.addWidget(costLabel, 2, 0, Qt.AlignRight)
        layout.addWidget(self.costSpin, 2, 1)
        layout.addWidget(tagLabel, 3, 0, Qt.AlignRight)
        layout.addLayout(hLayout2, 3, 1)
        layout.addWidget(commentLabel, 4, 0, Qt.AlignRight)
        layout.addWidget(self.commentEdit, 4, 1)
        layout.addWidget(self.buttonBox, 5, 1)
        
        self.setLayout(layout)
        self.titleEdit.setFocus()
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
    def listTitle(self):
        self.listConditions('Title')
        
    def listTags(self):
        self.listConditions('Tags')
        
    def listConditions(self, category):
        dialog = Selector(category) if category == 'Tags' else SingleSelector(category)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.retrieveData()
            
            if category == 'Title':
                self.titleEdit.setText(data)
            elif category == 'Tags':
                self.tagEdit.setText(data)
        
    def retrieveData(self):
        ''' return date, title, cost, tags, comment '''
        tags = self.tagEdit.text()
        tagList = tags.split(',')
        for tag in tagList:
            tag = tag.trimmed()
        
        tags = tagList.join(', ')
        while tags.endsWith(',') or tags.endsWith(' '):
            tags.chop(1)
        
        return (self.dateEdit.date().toString('yyyy-MM-dd'), 
                self.titleEdit.text(), 
                QString.number(self.costSpin.value()), 
                tags, 
                self.commentEdit.text())
