
from pyforms.gui.appmanager import start_app
from pyforms.gui.basewidget import BaseWidget
from pyforms.gui.controls.ControlButton import ControlButton
from pyforms.gui.controls.ControlDir import ControlDir
from pyforms.gui.controls.ControlFile import ControlFile
from pyforms.gui.controls.ControlText import ControlText
from pyforms.gui.controls.ControlTextArea import ControlTextArea

class PyGitLatex(BaseWidget):

    def __init__(self):
        super(PyGitLatex,self).__init__('PyGitLatex')

        # define controls
        
        self.filProjectDir = ControlDir('Project Directory')
        
        self.btnGitStatus = ControlButton('Status')
        self.btnGitAdd = ControlButton('Add')
        self.btnGitCommit = ControlButton('Commit')
        self.btnGitLog = ControlButton('Log')
        self.btnGitPull = ControlButton('Pull')
        self.btnGitPush = ControlButton('Push')
        self.txaGitConsole = ControlTextArea('Git Output')
        self.txtGitCommand = ControlText('Git Command')
        self.btnGitRun = ControlButton('Run Command')
        self.btnGitClear = ControlButton('Clear Ouput')
        
        self.filTexFile = ControlFile('Latex File')
        self.btnTexCompile = ControlButton('Compile')
        self.btnTexView = ControlButton('View')
        self.btnTexEdit = ControlButton('Edit')
        self.btnTexBlame = ControlButton('Blame')
        self.btnTexSrcDiff = ControlButton('Source Diff')
        self.btnTexPdfDiff = ControlButton('PDF Diff')
        self.txaTexConsole = ControlTextArea('Latex Output')
        self.txtTexCommand = ControlText('Latex Command')
        self.btnTexRun = ControlButton('Run Command')
        self.btnTexClear = ControlButton('Clear Ouput')
        
        # set up the layout of the GUI
        
        self.set_margin(10)
        self.formset = [ \
            'filProjectDir', \
            {'a:Git':
                [('btnGitStatus','btnGitAdd','btnGitCommit'), \
                 ('btnGitLog','btnGitPull','btnGitPush'), \
                 'txaGitConsole', \
                 'txtGitCommand', \
                 (' ','btnGitClear','btnGitRun')], \
             'b:Latex':
                ['filTexFile', \
                 ('btnTexCompile','btnTexView','btnTexEdit'), \
                 ('btnTexBlame','btnTexSrcDiff','btnTexPdfDiff'),\
                 'txaTexConsole', \
                 'txtTexCommand', \
                 (' ','btnTexClear','btnTexRun')] \
            } \
        ]
        self.mainmenu = [ \
            {'File': [{'Initialize Project':self.init_project}, \
                      {'Clone Project':self.clone_project}, \
                      '-', \
                      {'Exit':self.exit_app}] \
            } \
        ]
            
    def init_project(self):
        pass
    
    def clone_project(self):
        pass
    
    def exit_app(self):
        exit()


#Execute the application
if __name__ == "__main__":
    start_app(PyGitLatex, geometry=(100,100,620,520) )