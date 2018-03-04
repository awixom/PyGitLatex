#! python3

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
from AnyQt.QtWidgets import QFileDialog
import os

os.environ['GIT_ASKPASS'] = \
    'D:\Andy\Documents\PyGitLatex\pygitlatex_gitaskpass.py'

class MessageWindow(BaseWidget):
    
    def __init__(self, msg, title='PyGitLatex Message'):
        super(MessageWindow, self).__init__(title)
        self.btnOk = ControlButton('Okay')
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
        self.lstModFiles = ControlList('Modified Files:')
        self.lstModFiles.readonly = True
        for item in self.repo.index.diff(None):
            self.lstModFiles += [item.a_path]
        self.lstNewFiles = ControlList('Untracked Files:')
        self.lstNewFiles.readonly = True
        for file in self.repo.untracked_files:
            self.lstNewFiles += [file]
        self.btnAddFiles = ControlButton('Add Files')
        self.btnAddFiles.value = self.add_files
        self.btnAddAllFiles = ControlButton('Add All Files')
        self.btnAddAllFiles.value = self.add_all_files
        self.btnCancel = ControlButton('Cancel')
        self.btnCancel.value = self.close
        self.set_margin(10)
        self.formset = ['info:Select files to add to the project.', \
                        'lstModFiles', \
                        'lstNewFiles', \
                        ('btnAddAllFiles','btnAddFiles'), \
                        'btnCancel']
        
    def add_files(self):
        files_to_add = [self.lstModFiles.value[x] \
                        for x in self.lstModFiles.selected_rows_indexes]
        files_to_add += [self.lstNewFiles.value[x] \
                         for x in self.lstNewFiles.selected_rows_indexes]
        for file in files_to_add:
            self.repo.git.add(file)
        self.close()
        
    def add_all_files(self):
        for file in self.repo.untracked_files:
            self.repo.git.add(file)
        for item in self.repo.index.diff(None):
            self.repo.git.add(item.a_path)
        self.close()

class GitCommit(BaseWidget):
    
    def __init__(self, repo):
        super(GitCommit,self).__init__('Git: Commit message')
        self.repo = repo
        self.txtCommitMsg = ControlText()
        self.btnCommit = ControlButton('Commit')
        self.btnCommit.value = self.git_commit
        self.btnCancel = ControlButton('Cancel')
        self.btnCancel.value = self.close
        self.set_margin(10)
        self.formset = ['info:Input a commit message', \
                        'txtCommitMsg',('btnCommit','btnCancel')]
        
    def git_commit(self):
        if not self.txtCommitMsg.value:
            ntwin = MessageWindow('Error: Cannot have an empty commit '\
                                  + 'message. Please try again.')
            ntwin.show()
        else:
            self.repo.git.commit('-m',self.txtCommitMsg.value)
            self.close()
        
class PyGitLatex(BaseWidget):

    def __init__(self):
        super(PyGitLatex,self).__init__('PyGitLatex')
        
        # basic data attributes
        
        self.repo = None
        self.rgit = None
        self.remote_name = 'origin'
        self.branch_name = 'master'
        self.local_proj_name = None

        # define controls
        
        self.dirProjectDir = ControlDir('Project Directory')
        self.dirProjectDir.click = self.set_project_dir
        
        self.btnGitStatus = ControlButton('Status')
        self.btnGitStatus.value = self.git_status
        self.btnGitAdd = ControlButton('Add')
        self.btnGitAdd.value = self.git_add
        self.btnGitCommit = ControlButton('Commit')
        self.btnGitCommit.value = self.git_commit
        self.btnGitLog = ControlButton('Log')
        self.btnGitLog.value = self.git_log
        self.btnGitPull = ControlButton('Pull')
        self.btnGitPull.value = self.git_pull
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
            self.local_proj_name = self.dirProjectDir.value.split(os.sep)[-1]
        except (InvalidGitRepositoryError):
            msg = 'No git repository was detected in this directory, ' \
                + 'would you like to initialize one here?'
            title = 'Warning: No git repository detected'
            ynwin = YesNoDialog(msg, \
                        lambda : self.init_project(self.dirProjectDir.value), \
                        self.no_git_repo_detected, title)
            ynwin.show()
    
    def init_project(self, directory=None):
        if not directory:
            directory = str(QFileDialog.getExistingDirectory())
            self.dirProjectDir.value = directory
        self.repo = Repo.init(directory)
        self.rgit = self.repo.git
        self.local_proj_name = directory.split(os.sep)[-1]
    
    def no_git_repo_detected(self):
        self.dirProjectDir.value = ''
        self.update_git_console(output='Please select a directory with an ' \
            + 'existing project git repository or initialize a new one.' \
            + 'In order to clone an existing project, please use the ' \
            + '"File->Clone Project" command.')
    
    def check_repo(self, level=3):
        
        check = True
        
        # level one check: do we have a project open, if not ask the user to
        # open one
        
        if level >= 1 and check:
            if self.repo:
                check = True
            else:
                check = False
                self.update_git_console(output='Please open a project.')
        
        # level two check: is there a correctly named remote in the repo? 
        # If not, ask if they want to create one
        
        if level >= 2 and check:
            try: 
                self.repo.remotes[self.remote_name]
                check = True
            except (IndexError):
                check = False
                ynwin = YesNoDialog(['No project remote was detected.', \
                    'Currently looking for a remote called: '\
                        + self.remote_name, \
                    'Would you like to create a new remote repository?', \
                    'Select no if you want to try and fix the problem ' \
                        + ' a different way.'], \
                    yes_action=self.create_project_remote_rpo, \
                    title='No Remote Detected')
                ynwin.show()
                
        # level three check: can we actually use the remote? try to fetch it,
        # if it doesn't work, notify and see if they want us to try and 
        # auto-fix the remote url
        
        
        
        return check
    
    def clone_project(self):
        pass
    
    def create_project_remote_repo(self):
        out = QFileDialog.getSaveFileName(self, \
                                          'Choose a bare git repository', \
                                          self.local_proj_name+'.git', \
                                          'Bare git repo (*.git)')
        remote_loc = self.rgit.polish_url(out[0])
        self.repo.clone(remote_loc, bare=True)
        self.rgit.remote('add', self.remote_name, remote_loc)
    
    def update_git_console(self, command=None, output=None):
        if command is not None:
            self.txaGitConsole += '>> ' + command
        if output is not None:
            self.txaGitConsole += output + '\n'
    
    def clear_git_console(self):
        self.txaGitConsole.value = ''
        
    def check_git_command_event(self, event):
        if event.key() == QtCore.Qt.Key_Return \
        or event.key() == QtCore.Qt.Key_Enter:
            self.parse_git_command()
        
    def parse_git_command(self):
        if not self.check_repo(1):
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
        if not self.check_repo(1):
            return
        if not self.repo.untracked_files and not self.repo.is_dirty():
            self.update_git_console(command='git add', \
                                    output='No files to add.')
            return
        gawin = GitAddFiles(self.repo)
        gawin.show()
        
    def git_commit(self):
        if not self.check_repo(1):
            return
        if not self.repo.is_dirty():
            self.update_git_console(command='git commit', 
                                    output='No files to commit. '\
                                           '(Try add first.)')
            return
        gcwin = GitCommit(self.repo)
        gcwin.show()
        
    def git_log(self):
        if self.check_repo(1):
            self.update_git_console('git log', self.rgit.log())
        
    def git_pull(self):
        if self.check_repo(2):
            out = self.rgit.pull(self.remote_name, self.branch_name)
            self.update_git_console('git pull', out)
        
    def git_status(self):
        if self.check_repo(1):
            self.update_git_console(command='git status', \
                                    output=self.rgit.status())
            
    def exit_app(self):
        self.close()
        exit()

# run the app if this is executed as a script
        
if __name__ == "__main__":
    start_app(PyGitLatex, geometry=(100,100,620,520) )