import sys, mysql.connector, json, os, re
from PySide2.QtCore import Qt, QPointF
from PySide2.QtGui import QColor, QPalette, QFont, QConicalGradient, QGradient, QBrush, QKeySequence
from PySide2.QtWidgets import (QPushButton, QWidget, QMainWindow, QLineEdit, QDialog, QApplication,
                                QStyleFactory, QVBoxLayout, QHBoxLayout, QLabel, QFormLayout, QGridLayout,
                                QMessageBox, QShortcut)


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Login to Backend Discord GUI")

        grad = QPalette()
        gradient = QConicalGradient(QPointF(400, -10), 200)
        gradient.setColorAt(0.0, QColor(30, 30, 30))
        gradient.setColorAt(0.5, QColor(50, 50, 50))
        gradient.setColorAt(0.95, QColor(50, 13, 150))
        gradient.setColorAt(1.0, QColor(106, 13, 173))
        gradient.setSpread(QGradient.RepeatSpread)
        grad.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(grad)

        # Status Bar
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Looking for data...")
        self.searchData()

        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()    
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

        self.setCentralWidget(widget)

    def openSignUp(self):
        self.setCentralWidget(SignUpForm())
        self.setWindowTitle("Sign Up to Backend Discord GUI")
        self.setStatusBar("")

    def openLogIn(self):
        self.setCentralWidget(Form())
        self.setWindowTitle("Login to Backend Discord GUI")
        self.searchData()

    def searchData(self):
        try:
            with open("./app/data-store/._login.json", "r") as f:
                data = json.load(f)
                if data["hasPrevLogin"] == 1:
                    if data["un"] == "" or data["pw"] == "":
                        self.setStatusBar("Previous Login found, No Login Data found.")
                    else:
                        self.setStatusBar("Auto Login as {}".format(data["un"]))
                elif data["hasPrevLogin"] == 0:
                    self.setStatusBar("New Login User")
                else:
                    self.setStatusBar("ERROR: hasPrevLogin: not 1 or 0, app failed. New ._login.json file needed.", True)
        except Exception as e:
            self.setStatusBar("ERROR: no ._login.json file found.", True)
            print(e)

    def setStatusBar(self, text, isError=False):
        if isError:
            palette = QPalette()
            palette.setColor(QPalette.WindowText, QColor(175,0,0))
            self.statusbar.setPalette(palette)
        else:
            palette = QPalette()
            palette.setColor(QPalette.WindowText, Qt.white)
            self.statusbar.setPalette(palette)
        self.statusbar.showMessage(text)


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form,self).__init__(parent)

        self.setWindowTitle("Backend Discord-GUI")
        self.changeStyle('fusion')

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(60, 60, 60))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Base, QColor(40, 40, 40))
        palette.setColor(QPalette.ToolTipBase, QColor(60, 60, 60))
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.PlaceholderText, QColor(100, 60, 60))
        palette.setColor(QPalette.BrightText, Qt.white)
        palette.setColor(QPalette.Highlight, QColor(106, 13, 173))
        palette.setColor(QPalette.HighlightedText, Qt.white)

        mainLayout = QVBoxLayout()
        hMainLayout = QHBoxLayout()
        passwordLayout =QHBoxLayout()

        self.username = QLineEdit(self)
        self.QUserLabel = QLabel("Username")
        self.username.setStyleSheet("QToolTop { border: 0px; border-radius: 3px }")
        self.QUserLabel.setFont(QFont("Copperplate", 12))

        self.password = QLineEdit(self)
        self.QPasswordLabel = QLabel("Password")
        self.password.setStyleSheet("QToolTip { border: 0px; border-radius: 3px }")
        self.QPasswordLabel.setFont(QFont("Copperplate", 12))
        self.showhideButton = QPushButton("Show")
        self.showhideButton.setCheckable(True)
        self.showhideButton.setChecked(False)
        self.showhideButton.clicked.connect(lambda:self.show_hide())
        self.password.setEchoMode(QLineEdit.Password)
        passwordLayout.addWidget(self.QPasswordLabel)
        passwordLayout.addWidget(self.password)
        passwordLayout.addWidget(self.showhideButton)

        self.btn_Submit = QPushButton("Login")

        shortcut = QShortcut(QKeySequence("Return"), self.btn_Submit)
        shortcut.activated.connect(lambda: self.do_nothing())
        shortcut.setEnabled(True)

        self.btn_SignUp = QPushButton("Sign Up")
        self.btn_SignUp.clicked.connect(lambda:window.openSignUp())

        layout = QFormLayout()
        layout.addRow(self.QUserLabel,self.username)
        layout.addRow(passwordLayout)
        layout.addRow(self.btn_Submit)
        layout.addRow(self.btn_SignUp)

        Label = QLabel("Welcome To The\nBackend Discord-GUI Development")
        Label.setFont(QFont("Copperplate", 15, QFont.Bold))
        Label.setAlignment(Qt.AlignCenter)

        mainLayout.addSpacing(80)
        mainLayout.addWidget(Label)
        mainLayout.addLayout(layout)
        mainLayout.addSpacing(100)

        hMainLayout.addSpacing(125)
        hMainLayout.addLayout(mainLayout)
        hMainLayout.addSpacing(125)
        self.setLayout(hMainLayout)

        QApplication.setPalette(palette)

    def do_nothing(self):
        print("Logged In")

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            pass

    def show_hide(self):
        if self.showhideButton.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
            self.showhideButton.setText("Hide")
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.showhideButton.setText("Show")

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))


class SignUpForm(QDialog):
    def __init__(self, parent=None):
        super(SignUpForm,self).__init__(parent)

        self.checkedPass = 0

        self.setWindowTitle("Backend Discord-GUI")
        self.changeStyle('fusion')

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(60, 60, 60))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Base, QColor(40, 40, 40))
        palette.setColor(QPalette.ToolTipBase, QColor(60, 60, 60))
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.PlaceholderText, QColor(100, 60, 60))
        palette.setColor(QPalette.BrightText, Qt.white)
        palette.setColor(QPalette.Highlight, QColor(106, 13, 173))
        palette.setColor(QPalette.HighlightedText, Qt.white)

        mainLayout = QVBoxLayout()
        hMainLayout = QHBoxLayout()
        passwordLayout =QHBoxLayout()

        entryBG = QPalette()
        gradient = QGradient()
        gradient.setColorAt(0.0, QColor(30, 30, 30))
        gradient.setColorAt(0.4, QColor(30, 30, 30))
        gradient.setColorAt(1.0, QColor(70, 70, 70))
        gradient.setSpread(QGradient.RepeatSpread)
        entryBG.setBrush(QPalette.Button, QBrush(gradient))

        self.name = QLineEdit(self)
        self.name.setFixedHeight(24)
        self.name.setToolTip("Max 64 Characters")
        self.name.setStyleSheet("QToolTip { border: 0px; border-radius: 3px; }")
        self.name.setPalette(entryBG)
        self.QNameLabel = QLabel("Full Name")
        self.QNameLabel.setFont(QFont("Copperplate", 12))
        self.name.setMaxLength(64)

        self.email = QLineEdit(self)
        self.email.setFixedHeight(24)
        self.email.setToolTip("Max 128 Characters, Example - username@company.domain")
        self.email.setStyleSheet("QToolTip { border: 0px; border-radius: 3px }")
        self.email.setPalette(entryBG)
        self.QEmailLabel = QLabel("Email")
        self.QEmailLabel.setFont(QFont("Copperplate", 12))
        self.email.setMaxLength(128)

        self.username = QLineEdit(self)
        self.username.setFixedHeight(24)
        self.username.setToolTip("Max 16 Characters")
        self.username.setStyleSheet("QToolTip { border: 0px; border-radius: 3px }")
        self.username.setPalette(entryBG)
        self.QUserLabel = QLabel("Username")
        self.QUserLabel.setFont(QFont("Copperplate", 12))
        self.username.setMaxLength(16)

        self.password = QLineEdit(self)
        self.password.setFixedHeight(24)
        self.password.setToolTip("Max 32 Characters, Must Include = Uppercase Letter,\nNumber and Special Character")
        self.password.setStyleSheet("QToolTip { border: 0px; border-radius: 3px }")
        self.password.setPalette(entryBG)
        self.QPasswordLabel = QLabel("Password ")
        self.password.setMaxLength(32)
        self.QPasswordLabel.setFont(QFont("Copperplate", 12))
        self.showhideButton = QPushButton("Show")
        self.showhideButton.setCheckable(True)
        self.showhideButton.setChecked(False)
        self.showhideButton.clicked.connect(lambda:self.show_hide())
        self.password.setEchoMode(QLineEdit.Password)
        passwordLayout.addWidget(self.QPasswordLabel)
        passwordLayout.addWidget(self.password)
        passwordLayout.addWidget(self.showhideButton)

        self.btn_SignUp = QPushButton("Sign Up")
        self.btn_SignUp.clicked.connect(lambda:self.signUpWindow())

        shortcut = QShortcut(QKeySequence("Return"), self.btn_SignUp)
        shortcut.activated.connect(lambda: self.signUpWindow())
        shortcut.setEnabled(True)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(lambda:self.cancel())

        layout = QFormLayout()
        layout.addRow(self.QNameLabel,self.name)
        layout.addRow(self.QEmailLabel,self.email)
        layout.addRow(self.QUserLabel,self.username)
        layout.addRow(passwordLayout)
        layout.addRow(self.btn_SignUp)
        layout.addRow(self.btn_cancel)

        Label = QLabel("Sign Up To The\nBackend Discord-GUI Development")
        Label.setFont(QFont("Copperplate", 15, QFont.Bold))
        Label.setAlignment(Qt.AlignCenter)

        mainLayout.addSpacing(40)
        mainLayout.addWidget(Label)
        mainLayout.addLayout(layout)
        mainLayout.addSpacing(60)

        hMainLayout.addSpacing(115)
        hMainLayout.addLayout(mainLayout)
        hMainLayout.addSpacing(115)
        self.setLayout(hMainLayout)

        QApplication.setPalette(palette)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            pass

    def check_passwordCheck(self):
        if self.checkedPass <= 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Check Password?")
            msg.setInformativeText("Are you sure you want to Sign Up, you haven't checked your password. Do you want to proceed?")
            msg.setWindowTitle("Check Password?")
            msg.setDetailedText("We monitor basic actions you make, this is part of our policy. This MessageBox "+
            "was generated because we detected you did not check your password before clicking "+
            "the sign up button. We recommend this just incase you forget your password.\n\n"+
            "We believe in the best for our customers, so we try to minimise simple errors, "+
            "like this, to serve customers quicker when there is a higher priority support request.")
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg.buttonClicked.connect(self.signUp)
	
            retval = msg.exec_()
        else:
            self.signUp(proceed=True)

    def signUpWindow(self):
        namePassed, emailPassed, usernamePassed, passwordPassed = False, False, False, False
        errors = []
        if len(self.name.text()) <= 1:
            self.name.setStyleSheet("QLineEdit { border: 1px solid red; border-radius: 3px; } QToolTip { border: 0px }")
            errors.append("Name: Too Short")
        else:
            self.name.setStyleSheet("QLineEdit { border: 0px; border-radius: 3px; } QToolTip { border: 0px }")
            namePassed = True

        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.email.text()):
            self.email.setStyleSheet("QLineEdit { border: 0px; border-radius: 3px; } QToolTip { border: 0px }")
            emailPassed = True
        else:
            self.email.setStyleSheet("QLineEdit { border: 1px solid red; border-radius: 3px; } QToolTip { border: 0px }")
            errors.append("Email: This is not a valid Email")

        if len(self.username.text()) <= 2:
            self.username.setStyleSheet("QLineEdit { border: 1px solid red; border-radius: 3px; } QToolTip { border: 0px }")
            errors.append("Username: Too Short")
        else:
            if re.match(r"([a-zA-Z0-9_]+$)", self.username.text()):
                self.username.setStyleSheet("QLineEdit { border: 0px; border-radius: 3px; } QToolTip { border: 0px }")
                usernamePassed = True
            else:
                self.username.setStyleSheet("QLineEdit { border: 1px solid red; border-radius: 3px; } QToolTip { border: 0px }")
                errors.append("Username: Can only have, a-z (A-Z), 0-9 and '_'")

        if len(self.password.text()) <= 7:
            self.password.setStyleSheet("QLineEdit { border: 1px solid red; border-radius: 3px; } QToolTip { border: 0px }")
            errors.append("Password: Too Short")
        else:
            if re.match(r'^.*(?=.{8,10})(?=.*[a-zA-Z])(?=.*?[A-Z])(?=.*\d)[a-zA-Z0-9!@£$%^&*()_+={}?:~\[\]]+$', self.password.text()):
                self.password.setStyleSheet("QLineEdit { border: 0px; border-radius: 3px; } QToolTip { border: 0px }")
                passwordPassed = True
            else:
                self.password.setStyleSheet("QLineEdit { border: 1px solid red; border-radius: 3px; } QToolTip { border: 0px }")
                errors.append("Password: Needs to have, Capital Letter, Number, Special Character")

        if namePassed and emailPassed and usernamePassed and passwordPassed:
            self.check_passwordCheck()
        else:
            if len(errors) > 2:
                string = "; ".join(errors[:2])
                overall_string = str("Errors: " + string + " +{} more".format(len(errors)-2))
            else:
                string = "; ".join(errors)
                overall_string = str("Errors: " + string)
            window.setStatusBar(overall_string, True)

    def signUp(self, i=None, proceed=False):
        if i != None:
            if i.text() == "&Yes":
                signUp = True
                QApplication.quit()
            else: pass
        signUp = proceed
        if signUp == True:
            print("Signed Up")
            QApplication.quit()

    def show_hide(self):
        if self.showhideButton.isChecked():
            self.checkedPass += 1
            self.password.setEchoMode(QLineEdit.Normal)
            self.showhideButton.setText("Hide")
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.showhideButton.setText("Show")


    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))

    def cancel(self):
        window.openLogIn()


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    widget = Form()
    # QMainWindow using QWidget as central widget
    window = MainWindow(widget)
    window.setMinimumSize(600,400)
    window.setMaximumSize(600,400)
    window.resize(600, 400)
    window.show()

    # Execute application
    sys.exit(app.exec_())