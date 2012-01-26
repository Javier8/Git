# -*- coding: utf-8 *-*
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *



class W(QWidget):

    def __init__(self):
        super(W, self).__init__()


        self.list = QListWidget(self)

        self.item = QListWidgetItem()

        self.widget = QCheckBox("Uno")

        item2 = QListWidgetItem()

        widget2 = QCheckBox("Dos")

        self.list.addItem(self.item)
        self.list.addItem(item2)

        self.list.setItemWidget(self.item,self.widget)
        self.list.setItemWidget(item2,widget2)

        button = QPushButton("Borra", self)
        button.move(50,50)

        self.connect(button,SIGNAL("clicked()"), self.borra)


    def borra(self):

        self.list.removeItemWidget(self.item)
        self.list.takeItem(0)


class WG(QWidget):

    def __init__(self):
        super(WG, self).__init__()

        g = QGridLayout(self)

        g.addWidget(QLabel("centro"),0,0,0,2,Qt.AlignTop)
        g.addWidget(QLabel("izquierda"),1,0)
        g.addWidget(QLabel("izquierda2"),2,0)
        g.addWidget(QLabel("derecha"),1,1)
        g.addWidget(QLabel("derecha2"),2,1)


        w = QMessageBox()
        w.setText("No es posible cambiar")
        w.setIcon(w.Warning)

        w.exec_()#hol

app = QApplication(sys.argv)
icon = WG()
icon.show()
app.exec_()
