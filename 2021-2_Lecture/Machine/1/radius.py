import cv2
import numpy as np
import math
from PIL import Image
###=============== 구현하고 싶은 것 ===========================#
# pixel 두개를 찍고 우클릭으로 , 좌클릭으로 높이 지정, 중간 버튼 축적 입력
pts = []
check = []
def onChange(pos):
    pass
class Length:
    def __init__(self, IMG_DIR):
        self.IMG_DIR = IMG_DIR

# :mouse callback function
    def Pix_mm(self, event, x, y, flags, param):
        IMG_DIR = self.IMG_DIR
        img = cv2.imread(IMG_DIR, 0)
        img2 = img.copy()
        if event == cv2.EVENT_LBUTTONDOWN:  # Left click, select point
            pts.append((x, y))
            print(pts)
        if event == cv2.EVENT_RBUTTONDOWN:  # Right click to cancel the last selected point
            check.append((x,y))
            print(check)
            self.check_y = check[0][1]


        if event == cv2.EVENT_MBUTTONDOWN:  # center click
            points = np.array(pts)
            print(points)
            len = pts[0][0] - pts[1][0]
            print("길이", pts[0][0] - pts[1][0], pts[0][0] , pts[1][0])
            length_mm = int(input("수치 정보입력 : "))
            self.mm_pixel = abs(length_mm / len)
            self.pixel_mm = abs(len / length_mm)
            print(self.mm_pixel, self.pixel_mm)
        cv2.imshow('img',img)

    def get_height(self, event, x, y, flags, param):
        IMG_DIR = self.IMG_DIR

        img = cv2.imread(IMG_DIR, 0)
        img2 = img.copy()

        if event == cv2.EVENT_RBUTTONDOWN:  # Right click to cancel the last selected point
            check.append((x,y))
            print(check)
            self.check_y = check[0][1]
        cv2.imshow('img',img)



    def distance(self):
        min_x = self.mm_pixel
        min_y = self.pixel_mm
        return min_x, min_y

    def height(self):
        check_y = self.check_y
        return check_y

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

            cv2.imshow("Trackbar Windows", binary)

        cv2.imwrite("thresh.jpg", binary)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return thresh, maxval




class Radius:
    def __init__(self, IMG, th):
        img = Image.open(IMG).convert('L')
        img_array = np.array(img)

        th, dst = cv2.threshold(img_array, th, 255, cv2.THRESH_BINARY)

        self.dst = dst
        ############
## 위에 포인트 찾기
    def first(self):
        dst = self.dst
        size = np.shape(dst)

        row = size[0]
        col = size[1]
        print(size, row, col)

        first_point = 0

        for i in range(100, row):
            print("i", i)
            check_row = dst[i, :]
            for j in range(150, len(check_row)):
                value_temp = check_row[j]
                if value_temp != 0:
                    first_point = [i, j]
                    break
            if value_temp != 0:
                break

        print(first_point)

        #########inner_high############
        high_col = dst[:, first_point[1]]

        high_col_reverse = np.flipud(high_col)
        first_point2 = 0
        for i in range(20, len(high_col_reverse)):
            value_temp = high_col_reverse[i]
            if value_temp != 0:
                print(size[0] - i, i)
                first_point2 = [size[0] - i, first_point[1]]
                break
        return first_point, first_point2

    def second(self, collum):
        dst = self.dst
        size = np.shape(dst)
        first_row = dst[collum, :]

        point1 = []
        point2 = []
        left_point = 0

        for i in range(1, len(first_row)):
            value_temp = first_row[i]
            if first_row[i - 1] < first_row[i]:
                left_point = i
                point1.append(left_point)
            elif first_row[i - 1] > first_row[i]:
                left_point = i
                point2.append(left_point)
        print("point",point1,point2)
        out_1 = (collum, point1[0])
        out_2 = (collum, point2[-1])
        in_1 = (collum, point2[0])
        in_2 = (collum, point1[-1])
        return out_1, out_2, in_1, in_2

    def outter(self, collum):
        dst = self.dst
        size = np.shape(dst)
        first_row = dst[collum, :]

        point1 = []
        point2 = []
        left_point = 0

        for i in range(1, len(first_row)):
            value_temp = first_row[i]
            if first_row[i - 1] < first_row[i]:
                left_point = i
                point1.append(left_point)
            elif first_row[i - 1] > first_row[i]:
                left_point = i
                point2.append(left_point)
        print("point", point1, point2)
        out_1 = (collum, point1[0])
        out_2 = (collum, point2[-1])
        return out_1, out_2

    def inner(self, collum):
        dst = self.dst
        size = np.shape(dst)
        first_row = dst[collum, :]

        point1 = []
        point2 = []
        left_point = 0

        for i in range(1, len(first_row)):
            value_temp = first_row[i]
            if first_row[i - 1] < first_row[i]:
                left_point = i
                point1.append(left_point)
            elif first_row[i - 1] > first_row[i]:
                left_point = i
                point2.append(left_point)
        print("point", point1, point2)
        in_1 = (collum, point2[0])
        in_2 = (collum, point1[-1])
        return in_1, in_2
        # Visualize the result

        ############
        # %%
        #######high#####################





class cal:
    def radius(A,B,C):
        x1 = A[0]
        x2 = B[0]
        x3 = C[0]
        y1 = A[1]
        y2 = B[1]
        y3 = C[1]

        a = x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2
        b = (x1 ** 2 + y1 ** 2) * (y3 - y2) + (x2 ** 2 + y2 ** 2) * (y1 - y3) + (x3 ** 2 + y3 ** 2) * (y2 - y1)
        c = (x1 ** 2 + y1 ** 2) * (x2 - x3) + (x2 ** 2 + y2 ** 2) * (x3 - x1) + (x3 ** 2 + y3 ** 2) * (x1 - x2)
        d = (x1 ** 2 + y1 ** 2) * (x3 * y2 - x2 * y3) + (x2 ** 2 + y2 ** 2) * (x1 * y3 - x3 * y1) + (x3 ** 2 + y3 ** 2) * (x2 * y1 - x1 * y2)
        Xc = (-1) * b / (2 * a)
        Yc = (-1) * c / (2 * a)
        R = math.sqrt((b ** 2 + c ** 2 - (4 * a * d)) / (4 * a ** 2))
        return Xc, Yc, R





if __name__ == "__main__":
    # ## mm / pixel calculate
    IMG = "View_1.jpg"
    length = Length(IMG)
    cv2.namedWindow('img')
    cv2.setMouseCallback('img', length.Pix_mm)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    m_p, p_m = length.distance() # m_p is mm / pixel p_m is pixel/mm
    print(m_p, p_m)

    # get threshold
    thr1, max = Callback.threshold(IMG)
    print(thr1)
    THR = "thresh.jpg"
    #outter point

    Rad = Radius(IMG,thr1)


    # high 1, 2
    high_out, high_in = Rad.first()
    length = Length(THR)
    cv2.namedWindow('img')
    cv2.setMouseCallback('img', length.get_height)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    high = length.height()

    out1, out2= Rad.outter(high)

    check = []
    # high 1, 2

    length = Length(THR)
    cv2.namedWindow('img')
    cv2.setMouseCallback('img', length.get_height)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    high2 = length.height()

    in1, in2= Rad.inner(high2)

    # radius
    A = high_out
    B = out1
    C = out2
    a = high_in
    b = in1
    c = in2
    print(A,B,C,a,b,c)
    Xc, Yc, R = cal.radius(A, B, C)
    xc, yc, r = cal.radius(a,b,c)
    print("pixel",Xc, Yc, xc, yc, R, r)
    R_m = R * m_p
    r_m = r * m_p
    print("radius(mm):",R_m, r_m)

    img = cv2.imread(IMG,cv2.IMREAD_COLOR)
    cv2.circle(img, (int(A[1]),int(A[0])), 5, (0,255,0),3)
    cv2.circle(img, (int(B[1]), int(B[0])), 5, (0, 255, 0), 3)
    cv2.circle(img, (int(C[1]), int(C[0])), 5, (0, 255, 0), 3)
    cv2.circle(img, (int(a[1]), int(a[0])), 5, (255, 0, 0), 3)
    cv2.circle(img, (int(b[1]), int(b[0])), 5, (255, 0, 0), 3)
    cv2.circle(img, (int(c[1]), int(c[0])), 5, (255, 0, 0), 3)
    cv2.circle(img, (int(Yc), int(Xc)), int(R), (0, 255, 0), 3)
    cv2.circle(img, (int(yc),int(xc)), int(r), (255, 0, 0), 3)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
