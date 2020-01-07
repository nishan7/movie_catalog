# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Setting(object):
    path=''
    def setupUi(self, Setting, path):
        Setting.setObjectName("Setting")
        Setting.setWindowModality(QtCore.Qt.ApplicationModal)
        Setting.resize(685, 218)
        Setting.setMaximumSize(QtCore.QSize(16777215, 16777206))
        Setting.setSizeGripEnabled(False)
        Setting.setModal(False)
        self.layoutWidget = QtWidgets.QWidget(Setting)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 20, 591, 141))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText(path)
        self.horizontalLayout.addWidget(self.lineEdit)
        self.search_button = QtWidgets.QPushButton(self.layoutWidget)
        self.search_button.setMaximumSize(QtCore.QSize(104, 27))
        self.search_button.setObjectName("search_button")
        self.horizontalLayout.addWidget(self.search_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Setting)
        QtCore.QMetaObject.connectSlotsByName(Setting)

    def retranslateUi(self, Setting):
        _translate = QtCore.QCoreApplication.translate
        Setting.setWindowTitle(_translate("Setting", "Setting"))
        self.label.setText(_translate("Setting", "Select the main folder for your movies..."))
        self.search_button.setText(_translate("Setting", "Search"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Setting = QtWidgets.QDialog()
    ui = Ui_Setting()
    ui.setupUi(Setting)
    Setting.show()
    sys.exit(app.exec_())
