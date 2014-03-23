# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_fxcc2qgis.ui'
#
# Created: Sun Mar 23 00:30:56 2014
#      by: PyQt4 UI code generator 4.10.3
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
        fxcc2Qgis.resize(400, 227)
        self.buttonBox = QtGui.QDialogButtonBox(fxcc2Qgis)
        self.buttonBox.setGeometry(QtCore.QRect(40, 180, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(fxcc2Qgis)
        self.label.setGeometry(QtCore.QRect(20, 20, 361, 41))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(fxcc2Qgis)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 361, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.cmpRuta = QtGui.QLineEdit(fxcc2Qgis)
        self.cmpRuta.setGeometry(QtCore.QRect(20, 120, 251, 34))
        self.cmpRuta.setObjectName(_fromUtf8("cmpRuta"))
        self.btnSeleccionar = QtGui.QPushButton(fxcc2Qgis)
        self.btnSeleccionar.setGeometry(QtCore.QRect(280, 120, 101, 32))
        self.btnSeleccionar.setObjectName(_fromUtf8("btnSeleccionar"))

        self.retranslateUi(fxcc2Qgis)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), fxcc2Qgis.reject)
        QtCore.QMetaObject.connectSlotsByName(fxcc2Qgis)

    def retranslateUi(self, fxcc2Qgis):
        fxcc2Qgis.setWindowTitle(_translate("fxcc2Qgis", "fxcc2Qgis", None))
        self.label.setText(_translate("fxcc2Qgis", "Con este plugin se puede procesar ficheros de intercambio FXCC de Catastro.", None))
        self.label_2.setText(_translate("fxcc2Qgis", "Seleccione el directorio con FXCC a importar:", None))
        self.btnSeleccionar.setText(_translate("fxcc2Qgis", "Seleccionar", None))

