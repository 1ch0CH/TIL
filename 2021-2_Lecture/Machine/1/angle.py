# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 14:37:27 2021

@author: user
"""

import cv2
import numpy as np
from PIL import Image
import math
import matplotlib.pyplot as plt


def onChange(pos):
    pass

class Callback:
    def threshold(IMG_DIR):
        src = cv2.imread(IMG_DIR, cv2.IMREAD_GRAYSCALE)

        cv2.namedWindow("Trackbar Windows")

        cv2.createTrackbar("threshold", "Trackbar Windows", 0, 255, onChange)
        cv2.createTrackbar("maxValue", "Trackbar Windows", 0, 255, lambda x : x)

        cv2.setTrackbarPos("threshold", "Trackbar Windows", 127)
        cv2.setTrackbarPos("maxValue", "Trackbar Windows", 255)

        while cv2.waitKey(1) != ord('q'):
            thresh = cv2.getTrackbarPos("threshold", "Trackbar Windows")
            maxval = cv2.getTrackbarPos("maxValue", "Trackbar Windows")
            _, binary = cv2.threshold(src, thresh, maxval, cv2.THRESH_BINARY)
            cv2.namedWindow("Trackbar Windows",cv2.WINDOW_NORMAL)
            cv2.imshow("Trackbar Windows", binary)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return thresh, maxval

class Angle:
    def __init__(self, IMG_DIR):
        self.IMG_DIR = IMG_DIR

    def get_image(self, thr1, thr2):
        img_gray = Image.open(self.IMG_DIR).convert('L')
        img_array = np.array(img_gray)
        th, dst = cv2.threshold(img_array, thr1, 255, cv2.THRESH_BINARY)

        size = np.shape(dst) #size[0]=row, size[1]=collum

        #######1.  first row #################################
        first_row = dst[253,:]
        left_point = 0
        for i in range(len(first_row)):
            value_temp = first_row[i]
            if value_temp != 0:
                left_point = i
                break

        point_1st = [253,left_point]

        first_row_reverse = np.flipud(first_row)
        right_point = 0

        for i in range(len(first_row_reverse)):
            value_temp = first_row_reverse[i]
            if value_temp != 0:
                right_point = i
                break

        point_2nd = [253, size[1] - right_point]
        print(type(point_1st))
        point_mid = (point_1st[1]+point_2nd[1])/2

    ################2. second row #########################
        second_row = dst[1833, :]
        print("d", second_row.size)
        second_left_point = 0

        for i in range(len(second_row)):
            value_temp = second_row[i]
            if value_temp != 0:
                second_left_point = i
                break

        second_point_1st = [1833, second_left_point]

        second_row_reverse = np.flipud(second_row)

        second_right_point = 0

        for i in range(len(second_row_reverse)):
            value_temp = second_row_reverse[i]
            if value_temp != 0:
                second_right_point = i
                break

        second_point_2nd = [1833, size[1] - second_right_point]

        second_point_mid = (second_point_1st[1] + second_point_2nd[1]) / 2
        
        ##
        
        first_collum = dst[:, 680]
        # col_30 = dst_col[:,30]

        left_point_col = 0

        for i in range(len(first_collum)):
            value_temp = first_collum[i]
            if value_temp != 0:
                left_point_col = i
                break

        p1 = [680, left_point_col]

        first_collum_reverse = np.flipud(first_collum)

        right_point_col = 0

        for i in range(len(first_collum_reverse)):
            value_temp = first_collum_reverse[i]
            if value_temp != 0:
                right_point_col = i
                break
        # Visualize the result
        p2 = [680, size[0] - right_point_col]
        
        
        ##################################
        th, dst_col = cv2.threshold(img_array, thr2, 255, cv2.THRESH_BINARY)

        first_collum = dst_col[200:, 253]
        # col_30 = dst_col[:,30]

        left_point_col = 0

        for i in range(len(first_collum)):
            value_temp = first_collum[i]
            if value_temp != 0:
                left_point_col = i
                break

        point_1st_col = [200+left_point_col, 253]

        first_collum_reverse = np.flipud(first_collum)

        right_point_col = 0

        for i in range(len(first_collum_reverse)):
            value_temp = first_collum_reverse[i]
            if value_temp != 0:
                right_point_col = i
                break

        point_2nd_col = [size[0] - right_point_col, 253]
        point_mid_col = (left_point_col+200 + size[0] - right_point_col) / 2

        mid = [(point_mid + second_point_mid) / 2, point_mid_col]
        self.point_mid = point_mid
        self.second_point_mid = second_point_mid
        self.point_mid_col = point_mid_col
        self.mid = mid
        self.p1 = p1
        self.p2 = p2
        fig = plt.figure(figsize=(16, 16))
        plt.imshow(dst_col, cmap='gray')
        plt.scatter(point_1st[1], point_1st[0], color='r', linewidth=10)
        plt.scatter(point_2nd[1], point_2nd[0], color='r', linewidth=10)
        plt.scatter(point_mid, point_1st[0], color='r', linewidth=10)
        plt.scatter(second_point_1st[1], second_point_1st[0], color='r', linewidth=10)
        plt.scatter(second_point_2nd[1], second_point_2nd[0], color='r', linewidth=10)
        plt.scatter(second_point_mid, second_point_1st[0], color='r', linewidth=10)
        plt.scatter(p1[0], p1[1], color='b', linewidth=10)
        plt.scatter(p2[0], p2[1], color='b', linewidth=10)

        plt.scatter(point_1st_col[1], point_1st_col[0], color='b', linewidth=10)
        plt.scatter(point_2nd_col[1], point_2nd_col[0], color='b', linewidth=10)
        self.point_mid_col = (point_2nd_col[0] - point_1st_col[0]) / 2 + point_1st_col[0]

        plt.scatter(point_1st_col[1], point_mid_col, color='b', linewidth=10)

        self.mx = (p1[0] + p2[0])/2
        self.my = (p1[1]+ p2[1])/2
        #####################################
        plt.scatter((point_mid + second_point_mid) / 2, point_mid_col, color='y', linewidth=10)
        plt.scatter(mid[0], point_mid_col, color='g', linewidth=10)
        plt.show()
    def angle(self):
        print(self.point_mid, self.second_point_mid, self.mid, self.p1, self.p2)
        x = (self.point_mid + self.second_point_mid) / 2
        y = self.point_mid_col-self.mid[1]
        A = math.sqrt(x**2 + y**2)
        x2 =self.mx-self.point_mid
        y2 = self.my
        B = math.sqrt(x2**2 + y2**2)
        C = math.sqrt(((self.point_mid + self.second_point_mid) / 2) ** 2 + (self.point_mid_col) ** 2)

        theta = 180 *math.acos((A ** 2 + B ** 2 - C ** 2) / 2 / B / A) / math.pi

        print("angle:", theta)
        return theta

if __name__ == "__main__":
    IMG = "View_2.jpg"
    thr1, max = Callback.threshold(IMG)
    thr2, max = Callback.threshold(IMG)
    Degree = Angle(IMG)
    Degree.get_image(thr1, thr2)
    theta = Degree.angle()


    print(thr1,thr2, max)
    print(theta)

    cv2.destroyAllWindows()
