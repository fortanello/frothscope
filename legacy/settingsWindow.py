from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator, QIntValidator
from PyQt5.QtWidgets import QDesktopWidget
from selectedArea import ImageSelector
from selectedAreaPolygons import ImageSelectorPolygons
import functions

functions.read_settings()

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        data = functions.read_settings()
        Dialog.setObjectName("Dialog")
        Dialog.resize(649, 764)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_16 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_16.setFont(font)
        self.label_16.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_3.addWidget(self.label_16)
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_3.addWidget(self.pushButton_6)
        self.pushButton_7 = QtWidgets.QPushButton(Dialog)
        self.pushButton_7.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout_3.addWidget(self.pushButton_7)
        self.gridLayout.addLayout(self.verticalLayout_3, 1, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_15 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.verticalLayout.addWidget(self.label_15)
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.label_10 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.label_11 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.verticalLayout.addWidget(self.label_11)
        self.label_17 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.verticalLayout.addWidget(self.label_17)
        self.label_18 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.verticalLayout.addWidget(self.label_18)
        self.label_12 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.verticalLayout.addWidget(self.label_12)
        self.label_13 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.verticalLayout.addWidget(self.label_13)
        self.label_14 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.verticalLayout.addWidget(self.label_14)
        self.label_19 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.verticalLayout.addWidget(self.label_19)
        self.label_20 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.verticalLayout.addWidget(self.label_20)
        self.label_21 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.verticalLayout.addWidget(self.label_21)
        self.horizontalLayout_6.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_2.addWidget(self.lineEdit_3)
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.verticalLayout_2.addWidget(self.lineEdit_4)
        self.lineEdit_5 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.verticalLayout_2.addWidget(self.lineEdit_5)
        self.lineEdit_6 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.verticalLayout_2.addWidget(self.lineEdit_6)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.lineEdit_7 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.horizontalLayout_3.addWidget(self.lineEdit_7)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_4.addWidget(self.pushButton_4)
        self.lineEdit_8 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.horizontalLayout_4.addWidget(self.lineEdit_8)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_5.addWidget(self.pushButton_5)
        self.lineEdit_9 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_9.setFont(font)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.horizontalLayout_5.addWidget(self.lineEdit_9)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout_2.addWidget(self.comboBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_8 = QtWidgets.QPushButton(Dialog)
        self.pushButton_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_2.addWidget(self.pushButton_8)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.lineEdit_10 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_10.setFont(font)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.horizontalLayout_2.addWidget(self.lineEdit_10)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.lineEdit_11 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_11.setFont(font)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.verticalLayout_2.addWidget(self.lineEdit_11)
        self.lineEdit_15 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_15.setFont(font)
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.verticalLayout_2.addWidget(self.lineEdit_15)
        self.lineEdit_14 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_14.setFont(font)
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.verticalLayout_2.addWidget(self.lineEdit_14)
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName("comboBox_2")
        self.verticalLayout_2.addWidget(self.comboBox_2)
        self.lineEdit_12 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_12.setFont(font)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.verticalLayout_2.addWidget(self.lineEdit_12)
        self.lineEdit_13 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_13.setFont(font)
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.verticalLayout_2.addWidget(self.lineEdit_13)
        self.lineEdit_16 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_16.setFont(font)
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.verticalLayout_2.addWidget(self.lineEdit_16)
        self.lineEdit_17 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_17.setFont(font)
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.verticalLayout_2.addWidget(self.lineEdit_17)
        self.comboBox_3 = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_3.setFont(font)
        self.comboBox_3.setObjectName("comboBox_3")
        self.verticalLayout_2.addWidget(self.comboBox_3)
        self.horizontalLayout_6.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        #new

        self.lineEdit.setText(str(data['filePath']))
        self.lineEdit_2.setText(str(data['frameNumber']))
        self.lineEdit_3.setText(str(data['framesInterval']))
        self.lineEdit_4.setText(str(data['frame_count']))
        self.lineEdit_5.setText(str(data['min_bubble_area']))
        self.lineEdit_6.setText(str(data['max_bubble_area']))
        self.lineEdit_7.setText(str(data['koefBin']))
        self.lineEdit_8.setText(str(data['koefContrast']))
        self.lineEdit_9.setText(str(data['koefAntiGlare']))
        self.comboBox.addItem("Прямоугольник")
        self.comboBox.addItem("Полигоны")
        self.comboBox.setCurrentIndex(int(data['selectedAreaMode']))
        self.lineEdit_10.setText(str(data['windowCoords']))
        #self.lineEdit_10.setReadOnly(True)
        self.lineEdit_11.setText(str(data['pointsOnGraph']))
        self.lineEdit_15.setText(str(data['delay']))
        self.lineEdit_14.setText(str(data['usr']))
        self.comboBox_2.addItem("Нейросеть (новый)")
        self.comboBox_2.addItem("По освещенности (старый)")
        self.comboBox_2.addItem("Отсутствует")
        self.comboBox_2.setCurrentIndex(int(data['syncMode']))

        self.comboBox_3.addItem("Максимальных пиках")
        self.comboBox_3.addItem("Минимальных пиках")
        self.comboBox_3.setCurrentIndex(int(data['peak']))

        if data['syncMode'] == '2':
            self.label_14.hide()
            self.lineEdit_13.hide()
            self.label_13.hide()
            self.lineEdit_12.hide()
            self.lineEdit_15.hide()
            self.lineEdit_16.hide()
            self.lineEdit_17.hide()
            self.label_19.hide()
            self.label_20.hide()
            self.label_21.hide()
            self.comboBox_3.hide()
        elif data['syncMode'] == '0':
            
            self.lineEdit_12.setText(str(data['skipFrames']))
            self.label_13.setText('- сколько пропускать: ')
            self.label_14.hide()
            self.lineEdit_13.hide()
            self.lineEdit_16.hide()
            self.lineEdit_17.hide()
            self.label_19.hide()
            self.label_20.hide()
            self.label_21.hide()
            self.comboBox_3.hide()
        else:
            self.lineEdit_12.setText(str(data['R']))
            self.lineEdit_13.setText(str(data['delta_t']))
            self.lineEdit_16.setText(str(data['N']))
            self.lineEdit_17.setText(str(data['delaySync']))
        self.comboBox_2.currentIndexChanged.connect(self.on_combobox_changed)
        self.comboBox_3.currentIndexChanged.connect(self.on_cbx_changed)


        self.update_data()

        self.pushButton.clicked.connect(self.load_file)
        self.pushButton_3.clicked.connect(lambda: self.resetKoef(0))
        self.pushButton_4.clicked.connect(lambda: self.resetKoef(1))
        self.pushButton_5.clicked.connect(lambda: self.resetKoef(2))
        self.pushButton_2.clicked.connect(self.getCoords)
        self.pushButton_8.clicked.connect(self.resetCoords)
        self.pushButton_6.clicked.connect(self.saveChanges)
        self.pushButton_7.clicked.connect(Dialog.close)



        self.lineEdit.textChanged.connect(lambda: self.onTextChanged(self.lineEdit))
        self.lineEdit_2.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_2))
        self.lineEdit_3.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_3))
        self.lineEdit_4.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_4))
        self.lineEdit_5.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_5))
        self.lineEdit_6.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_6))
        self.lineEdit_7.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_7))
        self.lineEdit_8.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_8))
        self.lineEdit_9.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_9))
        self.lineEdit_10.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_10))
        self.lineEdit_11.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_11))
        self.lineEdit_12.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_12))
        self.lineEdit_13.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_13))
        self.lineEdit_14.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_14))
        self.lineEdit_15.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_15))
        self.lineEdit_16.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_16))
        self.lineEdit_17.textChanged.connect(lambda: self.onTextChanged(self.lineEdit_17))

        self.setLineEditValidator(self.lineEdit)
        self.setLineEditValidator(self.lineEdit_2)
        self.setLineEditValidator3(self.lineEdit_3)
        self.setLineEditValidator(self.lineEdit_4)
        self.setLineEditValidator(self.lineEdit_5)
        self.setLineEditValidator(self.lineEdit_6)
        self.setLineEditValidator(self.lineEdit_7)
        self.setLineEditValidator(self.lineEdit_8)
        self.setLineEditValidator(self.lineEdit_9)
        self.setLineEditValidator2(self.lineEdit_10)
        self.setLineEditValidator(self.lineEdit_17)
        self.setLineEditValidator(self.lineEdit_11)
        self.setLineEditValidator(self.lineEdit_12)
        self.setLineEditValidator(self.lineEdit_13)
        self.setLineEditValidator(self.lineEdit_16)

    def resetCoords(self):
        self.lineEdit_10.setText('-1')

    def on_cbx_changed(self):
        self.label_16.setText("")
    def on_combobox_changed(self, index):
        self.label_16.setText("")
        self.update_data()
        data = functions.read_settings()
        if index == 1:
            self.label_14.show()
            self.lineEdit_13.show()
            self.label_13.show()
            self.label_13.setText('- на сколько делить: ')
            self.lineEdit_12.show()
            self.lineEdit_12.setText(str(data['R']))
            self.lineEdit_13.setText(str(data['delta_t']))

            self.label_19.show()
            self.label_20.show()
            self.lineEdit_16.show()
            self.lineEdit_17.show()
            self.lineEdit_16.setText(str(data['N']))
            self.lineEdit_17.setText(str(data['delaySync']))
            self.comboBox_3.show()
            self.label_21.show()
        elif index == 0:
            self.lineEdit_12.show()
            self.label_13.show()
            self.lineEdit_12.setText(str(data['skipFrames']))
            self.label_13.setText('- сколько пропускать: ')
            self.label_14.hide()
            self.lineEdit_13.hide()
            self.lineEdit_16.hide()
            self.lineEdit_17.hide()
            self.label_19.hide()
            self.label_20.hide()
            self.label_21.hide()
            self.comboBox_3.hide()
        else:
            self.label_19.hide()
            self.label_20.hide()
            self.label_21.hide()
            self.lineEdit_16.hide()
            self.lineEdit_17.hide()
            self.lineEdit_12.setText(str(data['R']))
            self.lineEdit_13.setText(str(data['delta_t']))
            self.label_14.hide()
            self.lineEdit_13.hide()
            self.label_13.hide()
            self.lineEdit_12.hide()
            self.comboBox_3.hide()

    def load_file(self):
        try:
            file_dialog = QtWidgets.QFileDialog()
            file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            file_dialog.setNameFilter("Video files (*.mp4 *.avi *.mpg *.mpeg *.jpg *.jpeg *.png)")

            if file_dialog.exec_():
                selected_file = file_dialog.selectedFiles()
                file_path = selected_file[0]
                self.lineEdit.setText(file_path)
        except Exception as ex:
            print(ex)
            
    def resetKoef(self, idx):
        if idx == 0:
            self.lineEdit_7.setText('-1')
        elif idx == 1:
            self.lineEdit_8.setText('-1')
        else:
            self.lineEdit_9.setText('-1')


    

    def getCoords(self):
        try:
            if (self.comboBox.currentIndex() == 0):
                self.imageSelector = ImageSelector(file_path = self.lineEdit.text(), idx=0, frameNumber = int(self.lineEdit_2.text()))
            elif (self.comboBox.currentIndex() == 1):
                print(self.lineEdit.text())
                self.imageSelector = ImageSelectorPolygons(file_path = self.lineEdit.text(), idx=0, frameNumber = int(self.lineEdit_2.text()))
                print(1)
                
            self.imageSelector.dataSaved.connect(self.handleDataSaved)
            self.imageSelector.exec_()
            self.imageSelector.raise_()
            self.imageSelector.activateWindow()
        except Exception as ex:
            print(ex)
    def handleDataSaved(self, idx, data):
        self.lineEdit_10.setText(data)

    def saveChanges(self):
        try:
            with open("settings.ini", "r") as file:
                lines = file.readlines()
                lines[0] = self.lineEdit.text() + " ; файл или порт камеры\n"
                lines[1] = self.lineEdit_2.text()+ " ; номер кадра, с которого начинать обработку\n"
                lines[2] = self.lineEdit_3.text() + " ; мин. интервал между кадрами (в секундах)\n"
                lines[3] = self.lineEdit_4.text() + " ; сколько кадров обрабатывать\n"
                lines[4] = self.lineEdit_5.text() + " ; мин. площадь пузырька (в пикселях)\n"
                lines[5] = self.lineEdit_6.text() + " ; макс. площадь пузырька (в пикселях)\n"
                lines[6] = self.lineEdit_7.text() + " ; коэффициент бинаризации\n"
                lines[7] = self.lineEdit_8.text() + " ; уровень контрастности\n"
                lines[8] = self.lineEdit_9.text() + " ; антиблик\n"
                lines[9] = str(self.comboBox.currentIndex()) + " ; режим выделяемой области\n"
                lines[10] = self.lineEdit_10.text() + " ; координаты окна\n"
                lines[11] = self.lineEdit_11.text() + " ; количество точек на графиках\n"
                lines[12] = str(self.comboBox_2.currentIndex()) + " ; алгоритм синхронизации\n"
                if self.comboBox_2.currentIndex() == 1:
                    lines[13] = self.lineEdit_12.text() + " ; на сколько делить при синхронизации\n"
                    lines[14] = self.lineEdit_13.text() + " ; промежуток времени при синхронизации (delta_t)\n"
                    lines[101] = self.lineEdit_16.text() + " ; N_lab\n"
                    lines[106] = self.lineEdit_17.text() + " ; delaySync_lab\n"
                    lines[111] = str(self.comboBox_3.currentIndex()) + " ; peak_lab\n"
                elif self.comboBox_2.currentIndex() == 0:
                    lines[15] = self.lineEdit_12.text() + " ; сколько кадров пропускать при распознавании\n"
                lines[16] = self.lineEdit_15.text() + " ; запаздывание\n"
                lines[17] = self.lineEdit_14.text() + " ; усредненное\n"
                with open("settings.ini", "w") as file:
                    file.writelines(lines)
                self.label_16.setText("Изменения сохранены")
                self.update_data()
        except Exception as ex:
            print(ex)
    '''
    def onTextChanged(self, text):
        if text == ".":
            text
        if "-1" in self.lineEdit_7.text():
            self.lineEdit_7.setText('-1')
        elif "-1" in self.lineEdit_8.text():
            self.lineEdit_8.setText('-1')
        elif "-1" in self.lineEdit_9.text():
            self.lineEdit_9.setText('-1')
        elif "-" in self.lineEdit_7.text():
            if self.lineEdit_7.text() == '-':
                self.lineEdit_7.setText('-')
            else:
                self.lineEdit_7.setText('-1')
        elif "-" in self.lineEdit_8.text():
            if self.lineEdit_8.text() == '-':
                self.lineEdit_8.setText('-')
            else:
                self.lineEdit_8.setText('-1')
        elif "-" in self.lineEdit_9.text():
            if self.lineEdit_9.text() == '-':
                self.lineEdit_9.setText('-')
            else:
                self.lineEdit_9.setText('-1')
        self.label_16.setText("")
        if not all([
        self.lineEdit.text(),
        self.lineEdit_2.text(),
        self.lineEdit_3.text(),
        self.lineEdit_4.text(),
        self.lineEdit_5.text(),
        self.lineEdit_6.text(),
        self.lineEdit_7.text(),
        self.lineEdit_8.text(),
        self.lineEdit_9.text(),
        self.lineEdit_10.text(),
        self.lineEdit_11.text(),
        self.lineEdit_12.text()]) or ((self.lineEdit_13.text() == '' and self.lineEdit_16.text() == '' and self.lineEdit_17.text() == '') and self.comboBox_2.currentIndex() == 0):
            self.pushButton_6.setEnabled(False)
        else:
            self.pushButton_6.setEnabled(True)
    '''
    
    def onTextChanged(self, line_edit):
        try:
            line_edits = [
                self.lineEdit_10,
                self.lineEdit
            ]
            if line_edit not in line_edits:
                text = line_edit.text()
                if text:
                    if text == '.':
                        line_edit.setText('')
                    if text[0] == '0' and len(text) > 1 and text[1].isdigit():
                        line_edit.setText(text[1:])
                        
                    if text[0] == '0' and len(text) > 1 and text[1] == '0':
                        line_edit.setText(text[1:])
                    
                
                if '-1' in text:
                    line_edit.setText('-1')
                elif '-' in text:
                    if text == '-':
                        line_edit.setText('-')
                    else:
                        line_edit.setText('-')
            
            self.label_16.setText("")
            if not all([
            self.lineEdit.text(),
            self.lineEdit_2.text(),
            self.lineEdit_3.text(),
            self.lineEdit_4.text(),
            self.lineEdit_5.text(),
            self.lineEdit_6.text(),
            self.lineEdit_7.text(),
            self.lineEdit_8.text(),
            self.lineEdit_9.text(),
            self.lineEdit_10.text(),
            self.lineEdit_11.text(),
            self.lineEdit_15.text(),
            self.lineEdit_12.text()]) or ((self.lineEdit_13.text() == '' or self.lineEdit_16.text() == '' or self.lineEdit_17.text() == '') and self.comboBox_2.currentIndex() == 1):
                self.pushButton_6.setEnabled(False)
            else:
                self.pushButton_6.setEnabled(True)

            if self.lineEdit.text() == '' or self.lineEdit_2.text() == '':
                self.pushButton_2.setEnabled(False)
            else:
                self.pushButton_2.setEnabled(True)
        except Exception as ex:
            print(ex)

    def setLineEditValidator(self, lineEdit):
        regex = QRegularExpression(r'^[0-9][0-9]*$') 
        validator = QRegularExpressionValidator(regex, lineEdit)
        lineEdit.setValidator(validator)

    def setLineEditValidator2(self, lineEdit):
        regex = QRegularExpression(r'^[0-9][0-9 ]*$')
        validator = QRegularExpressionValidator(regex, lineEdit)
        lineEdit.setValidator(validator)

    def setLineEditValidator3(self, lineEdit):
        regex = QRegularExpression(r'^[0-9]*(\.[0-9]*)?$')  
        validator = QRegularExpressionValidator(regex, lineEdit)
        lineEdit.setValidator(validator)


    def update_data(self):
        data = functions.read_settings()
        self.lineEdit.setPlaceholderText(str(data['filePath']))
        self.lineEdit_2.setPlaceholderText(str(data['frameNumber']))
        self.lineEdit_3.setPlaceholderText(str(data['framesInterval']))
        self.lineEdit_4.setPlaceholderText(str(data['frame_count']))
        self.lineEdit_5.setPlaceholderText(str(data['min_bubble_area']))
        self.lineEdit_6.setPlaceholderText(str(data['max_bubble_area']))
        self.lineEdit_7.setPlaceholderText(str(data['koefBin']))
        self.lineEdit_8.setPlaceholderText(str(data['koefContrast']))
        self.lineEdit_9.setPlaceholderText(str(data['koefAntiGlare']))
        self.lineEdit_10.setPlaceholderText(str(data['windowCoords']))
        self.lineEdit_11.setPlaceholderText(str(data['pointsOnGraph']))
        if self.comboBox_2.currentIndex() == 1:
            self.lineEdit_12.setPlaceholderText(str(data['R']))
            self.lineEdit_13.setPlaceholderText(str(data['delta_t']))
            self.lineEdit_16.setPlaceholderText(str(data['N']))
            self.lineEdit_17.setPlaceholderText(str(data['delaySync']))
        elif self.comboBox_2.currentIndex() == 0:
            self.lineEdit_12.setPlaceholderText(str(data['skipFrames']))

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Меню настроек"))
        self.label_16.setText(_translate("Dialog", ""))
        self.pushButton_6.setText(_translate("Dialog", "Сохранить изменения"))
        self.pushButton_7.setText(_translate("Dialog", "Назад"))
        self.label_15.setText(_translate("Dialog", "Путь до файла / Порт камеры:"))
        self.label.setText(_translate("Dialog", "1. Номер кадра, с которого начинать обработку:"))
        self.label_2.setText(_translate("Dialog", "2. Мин. интервал между кадрами (в секундах):"))
        self.label_3.setText(_translate("Dialog", "3. Сколько кадров обрабатывать:"))
        self.label_4.setText(_translate("Dialog", "4. Мин. площадь пузырька (в пикселях):"))
        self.label_5.setText(_translate("Dialog", "5. Макс. площадь пузырька (в пикселях):"))
        self.label_6.setText(_translate("Dialog", "6. Коэффициент бинаризации:"))
        self.label_7.setText(_translate("Dialog", "7. Уровень контрастности:"))
        self.label_8.setText(_translate("Dialog", "8. Коэффициент антиблика:"))
        self.label_9.setText(_translate("Dialog", "9. Выделямая область: "))
        self.label_10.setText(_translate("Dialog", "- координаты:"))
        self.label_11.setText(_translate("Dialog", "10. Количество точек на графиках:"))
        self.label_17.setText(_translate("Dialog", "11. Запаздывание"))
        self.label_18.setText(_translate("Dialog", "12. Усредненное количество точек"))
        self.label_12.setText(_translate("Dialog", "13. Алгоритм синхронизации с пеногоном:"))
        self.label_13.setText(_translate("Dialog", "- на сколько делить: "))
        self.label_14.setText(_translate("Dialog", "- промежуток времени при синхронизации (Δt): "))
        self.label_19.setText(_translate("Dialog", "- количество отсчетов:"))
        self.label_20.setText(_translate("Dialog", "- запаздывание:"))
        self.label_21.setText(_translate("Dialog", "- нахождение точки синхронизации при:"))
        self.pushButton.setText(_translate("Dialog", "Выбрать файл"))
        self.pushButton_3.setText(_translate("Dialog", "Сбросить"))
        self.pushButton_4.setText(_translate("Dialog", "Сбросить"))
        self.pushButton_5.setText(_translate("Dialog", "Сбросить"))
        self.pushButton_8.setText(_translate("Dialog", "Сбросить"))
        self.pushButton_2.setText(_translate("Dialog", "Задать"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
