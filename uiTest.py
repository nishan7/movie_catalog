# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#

## TODO add info dialog add to ui
## TODO add setting dialog and add to ui
## TODO try having intitalization screen
## TODO context menu and link to google search
## TODO other sorts and  searching
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QDialog, QAction, QSplashScreen

import database


class FlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=-1, hspacing=-1, vspacing=-1):
        super(FlowLayout, self).__init__(parent)
        self._hspacing = hspacing
        self._vspacing = vspacing
        self._items = []
        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self):
        del self._items[:]

    def addItem(self, item):
        self._items.append(item)

    def horizontalSpacing(self):
        if self._hspacing >= 0:
            return self._hspacing
        else:
            return self.smartSpacing(
                QtWidgets.QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self._vspacing >= 0:
            return self._vspacing
        else:
            return self.smartSpacing(
                QtWidgets.QStyle.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)

    def expandingDirections(self):
        return QtCore.Qt.Orientations(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QtCore.QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QtCore.QSize(left + right, top + bottom)
        return size

    def doLayout(self, rect, testonly):
        left, top, right, bottom = self.getContentsMargins()
        effective = rect.adjusted(+left, +top, -right, -bottom)
        x = effective.x()
        y = effective.y()
        lineheight = 0
        for item in self._items:
            widget = item.widget()
            hspace = self.horizontalSpacing()
            if hspace == -1:
                hspace = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton,
                    QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Horizontal)
            vspace = self.verticalSpacing()
            if vspace == -1:
                vspace = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton,
                    QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Vertical)
            nextX = x + item.sizeHint().width() + hspace
            if nextX - hspace > effective.right() and lineheight > 0:
                x = effective.x()
                y = y + lineheight + vspace
                nextX = x + item.sizeHint().width() + hspace
                lineheight = 0
            if not testonly:
                item.setGeometry(
                    QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))
            x = nextX
            lineheight = max(lineheight, item.sizeHint().height())
        return y + lineheight - rect.y() + bottom

    def smartSpacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()


class MainWindow(QtWidgets.QMainWindow):
    actionAbout1: QAction
    poster_value: QLabel
    movie_list = []
    path = ''

    def __init__(self, db, parent=None):
        super().__init__()
        self.db = db
        self.initUI(self)

        # root = tkinter.Tk()
        # self.width = root.winfo_screenwidth()
        # self.height = root.winfo_screenheight()
        # print(self.width, self.height);

    def setting_window(self):
        # If you pass a parent (self) will block the Main Window,
        # and if you do not pass both will be independent,
        # I recommend you try both cases.
        widget = QDialog(self)
        from setting import Ui_Setting
        ui = Ui_Setting()
        print(self.db.path)
        ui.path = self.db.path
        ui.setupUi(widget)
        print(self.path)
        widget.exec_()

    def info_window(self):
        # If you pass a parent (self) will block the Main Window,
        # and if you do not pass both will be independent,
        # I recommend you try both cases.
        widget = QDialog(self)
        from info import Ui_info
        ui = Ui_info()

        ui.setupUi(widget)
        widget.exec_()

    def initUI(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(self.width*.9, self.height*.9)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.navbar_horizontal_layout = QtWidgets.QHBoxLayout()
        self.navbar_horizontal_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.navbar_horizontal_layout.setObjectName("navbar_horizontal_layout")
        self.search_field = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_field.sizePolicy().hasHeightForWidth())
        self.search_field.setSizePolicy(sizePolicy)
        self.search_field.setMinimumSize(QtCore.QSize(0, 10))
        self.search_field.setMaximumSize(QtCore.QSize(185, 30))
        self.search_field.setToolTip("Search for movies")
        # self.search_field.setText("Search..")
        # self.search_field.setPlaceholderText("Search..")
        self.search_field.setObjectName("search_field")
        self.navbar_horizontal_layout.addWidget(self.search_field)
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setMaximumSize(QtCore.QSize(68, 32))
        self.search_button.setObjectName("search_button")
        self.navbar_horizontal_layout.addWidget(self.search_button)
        spacerItem = QtWidgets.QSpacerItem(10, 31, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.navbar_horizontal_layout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(46, 16777215))
        self.label.setObjectName("label")
        self.navbar_horizontal_layout.addWidget(self.label)
        self.sort_combo_box = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sort_combo_box.sizePolicy().hasHeightForWidth())
        self.sort_combo_box.setSizePolicy(sizePolicy)
        self.sort_combo_box.setMinimumSize(QtCore.QSize(0, 28))
        self.sort_combo_box.setMaximumSize(QtCore.QSize(108, 33))
        self.sort_combo_box.setObjectName("sort_combo_box")
        self.sort_combo_box.addItem("")
        self.sort_combo_box.addItem("")
        self.sort_combo_box.addItem("")
        self.sort_combo_box.addItem("")
        self.navbar_horizontal_layout.addWidget(self.sort_combo_box)
        self.properties = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.properties.sizePolicy().hasHeightForWidth())
        self.properties.setSizePolicy(sizePolicy)
        self.properties.setMinimumSize(QtCore.QSize(0, 40))
        self.properties.setMaximumSize(QtCore.QSize(79, 16777215))
        self.properties.setObjectName("properties")
        self.navbar_horizontal_layout.addWidget(self.properties)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.navbar_horizontal_layout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.navbar_horizontal_layout)

        self.main_area_horizontal_layout = QtWidgets.QHBoxLayout()
        self.main_area_horizontal_layout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.main_area_horizontal_layout.setObjectName("main_area_horizontal_layout")

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Movie Area
        self.movie_area = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.movie_area.sizePolicy().hasHeightForWidth())
        self.movie_area.setSizePolicy(sizePolicy)
        self.movie_area.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.movie_area.setWidgetResizable(True)
        self.movie_area.setObjectName("movie_area")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 395, 748))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        # Adding Buttons in FlowLayout
        self.flow_layout = FlowLayout(self.scrollAreaWidgetContents, hspacing=15, vspacing=10)

        lst = list(self.db.database.keys())
        lst.sort()
        self.add_buttons(lst)

        self.movie_area.setWidget(self.scrollAreaWidgetContents)
        self.main_area_horizontal_layout.addWidget(self.movie_area)

        # Spacer between movie area and info area
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_area_horizontal_layout.addItem(spacerItem2)

        # Info Area
        self.info_area = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_area.sizePolicy().hasHeightForWidth())
        self.info_area.setSizePolicy(sizePolicy)
        self.info_area.setMinimumSize(QtCore.QSize(670, 0))
        self.info_area.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.info_area.setWidgetResizable(True)
        self.info_area.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.info_area.setObjectName("info_area")
        self.info_scroll_area = QtWidgets.QWidget()
        self.info_scroll_area.setGeometry(QtCore.QRect(0, 0, 668, 806))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_scroll_area.sizePolicy().hasHeightForWidth())
        self.info_scroll_area.setSizePolicy(sizePolicy)
        self.info_scroll_area.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.info_scroll_area.setObjectName("info_scroll_area")
        self.info_area_vertical_layout = QtWidgets.QVBoxLayout(self.info_scroll_area)
        self.info_area_vertical_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.info_area_vertical_layout.setContentsMargins(10, -1, -1, -1)
        self.info_area_vertical_layout.setSpacing(5)
        self.info_area_vertical_layout.setObjectName("info_area_vertical_layout")
        self.title_value = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_value.sizePolicy().hasHeightForWidth())
        self.title_value.setSizePolicy(sizePolicy)
        self.title_value.setMaximumSize(QtCore.QSize(16777215, 32))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.title_value.setFont(font)
        self.title_value.setMidLineWidth(0)
        self.title_value.setScaledContents(False)
        self.title_value.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.title_value.setWordWrap(True)
        self.title_value.setOpenExternalLinks(True)
        self.title_value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        self.title_value.setObjectName("title_value")
        self.info_area_vertical_layout.addWidget(self.title_value)
        self.image = QtWidgets.QVBoxLayout()
        self.image.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.image.setSpacing(0)
        self.image.setObjectName("image")
        self.backdrop_value = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backdrop_value.sizePolicy().hasHeightForWidth())
        self.backdrop_value.setSizePolicy(sizePolicy)
        self.backdrop_value.setMinimumSize(QtCore.QSize(624, 351))
        self.backdrop_value.setMaximumSize(QtCore.QSize(624, 351))
        self.backdrop_value.setPixmap(QtGui.QPixmap("(500) Days of Summer.jpg"))
        self.backdrop_value.setScaledContents(True)
        self.backdrop_value.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.backdrop_value.setObjectName("backdrop_value")
        self.image.addWidget(self.backdrop_value)
        self.poster_value = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.poster_value.sizePolicy().hasHeightForWidth())
        self.poster_value.setSizePolicy(sizePolicy)
        self.poster_value.setMinimumSize(QtCore.QSize(0, 52))
        self.poster_value.setMaximumSize(QtCore.QSize(16777215, 240))
        self.poster_value.setPixmap(QtGui.QPixmap("A Beautiful Mind.jpg"))
        self.poster_value.setScaledContents(False)
        self.poster_value.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.poster_value.setIndent(0)
        self.poster_value.setStyleSheet('''padding: 0px 0px 0px 10px;''')
        self.poster_value.setObjectName("poster_value")
        self.image.addWidget(self.poster_value)
        self.info_area_vertical_layout.addLayout(self.image)

        self.tagline = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagline.sizePolicy().hasHeightForWidth())
        self.tagline.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tagline.setFont(font)
        self.tagline.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.tagline.setWordWrap(True)
        self.tagline.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        self.tagline.setObjectName("tagline")
        self.info_area_vertical_layout.addWidget(self.tagline)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.info_area_vertical_layout.addItem(spacerItem3)
        self.year_box = QtWidgets.QHBoxLayout()
        self.year_box.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.year_box.setObjectName("year_box")
        self.year = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.year.sizePolicy().hasHeightForWidth())
        self.year.setSizePolicy(sizePolicy)
        self.year.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.year.setFont(font)
        self.year.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.year.setObjectName("year")
        self.year_box.addWidget(self.year)
        self.year_value = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.year_value.sizePolicy().hasHeightForWidth())
        self.year_value.setSizePolicy(sizePolicy)
        self.year_value.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.year_value.setFont(font)
        self.year_value.setFrameShadow(QtWidgets.QFrame.Raised)
        self.year_value.setTextFormat(QtCore.Qt.PlainText)
        self.year_value.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.year_value.setOpenExternalLinks(True)
        self.year_value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        self.year_value.setObjectName("year_value")
        self.year_box.addWidget(self.year_value)
        self.info_area_vertical_layout.addLayout(self.year_box)
        self.rating_box = QtWidgets.QHBoxLayout()
        self.rating_box.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.rating_box.setObjectName("rating_box")
        self.rating = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rating.sizePolicy().hasHeightForWidth())
        self.rating.setSizePolicy(sizePolicy)
        self.rating.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.rating.setFont(font)
        self.rating.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.rating.setObjectName("rating")
        self.rating_box.addWidget(self.rating)
        self.rating_value = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rating_value.sizePolicy().hasHeightForWidth())
        self.rating_value.setSizePolicy(sizePolicy)
        self.rating_value.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.rating_value.setFont(font)
        self.rating_value.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.rating_value.setOpenExternalLinks(True)
        self.rating_value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        self.rating_value.setObjectName("rating_value")
        self.rating_box.addWidget(self.rating_value)
        self.info_area_vertical_layout.addLayout(self.rating_box)
        self.director_box = QtWidgets.QHBoxLayout()
        self.director_box.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.director_box.setObjectName("director_box")
        self.director = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.director.sizePolicy().hasHeightForWidth())
        self.director.setSizePolicy(sizePolicy)
        self.director.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.director.setFont(font)
        self.director.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.director.setObjectName("director")
        self.director.setWordWrap(True)
        self.director_box.addWidget(self.director)
        self.director_value = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.director_value.sizePolicy().hasHeightForWidth())
        self.director_value.setSizePolicy(sizePolicy)
        self.director_value.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.director_value.setFont(font)
        self.director_value.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.director_value.setOpenExternalLinks(True)
        self.director_value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        self.director_value.setObjectName("director_value")
        self.director_box.addWidget(self.director_value)
        self.info_area_vertical_layout.addLayout(self.director_box)
        self.runtime_box = QtWidgets.QHBoxLayout()
        self.runtime_box.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.runtime_box.setObjectName("runtime_box")
        self.runtime = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runtime.sizePolicy().hasHeightForWidth())
        self.runtime.setSizePolicy(sizePolicy)
        self.runtime.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.runtime.setFont(font)
        self.runtime.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.runtime.setObjectName("runtime")
        self.runtime_box.addWidget(self.runtime)
        self.runtime_value = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runtime_value.sizePolicy().hasHeightForWidth())
        self.runtime_value.setSizePolicy(sizePolicy)
        self.runtime_value.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.runtime_value.setFont(font)
        self.runtime_value.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.runtime_value.setOpenExternalLinks(True)
        self.runtime_value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        self.runtime_value.setObjectName("runtime_value")
        self.runtime_box.addWidget(self.runtime_value)
        self.info_area_vertical_layout.addLayout(self.runtime_box)
        self.genre_box = QtWidgets.QHBoxLayout()
        self.genre_box.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.genre_box.setObjectName("genre_box")
        self.genre = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.genre.sizePolicy().hasHeightForWidth())
        self.genre.setSizePolicy(sizePolicy)
        self.genre.setWordWrap(True)
        self.genre.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.genre.setFont(font)
        self.genre.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.genre.setObjectName("genre")
        self.genre_box.addWidget(self.genre)
        self.genre_value = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.genre_value.sizePolicy().hasHeightForWidth())
        self.genre_value.setSizePolicy(sizePolicy)
        self.genre_value.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.genre_value.setFont(font)
        self.genre_value.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.genre_value.setOpenExternalLinks(True)
        self.genre_value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        self.genre_value.setObjectName("genre_value")
        self.genre_box.addWidget(self.genre_value)
        self.info_area_vertical_layout.addLayout(self.genre_box)
        self.budget_box = QtWidgets.QHBoxLayout()
        self.budget_box.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.budget_box.setObjectName("budget_box")
        self.budget = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.budget.sizePolicy().hasHeightForWidth())
        self.budget.setSizePolicy(sizePolicy)
        self.budget.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.budget.setFont(font)
        self.budget.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.budget.setObjectName("budget")
        self.budget_box.addWidget(self.budget)
        self.budget_value = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.budget_value.sizePolicy().hasHeightForWidth())
        self.budget_value.setSizePolicy(sizePolicy)
        self.budget_value.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.budget_value.setFont(font)
        self.budget_value.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.budget_value.setOpenExternalLinks(True)
        self.budget_value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        self.budget_value.setObjectName("budget_value")
        self.budget_box.addWidget(self.budget_value)
        self.info_area_vertical_layout.addLayout(self.budget_box)
        self.box_office_box = QtWidgets.QHBoxLayout()
        self.box_office_box.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.box_office_box.setObjectName("box_office_box")
        self.box_office = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box_office.sizePolicy().hasHeightForWidth())
        self.box_office.setSizePolicy(sizePolicy)
        self.box_office.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.box_office.setFont(font)
        self.box_office.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.box_office.setObjectName("box_office")
        self.box_office_box.addWidget(self.box_office)
        self.box_office_value = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box_office_value.sizePolicy().hasHeightForWidth())
        self.box_office_value.setSizePolicy(sizePolicy)
        self.box_office_value.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.box_office_value.setFont(font)
        self.box_office_value.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.box_office_value.setOpenExternalLinks(True)
        self.box_office_value.setObjectName("box_office_value")
        self.box_office_box.addWidget(self.box_office_value)
        self.info_area_vertical_layout.addLayout(self.box_office_box)
        self.cast_box = QtWidgets.QVBoxLayout()
        self.cast_box.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.cast_box.setSpacing(4)
        self.cast_box.setObjectName("cast_box")
        self.cast = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cast.sizePolicy().hasHeightForWidth())
        self.cast.setSizePolicy(sizePolicy)
        self.cast.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.cast.setFont(font)
        self.cast.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.cast.setObjectName("cast")
        self.cast_box.addWidget(self.cast)
        self.cast_value = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cast_value.sizePolicy().hasHeightForWidth())
        self.cast_value.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.cast_value.setFont(font)
        self.cast_value.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.cast_value.setWordWrap(True)
        self.cast_value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        self.cast_value.setObjectName("cast_value")
        self.cast_box.addWidget(self.cast_value)
        self.info_area_vertical_layout.addLayout(self.cast_box)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.info_area_vertical_layout.addItem(spacerItem4)
        self.plot_value = QtWidgets.QLabel(self.info_scroll_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_value.sizePolicy().hasHeightForWidth())
        self.plot_value.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.plot_value.setFont(font)
        self.plot_value.setTextFormat(QtCore.Qt.AutoText)
        self.plot_value.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.plot_value.setWordWrap(True)
        self.plot_value.setObjectName("plot_value")
        self.info_area_vertical_layout.addWidget(self.plot_value)
        self.info_area.setWidget(self.info_scroll_area)
        self.main_area_horizontal_layout.addWidget(self.info_area)
        self.verticalLayout.addLayout(self.main_area_horizontal_layout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 886, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStatusTip("")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSetting = QtWidgets.QAction(MainWindow)
        self.actionSetting.setObjectName("actionSetting")
        self.actionAbout1 = QtWidgets.QAction(MainWindow)
        self.actionAbout1.setObjectName("actionAbout1")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionSetting)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout1)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        # self.pushButton_3.clicked.connect(self.info_area.repaint)
        self.search_button.clicked.connect(self.search_option)
        self.search_field.returnPressed.connect(self.search_option)
        self.search_field.textChanged.connect(self.search_option)
        self.sort_combo_box.currentIndexChanged['QString'].connect(self.sort_option_changed)

        # self.sort_combo_box
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # self.button_event()
        self.signal_handling()

        self.actionExit.triggered.connect(MainWindow.close)
        self.actionSetting.triggered.connect(self.setting_window)
        self.actionAbout1.triggered.connect(self.info_window)

        self.update_movie_info(self.buttons[0].objectName())

    # def button_event(self):
    #     for b in self.buttons:
    #         b.clicked.connect(self.update_movie_info)
    #         b.doubleClicked.connect(self.open_movie)
    #
    # def remove_button_objects(self):
    #     for b in self.buttons:
    #         del b
    #     self.button_event()

    def signal_handling(self):
        for b in self.buttons:
            b.installEventFilter(self)

            # print(b)

    def remove_event(self):
        for b in self.buttons:
            b.removeEventFilter(self)
        self.signal_handling()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("Double Click")
            self.open_movie(obj)

        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                print(obj.objectName(), "Left click")
                self.update_movie_info(movie_name=obj.objectName())



            elif event.button() == QtCore.Qt.RightButton:
                print(obj.objectName(), "Right click")
                # self.actionRight(obj)


            elif event.button() == QtCore.Qt.MiddleButton:
                print(obj.objectName(), "Middle click")
        return QtCore.QObject.event(obj, event)

    def sort_option_changed(self):
        print("Want to wipe out movie area")
        for i in reversed(range(self.flow_layout.count())):
            self.flow_layout.itemAt(i).widget().setParent(None)

        text = self.sender().currentText()
        print(text)
        self.movie_list = list(self.db.database.keys())
        if text == 'Name A->Z':
            self.movie_list.sort()
        elif text == 'Name Z->A':
            self.movie_list.sort(reverse=True)
        elif text == 'Rating':
            self.movie_list = self.sort_by('vote_average')
        elif text == 'Year':
            self.movie_list = self.sort_by('release_date')

        self.add_buttons(self.movie_list)
        self.movie_area.repaint()
        self.remove_event()
        # self.remove_button_objects()
        # self.movie_area.update()

    def search_option(self):
        print("Want to wipe out movie area")
        query = self.search_field.text()
        print("query i:=", query)
        #
        # if query=='':
        #     self.movie_list=self.db.database.keys()

        # if len(self.movie_list) == 0:
        #     return

        self.movie_list = self.db.database.keys()
        self.movie_list = [name for name in self.movie_list if query.lower() in name.lower()]

        self.remove_event()
        for i in reversed(range(self.flow_layout.count())):
            self.flow_layout.itemAt(i).widget().setParent(None)
        self.add_buttons(self.movie_list)
        self.signal_handling()

    def sort_by(self, order):
        print("sort by function", order)
        sort_list = []
        for movie_name, info in self.db.database.items():
            print(movie_name, info)
            sort_list.append((info[order], movie_name))

        sort_list.sort(reverse=True)
        temp = [movie_name for info_order, movie_name in sort_list]
        return temp

    def open_movie(self, obj):
        movie_name = obj.objectName()
        print(movie_name, self.db.database[movie_name]['location'])
        os.startfile(self.db.database[movie_name]['location'])

    def update_movie_info(self, movie_name=None):
        if not movie_name:
            movie_name = self.sender().objectName()
        print('\n' + movie_name)

        self.rating_value.setText(str(self.db.database[movie_name]['vote_average']))
        self.budget_value.setText(str(self.db.database[movie_name]['budget'] // 1000000) + 'm')
        self.box_office_value.setText(str(self.db.database[movie_name]['revenue'] // 1000000) + 'm')
        self.year_value.setText(self.db.database[movie_name]['release_date'][:4])
        self.tagline.setText(self.db.database[movie_name]['tagline'])
        self.title_value.setText(self.db.database[movie_name]['title'])
        self.plot_value.setText(self.db.database[movie_name]['overview'])

        self.poster_value.setPixmap(QtGui.QPixmap('./media/poster/' + movie_name + '.jpg'))
        self.backdrop_value.setPixmap(QtGui.QPixmap('./media/backdrop/' + movie_name + '.jpg'))
        self.runtime_value.setText(str(self.db.database[movie_name]['runtime']) + ' minutes')

        cast_dict = self.db.database[movie_name]['cast']
        cast = ", ".join([actor for actor in cast_dict.keys()])
        self.cast_value.setText(cast)

        self.director_value.setText(", ".join(director for director in self.db.database[movie_name]['director']))

        # print(self.db.database[movie_name]['genres'])
        genres_dict = self.db.database[movie_name]['genres']
        # for genre in genres_dict:
        print('got here')

        self.genre_value.setText(", ".join(genre["name"] for genre in self.db.database[movie_name]['genres']))

        # self.flow_layout.update()
        self.info_area.repaint()
        # self.info_area.update()
        # self.button_event()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Movie Catalog"))
        self.search_button.setText(_translate("MainWindow", "Search"))
        self.label.setText(_translate("MainWindow", "Sort By"))
        self.sort_combo_box.setItemText(0, _translate("MainWindow", "Name A->Z"))
        self.sort_combo_box.setItemText(1, _translate("MainWindow", "Name Z->A"))
        self.sort_combo_box.setItemText(2, _translate("MainWindow", "Rating"))
        self.sort_combo_box.setItemText(3, _translate("MainWindow", "Year"))
        # self.pushButton.setText(_translate("MainWindow", "Properties"))
        self.properties.setText(_translate("MainWindow", "Properties"))
        self.title_value.setText(_translate("MainWindow", "TextLabel"))
        self.tagline.setText(_translate("MainWindow", "dsjfklsadfkjfsdlfjs lfsad"))
        self.year.setText(_translate("MainWindow", "Year"))
        self.year_value.setText(_translate("MainWindow", "TextLabel"))
        self.director.setText(_translate("MainWindow", "Director"))
        self.director_value.setText(_translate("MainWindow", "TextLabel"))
        self.genre.setText(_translate("MainWindow", "Genre"))
        self.genre_value.setText(_translate("MainWindow", "TextLabel"))
        self.rating.setText(_translate("MainWindow", "Rating"))
        self.rating_value.setText(_translate("MainWindow", "TextLabel"))
        self.runtime.setText(_translate("MainWindow", "Duration"))
        self.runtime_value.setText(_translate("MainWindow", "TextLabel"))
        self.cast.setText(_translate("MainWindow", "Cast"))
        self.budget.setText(_translate("MainWindow", "Budget"))
        self.budget_value.setText(_translate("MainWindow", "TextLabel"))
        self.box_office.setText(_translate("MainWindow", "Box Office"))
        self.box_office_value.setText(_translate("MainWindow", "TextLabel"))
        self.cast_value.setText(_translate("MainWindow",
                                           "dskfjlksjdsflsdlfkjsflksjflkfsdj;lkds sa fds ds fsdfsjlfsdkjflskadjf;lskjsdf;lksdflkjfdslkdjsflksfdj;lksfjsLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen boo;fdlkfsl"))
        self.plot_value.setText(_translate("MainWindow",
                                           "dskfjlksjdsflsdlfkjsflksjflkfsdj;lkds sa fds ds fsdfsjlfsdkjflskadjf;lskjsdf;lksdflkjfdslkdjsflksfdj;lksfjsLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen boo;fdlkfsl"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionSetting.setText(_translate("MainWindow", "Setting"))
        self.actionAbout1.setText(_translate("MainWindow", "About"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

    def add_buttons(self, movie_list):
        self.movie_list = movie_list
        # Get the names of all the movie from database json
        # print(movie_lst)
        #
        s = QtCore.QSize(154, 240)

        self.buttons = []

        for movie in self.movie_list:
            # b = QtWidgets.QLabel()
            b = QtWidgets.QToolButton()
            b.setText(movie)
            b.setObjectName(movie)
            path = './media/poster/' + movie + '.jpg'
            # print(movie, path)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            b.setIcon(icon)
            b.setAutoRaise(True)
            b.setStyleSheet('''text-align:left;''')
            b.setIconSize(QtCore.QSize(154, 210))
            b.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            # b.setCheckable(True)

            b.setFixedSize(s)

            self.flow_layout.addWidget(b)

            self.buttons.append(b)
            self.statusbar.showMessage(str(len(self.movie_list)) + " movies loaded")


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # Splash Screen
    # splash_screen = QtGui.QSplashScreen()
    #     # splash_screen.show()
    pixmap = QPixmap("new.png")
    splash = QSplashScreen(pixmap)
    splash.showMessage("Loading..")
    app.processEvents()
    splash.show()

    for i in range(100000):
        print(i)
        continue

    db = database.Network("A:\\!Movie")
    db.start()


    window = MainWindow(db)
    splash.finish(window)
    window.show()
    sys.exit(app.exec_())
