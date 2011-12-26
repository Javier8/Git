# -*- coding: utf-8 *-*
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Tree(QTreeWidget):

    def __init__(self):
        QTreeWidget.__init__(self)


        self.setColumnCount(1)
        items = []

        for i in range(10):

            items.append(QTreeWidgetItem( QStringList(QString("item: %1").arg(i))))
        self.insertTopLevelItems(0,items)



        print self.topLevelItem(0)

app = QApplication(sys.argv)
icon = Tree()
icon.show()
app.exec_()
