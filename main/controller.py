from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
from UI import Ui_Form
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


class Form_controller(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        # TODO
        # qpushbutton doc: https://doc.qt.io/qt-5/qpushbutton.html
        self.ui.pushButton.clicked.connect(self.open_file)
        self.ui.pushButton_2.clicked.connect(self.open_file_2)
        self.ui.Button_separation.clicked.connect(self.color_sperate)
        self.ui.Button_transformation.clicked.connect(
            self.color_transformation)
        self.ui.Button_Detection.clicked.connect(self.color_detection)
        self.ui.Button_Blend.clicked.connect(self.blending)
        self.ui.Button_Gaussian.clicked.connect(self.gaussian_blur)
        self.ui.Button_Bilateral.clicked.connect(self.bilateral_blur)
        self.ui.Button_Median.clicked.connect(self.median_blur)

    def open_file(self):
        filename, filetype = QFileDialog.getOpenFileName(
            self, "Open file", "./")                 # start path
        # print(filename, filetype)
        result = os.path.split(filename)[1]
        self.img = cv2.imread(filename, -1)

        if self.img.size == 1:
            return

        self.refreshShow()

        self.ui.label.setText(result)

    def open_file_2(self):
        filename2, filetype = QFileDialog.getOpenFileName(
            self, "Open file", "./")                 # start path
        # print(filename, filetype)
        result2 = os.path.split(filename2)[1]
        self.img_2 = cv2.imread(filename2, -1)

        if self.img_2.size == 1:
            return

        self.refreshShow2()

        self.ui.label_2.setText(result2)

    def refreshShow(self):
        # 提取影象的尺寸和通道, 用於將opencv下的image轉換成Qimage
        height, width, channel = self.img.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()

        # 將Qimage顯示出來
        # self.label.setPixmap(QPixmap.fromImage(self.qImg))
    def refreshShow2(self):
        # 提取影象的尺寸和通道, 用於將opencv下的image轉換成Qimage
        height, width, channel = self.img_2.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.img_2.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()

        # 將Qimage顯示出來
        # self.label.setPixmap(QPixmap.fromImage(self.qImg))

    def color_sperate(self):
        if self.img.size == 1:
            return
        # display an image
        cv2.imshow('Original image', self.img)
        b, g, r = cv2.split(self.img)
        zeros = np.zeros(self.img.shape[:2], dtype="uint8")
        cv2.imshow("Red", cv2.merge([zeros, zeros, r]))
        cv2.imshow("Green", cv2.merge([zeros, g, zeros]))
        cv2.imshow("Blue", cv2.merge([b, zeros, zeros]))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        self.refreshShow()

    def color_transformation(self):
        # display an image
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        grayimg2 = np.zeros(self.img.shape, np.uint8)
        for i in range(grayimg2.shape[0]):
            for j in range(grayimg2.shape[1]):
                grayimg2[i, j] = 1 / 3 * self.img[i, j, 0] + 1 / \
                    3 * self.img[i, j, 1] + 1 / 3 * self.img[i, j, 2]
        cv2.imshow("average weighted", grayimg2)
        cv2.imshow("Original image", self.img)
        cv2.imshow("Gray image", gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        self.refreshShow()

    def color_detection(self):
        # img = cv2.imread(
        #     "/Users/kongheng/Desktop/HW_1 computer vision/111.png")
        img_hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        # red color
        low_red = np.array([0, 50, 50])
        high_red = np.array([15, 255, 255])
        red_mask = cv2.inRange(img_hsv, low_red, high_red)
        red = cv2.bitwise_and(self.img, self.img, mask=red_mask)
        # Blue color
        low_blue = np.array([94, 80, 2])
        high_blue = np.array([126, 255, 255])
        blue_mask = cv2.inRange(img_hsv, low_blue, high_blue)
        blue = cv2.bitwise_and(self.img, self.img, mask=blue_mask)
        # Green color
        low_green = np.array([40, 50, 20])
        high_green = np.array([80, 255, 255])
        green_mask = cv2.inRange(img_hsv, low_green, high_green)
        green = cv2.bitwise_and(self.img, self.img, mask=green_mask)
        # while color
        low_white = np.array([0, 0, 200])
        high_white = np.array([180, 20, 255])
        white_mask = cv2.inRange(img_hsv, low_white, high_white)
        white = cv2.bitwise_and(self.img, self.img, mask=white_mask)

        cv2.imshow("Original image", self.img)
        cv2.imshow("Red", red)
        cv2.imshow("Blue", blue)
        cv2.imshow("Green", green)
        cv2.imshow("White", white)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        self.refreshShow()

    def blending(self):
        # img1 = cv2.imread('/Users/kongheng/Desktop/HW_1 computer vision/cat.jpeg')
        # img2 = cv2.imread('/Users/kongheng/Desktop/HW_1 computer vision/dog.jpeg')

        img1 = cv2.resize(self.img, (400, 400))
        img2 = cv2.resize(self.img_2, (400, 400))
        img = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
        cv2.imshow("Blend", img)

        def blend(val):
            print(val)
            alpha = val/100
            beta = (1.0 - alpha)
            result = cv2.addWeighted(img1, alpha, img2, beta, 0.0)
            cv2.imshow('Result', result)

        cv2.createTrackbar("Blend", "Blend", 0, 255, blend)
        cv2.setTrackbarPos('Blend', 'Blend', 0)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        self.refreshShow()
        self.refreshShow2()

    def gaussian_blur(self):
        # img = cv2.imread("/Users/kongheng/Desktop/HW_1 computer vision/gg.jpg")
        img1 = cv2.resize(self.img, (400, 400))
        cv2.imshow("Gassian Blur", img1)

        def blur(val):
            if val > 0:
                kx = 2*val+1
                ky = 2*val+1
                gass_blur = cv2.GaussianBlur(self.img, (kx, ky), 0)
                cv2.imshow("Result", gass_blur)
            else:
                return self.img

        cv2.createTrackbar("Magnitude", "Gassian Blur", 0, 10, blur)
        cv2.setTrackbarPos("Magnitude", "Gassian Blur", 0)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        self.refreshShow()

    def bilateral_blur(self):
        # img = cv2.imread("/Users/kongheng/Desktop/HW_1 computer vision/gg.jpg")
        img1 = cv2.resize(self.img, (400, 400))
        cv2.imshow("Bilateral Filter", img1)

        def blur(val):
            if val > 0:
                kx = 90
                ky = 90
                bil_blur = cv2.bilateralFilter(self.img, 11, kx, ky)
                cv2.imshow("Result", bil_blur)
            else:
                return self.img

        cv2.createTrackbar("Magnitude", "Bilateral Filter", 0, 30, blur)
        cv2.setTrackbarPos("Magnitude", "Bilateral Filter", 0)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        self.refreshShow()

    def median_blur(self):
        # img = cv2.imread("/Users/kongheng/Desktop/HW_1 computer vision/gg.jpg")
        img1 = cv2.resize(self.img, (400, 400))
        cv2.imshow("Median Filter", img1)

        def blur(val):
            if val > 0:
                k = 2*val+1
                med_blur = cv2.medianBlur(self.img, k)
                cv2.imshow("Result", med_blur)
            else:
                return self.img

        cv2.createTrackbar("Magnitude", "Median Filter", 0, 10, blur)
        cv2.setTrackbarPos("Magnitude", "Median Filter", 0)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        self.refreshShow()
