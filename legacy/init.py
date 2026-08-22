from PyQt5 import QtWidgets
import mainWindow

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow.MainWindow = QtWidgets.QMainWindow()
    ui = mainWindow.Ui_MainWindow()
    ui.setupUi(mainWindow.MainWindow)
    mainWindow.MainWindow.show()
    sys.exit(app.exec_())

