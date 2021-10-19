
# import lib
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import cv2
import math

filename='cc3.png'
file = 'D:\\VISION_LECTURE\\term2\\IMG\\'+filename
img = Image.open(file).convert('L')
#img_np = np.array(img)
img_array = np.array(img)

img_size = img_array.shape
print(img_size)
plt.imshow(img)
#%%
    
def define_circle(p1, p2, p3):
    """
    Returns the center and radius of the circle passing the given 3 points.
    In case the 3 points form a line, returns (None, infinity).
    """
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])

    if abs(det) < 1.0e-6:
        return (None, np.inf)

    # Center of circle
    cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det

    radius = np.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
    return ((cx, cy), radius)

# Plot point
def plotPoint(p):
    plt.scatter(p[1],p[0], color = 'r')
    

#%%
if filename=='sound.png':
    threshold=60
else:
    threshold=70
row = 1000;
col = 1200;
#%%
#plt.imshow(img_array, cmap = 'gray')

rows, cols = np.shape(img_array)
sobelx = cv2.Sobel(img_array,cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(img_array,cv2.CV_64F,0,1,ksize=5)
profile1 = abs(sobelx[row,:])
profile2 = abs(sobely[:,col])


line1 = profile1/max(profile1[0:int(cols/2)])
line2 = profile1/max(profile1[int(cols/2):cols-1])
line3 = profile2/max(profile2[0:int(rows/2)])


# find point 1
index = 0
for i in range(int(cols/2),0,-1):
    temp = line1[i]
    if temp > 0.99:
        index = i
        break
p1 = [row,index]

#find point 2
for i in range(int(cols/2),cols-1,1):
    temp = line2[i]
    if temp > 0.99:
        index = i
        break
p2 = [row,index]

# find point 3
for i in range(int(rows/2),0,-1):
    temp = line3[i]
    if temp > 0.99:
        index = i
        break
p3 = [index,col]

#find outer circle
for i in range(p1[1]-120,int(cols/2),+1):
    temp = line1[i]
    if temp > 0.15:
        index = i
        break
p4 = [row,index]

#find point 5
for i in range(p2[1]+120,int(cols/2),-1):
    temp = line2[i]
    if temp > 0.15:
        index = i
        break
p5 = [row,index]

# find point 6
for i in range(p3[0]-120,int(rows/2),1):
    temp = line3[i]
    if temp > 0.15:
        index = i
        break
p6 = [index,col]

center, r = define_circle(p1, p2, p3)
center2,r2 = define_circle(p4, p5, p6)


###

loop = 1000
cir_profile = np.zeros(loop)
x = np.zeros(loop)
y = np.zeros(loop)
delta = np.zeros(loop)

for i in range(loop):
    phi = i*2*math.pi/loop
    x[i] = center[1] + (r+r2)*math.cos(phi)/2
    y[i] = center[0] + (r+r2)*math.sin(phi)/2
    cir_profile[i] = img_array[int(y[i]),int(x[i])]





for i in range(loop-1):
    delta[i] = cir_profile[i+1]-cir_profile[i]
    
delta[loop-1] = cir_profile[1]-cir_profile[loop-1]

a = []
Fail = 0
x_fail = np.zeros(loop)
y_fail = np.zeros(loop)
phi_fail = np.zeros(loop)
for i in range(len(cir_profile)):
#    temp = cir_profile[i]
    if cir_profile[i] < threshold:   #이진화
        phi = 2*i*math.pi/loop
        y_fail[Fail] = int(center[1] + (r+r2)*math.cos(phi)/2)
        x_fail[Fail] = int(center[0] + (r+r2)*math.sin(phi)/2)
        phi_fail[Fail] = i*360/1000
        Fail = Fail+1
        a.append(i)

fig, ax = plt.subplots(figsize=(10, 10));
ax.imshow(img, cmap = 'gray')
circle1 = plt.Circle([center[1],center[0]], r,linewidth=2, color='r',fill=False)
ax.add_patch(circle1)

circle2 = plt.Circle([center2[1],center2[0]], r2,linewidth=2, color='b',fill=False)
ax.add_patch(circle2)

count = 0
if Fail > 0:
    plt.text(50,50,"crack object",fontsize = 30,color = 'white',backgroundcolor ='black')
    print("this is crack object")
    for i in range(Fail):
        if phi_fail[i+1] - phi_fail[i] > 5 or i == Fail-1:
            start_point = (y_fail[i]-100,x_fail[i]-100)
            rectangle1 = Rectangle(start_point,200,200 , linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rectangle1)
            count = count+1
            left = y_fail[i]-100
            top = x_fail[i]-100
            right = y_fail[i]+100
            bottom = x_fail[i]+100
            crop_img = img.crop((left, top, right, bottom))
            crop_name = "D:\\VISION_LECTURE\\term2\\cro3" + str(count) + ".png"
            crop_img.save(crop_name)
          
else:
    plt.text(50,50,"sound object",fontsize = 30,color = 'white',backgroundcolor ='black')
    print("this is sound object")
    
fig2, ax2 = plt.subplots(figsize=(10, 10));
ax2.imshow(crop_img, cmap='gray')
