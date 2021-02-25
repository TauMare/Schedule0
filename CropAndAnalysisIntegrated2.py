import cv2
from pdf2image import convert_from_path
import pyautogui
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import pytesseract
import datetime
import os
from iteration_utilities import unique_everseen
from iteration_utilities import duplicates

now = datetime.datetime.now()
todaysdayNum = now.isoweekday()

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
config = '--oem 3 --psm 6'

# Переводим PDF в изображение с названием PDFtoImagePicture
pages = convert_from_path('pdfs/testfile6.pdf', 500, poppler_path=r"C:\Program Files\poppler-21.01.0\Library\bin")
for page in pages:
    page.save('firstcropimg/ProcessingImages/PDFtoImagePicture.png', 'PNG')

testingweekdays_image_grayscale = cv2.imread('firstcropimg/ProcessingImages/PDFtoImagePicture.png', cv2.IMREAD_GRAYSCALE)
# _, threshold = cv2.threshold(testingweekdays_image_grayscale, 110, 255, cv2.THRESH_BINARY)
# contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
canny = cv2.Canny(testingweekdays_image_grayscale, 125, 175)
contours, hierarchies = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
testDaysList = []
testCropNumCounterMarked = 0
for cnt in contours:
    x, y, w, h = bbox = cv2.boundingRect(cnt)
    if 1000 < h < 2000 and w < 300:
        x = bbox[0]
        y = bbox[1]
        w = bbox[2]
        h = bbox[3]
        crop_img = testingweekdays_image_grayscale[y: y + h, x: x + w].copy()
        cv2.imwrite("firstcropimg/ProcessingImages/weekdaycropped" + str(testCropNumCounterMarked) + ".png", crop_img)
        rotating_image = Image.open("firstcropimg/ProcessingImages/weekdaycropped" + str(testCropNumCounterMarked) + ".png")
        rotated_image = rotating_image.transpose(Image.ROTATE_270)
        data = pytesseract.image_to_string(rotated_image, lang="rus+eng", config=config)
        dataClear = data.replace("\n\x0c", "")
        testDaysList.append(dataClear)
        testCropNumCounterMarked += 1
print("testDaysList")
NewList = list(unique_everseen(testDaysList))
print(NewList)
NewList.reverse()
testDaysList.reverse()
# testDaysList.
print(testDaysList)



daysDict = {
    1: "ПОНЕДЕЛЬНИК",
    2: "ВТОРНИК",
    3: "СРЕДА",
    4: "ЧЕТВЕРГ",
    5: "ПЯТНИЦА",
    6: "СУББОТА",
    7: "ВОСКРЕСЕНЬЕ",
    8: "ПОНЕДЕЛЬНИК",
    9: "ВТОРНИК",
    10: "СРЕДА",
    11: "ЧЕТВЕРГ",
    12: "ПЯТНИЦА",
    13: "СУББОТА"
}
print(daysDict[todaysdayNum])

FoundDateInList = "День не был найден"
foundIndex = 0
elementcounter = 0
for element in NewList:
    if element.find(daysDict[todaysdayNum+1]) != -1: #к сегодняшнему дню можно докинуть цифр чтобы чекать завтрашний день
        FoundDateInList = element
        foundIndex = elementcounter
    elementcounter += 1
print("FoundDateInList")
print(FoundDateInList)
print("foundIndex")
print(foundIndex)
# Прописать, чтобы корректно обрабатывалось воскресенье
if daysDict[todaysdayNum+2] != daysDict[7] and FoundDateInList != "День не был найден":
# Проверяем, есть ли в изображении PDFtoImagePicture примитивные основные контуры и отрисовываем их в случае нахождения
# После - сохраняем файл с обведенными найденными контурами, обрезаем по каждому контуру и сохраняем с названием intelcropped(i)
    intelPictureBeforeFirstCrop_colored = cv2.imread('firstcropimg/ProcessingImages/PDFtoImagePicture.png', cv2.IMREAD_COLOR)
    intelPictureBeforeFirstCrop_grayscale = cv2.imread('firstcropimg/ProcessingImages/PDFtoImagePicture.png', cv2.IMREAD_GRAYSCALE)
    canny = cv2.Canny(intelPictureBeforeFirstCrop_grayscale, 125, 175)
    contours, hierarchies = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    DaysList = []
    if len(contours) == 1 or len(contours) == 2:
        CropNumCounterMarked = 0
        for cnt in contours:
            x, y, w, h = bbox = cv2.boundingRect(cnt)
            crop_img = cv2.drawContours(intelPictureBeforeFirstCrop_grayscale, contours, -1, (0, 255, 255), 20)
            # cv2.imwrite("firstcropimg/ProcessingImages/intelsadda.png",crop_img)
            crop_img = intelPictureBeforeFirstCrop_grayscale[y: y + h, x: x + w].copy()  # (x1, y1) будет верхний левый угол и (x2, y2) внизу справа.[y1:y2, x1:x2]
            cv2.imwrite("firstcropimg/ProcessingImages/intelcropped" + str(CropNumCounterMarked) + ".png", crop_img)
            CropNumCounterMarked += 1

        ImageName = "firstcropimg/ProcessingImages/intelcropped0.png"
        print("CropNumCounterMarked")
        print(CropNumCounterMarked)
        if CropNumCounterMarked >= 2:
            intelCropped0 = Image.open('firstcropimg/ProcessingImages/intelcropped1.png')
            width_intelCropped0, height_intelCropped0 = intelCropped0.size
            intelCropped1 = Image.open('firstcropimg/ProcessingImages/intelcropped0.png')
            width_intelCropped1, height_intelCropped1 = intelCropped1.size

            img = Image.new('RGB', (width_intelCropped0, height_intelCropped0 + height_intelCropped1))

            img.paste(intelCropped0, (0, 0))
            img.paste(intelCropped1, (0, height_intelCropped0))

            ImageName = "firstcropimg/ProcessingImages/intelcropped-first.png"
            img.save(ImageName)
        print(ImageName)
### Проверяем, есть ли в изображении PDFtoImagePicture примитивные основные контуры и отрисовываем их в случае нахождения ###
### После - сохраняем файл с обведенными найденными контурами, обрезаем по каждому контуру и сохраняем с названием intelcropped(i) ###
        intelPictureAfterFirstCrop_colored = cv2.imread(ImageName, cv2.IMREAD_COLOR)
        intelPictureAfterFirstCrop_grayscale = cv2.imread(ImageName, cv2.IMREAD_GRAYSCALE)
        canny = cv2.Canny(intelPictureAfterFirstCrop_grayscale, 125, 175)
        contours, hierarchies = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print("Я нашел " + str(len(contours)) + " контуров")
        CropNumCounterMarked = 0
        for cnt in contours:
            x, y, w, h = bbox = cv2.boundingRect(cnt)
            if 1000 < h < 3000 and w < 400:
                x = bbox[0]
                y = bbox[1]
                w = bbox[2]
                h = bbox[3]
                start_point = (x, y)
                end_point = (x+w, y+h)
                color = (255, 0, 0)
                img_height, img_width, channels = intelPictureAfterFirstCrop_colored.shape
                thickness = 5
                intelPictureAfterFirstCrop_colored = cv2.rectangle(intelPictureAfterFirstCrop_colored, start_point, end_point, color, thickness)
                intelPictureAfterFirstCrop_colored = cv2.rectangle(intelPictureAfterFirstCrop_colored, (x+img_width-80, y+h-20), (x+img_width-40, y+h-60), (0, 0, 255), -1)
                intelPictureAfterFirstCrop_colored = cv2.circle(intelPictureAfterFirstCrop_colored, (x+110, y+50), 40, color, -1)
        cv2.imwrite('firstcropimg/ProcessingImages/intelPictureAfterFirstCrop.png', intelPictureAfterFirstCrop_colored)

        somevar = list(pyautogui.locateAll("firstcropimg/Marks/Circlemark1.png", "firstcropimg/ProcessingImages/intelPictureAfterFirstCrop.png", confidence = 0.99))
        somelist = []
        FilterList = []
        i=0
        for element in somevar:
            sth = somevar[i]
            i += 1
            sth = str(sth)
            sth=sth.replace("Box(","")
            sth=sth.replace(")","")
            sth=sth.replace(" ","")
            sth = sth.split(",")

            x1 = int(str(sth[0]).replace("left=",""))
            y1 = int(str(sth[1]).replace("top=",""))
            x2 = int(str(sth[2]).replace("width=",""))
            y2 = int(str(sth[3]).replace("height=",""))
            FilterListObj = str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2)
            FilterListObj.replace("94,", "")
            FilterListObj.replace("91,", "")
            FilterList.append(FilterListObj)

        somevar2 = list(pyautogui.locateAll("firstcropimg/Marks/Squaremark2.png", "firstcropimg/ProcessingImages/intelPictureAfterFirstCrop.png", confidence = 0.99))
        FilterList2 = []
        i=0
        for element in somevar2:
            sth = somevar2[i]
            i += 1
            sth = str(sth)
            sth=sth.replace("Box(","")
            sth=sth.replace(")","")
            sth=sth.replace(" ","")
            sth = sth.split(",")

            x1 = int(str(sth[0]).replace("left=",""))
            y1 = int(str(sth[1]).replace("top=",""))
            x2 = int(str(sth[2]).replace("width=",""))
            y2 = int(str(sth[3]).replace("height=",""))
            FilterListObj2 = str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2)
            FilterList2.append(FilterListObj2)

        print("Найденные элементы в списке FilterList " + str(FilterList))
        print("Найденные элементы в списке FilterList2 " + str(FilterList2))

        FirstTableCoords_circle = FilterList[foundIndex].split(",")
        FirstTableCoords_square = FilterList2[foundIndex].split(",")

        print("Координаты найденного круга " + str(FirstTableCoords_circle))
        print("Координаты найденного квадрата " + str(FirstTableCoords_square))

        x1 = int(FirstTableCoords_circle[0]) + int(FirstTableCoords_circle[2])*2-20
        y1 = int(FirstTableCoords_circle[1]) #+ int(FirstTableCoords_circle[2])*2
        x2 = int(FirstTableCoords_square[0]) + int(FirstTableCoords_square[2])
        y2 = int(FirstTableCoords_square[1]) + int(FirstTableCoords_square[3])

        print("x1 " + str(x1))
        print("y1 " + str(y1))
        print("x2 " + str(x2))
        print("y2 " + str(y2))

        intelPictureAfterFirstCrop_grayscale = cv2.imread(ImageName, cv2.IMREAD_GRAYSCALE)
        crop_img = intelPictureAfterFirstCrop_grayscale[y1:y2, x1:x2]
        cv2.imwrite("firstcropimg/ProcessingImages/finallyCroppedAndPreparedToAnalyze.png", crop_img)

        font = cv2.FONT_HERSHEY_COMPLEX
        intelPictureAfterFirstCrop_colored = cv2.imread('firstcropimg/ProcessingImages/finallyCroppedAndPreparedToAnalyze.png', cv2.IMREAD_COLOR)
        intelPictureAfterFirstCrop_grayscale = cv2.imread('firstcropimg/ProcessingImages/finallyCroppedAndPreparedToAnalyze.png', cv2.IMREAD_GRAYSCALE)
        _, threshold = cv2.threshold(intelPictureAfterFirstCrop_grayscale, 110, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            cv2.drawContours(intelPictureAfterFirstCrop_colored, contours, -1, (0, 0, 0), 3)
            x, y, w, h = bbox = cv2.boundingRect(cnt)
        cv2.imwrite('processingimages/intelPictureWithCorrectedContours.png', intelPictureAfterFirstCrop_colored)

        intelPictureWithCorrectedContoursProcessing_colored = cv2.imread('processingimages/intelPictureWithCorrectedContours.png',
                                                                         cv2.IMREAD_COLOR)
        intelPictureWithCorrectedContoursProcessing_grayscale = cv2.imread('processingimages/intelPictureWithCorrectedContours.png',
                                                                           cv2.IMREAD_GRAYSCALE)
        _, threshold = cv2.threshold(intelPictureWithCorrectedContoursProcessing_grayscale, 110, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, w, h = bbox = cv2.boundingRect(cnt)
            x = bbox[0]
            y = bbox[1]
            cv2.circle(intelPictureAfterFirstCrop_colored, (x + 30, y + 30), 20, (0, 0, 255), -1)
        cv2.imwrite('processingimages/intelPictureWithCorrectedContoursProcessed.png', intelPictureAfterFirstCrop_colored)

        intelPictureAfterFirstCropDoubleProceed = cv2.imread('processingimages/intelPictureWithCorrectedContoursProcessed.png',
                                                             cv2.IMREAD_COLOR)
        fontpath = "cambria.ttc"
        b, g, r, a = 0, 0, 0, 0
        font2 = ImageFont.truetype(fontpath, 60)
        ImagePIL = Image.fromarray(intelPictureAfterFirstCropDoubleProceed)
        draw = ImageDraw.Draw(ImagePIL)
        for cnt in contours:
            x, y, w, h = bbox = cv2.boundingRect(cnt)
            x = bbox[0]
            y = bbox[1]
            if 1000 < bbox[2] < 2000:
                draw.text((x + 100, y), "Сдвоенная пара", font=font2, fill=(b, g, r, a))
            elif 2000 < bbox[2] < 4000:
                draw.text((x + 100, y), "Счетверенная пара", font=font2, fill=(b, g, r, a))
            elif 4000 < bbox[2] < 7000:
                draw.text((x + 100, y), "Свосьмеренная пара", font=font2, fill=(b, g, r, a))
        OutputPILImage = np.array(ImagePIL)
        cv2.imwrite("processingimages/intelPictureWithCorrectedContoursProcessedWithDouble.png", OutputPILImage)

        CropNumCounter = 0
        print("Было найдено " + str(len(contours)) + " контуров")
        for cnt in contours:
            x, y, w, h = bbox = cv2.boundingRect(cnt)
            crop_img = intelPictureAfterFirstCrop_grayscale[y: y + h,
                       x: x + w].copy()  # (x1, y1) будет верхний левый угол и (x2, y2) внизу справа.[y1:y2, x1:x2]
            cv2.imwrite("processingimages/imgs/cropped" + str(CropNumCounter) + ".png", crop_img)
            CropNumCounter = CropNumCounter + 1

        somevar = list(pyautogui.locateAll("processingimages/markers/testFind4.png",
                                           "processingimages/intelPictureWithCorrectedContoursProcessedWithDouble.png"))  # confidence = 0.972
        somelist = []
        i = 0
        for element in somevar:
            sth = somevar[i]
            i += 1
            sth = str(sth)
            sth = sth.replace("Box(", "")
            sth = sth.replace(")", "")
            sth = sth.replace(" ", "")
            sth = sth.split(",")

            x1 = int(str(sth[0]).replace("left=", ""))
            y1 = int(str(sth[1]).replace("top=", ""))
            x2 = int(str(sth[2]).replace("width=", ""))
            y2 = int(str(sth[3]).replace("height=", ""))

            newListObj = str(x1) + "," + str(y1)
            somelist.append(newListObj)

        intelPictureAfterFirstCropDoubleProceedWindow = cv2.imread(
            'processingimages/intelPictureWithCorrectedContoursProcessedWithDouble.png', cv2.IMREAD_COLOR)
        ImagePIL = Image.fromarray(intelPictureAfterFirstCropDoubleProceedWindow)
        draw = ImageDraw.Draw(ImagePIL)
        for j in range(0, len(somelist)):
            somelist_coord = str(somelist[j])
            somelist_coord = somelist_coord.split(",")
            x = int(somelist_coord[0])
            y = int(somelist_coord[1])
            draw.text((x + 100, y), "Окно", font=font2, fill=(b, g, r, a))
        OutputPILImage = np.array(ImagePIL)
        cv2.imwrite("processingimages/intelPictureWithCorrectedContoursProcessedWithDouble.png", OutputPILImage)

        intelPictureAfterFirstCropMarked_colored = cv2.imread(
            'processingimages/intelPictureWithCorrectedContoursProcessedWithDouble.png', cv2.IMREAD_COLOR)
        intelPictureAfterFirstCropMarked_grayscale = cv2.imread(
            'processingimages/intelPictureWithCorrectedContoursProcessedWithDouble.png', cv2.IMREAD_GRAYSCALE)
        _, threshold = cv2.threshold(intelPictureAfterFirstCropMarked_grayscale, 110, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        CropNumCounterMarked = 0
        contoursLenght = len(contours)
        print("Было найдено " + str(len(contours)) + " контуров")
        for cnt in contours:
            x, y, w, h = bbox = cv2.boundingRect(cnt)
            crop_img = intelPictureAfterFirstCropMarked_grayscale[y: y + h,
                       x: x + w].copy()  # (x1, y1) будет верхний левый угол и (x2, y2) внизу справа.[y1:y2, x1:x2]
            cv2.imwrite("processingimages/imagesWithMarkers/cropped" + str(CropNumCounterMarked) + ".png", crop_img)
            CropNumCounterMarked = CropNumCounterMarked + 1

        cv2.destroyAllWindows()

        LessonsStringList = []
        for contoursLenght in range(0, contoursLenght):
            imgNameProcessor = "processingimages/imagesWithMarkers/cropped" + str(contoursLenght) + ".png"
            img = cv2.imread(imgNameProcessor)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            data = pytesseract.image_to_string(img, lang="rus+eng", config=config)
            dataClear = data
            dataClear = dataClear.replace("®", " ")
            dataClear = dataClear.replace("©", " ")
            dataClear = dataClear.replace("\n", " ")
            dataClear = dataClear.replace("", " ")
            dataClear = dataClear.replace("@", " ")
            dataClear = dataClear.replace("°", " ")
            dataClear = dataClear.replace("  ", "")  # \\/
            dataClear = dataClear.replace("\\/", "W")  # Листанционно
            dataClear = dataClear.replace("Листанционно", "Дистанционно")  # ПМ.О2
            dataClear = dataClear.replace("ПМ.О2", "ПМ.02")#ю
            dataClear = dataClear.replace("ю ", "")
            dataClear = dataClear.replace("Слвоенная","Сдвоенная")
            dataClear = dataClear.replace("IIM.02", "ПМ.02")
            dataClear = dataClear.replace("У\\У","W")
            print("Была найдена строка " + dataClear)
            print(contoursLenght)
            if len(dataClear) == 2:
                dataClear = dataClear.replace(" ", "")
            if dataClear == " ":
                dataClear = "Пустое поле"
            LessonsStringList.append(dataClear)
            contoursLenght = contoursLenght - 1
        print(LessonsStringList)
        LessonsStringList.reverse()
        print(LessonsStringList)

        LessonsAnchorList = []
        for i, string in enumerate(LessonsStringList):
            if len(string) == 1:
                print(string + " " + str(i))
                LessonsAnchorList.append(i)
        print(LessonsAnchorList)
        print(LessonsStringList[LessonsAnchorList[0] + 1] + "\n" + LessonsStringList[LessonsAnchorList[1] + 1] + "\n" +
              LessonsStringList[LessonsAnchorList[2] + 1] + "\n" + LessonsStringList[LessonsAnchorList[3] + 1] + "\n" +
              LessonsStringList[LessonsAnchorList[4] + 1])

        FirstAnchorLineList = []
        SecondAnchorLineList = []
        ThirdAnchorLineList = []
        FourthAnchorLineList = []
        FifthAnchorLineList = []
        LineComponent = ["First", "Second", "Third", "Fourth", "Fifth"]
        LineCounter = 0
        FirstAnchorCounter, SecondAnchorCounter, ThirdAnchorCounter, FourthAnchorCounter, FifthAnchorCounter = 0, 0, 0, 0, 0
        FirstAnchorIndex, SecondAnchorIndex, ThirdAnchorIndex, FourthAnchorIndex, FifthAnchorIndex = LessonsAnchorList[0], LessonsAnchorList[1], LessonsAnchorList[2], LessonsAnchorList[3], LessonsAnchorList[4]
        LineDict = {"FirstAnchorLineList": FirstAnchorLineList, "SecondAnchorLineList": SecondAnchorLineList,
                    "ThirdAnchorLineList": ThirdAnchorLineList, "FourthAnchorLineList": FourthAnchorLineList,
                    "FifthAnchorLineList": FifthAnchorLineList}
        LineCountersDict = {"FirstAnchorCounter": FirstAnchorCounter, "SecondAnchorCounter": SecondAnchorCounter,
                            "ThirdAnchorCounter": ThirdAnchorCounter, "FourthAnchorCounter": FourthAnchorCounter,
                            "FifthAnchorCounter": FifthAnchorCounter}
        LineIndexiesDict = {"FirstAnchorIndex": FirstAnchorIndex, "SecondAnchorIndex": SecondAnchorIndex,
                            "ThirdAnchorIndex": ThirdAnchorIndex, "FourthAnchorIndex": FourthAnchorIndex,
                            "FifthAnchorIndex": FifthAnchorIndex}

        for LineCounter in range(len(LessonsAnchorList)):
            LineVar = LineComponent[LineCounter] + "AnchorLineList"
            LineVarInside_processor = LineComponent[LineCounter] + "AnchorCounter"
            LineIndexies_processor = LineComponent[LineCounter] + "AnchorIndex"
            try:
                LineIndexies2_processor = LineComponent[LineCounter + 1] + "AnchorIndex"
                SecondRange = LineIndexiesDict[LineIndexies2_processor]
            except(IndexError):
                SecondRange = contoursLenght
                print("kekw")
            FirstRange = LineIndexiesDict[LineIndexies_processor] + 1
            LineCountersDict[LineVarInside_processor] = 0
            print(FirstRange)
            print(SecondRange)
            for LineCountersDict[LineVarInside_processor] in range(FirstRange, SecondRange):
                LineDict[LineVar].append(
                    LessonsStringList[LessonsAnchorList[0] + LineCountersDict[LineVarInside_processor]])
                LineCountersDict[LineVarInside_processor] += 1
            LineCounter += 1

        for k in range(0, len(FirstAnchorLineList)):
            if len(FirstAnchorLineList) < 12:
                FirstAnchorLineList.append("Пустое поле")
        for k in range(0, len(SecondAnchorLineList)):
            if len(SecondAnchorLineList) < 12:
                SecondAnchorLineList.append("Пустое поле")
        for k in range(0, len(ThirdAnchorLineList)):
            if len(ThirdAnchorLineList) < 12:
                ThirdAnchorLineList.append("Пустое поле")
        for k in range(0, len(FourthAnchorLineList)):
            if len(FourthAnchorLineList) < 12:
                FourthAnchorLineList.append("Пустое поле")
        for k in range(0, len(FifthAnchorLineList)):
            if len(FifthAnchorLineList) < 12:
                FifthAnchorLineList.append("Пустое поле")


        Lessons_801a1, Lessons_801a2, Lessons_801b1, Lessons_801b2, Lessons_803a1, Lessons_803a2, Lessons_803b1, Lessons_803b2, Lessons_803v1, Lessons_803v2, Lessons_803g1, Lessons_803g2 = [], [], [], [], [], [], [], [], [], [], [], []
        Lessons_Dict = {
            "Lessons_801a1": Lessons_801a1,
            "Lessons_801a2": Lessons_801a2,
            "Lessons_801b1": Lessons_801b1,
            "Lessons_801b2": Lessons_801b2,
            "Lessons_803a1": Lessons_803a1,
            "Lessons_803a2": Lessons_803a2,
            "Lessons_803b1": Lessons_803b1,
            "Lessons_803b2": Lessons_803b2,
            "Lessons_803v1": Lessons_803v1,
            "Lessons_803v2": Lessons_803v2,
            "Lessons_803g1": Lessons_803g1,
            "Lessons_803g2": Lessons_803g2
        }
        group_801a1, group_801a2, group_801b1, group_801b2, group_803a1, group_803a2, group_803b1, group_803b2, group_803v1, group_803v2, group_803g1, group_803g2 = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
        Groups_Dict = {
            "group_801a1": group_801a1,
            "group_801a2": group_801a2,
            "group_801b1": group_801b1,
            "group_801b2": group_801b2,
            "group_803a1": group_803a1,
            "group_803a2": group_803a2,
            "group_803b1": group_803b1,
            "group_803b2": group_803b2,
            "group_803v1": group_803v1,
            "group_803v2": group_803v2,
            "group_803g1": group_803g1,
            "group_803g2": group_803g2
        }
        GroupComponent = ["_801a1", "_801a2", "_801b1", "_801b2", "_803a1", "_803a2", "_803b1", "_803b2", "_803v1",
                          "_803v2", "_803g1", "_803g2"]
        # multiplex = group_801a1

        FirstAnchorLineListCopyDouble = FirstAnchorLineList
        FirstListCopyIndexiesDouble = []
        FirstListCopyText = []
        for CycleCounter, StringFromLine in enumerate(FirstAnchorLineList):
            if StringFromLine.find("Сдвоенная пара") != -1:
                FirstListCopyIndexiesDouble.append(CycleCounter)
                FirstListCopyText.append(StringFromLine)

        DoubleLessonsCounter = 0
        LenList = len(FirstListCopyIndexiesDouble)
        DoubleLessonsConter2 = 1
        for DoubleLessonsCounter in range(0, LenList):
            FirstAnchorLineListCopyDouble.insert(
                FirstListCopyIndexiesDouble[DoubleLessonsCounter] + DoubleLessonsConter2,
                FirstListCopyText[DoubleLessonsCounter])
            DoubleLessonsCounter += 1
            DoubleLessonsConter2 += 1

        FirstAnchorLineListCopyQuadruple = FirstAnchorLineListCopyDouble
        FirstListCopyIndexesQuadruple = []
        FirstListCopyText = []
        for CycleCounter, StringFromLine in enumerate(FirstAnchorLineList):
            if StringFromLine.find("Счетверенная пара") != -1:
                FirstListCopyIndexesQuadruple.append(CycleCounter)
                FirstListCopyText.append(StringFromLine)

        QuadrupleLessonsCounter = 0
        QuadrupleLessonsConter2 = 1
        for QuadrupleLessonsCounter in range(0, len(FirstListCopyIndexesQuadruple)):
            if QuadrupleLessonsCounter == 0:
                FirstAnchorLineListCopyQuadruple.insert(
                    FirstListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2,
                    FirstListCopyText[QuadrupleLessonsCounter])
                FirstAnchorLineListCopyQuadruple.insert(
                    FirstListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 1,
                    FirstListCopyText[QuadrupleLessonsCounter])
                FirstAnchorLineListCopyQuadruple.insert(
                    FirstListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 2,
                    FirstListCopyText[QuadrupleLessonsCounter])
            if QuadrupleLessonsCounter == 1:
                FirstAnchorLineListCopyQuadruple.insert(
                    FirstListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 2,
                    FirstListCopyText[QuadrupleLessonsCounter])
                FirstAnchorLineListCopyQuadruple.insert(
                    FirstListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 3,
                    FirstListCopyText[QuadrupleLessonsCounter])
                FirstAnchorLineListCopyQuadruple.insert(
                    FirstListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 4,
                    FirstListCopyText[QuadrupleLessonsCounter])
            if QuadrupleLessonsCounter == 2:
                FirstAnchorLineListCopyQuadruple.insert(
                    FirstListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 4,
                    FirstListCopyText[QuadrupleLessonsCounter])
                FirstAnchorLineListCopyQuadruple.insert(
                    FirstListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 5,
                    FirstListCopyText[QuadrupleLessonsCounter])
                FirstAnchorLineListCopyQuadruple.insert(
                    FirstListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 6,
                    FirstListCopyText[QuadrupleLessonsCounter])

            QuadrupleLessonsCounter += 1
            QuadrupleLessonsConter2 += 1

        FirstAnchorLineListCopyOctuple = FirstAnchorLineListCopyQuadruple
        FirstListCopyIndexesOctuple = []
        FirstListCopyTextOctuple = []
        for CycleCounter, StringFromLine in enumerate(FirstAnchorLineList):
            if StringFromLine.find("Свосьмеренная пара") != -1:
                FirstListCopyIndexesOctuple.append(CycleCounter)
                FirstListCopyTextOctuple.append(StringFromLine)

        OctupleLessonsCounter = 0
        OctupleLessonsConter2 = 1

        for OctupleLessonsCounter in range(0, len(FirstListCopyIndexesOctuple)):
            FirstAnchorLineListCopyOctuple.insert(
                FirstListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2,
                FirstListCopyTextOctuple[OctupleLessonsCounter])
            FirstAnchorLineListCopyOctuple.insert(
                FirstListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 1,
                FirstListCopyTextOctuple[OctupleLessonsCounter])
            FirstAnchorLineListCopyOctuple.insert(
                FirstListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 2,
                FirstListCopyTextOctuple[OctupleLessonsCounter])
            FirstAnchorLineListCopyOctuple.insert(
                FirstListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 3,
                FirstListCopyTextOctuple[OctupleLessonsCounter])
            FirstAnchorLineListCopyOctuple.insert(
                FirstListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 4,
                FirstListCopyTextOctuple[OctupleLessonsCounter])
            FirstAnchorLineListCopyOctuple.insert(
                FirstListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 5,
                FirstListCopyTextOctuple[OctupleLessonsCounter])
            FirstAnchorLineListCopyOctuple.insert(
                FirstListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 6,
                FirstListCopyTextOctuple[OctupleLessonsCounter])

            OctupleLessonsCounter += 1
            OctupleLessonsConter2 += 1

        SecondAnchorLineListCopyDouble = SecondAnchorLineList
        SecondListCopyIndexiesDouble = []
        SecondListCopyText = []
        for CycleCounter, StringFromLine in enumerate(SecondAnchorLineList):
            if StringFromLine.find("Сдвоенная пара") != -1:
                SecondListCopyIndexiesDouble.append(CycleCounter)
                SecondListCopyText.append(StringFromLine)

        DoubleLessonsCounter = 0
        LenList = len(SecondListCopyIndexiesDouble)
        DoubleLessonsConter2 = 1
        for DoubleLessonsCounter in range(0, LenList):
            SecondAnchorLineListCopyDouble.insert(
                SecondListCopyIndexiesDouble[DoubleLessonsCounter] + DoubleLessonsConter2,
                SecondListCopyText[DoubleLessonsCounter])
            DoubleLessonsCounter += 1
            DoubleLessonsConter2 += 1

        SecondAnchorLineListCopyQuadruple = SecondAnchorLineListCopyDouble
        SecondListCopyIndexesQuadruple = []
        SecondListCopyText = []
        for CycleCounter, StringFromLine in enumerate(SecondAnchorLineList):
            if StringFromLine.find("Счетверенная пара") != -1:
                SecondListCopyIndexesQuadruple.append(CycleCounter)
                SecondListCopyText.append(StringFromLine)

        QuadrupleLessonsCounter = 0
        QuadrupleLessonsConter2 = 1
        for QuadrupleLessonsCounter in range(0, len(SecondListCopyIndexesQuadruple)):
            if QuadrupleLessonsCounter == 0:
                SecondAnchorLineListCopyQuadruple.insert(
                    SecondListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2,
                    SecondListCopyText[QuadrupleLessonsCounter])
                SecondAnchorLineListCopyQuadruple.insert(
                    SecondListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 1,
                    SecondListCopyText[QuadrupleLessonsCounter])
                SecondAnchorLineListCopyQuadruple.insert(
                    SecondListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 2,
                    SecondListCopyText[QuadrupleLessonsCounter])
            if QuadrupleLessonsCounter == 1:
                SecondAnchorLineListCopyQuadruple.insert(
                    SecondListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 2,
                    SecondListCopyText[QuadrupleLessonsCounter])
                SecondAnchorLineListCopyQuadruple.insert(
                    SecondListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 3,
                    SecondListCopyText[QuadrupleLessonsCounter])
                SecondAnchorLineListCopyQuadruple.insert(
                    SecondListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 4,
                    SecondListCopyText[QuadrupleLessonsCounter])
            if QuadrupleLessonsCounter == 2:
                SecondAnchorLineListCopyQuadruple.insert(
                    SecondListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 4,
                    SecondListCopyText[QuadrupleLessonsCounter])
                SecondAnchorLineListCopyQuadruple.insert(
                    SecondListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 5,
                    SecondListCopyText[QuadrupleLessonsCounter])
                SecondAnchorLineListCopyQuadruple.insert(
                    SecondListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 6,
                    SecondListCopyText[QuadrupleLessonsCounter])

            QuadrupleLessonsCounter += 1
            QuadrupleLessonsConter2 += 1

        SecondAnchorLineListCopyOctuple = SecondAnchorLineListCopyQuadruple
        SecondListCopyIndexesOctuple = []
        SecondListCopyTextOctuple = []
        for CycleCounter, StringFromLine in enumerate(SecondAnchorLineList):
            if StringFromLine.find("Свосьмеренная пара") != -1:
                SecondListCopyIndexesOctuple.append(CycleCounter)
                SecondListCopyTextOctuple.append(StringFromLine)

        OctupleLessonsCounter = 0
        OctupleLessonsConter2 = 1

        for OctupleLessonsCounter in range(0, len(SecondListCopyIndexesOctuple)):
            SecondAnchorLineListCopyOctuple.insert(
                SecondListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2,
                SecondListCopyTextOctuple[OctupleLessonsCounter])
            SecondAnchorLineListCopyOctuple.insert(
                SecondListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 1,
                SecondListCopyTextOctuple[OctupleLessonsCounter])
            SecondAnchorLineListCopyOctuple.insert(
                SecondListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 2,
                SecondListCopyTextOctuple[OctupleLessonsCounter])
            SecondAnchorLineListCopyOctuple.insert(
                SecondListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 3,
                SecondListCopyTextOctuple[OctupleLessonsCounter])
            SecondAnchorLineListCopyOctuple.insert(
                SecondListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 4,
                SecondListCopyTextOctuple[OctupleLessonsCounter])
            SecondAnchorLineListCopyOctuple.insert(
                SecondListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 5,
                SecondListCopyTextOctuple[OctupleLessonsCounter])
            SecondAnchorLineListCopyOctuple.insert(
                SecondListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 6,
                SecondListCopyTextOctuple[OctupleLessonsCounter])

            OctupleLessonsCounter += 1
            OctupleLessonsConter2 += 1

        ThirdAnchorLineListCopyDouble = ThirdAnchorLineList
        ThirdListCopyIndexiesDouble = []
        ThirdListCopyText = []
        for CycleCounter, StringFromLine in enumerate(ThirdAnchorLineList):
            if StringFromLine.find("Сдвоенная пара") != -1:
                ThirdListCopyIndexiesDouble.append(CycleCounter)
                ThirdListCopyText.append(StringFromLine)

        DoubleLessonsCounter = 0
        LenList = len(ThirdListCopyIndexiesDouble)
        DoubleLessonsConter2 = 1
        for DoubleLessonsCounter in range(0, LenList):
            ThirdAnchorLineListCopyDouble.insert(
                ThirdListCopyIndexiesDouble[DoubleLessonsCounter] + DoubleLessonsConter2,
                ThirdListCopyText[DoubleLessonsCounter])
            DoubleLessonsCounter += 1
            DoubleLessonsConter2 += 1

        ThirdAnchorLineListCopyQuadruple = ThirdAnchorLineListCopyDouble
        ThirdListCopyIndexesQuadruple = []
        ThirdListCopyText = []
        for CycleCounter, StringFromLine in enumerate(ThirdAnchorLineList):
            if StringFromLine.find("Счетверенная пара") != -1:
                ThirdListCopyIndexesQuadruple.append(CycleCounter)
                ThirdListCopyText.append(StringFromLine)

        QuadrupleLessonsCounter = 0
        QuadrupleLessonsConter2 = 1
        for QuadrupleLessonsCounter in range(0, len(ThirdListCopyIndexesQuadruple)):
            if QuadrupleLessonsCounter == 0:
                ThirdAnchorLineListCopyQuadruple.insert(
                    ThirdListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2,
                    ThirdListCopyText[QuadrupleLessonsCounter])
                ThirdAnchorLineListCopyQuadruple.insert(
                    ThirdListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 1,
                    ThirdListCopyText[QuadrupleLessonsCounter])
                ThirdAnchorLineListCopyQuadruple.insert(
                    ThirdListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 2,
                    ThirdListCopyText[QuadrupleLessonsCounter])
            if QuadrupleLessonsCounter == 1:
                ThirdAnchorLineListCopyQuadruple.insert(
                    ThirdListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 2,
                    ThirdListCopyText[QuadrupleLessonsCounter])
                ThirdAnchorLineListCopyQuadruple.insert(
                    ThirdListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 3,
                    ThirdListCopyText[QuadrupleLessonsCounter])
                ThirdAnchorLineListCopyQuadruple.insert(
                    ThirdListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 4,
                    ThirdListCopyText[QuadrupleLessonsCounter])
            if QuadrupleLessonsCounter == 2:
                ThirdAnchorLineListCopyQuadruple.insert(
                    ThirdListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 4,
                    ThirdListCopyText[QuadrupleLessonsCounter])
                ThirdAnchorLineListCopyQuadruple.insert(
                    ThirdListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 5,
                    ThirdListCopyText[QuadrupleLessonsCounter])
                ThirdAnchorLineListCopyQuadruple.insert(
                    ThirdListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 6,
                    ThirdListCopyText[QuadrupleLessonsCounter])

            QuadrupleLessonsCounter += 1
            QuadrupleLessonsConter2 += 1

        ThirdAnchorLineListCopyOctuple = ThirdAnchorLineListCopyQuadruple
        ThirdListCopyIndexesOctuple = []
        ThirdListCopyTextOctuple = []
        for CycleCounter, StringFromLine in enumerate(ThirdAnchorLineList):
            if StringFromLine.find("Свосьмеренная пара") != -1:
                ThirdListCopyIndexesOctuple.append(CycleCounter)
                ThirdListCopyTextOctuple.append(StringFromLine)

        OctupleLessonsCounter = 0
        OctupleLessonsConter2 = 1

        for OctupleLessonsCounter in range(0, len(ThirdListCopyIndexesOctuple)):
            ThirdAnchorLineListCopyOctuple.insert(
                ThirdListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2,
                ThirdListCopyTextOctuple[OctupleLessonsCounter])
            ThirdAnchorLineListCopyOctuple.insert(
                ThirdListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 1,
                ThirdListCopyTextOctuple[OctupleLessonsCounter])
            ThirdAnchorLineListCopyOctuple.insert(
                ThirdListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 2,
                ThirdListCopyTextOctuple[OctupleLessonsCounter])
            ThirdAnchorLineListCopyOctuple.insert(
                ThirdListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 3,
                ThirdListCopyTextOctuple[OctupleLessonsCounter])
            ThirdAnchorLineListCopyOctuple.insert(
                ThirdListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 4,
                ThirdListCopyTextOctuple[OctupleLessonsCounter])
            ThirdAnchorLineListCopyOctuple.insert(
                ThirdListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 5,
                ThirdListCopyTextOctuple[OctupleLessonsCounter])
            ThirdAnchorLineListCopyOctuple.insert(
                ThirdListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 6,
                ThirdListCopyTextOctuple[OctupleLessonsCounter])

            OctupleLessonsCounter += 1
            OctupleLessonsConter2 += 1

        FourthAnchorLineListCopyDouble = FourthAnchorLineList
        FourthListCopyIndexiesDouble = []
        FourthListCopyText = []
        for CycleCounter, StringFromLine in enumerate(FourthAnchorLineList):
            if StringFromLine.find("Сдвоенная пара") != -1:
                FourthListCopyIndexiesDouble.append(CycleCounter)
                FourthListCopyText.append(StringFromLine)

        DoubleLessonsCounter = 0
        LenList = len(FourthListCopyIndexiesDouble)
        DoubleLessonsConter2 = 1
        for DoubleLessonsCounter in range(0, LenList):
            FourthAnchorLineListCopyDouble.insert(
                FourthListCopyIndexiesDouble[DoubleLessonsCounter] + DoubleLessonsConter2,
                FourthListCopyText[DoubleLessonsCounter])
            DoubleLessonsCounter += 1
            DoubleLessonsConter2 += 1

        FourthAnchorLineListCopyQuadruple = FourthAnchorLineListCopyDouble
        FourthListCopyIndexesQuadruple = []
        FourthListCopyText = []
        for CycleCounter, StringFromLine in enumerate(FourthAnchorLineList):
            if StringFromLine.find("Счетверенная пара") != -1:
                FourthListCopyIndexesQuadruple.append(CycleCounter)
                FourthListCopyText.append(StringFromLine)

        QuadrupleLessonsCounter = 0
        QuadrupleLessonsConter2 = 1
        for QuadrupleLessonsCounter in range(0, len(FourthListCopyIndexesQuadruple)):
            if QuadrupleLessonsCounter == 0:
                FourthAnchorLineListCopyQuadruple.insert(
                    FourthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2,
                    FourthListCopyText[QuadrupleLessonsCounter])
                FourthAnchorLineListCopyQuadruple.insert(
                    FourthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 1,
                    FourthListCopyText[QuadrupleLessonsCounter])
                FourthAnchorLineListCopyQuadruple.insert(
                    FourthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 2,
                    FourthListCopyText[QuadrupleLessonsCounter])
            if QuadrupleLessonsCounter == 1:
                FourthAnchorLineListCopyQuadruple.insert(
                    FourthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 2,
                    FourthListCopyText[QuadrupleLessonsCounter])
                FourthAnchorLineListCopyQuadruple.insert(
                    FourthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 3,
                    FourthListCopyText[QuadrupleLessonsCounter])
                FourthAnchorLineListCopyQuadruple.insert(
                    FourthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 4,
                    FourthListCopyText[QuadrupleLessonsCounter])
            if QuadrupleLessonsCounter == 2:
                FourthAnchorLineListCopyQuadruple.insert(
                    FourthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 4,
                    FourthListCopyText[QuadrupleLessonsCounter])
                FourthAnchorLineListCopyQuadruple.insert(
                    FourthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 5,
                    FourthListCopyText[QuadrupleLessonsCounter])
                FourthAnchorLineListCopyQuadruple.insert(
                    FourthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 6,
                    FourthListCopyText[QuadrupleLessonsCounter])

            QuadrupleLessonsCounter += 1
            QuadrupleLessonsConter2 += 1

        FourthAnchorLineListCopyOctuple = FourthAnchorLineListCopyQuadruple
        FourthListCopyIndexesOctuple = []
        FourthListCopyTextOctuple = []
        for CycleCounter, StringFromLine in enumerate(FourthAnchorLineList):
            if StringFromLine.find("Свосьмеренная пара") != -1:
                FourthListCopyIndexesOctuple.append(CycleCounter)
                FourthListCopyTextOctuple.append(StringFromLine)

        OctupleLessonsCounter = 0
        OctupleLessonsConter2 = 1

        for OctupleLessonsCounter in range(0, len(FourthListCopyIndexesOctuple)):
            FourthAnchorLineListCopyOctuple.insert(
                FourthListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2,
                FourthListCopyTextOctuple[OctupleLessonsCounter])
            FourthAnchorLineListCopyOctuple.insert(
                FourthListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 1,
                FourthListCopyTextOctuple[OctupleLessonsCounter])
            FourthAnchorLineListCopyOctuple.insert(
                FourthListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 2,
                FourthListCopyTextOctuple[OctupleLessonsCounter])
            FourthAnchorLineListCopyOctuple.insert(
                FourthListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 3,
                FourthListCopyTextOctuple[OctupleLessonsCounter])
            FourthAnchorLineListCopyOctuple.insert(
                FourthListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 4,
                FourthListCopyTextOctuple[OctupleLessonsCounter])
            FourthAnchorLineListCopyOctuple.insert(
                FourthListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 5,
                FourthListCopyTextOctuple[OctupleLessonsCounter])
            FourthAnchorLineListCopyOctuple.insert(
                FourthListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 6,
                FourthListCopyTextOctuple[OctupleLessonsCounter])

            OctupleLessonsCounter += 1
            OctupleLessonsConter2 += 1

        FifthAnchorLineListCopyDouble = FifthAnchorLineList
        FifthListCopyIndexiesDouble = []
        FifthListCopyText = []
        for CycleCounter, StringFromLine in enumerate(FifthAnchorLineList):
            if StringFromLine.find("Сдвоенная пара") != -1:
                FifthListCopyIndexiesDouble.append(CycleCounter)
                FifthListCopyText.append(StringFromLine)

        DoubleLessonsCounter = 0
        LenList = len(FifthListCopyIndexiesDouble)
        DoubleLessonsConter2 = 1
        for DoubleLessonsCounter in range(0, LenList):
            FifthAnchorLineListCopyDouble.insert(
                FifthListCopyIndexiesDouble[DoubleLessonsCounter] + DoubleLessonsConter2,
                FifthListCopyText[DoubleLessonsCounter])
            DoubleLessonsCounter += 1
            DoubleLessonsConter2 += 1

        FifthAnchorLineListCopyQuadruple = FifthAnchorLineListCopyDouble
        FifthListCopyIndexesQuadruple = []
        FifthListCopyText = []
        for CycleCounter, StringFromLine in enumerate(FifthAnchorLineList):
            if StringFromLine.find("Счетверенная пара") != -1:
                FifthListCopyIndexesQuadruple.append(CycleCounter)
                FifthListCopyText.append(StringFromLine)

        QuadrupleLessonsCounter = 0
        QuadrupleLessonsConter2 = 1
        for QuadrupleLessonsCounter in range(0, len(FifthListCopyIndexesQuadruple)):
            if QuadrupleLessonsCounter == 0:
                FifthAnchorLineListCopyQuadruple.insert(
                    FifthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2,
                    FifthListCopyText[QuadrupleLessonsCounter])
                FifthAnchorLineListCopyQuadruple.insert(
                    FifthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 1,
                    FifthListCopyText[QuadrupleLessonsCounter])
                FifthAnchorLineListCopyQuadruple.insert(
                    FifthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 2,
                    FifthListCopyText[QuadrupleLessonsCounter])
            if QuadrupleLessonsCounter == 1:
                FifthAnchorLineListCopyQuadruple.insert(
                    FifthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 2,
                    FifthListCopyText[QuadrupleLessonsCounter])
                FifthAnchorLineListCopyQuadruple.insert(
                    FifthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 3,
                    FifthListCopyText[QuadrupleLessonsCounter])
                FifthAnchorLineListCopyQuadruple.insert(
                    FifthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 4,
                    FifthListCopyText[QuadrupleLessonsCounter])
            if QuadrupleLessonsCounter == 2:
                FifthAnchorLineListCopyQuadruple.insert(
                    FifthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 4,
                    FifthListCopyText[QuadrupleLessonsCounter])
                FifthAnchorLineListCopyQuadruple.insert(
                    FifthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 5,
                    FifthListCopyText[QuadrupleLessonsCounter])
                FifthAnchorLineListCopyQuadruple.insert(
                    FifthListCopyIndexesQuadruple[QuadrupleLessonsCounter] + QuadrupleLessonsConter2 + 6,
                    FifthListCopyText[QuadrupleLessonsCounter])

            QuadrupleLessonsCounter += 1
            QuadrupleLessonsConter2 += 1

        FifthAnchorLineListCopyOctuple = FifthAnchorLineListCopyQuadruple
        FifthListCopyIndexesOctuple = []
        FifthListCopyTextOctuple = []
        for CycleCounter, StringFromLine in enumerate(FifthAnchorLineList):
            if StringFromLine.find("Свосьмеренная пара") != -1:
                FifthListCopyIndexesOctuple.append(CycleCounter)
                FifthListCopyTextOctuple.append(StringFromLine)

        OctupleLessonsCounter = 0
        OctupleLessonsConter2 = 1

        for OctupleLessonsCounter in range(0, len(FifthListCopyIndexesOctuple)):
            FifthAnchorLineListCopyOctuple.insert(
                FifthListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2,
                FifthListCopyTextOctuple[OctupleLessonsCounter])
            FifthAnchorLineListCopyOctuple.insert(
                FifthListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 1,
                FifthListCopyTextOctuple[OctupleLessonsCounter])
            FifthAnchorLineListCopyOctuple.insert(
                FifthListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 2,
                FifthListCopyTextOctuple[OctupleLessonsCounter])
            FifthAnchorLineListCopyOctuple.insert(
                FifthListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 3,
                FifthListCopyTextOctuple[OctupleLessonsCounter])
            FifthAnchorLineListCopyOctuple.insert(
                FifthListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 4,
                FifthListCopyTextOctuple[OctupleLessonsCounter])
            FifthAnchorLineListCopyOctuple.insert(
                FifthListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 5,
                FifthListCopyTextOctuple[OctupleLessonsCounter])
            FifthAnchorLineListCopyOctuple.insert(
                FifthListCopyIndexesOctuple[OctupleLessonsCounter] + OctupleLessonsConter2 + 6,
                FifthListCopyTextOctuple[OctupleLessonsCounter])

            OctupleLessonsCounter += 1
            OctupleLessonsConter2 += 1

        print(FirstAnchorLineListCopyOctuple)
        print(len(FirstAnchorLineListCopyOctuple))

        print(SecondAnchorLineListCopyOctuple)
        print(len(SecondAnchorLineListCopyOctuple))

        print(ThirdAnchorLineListCopyOctuple)
        print(len(ThirdAnchorLineListCopyOctuple))

        print(FourthAnchorLineListCopyOctuple)
        print(len(FourthAnchorLineListCopyOctuple))

        print(FifthAnchorLineListCopyOctuple)
        print(len(FifthAnchorLineListCopyOctuple))

        for element in FirstAnchorLineListCopyOctuple:
            if element == "Свосьмеренная пара" or element == "Счетверенная пара" or element == "Сдвоенная пара":
                elementIndex = FirstAnchorLineListCopyOctuple.index(element)
                FirstAnchorLineListCopyOctuple.pop(elementIndex)
                FirstAnchorLineListCopyOctuple.insert(elementIndex, "Окно")
        for element in SecondAnchorLineListCopyOctuple:
            if element == "Свосьмеренная пара" or element == "Счетверенная пара" or element == "Сдвоенная пара":
                elementIndex = SecondAnchorLineListCopyOctuple.index(element)
                SecondAnchorLineListCopyOctuple.pop(elementIndex)
                SecondAnchorLineListCopyOctuple.insert(elementIndex, "Окно")
        for element in ThirdAnchorLineListCopyOctuple:
            if element == "Свосьмеренная пара" or element == "Счетверенная пара" or element == "Сдвоенная пара":
                elementIndex = ThirdAnchorLineListCopyOctuple.index(element)
                ThirdAnchorLineListCopyOctuple.pop(elementIndex)
                ThirdAnchorLineListCopyOctuple.insert(elementIndex, "Окно")
        for element in FourthAnchorLineListCopyOctuple:
            if element == "Свосьмеренная пара" or element == "Счетверенная пара" or element == "Сдвоенная пара":
                elementIndex = FourthAnchorLineListCopyOctuple.index(element)
                FourthAnchorLineListCopyOctuple.pop(elementIndex)
                FourthAnchorLineListCopyOctuple.insert(elementIndex, "Окно")
        for element in FifthAnchorLineListCopyOctuple:
            if element == "Свосьмеренная пара" or element == "Счетверенная пара" or element == "Сдвоенная пара":
                elementIndex = FifthAnchorLineListCopyOctuple.index(element)
                FifthAnchorLineListCopyOctuple.pop(elementIndex)
                FifthAnchorLineListCopyOctuple.insert(elementIndex, "Окно")

        incounter = 0
        for incounter in range(0, len(GroupComponent)):
            Lessons_Generator = "Lessons" + GroupComponent[incounter]
            Group_Generator = "group" + GroupComponent[incounter]
            Lessons_Dict[Lessons_Generator].append(FirstAnchorLineListCopyOctuple[Groups_Dict[Group_Generator]])
            Lessons_Dict[Lessons_Generator].append(SecondAnchorLineListCopyOctuple[Groups_Dict[Group_Generator]])
            Lessons_Dict[Lessons_Generator].append(ThirdAnchorLineListCopyOctuple[Groups_Dict[Group_Generator]])
            Lessons_Dict[Lessons_Generator].append(FourthAnchorLineListCopyOctuple[Groups_Dict[Group_Generator]])
            Lessons_Dict[Lessons_Generator].append(FifthAnchorLineListCopyOctuple[Groups_Dict[Group_Generator]])
            incounter += 1

        #Удаляем все файлы
        for filename in os.listdir(path='firstcropimg/ProcessingImages'):
            os.remove('firstcropimg/ProcessingImages/' + filename)

        for filename in os.listdir(path='processingimages'):
            if filename.find(".png") != -1:
                os.remove('processingimages/' + filename)

        for filename in os.listdir(path='processingimages/imgs'):
            os.remove('processingimages/imgs/' + filename)

        for filename in os.listdir(path='processingimages/imagesWithMarkers'):
            os.remove('processingimages/imagesWithMarkers/' + filename)

        incounter = 0
        for incounter in range(0, len(GroupComponent)):
            Lessons_Generator = "Lessons" + GroupComponent[incounter]
            for element in Lessons_Dict[Lessons_Generator]:
                    insertrionElement = element
                    insertrionElement = insertrionElement.replace("Свосьмеренная пара ", "")
                    insertrionElement = insertrionElement.replace("Счетверенная пара ", "")
                    elementIndex = Lessons_Dict[Lessons_Generator].index(element)
                    Lessons_Dict[Lessons_Generator].pop(elementIndex)
                    Lessons_Dict[Lessons_Generator].insert(elementIndex, insertrionElement)
            incounter += 1
        print("801a1 " + str(Lessons_801a1))
        print("801a2 " + str(Lessons_801a2))
        print("801б1 " + str(Lessons_801b1))
        print("801б2 " + str(Lessons_801b2))
        print("803a1 " + str(Lessons_803a1))
        print("803a2 " + str(Lessons_803a2))
        print("803б1 " + str(Lessons_803b1))
        print("803б2 " + str(Lessons_803b2))
        print("803в1 " + str(Lessons_803v1))
        print("803в2 " + str(Lessons_803v2))
        print("803г1 " + str(Lessons_803g1))
        print("803г2 " + str(Lessons_803g2))

    else:
        print("Возникла проблемка")
else:
    print("В таблице не был найден сегодняшний или завтрашний день")
