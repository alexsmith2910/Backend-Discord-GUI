
from tkinter import *
from tkinter import messagebox

class MainWindow:
    def __init__(self):

        self.window = Tk()
        self.window.geometry("500x600")
        self.window.title("Discord-GUI")

        self.loadMenuAssets()
        self.loadMainAssets()
        
        self.window.mainloop()

    def loadMainAssets(self):
        
        self.topFrame = Frame(self.window, width=500, height=50, bg='grey15')
        self.topFrame.place(x=0,y=0)
        self.btn_bot_settings = Button(self.topFrame, text="Bot\nSettings", width=11, height=2)
        self.btn_unknown = Button(self.topFrame, text="?", width=11, height=2)
        self.btn_remove_elem = Button(self.topFrame, text="Remove\nElement", width=11, height=2)
        self.btn_add_elem = Button(self.topFrame, text="Add\nElement", width=11, height=2)
        self.btn_bot_settings.pack(side=LEFT, padx=(20,12))
        self.btn_unknown.pack(side=LEFT, padx=12)
        self.btn_remove_elem.pack(side=LEFT, padx=12)
        self.btn_add_elem.pack(side=LEFT, padx=(12,20))

    def loadMenuAssets(self):

        self.topMenu = Menu(self.window)
        
        self.fileMenu = Menu(self.topMenu)
        self.fileMenu.add_command(label="New Bot Project", command=lambda: self.ctrl_p(), accelerator="Ctrl+P")
        self.fileMenu.add_command(label="New Bot File", command=lambda: self.ctrl_n(), accelerator="Ctrl+N")
        self.fileMenu.add_command(label="New Interactive Playground", command=lambda: self.do_nothing())
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Open Bot Project", command=lambda: self.ctrl_o(), accelerator="Ctrl+O")
        self.fileMenu.add_command(label="Open Bot File", command=lambda: self.do_nothing())
        self.fileMenu.add_command(label="Open Interactive Playground", command=lambda: self.do_nothing())
        self.fileMenu.add_command(label="Add Bot File", command=lambda: self.do_nothing())
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Save Bot Project", command=lambda: self.do_nothing())
        self.fileMenu.add_command(label="Save Bot File", command=lambda: self.do_nothing())
        self.fileMenu.add_command(label="Save All", command=lambda: self.ctrl_s(), accelerator="Ctrl+S")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Close Editor", command=lambda: self.do_nothing())
        self.fileMenu.add_command(label="Close Workspace", command=lambda: self.ctrl_q(), accelerator="Ctrl+Q")

        self.editMenu = Menu(self.topMenu)
        self.editMenu.add_command(label="Find File", command=lambda: self.ctrl_f(), accelerator="Ctrl+F")
        self.editMenu.add_command(label="Open File Settings", command=lambda: self.ctrl_shift_s(), accelerator="Shift+Ctrl+S")
        self.editMenu.add_command(label="Toggle File", command=lambda: self.do_nothing())
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Delete File", command=lambda: self.ctrl_backspace(), accelerator="Ctrl+Backspace")
        self.editMenu.add_command(label="Remove File", command=lambda: self.do_nothing())

        self.viewMenu = Menu(self.topMenu)
        self.viewMenu.add_command(label="Command Palette", command=lambda: self.ctrl_shift_p(), accelerator="Shift+Ctrl+P")
        self.viewMenu.add_command(label="Open View", command=lambda: self.do_nothing())
        self.viewMenu.add_separator()
        self.viewMenu.add_command(label="Appearance Settings", command=lambda: self.do_nothing())
        self.viewMenu.add_separator()
        self.viewMenu.add_command(label="Output Console", command=lambda: self.do_nothing())
        self.viewMenu.add_command(label="Debug Console", command=lambda: self.do_nothing())
        self.viewMenu.add_command(label="Problems Log", command=lambda: self.do_nothing())
        self.viewMenu.add_command(label="View Logs", command=lambda: self.do_nothing())

        self.runMenu = Menu(self.topMenu)
        self.runMenu.add_command(label="Start", command=lambda: self.ctrl_r(), accelerator="Ctrl+R")
        self.runMenu.add_command(label="Stop", command=lambda: self.ctrl_t(), accelerator="Ctrl+T")
        self.runMenu.add_separator()
        self.runMenu.add_command(label="Test File", command=lambda: self.do_nothing())
        self.runMenu.add_separator()
        self.runMenu.add_command(label="Test Server Connect", command=lambda: self.ctrl_shift_r(), accelerator="Shift+Ctrl+R")
        self.runMenu.add_command(label="Test Activity Connect", command=lambda: self.do_nothing())
        self.runMenu.add_command(label="Test Ping Commands", command=lambda: self.do_nothing())
        self.runMenu.add_command(label="View Test Logs", command=lambda: self.do_nothing())

        self.terminalMenu = Menu(self.topMenu)
        self.terminalMenu.add_command(label="Start Bot", command=lambda: self.do_nothing())
        self.terminalMenu.add_command(label="Stop Bot", command=lambda: self.do_nothing())
        self.terminalMenu.add_separator()
        self.terminalMenu.add_command(label="View Terminal Logs", command=lambda: self.do_nothing())
        self.terminalMenu.add_separator()
        self.terminalMenu.add_command(label="Build Task as Python Discord", command=lambda: self.do_nothing())
        self.terminalMenu.add_command(label="Build Task as Javasript Discord", command=lambda: self.do_nothing())
        self.terminalMenu.add_command(label="Build Task as Discord-GUI", command=lambda: self.ctrl_shift_w(), accelerator="Shift+Ctrl+W")
        self.terminalMenu.add_command(label="View Build Errors", command=lambda: self.do_nothing())

        self.windowMenu = Menu(self.topMenu)
        self.windowMenu.add_command(label="Hide", command=lambda: self.do_nothing())
        self.windowMenu.add_command(label="Minimise", command=lambda: self.do_nothing())
        self.windowMenu.add_command(label="Maximise", command=lambda: self.do_nothing())
        self.windowMenu.add_separator()
        self.windowMenu.add_command(label="Discord-GUI Settings", command=lambda: self.ctrl_l(), accelerator="Ctrl+L")
        self.windowMenu.add_command(label="Open Discord-GUI Directory", command=lambda: self.do_nothing())

        self.helpMenu = Menu(self.topMenu)
        self.helpMenu.add_command(label="Welcome", command=lambda: self.do_nothing())
        self.helpMenu.add_command(label="Interactive Playground", command=lambda: self.do_nothing())
        self.helpMenu.add_command(label="Documentation", command=lambda: self.do_nothing())
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label="Keyboard Shortcuts", command=lambda: self.do_nothing())
        self.helpMenu.add_command(label="Report Issue", command=lambda: self.do_nothing())
        self.helpMenu.add_command(label="More Help", command=lambda: self.do_nothing())

        self.topMenu.add_cascade(label="File", menu=self.fileMenu)
        self.topMenu.add_cascade(label="Edit", menu=self.editMenu)
        self.topMenu.add_cascade(label="View", menu=self.viewMenu)
        self.topMenu.add_cascade(label="Run", menu=self.runMenu)
        self.topMenu.add_cascade(label="Terminal", menu=self.terminalMenu)
        self.topMenu.add_cascade(label="Window", menu=self.windowMenu)
        self.topMenu.add_cascade(label="Help", menu=self.helpMenu)
        self.window.config(menu=self.topMenu)

        self.window.bind('<Control-p>', (lambda event: self.ctrl_p()))
        self.window.bind('<Control-n>', (lambda event: self.ctrl_n()))
        self.window.bind('<Control-o>', (lambda event: self.ctrl_o()))
        self.window.bind('<Control-s>', (lambda event: self.ctrl_s()))
        self.window.bind('<Control-q>', (lambda event: self.ctrl_q()))
        self.window.bind('<Control-f>', (lambda event: self.ctrl_f()))
        self.window.bind('<Control-Shift-S>', (lambda event: self.ctrl_shift_s()))
        #self.window.bind('<Control-BackSpace>', (lambda event: self.ctrl_backspace())) # seems to already work with MenuBar
        self.window.bind('<Control-Shift-P>', (lambda event: self.ctrl_shift_p()))
        self.window.bind('<Control-r>', (lambda event: self.ctrl_r()))
        self.window.bind('<Control-t>', (lambda event: self.ctrl_t()))
        self.window.bind('<Control-Shift-R>', (lambda event: self.ctrl_shift_r()))
        self.window.bind('<Control-Shift-W>', (lambda event: self.ctrl_shift_w()))
        self.window.bind('<Control-l>', (lambda event: self.ctrl_l()))

    def do_nothing(self):
        pass

    def ctrl_p(self):
        print("ctrl+p")

    def ctrl_n(self):
        print("ctrl+n")
    
    def ctrl_o(self):
        print("ctrl+o")
    
    def ctrl_s(self):
        print("ctrl+s")
    
    def ctrl_q(self):
        if messagebox.askyesno("Quit Discord-GUI","Are you sure you want to quit?"):
            self.window.destroy()
        else: self.window.focus_force()
    
    def ctrl_f(self):
        print("ctrl+f")
    
    def ctrl_r(self):
        print("ctrl+r")
    
    def ctrl_t(self):
        print("ctrl+t")
    
    def ctrl_l(self):
        print("ctrl+l")
    
    def ctrl_backspace(self):
        print("ctrl+backspace")
    
    def ctrl_shift_s(self):
        print("ctrl+shift+s")
    
    def ctrl_shift_r(self):
        print("ctrl+shift+r")
    
    def ctrl_shift_w(self):
        print("ctrl+shift+w")

    def ctrl_shift_p(self):
        print("ctrl+shift+p")

if __name__ == "__main__":
    MainWindow()