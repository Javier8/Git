# -*- coding: utf-8 *-*
import subprocess
import os

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


class Pregunta(QDialog):

    def __init__(self,texto):
        QDialog.__init__(self)

        self.setWindowTitle('No existe git')

        self.label = QLabel("No existe soporte git para el proyecto:\n{0}\nDesea habilitarlo?".format(texto))

        self.img = QLabel('',self)
        self.img.setPixmap(QPixmap('/home/luis/.ninja_ide/addins/plugins/git/IMG/logo.png'))

        self.cancelar = QPushButton('Cancelar', self)
        self.aceptar = QPushButton('Aceptar', self)

        layout = QVBoxLayout(self)

        layout.addWidget(self.img)
        layout.addWidget(self.label)

        h = QHBoxLayout(self)
        h.addWidget(self.cancelar)
        h.addWidget(self.aceptar)

        layout.addLayout(h)

        self.setLayout(layout)
        self.connect(self.cancelar,SIGNAL('clicked()'), self.reject)
        self.connect(self.aceptar, SIGNAL('clicked()'),self.accept)


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

        self.explorer.projectOpened.connect(self.check_project)


        self.proyectos = []

        self.tree = self.explorer.get_tree_projects()
        self.tree.setColumnCount(2)

    def finish(self):

        print 'plugin is being killed =('

    def get_preferences_widget(self):

        pass

    def check_project(self,path):

        x=0
        while self.tree.topLevelItem(x):

            item = self.tree.topLevelItem(x)
            if path == item.path and self.look_git(path) == True:
                item.setIcon(1,QIcon('/home/luis/.ninja_ide/addins/plugins/git/IMG/g.png'))

            x+=1


    def look_git(self,path):

        run_dir = os.getcwd()
        os.chdir(path)
        check = subprocess.call(['git','status'])
        os.chdir(run_dir)

        if check == 0:
            return True
        else:
            return False


    def check_git(self):

        path = self.editor.get_project_owner()
        check = self.look_git(path)

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


        run_dir = os.getcwd()
        path = self.editor.get_project_owner()
        os.chdir(path)
        check = subprocess.check_output(['git','init'])
        os.chdir(run_dir)

        msgBox = QMessageBox()
        msgBox.setText("Soporte git añadido a proyecto")
        msgBox.setInformativeText(check)
        msgBox.exec_()

    def status(self):

        run_dir = os.getcwd()
        path = self.editor.get_project_owner()
        os.chdir(path)
        check = subprocess.check_output(['git','status'])
        os.chdir(run_dir)

        msgBox = QMessageBox()
        msgBox.setText("Status")
        msgBox.setInformativeText(check)
        msgBox.exec_()




