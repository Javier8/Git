# -*- coding: utf-8 *-*
import subprocess
import os
import re
import time

from GitCalls import git

from ninja_ide.core import file_manager
from ninja_ide.core import plugin

from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT

from PyQt4.QtGui import QAction
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextFormat
from PyQt4.QtGui import QColor


class GitStatus(QDialog):

    def __init__(self,plugin,git):
        QDialog.__init__(self)

        self.git = git
        self.plugin = plugin
        self.setWindowTitle('Git status')

        layout = QGridLayout(self)

        no_staged = QLabel("<h1>No staged</h1>")

        untracked_files = QLabel("Untracked files")
        self.untracked_files = QListWidget()

        modified_files = QLabel("Modified files")
        self.modified_files = QListWidget()

        deleted_files = QLabel("Deleted files")
        self.deleted_files = QListWidget()


        staged = QLabel("<h1>Staged</h1>")

        added_files = QLabel("Added files")
        self.added_files = QListWidget()

        s_modified_files = QLabel("Modified files")
        self.s_modified_files = QListWidget()

        s_deleted_files = QLabel("Deleted files")
        self.s_deleted_files = QListWidget()

        layout.addWidget(no_staged,0,0)
        layout.addWidget(untracked_files,1,0)
        layout.addWidget(self.untracked_files,2,0)
        layout.addWidget(modified_files,3,0)
        layout.addWidget(self.modified_files,4,0)
        layout.addWidget(deleted_files,5,0)
        layout.addWidget(self.deleted_files,6,0)

        layout.addWidget(staged,0,1)
        layout.addWidget(added_files,1,1)
        layout.addWidget(self.added_files,2,1)
        layout.addWidget(s_modified_files,3,1)
        layout.addWidget(self.s_modified_files,4,1)
        layout.addWidget(s_deleted_files,5,1)
        layout.addWidget(self.s_deleted_files,6,1)


        self.fill(self.git.no_staged["?"],self.untracked_files)
        self.fill(self.git.no_staged["M"],self.modified_files)
        self.fill(self.git.no_staged["D"],self.deleted_files)

        self.fill(self.git.staged["A"],self.added_files)
        self.fill(self.git.staged["M"],self.s_modified_files)
        self.fill(self.git.staged["D"],self.s_deleted_files)

        self.staged_b = QPushButton('Stage files', self)
        self.unstage_b = QPushButton("Unstage files", self)
        self.commit_b = QPushButton('Commit files', self)
        self.uncommit_b = QPushButton("Uncommit files", self)

        layout.addWidget(self.staged_b,7,0)
        layout.addWidget(self.unstage_b,8,0)
        layout.addWidget(self.commit_b,7,1)
        layout.addWidget(self.uncommit_b,8,1)

        self.setLayout(layout)

        self.connect(self.staged_b,SIGNAL('clicked()'), self.add)
        self.connect(self.unstage_b,SIGNAL('clicked()'), self.unstage)
        self.connect(self.commit_b, SIGNAL('clicked()'),self.commit)
        self.connect(self.uncommit_b,SIGNAL('clicked()'), self.uncommit)

    def fill(self,list,widget_list):

        for x in list:

            item = QListWidgetItem()
            widget_list.addItem(item)
            check_box  = QCheckBox(x)
            widget_list.setItemWidget(item,check_box)

    def add(self):

        path = self.plugin.editor.get_project_owner()
        for pos in range(self.untracked_files.count()):

            item = self.untracked_files.item(pos)
            widget = self.untracked_files.itemWidget(item)

            if widget.isChecked():
                self.git.add(path,widget.text())

        for pos in range(self.modified_files.count()):

            item = self.modified_files.item(pos)
            widget = self.modified_files.itemWidget(item)

            if widget.isChecked():
                self.git.add(path,widget.text())

        for pos in range(self.deleted_files.count()):

            item = self.deleted_files.item(pos)
            widget = self.deleted_files.itemWidget(item)

            if widget.isChecked():
                self.git.add(path,widget.text())

    def unstage(self):



        path = self.plugin.editor.get_project_owner()
        for pos in range(self.untracked_files.count()):

            item = self.untracked_files.item(pos)
            widget = self.untracked_files.itemWidget(item)

            if widget.isChecked():
                self.git.unstage(path,widget.text())

        for pos in range(self.modified_files.count()):

            item = self.modified_files.item(pos)
            widget = self.modified_files.itemWidget(item)

            if widget.isChecked():
                self.git.unstage(path,widget.text())

        for pos in range(self.deleted_files.count()):

            item = self.deleted_files.item(pos)
            widget = self.deleted_files.itemWidget(item)

            if widget.isChecked():
                self.git.unstage(path,widget.text())

    def commit(self):

        msg = QInputDialog.getText(self,"Commit message","Commit Message:")

        if msg[1] == False:
            return(0)

        path = self.plugin.editor.get_project_owner()
        for pos in range(self.added_files.count()):

            item = self.added_files.item(pos)
            widget = self.added_files.itemWidget(item)

            if widget.isChecked():
                self.git.commit(path,str(widget.text()),msg[0])

        for pos in range(self.s_modified_files.count()):

            item = self.s_modified_files.item(pos)
            widget = self.s_modified_files.itemWidget(item)

            if widget.isChecked():
                print 'si'
                self.git.commit(path,widget.text(),msg[0])

        for pos in range(self.s_deleted_files.count()):

            item = self.s_deleted_files.item(pos)
            widget = self.s_deleted_files.itemWidget(item)

            if widget.isChecked():
                self.git.commit(path,widget.text(),msg[0])


    def uncommit(self):


        path = self.plugin.editor.get_project_owner()
        for pos in range(self.added_files.count()):

            item = self.added_files.item(pos)
            widget = self.added_files.itemWidget(item)

            if widget.isChecked():
                self.git.uncommit(path,str(widget.text()))

        for pos in range(self.s_modified_files.count()):

            item = self.s_modified_files.item(pos)
            widget = self.s_modified_files.itemWidget(item)

            if widget.isChecked():
                self.git.uncommit(path,widget.text())

        for pos in range(self.s_deleted_files.count()):

            item = self.s_deleted_files.item(pos)
            widget = self.s_deleted_files.itemWidget(item)

            if widget.isChecked():
                self.git.uncommit(path,widget.text())


class Git(plugin.Plugin):

    def initialize(self):

        self.editor = self.locator.get_service('editor')
        self.toolbar = self.locator.get_service('toolbar')
        self.menu = self.locator.get_service('menuApp')
        self.explorer = self.locator.get_service('explorer')

        git_status = QAction(QIcon('/home/luis/.ninja_ide/addins/plugins/git/IMG/logo.png'),'GIT status', self)
        git_stage = QAction(QIcon('/home/luis/.ninja_ide/addins/plugins/git/IMG/stage.png'), 'Stage Current File',self)
        git_commit = QAction(QIcon('/home/luis/.ninja_ide/addins/plugins/git/IMG/commit.png'), 'Commit Current Changes',self)
        self.toolbar.add_action(git_status)
        self.toolbar.add_action(git_stage)
        self.toolbar.add_action(git_commit)

        self.connect(git_status, SIGNAL('triggered()'), self.check_git)

        self.connect(git_stage,SIGNAL('triggered()'), lambda: self.text_call("--staged"))

        self.connect(git_commit,SIGNAL('triggered()'), self.text_call)

        self.explorer.projectOpened.connect(self.check_project)


        self.proyectos = []

        self.tree = self.explorer.get_tree_projects()

        self.git  = git.Git()

        self.text = {}

    def finish(self):

        print 'plugin is being killed =('

    def get_preferences_widget(self):

        pass

    def check_project(self,path):

        x=0
        while self.tree.topLevelItem(x):

            item = self.tree.topLevelItem(x)
            if path == item.path and self.git.check_git(path) == True:
                item.setIcon(0,QIcon('/home/luis/.ninja_ide/addins/plugins/git/IMG/g.png'))

            x+=1




    def check_git(self):

        path = self.editor.get_project_owner()
        check = self.git.check_git(path)

        if check == True:
            self.status()

        else:

            project_name = self.editor.get_project_owner()
            msgBox = QMessageBox()
            msgBox.setText("Soporte Git no habilitado")
            msgBox.setInformativeText("Desea habilitarlo?")
            msgBox.setStandardButtons(QMessageBox.Ok |  QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Cancel)
            if msgBox.exec_() == QMessageBox.Ok:
                self.init()

    def init(self):

        path = self.editor.get_project_owner()
        check = self.git.init(path)


        msgBox = QMessageBox()
        msgBox.setText("Soporte git añadido a proyecto")
        msgBox.setInformativeText(check)
        msgBox.exec_()

    def status(self):

        self.git= git.Git()
        path = self.editor.get_project_owner()
        self.git.status(path)

        info = GitStatus(self,self.git)
        info.exec_()


    def text_call(self,state=False):

        self.git = git.Git()
        path = self.editor.get_project_owner()
        file = self.editor.get_editor_path()

        if state:
            self.editor.add_editor('staged({0})'.format(os.path.basename(file)))

        else:
            self.editor.add_editor('commited({0})'.format(os.path.basename(file)))

        editor = self.editor.get_editor()
        self.text[editor] = self.git.text(path,file,state)
        editor.insertPlainText(self.text[editor][0])


        self.connect(editor,SIGNAL("cursorPositionChanged()"), self.highlight)

        text = self.text[editor]

        for line in text[1]:
            if text[1][line] == "=":
                continue

            selection = QTextEdit.ExtraSelection()

            block = editor.document().findBlockByLineNumber(line)
            selection.cursor = editor.textCursor()
            selection.cursor.setPosition(block.position())
            if text[1][line] == "-":
                lineColor = QColor(255,0,0,50)
            if text[1][line] == "+":
                lineColor = QColor(0,0,255,50)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection,True)

            selection.cursor.movePosition(QTextCursor.EndOfBlock)
            editor.extraSelections.append(selection)

        editor.setExtraSelections(editor.extraSelections)
        editor.setReadOnly(True)
        editor.textModified = False


    def highlight(self):

        editor = self.editor.get_editor()
        text = self.text[editor]
        for line in text[1]:
            if text[1][line] == "=" :
                continue

            selection = QTextEdit.ExtraSelection()

            block = editor.document().findBlockByLineNumber(line)
            selection.cursor = editor.textCursor()
            selection.cursor.setPosition(block.position())
            if text[1][line] == "-":
                lineColor = QColor(255,0,0,50)
            if text[1][line] == "+":
                lineColor = QColor(0,0,255,50)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection,True)

            selection.cursor.movePosition(QTextCursor.EndOfBlock)
            editor.extraSelections.append(selection)

        editor.setExtraSelections(editor.extraSelections)
        editor.setReadOnly(True)
        editor.Document().setModified(False)
