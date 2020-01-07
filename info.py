# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'info.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_info(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Settings")
        Dialog.resize(400, 300)
        self.okay_button = QtWidgets.QPushButton(Dialog)
        self.okay_button.setGeometry(QtCore.QRect(160, 240, 93, 28))
        self.okay_button.setObjectName("okay_button")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(120, 80, 391, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.okay_button.clicked.connect(Dialog.close)



    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "About"))
        self.okay_button.setText(_translate("Dialog", "Okay"))
        self.label.setText(_translate("Dialog", "Author  ©  Nishan Paudel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_info()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
