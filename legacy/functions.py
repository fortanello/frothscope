from concurrent.futures import as_completed, ThreadPoolExecutor, ProcessPoolExecutor
import cv2
import torch
import numpy as np
from scipy.optimize import minimize

from sklearn.linear_model import LinearRegression

def read_settings():
    try:
        with open("settings.ini", "r") as file:
            lines = file.readlines()
                            
            settings_var0 = lines[0].split(';')[0].strip() # файл
            settings_var1 = lines[1].split(';')[0].strip() # номер кадра, с которого начинать обработку
            settings_var2 = lines[2].split(';')[0].strip() # мин.  интервал между кадрами (в секундах)
            settings_var3 = lines[3].split(';')[0].strip() # сколько кадров обрабатывать
            settings_var4 = lines[4].split(';')[0].strip() # мин. площадь пузырька (в пикселях)
            settings_var5 = lines[5].split(';')[0].strip() # макс. площадь пузырька (в пикселях)
            settings_var6 = lines[6].split(';')[0].strip() # бинаризация
            settings_var7 = lines[7].split(';')[0].strip() # контраст
            settings_var8 = lines[8].split(';')[0].strip() # антиблик
            settings_var9 = lines[9].split(';')[0].strip() # режим выделяемой области
            settings_var10 = lines[10].split(';')[0].strip() # координаты окна
            settings_var11 = lines[11].split(';')[0].strip() # количество точек на графиках
            settings_var12 = lines[12].split(';')[0].strip() # алгоритм синхронизации
            settings_var13 = lines[13].split(';')[0].strip() # на сколько делить
            settings_var14 = lines[14].split(';')[0].strip() # промежуток времени при синхронизации (delta t)
            settings_var15 = lines[15].split(';')[0].strip() # сколько кадров пропускать при распознвании
            settings_var15_1 = lines[16].split(';')[0].strip() # запаздывание
            settings_var15_2 = lines[17].split(';')[0].strip() # усредненное
            settings_var16 = lines[18].split(';')[0].strip() # режим (лаб. или завод.)
            settings_var17 = lines[101].split(';')[0].strip() # N
            settings_var18 = lines[106].split(';')[0].strip() # delaySync
            settings_var19 = lines[111].split(';')[0].strip() # peaks

        return {
            'filePath': settings_var0,
            'frameNumber': settings_var1,
            'framesInterval': settings_var2,
            'frame_count': settings_var3, 
            'min_bubble_area': settings_var4,    
            'max_bubble_area': settings_var5,
            'koefBin': settings_var6, 
            'koefContrast': settings_var7,
            'koefAntiGlare': settings_var8,
            'selectedAreaMode': settings_var9,
            'windowCoords': settings_var10,
            'pointsOnGraph': settings_var11,
            'syncMode': settings_var12,
            'R': settings_var13, 
            'delta_t': settings_var14,
            'skipFrames': settings_var15,
            'mode': settings_var16,
            'delay': settings_var15_1,
            'usr': settings_var15_2,
            'N': settings_var17,
            'delaySync': settings_var18,
            'peak': settings_var19
        } 
    except FileNotFoundError:
        print("Файл settings.ini не найден")

def read_settings_factory():
    try:
        with open("settings.ini", "r") as file:
            lines = file.readlines()

            #1          
            settings_var18 = lines[20].split(';')[0].strip() # ВКЛ
            settings_var19 = lines[21].split(';')[0].strip() # порт камеры
            settings_var20 = lines[22].split(';')[0].strip() # минимальная площадь пузырька (в пикселях)
            settings_var21 = lines[23].split(';')[0].strip() # максимальная площадь пузырька (в пикселях)
            settings_var22 = lines[24].split(';')[0].strip() # бинаризация
            settings_var23 = lines[25].split(';')[0].strip() # контраст
            settings_var24 = lines[26].split(';')[0].strip() # антиблик
            settings_var25 = lines[27].split(';')[0].strip() # мин. интервал между кадрами (в секундах)
            settings_var26 = lines[28].split(';')[0].strip() # T*
            settings_var26_0 = lines[29].split(';')[0].strip() # погрешность
            settings_var26_1 = lines[30].split(';')[0].strip() # запаздывание
            settings_var26_2 = lines[31].split(';')[0].strip() # усредненное
            settings_var27 = lines[32].split(';')[0].strip() # режим выделяемой области
            settings_var28 = lines[33].split(';')[0].strip() # координаты окна
            settings_var29 = lines[34].split(';')[0].strip() # количество точек на графиках
            settings_var30 = lines[35].split(';')[0].strip() # алгоритм синхронизации
            settings_var31 = lines[36].split(';')[0].strip() # на сколько делить при синхронизации
            settings_var32 = lines[37].split(';')[0].strip() # промежуток времени при синхронизации (delta_t)
            settings_var33 = lines[38].split(';')[0].strip() # сколько кадров пропускать при распознавании
            settings_var33_0 = lines[102].split(';')[0].strip()
            settings_var33_1 = lines[107].split(';')[0].strip()
            settings_var33_2 = lines[112].split(';')[0].strip()

            #2
            settings_var35 = lines[40].split(';')[0].strip() # ВКЛ
            settings_var36 = lines[41].split(';')[0].strip() # порт камеры
            settings_var37 = lines[42].split(';')[0].strip() # минимальная площадь пузырька (в пикселях)
            settings_var38 = lines[43].split(';')[0].strip() # максимальная площадь пузырька (в пикселях)
            settings_var39 = lines[44].split(';')[0].strip() # бинаризация
            settings_var40 = lines[45].split(';')[0].strip() # контраст
            settings_var41 = lines[46].split(';')[0].strip() # антиблик
            settings_var42 = lines[47].split(';')[0].strip() # мин. интервал между кадрами (в секундах)
            settings_var43 = lines[48].split(';')[0].strip() # T*
            settings_var43_0 = lines[49].split(';')[0].strip() # погрешность
            settings_var43_1 = lines[50].split(';')[0].strip() # запаздывание
            settings_var43_2 = lines[51].split(';')[0].strip() # усредненное
            settings_var44 = lines[52].split(';')[0].strip() # режим выделяемой области
            settings_var45 = lines[53].split(';')[0].strip() # координаты окна
            settings_var46 = lines[54].split(';')[0].strip() # количество точек на графиках
            settings_var47 = lines[55].split(';')[0].strip() # алгоритм синхронизации
            settings_var48 = lines[56].split(';')[0].strip() # на сколько делить при синхронизации
            settings_var49 = lines[57].split(';')[0].strip() # промежуток времени при синхронизации (delta_t)
            settings_var50 = lines[58].split(';')[0].strip() # сколько кадров пропускать при распознавании

            settings_var50_0 = lines[103].split(';')[0].strip()
            settings_var50_1 = lines[108].split(';')[0].strip()
            settings_var50_2 = lines[113].split(';')[0].strip()

            #3
            settings_var52 = lines[60].split(';')[0].strip() # ВКЛ
            settings_var53 = lines[61].split(';')[0].strip() # порт камеры
            settings_var54 = lines[62].split(';')[0].strip() # минимальная площадь пузырька (в пикселях)
            settings_var55 = lines[63].split(';')[0].strip() # максимальная площадь пузырька (в пикселях)
            settings_var56 = lines[64].split(';')[0].strip() # бинаризация
            settings_var57 = lines[65].split(';')[0].strip() # контраст
            settings_var58 = lines[66].split(';')[0].strip() # антиблик
            settings_var59 = lines[67].split(';')[0].strip() # мин. интервал между кадрами (в секундах)
            settings_var60 = lines[68].split(';')[0].strip() # T*
            settings_var60_0 = lines[69].split(';')[0].strip() # погрешность
            settings_var60_1 = lines[70].split(';')[0].strip() # запаздывание
            settings_var60_2 = lines[71].split(';')[0].strip() # усредненное
            settings_var61 = lines[72].split(';')[0].strip() # режим выделяемой области
            settings_var62 = lines[73].split(';')[0].strip() # координаты окна
            settings_var63 = lines[74].split(';')[0].strip() # количество точек на графиках
            settings_var64 = lines[75].split(';')[0].strip() # алгоритм синхронизации
            settings_var65 = lines[76].split(';')[0].strip() # на сколько делить при синхронизации
            settings_var66 = lines[77].split(';')[0].strip() # промежуток времени при синхронизации (delta_t)
            settings_var67 = lines[78].split(';')[0].strip() # сколько кадров пропускать при распознавании

            settings_var67_0 = lines[104].split(';')[0].strip()
            settings_var67_1 = lines[109].split(';')[0].strip()
            settings_var67_2 = lines[114].split(';')[0].strip()

            #4
            settings_var69 = lines[80].split(';')[0].strip() # ВКЛ
            settings_var70 = lines[81].split(';')[0].strip() # порт камеры
            settings_var71 = lines[82].split(';')[0].strip() # минимальная площадь пузырька (в пикселях)
            settings_var72 = lines[83].split(';')[0].strip() # максимальная площадь пузырька (в пикселях)
            settings_var73 = lines[84].split(';')[0].strip() # бинаризация
            settings_var74 = lines[85].split(';')[0].strip() # контраст
            settings_var75 = lines[86].split(';')[0].strip() # антиблик
            settings_var76 = lines[87].split(';')[0].strip() # мин. интервал между кадрами (в секундах)
            settings_var77 = lines[88].split(';')[0].strip() # T*
            settings_var77_0 = lines[89].split(';')[0].strip() # погрешность
            settings_var77_1 = lines[90].split(';')[0].strip() # запаздывание
            settings_var77_2 = lines[91].split(';')[0].strip() # усредненное
            settings_var78 = lines[92].split(';')[0].strip() # режим выделяемой области
            settings_var79 = lines[93].split(';')[0].strip() # координаты окна
            settings_var80 = lines[94].split(';')[0].strip() # количество точек на графиках
            settings_var81 = lines[95].split(';')[0].strip() # алгоритм синхронизации
            settings_var82 = lines[96].split(';')[0].strip() # на сколько делить при синхронизации
            settings_var83 = lines[97].split(';')[0].strip() # промежуток времени при синхронизации (delta_t)
            settings_var84 = lines[98].split(';')[0].strip() # сколько кадров пропускать при распознавании

            settings_var84_0 = lines[105].split(';')[0].strip()
            settings_var84_1 = lines[110].split(';')[0].strip()
            settings_var84_2 = lines[115].split(';')[0].strip()

            fullStatus = lines[100].split(';')[0].strip()

        return {
            'status': settings_var18,
            'status_2': settings_var35,
            'status_3': settings_var52,
            'status_4': settings_var69,
            
            'filePath': settings_var19,
            'filePath_2': settings_var36,
            'filePath_3': settings_var53,
            'filePath_4': settings_var70,

            'min_bubble_area': settings_var20,
            'min_bubble_area_2': settings_var37,
            'min_bubble_area_3': settings_var54,
            'min_bubble_area_4': settings_var71,

            'max_bubble_area': settings_var21,
            'max_bubble_area_2': settings_var38,
            'max_bubble_area_3': settings_var55,
            'max_bubble_area_4': settings_var72,

            'koefBin': settings_var22,
            'koefBin_2': settings_var39,
            'koefBin_3': settings_var56,
            'koefBin_4': settings_var73,

            'koefContrast': settings_var23,
            'koefContrast_2': settings_var40,
            'koefContrast_3': settings_var57,
            'koefContrast_4': settings_var74,

            'koefAntiGlare': settings_var24,
            'koefAntiGlare_2': settings_var41,
            'koefAntiGlare_3': settings_var58,
            'koefAntiGlare_4': settings_var75,

            'framesInterval': settings_var25,
            'framesInterval_2': settings_var42,
            'framesInterval_3': settings_var59,
            'framesInterval_4': settings_var76,

            'T': settings_var26,
            'T_2': settings_var43,
            'T_3': settings_var60,
            'T_4': settings_var77,

            'pogr': settings_var26_0,
            'pogr_2': settings_var43_0,
            'pogr_3': settings_var60_0,
            'pogr_4': settings_var77_0,

            'delay': settings_var26_1,
            'delay_2': settings_var43_1,
            'delay_3': settings_var60_1,
            'delay_4': settings_var77_1,

            'usr': settings_var26_2,
            'usr_2': settings_var43_2,
            'usr_3': settings_var60_2,
            'usr_4': settings_var77_2,
            

            'selectedAreaMode': settings_var27,
            'selectedAreaMode_2': settings_var44,
            'selectedAreaMode_3': settings_var61,
            'selectedAreaMode_4': settings_var78,

            'windowCoords': settings_var28,
            'windowCoords_2': settings_var45,
            'windowCoords_3': settings_var62,
            'windowCoords_4': settings_var79,

            'pointsOnGraph': settings_var29,
            'pointsOnGraph_2': settings_var46,
            'pointsOnGraph_3': settings_var63,
            'pointsOnGraph_4': settings_var80,

            'syncMode': settings_var30,
            'syncMode_2': settings_var47,
            'syncMode_3': settings_var64,
            'syncMode_4': settings_var81,
                
            'R': settings_var31,
            'R_2': settings_var48,
            'R_3': settings_var65,
            'R_4': settings_var82,
            
            'delta_t': settings_var32,
            'delta_t_2': settings_var49,
            'delta_t_3': settings_var66,
            'delta_t_4': settings_var83, 
        
            'skipFrames': settings_var33,
            'skipFrames_2': settings_var50,
            'skipFrames_3': settings_var67,
            'skipFrames_4': settings_var84,

            'N': settings_var33_0,
            'N_2': settings_var50_0,
            'N_3': settings_var67_0,
            'N_4': settings_var84_0,
            
            'delaySync': settings_var33_1,
            'delaySync_2': settings_var50_1,
            'delaySync_3': settings_var67_1,
            'delaySync_4': settings_var84_1,

            'peak': settings_var33_2,
            'peak_2': settings_var50_2,
            'peak_3': settings_var67_2,
            'peak_4': settings_var84_2,

            'fullStatus': fullStatus,
    } 
    except FileNotFoundError:
        print("Файл settings.ini не найден")

def getMode(file_path, frame_count):
    frame = None
    if check_digits(file_path):
        mode = 'cam'
    else:
       ext = file_path.split(".")[-1] 
       if ext.lower() in ['jpg', 'png', 'jpeg']:
           mode = 'img'
       elif ext.lower() in ['avi', 'mpeg', 'mpg', 'mp4']:
            mode = 'video'
    
    if mode == 'video' or mode == 'cam':
        cap = cv2.VideoCapture(file_path)
        if frame_count == 0:
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    elif mode == 'img':
        frame = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        cap = -1
    return mode, frame, frame_count, cap

def getSize(x, y, w, h, frame2):
    if x == 0 and y == 0 and w == 0 and h == 0:
        cimg = frame2.copy()
    else:
        cimg = frame2[y:y+h, x:x+w].copy()
    cimg = frame2[y:y+h, x:x+w].copy()

    cimg_height, cimg_width, _ = cimg.shape
    if cimg_height == 0 or cimg_width == 0:
        cimg = frame2
    return cimg

def detect_bubbles(binary, min_area, max_area):
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bubble_count = 0
    centers = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            bubble_count += 1
            M = cv2.moments(contour)
            if M["m00"] != 0:  # избегаем деления на ноль
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centers.append((cX, cY))
    return bubble_count, centers


def count_red_pixels(image):
    
    red_channel = image[:, :, 2]  # В OpenCV цветовая модель BGR, поэтому 2 - это красная компонента

    red_count = np.count_nonzero(red_channel)

    total_red_value = np.sum(red_channel)

    average_red_value = total_red_value / (image.shape[0] * image.shape[1])
    return average_red_value

def calculate_distances(bubble_centers):
    if len(bubble_centers) < 2:
        return None, None  # Меньше 2 пузырьков - нечего измерять
    distances = []
    for i in range(len(bubble_centers)):
        for j in range(i + 1, len(bubble_centers)):
            distance = np.sqrt((bubble_centers[i][0] - bubble_centers[j][0]) ** 2 +
                               (bubble_centers[i][1] - bubble_centers[j][1]) ** 2)
            distances.append(distance)
            
    mean_distance = np.mean(distances) if distances else None
    median_distance = np.median(distances) if distances else None
    return mean_distance, median_distance

def draw_detected_glare(image, koefBin, min_area, max_area):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, koefBin, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    count = 0
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if min_area < max_area:
            if area > min_area and area < max_area: 
                cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
            #cv2.putText(image, str(count), tuple(contour[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
            count += 1
    return image

def check_digits(input_str):
    return all(char.isdigit() and int(char) >= 0 and int(char) <= 9 for char in input_str)
def process_threshold(thresh_value, cimgGray, min_bubble_area, max_bubble_area):
    _, thresholded_img = cv2.threshold(cimgGray, thresh_value, 255, cv2.THRESH_BINARY)
    bubble_count, _ = detect_bubbles(thresholded_img, min_bubble_area, max_bubble_area)
    return thresh_value, bubble_count

def process_contrast(contrast_value, cimgCopy, koefBin, min_bubble_area, max_bubble_area):
    lab = cv2.cvtColor(cimgCopy, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=contrast_value, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)
    limg = cv2.merge((cl, a, b))
    cimg3 = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    cimgGray = cv2.cvtColor(cimg3, cv2.COLOR_BGR2GRAY)
    _, thresholded_img = cv2.threshold(cimgGray, koefBin, 255, cv2.THRESH_BINARY)
    bubble_count, _ = detect_bubbles(thresholded_img, min_bubble_area, max_bubble_area)
    return contrast_value, bubble_count

def process_antiglare(antiGlareValue, cimg4, koefBin, min_bubble_area, max_bubble_area):
    cimgGray = cv2.cvtColor(cimg4, cv2.COLOR_BGR2GRAY)
    cimg4_1 = cimg4.copy()

    _, thresholded_img = cv2.threshold(cimgGray, antiGlareValue, 255, cv2.THRESH_BINARY_INV)
    mask = (thresholded_img == 255)

    cimg4_1[mask] = (255, 255, 255)

    cimgGray = cv2.cvtColor(cimg4_1, cv2.COLOR_BGR2GRAY)
    _, thresholded_img = cv2.threshold(cimgGray, koefBin, 255, cv2.THRESH_BINARY)
    
    bubble_count, _ = detect_bubbles(thresholded_img, min_bubble_area, max_bubble_area)

    return antiGlareValue, bubble_count

## new 22.03.2025
'''
def binary_search_threshold(cimgGray, min_bubble_area, max_bubble_area, max_bubble_count, low=80, high=245):
    best_thresh = low

    while low <= high:
        mid = (low + high) // 2
        _, bubble_count = process_threshold(mid, cimgGray, min_bubble_area, max_bubble_area)

        if bubble_count > max_bubble_count:
            max_bubble_count = bubble_count
            best_thresh = mid

        
        _, left_count = process_threshold(mid - 1, cimgGray, min_bubble_area, max_bubble_area)
        _, right_count = process_threshold(mid + 1, cimgGray, min_bubble_area, max_bubble_area)

        if left_count > max_bubble_count:
            max_bubble_count = left_count
            best_thresh = mid - 1
        if right_count > max_bubble_count:
            max_bubble_count = right_count
            best_thresh = mid + 1

        
        if left_count > bubble_count:
            high = mid - 1
        else:
            low = mid + 1

    return best_thresh, max_bubble_count
'''
def binary_search_threshold(cimgGray, min_bubble_area, max_bubble_area, max_bubble_count, low=80, high=245):
    best_thresh = low
    best_count = 0

    while low <= high:
        mid = (low + high) // 2
        _, bubble_count = process_threshold(mid, cimgGray, min_bubble_area, max_bubble_area)

        # Обновляем лучшее значение, если нашли больше пузырей
        if bubble_count > best_count:
            best_count = bubble_count
            best_thresh = mid

        # Если количество пузырей превышает максимальное - ищем более высокий порог
        if bubble_count > max_bubble_count:
            low = mid + 1
        else:
            high = mid - 1

    return best_thresh, best_count

def find_optimal_threshold(cimgGray, min_bubble_area, max_bubble_area, max_bubble_count, low=80, high=244):
    best_thresh = low
    max_count = max_bubble_count
    
    while low <= high:
        mid = (low + high) // 2
        _, count_mid = process_threshold(mid, cimgGray, min_bubble_area, max_bubble_area)
        _, count_mid_plus = process_threshold(mid + 1, cimgGray, min_bubble_area, max_bubble_area)
        
        if count_mid < count_mid_plus:
            low = mid + 1
            if count_mid_plus > max_count:
                max_count = count_mid_plus
                best_thresh = mid + 1
        else:
            high = mid - 1
            if count_mid > max_count:
                max_count = count_mid
                best_thresh = mid
                
    return best_thresh, max_count

def binary_search_antiglare(cimg, koefBin, min_bubble_area, max_bubble_area, max_bubble_count, low=0, high=120):
    best_antiglare = low

    while low <= high:
        mid = (low + high) // 2
        _, bubble_count = process_antiglare(mid, cimg, koefBin, min_bubble_area, max_bubble_area)

        if bubble_count > max_bubble_count:
            max_bubble_count = bubble_count
            best_antiglare = mid


        _, left_count = process_antiglare(mid - 1, cimg, koefBin, min_bubble_area, max_bubble_area)
        _, right_count = process_antiglare(mid + 1, cimg, koefBin, min_bubble_area, max_bubble_area)

        if left_count > max_bubble_count:
            max_bubble_count = left_count
            best_antiglare = mid - 1
        if right_count > max_bubble_count:
            max_bubble_count = right_count
            best_antiglare = mid + 1


        if left_count > bubble_count:
            high = mid - 1
        else:
            low = mid + 1

    return best_antiglare, max_bubble_count

def process_frame(frameno, cimg, settings):
    try:
        idx = int(settings['idx'])
        frameno = int(settings['frameno'])
        koefBin = int(settings['koefBin'])
        koefContrast = int(settings['koefContrast'])
        koefAntiGlare = int(settings['koefAntiGlare'])
        min_bubble_area = int(settings['min_bubble_area'])
        max_bubble_area = int(settings['max_bubble_area'])
        framesArray = settings['framesArray']
        
        avgBeforeArray = settings['avgBeforeArray']
        avgAfterArray = settings['avgAfterArray']
        medianBeforeArray = settings['medianBeforeArray']
        medianAfterArray = settings['medianAfterArray']
        red_pixelsArray = settings['red_pixelsArray']
       
        bubblesBeforeArray = settings['bubblesBeforeArray']
        bubblesAfterArray = settings['bubblesAfterArray']

        processedFrame = int(settings['processedFrame'])
        framesProcessedArray = settings['framesProcessedArray']

        koefBin_values = settings['koefBin_values']
        koefBin_values2 = settings['koefBin_values2']
        koefContrast_values = settings['koefContrast_values']
        koefAntiGlare_values = settings['koefAntiGlare_values']
        points = int(settings['pointsOnGraph'])

        cimgCopy = cimg.copy()
        if len(framesProcessedArray) < points:
            processedFrame += 1
            framesProcessedArray.append(int(processedFrame))

        if koefBin == -1:
            koefBin_values = []
            import time
            first_time = time.time()
            
            
            profile_updates = []
            max_bubble_count = 0
            cimgGray = cv2.cvtColor(cimgCopy, cv2.COLOR_BGR2GRAY)
            #koefBin, max_bubble_count = binary_search_threshold(cimgGray, min_bubble_area, max_bubble_area, max_bubble_count)
            
            for i in range(80, 245):
                _, bubble_count = process_threshold(i, cimgGray, min_bubble_area, max_bubble_area)
                koefBin_values.append((i, bubble_count))
                if bubble_count > max_bubble_count:
                    max_bubble_count = bubble_count
                    koefBin = i
            
                        
            #print(1)
            if koefContrast == -1:
                koefBin_values2 = []
                koefContrast_values = []
            
                profile_updates.clear()
                
                for i in range(1, 10):
                    _, bubble_count = process_contrast(i, cimgCopy, koefBin, min_bubble_area, max_bubble_area)
                    koefContrast_values.append((i, bubble_count))
                    if bubble_count > max_bubble_count:
                        max_bubble_count = bubble_count
                        koefContrast = i 

            #print(2)            
            cimg3 = cimgCopy.copy()
            if koefContrast != -1 and koefContrast != 0:
                
                lab = cv2.cvtColor(cimgCopy, cv2.COLOR_BGR2LAB)
                l_channel, a, b = cv2.split(lab)
                clahe = cv2.createCLAHE(clipLimit=koefContrast, tileGridSize=(8, 8))
                cl = clahe.apply(l_channel)
                limg = cv2.merge((cl, a, b))
                cimg3 = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
                
                
                cimgGray = cv2.cvtColor(cimg3, cv2.COLOR_BGR2GRAY)
                
                for i in range(80, 245):
                    _, bubble_count = process_threshold(i, cimgGray, min_bubble_area, max_bubble_area)
                    koefBin_values2.append((i, bubble_count))
                    if bubble_count > max_bubble_count:
                        max_bubble_count = bubble_count
                        koefBin = i
                
                #koefBin, max_bubble_count = find_optimal_threshold(cimgGray, min_bubble_area, max_bubble_area, max_bubble_count)
                # step = 5
                # for i in range(80, 245, step):
                #     _, bubble_count = process_threshold(i, cimgGray, min_bubble_area, max_bubble_area)
                #     koefBin_values2.append((i, bubble_count))
                #     if bubble_count > max_bubble_count:
                #         max_bubble_count = bubble_count
                #         koefBin = i

                # Уточнение вблизи найденного значения
                # refined_range = range(max(80, koefBin - step), min(245, koefBin + step))
                # for i in refined_range:
                #     _, bubble_count = process_threshold(i, cimgGray, min_bubble_area, max_bubble_area)
                #     #koefBin_values2.append((i, bubble_count))
                #     if bubble_count > max_bubble_count:
                #         max_bubble_count = bubble_count
                #         koefBin = i
                
                
            #print(3)    
            if koefAntiGlare == -1:
                koefAntiGlare_values = []
                profile_updates.clear()
                #koefAntiGlare, max_bubble_count = binary_search_antiglare(cimg3, koefBin, min_bubble_area, max_bubble_area, max_bubble_count)
              
                for i in range(0, 120):
                    _, bubble_count = process_antiglare(i, cimg3, koefBin, min_bubble_area, max_bubble_area)
                    koefAntiGlare_values.append((i, bubble_count))
                    if bubble_count > max_bubble_count:
                        max_bubble_count = bubble_count
                        koefAntiGlare = i
              
            
                

                

            #print(4)
            print('t = ', time.time() - first_time)
            with open("settings.ini", "r") as file:
                lines = file.readlines()
                
            match idx:
                case 0:
                    lines[6] = str(koefBin) + " ; коэффициент бинаризации\n"
                    lines[7] = str(koefContrast) + " ; параметр контрастности\n"
                    lines[8] = str(koefAntiGlare) + " ; антиблик\n"
                case 1:
                    lines[24] = str(koefBin) + " ; коэффициент бинаризации\n"
                    lines[25] = str(koefContrast) + " ; параметр контрастности\n"
                    lines[26] = str(koefAntiGlare) + " ; антиблик\n"
                case 2:
                    lines[44] = str(koefBin) + " ; коэффициент бинаризации\n"
                    lines[45] = str(koefContrast) + " ; параметр контрастности\n"
                    lines[46] = str(koefAntiGlare) + " ; антиблик\n"
                case 3:
                    lines[64] = str(koefBin) + " ; коэффициент бинаризации\n"
                    lines[65] = str(koefContrast) + " ; параметр контрастности\n"
                    lines[66] = str(koefAntiGlare) + " ; антиблик\n"
                case 4:
                    lines[84] = str(koefBin) + " ; коэффициент бинаризации\n"
                    lines[85] = str(koefContrast) + " ; параметр контрастности\n"
                    lines[86] = str(koefAntiGlare) + " ; антиблик\n"

            with open("settings.ini", "w") as file:
                file.writelines(lines)

            

        
        cimgCopy6 = cimgCopy.copy()
           
        if koefContrast != 0 and koefContrast != -1:
            
            lab = cv2.cvtColor(cimgCopy6, cv2.COLOR_BGR2LAB)
            l_channel, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=koefContrast, tileGridSize=(8,8))
            cl = clahe.apply(l_channel)
            limg = cv2.merge((cl,a,b))
            cimgCopy6 = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        
        cimgGray = cv2.cvtColor(cimgCopy6, cv2.COLOR_BGR2GRAY)
        _, thresholded_img = cv2.threshold(cimgGray, koefBin, 255, cv2.THRESH_BINARY)
        bubble_count_before, centers = detect_bubbles(thresholded_img, min_bubble_area, max_bubble_area)
        avg_distance_before, median_distance_before = calculate_distances(centers)
        red_pixels = count_red_pixels(cimgCopy6)
        red_pixelsArray.append(red_pixels)
         
        avgBeforeArray.append(avg_distance_before)
        medianBeforeArray.append(median_distance_before)
        bubblesBeforeArray.append(bubble_count_before)
        
        if koefAntiGlare != 0 and koefAntiGlare != -1:
            cimgGray = cv2.cvtColor(cimgCopy6, cv2.COLOR_BGR2GRAY)
            _, thresholded_img = cv2.threshold(cimgGray, koefAntiGlare, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(thresholded_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for i, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if min_bubble_area < max_bubble_area:
                    if area > min_bubble_area and area < max_bubble_area:
                        cv2.drawContours(cimgCopy6, [contour], -1, (255, 255, 255), -1)
          
        cimgGray = cv2.cvtColor(cimgCopy6, cv2.COLOR_BGR2GRAY)
        _, thresholded_img = cv2.threshold(cimgGray, koefBin, 255, cv2.THRESH_BINARY)
        bubble_count_after, centers = detect_bubbles(thresholded_img, min_bubble_area, max_bubble_area)

        avg_distance_after, median_distance_after = calculate_distances(centers)
        avgAfterArray.append(avg_distance_after)
        medianAfterArray.append(median_distance_after)

        bubblesAfterArray.append(bubble_count_after)
        framesArray.append(int(frameno))
        
        
        return {
            'framesArray': framesArray, 
            'avgBeforeArray': avgBeforeArray, 
            'avgAfterArray': avgAfterArray,    
            'medianBeforeArray': medianBeforeArray,
            'medianAfterArray': medianAfterArray, 
            'red_pixelsArray': red_pixelsArray,
            'bubblesBeforeArray': bubblesBeforeArray,
            'bubblesAfterArray': bubblesAfterArray, 
            'thresholded_img': thresholded_img,
            'cimgCopy6': cimgCopy6,
            'processedFrame': processedFrame,
            'framesProcessedArray': framesProcessedArray,
            'bubble_count_before': bubble_count_before,
            'bubble_count_after': bubble_count_after,
            'avg_distance_before': avg_distance_before,
            'avg_distance_after': avg_distance_after,
            'red_pixels': red_pixels,
            'median_distance_before': median_distance_before,
            'median_distance_after': median_distance_after,
            'koefBin_values': koefBin_values,
            'koefBin_values2': koefBin_values2,
            'koefContrast_values': koefContrast_values,
            'koefAntiGlare_values': koefAntiGlare_values
        }
    except Exception:
        pass

def to_cuda(model):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'  # Проверка на наличие CUDA
    device = 'cpu'
    model.to(device) # Перемещение модели на GPU, если доступно
    return model



def is_penogon(model, frame, coordsMode, windowCoords):
    #print(frame, '0')
    penogon = False

    if windowCoords == '-1':
        mask = np.ones(frame.shape[:2], dtype=np.uint8) * 255  # Маска для всего изображения
        polygon = np.array([[0, 0], [frame.shape[1], 0], [frame.shape[1], frame.shape[0]], [0, frame.shape[0]]], dtype=np.int32)
    else:
        if coordsMode == '0':
            x, y, w, h = map(int, windowCoords.split())
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            polygon = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], dtype=np.int32)
            cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
        else:
            coords_str = windowCoords.strip()
            coords = coords_str.split()
            polygon_points = []
            for i in range(0, len(coords), 2):
                x = int(coords[i])
                y = int(coords[i + 1])
                polygon_points.append((x, y))
            polygon = np.array(polygon_points, dtype=np.int32)
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)

            cv2.fillPoly(mask, [polygon], 255)
    
    try:
        results = model.predict(frame, conf=0.25, imgsz=640, verbose=False, classes=1)
        if results is None or len(results) == 0 or results[0].masks is None:
            penogon = True
            return frame, penogon
        contoursMask = []
        masks = results[0].masks.data.cpu().numpy().astype(int)
        for mask in masks:
            mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)
            mask_contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            frame = cv2.drawContours(frame, mask_contours, -1, (255, 0, 0), 5)

            contoursMask.extend(mask_contours)

        #pon_polygon = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], dtype=np.int32)
        for contour in contoursMask:
            mask_polygon = cv2.convexHull(contour)
            
            if cv2.intersectConvexConvex(mask_polygon, polygon)[0]: 
                penogon = True
                break
    except Exception as ex:
        penogon = True
        print(ex)
        #print('pon')
    
    return frame, penogon


def calculate_illumination(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return np.mean(gray_frame)

def onul_func(delay, usr, array3_timeStart, array2_count):
    i_fix = -1
    cnt1 = 0
    sum1 = 0
    for i in range(len(array3_timeStart)):
        if array3_timeStart[i] > delay:
            i_fix = i
            break
    if i_fix != -1:
        if i_fix - usr >= 0:
            startIndex = i_fix - usr
            endIndex = i_fix
        else:
            startIndex = 0
            endIndex = usr
        for i in range(startIndex, endIndex):
            sum1 += array2_count[i]
            cnt1 += 1
    else:
        return 0
    avg = sum1 / cnt1
    return avg

def oed_func(delay, usr, array3_timeStart, array2_count):
    i_fix = -1
    sum1 = 0
    cnt1 = 0
    for i in range(len(array3_timeStart)):
        if array3_timeStart[i] > delay:
            i_fix = i
            break
    #print(i_fix)
    if len(array3_timeStart) - i_fix > usr:
        for k in range(i_fix + usr - 1, len(array3_timeStart)):
            sum1 += array2_count[k]
            cnt1 += 1
    else:
        for k in range(len(array3_timeStart) - usr - 1, len(array3_timeStart)):
            sum1 += array2_count[k]
        cnt1 = usr
            
    avg = sum1 / cnt1
        
    return avg


'''
def doit(delay, usr, array1_time, array2_count):
    try:
    
        #print('len = ', len(array1_time), 'usr = ', usr)
        if len(array1_time) >= usr and array1_time[-1] > delay:
            initial_T = 10
            
            array3_timeStart = [t - array1_time[0] for t in array1_time]
            onul = onul_func(delay, usr, array3_timeStart, array2_count)
            oed = oed_func(delay, usr, array3_timeStart, array2_count)
            #print('onul =',onul, 'oed = ', oed)
            
            
            array4_timeWithDelay = [
                max(0, t - delay) for t in array3_timeStart
            ]
            
            array5_countNorm = [
                (c - onul) / (oed - onul) for c in array2_count
            ]
            
            array6_countNormWithDelay = [
                array5_countNorm[i] if array3_timeStart[i] > delay else 0 for i in range(len(array3_timeStart))
            ]
            
            
            def cost_function(T):
                array7_process = [
                    1 * (1 - np.exp((-1 * delay_time) / T)) if T != 0 else 99999999
                    for delay_time in array4_timeWithDelay
                ]

                array8_pogr = [
                    (process - count_norm) ** 2 for process, count_norm in zip(array7_process, array6_countNormWithDelay)
                ]

                return sum(array8_pogr)
            bounds = [(1e-10, None)]
            result = minimize(cost_function, initial_T)

            optimal_T = result.x[0]
            optimal_sum_pogr = result.fun
            #print('T =', optimal_T)
            return optimal_T
        return None
    except Exception:
        pass
'''
def doit(delay, usr, array1_time, array2_count):
    try:
        # Преобразуем входные массивы в NumPy массивы
        array1_time = np.array(array1_time)
        array2_count = np.array(array2_count)

        if len(array2_count) == 300:
            with open("count.txt", "w", encoding="utf-8") as file:
                for line in array2_count:
                    file.write(str(line) + "\n")
            with open("time.txt", "w", encoding="utf-8") as file:
                for line in array1_time:
                    file.write(str(line) + "\n")

        if len(array1_time) < usr:
            return None

        if len(array1_time) >= usr and array1_time[-1] > delay:
                    
            array3_timeStart = array1_time - array1_time[0]
            onul = onul_func(delay, usr, array3_timeStart, array2_count)
            oed = oed_func(delay, usr, array3_timeStart, array2_count)

            array4_timeWithDelay = np.maximum(0, array3_timeStart - delay)
            
            array5_countNorm = (array2_count - onul) / (oed - onul)
            
            array6_countNormWithDelay = np.where(array3_timeStart > delay, array5_countNorm, 0)


            def cost_function(T):
                try:                    
                    array7_process = np.where(T > 1, 1 * (1 - np.exp((-1 * array4_timeWithDelay) / T)), 9999999)
                    
                    array8_pogr = np.square(array7_process - array6_countNormWithDelay)
                    
                    return np.sum(array8_pogr)
                except:
                    return 999999999999

            #bounds = [(1, np.inf)]
            initial_T = 10
            result = minimize(cost_function, initial_T)
            optimal_T = result.x[0]

            if optimal_T == 10:
                return np.inf

            #optimal_T = result.x[0]
            #optimal_sum_pogr = result.fun
            return optimal_T
        return None
    except Exception as e:
        print(f"An error occurred: {e}")


