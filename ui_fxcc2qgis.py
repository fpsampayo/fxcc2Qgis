# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_fxcc2qgis.ui'
#
# Created: Tue Feb 25 14:40:16 2014
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_fxcc2Qgis(object):
    def setupUi(self, fxcc2Qgis):
        fxcc2Qgis.setObjectName(_fromUtf8("fxcc2Qgis"))
        fxcc2Qgis.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(fxcc2Qgis)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.retranslateUi(fxcc2Qgis)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), fxcc2Qgis.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), fxcc2Qgis.reject)
        QtCore.QMetaObject.connectSlotsByName(fxcc2Qgis)

    def retranslateUi(self, fxcc2Qgis):
        fxcc2Qgis.setWindowTitle(_translate("fxcc2Qgis", "fxcc2Qgis", None))

