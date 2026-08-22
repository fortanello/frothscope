from PyQt5 import QtCore, QtGui, QtWidgets
from ultralytics import YOLO
import functions
import time
import cv2
import pytz
from datetime import datetime
import numpy as np

class VideoWorker(QtCore.QThread):
    frame_processed = QtCore.pyqtSignal(QtGui.QPixmap, QtWidgets.QGraphicsView)
    graphic_processed = QtCore.pyqtSignal(QtWidgets.QGraphicsView, int, list)
    list_processed = QtCore.pyqtSignal(str, QtWidgets.QGraphicsView)
    T_processed = QtCore.pyqtSignal(str)
    opc_data_updated = QtCore.pyqtSignal(dict, int)
    loading_processed = QtCore.pyqtSignal()
    loading_finished = QtCore.pyqtSignal()
    alarm_started = QtCore.pyqtSignal(int)
    alarm_finished = QtCore.pyqtSignal(int)

    def __init__(self, file_path, windowCoords, min_bubble_area, max_bubble_area, framesInterval, delta_t, R, numberThread, graphic1, graphics_view, mode1, frame_count, frameNumber, graphic2, graphics_bin, graphics_roi, textBox, conn, sync_mode, skipFrames, delay, usr, T, pogr, coordsMode, N, delaySync, peak):
        super().__init__()
        self.file_path = file_path
        self.windowCoords = windowCoords
        self.graphics_view = graphics_view

        self.graphics_bin = graphics_bin
        self.graphics_roi = graphics_roi

        self.min_bubble_area = min_bubble_area
        self.max_bubble_area = max_bubble_area
        self.framesInterval = float(framesInterval)

        self.delta_t = int(delta_t)
        self.R = float(R)

        self.numberThread = numberThread

        self.graphic = graphic1
        self.graphic2 = graphic2

        self.framesArray = []
        self.framesProcessedArray = []
        self.bubblesBeforeArray = []
        self.bubblesAfterArray = []
        self.avgBeforeArray = []
        self.avgAfterArray = []
        self.medianBeforeArray = []
        self.medianAfterArray = []
        self.red_pixelsArray = []

        self.koefBin_values = []
        self.koefBin_values2 = []
        self.koefContrast_values = []
        self.koefAntiGlare_values = []
        self.timeArray = []
        self.delay = int(delay)
        self.usr = int(usr)
        self.T = float(T)
        self.pogr = float(pogr)

        self.running = True
        self.L_max = 0
        self.L_min = 0
        self.brightness_array = []
        self.delaySyncOrig = delaySync
        self.delaySync = delaySync
        self.mode1 = mode1
        self.frame_count = frame_count
        self.frameNumber = frameNumber
        self.N = N
        self.peak = peak

        self.original_polygon_points = []

        self.mutex = QtCore.QMutex()
        self.paused = False
        self.time_o = time.time()-10
        self.time_l = time.time()
        self.fl = False
        if self.frameNumber > 10:
            self.fl0 = True
        else:
            self.fl0 = False

        self.textBox = textBox
        self.timezone = pytz.timezone('Asia/Kolkata')
        self.coordsMode = coordsMode

        if functions.check_digits(file_path):
            mode = 'cam'
        else:
           ext = file_path.split(".")[-1] 
           if ext.lower() in ['jpg', 'png', 'jpeg']:
               mode = 'img'
           elif ext.lower() in ['avi', 'mpeg', 'mpg', 'mp4']:
            mode = 'video'
                
        self.sync_mode = sync_mode
        
        if mode != 'img' and sync_mode == '0':
            self.model = YOLO('../weights/best.pt')
            self.model = functions.to_cuda(self.model)
            self.isPenogon = False
        
        self.skip_frame_count = 0
        self.skipFrames = int(skipFrames)

        self.conn = conn
        if self.conn != -1:
            self.cursor = self.conn.cursor()
    def run(self):
        try: 
            frameno = 0
            processedFrame = 0
            if self.mode1 == 'Lab':
                fps = 60
            else:
                fps = 60
            delay = int(1000 / fps)
            if self.windowCoords != '-1':
                if self.coordsMode == '0':
                    x, y, w, h = map(int, self.windowCoords.split()) # координаты окна
                else:
                    coords_str = self.windowCoords.strip()
                    coords = coords_str.split()
                    for i in range(0, len(coords), 2):  # Проходим через все координаты по парам
                        x = int(coords[i])
                        y = int(coords[i + 1])
                        self.original_polygon_points.append(QtCore.QPoint(x, y))
        
            last_time = 0
            max_bubble_count = 0
            first_time = time.time()
            if self.mode1 == 'Lab':
                mode, frame, frame_count, cap = functions.getMode(self.file_path, self.frame_count)
            else:
                cap = cv2.VideoCapture(self.file_path)
                mode = -1

            while self.running:
                self.mutex.lock()
                if self.paused:
                    self.mutex.unlock()
                    self.msleep(100)  # Ждем, пока поток не будет возобновлен
                    continue
                self.mutex.unlock()
                if self.mode1 == 'Lab':
                    if mode == 'img':
                        self.frame_count = 0
                        ret = True
                    else:
                        if self.fl0:
                            self.loading_processed.emit()
                            self.fl = True
                        while frameno < self.frameNumber:
                            _, frame = cap.read()
                            frameno += 1
                        ret, frame = cap.read()
                        if self.fl:
                            self.loading_finished.emit()
                            self.fl = False
                            self.fl0 = False 
                else:                  
                    ret, frame = cap.read()
                
                if ret:
                    
                    frameno += 1    
                    frame2 = frame.copy()
                    cur_time = time.time() - first_time
                    
                    isProcess = False
                    if self.sync_mode == '0':
                        if self.skip_frame_count > 0:
                            self.skip_frame_count -= 1
                              
                        if (cur_time - last_time > self.framesInterval and self.skip_frame_count == 0):
                            frame, isPenogon = functions.is_penogon(self.model, frame, self.coordsMode, self.windowCoords)
                            #print(1)
                            if not isPenogon:
                                isProcess = True
                                #print(2)
                            else:
                                self.skip_frame_count = self.skipFrames
                    
                               
                    elif self.sync_mode == '2' and cur_time - last_time > self.framesInterval:
                        isProcess = True
                    elif self.sync_mode == '1':
                        frame99 = frame.copy()
                        if self.windowCoords == '-1':
                            ponImg = frame99.copy()
                        else:
                            if self.coordsMode == '0':
                                cv2.rectangle(frame99, (x,y), (x+w,y+h), (0,255,0), 7)
                                ponImg = frame99[y:y+h, x:x+w].copy()
                            else:
                                points = np.array([(p.x(), p.y()) for p in self.original_polygon_points], np.int32)
                                points = points.reshape((-1, 1, 2))
                                cv2.polylines(frame99, [points], isClosed=True, color=(0, 255, 0), thickness=9)
                                self.mask = np.zeros(frame99.shape[:2], dtype=np.uint8)
                                cv2.fillPoly(self.mask, [points], 255)

                                frame3 = frame99.copy()
                                frame3 = cv2.bitwise_and(frame99, frame99, mask=self.mask)
                                x, y, w, h = cv2.boundingRect(self.mask)
                                ponImg = frame3[y:y+h, x:x+w]
                       
                        #alpha = 2.5  # Увеличение контрастности
                        #beta = 0     # Смещение, можно настроить
                        #ponImg = cv2.convertScaleAbs(ponImg, alpha=alpha, beta=beta)
                        #
                        brightness_value = functions.calculate_illumination(ponImg)
                        self.brightness_array.append(brightness_value)
                        L_array = self.brightness_array[-self.N:]
                        self.L_max = max(L_array)
                        self.L_min = min(L_array)

                        L = (self.L_max - self.L_min) / self.R
                        
                        if len(self.brightness_array) >= self.delta_t:
                            O_delta_t = self.brightness_array[-self.delta_t]
                        else:
                            O_delta_t = 0
                            
                        isSync = False
                        if cur_time - last_time > self.framesInterval:
                            if self.peak == '0':
                                if ((self.brightness_array[-1] - O_delta_t) >= L):
                                    isSync = True
                            else:
                                if not((self.brightness_array[-1] - O_delta_t) >= L):
                                    isSync = True
                        if isSync:
                            if self.delaySync > 0:
                                self.delaySync -= 1 
                            if self.delaySync == 0:
                                isProcess = True
                                self.delaySync = self.delaySyncOrig
                        else:
                            self.delaySync = self.delaySyncOrig
                    
                    if (self.mode1 == 'Lab' and mode == 'img'):
                        isProcess = True

                    if self.windowCoords != '-1':
                        if self.coordsMode == '0':
                            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 7)
                        else:
                            points = np.array([(p.x(), p.y()) for p in self.original_polygon_points], np.int32)
                            points = points.reshape((-1, 1, 2))
                            cv2.polylines(frame, [points], isClosed=True, color=(0, 255, 0), thickness=9)
                            self.mask = np.zeros(frame.shape[:2], dtype=np.uint8)
                            cv2.fillPoly(self.mask, [points], 255)
                        
                    
                    if isProcess:
                        last_time =  time.time() - first_time
                        if self.windowCoords == '-1':
                            cimg = cimg = frame2.copy()
                        else:    
                            if self.coordsMode == '0':
                                #cimg = functions.getSize(self.windowCoords, frame2)
                                cimg = frame2[y:y+h, x:x+w].copy()
                            else:
                                frame3 = frame2.copy()
                                frame3 = cv2.bitwise_and(frame2, frame2, mask=self.mask)
                                x, y, w, h = cv2.boundingRect(self.mask)
                                cimg = frame3[y:y+h, x:x+w]
                        

                        if self.mode1 == 'Lab':
                            properties = functions.read_settings()
                            koefBin = int(properties['koefBin'])
                            koefContrast = int(properties['koefContrast'])
                            koefAntiGlare = int(properties['koefAntiGlare'])
                            pointsOnGraph = int(properties['pointsOnGraph'])
                        else:
                            properties = functions.read_settings_factory()
                            match self.numberThread:
                                case 1:
                                    koefBin = int(properties['koefBin'])
                                    koefContrast = int(properties['koefContrast'])
                                    koefAntiGlare = int(properties['koefAntiGlare'])
                                    pointsOnGraph = int(properties['pointsOnGraph'])
                                case 2:
                                    koefBin = int(properties['koefBin_2'])
                                    koefContrast = int(properties['koefContrast_2'])
                                    koefAntiGlare = int(properties['koefAntiGlare_2'])
                                    pointsOnGraph = int(properties['pointsOnGraph_2'])
                                case 3:
                                    koefBin = int(properties['koefBin_3'])
                                    koefContrast = int(properties['koefContrast_3'])
                                    koefAntiGlare = int(properties['koefAntiGlare_3'])
                                    pointsOnGraph = int(properties['pointsOnGraph_3'])
                                case 4:
                                    koefBin = int(properties['koefBin_4'])
                                    koefContrast = int(properties['koefContrast_4'])
                                    koefAntiGlare = int(properties['koefAntiGlare_4'])
                                    pointsOnGraph = int(properties['pointsOnGraph_4'])
                        
                        settings = {
                            'pointsOnGraph': pointsOnGraph,
                            'idx': self.numberThread,
                            'frameno': frameno, 
                            'cimg': cimg,
                            'koefBin': koefBin, 
                            'koefContrast': koefContrast,
                            'koefAntiGlare': koefAntiGlare, 
                            'min_bubble_area': self.min_bubble_area,
                            'max_bubble_area': self.max_bubble_area, 
                            'framesArray': self.framesArray,
                            'avgBeforeArray': self.avgBeforeArray,
                            'avgAfterArray': self.avgAfterArray,
                            'medianBeforeArray': self.medianBeforeArray, 
                            'medianAfterArray': self.medianAfterArray,
                            'red_pixelsArray': self.red_pixelsArray, 
                            'bubblesBeforeArray': self.bubblesBeforeArray, 
                            'bubblesAfterArray': self.bubblesAfterArray,
                            'processedFrame': processedFrame,
                            'framesProcessedArray': self.framesProcessedArray,
                            'koefBin_values': self.koefBin_values,
                            'koefBin_values2': self.koefBin_values2,
                            'koefContrast_values': self.koefContrast_values,
                            'koefAntiGlare_values': self.koefAntiGlare_values,
                        }
                        
                        if abs(self.time_l - self.time_o) > 0.1:
                            self.loading_processed.emit()
                            self.fl = True
                        #if self.numberThread == 0 and koefBin == -1:
                        self.time_o = self.time_l    
                        self.time_l = time.time()
                        
                        processed_data = functions.process_frame(frameno, cimg, settings)
                        
                        self.timeArray.append(round(float(time.time() - first_time), 3))
                        
                        self.time_l = time.time() - self.time_l
                        if self.fl:
                            self.loading_finished.emit()
                            self.fl = False
                        self.framesArray = processed_data['framesArray']
                        self.avgBeforeArray = processed_data['avgBeforeArray']
                        self.avgAfterArray = processed_data['avgAfterArray']
                        self.medianBeforeArray = processed_data['medianBeforeArray']
                        self.medianAfterArray = processed_data['medianAfterArray']
                        self.red_pixelsArray = processed_data['red_pixelsArray']
                        self.bubblesBeforeArray = processed_data['bubblesBeforeArray']
                        self.bubblesAfterArray = processed_data['bubblesAfterArray']
                        thresholded_img = processed_data['thresholded_img']
                        cimgCopy6 = processed_data['cimgCopy6']
                        processedFrame = processed_data['processedFrame']
                        self.framesProcessedArray = processed_data['framesProcessedArray']

                        self.koefBin_values = processed_data['koefBin_values']
                        self.koefBin_values2 = processed_data['koefBin_values2']
                        self.koefContrast_values = processed_data['koefContrast_values']
                        self.koefAntiGlare_values = processed_data['koefAntiGlare_values']

                        
                        bubble_count_before = processed_data['bubble_count_before']
                        bubble_count_after = processed_data['bubble_count_after']
                        avg_distance_before = processed_data['avg_distance_before']
                        if avg_distance_before == None:
                            avg_distance_before = 0
                        else:    
                            avg_distance_before = round(avg_distance_before, 2)
                        avg_distance_after = processed_data['avg_distance_after']
                        if avg_distance_after == None:
                            avg_distance_after = 0
                        else:
                            avg_distance_after = round(avg_distance_after, 2)
                        median_distance_before = processed_data['median_distance_before']
                        if median_distance_before == None:
                            median_distance_before = 0
                        else:
                            median_distance_before = round(median_distance_before, 2)
                        median_distance_after = processed_data['median_distance_after']
                        if median_distance_after == None:
                            median_distance_after = 0
                        else:
                            median_distance_after = round(median_distance_after, 2)
                        red_pixels = processed_data['red_pixels']
                        if red_pixels == None:
                            red_pixels = 0
                        else:
                            red_pixels = round(red_pixels, 2)
                        T_res = None
                        if self.usr > 0:
                            #T_res = functions.doit(self.delay, self.usr, self.timeArray, self.bubblesAfterArray)
                            T_res = functions.doit(self.delay, self.usr, self.timeArray, self.bubblesBeforeArray)
                        if self.mode1 == 'Lab':
                            self.T_processed.emit(str(T_res))
                        

                        if self.mode1 == 'Lab':
                            properties = functions.read_settings()
                            koefBin = int(properties['koefBin'])
                            koefContrast = int(properties['koefContrast'])
                            koefAntiGlare = int(properties['koefAntiGlare'])
                        else:
                            properties = functions.read_settings_factory()
                            current_time = datetime.now(self.timezone)
                            date1 = current_time.strftime('%d-%m-%Y %H:%M:%S')
                            match self.numberThread:
                                case 1:
                                    koefBin = int(properties['koefBin'])
                                    koefContrast = int(properties['koefContrast'])
                                    koefAntiGlare = int(properties['koefAntiGlare'])

                                    values = {
                                        'port_number1': self.file_path,
                                        'bubble_count1_1': bubble_count_before,
                                        'bubble_count1_2': bubble_count_after,
                                        'avg_distance1_1': avg_distance_before,
                                        'avg_distance1_2': avg_distance_after,
                                        'median_distance1_1': median_distance_before,
                                        'median_distance1_2': median_distance_after,
                                        'red_component1': red_pixels,
                                        'date1': date1
                                    }
                                case 2:
                                    koefBin = int(properties['koefBin_2'])
                                    koefContrast = int(properties['koefContrast_2'])
                                    koefAntiGlare = int(properties['koefAntiGlare_2'])

                                    values = {
                                        'port_number2': self.file_path,
                                        'bubble_count2_1': bubble_count_before,
                                        'bubble_count2_2': bubble_count_after,
                                        'avg_distance2_1': avg_distance_before,
                                        'avg_distance2_2': avg_distance_after,
                                        'median_distance2_1': median_distance_before,
                                        'median_distance2_2': median_distance_after,
                                        'red_component2': red_pixels,
                                        'date2': date1
                                    }
                                case 3:
                                    koefBin = int(properties['koefBin_3'])
                                    koefContrast = int(properties['koefContrast_3'])
                                    koefAntiGlare = int(properties['koefAntiGlare_3'])

                                    values = {
                                        'port_number3': self.file_path,
                                        'bubble_count3_1': bubble_count_before,
                                        'bubble_count3_2': bubble_count_after,
                                        'avg_distance3_1': avg_distance_before,
                                        'avg_distance3_2': avg_distance_after,
                                        'median_distance3_1': median_distance_before,
                                        'median_distance3_2': median_distance_after,
                                        'red_component3': red_pixels,
                                        'date3': date1
                                    }
                                case 4:
                                    koefBin = int(properties['koefBin_4'])
                                    koefContrast = int(properties['koefContrast_4'])
                                    koefAntiGlare = int(properties['koefAntiGlare_4'])

                                    values = {
                                        'port_number4': self.file_path,
                                        'bubble_count4_1': bubble_count_before,
                                        'bubble_count4_2': bubble_count_after,
                                        'avg_distance4_1': avg_distance_before,
                                        'avg_distance4_2': avg_distance_after,
                                        'median_distance4_1': median_distance_before,
                                        'median_distance4_2': median_distance_after,
                                        'red_component4': red_pixels,
                                        'date4': date1
                                    }                            
                        data_for_graph = [self.framesProcessedArray, self.bubblesBeforeArray, self.bubblesAfterArray, self.avgBeforeArray, self.avgAfterArray, self.medianBeforeArray, self.medianAfterArray, self.red_pixelsArray, self.framesArray, self.koefBin_values, self.koefBin_values2, self.koefContrast_values, self.koefAntiGlare_values]
        
                        
                        if self.mode1 != 'Lab':
                            self.graphic_processed.emit(self.graphic, self.numberThread, data_for_graph)
                        if self.mode1 == 'Lab':
                            self.graphic_processed.emit(self.graphic, self.numberThread, data_for_graph)
                            self.graphic_processed.emit(self.graphic2, self.numberThread, data_for_graph)

                            stringForOutput = "Прошло кадров: " + str(frameno) + ", распознано пузырьков: " + str(bubble_count_before) + " (" + str(bubble_count_after) + ")"
                            self.list_processed.emit(stringForOutput, self.textBox)
                            stringForOutput = "Средне -арифметическое расстояние:  " + str(avg_distance_before) + " (" + str(avg_distance_after) + ")" + ", -медианное:  " + str(median_distance_before) + " (" + str(median_distance_after) + ")"
                            self.list_processed.emit(stringForOutput, self.textBox)
                            stringForOutput = "Красная компонента:  " + str(red_pixels)
                            self.list_processed.emit(stringForOutput, self.textBox)
                            stringForOutput = ""
                            self.list_processed.emit(stringForOutput, self.textBox)

                            thresholded_img = cv2.cvtColor(thresholded_img, cv2.COLOR_GRAY2RGB)
                            bytesPerLine = 3 * thresholded_img.shape[1]
                            qImg = QtGui.QImage(thresholded_img.data, thresholded_img.shape[1], thresholded_img.shape[0], bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
                            qPixMap = QtGui.QPixmap.fromImage(qImg).scaled(self.graphics_bin.size(), QtCore.Qt.KeepAspectRatio)
                            

                            self.frame_processed.emit(qPixMap, self.graphics_bin)
                            
                            cimgCopyRoi = cimgCopy6.copy()
                            
                            cimgCopyRoi = functions.draw_detected_glare(cimgCopyRoi, koefBin, self.min_bubble_area, self.max_bubble_area)
                            
                            bytesPerLine = 3 * cimgCopyRoi.shape[1]
                            qImg = QtGui.QImage(cimgCopyRoi.data, cimgCopyRoi.shape[1], cimgCopyRoi.shape[0], bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
                            qPixMap = QtGui.QPixmap.fromImage(qImg).scaled(self.graphics_view.size(), QtCore.Qt.KeepAspectRatio)

                            self.frame_processed.emit(qPixMap, self.graphics_roi)
                        else:
                            stringForOutput = "Распознано пузырьков:  " + str(bubble_count_before) + " (" + str(bubble_count_after)+ ")"
                            self.list_processed.emit(stringForOutput, self.textBox)
                            stringForOutput = "Среднее арифметическое:  " + str(round(avg_distance_before,2)) + " (" + str(round(avg_distance_after,2)) + ")"
                            self.list_processed.emit(stringForOutput, self.textBox)
                            stringForOutput = "Среднее медианное:  " + str(round(median_distance_before,2)) + " (" + str(round(median_distance_after,2)) + ")"
                            self.list_processed.emit(stringForOutput, self.textBox)
                            stringForOutput = "Красная компонента:  " + str(round(red_pixels,2))
                            self.list_processed.emit(stringForOutput, self.textBox)
                            stringForOutput = ""
                            self.list_processed.emit(stringForOutput, self.textBox)
                            if T_res is not None:  
                                if (abs(T_res - self.T)) <= self.pogr:
                                    self.opc_data_updated.emit(values, self.numberThread)
                                    self.alarm_started.emit(self.numberThread)
                                    #print(self.numberThread)
                                    

                                    if self.conn != -1:
                                        self.cursor.execute("CALL insert_data(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.file_path, int(bubble_count_before), int(bubble_count_after), float(avg_distance_before), float(avg_distance_after), float(median_distance_before), float(median_distance_after), float(red_pixels), True))
                                        self.conn.commit()
                                else:
                                    self.alarm_finished.emit(self.numberThread)
                                    if self.conn != -1:
                                        self.cursor.execute("CALL insert_data(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.file_path, int(bubble_count_before), int(bubble_count_after), float(avg_distance_before), float(avg_distance_after), float(median_distance_before), float(median_distance_after), float(red_pixels), False))
                                        self.conn.commit()
                            else:
                                self.alarm_finished.emit(self.numberThread)
                                if self.conn != -1:
                                    self.cursor.execute("CALL insert_data(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.file_path, int(bubble_count_before), int(bubble_count_after), float(avg_distance_before), float(avg_distance_after), float(median_distance_before), float(median_distance_after), float(red_pixels), False))
                                    self.conn.commit()
                            
                            
             
                    height, width, channel = frame.shape
                    bytesPerLine = 3 * width
                    qImg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
                    qPixMap = QtGui.QPixmap.fromImage(qImg).scaled(self.graphics_view.size(), QtCore.Qt.KeepAspectRatio)
                    self.frame_processed.emit(qPixMap, self.graphics_view)
                    QtCore.QThread.msleep(delay)

                    if mode == 'img':
                        self.running = False
                else:
                    break
            if mode != 'img':
                cap.release()
        except Exception as e:
            print(e)
            

    def stop(self):
        self.running = False

    def pause(self):
        self.mutex.lock()
        self.paused = True
        self.mutex.unlock()

    def resume(self):
        self.mutex.lock()
        self.paused = False
        self.mutex.unlock()

    ###

    def flash_color(self, graphics_view):
        new_style = "background-color: red;"
        graphics_view.setStyleSheet(new_style)

    def restore_view(self, graphics_view):
        graphics_view.setStyleSheet("")

    ##
