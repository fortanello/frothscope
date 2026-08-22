import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage, QFont, QCursor, QPolygon
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
import cv2
import numpy as np
import functions

class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_polygon_points = []  
        self.scaled_polygon_points = []  
        self.image_pixmap = None
        self.original_size = None 
        self.scaled_size = None  
        self.setMinimumSize(500, 300)

    def setImage(self, pixmap):
        self.image_pixmap = pixmap
        self.original_size = pixmap.size()  
        self.scaled_size = self.image_pixmap.size() 
        self.update()  

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.image_pixmap:
            if self.isInsideImage(event.pos()):
                original_x = int(event.pos().x() * self.original_size.width() / self.scaled_size.width())
                original_y = int(event.pos().y() * self.original_size.height() / self.scaled_size.height())
                
                if 0 <= original_x < self.original_size.width() and 0 <= original_y < self.original_size.height():
                    self.original_polygon_points.append(QPoint(original_x, original_y))
                    self.updateScaledPolygonPoints()

                self.update()

    def isInsideImage(self, pos):
        return 0 <= pos.x() < self.scaled_size.width() and 0 <= pos.y() < self.scaled_size.height()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.image_pixmap:
            scaled_pixmap = self.image_pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter = QPainter(self)
            painter.drawPixmap(0, 0, scaled_pixmap) 
            
            if len(self.scaled_polygon_points) > 0:
                painter.setPen(QPen(Qt.green, 2, Qt.DashLine))
                painter.drawPolygon(QPolygon(self.scaled_polygon_points))


    def scalePoint(self, point):
        if self.scaled_size:
            scale_x = self.scaled_size.width() / self.original_size.width()
            scale_y = self.scaled_size.height() / self.original_size.height()
            return QPoint(int(point.x() * scale_x), int(point.y() * scale_y))
        return point

    def updateScaledPolygonPoints(self):
        self.scaled_polygon_points = [self.scalePoint(p) for p in self.original_polygon_points]
        self.update() 

    def resetPolygon(self):
        self.original_polygon_points.clear()
        self.scaled_polygon_points.clear() 
        self.update()  

    def resizeEvent(self, event):
        self.scaled_size = self.image_pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation).size()
        self.updateScaledPolygonPoints() 
        self.update() 

    def savePolygonToFile(self):
        toOutput = ' '.join(f"{p.x()} {p.y()}" for p in self.original_polygon_points)
        return toOutput

    def loadPolygonFromFile(self, file_path):
        self.original_polygon_points.clear()
        try:
            with open(file_path, 'r') as f:
                coords_str = f.read().strip() 
                coords = coords_str.split()
                for i in range(0, len(coords), 2): 
                    x = int(coords[i])
                    y = int(coords[i + 1])
                    self.original_polygon_points.append(QPoint(x, y))
            self.updateScaledPolygonPoints()
            print(f"Координаты полигона загружены из {file_path}")
        except Exception as e:
            print(f"Ошибка загрузки: {e}")


class ImageSelectorPolygons(QDialog):
    dataSaved = pyqtSignal(int, str)
    
    def __init__(self, file_path, idx, frameNumber):
        super().__init__()
        self.initUI(file_path, idx, frameNumber)

    def initUI(self, file_path, idx, frameNumber):
        self.setWindowTitle('Выбор области изображения')
        self.layout = QVBoxLayout()

        self.imageLabel = ImageLabel(self)
        self.layout.addWidget(self.imageLabel)

        font = QFont()
        font.setPointSize(12)
        
        self.saveButton = QPushButton('Сохранить маску', self)
        self.saveButton.clicked.connect(self.savePolygon)
        self.layout.addWidget(self.saveButton)
        self.saveButton.setFont(font)
        self.saveButton.setMinimumHeight(35)
        self.saveButton.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.resetButton = QPushButton('Сбросить выделение', self)
        self.resetButton.clicked.connect(self.resetSelection)
        self.resetButton.setFont(font)
        self.resetButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.layout.addWidget(self.resetButton)

        

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
            frameNumber = int(data['frameNumber'])
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
    
        
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(qImg)
        self.imageLabel.setImage(pixmap)

    def savePolygon(self):
        try:
            toOutput = self.imageLabel.savePolygonToFile()
            self.dataSaved.emit(self.idx, toOutput)
            self.close()
        except Exception as ex:
            print(ex)

    def loadPolygon(self):
        self.imageLabel.loadPolygonFromFile("polygon_mask.txt")

    def saveRoi(self):
        try:
            if self.imageLabel.original_polygon_points:
                mask = np.zeros((self.imageLabel.original_size.height(), self.imageLabel.original_size.width()), dtype=np.uint8)
                
                if len(self.imageLabel.original_polygon_points) == 0:
                    print("Нет точек для заполнения полигона.")
                    return

                points = np.array([(p.x(), p.y()) for p in self.imageLabel.original_polygon_points], np.int32)
                points = points.reshape((-1, 1, 2))
                cv2.fillPoly(mask, [points], (255, 255, 255))

                original_image = self.imageLabel.image_pixmap.toImage()
                original_image = original_image.convertToFormat(QImage.Format_RGB888)

                ptr = original_image.constBits()
                ptr.setsize(original_image.byteCount())  
                arr = np.array(ptr).reshape(original_image.height(), original_image.width(), 3) 

                roi = cv2.bitwise_and(arr, arr, mask=mask)

                
                x, y, w, h = cv2.boundingRect(mask)
                cropped_roi = roi[y:y+h, x:x+w]

                
                cv2.imshow("Highlighted Region", cropped_roi)
                cv2.waitKey(0)  
                cv2.destroyAllWindows()  

                self.saveImageWithPolygon(arr, points)

            
                self.saveCroppedImage(cropped_roi)


                points_str = " ".join(f"{p.x()} {p.y()}" for p in self.imageLabel.original_polygon_points)
                self.dataSaved.emit(self.idx, points_str)
                self.close()
        except Exception as e:
            print(e)

    def saveImageWithPolygon(self, image_array, points):
        image_with_polygon = image_array.copy()

        cv2.polylines(image_with_polygon, [points], isClosed=True, color=(0, 255, 0), thickness=2)

        output_file = "highlighted_area.png" 
        cv2.imwrite(output_file, image_with_polygon)
        print(f"Изображение сохранено как {output_file}")

    def saveCroppedImage(self, cropped_image):
        output_file = "cropped_area.png"
        cv2.imwrite(output_file, cropped_image)
        print(f"Выделенная область сохранена как {output_file}")

    def resetSelection(self):
        self.imageLabel.resetPolygon()


filepath = "C:/Users/STANISLAV/Desktop/input_data_gp/VID00022.mp4"
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageSelectorPolygons(filepath, 0, 0)
    ex.show()
    sys.exit(app.exec_())
