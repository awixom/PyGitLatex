
from pyforms.gui.appmanager import start_app
from pyforms.gui.basewidget import BaseWidget
from pyforms.gui.controls.ControlButton import ControlButton
from pyforms.gui.controls.ControlDir import ControlDir
from pyforms.gui.controls.ControlFile import ControlFile
from pyforms.gui.controls.ControlList import ControlList
from pyforms.gui.controls.ControlText import ControlText
from pyforms.gui.controls.ControlTextArea import ControlTextArea

from git import Repo, InvalidGitRepositoryError
from AnyQt import QtCore

class WarnWindow(BaseWidget):
    
    def __init__(self, msg, title=''):
        super(WarnWindow, self).__init__(title)
        self.btnOk = ControlButton('Ok')
        self.btnOk.value = self.close
        self.set_margin(10)
        self.formset = [msg,(' ','btnOk',' ')]

class YesNoDialog(BaseWidget):
    
    def __init__(self, msg, yes_action=None, no_action=None, title=''):
        super(YesNoDialog,self).__init__(title)
        self.yes_action = yes_action
        self.no_action = no_action
        self.btnYes = ControlButton('Yes')
        self.btnYes.value = self.yes_clicked
        self.btnNo = ControlButton('No')
        self.btnNo.value = self.no_clicked
        self.set_margin(10)
        self.formset = [msg,(' ','btnYes','btnNo',' ')]

    def yes_clicked(self):
        if self.yes_action:
            self.yes_action()
        self.close()
        
    def no_clicked(self):
        if self.no_action:
            self.no_action()
        self.close()
        
class GitAddFiles(BaseWidget):
    
    def __init__(self, repo):
        super(GitAddFiles,self).__init__('Git: Add Files')
        self.repo = repo
        self.lstFileList = ControlList('Select files to add:')
        for file in self.repo.untracked_files:
            self.lstFileList += [file]
        self.btnAddFiles = ControlButton('Add Files')
        self.btnAddFiles.value = self.add_files
        self.btnAddAllFiles = ControlButton('Add All Files')
        self.btnAddAllFiles.value = self.add_all_files
        self.btnCancel = ControlButton('Cancel')
        self.btnCancel.value = self.close
        self.set_margin(10)
        self.formset = ['lstFileList', \
                        ('btnAddAllFiles','btnAddFiles'), \
                        'btnCancel']
        
    def add_files(self):
        files_to_add = [self.repo.untracked_files[x] \
                        for x in self.lstFileList.selected_rows_indexes]
        for file in files_to_add:
            self.repo.git.add(file)
        self.close()
        
    def add_all_files(self):
        for file in self.repo.untracked_files:
            self.repo.git.add(file)
        self.close()

class GitCommit(BaseWidget):
    
    def __init__(self, repo):
        super(GitCommit,self).__init__('Git: Commit message')
        self.repo = repo
        self.txaCommitMsg = ControlTextArea('Input a commit message')
        self.btnCommit = ControlButton('Commit')
        self.btnCommit.value = self.git_commit
        self.btnCancel = ControlButton('Cancel')
        self.btnCancel.value = self.close
        self.set_margin(10)
        self.formset = ['txaCommitMsg',('btnCommit','btnCancel')]
        
    def git_commit(self):
        print('test'+self.txaCommitMsg.value+'test')
        if not self.txaCommitMsg.value:
            print('in not')
            ntwin = WarnWindow('Error: Cannot have an empty commit '\
                               + 'message. Please try again.')
            ntwin.show()
        else:
            self.repo.git.commit('-m',self.txaCommitMsg.value)
            self.close()
        
class PyGitLatex(BaseWidget):

    def __init__(self):
        super(PyGitLatex,self).__init__('PyGitLatex')
        
        # basic data attributes
        
        self.repo = None
        self.rgit = None

        # define controls
        
        self.dirProjectDir = ControlDir('Project Directory')
        self.dirProjectDir.click = self.set_project_dir
        
        self.btnGitStatus = ControlButton('Status')
        self.btnGitStatus.value = self.print_git_status
        self.btnGitAdd = ControlButton('Add')
        self.btnGitAdd.value = self.git_add
        self.btnGitCommit = ControlButton('Commit')
        self.btnGitCommit.value = self.git_commit
        self.btnGitLog = ControlButton('Log')
        self.btnGitPull = ControlButton('Pull')
        self.btnGitPush = ControlButton('Push')
        self.txaGitConsole = ControlTextArea('Git Output')
        self.txtGitCommand = ControlText('Git Command')
        self.txtGitCommand.key_pressed_event = self.check_git_command_event
        self.btnGitRun = ControlButton('Run Command')
        self.btnGitRun.value = self.parse_git_command
        self.btnGitClear = ControlButton('Clear Ouput')
        self.btnGitClear.value = self.clear_git_console
        
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
            'dirProjectDir', \
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


    def set_project_dir(self):
        ControlDir.click(self.dirProjectDir)
        try:
            self.repo = Repo(self.dirProjectDir.value)
            self.rgit = self.repo.git
        except (InvalidGitRepositoryError):
            msg = 'No git repository was detected in this directory, ' \
                + 'would you like to initialize one here?'
            title = 'Warning: No git repository detected'
            ynwin = YesNoDialog(msg, self.init_project, \
                                self.no_git_repo_detected, title)
            ynwin.show()
    
    def init_project(self):
        self.repo = Repo.init(self.dirProjectDir.value)
        self.rgit = self.repo.git
    
    def no_git_repo_detected(self):
        self.dirProjectDir.value = ''
        self.update_git_console(output='Please select a directory with an ' \
            + 'existing project git repository or initialize a new one.' \
            + 'In order to clone an existing project, please use the ' \
            + '"File->Clone Project" command.')
        
    def clone_project(self):
        pass
    
    def update_git_console(self, command=None, output=None):
        if command is not None:
            self.txaGitConsole += '>> ' + command
        if output is not None:
            self.txaGitConsole += output + '\n'
    
    def clear_git_console(self):
        self.txaGitConsole.value = ''
        
    def print_git_status(self):
        if self.rgit is None:
            self.update_git_console(output='Please open a project.')
        else:
            self.update_git_console(command='git status', \
                                    output=self.rgit.status())
    
    def check_git_command_event(self, event):
        if event.key() == QtCore.Qt.Key_Return \
        or event.key() == QtCore.Qt.Key_Enter:
            self.parse_git_command()
        
    def parse_git_command(self):
        if self.rgit is None:
            self.update_git_console(output='Please open a project.')
            return
        command = self.txtGitCommand.value
        parts = command.split()
        if parts[0] != 'git':
            self.update_git_console(command, \
                        'Error: Git command must start with "git".')
        else:
            try:
                out = getattr(self.rgit, parts[1])(*parts[2:])
                self.update_git_console(command, out)
            except:
                self.update_git_console(command, \
                                        "Error: Problem with git command.")
        self.txtGitCommand.value = ''
    
    def git_add(self):
        if self.repo is None:
            self.update_git_console(output='Please open a project.')
            return
        if not self.repo.untracked_files:
            self.update_git_console(command='git add', \
                                    output='No files to add.')
            return
        gawin = GitAddFiles(self.repo)
        gawin.show()
        
    def git_commit(self):
        if self.repo is None:
            self.update_git_console(output='Please open a project.')
            return
        if not self.repo.is_dirty():
            self.update_git_console(command='git commit', 
                                    output='No files to commit. '\
                                           '(Try add first.)')
            return
        gcwin = GitCommit(self.repo)
        gcwin.show()
        
    def exit_app(self):
        self.close()
        exit()
        
        
        
        

#Execute the application
if __name__ == "__main__":
    start_app(PyGitLatex, geometry=(100,100,620,520) )