import sys, random
from sys import platform
from PySide2.QtCore import Slot, Qt, QPointF, QTimer, QObject, QPoint
from PySide2.QtGui import (QPalette, QColor, QConicalGradient, QGradient, QBrush, QKeySequence, QPainter, QPen, QFont)
from PySide2.QtWidgets import (QWidget, QMainWindow, QGroupBox, QPushButton, QApplication, QStyleFactory,
                                QHBoxLayout, QVBoxLayout, QLabel, QDirModel, QTreeView, QProgressBar,
                                QGridLayout, QAction, QDesktopWidget, QScrollArea, QShortcut, QDialog, QListWidget,
                                QLineEdit)

PLATFORM = platform


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

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
        palette.setColor(QPalette.PlaceholderText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.white)
        palette.setColor(QPalette.Highlight, QColor(106, 13, 173))
        palette.setColor(QPalette.HighlightedText, Qt.white)

        topButtonLayout = QGroupBox("Configurations")
        topStatsLayout = QGroupBox("Statistics")

        layoutLeft = QHBoxLayout()

        botConfigButton = QPushButton("Bot Config")
        botConfigButton.clicked.connect(lambda: CommentPopup())
        serverSettingsButton = QPushButton("Server Settings")
        settingsButton = QPushButton("Settings")

        layoutLeft.addWidget(botConfigButton)
        layoutLeft.addWidget(serverSettingsButton)
        layoutLeft.addWidget(settingsButton)

        layoutRight = QVBoxLayout()

        botReadyLabel = QLabel("Bot_Ready: False")
        botStatusLabel = QLabel("Bot_Status: Off")
        # botDatabaseLabel = QLabel("Bot_Database: None")
        # botStandbyLabel = QLabel("Bot_Standby: False")

        layoutRight.addWidget(botReadyLabel)
        layoutRight.addWidget(botStatusLabel)
        # layoutRight.addWidget(botDatabaseLabel)
        # layoutRight.addWidget(botStandbyLabel)

        topButtonLayout.setLayout(layoutLeft)
        topStatsLayout.setLayout(layoutRight)

        self.createLeftSide()
        self.createRightSide()
        self.createProgressBar()

        topLayout = QGridLayout()
        topLayout.addWidget(topButtonLayout, 0, 0)
        topLayout.addWidget(topStatsLayout, 0, 1)
        topLayout.setColumnStretch(0, 1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.leftSideGB, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 2)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 2)
        self.setLayout(mainLayout)

        QApplication.setPalette(palette)

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))

    def advanceProgressBarLoading(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        if curVal != maxVal:
            num = random.randint(1,30)
            self.progressBar.setValue(curVal + num)
        else:
            self.timer.stop()
            change_status('Ready')
            self.progressBar.setValue(0)

    def createLeftSide(self):
        self.leftSideGB = QGroupBox()

        home_directory = "./app/"

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))

        model = QDirModel()
        view = QTreeView()
        view.setStyleSheet("QTreeView { border: 0px; }")
        view.setModel(model)
        view.setRootIndex(model.index(home_directory))
        view.setColumnHidden(1, True)
        view.setColumnHidden(2, True)
        view.setColumnHidden(3, True)
        view.show()
        view.setPalette(palette)

        runButton = QPushButton("►")
        stopButton = QPushButton("❚❚")

        bottomBar = QHBoxLayout()
        bottomBar.addWidget(runButton)
        bottomBar.addWidget(stopButton)

        layout = QVBoxLayout()
        layout.addWidget(view)
        layout.addLayout(bottomBar)
        layout.setStretch(0, 2)
        self.leftSideGB.setLayout(layout) 

    def createRightSide(self):
        self.topRightGroupBox = QGroupBox()
        self.totalLength = 0
        self.elems = 0
        self.elems_list = []

        self.overall_layout = QVBoxLayout()

        grad = QPalette()
        gradient = QConicalGradient(QPointF(1100, 150), -190)
        gradient.setColorAt(0.0, QColor(30, 30, 30))
        gradient.setColorAt(0.5, QColor(50, 50, 50))
        gradient.setColorAt(0.97, QColor(50, 13, 150))
        gradient.setColorAt(1.0, QColor(106, 13, 173))
        gradient.setSpread(QGradient.RepeatSpread)
        grad.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(grad)

        self.scrollarea = QScrollArea()
        self.scrollarea.setWidgetResizable(True)

        self.widget = QWidget()
        self.scrollarea.setWidget(self.widget)

        self.layout = QVBoxLayout(self.widget)

        self.add_elem = QPushButton("Add Element")
        if PLATFORM == "darwin": self.add_elem.setToolTip("Shortcut: ⌘E")
        else: self.add_elem.setToolTip("Shortcut: Ctrl+E")
        self.add_elem.setStyleSheet("QToolTip { border: 0px; border-radius: 3px }")
        self.add_elem.clicked.connect(lambda: ElementPopup())
        self.add_elem.setFixedWidth(300)

        shortcut = QShortcut(QKeySequence("Ctrl+E"), self.add_elem)
        shortcut.activated.connect(lambda: ElementPopup())
        shortcut.setEnabled(True)

        self.layout.addWidget(self.add_elem)
        self.layout.setAlignment(self.add_elem, Qt.AlignCenter | Qt.AlignTop)
        self.overall_layout.addWidget(self.scrollarea)
        self.topRightGroupBox.setLayout(self.overall_layout)

    def add_element(self, title, type, isDupe=False, indexForDupe=0, data=""):
        # open form of widget lists
        if data != "": title = title + ": " + data
        elem = create_elem(title, type, data)
        self.elems_list.append(elem.getElem())
        self.elems += 1
        self.totalLength += 100

        if isDupe:
            self.layout.insertWidget(indexForDupe+1,self.elems_list[self.elems - 1])
        else:
            self.layout.insertWidget(self.elems-1,self.elems_list[self.elems - 1])

        if self.totalLength > self.topRightGroupBox.height():
            self.scrollarea.verticalScrollBar().setMaximum(self.scrollarea.verticalScrollBar().maximum() + 85)
            self.scrollarea.verticalScrollBar().setValue(self.scrollarea.verticalScrollBar().maximum())
        self.topRightGroupBox.update()

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setFixedHeight(5)

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.advanceProgressBarLoading)
        # self.timer.start(10)

    @Slot()
    def quit_application(self):
        QApplication.quit()


class CommentPopup(QDialog):
    def __init__(self, prevData=None):
        super().__init__()
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setLayout(QVBoxLayout())
        mainLayout = QGroupBox("Comment Settings")
        self.resize(600,400)

        layout = QHBoxLayout()
        button_save = QPushButton('Save')
        button_close = QPushButton('Close')
        layout.addWidget(button_save)
        layout.addWidget(button_close)

        topLayout = QVBoxLayout()
        middleLayout = QHBoxLayout()
        if prevData == None: self.entry = QLineEdit()
        else: self.entry = QLineEdit(prevData)
        label = QLabel("Text:")
        middleLayout.addWidget(label)
        middleLayout.addWidget(self.entry)
        help = QLabel("<b>Comment</b>: Used for nothing more than a reminder, it does not directly affect the code<br>" +
                                    "itself. It will be shown when exporting a bot to a coded langauge.")
        topLayout.addLayout(middleLayout)
        topLayout.addWidget(help)
        topLayout.setAlignment(middleLayout, Qt.AlignTop)
        topLayout.setAlignment(help, Qt.AlignBottom)
        mainLayout.setLayout(topLayout)

        self.layout().addWidget(mainLayout)
        self.layout().addLayout(layout)

        button_save.clicked.connect(lambda: self.saveElement())
        button_close.clicked.connect(self.close)
        self.exec_()

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.center())

    def saveElement(self):
        self.close()
        return self.entry.text()
        # widget.add_element(selectedItem[0].text())
        # self.close()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


class ElementPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setLayout(QVBoxLayout())
        self.resize(300, 300)
        layout = QHBoxLayout()
        button_add = QPushButton('Add')
        button_close = QPushButton('Close')
        self.list_widget = QListWidget()
        self.list_widget.addItem("Comment")
        self.list_widget.addItem("Channel Send")
        layout.addWidget(button_add)
        layout.addWidget(button_close)
        self.layout().addWidget(self.list_widget)
        self.layout().addLayout(layout)
        button_add.clicked.connect(lambda: self.addElement())
        button_close.clicked.connect(self.close)
        self.exec_()

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.center())

    def addElement(self):
        selectedItem = self.list_widget.selectedItems()
        try: widget.add_element(selectedItem[0].text(), selectedItem[0].text())
        except: pass
        self.close()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Backend Discord GUI")

        grad = QPalette()
        gradient = QConicalGradient(QPointF(700, -10), 195)
        gradient.setColorAt(0.0, QColor(30, 30, 30))
        gradient.setColorAt(0.5, QColor(50, 50, 50))
        gradient.setColorAt(0.97, QColor(50, 13, 150))
        gradient.setColorAt(1.0, QColor(106, 13, 173))
        gradient.setSpread(QGradient.RepeatSpread)
        grad.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(grad)

        # Status Bar
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Preparing Window...")

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Menu
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("File")

        new_bot_proj = QAction("New Bot Project", self)
        new_bot_proj.setShortcut("Ctrl+P")
        new_bot_proj.setStatusTip('Create a new Bot')
        new_bot_proj.triggered.connect(self.do_nothing)

        new_bot_file = QAction("New Bot File", self)
        new_bot_file.setShortcut("Ctrl+N")
        new_bot_file.setStatusTip('Create a new Command file')
        new_bot_file.triggered.connect(self.do_nothing)

        new_int_play = QAction("New Interactive Playground", self)
        new_int_play.setStatusTip('Create a Test App')
        new_int_play.triggered.connect(self.do_nothing)

        open_bot_proj = QAction("Open Bot Project", self)
        open_bot_proj.setShortcut("Ctrl+O")
        open_bot_proj.setStatusTip('Open a Bot Project')
        open_bot_proj.triggered.connect(self.do_nothing)

        open_bot_file = QAction("Open Bot File", self)
        open_bot_file.setStatusTip('Open a Command file')
        open_bot_file.triggered.connect(self.do_nothing)

        open_bot_iplay = QAction("Open Interactive Playground", self)
        open_bot_iplay.setStatusTip('Open a Test App')
        open_bot_iplay.triggered.connect(self.do_nothing)

        add_bot_file = QAction("Add Bot File", self)
        add_bot_file.setStatusTip('Add existing Command file')
        add_bot_file.triggered.connect(self.do_nothing)

        save_bot_proj = QAction("Save Bot Project", self)
        save_bot_proj.setStatusTip('Save a Bot Project')
        save_bot_proj.triggered.connect(self.do_nothing)

        save_bot_file = QAction("Save Bot File", self)
        save_bot_file.setStatusTip('Save a Command file')
        save_bot_file.triggered.connect(self.do_nothing)

        save_all = QAction("Save All", self)
        save_all.setShortcut("Ctrl+S")
        save_all.triggered.connect(self.do_nothing)

        close_editor = QAction("Close Editor", self)
        close_editor.setStatusTip('Close the editor only')
        close_editor.triggered.connect(self.do_nothing)

        close_workspace = QAction("Close Workspace", self)
        close_workspace.setShortcut("Ctrl+Q")
        close_workspace.setStatusTip('Close everything')
        close_workspace.triggered.connect(self.do_nothing)

        file_menu.addAction(new_bot_proj)
        file_menu.addAction(new_bot_file)
        file_menu.addAction(new_int_play)
        file_menu.addSeparator()
        file_menu.addAction(open_bot_proj)
        file_menu.addAction(open_bot_file)
        file_menu.addAction(open_bot_iplay)
        file_menu.addAction(add_bot_file)
        file_menu.addSeparator()
        file_menu.addAction(save_bot_proj)
        file_menu.addAction(save_bot_file)
        file_menu.addAction(save_all)
        file_menu.addSeparator()
        file_menu.addAction(close_editor)
        file_menu.addAction(close_workspace)

        edit_menu = self.menu.addMenu("Edit")

        find_file = QAction("Find File", self)
        find_file.setShortcut("Ctrl+F")
        find_file.setStatusTip("Find a Command")
        find_file.triggered.connect(self.do_nothing)

        file_settings = QAction("Open Find Settings", self)
        file_settings.setShortcut("Ctrl+Shift+S")
        file_settings.setStatusTip("Find a Command")
        file_settings.triggered.connect(self.do_nothing)

        toggle_file = QAction("Toggle File", self, checkable=True)
        toggle_file.setStatusTip("Toggles a Command file to be used")
        toggle_file.setChecked(True)
        toggle_file.triggered.connect(self.do_nothing)

        delete_file = QAction("Delete File", self)
        delete_file.setShortcut("Ctrl+Backspace")
        delete_file.setStatusTip("Delete a Command file")
        delete_file.triggered.connect(self.do_nothing)

        remove_file = QAction("Remove File", self)
        remove_file.setStatusTip("Removes a Command file from workspace")
        remove_file.triggered.connect(self.do_nothing)

        edit_menu.addAction(find_file)
        edit_menu.addAction(file_settings)
        edit_menu.addAction(toggle_file)
        edit_menu.addSeparator()
        edit_menu.addAction(delete_file)
        edit_menu.addAction(remove_file)

        viewMenu = self.menu.addMenu('View')

        command_palette = QAction("Command Palette", self)
        command_palette.setShortcut("Ctrl+Shift+P")
        command_palette.setStatusTip("Delete a Command file")
        command_palette.triggered.connect(self.do_nothing)
        
        open_view = QAction("Open View", self)
        open_view.setStatusTip("Delete a Command file")
        open_view.triggered.connect(self.do_nothing)

        appearance_settings = QAction("Appearance Settings", self)
        appearance_settings.setStatusTip("Delete a Command file")
        appearance_settings.triggered.connect(self.do_nothing)

        output_console = QAction("Output Console", self)
        output_console.setStatusTip("Delete a Command file")
        output_console.triggered.connect(self.do_nothing)

        debug_console = QAction("Debug Console", self)
        debug_console.setStatusTip("Delete a Command file")
        debug_console.triggered.connect(self.do_nothing)

        error_log = QAction("Error Log", self)
        error_log.setStatusTip("Delete a Command file")
        error_log.triggered.connect(self.do_nothing)

        view_logs = QAction("View All Logs", self)
        view_logs.setStatusTip("Delete a Command file")
        view_logs.triggered.connect(self.do_nothing)

        viewStatAct = QAction('View statusbar', self, checkable=True)
        viewStatAct.setStatusTip('View statusbar')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.toggleMenu)

        viewMenu.addAction(command_palette)
        viewMenu.addAction(open_view)
        viewMenu.addSeparator()
        viewMenu.addAction(appearance_settings)
        viewMenu.addSeparator()
        viewMenu.addAction(output_console)
        viewMenu.addAction(debug_console)
        viewMenu.addAction(error_log)
        viewMenu.addAction(view_logs)
        viewMenu.addSeparator()
        viewMenu.addAction(viewStatAct)

        runMenu = self.menu.addMenu('Run')

        start = QAction("Start", self)
        start.setShortcut("Ctrl+R")
        start.setStatusTip("Begin to start Command")
        start.triggered.connect(self.do_nothing)

        stop = QAction("Stop", self)
        stop.setShortcut("Ctrl+T")
        stop.setStatusTip("Terminate the Command")
        stop.triggered.connect(self.do_nothing)

        test_file = QAction("Test File", self)
        test_file.setStatusTip("Test the Command open on test server")
        test_file.triggered.connect(self.do_nothing)

        test_server = QAction("Test Server Connect", self)
        test_server.setShortcut("Ctrl+Shift+R")
        test_server.setStatusTip("Test server connection")
        test_server.triggered.connect(self.do_nothing)

        test_ping = QAction("Test Activity Ping", self)
        test_ping.setStatusTip("Test Bot API connection")
        test_ping.triggered.connect(self.do_nothing)

        test_commands = QAction("Test Ping Commands", self)
        test_commands.setStatusTip("Test all commands received")
        test_commands.triggered.connect(self.do_nothing)

        open_test_logs = QAction("View Test Logs", self)
        open_test_logs.setStatusTip("Open the logs for testing")
        open_test_logs.triggered.connect(self.do_nothing)

        runMenu.addAction(start)
        runMenu.addAction(stop)
        runMenu.addSeparator()
        runMenu.addAction(test_file)
        runMenu.addAction(test_server)
        runMenu.addAction(test_ping)
        runMenu.addAction(test_commands)
        runMenu.addAction(open_test_logs)

        terminalMenu = self.menu.addMenu('Terminal')

        start_bot = QAction("Start Bot", self)
        start_bot.setStatusTip("Begin to start Bot")
        start_bot.triggered.connect(self.do_nothing)

        stop_bot = QAction("Stop Bot", self)
        stop_bot.setStatusTip("Terminate the Bot")
        stop_bot.triggered.connect(self.do_nothing)

        terminal_logs = QAction("View Terminal Logs", self)
        terminal_logs.setStatusTip("Opens the Terminal logs")
        terminal_logs.triggered.connect(self.do_nothing)

        python_discord = QAction("Build Task as Python Discord", self)
        python_discord.setStatusTip("Builds the Bot in Python Programming Language")
        python_discord.triggered.connect(self.do_nothing)

        javascript_discord = QAction("Build Task as Javascript Discord", self)
        javascript_discord.setStatusTip("Builds the Bot in Javascript Programming Language")
        javascript_discord.triggered.connect(self.do_nothing)

        discordGUI_discord = QAction("Build Task as Discord-GUI", self)
        discordGUI_discord.setShortcut("Ctrl+Shift+W")
        discordGUI_discord.setStatusTip("Builds the Bot in Discord-GUI Readable Language")
        discordGUI_discord.triggered.connect(self.do_nothing)

        build_errors = QAction("View Build Errors", self)
        build_errors.setStatusTip("Opens the Build Error Log")
        build_errors.triggered.connect(self.do_nothing)

        terminalMenu.addAction(start_bot)
        terminalMenu.addAction(stop_bot)
        terminalMenu.addSeparator()
        terminalMenu.addAction(terminal_logs)
        terminalMenu.addSeparator()
        terminalMenu.addAction(python_discord)
        terminalMenu.addAction(javascript_discord)
        terminalMenu.addAction(discordGUI_discord)
        terminalMenu.addAction(build_errors)

        windowMenu = self.menu.addMenu('Window')

        hide = QAction("Hide", self)
        hide.setStatusTip("Hide the Window")
        hide.triggered.connect(self.do_nothing)

        minimise = QAction("Minimise", self)
        minimise.setStatusTip("Minimise the Window")
        minimise.triggered.connect(self.do_nothing)

        maximise = QAction("Maximise", self)
        maximise.setStatusTip("Maximise the Window")
        maximise.triggered.connect(self.do_nothing)

        settings = QAction("Discord-GUI Settings", self)
        settings.setShortcut("Ctrl+L")
        settings.setStatusTip("Opens Discord-GUI's Settings")
        settings.triggered.connect(self.do_nothing)

        directory = QAction("Open Discord-GUI Directory", self)
        directory.setStatusTip("Goto the Discord-GUI Directory")
        directory.triggered.connect(self.do_nothing)

        windowMenu.addAction(hide)
        windowMenu.addAction(minimise)
        windowMenu.addAction(maximise)
        windowMenu.addSeparator()
        windowMenu.addAction(settings)
        windowMenu.addAction(directory)

        helpMenu = self.menu.addMenu('Help')

        welcome = QAction("Welcome", self)
        welcome.setStatusTip("Displays Welcome Message")
        welcome.triggered.connect(self.do_nothing)

        int_play = QAction("Interactive Playground", self)
        int_play.setStatusTip("Displays Interactive Playground Help")
        int_play.triggered.connect(self.do_nothing)

        docs = QAction("Documentation", self)
        docs.setStatusTip("Redirects to the Documentation of the app")
        docs.triggered.connect(self.do_nothing)

        keys_shorts = QAction("Keyboard Shortcuts", self)
        keys_shorts.setStatusTip("Displays Keyboard Shortcuts")
        keys_shorts.triggered.connect(self.do_nothing)

        report_issue = QAction("Report Issue", self)
        report_issue.setStatusTip("Redirects to Reporting an Issue")
        report_issue.triggered.connect(self.do_nothing)

        more_help = QAction("More Help", self)
        more_help.setStatusTip("Redirects to More Help Page")
        more_help.triggered.connect(self.do_nothing)

        helpMenu.addAction(welcome)
        helpMenu.addAction(int_play)
        helpMenu.addAction(docs)
        helpMenu.addSeparator()
        helpMenu.addAction(keys_shorts)
        helpMenu.addAction(report_issue)
        helpMenu.addAction(more_help)

        self.setCentralWidget(widget)

    def do_nothing(self, state):
        pass

    def toggleMenu(self, state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

    def exit_app(self, state):
        QApplication.quit()


class create_elem(QGroupBox):
    def __init__(self, name, type, data=""):
        QGroupBox.__init__(self)

        if name.find(": ") != -1: name = name.split(": ")[0]
        self.name, self.type = name, type
        self.data = data

        self.defaultElement = QGroupBox()
        mainElementLayout = QVBoxLayout()
        elementLayout = QHBoxLayout()
        if self.data == "": self.lName = QLabel(str(name))
        else: self.lName = QLabel(str(name) + ": " + str(self.data))
        self.lName.setMinimumSize(10,10)
        duplicate = QPushButton("❐")
        duplicate.clicked.connect(lambda: self.duplicateElement())
        edit = QPushButton("✎")
        edit.clicked.connect(lambda: self.editText())
        remove = QPushButton("×")
        remove.clicked.connect(lambda: self.delElement())
        elementLayout.addWidget(self.lName)
        elementLayout.addWidget(duplicate)
        elementLayout.addWidget(edit)
        elementLayout.addWidget(remove)
        elementLayout.setStretch(0, 2)
        mainElementLayout.addLayout(elementLayout)
        mainElementLayout.addSpacing(10)
        self.defaultElement.setLayout(mainElementLayout)
        self.defaultElement.setFixedHeight(80)

    def editText(self):
        if self.type == "Comment":
            if self.data != "": text = CommentPopup(self.data)
            else: text = CommentPopup()
            self.data = text.saveElement()
            if self.data == "": self.lName.setText(self.name)
            else: self.lName.setText(self.name + ": " + self.data)

    def getElem(self):
        return self.defaultElement

    def duplicateElement(self):
        index = widget.elems_list.index(self.defaultElement)
        if self.type == "Comment":
            widget.add_element(self.name, self.type, True, index, self.data)

    def delElement(self):
        self.defaultElement.deleteLater()
        widget.elems -= 1
        widget.layout.removeWidget(self.defaultElement)
        widget.elems_list.remove(self.defaultElement)
        widget.update()


def change_status(text):
    window.statusbar.showMessage(str(text))

if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    widget = Widget()
    # QMainWindow using QWidget as central widget
    window = MainWindow(widget)
    window.setMinimumSize(1000,600)
    window.resize(1000, 600)
    window.show()

    # Execute application
    sys.exit(app.exec_())
