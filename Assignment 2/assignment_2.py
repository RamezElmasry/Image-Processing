import numpy as np
import cv2
from matplotlib import pyplot as plt

def erode(img, s):
    kernel = np.ones((s,s), np.int64)
    p,q = kernel.shape
    img0 = img.copy()
    r,c = img0.shape
    for i in range(r):
        for j in range(c):
            window = img0[i:i+p,j:j+q]
            m_w,n_w = window.shape
            if m_w != p or n_w != q:
                break
            img0[i,j] = np.amin(window)

    #print(img0)
    #cv2.imshow('Image', img0)
    #v2.waitKey(0)
    return img0

def dilate(img, s):
    kernel = np.ones((s,s), np.int64)
    p,q = kernel.shape
    img0 = img.copy()
    r,c = img0.shape
    for i in range(r):
        for j in range(c):
            window = img0[i:i+p,j:j+q]
            m_w,n_w = window.shape
            if m_w != p or n_w != q:
                break
            img0[i,j] = np.amax(window)

    #print(img0)
    #cv2.imshow('Image', img0)
    #cv2.waitKey(0)
    return img0

def increase_contrast(img, a, b, s):
    r,g,bu = cv2.split(img)
    bu = bu.astype(np.int64)
    g = g.astype(np.int64)
    r = r.astype(np.int64)
    #print(r.dtype)
    # Opening
    r1 = erode(r,s)
    open_r = dilate(r1,s)
    #print(open_r.dtype)
    g1 = erode(g,s)
    open_g = dilate(g1,s)
    b1 = erode(bu,s)
    open_b = dilate(b1,s)
    # Closing
    r2 = dilate(r,s)
    close_r = erode(r2,s)
    g2 = dilate(g,s)
    close_g = erode(g2,s)
    b2 = dilate(bu,s)
    close_b = erode(b2,s)

    # output = original + a * (original - result_opening) - b * (result_closing - original)
    out_r = r + (a * (r - open_r)) - (b * (close_r - r))
    out_g = g + (a * (g - open_g)) - (b * (close_g - g))
    out_b = bu + (a * (bu - open_b)) - (b * (close_b - bu))

    
    out = cv2.merge([out_r,out_g,out_b])
    out = out.astype(np.int64)
    #print(out.shape)
    #cv2.imwrite('3x3_a=1,b=5.jpg', out)
    return out
   
img = cv2.imread('Suez Canal.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = img.astype(np.int64)


out1 = increase_contrast(img, 1, 1, 3)
out2 = increase_contrast(img, 1, 5, 3)
out3 = increase_contrast(img, 5, 1, 3)
out4 = increase_contrast(img, 1, 1, 9)


plt.subplot(2,2,1)
plt.imshow(out1)
plt.title('3x3 a=1,b=1')

plt.subplot(2,2,2)
plt.imshow(out2)
plt.title('3x3 a=1,b=5')

plt.subplot(2,2,3)
plt.imshow(out3)
plt.title('3x3 a=5,b=1')

plt.subplot(2,2,4)
plt.imshow(out4)
plt.title('9x9 a=1,b=1')
plt.show()