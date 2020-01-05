# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#

from PyQt5 import QtCore, QtGui, QtWidgets

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
    def __init__(self, db, parent=None, ):
        super().__init__()
        self.db = db
        self.initUI(self)

        # root = tkinter.Tk()
        # self.width = root.winfo_screenwidth()
        # self.height = root.winfo_screenheight()
        # print(self.width, self.height);

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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.search_field = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_field.sizePolicy().hasHeightForWidth())
        self.search_field.setSizePolicy(sizePolicy)
        self.search_field.setMaximumSize(QtCore.QSize(185, 28))
        self.search_field.setToolTip("")
        self.search_field.setPlainText("")
        self.search_field.setPlaceholderText("")
        self.search_field.setObjectName("search_field")
        self.horizontalLayout.addWidget(self.search_field)
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setMaximumSize(QtCore.QSize(68, 32))
        self.search_button.setObjectName("search_button")
        self.horizontalLayout.addWidget(self.search_button)
        spacerItem = QtWidgets.QSpacerItem(10, 31, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(46, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.sort_combo_box = QtWidgets.QComboBox(self.centralwidget)
        self.sort_combo_box.setMinimumSize(QtCore.QSize(0, 28))
        self.sort_combo_box.setMaximumSize(QtCore.QSize(108, 16777215))
        self.sort_combo_box.setObjectName("sort_combo_box")
        self.sort_combo_box.addItem("")
        self.sort_combo_box.addItem("")
        self.sort_combo_box.addItem("")
        self.sort_combo_box.addItem("")
        self.horizontalLayout.addWidget(self.sort_combo_box)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMaximumSize(QtCore.QSize(79, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")


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

        self.add_buttons()

        self.movie_area.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.movie_area)

        # Spacer between movie area and info area
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(spacerItem2)

        # Info Area
        self.info_area = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_area.sizePolicy().hasHeightForWidth())
        self.info_area.setSizePolicy(sizePolicy)
        self.info_area.setWidgetResizable(True)
        self.info_area.setMinimumSize(QtCore.QSize(700, 0))
        self.info_area.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.info_area.setObjectName("info_area")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 497, 631))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_2.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.title_value = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_value.sizePolicy().hasHeightForWidth())
        self.title_value.setSizePolicy(sizePolicy)
        self.title_value.setMaximumSize(QtCore.QSize(16777215, 28))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.title_value.setFont(font)
        self.title_value.setMidLineWidth(0)
        self.title_value.setScaledContents(False)
        self.title_value.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.title_value.setWordWrap(True)
        self.title_value.setOpenExternalLinks(False)
        self.title_value.setObjectName("title_value")
        self.verticalLayout_4.addWidget(self.title_value)
        self.poster_value = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.poster_value.sizePolicy().hasHeightForWidth())
        self.poster_value.setSizePolicy(sizePolicy)
        self.poster_value.setMaximumSize(QtCore.QSize(16777215, 432))
        self.poster_value.setText("")
        self.poster_value.setPixmap(QtGui.QPixmap("A Beautiful Mind.jpg"))
        self.poster_value.setScaledContents(False)
        self.poster_value.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.poster_value.setObjectName("poster_value")
        self.verticalLayout_4.addWidget(self.poster_value)
        self.tagline = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagline.sizePolicy().hasHeightForWidth())
        self.tagline.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tagline.setFont(font)
        self.tagline.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.tagline.setObjectName("tagline")
        self.verticalLayout_4.addWidget(self.tagline)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.year = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.year.sizePolicy().hasHeightForWidth())
        self.year.setSizePolicy(sizePolicy)
        self.year.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.year.setFont(font)
        self.year.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.year.setObjectName("year")
        self.horizontalLayout_3.addWidget(self.year)
        self.year_value = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.year_value.sizePolicy().hasHeightForWidth())
        self.year_value.setSizePolicy(sizePolicy)
        self.year_value.setMaximumSize(QtCore.QSize(16777215, 15))
        self.year_value.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.year_value.setObjectName("yearValue")
        self.horizontalLayout_3.addWidget(self.year_value)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.rating = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rating.sizePolicy().hasHeightForWidth())
        self.rating.setSizePolicy(sizePolicy)
        self.rating.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.rating.setFont(font)
        self.rating.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.rating.setObjectName("rating")
        self.horizontalLayout_4.addWidget(self.rating)
        self.rating_value = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rating_value.sizePolicy().hasHeightForWidth())
        self.rating_value.setSizePolicy(sizePolicy)
        self.rating_value.setMaximumSize(QtCore.QSize(16777215, 15))
        self.rating_value.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.rating_value.setObjectName("rating_value")
        self.horizontalLayout_4.addWidget(self.rating_value)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.director = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.director.sizePolicy().hasHeightForWidth())
        self.director.setSizePolicy(sizePolicy)
        self.director.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.director.setFont(font)
        self.director.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.director.setObjectName("director")
        self.horizontalLayout_7.addWidget(self.director)
        self.director_value = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.director_value.sizePolicy().hasHeightForWidth())
        self.director_value.setSizePolicy(sizePolicy)
        self.director_value.setMaximumSize(QtCore.QSize(16777215, 15))
        self.director_value.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.director_value.setObjectName("director_value")
        self.horizontalLayout_7.addWidget(self.director_value)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.runtime = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runtime.sizePolicy().hasHeightForWidth())
        self.runtime.setSizePolicy(sizePolicy)
        self.runtime.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.runtime.setFont(font)
        self.runtime.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)
        self.runtime.setObjectName("runtime")
        self.horizontalLayout_5.addWidget(self.runtime)
        self.runtime_value = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runtime_value.sizePolicy().hasHeightForWidth())
        self.runtime_value.setSizePolicy(sizePolicy)
        self.runtime_value.setMaximumSize(QtCore.QSize(16777215, 15))
        self.runtime_value.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.runtime_value.setObjectName("runtime_value")
        self.horizontalLayout_5.addWidget(self.runtime_value)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.genre = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.genre.sizePolicy().hasHeightForWidth())
        self.genre.setSizePolicy(sizePolicy)
        self.genre.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.genre.setFont(font)
        self.genre.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.genre.setObjectName("genre")
        self.horizontalLayout_6.addWidget(self.genre)
        self.genre_value = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.genre_value.sizePolicy().hasHeightForWidth())
        self.genre_value.setSizePolicy(sizePolicy)
        self.genre_value.setMaximumSize(QtCore.QSize(16777215, 15))
        self.genre_value.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.genre_value.setObjectName("genre_value")
        self.horizontalLayout_6.addWidget(self.genre_value)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.cast = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cast.sizePolicy().hasHeightForWidth())
        self.cast.setSizePolicy(sizePolicy)
        self.cast.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.cast.setFont(font)
        self.cast.setAlignment(QtCore.Qt.AlignCenter)
        self.cast.setObjectName("cast")
        self.verticalLayout_3.addWidget(self.cast)
        self.cast_value = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cast_value.sizePolicy().hasHeightForWidth())
        self.cast_value.setSizePolicy(sizePolicy)
        self.cast_value.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.cast_value.setWordWrap(True)
        self.cast_value.setObjectName("cast_value")
        self.verticalLayout_3.addWidget(self.cast_value)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.plot_value = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_value.sizePolicy().hasHeightForWidth())
        self.plot_value.setSizePolicy(sizePolicy)
        self.plot_value.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.plot_value.setWordWrap(True)
        self.plot_value.setObjectName("plot_value")
        self.verticalLayout_4.addWidget(self.plot_value)
        self.info_area.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_2.addWidget(self.info_area)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 954, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)




        self.actionSetting = QtWidgets.QAction(MainWindow)
        self.actionSetting.setObjectName("actionSetting")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionSetting)
        self.menuFile.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())

        for b in self.buttons:
            b.clicked.connect(self.update_movie_info)

        self.retranslateUi(MainWindow)
        # self.pushButton_3.clicked.connect(self.info_area.repaint)
        self.search_button.clicked.connect(self.movie_area.repaint)
        self.sort_combo_box.currentIndexChanged['QString'].connect(self.movie_area.repaint)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # def action(self):
    #     sender = self.sender()
    #     print(sender.objectName())

        ## Get movie info
        ## Update the movie info and repaint



    def update_movie_info(self, movie_name):
        movie_name = self.sender.objectName()

        self.rating_value.setText(self.db.database[movie_name]['vote_average'])
        self.year_value.setText(self.db.database[movie_name]['release_date'])
        self.runtime_value.setText(self.db.database[movie_name]['runtime'])
        # self.director_value.setText(self.db.database[movie_name][''])


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Movie Catalog"))
        self.search_button.setText(_translate("MainWindow", "Search"))
        self.label.setText(_translate("MainWindow", "Sort By"))
        self.sort_combo_box.setItemText(0, _translate("MainWindow", "Name A->Z"))
        self.sort_combo_box.setItemText(1, _translate("MainWindow", "Name Z-A"))
        self.sort_combo_box.setItemText(2, _translate("MainWindow", "Rating"))
        self.sort_combo_box.setItemText(3, _translate("MainWindow", "Year"))
        # self.pushButton.setText(_translate("MainWindow", "Properties"))
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
        self.cast_value.setText(_translate("MainWindow",
                                           "dskfjlksjdsflsdlfkjsflksjflkfsdj;lkds sa fds ds fsdfsjlfsdkjflskadjf;lskjsdf;lksdflkjfdslkdjsflksfdj;lksfjsLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen boo;fdlkfsl"))
        self.plot_value.setText(_translate("MainWindow",
                                           "dskfjlksjdsflsdlfkjsflksjflkfsdj;lkds sa fds ds fsdfsjlfsdkjflskadjf;lskjsdf;lksdflkjfdslkdjsflksfdj;lksfjsLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen boo;fdlkfsl"))
        self.actionSetting.setText(_translate("MainWindow", "Setting"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

    def add_buttons(self):
        # Get the names of all the movie from database json
        movie_lst = self.db.database.keys()
        # print(movie_lst)
        #
        s = QtCore.QSize(154, 240)

        self.buttons = []

        for movie in movie_lst:
            # b = QtWidgets.QLabel()
            b = QtWidgets.QToolButton()
            b.setText(movie)
            b.setObjectName(movie)
            path ='./media/poster/' + movie + '.jpg'
            print(movie, path)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            b.setIcon(icon)
            b.setAutoRaise(True)
            b.setStyleSheet('''text-align:left;''')
            b.setIconSize(QtCore.QSize(154, 210))
            b.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            b.setFixedSize(s)
            self.flow_layout.addWidget(b)
            self.buttons.append(b)
            self.statusbar.showMessage(str(len(movie_lst))+ " movies loaded")



if __name__ == '__main__':
    import sys

    db = database.Network("A:\\!Movie")
    db.start()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(db)
    window.show()
    sys.exit(app.exec_())
