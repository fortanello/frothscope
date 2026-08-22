from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDateTime
import psycopg2
import datetime
import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.utils.dataframe import dataframe_to_rows
import os


class DatabaseWidget(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1042, 786)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dateTimeEdit.setFont(font)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.horizontalLayout.addWidget(self.dateTimeEdit)
        self.dateTimeEdit_2 = QtWidgets.QDateTimeEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dateTimeEdit_2.setFont(font)
        self.dateTimeEdit_2.setObjectName("dateTimeEdit_2")
        self.horizontalLayout.addWidget(self.dateTimeEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setMaximumSize(QtCore.QSize(16777215, 160))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.checkBox = QtWidgets.QComboBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        self.checkBox.setMinimumSize(QtCore.QSize(0, 0))
        self.checkBox.setSizeIncrement(QtCore.QSize(0, 0))
        #self.checkBox.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setUnderline(False)
        self.checkBox.setFont(font)
        self.checkBox.addItem("Наличие")
        self.checkBox.addItem("Отсутствие")
        self.checkBox.addItem("Все данные")
        #self.checkBox.setText("")
        #self.checkBox.setIconSize(QtCore.QSize(16, 16))
        #self.checkBox.setChecked(False)
        #self.checkBox.setAutoRepeat(False)
        #self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_3.addWidget(self.checkBox)
        #spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 460))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(self.export_to_excel)
        self.pushButton_2.clicked.connect(self.delete_selected_rows)
        self.pushButton_3.clicked.connect(self.load_data)

        
        self.tableWidget.setColumnCount(11) 
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Порт", "Кол-во пузырьков", "КП с антибликом", "Ср. арифм. расстояние", "САР с антибликом", "Ср. медианное расстояние", "СМР с антибликом", "Красная компонента", "Переходный процесс", "Время"])
        self.tableWidget.setColumnHidden(0, True)
        for column in range(self.tableWidget.columnCount()):
            self.tableWidget.resizeColumnToContents(column)

        self.conn = psycopg2.connect(
                    dbname="foams",
                    user="postgres",
                    password="root",
                    host="localhost"
                )
        self.cursor = self.conn.cursor()
        self.load_ports()
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime().addMonths(-1))
        self.dateTimeEdit_2.setDateTime(QDateTime.currentDateTime())

    def load_ports(self):
        self.cursor.execute("SELECT DISTINCT port_number FROM inform")
        ports = self.cursor.fetchall()
        for port in ports:
            self.listWidget.addItem(port[0])

    def load_data(self):
        try:
            self.tableWidget.setRowCount(0)

            start_datetime = self.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
            end_datetime = self.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd hh:mm:ss")

            selected_ports = [self.listWidget.item(i).text() for i in range(self.listWidget.count()) if self.listWidget.item(i).isSelected()]
            if not selected_ports:
                self.cursor.execute("SELECT DISTINCT port_number FROM inform")
                ports = self.cursor.fetchall()
                selected_ports = [port[0] for port in ports]

            in_clause = ','.join(['%s'] * len(selected_ports))
            combo_index = self.checkBox.currentIndex()
            if combo_index == 0:  # Наличие
                comment_condition = "AND is_transition = True"
            elif combo_index == 1:  # Отсутствие
                comment_condition = "AND is_transition != True"
            else:  # Все данные
                comment_condition = ""
            query = f"""
                SELECT id, port_number, cnt, cnt_antiglare, 
                    avg_value, avg_antiglare_value, median_value, 
                    median_antiglare_value, red_c_value, is_transition, date1
                FROM inform
                WHERE date1 BETWEEN %s AND %s 
                AND port_number IN ({in_clause})
                {comment_condition}
            """ 

            params = [start_datetime, end_datetime] + selected_ports
            self.cursor.execute(query, params)

            rows = self.cursor.fetchall()
            for row in rows:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                for column, value in enumerate(row):
                    if column == 10:
                        date_value = value.strftime('%d.%m.%Y %H:%M:%S') if value else ''
                        self.tableWidget.setItem(row_position, column, QTableWidgetItem(date_value))
                    else:
                        self.tableWidget.setItem(row_position, column, QTableWidgetItem(str(value)))

            self.tableWidget.resizeColumnsToContents()
            
        except Exception as ex:
            print(ex)

    def delete_selected_rows(self):
        try:
            selected_rows = self.tableWidget.selectedIndexes()
            if not selected_rows:
                return

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Подтверждение удаления")
            msg_box.setText("Вы уверены, что хотите удалить выбранные записи?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            response = msg_box.exec()

            if response == QMessageBox.Yes:
                ids_to_delete = set()
                for index in selected_rows:
                    row = index.row()
                    item = self.tableWidget.item(row, 0) 
                    if item:
                        ids_to_delete.add(item.text())

                if ids_to_delete:
                    ids_to_delete_list = [int(id) for id in ids_to_delete]
                    self.cursor.execute("CALL delete_data(%s)", (ids_to_delete_list,))
                    self.conn.commit()
                    self.load_data()

        except Exception as ex:
            print(ex)

    def export_to_excel(self):
        try:
            rows = []
            for i in range(self.tableWidget.rowCount()):
                row = []
                for j in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(i, j)
                    if j == 10:
                        if item:
                            date_value = item.text()
                            formatted_date = datetime.datetime.strptime(date_value, '%d.%m.%Y %H:%M:%S').strftime('%d.%m.%Y %H:%M:%S')
                            row.append(formatted_date)
                        else:
                            row.append('')
                    elif j != 0:
                        row.append(item.text() if item else "")
                rows.append(row)

            df = pd.DataFrame(rows)
            headers = ["Порт", "Количество пузырьков", "КП с антибликом", "Среднее арифметическое расстояние", 
                       "САР с антибликом", "Среднее медианное расстояние", "СМР с антибликом", "Красная компонента", 
                       "Переходный процесс", "Время"]
            df.columns = headers

            excel_file_name = "data_exported.xlsx"
            wb = Workbook()
            ws = wb.active
            ws.title = "Data"
            for row in dataframe_to_rows(df, index=False, header=True):
                ws.append(row)
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                ws.column_dimensions[column_letter].width = adjusted_width
            wb.save(excel_file_name)
            os.startfile(excel_file_name)
            QMessageBox.information(self, "Экспорт в Excel", f"Данные успешно экспортированы в {excel_file_name}")
        
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            QMessageBox.critical(self, "Ошибка", "Произошла ошибка при экспорте данных в Excel.")
            
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "База данных пузырьков"))
        self.label.setText(_translate("Dialog", "- Период"))
        self.label_2.setText(_translate("Dialog", "- Порты"))
        self.label_3.setText(_translate("Dialog", "- Переходный процесс"))
        self.pushButton_3.setText(_translate("Dialog", "Вывести данные"))
        self.pushButton.setText(_translate("Dialog", "Экспорт в Excel"))
        self.pushButton_2.setText(_translate("Dialog", "Удалить выбранные"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = DatabaseWidget()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
