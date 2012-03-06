#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Database import *
from GeneralTab import *
from StatisticsTab import *


__version__ = "2.5"


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.profilePath = QString()
        self.createLayout()
        self.readSettings()
        
        if self.profilePath.isEmpty() or not QFile.exists(self.profilePath):
            self.promptNewProfilePath(callByAction=False)
        else:
            self.establishConnection()
        
        self.tabChanged(self.tabWidget.indexOf(self.generalTab))
        
    def retrieveProfileName(self):
        index = self.profilePath.lastIndexOf("/")
        if index == -1 or self.profilePath.isEmpty():
            return QString()
        
        profileName = self.profilePath.right(self.profilePath.length() - index - 1)
        profileName.chop(3)  # chop file extension name
        return profileName
        
    def createLayout(self):
        self.generalTab = GeneralTab(self)
        self.statisticsTab = StatisticsTab(self)
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.generalTab, self.tr("Ge&neral"))
        self.tabWidget.addTab(self.statisticsTab, self.tr("&Statistics"))
        
        self.createMenu()
        self.setCentralWidget(self.tabWidget)
        self.statusBar()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle(self.tr("Money Expenser"))
        
        self.tabWidget.currentChanged.connect(self.tabChanged)
        
    def toggleButton(self, status):
        self.generalTab.addButton.setEnabled(status)
        self.generalTab.removeButton.setEnabled(status)
        self.statisticsTab.setEnabled(status)
        
    def promptNewProfilePath(self, callByAction=True):
        result = QMessageBox.Ok
        if not callByAction:
            result = QMessageBox.question(self, self.tr("Profile not found"), 
                                        self.tr("Create a new profile?"), 
                                        QMessageBox.Ok | QMessageBox.Cancel)
        if result == QMessageBox.Ok:
            profilePath = QFileDialog.getSaveFileName(self, 
                            self.tr("Create new profile"), 
                            QDir.homePath() + QDir.separator() + QDir.home().dirName() + ".me", 
                            self.tr("Money Expenser database (*.me)"))
            if not profilePath.isEmpty():
                self.profilePath = profilePath
        else:
            self.profilePath = QString()
        
        self.establishConnection(showWarning=False)
        
    def loadAction(self):
        profilePath = QFileDialog.getOpenFileName(self, 
                            self.tr("Load profile"), 
                            QDir.homePath(), 
                            self.tr("Money Expenser database (*.me)"))
        if not profilePath.isEmpty():
            if QFile.exists(profilePath):
                self.profilePath = profilePath
                self.establishConnection()
                self.generalTab.updateTable()
            else:
                QMessageBox.critical(self, self.tr("Error"), self.tr("File not found."))
        
    def establishConnection(self, showWarning=True):
        status = db.connectTo(self.profilePath)
        self.generalTab.setTitle(self.retrieveProfileName())
        self.toggleButton(status)
        if not status and showWarning:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Cannot open database."), QMessageBox.Ok)
        
    def tabChanged(self, index):
        if index == self.tabWidget.indexOf(self.generalTab):
            QTimer.singleShot(0, self.generalTab.updateTable)
        elif index == self.tabWidget.indexOf(self.statisticsTab):
            QTimer.singleShot(0, self.statisticsTab.updateTable)
            self.setStatusBarMessage(self.tr("Please specify the condition then press \"GO!\""))
        
    def setStatusBarMessage(self, msg):
        self.statusBar().showMessage(msg)
        
    def writeSettings(self):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "OGC", "MoneyExpenser")
        
        settings.setValue("lastProfilePath", QVariant(self.profilePath))
        
        settings.beginGroup("Layout")
        settings.setValue("size", QVariant(self.size()))
        settings.setValue("pos", QVariant(self.pos()))
        settings.endGroup()
        
    def readSettings(self):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "OGC", "MoneyExpenser")
        
        self.profilePath = settings.value("lastProfilePath", QVariant("")).toString()
        
        settings.beginGroup("Layout")
        self.resize(settings.value("size", QVariant(QSize(842, 525))).toSize())
        self.move(settings.value("pos", QVariant(QApplication.desktop().availableGeometry().center() / 2)).toPoint())
        settings.endGroup()
        
    def closeEvent(self, event):
        self.writeSettings()
        
    def createMenu(self):
        createProfileAct = QAction(self.tr("Cr&eate new profile"), self)
        loadProfileAct = QAction(self.tr("&Load profile"), self)
        exitAct = QAction(self.tr("E&xit"), self)
        aboutAct = QAction(self.tr("About"), self)
        aboutQtAct = QAction(self.tr("About Qt"), self)
        
        createProfileAct.setShortcut("Ctrl+E")
        loadProfileAct.setShortcut("Ctrl+L")
        exitAct.setShortcut("Ctrl+Q")
        
        createProfileAct.triggered.connect(self.promptNewProfilePath)
        loadProfileAct.triggered.connect(self.loadAction)
        exitAct.triggered.connect(self.close)
        aboutAct.triggered.connect(self.about)
        aboutQtAct.triggered.connect(qApp.aboutQt)
        
        fileMenu = self.menuBar().addMenu(self.tr("&File"))
        fileMenu.addAction(createProfileAct)
        fileMenu.addAction(loadProfileAct)
        fileMenu.addAction(exitAct)
        
        helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        helpMenu.addAction(aboutAct)
        helpMenu.addAction(aboutQtAct)
        
    def about(self):
        QMessageBox.about(self, 'About',
                          '''<p><b>Money Expenser</b> {0}</p>
                          <p>A personal expense recorder.</p>
                          <p>By Amulet<br />
                          <a href="http://ogc-daily.blogspot.com">http://ogc-daily.blogspot.com</a></p>'''
                          .format(__version__))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    app.exec_()
