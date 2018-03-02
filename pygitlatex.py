
from pyforms.gui.appmanager import start_app
from pyforms.gui.basewidget import BaseWidget
from pyforms.gui.controls.ControlButton import ControlButton
from pyforms.gui.controls.ControlDir import ControlDir
from pyforms.gui.controls.ControlFile import ControlFile
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
        
        self.filLatexFile = ControlFile('Latex File')
        self.btnLatexCompile = ControlButton('Compile')
        self.btnLatexView = ControlButton('View')
        self.btnLatexEdit = ControlButton('Edit')
        self.txaLatexConsole = ControlTextArea('Latex Output')
        
        # set up look of the GUI
        
        self.set_margin(10)
        self.formset = ['filProjectDir', \
            {'a:Git':[('btnGitStatus','btnGitAdd','btnGitCommit'), \
                      ('btnGitLog','btnGitPull','btnGitPush'), \
                      'txaGitConsole'], \
             'b:Latex':['filLatexFile', \
                        ('btnLatexCompile','btnLatexView','btnLatexEdit'), \
                        'txaLatexConsole'] \
            }]

#Execute the application
if __name__ == "__main__":
    start_app(PyGitLatex, geometry=(200,200,620,420) )