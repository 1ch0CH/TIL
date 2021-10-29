


# import lib
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2
import math

left_fileName1 = "C:\\Users\\a307\\Machine\\L1.jpg"
right_fileName1 = "C:\\Users\\a307\\Machine\\R1.jpg"



left_img1 = Image.open(left_fileName1).convert('L')
right_img1 = Image.open(right_fileName1).convert('L')

left_img_array1 = np.array(left_img1)
right_img_array1 = np.array(right_img1)

left_fileName2 = "C:\\Users\\a307\\Machine\\L2.jpg"
right_fileName2 = "C:\\Users\\a307\\Machine\\R2.jpg"

left_img2 = Image.open(left_fileName2).convert('L')
right_img2 = Image.open(right_fileName2).convert('L')

left_img_array2 = np.array(left_img2)
right_img_array2 = np.array(right_img2)


#%%
# crop template on the left image
y0 = 20
x0 = 20
dx = 40
dy = 40
h = w = 20
# y0 = 40
# x0 = 10
# dx = 15
# dy = 12
# h = 8
# w = 12
templates = []
template_points = []

# array (y, x)

for j in range(10):
    for i in range(10):
        crop_img = left_img_array1[(y0+dy*j):(y0+dy*j+h), (x0+dx*i):(x0+dx*i+w)]
        templates.append(crop_img)
        template_points.append((x0 + dx*i,y0 + dy*j))
        

fig, ax = plt.subplots()
plt.imshow(left_img_array1, cmap = 'gray')
for j in range(10):
    for i in range(10):
        point = (x0 + dx*i, y0 + dy*j)
        rectangle1 = Rectangle(point,w,h , linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rectangle1)

# template matching on the right image
fig, ax = plt.subplots()
right_img_cpy = right_img_array1.copy()
results = []
for i in range(len(templates)):
    
    # Read the template
    template = templates[i]
    
    # Store width and height of template in w and h
    w, h = template.shape[::-1]
    
    # All the 6 methods for comparison in a list
    #methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    
    meth = 'cv2.TM_CCOEFF_NORMED'
    img = right_img_array1
    method = eval(meth)
    
    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
        
    bottom_right = (top_left[0] + w, top_left[1] + h)
#    cv2.rectangle(right_img_cpy,top_left, bottom_right, (255,0,0), 2)
    
    
#    rectangle1 = Rectangle(top_left ,h,w , linewidth=1, edgecolor='r', facecolor='none')
    results.append((top_left[0],top_left[1]))

    #plt.subplot(121),plt.imshow(res,cmap = 'gray')
    #plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    #plt.subplot(122),plt.imshow(img,cmap = 'gray')
    #plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    #plt.suptitle(meth)
    
fig, ax = plt.subplots()
#plt.subplot(211)
#plt.imshow(left_img_array, cmap = 'gray')
#for i in range(len(template_points)):
#    point = template_points[i]
#    rectangle1 = Rectangle(point,h,w , linewidth=1, edgecolor='r', facecolor='none')
#    ax.add_patch(rectangle1)
        
#plt.subplot(212)
#plt.imshow(right_img_cpy, cmap = 'gray')
#plt.subplot(212)
plt.imshow(right_img_array, cmap = 'gray')
for i in range(len(results)):
    point = results[i]
    rectangle1 = Rectangle(point,w,h , linewidth=1, edgecolor='b', facecolor='none')
    ax.add_patch(rectangle1)
    

#%%

y0 = 20
x0 = 20
dx = 40
dy = 40
h = w = 20
templates2 = []
template_points2 = []

# array (y, x)

for j in range(10):
    for i in range(10):
        crop_img = left_img_array2[(y0+dy*j):(y0+dy*j+h), (x0+dx*i):(x0+dx*i+w)]
        templates2.append(crop_img)
        template_points2.append((x0 + dx*i,y0 + dy*j))
        

fig, ax = plt.subplots()
plt.imshow(left_img_array, cmap = 'gray')
for j in range(10):
    for i in range(10):
        point = (x0 + dx*i, y0 + dy*j)
        rectangle1 = Rectangle(point,w,h , linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rectangle1)

# template matching on the right image
fig, ax = plt.subplots()
right_img_cpy = right_img_array2.copy()
results2 = []
for i in range(len(templates2)):
    
    # Read the template
    template = templates2[i]
    
    # Store width and height of template in w and h
    w, h = template.shape[::-1]
    
    # All the 6 methods for comparison in a list
    #methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    
    meth = 'cv2.TM_CCOEFF_NORMED'
    img = right_img_array2
    method = eval(meth)
    
    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
        
    bottom_right = (top_left[0] + w, top_left[1] + h)

    results2.append((top_left[0],top_left[1]))

    
fig, ax = plt.subplots()

plt.imshow(right_img_array, cmap = 'gray')
for i in range(len(results2)):
    point = results2[i]
    rectangle1 = Rectangle(point,w,h , linewidth=1, edgecolor='b', facecolor='none')
    ax.add_patch(rectangle1)
    
    
    #%%
# second

disparites = []
Left_x = []
Left_y = []
for i in range(100):
    L_value = template_points[i]
    R_value = results[i]
    x = L_value[0]
    y = L_value[1]
    
    Left_x.append(x)
    Left_y.append(y)
    temp = L_value[0] - R_value[0]
    
    disparites.append(temp)
    
    
# left image
xs1 = Left_x
ys1 = Left_y
zs1 = disparites


disparites = []
Left_x = []
Left_y = []
for i in range(100):
    L_value = template_points2[i]
    R_value = results2[i]
    x = L_value[0]
    y = L_value[1]
    
    Left_x.append(x)
    Left_y.append(y)
    temp = L_value[0] - R_value[0]

    
    disparites.append(temp)

plt.plot(disparites)
    
# left image
xs2 = Left_x
ys2 = Left_y
zs2 = disparites

fig = plt.figure(figsize = (16,16))

ax_3 = fig.add_subplot(111, projection='3d')

ax_3d = fig.add_subplot(111, projection='3d')
ax_3d.set_zlim(-420,-360)
ax_3.scatter(xs1, ys1, zs1)
ax_3d.scatter(xs1, ys1, zs1)
ax_3d.scatter(xs2, ys2, zs2, color='r')


    
    
    
    
    
    
    
