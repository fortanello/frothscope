from opcua import Client
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from functools import partial 
from settingsWindow import Ui_Dialog
from settingsWindowFactory import Ui_Dialog_Factory
from videoWorker import VideoWorker
from widgetDB import DatabaseWidget
import functions
import psycopg2


properties = functions.read_settings()
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class ConnectDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Подключение к OPC-серверу")
        self.setGeometry(100, 100, 300, 150)

        self.layout = QVBoxLayout()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_ip = QLabel("Введите IP-адрес:")
        self.layout.addWidget(self.label_ip)
        self.input_ip = QLineEdit(self)
        self.layout.addWidget(self.input_ip)

        self.label_port = QLabel("Введите порт:")
        self.layout.addWidget(self.label_port)
        self.input_port = QLineEdit(self)
        self.layout.addWidget(self.input_port)

        self.connect_button = QPushButton("Подключиться", self)
        self.connect_button.clicked.connect(self.connect_to_server)
        self.layout.addWidget(self.connect_button)
        
        self.connect_button.setFont(font)
        self.label_ip.setFont(font)
        self.label_port.setFont(font)
        self.input_port.setFont(font)
        self.input_ip.setFont(font)
        self.connect_button.setMinimumHeight(35)
        self.connect_button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))

        self.setLayout(self.layout)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def connect_to_server(self):
        ip = self.input_ip.text()
        port = self.input_port.text()


        if not port.isdigit():
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Critical)
            msg_box.setWindowTitle("Ошибка")
            msg_box.setText("Порт должен быть числом")

            font = QtGui.QFont()
            font.setPointSize(12)
            msg_box.setFont(font)
            msg_box.addButton("OK", QtWidgets.QMessageBox.AcceptRole)
            msg_box.exec_()
            return

        self.server_url = f"opc.tcp://{ip}:{port}/freeopcua/server/"

        
        self.client_thread = OPCClientThread(self.server_url) # Создаем поток для подключения
        self.client_thread.connected_signal.connect(self.on_connected)  
        self.client_thread.error_signal.connect(self.on_error)  
        self.client_thread.start()


        self.connect_button.setEnabled(False)
        self.connect_button.setText("Подключение...") 

    def on_connected(self):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setWindowTitle("Успешно")
        msg_box.setText("Подключение успешно")

        font = QtGui.QFont()
        font.setPointSize(12)
        msg_box.setFont(font)
        msg_box.addButton("OK", QtWidgets.QMessageBox.AcceptRole)
        msg_box.exec_()
        self.accept()  

        self.connect_button.setEnabled(True)
        self.connect_button.setText("Подключиться")

    def on_error(self, error_message):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Critical)
        msg_box.setWindowTitle("Ошибка подключения")
        msg_box.setText(f"Не удалось подключиться: {error_message}")

        font = QtGui.QFont()
        font.setPointSize(12)
        msg_box.setFont(font)
        msg_box.addButton("OK", QtWidgets.QMessageBox.AcceptRole)
        msg_box.exec_()
        #QMessageBox.critical(self, "Ошибка подключения", f"Не удалось подключиться: {error_message}")
        
        self.connect_button.setEnabled(True)
        self.connect_button.setText("Подключиться")

    


class OPCClientThread(QThread):
    update_signal = pyqtSignal(dict)
    connected_signal = pyqtSignal()
    error_signal = pyqtSignal(str)  # Сигнал для передачи ошибки

    def __init__(self, server_url):
        super().__init__()
        self.server_url = server_url
        self.client = Client(self.server_url)

    def run(self):
        try:
            self.client.connect()
            print(f"Connected to OPC-UA server at {self.server_url}")
            self.connected_signal.emit()
            
            while True:
                port_number1 = self.client.get_node("ns=2;i=2").get_value()
                bubble_count1_1 = self.client.get_node("ns=2;i=3").get_value()
                bubble_count1_2 = self.client.get_node("ns=2;i=4").get_value()
                avg_distance1_1 = self.client.get_node("ns=2;i=5").get_value()
                avg_distance1_2 = self.client.get_node("ns=2;i=6").get_value()
                median_distance1_1 = self.client.get_node("ns=2;i=7").get_value()
                median_distance1_2 = self.client.get_node("ns=2;i=8").get_value()
                red_component1 = self.client.get_node("ns=2;i=9").get_value()
                date1 = self.client.get_node("ns=2;i=10").get_value()

                port_number2 = self.client.get_node("ns=2;i=11").get_value()
                bubble_count2_1 = self.client.get_node("ns=2;i=12").get_value()
                bubble_count2_2 = self.client.get_node("ns=2;i=13").get_value()
                avg_distance2_1 = self.client.get_node("ns=2;i=14").get_value()
                avg_distance2_2 = self.client.get_node("ns=2;i=15").get_value()
                median_distance2_1 = self.client.get_node("ns=2;i=16").get_value()
                median_distance2_2 = self.client.get_node("ns=2;i=17").get_value()
                red_component2 = self.client.get_node("ns=2;i=18").get_value()
                date2 = self.client.get_node("ns=2;i=19").get_value()

                port_number3 = self.client.get_node("ns=2;i=20").get_value()
                bubble_count3_1 = self.client.get_node("ns=2;i=21").get_value()
                bubble_count3_2 = self.client.get_node("ns=2;i=22").get_value()
                avg_distance3_1 = self.client.get_node("ns=2;i=23").get_value()
                avg_distance3_2 = self.client.get_node("ns=2;i=24").get_value()
                median_distance3_1 = self.client.get_node("ns=2;i=25").get_value()
                median_distance3_2 = self.client.get_node("ns=2;i=26").get_value()
                red_component3 = self.client.get_node("ns=2;i=27").get_value()
                date3 = self.client.get_node("ns=2;i=28").get_value()

                port_number4 = self.client.get_node("ns=2;i=29").get_value()
                bubble_count4_1 = self.client.get_node("ns=2;i=30").get_value()
                bubble_count4_2 = self.client.get_node("ns=2;i=31").get_value()
                avg_distance4_1 = self.client.get_node("ns=2;i=32").get_value()
                avg_distance4_2 = self.client.get_node("ns=2;i=33").get_value()
                median_distance4_1 = self.client.get_node("ns=2;i=34").get_value()
                median_distance4_2 = self.client.get_node("ns=2;i=35").get_value()
                red_component4 = self.client.get_node("ns=2;i=36").get_value()
                date4 = self.client.get_node("ns=2;i=37").get_value()
                values = {
                    'port_number1': port_number1,
                    'bubble_count1_1': bubble_count1_1,
                    'bubble_count1_2': bubble_count1_2,
                    'avg_distance1_1': avg_distance1_1,
                    'avg_distance1_2': avg_distance1_2,
                    'median_distance1_1': median_distance1_1,
                    'median_distance1_2': median_distance1_2,
                    'red_component1': red_component1,
                    'date1': date1,

                    'port_number2': port_number2,
                    'bubble_count2_1': bubble_count2_1,
                    'bubble_count2_2': bubble_count2_2,
                    'avg_distance2_1': avg_distance2_1,
                    'avg_distance2_2': avg_distance2_2,
                    'median_distance2_1': median_distance2_1,
                    'median_distance2_2': median_distance2_2,
                    'red_component2': red_component2,
                    'date2': date2,

                    'port_number3': port_number3,
                    'bubble_count3_1': bubble_count3_1,
                    'bubble_count3_2': bubble_count3_2,
                    'avg_distance3_1': avg_distance3_1,
                    'avg_distance3_2': avg_distance3_2,
                    'median_distance3_1': median_distance3_1,
                    'median_distance3_2': median_distance3_2,
                    'red_component3': red_component3,
                    'date3': date3,

                    'port_number4': port_number4,
                    'bubble_count4_1': bubble_count4_1,
                    'bubble_count4_2': bubble_count4_2,
                    'avg_distance4_1': avg_distance4_1,
                    'avg_distance4_2': avg_distance4_2,
                    'median_distance4_1': median_distance4_1,
                    'median_distance4_2': median_distance4_2,
                    'red_component4': red_component4,
                    'date4': date4,
                }
                
                
                self.update_signal.emit(values)
                self.sleep(1)
            self.client.disconnect()
            
        except Exception as e:
            print(f"Error connecting to server: {e}")
            error_message = str(e)
            print('erer')
            self.error_signal.emit(error_message)
            
    def stop(self):
        self._running = False

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.main_window = Ui_MainWindow

    def clear_graph(self):
        self.axes.clear()
        self.draw() 

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1250, 860)
        MainWindow.setMinimumSize(1250, 860)
        
        if str(properties['mode']) == '1':
            self.toFactoryMode(1)
        else:
            self.toLabMode(1)
        
            


    def toLabMode(self, status1):
        self.conn = -1
        try:
            if self.client_thread is not None:
                self.client_thread.stop()  
                self.client_thread = None
        except Exception as ex:
            pass
        try:
            with open("settings.ini", "r") as file:
                lines = file.readlines()
            lines[18] = "0" + " ; режим\n"
            with open("settings.ini", "w") as file:
                file.writelines(lines)
            self.properties_general = functions.read_settings()
            if (status1 == 0):
                self.stop_all_workers()
                self.graphic1.clear_graph()
                self.graphic2.clear_graph()
                self.graphic3.clear_graph()
                self.graphic4.clear_graph()
                for i in reversed(range(self.gridLayout.count())): 
                    widget = self.gridLayout.itemAt(i).widget()
                    if widget is not None: 
                        widget.deleteLater()

            #############

            MainWindow.setObjectName("MainWindow")

            MainWindow.setStyleSheet("background-color: qlinegradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgb(81, 0, 135, 255), stop:0.427447 rgba(41, 61, 132, 235), stop: 1 rgba(155, 79, 165, 255));")
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setMinimumSize(QtCore.QSize(1250, 800))
            self.centralwidget.setStyleSheet("background-color: qlinegradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgb(240, 255, 255, 255), stop:0.427447 rgba(255, 255, 255, 255), stop: 1 rgba(255, 255, 255, 255));")
            self.centralwidget.setObjectName("centralwidget")
            self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
            self.gridLayout.setObjectName("gridLayout")

            self.binImg = QtWidgets.QGraphicsView(self.centralwidget)
            self.binImg.setMinimumSize(QtCore.QSize(0, 200))
            self.binImg.setMaximumSize(QtCore.QSize(500, 16777215))
            self.binImg.setObjectName("binImg")
            self.binImg.setStyleSheet("border: none;")
            self.gridLayout.addWidget(self.binImg, 2, 0, 2, 1)
            self.outputText = QtWidgets.QTextBrowser(self.centralwidget)
            self.outputText.setMinimumSize(QtCore.QSize(0, 0))
            self.outputText.setMaximumSize(QtCore.QSize(16777215, 90))
            self.outputText.setObjectName("outputText")
            self.outputText.setStyleSheet("border: none; font-size: 12pt;")
            self.gridLayout.addWidget(self.outputText, 4, 0, 1, 2)
            self.roi = QtWidgets.QGraphicsView(self.centralwidget)
            self.roi.setMinimumSize(QtCore.QSize(0, 200))
            self.roi.setMaximumSize(QtCore.QSize(500, 16777215))
            self.roi.setObjectName("roi")
            self.roi.setStyleSheet("border: none;")
            self.gridLayout.addWidget(self.roi, 1, 0, 1, 1)
            self.fileOrCamera = QtWidgets.QGraphicsView(self.centralwidget)
            self.fileOrCamera.setMinimumSize(QtCore.QSize(0, 300))
            self.fileOrCamera.setMaximumSize(QtCore.QSize(500, 16777215))
            self.fileOrCamera.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.fileOrCamera.setInteractive(True)
            self.fileOrCamera.setObjectName("fileOrCamera")
            self.fileOrCamera.setStyleSheet("border: none;")
            self.gridLayout.addWidget(self.fileOrCamera, 0, 0, 1, 1)
            
            
            self.graphic6 = MplCanvas(self, width=5, height=4, dpi=100)
            self.graphic6.setMinimumSize(QtCore.QSize(750, 200))
            self.graphic6.setObjectName("graphic2")
            self.gridLayout.addWidget(self.graphic6, 1, 1, 2, 3)
            self.graphic5 = MplCanvas(self, width=5, height=4, dpi=100)
            self.graphic5.customContextMenuRequested.connect(partial(self.show_diff_graphics, graphic=self.graphic5))
            self.graphic6.customContextMenuRequested.connect(partial(self.show_diff_graphics, graphic=self.graphic6))
            self.graphic5.setMinimumSize(QtCore.QSize(750, 200))
            self.graphic5.setObjectName("graphic5")
            self.gridLayout.addWidget(self.graphic5, 0, 1, 1, 3)
            
            self.gridLayout.addWidget(self.graphic6, 1, 1, 2, 3)
            
            self.textT = QtWidgets.QLabel(self.centralwidget)
            self.textT.setMaximumSize(QtCore.QSize(16777215, 100))
            font = QtGui.QFont()
            font.setPointSize(20)
            font.setBold(False)
            font.setWeight(50)
            self.textT.setFont(font)
            self.textT.setObjectName("textT")
            self.gridLayout.addWidget(self.textT, 3, 1, 1, 2)
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setMaximumSize(QtCore.QSize(90, 90))
            self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
            self.label.setObjectName("label")
            self.gridLayout.addWidget(self.label, 3, 3, 1, 1)

            
            self.btnStart = QtWidgets.QPushButton(self.centralwidget)
            self.btnStart.setMinimumSize(QtCore.QSize(250, 80))
            self.btnStart.setMaximumSize(QtCore.QSize(250, 90))
            font = QtGui.QFont()
            font.setPointSize(20)
            font.setBold(False)
            font.setWeight(50)
            self.btnStart.setFont(font)
            self.btnStart.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.btnStart.setObjectName("btnStart")
            self.gridLayout.addWidget(self.btnStart, 4, 2, 1, 1)
            self.btnStop = QtWidgets.QPushButton(self.centralwidget)
            self.btnStop.setMinimumSize(QtCore.QSize(250, 80))
            self.btnStop.setMaximumSize(QtCore.QSize(250, 90))
            self.btnStop.setFont(font)
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(False)
            font.setWeight(75)
            self.btnStop.setText("Стоп")
            self.btnStart.setText("Старт")
            
            
            self.btnStop.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.btnStop.setObjectName("btnStop")
            self.gridLayout.addWidget(self.btnStop, 4, 3, 1, 1)
            MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 1250, 21))
            self.menubar.setObjectName("menubar")
            self.menuSettings = QtWidgets.QMenu(self.menubar)
            self.menuSettings.setObjectName("menuSettings")
            MainWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)
            self.actionAbout = QtWidgets.QAction(MainWindow)
            self.actionAbout.setObjectName("actionAbout")
            self.actionSettings = QtWidgets.QAction(MainWindow)
            self.actionSettings.setObjectName("actionSettings")
            self.actionDB = QtWidgets.QAction(MainWindow)
            self.actionDB.setObjectName("actionDB")
            self.menuSettings.setStyleSheet("QMenu { font-size: 14px; }")
            self.menuSettings.addAction(self.actionSettings)
            self.menuSettings.addAction(self.actionAbout)
            self.menubar.addAction(self.menuSettings.menuAction())
            self.opcSettings = QtWidgets.QMenu(self.menubar)
            self.opcSettings.setObjectName("opcSettings")
            self.menubar.addAction(self.actionDB)
            self.menubar.setStyleSheet("QMenuBar { font-size: 14px; }")
            self.opcSettings.setStyleSheet("QMenu { font-size: 14px; }")
            #self.menubar.addAction(self.opcSettings.menuAction())
            self.actionOPC = QtWidgets.QAction(MainWindow)
            self.actionOPC.setObjectName("actionOPC")
            self.actionOPC2 = QtWidgets.QAction(MainWindow)
            self.actionOPC2.setObjectName("actionOPC2")
            self.retranslateUi(MainWindow)
            
    
            self.actionDB.triggered.connect(self.toDBWindow)
            self.btnStart.clicked.connect(self.playVideo)
            self.actionSettings.triggered.connect(self.settingsWindow)
            self.actionAbout.triggered.connect(partial(self.toFactoryMode, status1=0))
            
            self.btnStop.clicked.connect(self.stopProgram)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

            self.idxGraph1 = 0
            self.idxGraph2 = 0            
            self.framesArray = []
            self.framesProcessedArray = []
            self.bubblesBeforeArray = []
            self.bubblesAfterArray = []
            self.avgBeforeArray = []
            self.avgAfterArray = []
            self.medianBeforeArray = []
            self.medianAfterArray = []
            self.red_pixelsArray = []

            self.video_workers = []
            self.idxGraph1 = 0
            self.idxGraph2 = 0

            self.idxsGraph = {
                '1': 0,
                '2': 0
            }
            self.video_data = {
                '0': {
                    'framesProcessedArray': [],
                    'bubblesBeforeArray': [],
                    'bubblesAfterArray': [],
                    'avgBeforeArray': [],
                    'avgAfterArray': [],
                    'medianBeforeArray': [],
                    'medianAfterArray': [],
                    'red_pixelsArray': [],
                    'framesArray': [],
                    'koefBin_values': [],
                    'koefBin_values2': [],
                    'koefContrast_values': [],
                    'koefAntiGlare_values': [],
                    'pointsOnGraph': 0
                }
            }
        except Exception as e:
            print(e)
        
    
            
    def toFactoryMode(self, status1):
        try:
            with open("settings.ini", "r") as file:
                lines = file.readlines()
            lines[18] = "1" + " ; режим\n"
            with open("settings.ini", "w") as file:
                file.writelines(lines)
            self.properties_general = functions.read_settings()
            if status1 == 0:
                self.stop_all_workers()
                self.graphic5.clear_graph()
                self.graphic6.clear_graph()
                for i in reversed(range(self.gridLayout.count())): 
                    widget = self.gridLayout.itemAt(i).widget()
                    if widget is not None: 
                        widget.deleteLater()
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
            self.gridLayout_5.setObjectName("gridLayout_5")
            self.gridLayout = QtWidgets.QGridLayout()
            self.gridLayout.setObjectName("gridLayout")
            self.splitter = QtWidgets.QSplitter(self.centralwidget)
            self.splitter.setOrientation(QtCore.Qt.Vertical)
            self.splitter.setObjectName("splitter")
            self.graphicsView = QtWidgets.QGraphicsView(self.splitter)
            self.graphicsView.setMaximumSize(QtCore.QSize(16777215, 160))
            self.graphicsView.setObjectName("graphicsView")
            self.graphicsView.setStyleSheet("border: none;")
            self.graphicsView.setMinimumSize(QtCore.QSize(140, 0))
            self.label = QtWidgets.QLabel(self.splitter)
            self.label.setMinimumSize(QtCore.QSize(207, 231))
            self.label.setBaseSize(QtCore.QSize(0, 0))
            self.label.setText("")
            self.label.setScaledContents(True)
            self.label.setStyleSheet("background-color: white;")
            self.label.setObjectName("label")
            self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
            self.verticalLayout = QtWidgets.QVBoxLayout()
            self.verticalLayout.setObjectName("verticalLayout")
            self.graphic1 = MplCanvas(self, width=3, height=2, dpi=100)
            self.graphic1.setMinimumSize(QtCore.QSize(400, 170))
            self.graphic1.setMaximumSize(QtCore.QSize(686, 348))
            self.graphic1.setObjectName("graphic1")
            self.verticalLayout.addWidget(self.graphic1)
            self.graphic1.customContextMenuRequested.connect(lambda pos: self.show_diff_graphics(pos, self.graphic1))  
            self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
            self.textBrowser.setMaximumSize(QtCore.QSize(686, 120))
            self.textBrowser.setObjectName("textBrowser")
            self.textBrowser.setStyleSheet("border: none;")
            self.verticalLayout.addWidget(self.textBrowser)
            self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
            self.gridLayout_5.addLayout(self.gridLayout, 0, 0, 1, 1)
            self.gridLayout_2 = QtWidgets.QGridLayout()
            self.gridLayout_2.setObjectName("gridLayout_2")
            self.verticalLayout_2 = QtWidgets.QVBoxLayout()
            self.verticalLayout_2.setObjectName("verticalLayout_2")
            self.graphic2 = MplCanvas(self, width=3, height=2, dpi=100)
            self.graphic2.setMinimumSize(QtCore.QSize(400, 170))
            self.graphic2.setMaximumSize(QtCore.QSize(686, 348))
            self.graphic2.setObjectName("graphic2")
            self.verticalLayout_2.addWidget(self.graphic2)
            self.graphic2.customContextMenuRequested.connect(lambda pos: self.show_diff_graphics(pos, self.graphic2))
            self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
            self.textBrowser_2.setMaximumSize(QtCore.QSize(686, 120))
            self.textBrowser_2.setObjectName("textBrowser_2")
            self.textBrowser_2.setStyleSheet("border: none;")
            self.verticalLayout_2.addWidget(self.textBrowser_2)
            self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
            self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
            self.splitter_2.setOrientation(QtCore.Qt.Vertical)
            self.splitter_2.setObjectName("splitter_2")
            self.graphicsView_3 = QtWidgets.QGraphicsView(self.splitter_2)
            self.graphicsView_3.setMaximumSize(QtCore.QSize(16777215, 160))
            self.graphicsView_3.setObjectName("graphicsView_3")
            self.graphicsView_3.setStyleSheet("border: none;")
            self.label_2 = QtWidgets.QLabel(self.splitter_2)
            self.label_2.setMinimumSize(QtCore.QSize(207, 231))
            self.label_2.setText("")
            self.label_2.setScaledContents(True)
            self.label_2.setStyleSheet("background-color: white;")
            self.label_2.setObjectName("label_2")
            self.gridLayout_2.addWidget(self.splitter_2, 0, 0, 1, 1)
            self.gridLayout_5.addLayout(self.gridLayout_2, 0, 1, 1, 1)
            self.gridLayout_4 = QtWidgets.QGridLayout()
            self.gridLayout_4.setObjectName("gridLayout_4")
            self.splitter_4 = QtWidgets.QSplitter(self.centralwidget)
            self.splitter_4.setOrientation(QtCore.Qt.Vertical)
            self.splitter_4.setObjectName("splitter_4")
            self.graphicsView_10 = QtWidgets.QGraphicsView(self.splitter_4)
            self.graphicsView_10.setMaximumSize(QtCore.QSize(16777215, 160))
            self.graphicsView_10.setObjectName("graphicsView_10")
            self.graphicsView_10.setStyleSheet("border: none;")
            self.label_3 = QtWidgets.QLabel(self.splitter_4)
            self.label_3.setMinimumSize(QtCore.QSize(207, 231))
            self.label_3.setText("")
            self.label_3.setScaledContents(True)
            self.label_3.setStyleSheet("background-color: white;")
            self.label_3.setObjectName("label_3")
            self.gridLayout_4.addWidget(self.splitter_4, 0, 0, 1, 1)
            self.verticalLayout_4 = QtWidgets.QVBoxLayout()
            self.verticalLayout_4.setObjectName("verticalLayout_4")
            self.graphic3 = MplCanvas(self, width=3, height=2, dpi=100)
            self.graphic3.setMinimumSize(QtCore.QSize(400, 170))
            self.graphic3.setMaximumSize(QtCore.QSize(686, 348))
            self.graphic3.setObjectName("graphic3")
            self.verticalLayout_4.addWidget(self.graphic3)
            self.graphic3.customContextMenuRequested.connect(lambda pos: self.show_diff_graphics(pos, self.graphic3))
            self.textBrowser_4 = QtWidgets.QTextBrowser(self.centralwidget)
            self.textBrowser_4.setMaximumSize(QtCore.QSize(686, 120))
            self.textBrowser_4.setMinimumSize(QtCore.QSize(300, 0))
            self.textBrowser_4.setObjectName("textBrowser_4")
            self.textBrowser_4.setStyleSheet("border: none;")
            self.verticalLayout_4.addWidget(self.textBrowser_4)
            self.gridLayout_4.addLayout(self.verticalLayout_4, 0, 1, 1, 1)
            self.gridLayout_5.addLayout(self.gridLayout_4, 1, 0, 1, 1)
            self.gridLayout_3 = QtWidgets.QGridLayout()
            self.gridLayout_3.setObjectName("gridLayout_3")
            self.splitter_3 = QtWidgets.QSplitter(self.centralwidget)
            self.splitter_3.setOrientation(QtCore.Qt.Vertical)
            self.splitter_3.setObjectName("splitter_3")
            self.graphicsView_7 = QtWidgets.QGraphicsView(self.splitter_3)
            self.graphicsView_7.setMaximumSize(QtCore.QSize(16777215, 160))
            self.graphicsView_7.setObjectName("graphicsView_7")
            self.graphicsView_7.setStyleSheet("border: none;")
            self.label_4 = QtWidgets.QLabel(self.splitter_3)
            self.label_4.setMinimumSize(QtCore.QSize(207, 231))
            self.label_4.setText("")
            self.label_4.setScaledContents(True)
            self.label_4.setStyleSheet("background-color: white;")
            self.label_4.setObjectName("label_4")
            self.gridLayout_3.addWidget(self.splitter_3, 0, 0, 1, 1)
            self.verticalLayout_3 = QtWidgets.QVBoxLayout()
            self.verticalLayout_3.setObjectName("verticalLayout_3")
            self.graphic4 = MplCanvas(self, width=3, height=2, dpi=100)
            self.graphic4.setMinimumSize(QtCore.QSize(400, 170))
            self.graphic4.setMaximumSize(QtCore.QSize(686, 348))
            self.graphic4.setObjectName("graphic4")
            self.verticalLayout_3.addWidget(self.graphic4)
            self.graphic4.customContextMenuRequested.connect(partial(self.show_diff_graphics, graphic=self.graphic4))
            self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
            self.textBrowser_3.setMaximumSize(QtCore.QSize(686, 120))
            self.textBrowser_3.setObjectName("textBrowser_3")
            self.textBrowser_3.setStyleSheet("border: none;")
            self.verticalLayout_3.addWidget(self.textBrowser_3)
            self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
            self.gridLayout_5.addLayout(self.gridLayout_3, 1, 1, 1, 1)

            

            MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 1250, 21))
            self.menubar.setStyleSheet("QMenuBar { font-size: 14px; }")
            self.menubar.setObjectName("menubar")
            self.menuSettings = QtWidgets.QMenu(self.menubar)
            self.menuSettings.setObjectName("menuSettings")
            self.opcSettings = QtWidgets.QMenu(self.menubar)
            self.opcSettings.setObjectName("opcSettings")
            MainWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)
            self.actionAbout = QtWidgets.QAction(MainWindow)
            self.actionAbout.setObjectName("actionAbout")
            self.actionSettings = QtWidgets.QAction(MainWindow)
            self.actionSettings.setObjectName("actionSettings")
            self.actionDB = QtWidgets.QAction(MainWindow)
            self.actionDB.setObjectName("actionDB")
            self.actionOPC = QtWidgets.QAction(MainWindow)
            self.actionOPC.setObjectName("actionOPC")
            self.actionOPC2 = QtWidgets.QAction(MainWindow)
            self.actionOPC2.setObjectName("actionOPC2")
            self.menuSettings.setStyleSheet("QMenu { font-size: 14px; }")
            self.opcSettings.setStyleSheet("QMenu { font-size: 14px; }")
            
            self.menuSettings.addAction(self.actionSettings)
            self.menuSettings.addAction(self.actionAbout)
            self.opcSettings.addAction(self.actionOPC)
            self.opcSettings.addAction(self.actionOPC2)
            
            self.menubar.addAction(self.menuSettings.menuAction())
            self.menubar.addAction(self.actionDB)
            self.menubar.addAction(self.opcSettings.menuAction())
            #self.menubar.addAction(self.actionOPC)
            
            
            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

            font = QtGui.QFont()
            font.setPointSize(11)
            #font.setWeight(75)
            self.textBrowser_4.setFont(font)
            self.textBrowser_3.setFont(font)
            self.textBrowser_2.setFont(font)
            self.textBrowser.setFont(font)
            
            self.actionAbout.triggered.connect(partial(self.toLabMode, status1=0))
            self.actionSettings.triggered.connect(self.settingsWindowFactory)
            self.actionDB.triggered.connect(self.toDBWindow)
            self.actionOPC.triggered.connect(self.toOPCServer)
            self.actionOPC2.triggered.connect(self.disconnectOPC)
            self.video_workers = []
            self.idxGraph1 = 0
            self.idxGraph2 = 0
            self.idxGraph3 = 0
            self.idxGraph4 = 0

            self.idxGraph1 = 0
            self.idxGraph2 = 0            
            self.framesArray = []
            self.framesProcessedArray = []
            self.bubblesBeforeArray = []
            self.bubblesAfterArray = []
            self.avgBeforeArray = []
            self.avgAfterArray = []
            self.medianBeforeArray = []
            self.medianAfterArray = []
            self.red_pixelsArray = []

            self.numberThread = 0
            self.client_thread = None
            self.client_bool = False

            self.movie1 = QtGui.QMovie("alarm.gif")
            self.movie2 = QtGui.QMovie("alarm.gif")
            self.movie3 = QtGui.QMovie("alarm.gif")
            self.movie4 = QtGui.QMovie("alarm.gif")

            self.idxsGraph = {
                '1': 0,
                '2': 0,
                '3': 0,
                '4': 0
            }
            self.video_data = {
                '1': {
                    'framesProcessedArray': [],
                    'bubblesBeforeArray': [],
                    'bubblesAfterArray': [],
                    'avgBeforeArray': [],
                    'avgAfterArray': [],
                    'medianBeforeArray': [],
                    'medianAfterArray': [],
                    'red_pixelsArray': [],
                    'framesArray': [],
                    'pointsOnGraph': 0
                },
                '2': {
                    'framesProcessedArray': [],
                    'bubblesBeforeArray': [],
                    'bubblesAfterArray': [],
                    'avgBeforeArray': [],
                    'avgAfterArray': [],
                    'medianBeforeArray': [],
                    'medianAfterArray': [],
                    'red_pixelsArray': [],
                    'framesArray': [],
                    'pointsOnGraph': 0
                },
                '3': {
                    'framesProcessedArray': [],
                    'bubblesBeforeArray': [],
                    'bubblesAfterArray': [],
                    'avgBeforeArray': [],
                    'avgAfterArray': [],
                    'medianBeforeArray': [],
                    'medianAfterArray': [],
                    'red_pixelsArray': [],
                    'framesArray': [],
                    'pointsOnGraph': 0
                },
                '4': {
                    'framesProcessedArray': [],
                    'bubblesBeforeArray': [],
                    'bubblesAfterArray': [],
                    'avgBeforeArray': [],
                    'avgAfterArray': [],
                    'medianBeforeArray': [],
                    'medianAfterArray': [],
                    'red_pixelsArray': [],
                    'framesArray': [],
                    'pointsOnGraph': 0
                }
            }
            try:
                self.conn = psycopg2.connect(
                        dbname="foams",
                        user="postgres",
                        password="root",
                        host="localhost"
                    )
            except Exception:
                QtWidgets.QMessageBox.information(MainWindow, "Ошибка подключения", "Не удалось подключиться к базе данных")
                self.conn = -1
            data = functions.read_settings_factory()
            if str(data['fullStatus']) == 'True':
                self.factoryVideos()
        except Exception as e:
            print(e)
            

    def factoryVideos(self):
        try:
            
            cnt = 0
            video_files = []
            windowCoordsArray = []
            min_bubble_areaArray = []
            max_bubble_areaArray = []
            framesIntervalArray = []
            delta_tArray = []
            R_Array = []
            textBoxes = []
            threads = []
            graphics_view = []
            graphic = []
            #graphics_view_alarm = []
            sync_array = []
            skipFrames_array = []
            properties = functions.read_settings_factory()
            delay_array = []
            usr_array = []
            T_array = []
            pogr_array = []
            coordsMode_array = []

            N = []
            delaySync = []
            peak = []
                
            if str(properties['status']) == 'True':
                file_path1 = str(properties['filePath'])
                video_files.append(file_path1)
                graphics_view.append(self.graphicsView)
                graphic.append(self.graphic1)
                windowCoords1 = properties['windowCoords']
                windowCoordsArray.append(windowCoords1)
                min_bubble_area1 = properties['min_bubble_area']
                min_bubble_areaArray.append(min_bubble_area1)
                max_bubble_area1 = properties['max_bubble_area']
                max_bubble_areaArray.append(max_bubble_area1)
                framesInterval1 = properties['framesInterval']
                framesIntervalArray.append(framesInterval1)
                delta_t1 = properties['delta_t']
                delta_tArray.append(delta_t1)
                R1 = properties['R']
                R_Array.append(R1)
                sync_array.append(properties['syncMode'])
                skipFrames_array.append(properties['skipFrames'])
                delay_array.append(properties['delay'])
                usr_array.append(properties['usr'])
                T_array.append(properties['T'])
                pogr_array.append(properties['pogr'])
                coordsMode_array.append(properties['selectedAreaMode'])
                N.append(int(properties['N']))
                delaySync.append(int(properties['delaySync']))
                peak.append(properties['peak'])
                #graphics_view_alarm.append(self.graphicsView_4)
                textBoxes.append(self.textBrowser)
                threads.append(1)
                cnt += 1

            if str(properties['status_2']) == 'True':
                file_path2 = str(properties['filePath_2'])
                video_files.append(file_path2)
                graphics_view.append(self.graphicsView_3)
                graphic.append(self.graphic2)
                windowCoords2 = properties['windowCoords_2']
                windowCoordsArray.append(windowCoords2)
                min_bubble_area2 = properties['min_bubble_area_2']
                min_bubble_areaArray.append(min_bubble_area2)
                max_bubble_area2 = properties['max_bubble_area_2']
                max_bubble_areaArray.append(max_bubble_area2)
                framesInterval2 = properties['framesInterval_2']
                framesIntervalArray.append(framesInterval2)
                delta_t2 = properties['delta_t_2']
                delta_tArray.append(delta_t2)
                R2 = properties['R_2']
                R_Array.append(R2)
                sync_array.append(properties['syncMode_2'])
                skipFrames_array.append(properties['skipFrames_2'])
                delay_array.append(properties['delay_2'])
                usr_array.append(properties['usr_2'])
                T_array.append(properties['T_2'])
                pogr_array.append(properties['pogr_2'])
                coordsMode_array.append(properties['selectedAreaMode_2'])
                N.append(int(properties['N_2']))
                delaySync.append(int(properties['delaySync_2']))
                peak.append(properties['peak_2'])
                #graphics_view_alarm.append(self.graphicsView_5)
                textBoxes.append(self.textBrowser_2)
                threads.append(2)
                cnt += 1
            if str(properties['status_3']) == 'True':
                file_path3 = str(properties['filePath_3'])
                video_files.append(file_path3)
                graphics_view.append(self.graphicsView_10)
                graphic.append(self.graphic3)
                windowCoords3 = properties['windowCoords_3']
                windowCoordsArray.append(windowCoords3)
                min_bubble_area3 = properties['min_bubble_area_3']
                min_bubble_areaArray.append(min_bubble_area3)
                max_bubble_area3 = properties['max_bubble_area_3']
                max_bubble_areaArray.append(max_bubble_area3)
                framesInterval3 = properties['framesInterval_3']
                framesIntervalArray.append(framesInterval3)
                delta_t3 = properties['delta_t_3']
                delta_tArray.append(delta_t3)
                R3 = properties['R_3']
                R_Array.append(R3)
                sync_array.append(properties['syncMode_3'])
                skipFrames_array.append(properties['skipFrames_3'])
                delay_array.append(properties['delay_3'])
                usr_array.append(properties['usr_3'])
                T_array.append(properties['T_3'])
                pogr_array.append(properties['pogr_3'])
                coordsMode_array.append(properties['selectedAreaMode_3'])
                N.append(int(properties['N_3']))
                delaySync.append(int(properties['delaySync_3']))
                peak.append(properties['peak_3'])
                #graphics_view_alarm.append(self.graphicsView_11)
                textBoxes.append(self.textBrowser_4)
                threads.append(3)
                cnt += 1
            if str(properties['status_4']) == 'True':
                file_path4 = str(properties['filePath_4'])
                video_files.append(file_path4)
                graphics_view.append(self.graphicsView_7)
                graphic.append(self.graphic4)
                windowCoords4 = properties['windowCoords_4']
                windowCoordsArray.append(windowCoords4)
                min_bubble_area4 = properties['min_bubble_area_4']
                min_bubble_areaArray.append(min_bubble_area4)
                max_bubble_area4 = properties['max_bubble_area_4']
                max_bubble_areaArray.append(max_bubble_area4)
                framesInterval4 = properties['framesInterval_4']
                framesIntervalArray.append(framesInterval4)
                delta_t4 = properties['delta_t_4']
                delta_tArray.append(delta_t4)
                R4 = properties['R_4']
                R_Array.append(R4)
                sync_array.append(properties['syncMode_4'])
                skipFrames_array.append(properties['skipFrames_4'])
                delay_array.append(properties['delay_4'])
                usr_array.append(properties['usr_4'])
                T_array.append(properties['T_4'])
                pogr_array.append(properties['pogr_4'])
                coordsMode_array.append(properties['selectedAreaMode_4'])
                N.append(int(properties['N_4']))
                delaySync.append(int(properties['delaySync_4']))
                peak.append(properties['peak_4'])
                #graphics_view_alarm.append(self.graphicsView_8)
                textBoxes.append(self.textBrowser_3)
                threads.append(4)
                cnt += 1

            for i in range(cnt):
                file_path = video_files[i]
                windowCoords = windowCoordsArray[i]
                min_bubble_area = min_bubble_areaArray[i]
                max_bubble_area = max_bubble_areaArray[i]
                framesInterval = framesIntervalArray[i]
                delta_t = delta_tArray[i]
                R = R_Array[i]
                sync_mode = sync_array[i]
                skipFrames = skipFrames_array[i]
                delay = delay_array[i]
                usr = usr_array[i]
                T = T_array[i]
                pogr = pogr_array[i]
                coordsMode = coordsMode_array[i]
                worker = VideoWorker(file_path, windowCoords, min_bubble_area, max_bubble_area, framesInterval, delta_t, R, threads[i], graphic[i], graphics_view[i], 'Factory', -1, -1, -1, -1, graphics_view[i], textBoxes[i], self.conn, sync_mode, skipFrames, delay, usr, T, pogr, coordsMode, N[i], delaySync[i], peak[i])
                worker.frame_processed.connect(self.updateGraphicsView)
                worker.list_processed.connect(self.appendText)
                worker.graphic_processed.connect(self.updateGraphicFromWorker)
                worker.opc_data_updated.connect(self.update_opc_data)
                worker.alarm_started.connect(self.set_alarm)
                worker.alarm_finished.connect(self.unset_alarm)
                
                self.video_workers.append(worker)
                worker.start()
        except Exception as e:
            print(e)
            
    def set_alarm(self, numberThread):
        try:
            match numberThread:
                case 1:
                    if self.movie1.state() == QtGui.QMovie.NotRunning:
                        self.label.setMovie(self.movie1)
                        self.movie1.start()
                case 2:
                    if self.movie2.state() == QtGui.QMovie.NotRunning:
                        self.label_2.setMovie(self.movie2)
                        self.movie2.start()
                case 3:
                    if self.movie3.state() == QtGui.QMovie.NotRunning:
                        self.label_3.setMovie(self.movie3)
                        self.movie3.start()
                case 4:
                    if self.movie4.state() == QtGui.QMovie.NotRunning:
                        self.label_4.setMovie(self.movie4)
                        self.movie4.start()
        except Exception as ex:
            print(ex)

    def unset_alarm(self, numberThread):
        try:
            match numberThread:
                case 1:
                    self.movie1.stop()
                    self.label.clear()
                case 2:
                    self.movie2.stop()
                    self.label_2.clear()
                case 3:
                    self.movie3.stop()
                    self.label_3.clear()
                case 4:
                    self.movie4.stop()
                    self.label_4.clear()
        except Exception:
            pass
        
                
    def update_opc_data(self, values, numberThread):
        try:
            #print(numberThread)
            
            if self.client_thread != None:
                match numberThread:
                    case 1:
                        self.client_thread.client.get_node("ns=2;i=2").set_value(values['port_number1'])
                        self.client_thread.client.get_node("ns=2;i=3").set_value(values['bubble_count1_1'])
                        self.client_thread.client.get_node("ns=2;i=4").set_value(values['bubble_count1_2'])
                        self.client_thread.client.get_node("ns=2;i=5").set_value(values['avg_distance1_1'])
                        self.client_thread.client.get_node("ns=2;i=6").set_value(values['avg_distance1_2'])
                        self.client_thread.client.get_node("ns=2;i=7").set_value(values['median_distance1_1'])
                        self.client_thread.client.get_node("ns=2;i=8").set_value(values['median_distance1_2'])
                        self.client_thread.client.get_node("ns=2;i=9").set_value(values['red_component1'])
                        self.client_thread.client.get_node("ns=2;i=10").set_value(values['date1'])
                    case 2:
                        self.client_thread.client.get_node("ns=2;i=11").set_value(values['port_number2'])
                        self.client_thread.client.get_node("ns=2;i=12").set_value(values['bubble_count2_1'])
                        self.client_thread.client.get_node("ns=2;i=13").set_value(values['bubble_count2_2'])
                        self.client_thread.client.get_node("ns=2;i=14").set_value(values['avg_distance2_1'])
                        self.client_thread.client.get_node("ns=2;i=15").set_value(values['avg_distance2_2'])
                        self.client_thread.client.get_node("ns=2;i=16").set_value(values['median_distance2_1'])
                        self.client_thread.client.get_node("ns=2;i=17").set_value(values['median_distance2_2'])
                        self.client_thread.client.get_node("ns=2;i=18").set_value(values['red_component2'])
                        self.client_thread.client.get_node("ns=2;i=19").set_value(values['date2'])
                    case 3:
                        self.client_thread.client.get_node("ns=2;i=20").set_value(values['port_number3'])
                        self.client_thread.client.get_node("ns=2;i=21").set_value(values['bubble_count3_1'])
                        self.client_thread.client.get_node("ns=2;i=22").set_value(values['bubble_count3_2'])
                        self.client_thread.client.get_node("ns=2;i=23").set_value(values['avg_distance3_1'])
                        self.client_thread.client.get_node("ns=2;i=24").set_value(values['avg_distance3_2'])
                        self.client_thread.client.get_node("ns=2;i=25").set_value(values['median_distance3_1'])
                        self.client_thread.client.get_node("ns=2;i=26").set_value(values['median_distance3_2'])
                        self.client_thread.client.get_node("ns=2;i=27").set_value(values['red_component3'])
                        self.client_thread.client.get_node("ns=2;i=28").set_value(values['date3'])
                    case 4:
                        self.client_thread.client.get_node("ns=2;i=29").set_value(values['port_number4'])
                        self.client_thread.client.get_node("ns=2;i=30").set_value(values['bubble_count4_1'])
                        self.client_thread.client.get_node("ns=2;i=31").set_value(values['bubble_count4_2'])
                        self.client_thread.client.get_node("ns=2;i=32").set_value(values['avg_distance4_1'])
                        self.client_thread.client.get_node("ns=2;i=33").set_value(values['avg_distance4_2'])
                        self.client_thread.client.get_node("ns=2;i=34").set_value(values['median_distance4_1'])
                        self.client_thread.client.get_node("ns=2;i=35").set_value(values['median_distance4_2'])
                        self.client_thread.client.get_node("ns=2;i=36").set_value(values['red_component4'])
                        self.client_thread.client.get_node("ns=2;i=37").set_value(values['date4'])
        except Exception as ex:
            print(ex)
    def stop_all_workers(self):
        for worker in self.video_workers:
            worker.stop()
            worker.wait()
            
    def appendText(self, text, textBox):
        textBox.append(text)

    def appendT(self, text):
        #self.textT.setText("T = ", text)
        if text != 'None':
            str1 = 'T = '
            str1 += str(round(float(text), 2))
            self.textT.setText(str1)
        
    def show_gif(self):
        self.movie = QtGui.QMovie("loading.gif")
        #print('show')
        self.label.setMovie(self.movie)
        self.label.setScaledContents(True)
        self.movie.start()
        self.label.show()
    def hide_gif(self):
        self.label.hide()
        self.movie.stop()
        
    
    def updateGraphicsView(self, pixmap, graphics_view):
        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(pixmap)
        graphics_view.setScene(scene)

    def updateGraphicFromWorker(self, graphic, numberThread, data):
        try:
            self.video_data[str(numberThread)]['framesProcessedArray'] = data[0]
            self.video_data[str(numberThread)]['bubblesBeforeArray'] = data[1]
            self.video_data[str(numberThread)]['bubblesAfterArray'] = data[2]
            self.video_data[str(numberThread)]['avgBeforeArray'] = data[3]
            self.video_data[str(numberThread)]['avgAfterArray'] = data[4]
            self.video_data[str(numberThread)]['medianBeforeArray'] = data[5]
            self.video_data[str(numberThread)]['medianAfterArray'] = data[6]
            self.video_data[str(numberThread)]['red_pixelsArray'] = data[7]
            self.video_data[str(numberThread)]['framesArray'] = data[8]
            if numberThread == 0:
                data1 = functions.read_settings()
                self.video_data[str(numberThread)]['pointsOnGraph'] = data1['pointsOnGraph']
                self.video_data[str(numberThread)]['koefBin_values'] = data[9]
                self.video_data[str(numberThread)]['koefBin_values2'] = data[10]
                self.video_data[str(numberThread)]['koefContrast_values'] = data[11]
                self.video_data[str(numberThread)]['koefAntiGlare_values'] = data[12]
            else:
                data1 = functions.read_settings_factory()
                match numberThread:
                    case 1:
                        self.video_data[str(numberThread)]['pointsOnGraph'] = data1['pointsOnGraph']
                    case 2:
                        self.video_data[str(numberThread)]['pointsOnGraph'] = data1['pointsOnGraph_2']
                    case 3:
                        self.video_data[str(numberThread)]['pointsOnGraph'] = data1['pointsOnGraph_3']
                    case 4:
                        self.video_data[str(numberThread)]['pointsOnGraph'] = data1['pointsOnGraph_4']
                
            self.update_graphic(graphic, numberThread)
            
            
        except Exception as e:
            print(e)
            

    def closeEvent(self, event):
        for worker in self.video_workers:
            worker.stop()
            worker.wait()  # Wait for the thread to finish
        super().closeEvent(event)

    def stop_all_workers(self):
        for worker in self.video_workers:
            worker.stop()
            worker.wait()

    def show_diff_graphics(self, pos, graphic):
        try:
            menu = QtWidgets.QMenu(self.centralwidget)
            font = QtGui.QFont()
            font.setPointSize(11)
            
            menu.setFont(font)
            elements = ['Количество пузырьков', 'Среднее арифметическое расстояние', 'Среднее медианное расстояние', 'Красная компонента']
            
            for i, element in enumerate(elements): 
                action = QtWidgets.QAction(element, menu)
                action.triggered.connect(lambda checked, index=i, graphic=graphic: self.item_selected(index, graphic))
                menu.addAction(action)
                
            if str(self.properties_general['mode']) == '0':
                profiles_menu = menu.addMenu("Профили")
                profiles_elements = ['Бинаризация', 'Антиблик', 'Контраст']
                #profiles_menu.setFont(font)
                start_index = len(elements)
                for j, profile in enumerate(profiles_elements):
                    action = QtWidgets.QAction(profile, profiles_menu)
                    action.triggered.connect(lambda checked, index=start_index + j, graphic=graphic: self.item_selected(index, graphic))
                    profiles_menu.addAction(action)
                    action.setFont(font)
            
            menu.exec_(graphic.mapToGlobal(pos))
        except Exception as e:
            print(e)

    def item_selected(self, index, graphic):
        #print(index)
        try:
           
           if str(self.properties_general['mode']) == '1':
               match graphic:
                   case self.graphic1:
                       self.numberThread = 1
                   case self.graphic2:
                       self.numberThread = 2
                   case self.graphic3:
                       self.numberThread = 3
                   case self.graphic4:
                       self.numberThread = 4
               self.idxsGraph[str(self.numberThread)] = index
           else:
               self.numberThread = 0
               match graphic:
                   case self.graphic5:
                       self.idxGraph1 = index
                   case self.graphic6:
                       self.idxGraph2 = index
           self.update_graphic(graphic, self.numberThread)
        
        except Exception as e:
           print(e)  
        
    def settingsWindow(self):
        try:
            for worker in self.video_workers:
                worker.pause()
            self.isStopped = False
            Dialog = QtWidgets.QDialog()
            ui = Ui_Dialog()
            ui.setupUi(Dialog)
            Dialog.finished.connect(lambda: self.resumeWorkers())
            Dialog.exec_()
        except Exception as e:
            print(e)

    def disconnectOPC(self):
        try:
            self.client_thread.stop()  
            self.client_thread = None

            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Information)
            msg_box.setWindowTitle("Успешно")
            msg_box.setText("Вы отключились от OPC-сервера")

            font = QtGui.QFont()
            font.setPointSize(12)
            msg_box.setFont(font)
            msg_box.addButton("OK", QtWidgets.QMessageBox.AcceptRole)
            msg_box.exec_()
        except Exception as ex:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Critical)
            msg_box.setWindowTitle("Ошибка отключения")
            msg_box.setText(f"OPC-сервер не был подключен")

            font = QtGui.QFont()
            font.setPointSize(12)
            msg_box.setFont(font)
            msg_box.addButton("OK", QtWidgets.QMessageBox.AcceptRole)
            msg_box.exec_()
    def toOPCServer(self):
        try:
            if self.client_thread is None:
                dialog = ConnectDialog()
                if dialog.exec_() == QDialog.Accepted:
                    self.server_url = dialog.server_url
                    try:
                        dialog.client_thread.stop()
                        self.client_thread = OPCClientThread(self.server_url)
                        self.client_thread.start()
                    except Exception as e:
                        print(e)
            else:
                msg_box = QtWidgets.QMessageBox()
                msg_box.setIcon(QtWidgets.QMessageBox.Critical)
                msg_box.setWindowTitle("Ошибка подключения")
                msg_box.setText(f"Вы уже подключены к OPC-серверу")

                font = QtGui.QFont()
                font.setPointSize(12)
                msg_box.setFont(font)
                msg_box.addButton("OK", QtWidgets.QMessageBox.AcceptRole)
                msg_box.exec_()
                    
        except Exception as ex:
            print(ex)
            
    def update_table(self, values):
        try:
            bubble_count1_1 = values['bubble_count1_1']
            bubble_count1_2 = values['bubble_count1_2']
            avg_distance1_1 = values['avg_distance1_1']
            #print(bubble_count1_1)
            #bubble_count1_1 = self.client_thread.client.get_node("ns=2;i=2").get_value()

        except Exception as e:
            print(f"Error fetching data from server: {e}")
            
    def toDBWindow(self):
        if self.conn == -1:
            try:
                self.conn = psycopg2.connect(
                        dbname="foaminfo",
                        user="postgres",
                        password="root",
                        host="176.108.251.124"
                    )
            except Exception:
                self.conn = -1
        if self.conn == -1:
            QtWidgets.QMessageBox.information(MainWindow, "Ошибка подключения", "Не удалось подключиться к базе данных")
        else:
            try:
                #for worker in self.video_workers:
                    #worker.pause()
                #self.isStopped = False
                Dialog = QtWidgets.QDialog()
                ui = DatabaseWidget()
                ui.setupUi(Dialog)
                #Dialog.finished.connect(lambda: self.resumeWorkers())
                Dialog.exec_()
            except Exception as e:
                print(e)

    def resumeWorkers(self):
        for worker in self.video_workers:
            worker.resume()

    def settingsWindowFactory(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog_Factory()
        ui.setupUi(Dialog)
        Dialog.finished.connect(self.checkTerms)
        
        self.stop_all_workers()
        self.graphic1.clear_graph()
        self.graphic2.clear_graph()
        self.graphic3.clear_graph()
        self.graphic4.clear_graph()
        
        Dialog.exec_()

    def checkTerms(self):
        data = functions.read_settings_factory()
        if str(data['fullStatus']) == 'True':
            self.factoryVideos()
        

    def stopProgram(self):
        #self.isStopped = True
        self.stop_all_workers()

    def update_graphic(self, graphic1, numberThread):
        #print(graphic1.size())
        try:
            graphic1.axes.clear()
            if str(self.properties_general['mode']) == '1':
                #print('fac')
                data = self.video_data[str(numberThread)]
                idx = self.idxsGraph[str(numberThread)]
            else:
                #print('lab')
                data = self.video_data['0']
                match graphic1:
                   case self.graphic5:
                       idx = self.idxGraph1
                   case self.graphic6:
                       idx = self.idxGraph2
            
            points = int(data['pointsOnGraph'])
            graphic1.axes.set_xlim(0, points)
            match idx:
                case 0:
                    graphic1.axes.plot(data['framesProcessedArray'], data['bubblesBeforeArray'][-points:], color='black')
                    graphic1.axes.plot(data['framesProcessedArray'], data['bubblesAfterArray'][-points:], linestyle='dashed', color='gray')
                case 1:
                    graphic1.axes.plot(data['framesProcessedArray'], data['avgBeforeArray'][-points:], color='black')
                    graphic1.axes.plot(data['framesProcessedArray'], data['avgAfterArray'][-points:], linestyle='dashed', color='gray')
                case 2:
                    graphic1.axes.plot(data['framesProcessedArray'], data['medianBeforeArray'][-points:], color='black')
                    graphic1.axes.plot(data['framesProcessedArray'], data['medianAfterArray'][-points:], linestyle='dashed', color='gray')
                case 3:
                    graphic1.axes.plot(data['framesProcessedArray'], data['red_pixelsArray'][-points:], color='red')
                case 4:
                    arr_bubbles = []
                    arr_koefs = []
                    for item in data['koefBin_values']:
                        #print(item)
                        bbl = item[1]
                        thresh = item[0]
                        arr_bubbles.append(bbl)
                        arr_koefs.append(thresh)
                        
                    arr_bubbles2 = []
                    arr_koefs2 = []
                    graphic1.axes.plot(arr_koefs, arr_bubbles, linestyle='dashed', color='gray')
                    for item in data['koefBin_values2']:
                        bbl = item[1]
                        thresh = item[0]
                        arr_bubbles2.append(bbl)
                        arr_koefs2.append(thresh)
                    
                    graphic1.axes.plot(arr_koefs2, arr_bubbles2, color='black')
                    graphic1.axes.set_xlim(70, 250)
                case 5:
                    arr_bubbles = []
                    arr_koefs = []
                    for item in data['koefAntiGlare_values']:
                        bbl = item[1]
                        thresh = item[0]
                        arr_bubbles.append(bbl)
                        arr_koefs.append(thresh)

                    graphic1.axes.plot(arr_koefs, arr_bubbles, color='black')
                    graphic1.axes.set_xlim(0, 120)
                case 6:
                    arr_bubbles = []
                    arr_koefs = []
                    for item in data['koefContrast_values']:
                        bbl = item[1]
                        thresh = item[0]
                        arr_bubbles.append(bbl)
                        arr_koefs.append(thresh)

                    graphic1.axes.plot(arr_koefs, arr_bubbles, color='black')
                    graphic1.axes.set_xlim(0, 10)
                
            if idx in (0, 1, 2, 3):
                n = min(len(data['framesProcessedArray']), points)
                if points <= 100:
                    step = int(round(max(n / 20, 10), 0))
                else:
                    step = int(round(points * 0.125, 0))

                xticks_indices = range(0, n, step)  
                xticks_labels = data['framesArray'][-n:][::step]  

                graphic1.axes.set_xticks(xticks_indices)  
                graphic1.axes.set_xticklabels(xticks_labels, fontsize=10)

            graphic1.figure.canvas.draw()
        except Exception as e:
            print(e, 'ee')

    def playVideo(self):
        self.textT.setText('T =')
        self.stop_all_workers()
        self.isStopped = False
        try:
            #self.graphic5.clear_graph()
            #self.graphic6.clear_graph()

            properties = functions.read_settings()
            frameNumber = int(properties['frameNumber'])
            frame_count = int(properties['frame_count'])
            min_bubble_area = int(properties['min_bubble_area'])
            max_bubble_area = int(properties['max_bubble_area'])
            framesInterval = float(properties['framesInterval'])
            windowCoords = properties['windowCoords']
            coordsMode = properties['selectedAreaMode']

            delta_t = int(properties['delta_t'])  # промежуток времени delta t
            R = float(properties['R'])  # параметр R
            sync_mode = str(properties['syncMode'])
            file_path = str(properties['filePath'])
            skipFrames = int(properties['skipFrames'])
            delay = int(properties['delay'])
            usr = int(properties['usr'])
            N = int(properties['N'])
            delaySync = int(properties['delaySync'])
            peak = properties['peak']

            for i in range(1):

                worker = VideoWorker(file_path, windowCoords, min_bubble_area, max_bubble_area, framesInterval, delta_t, R, 0, self.graphic5, self.fileOrCamera, 'Lab', frame_count, frameNumber, self.graphic6, self.binImg, self.roi, self.outputText, self.conn, sync_mode, skipFrames, delay, usr, -1, -1, coordsMode, N, delaySync, peak)
                worker.frame_processed.connect(self.updateGraphicsView)
                worker.graphic_processed.connect(self.updateGraphicFromWorker)
                worker.list_processed.connect(self.appendText)
                worker.T_processed.connect(self.appendT)
                worker.loading_processed.connect(self.show_gif)
                worker.loading_finished.connect(self.hide_gif)
                self.video_workers.append(worker)
                worker.start()

        except Exception as ex:
            print(ex)
    

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Пузырьки"))
        self.menuSettings.setTitle(_translate("MainWindow", "Параметры"))
        self.opcSettings.setTitle(_translate("MainWindow", "OPC"))
        self.actionAbout.setText(_translate("MainWindow", "Изменить режим"))
        self.actionSettings.setText(_translate("MainWindow", "Изменить настройки"))
        self.actionDB.setText(_translate("MainWindow", "База данных"))
        self.actionOPC.setText(_translate("MainWindow", "Подключиться к OPC-серверу"))
        self.actionOPC2.setText(_translate("MainWindow", "Отключиться от OPC-сервера"))
        if str(properties['mode']) == '0':
            self.btnStop.setText(_translate("MainWindow", "Стоп"))
            self.btnStart.setText(_translate("MainWindow", "Старт"))
            self.textT.setText(_translate("MainWindow", "T ="))
            #self.label.setText(_translate("MainWindow", "TextLabel"))
    
            

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


