import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage, QFont, QCursor
from PyQt5.QtCore import Qt, QRect, QPoint, pyqtSignal
import functions
import cv2
import numpy as np

class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_point = None
        self.end_point = None
        self.original_start_point = None  
        self.original_end_point = None
        self.image_pixmap = None
        self.drawing = False
        self.setMinimumSize(500, 300)

    def setImage(self, pixmap):
        self.image_pixmap = pixmap
        self.original_size = pixmap.size()
        self.update() 

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.image_pixmap:
            if self.isInsideImage(event.pos()):
                self.start_point = event.pos()  
                self.original_start_point = self.getOriginalPoint(self.start_point)  
                self.drawing = True

    def mouseMoveEvent(self, event):
        if self.drawing and self.image_pixmap:
            if self.isInsideImage(event.pos()):
                self.end_point = event.pos()
                self.original_end_point = self.getOriginalPoint(self.end_point)  
                self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.drawing:
                if self.isInsideImage(event.pos()):
                    self.end_point = event.pos()
                    self.original_end_point = self.getOriginalPoint(self.end_point) 
                self.drawing = False
                self.update()

    def isInsideImage(self, pos):
        scaled_pixmap = self.image_pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return 0 <= pos.x() < scaled_pixmap.width() and 0 <= pos.y() < scaled_pixmap.height()

    def getOriginalPoint(self, scaled_point):
        if self.image_pixmap:
            scaled_pixmap = self.image_pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            scale_x = self.image_pixmap.width() / scaled_pixmap.width()
            scale_y = self.image_pixmap.height() / scaled_pixmap.height()
            original_x = int(scaled_point.x() * scale_x)
            original_y = int(scaled_point.y() * scale_y)
            return QPoint(original_x, original_y)
        return scaled_point

    def getScaledRect(self):
        if self.original_start_point and self.original_end_point:
            scaled_pixmap = self.image_pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            scale_x = self.image_pixmap.width() / scaled_pixmap.width()
            scale_y = self.image_pixmap.height() / scaled_pixmap.height()

            '''
            x1 = int(min(self.original_start_point.x(), self.original_end_point.x()) * scale_x)
            y1 = int(min(self.original_start_point.y(), self.original_end_point.y()) * scale_y)
            x2 = int(max(self.original_start_point.x(), self.original_end_point.x()) * scale_x)
            y2 = int(max(self.original_start_point.y(), self.original_end_point.y()) * scale_y)
            '''
            x1 = int(min(self.original_start_point.x(), self.original_end_point.x()))
            y1 = int(min(self.original_start_point.y(), self.original_end_point.y()))
            x2 = int(max(self.original_start_point.x(), self.original_end_point.x()))
            y2 = int(max(self.original_start_point.y(), self.original_end_point.y()))
            return QRect(QPoint(x1, y1), QPoint(x2, y2))
        return QRect()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.image_pixmap:
            scaled_pixmap = self.image_pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter = QPainter(self)
            painter.drawPixmap(0, 0, scaled_pixmap)  
            if self.start_point and self.end_point:  
                rect = QRect(self.start_point, self.end_point)
                painter.setPen(QPen(Qt.green, 2, Qt.DashLine))
                painter.drawRect(rect.normalized())  

    def resizeEvent(self, event):
        """Обрабатываем изменение размера окна."""
        self.scaled_size = self.image_pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation).size()
        super().resizeEvent(event)
        self.update() 

        
        if self.original_start_point and self.original_end_point:
            self.start_point = self.getScaledPoint(self.original_start_point)
            self.end_point = self.getScaledPoint(self.original_end_point)
            #print(self.start_point, self.end_point)
            self.update()  

    def getScaledPoint(self, original_point):
        """Преобразует оригинальные координаты в масштабированные в зависимости от размера окна."""
        if self.original_start_point and self.original_end_point:
            scaled_pixmap = self.image_pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            scale_x = scaled_pixmap.width() / self.image_pixmap.width()
            scale_y = scaled_pixmap.height() / self.image_pixmap.height()
            scaled_x = int(original_point.x() * scale_x)
            scaled_y = int(original_point.y() * scale_y)
            return QPoint(scaled_x, scaled_y)
        return original_point



class ImageSelector(QDialog):
    dataSaved = pyqtSignal(int, str)
    def __init__(self, file_path, idx, frameNumber):
        try:
            super().__init__()
            self.initUI(file_path, idx, frameNumber)
        except Exception as e:
            print(e)

    def initUI(self, file_path, idx, frameNumber):
        try:
            self.setWindowTitle('Выбор области изображения')
            self.layout = QVBoxLayout()

            self.imageLabel = ImageLabel(self)
            self.layout.addWidget(self.imageLabel)

            self.saveButton = QPushButton('Сохранить', self)
            self.saveButton.clicked.connect(self.saveRoi)
            self.layout.addWidget(self.saveButton)
            font = QFont()
            font.setPointSize(12)
            self.saveButton.setFont(font)
            self.saveButton.setMinimumHeight(35)
            self.saveButton.setCursor(QCursor(Qt.PointingHandCursor))

            self.backButton = QPushButton('Назад', self)
            self.backButton.clicked.connect(self.close)
            self.backButton.setFont(font)
            self.backButton.setCursor(QCursor(Qt.PointingHandCursor))
            self.layout.addWidget(self.backButton)

            self.setLayout(self.layout)
            self.setMouseTracking(True)

            self.idx = idx
            self.file_path = file_path
            self.frameNumber = frameNumber
            if self.idx == 0:
                data = functions.read_settings()
                #file_path = data['filePath']
                #frameNumber = int(data['frameNumber'])
                frameno = 0
                ext = self.file_path.split(".")[-1] 
                if ext.lower() in ['jpg', 'png', 'jpeg']:
                    img = cv2.imdecode(np.fromfile(self.file_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED) 
                elif ext.lower() in ['avi', 'mpeg', 'mpg', 'mp4']:
                    cap = cv2.VideoCapture()
                    cap.open(self.file_path)
                    while frameno <= self.frameNumber:
                        _, img = cap.read()
                        frameno += 1
            else:
                cap = cv2.VideoCapture()
                cap.open(self.file_path)

                _, img = cap.read()
            bytesPerLine = 3 * img.shape[1]
            qImg = QImage(img.data, img.shape[1], img.shape[0], bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap(qImg)
            self.imageLabel.setImage(pixmap)
            self.imageLabel.start_point = None
            self.imageLabel.end_point = None  
        except Exception as e:
            print(e)
                        
                

    def saveRoi(self):
        rect = self.imageLabel.getScaledRect()
        if rect.isValid() and self.imageLabel.image_pixmap:
            roi_pixmap = self.imageLabel.image_pixmap.copy(rect) 
        if rect.width() == 1 and rect.height == 1:
            toOutput = "0 0 0 0"
        else:
            toOutput = str(rect.x()) + " " + str(rect.y()) + " " + str(rect.width()) + " " + str(rect.height())
        self.dataSaved.emit(self.idx, toOutput)
        self.close()
            
filepath = "C:/Users/Kuzne/Desktop/snil/videos/VID00022.mp4"
if __name__ == '__main__':
    try:
        
        app = QApplication(sys.argv)
        ex = ImageSelector(filepath, 0)
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
