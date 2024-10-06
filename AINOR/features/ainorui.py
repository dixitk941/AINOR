from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 907)
        MainWindow.setStyleSheet("background-color: #282c34;")  # Dark background
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Background Animation (Optional)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1440, 900))
        self.label.setPixmap(QtGui.QPixmap("AINOR/utils/images/Designer.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # Modern Button Style
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1180, 790, 101, 51))
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: rgb(0, 170, 255);
                font: 75 18pt "MS Shell Dlg 2";
                border-radius: 10px;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: rgb(0, 150, 200);
            }
            QPushButton:pressed {
                background-color: rgb(0, 130, 150);
            }
        """)
        self.pushButton.setObjectName("pushButton")
        
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1310, 790, 101, 51))
        self.pushButton_2.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 0, 0);
                font: 75 18pt "MS Shell Dlg 2";
                border-radius: 10px;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: rgb(200, 0, 0);
            }
            QPushButton:pressed {
                background-color: rgb(150, 0, 0);
            }
        """)
        self.pushButton_2.setObjectName("pushButton_2")
        
        # Animated Label (GIF)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 401, 91))
        self.label_2.setPixmap(QtGui.QPixmap("AINOR/utils/images/initiating.gif"))
        self.label_2.setObjectName("label_2")
        
        # Modern Text Browser
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(640, 30, 291, 61))
        self.textBrowser.setStyleSheet("""
            font: 75 16pt "MS Shell Dlg 2";
            background-color: transparent;
            color: white;  # Text color
            border: none;
            padding: 5px;
        """)
        self.textBrowser.setObjectName("textBrowser")
        
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(930, 30, 291, 61))
        self.textBrowser_2.setStyleSheet("""
            font: 75 16pt "MS Shell Dlg 2";
            background-color: transparent;
            color: white;  # Text color
            border: none;
            padding: 5px;
        """)
        self.textBrowser_2.setObjectName("textBrowser_2")
        
        # Command Output Text Browser
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setGeometry(QtCore.QRect(1000, 500, 431, 281))
        self.textBrowser_3.setStyleSheet("""
            font: 11pt "MS Shell Dlg 2";
            background-color: transparent;
            color: white;  # Text color
            border: none;
            padding: 5px;
        """)
        self.textBrowser_3.setObjectName("textBrowser_3")

        # Connect the button to display output
        self.pushButton.clicked.connect(self.displayCommandOutput)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AINOR"))
        self.pushButton.setText(_translate("MainWindow", "Run"))
        self.pushButton_2.setText(_translate("MainWindow", "Exit"))

    def displayCommandOutput(self):
        # Simulate command execution and display output
        command_output = "Command executed successfully!"  # Example output
        self.textBrowser_3.append(command_output)  # Append output to the text browser

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())