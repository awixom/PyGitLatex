#! C:\Users\awixo\Anaconda3\python

from pyforms.gui.appmanager import start_app
from pyforms.gui.basewidget import BaseWidget
from pyforms.gui.controls.ControlButton import ControlButton
from pyforms.gui.controls.ControlText import ControlText

import sys
from AnyQt.QtWidgets import QLineEdit
from AnyQt import QtCore

class GitAskPass(BaseWidget):
    
    def __init__(self):
        super(GitAskPass,self).__init__('Git: Authentication')
        #self.repo = repo
        self.txtInput = ControlText()
        self.txtInput.form.lineEdit.setEchoMode(QLineEdit.Password)
        self.txtInput.key_pressed_event = self.check_for_enter
        self.btnSubmit = ControlButton('Submit')
        self.btnSubmit.value = self.submit
        self.btnCancel = ControlButton('Cancel')
        self.btnCancel.value = self.cancel
        self.set_margin(10)
        self.formset = ['info:'+sys.argv[1], 'txtInput', \
                        ('btnSubmit','btnCancel')]
        
    def check_for_enter(self, event):
        if event.key() == QtCore.Qt.Key_Return \
        or event.key() == QtCore.Qt.Key_Enter:
            self.submit()
        
    def submit(self):
        print(self.txtInput.value)
        self.close()
        exit()
        
    def cancel(self):
        self.close()
        exit()
            
# run the app if this is executed as a script
        
if __name__ == "__main__":
    start_app(GitAskPass, geometry=(100,100,1,1))