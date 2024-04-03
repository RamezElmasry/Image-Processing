import cv2
import numpy as np

img = cv2.imread('Suez Canal.png')
#img = cv2.resize(img, (1024,576))


def distance_transform_helper(img, distance_measure, img_type):
    d_twoships = 0
    d_bigship_leftcanal = 0
    d_bigship_right_canal = 0
    d_smallship_leftcanal = 0
    d_smallship_rightcanal = 0
    shift = 0

    h,w = img.shape
    img = np.array(img, dtype = np.float32)
    for row in range(0,h):
        for col in range(0,w):
            if img[row, col] == 0:
                img[row, col] = np.inf
            elif img[row, col] == 255:
                img[row, col] = 1
 
    # first pass
    for row in range(1,h-1):
        for col in range(1,w-1):   
            kernel=(img[row-1,col-1],img[row-1,col],img[row,col-1],img[row+1,col-1],img[row,col])
            m=min(kernel)
            idx=kernel.index(m)
            if distance_measure == 'cityblock':
                if idx == 0:
                    img[row,col]=img[row-1,col-1] + 2
                elif idx == 1:
                    img[row,col]=img[row-1,col] + 1
                elif idx == 2:
                    img[row,col]=img[row,col-1] + 1
                elif idx == 3:
                    img[row,col]=img[row+1,col-1] + 2

            if distance_measure == 'chessboard':
                if idx == 0:
                    img[row,col]=img[row-1,col-1] + 1
                elif idx == 1:
                    img[row,col]=img[row-1,col] + 1
                elif idx == 2:
                    img[row,col]=img[row,col-1] + 1
                elif idx == 3:
                    img[row,col]=img[row+1,col-1] + 1
            
            if distance_measure == 'euclidean':
                if idx == 0:
                    img[row,col]=img[row-1,col-1] + np.sqrt(np.power((row - (row-1)), 2) + np.power((col - (col-1)), 2))
                elif idx == 1:
                    img[row,col]=img[row-1,col] + np.sqrt(np.power((row - (row-1)), 2) + np.power((col - col), 2))
                elif idx == 2:
                    img[row,col]=img[row,col-1] + np.sqrt(np.power((row - row), 2) + np.power((col - (col-1)), 2))
                elif idx == 3:
                    img[row,col]=img[row+1,col-1] + np.sqrt(np.power((row - (row+1)), 2) + np.power((col - (col-1)), 2))

    first_pass = img.copy()

    #second pass                 
    for row in range(h-2,0,-1):
        for col in range(w-2,0,-1):      
            kernel = (img[row+1,col+1],img[row+1,col],img[row,col+1],img[row-1,col+1],img[row,col])
            m = min(kernel)       
            idx = kernel.index(m)
            if distance_measure == 'cityblock':
                if idx == 0:
                    img[row,col]=img[row+1,col+1] + 2
                elif idx == 1:
                    img[row,col]=img[row+1,col] + 1
                elif idx == 2:
                    img[row,col]=img[row,col+1] + 1
                elif idx == 3:
                    img[row,col]=img[row-1,col+1] + 2

            if distance_measure == 'chessboard':
                if idx == 0:
                    img[row,col]=img[row+1,col+1] + 1
                elif idx == 1:
                    img[row,col]=img[row+1,col] + 1
                elif idx == 2:
                    img[row,col]=img[row,col+1] + 1
                elif idx == 3:
                    img[row,col]=img[row-1,col+1] + 1

            if distance_measure == 'euclidean':
                if idx == 0:
                    img[row,col]=img[row+1,col+1] + np.sqrt(np.power((row - (row+1)), 2) + np.power((col - (col+1)), 2))
                elif idx == 1:
                    img[row,col]=img[row+1,col] + np.sqrt(np.power((row - (row+1)), 2) + np.power((col - col), 2))
                elif idx == 2:
                    img[row,col]=img[row,col+1] + np.sqrt(np.power((row - row), 2) + np.power((col - (col+1)), 2))
                elif idx == 3:
                    img[row,col]=img[row-1,col+1] + np.sqrt(np.power((row - (row-1)), 2) + np.power((col - (col+1)), 2))

    # The distance between the smallship and bigship from the distance transform, is actually the
    # the distance between the representative point of the small ship and the nearest edge of
    # of the bigship, so we calculate this shift w.r.t distance measure and add it to the distance
    # acquired form the distance transform.
    # The shift is calculated between the representative points of the big ship and its bottom side
    if distance_measure == 'cityblock':
        shift = abs(150-200) + abs(200-200)
    if distance_measure == 'chessboard':
        shift = max(abs(150-200),abs(200-200))
    if distance_measure == 'euclidean':
        shift = np.sqrt(np.power((150-200),2) + np.power((200-200),2))

    if img_type == 'bigship':
        d_bigship_right_canal = img[150,292]
        d_bigship_leftcanal = img[150,151]
        d_twoships = img[310,175] + shift
        return first_pass, img, d_twoships, d_bigship_leftcanal, d_bigship_right_canal

    elif img_type == 'smallship':
        d_smallship_rightcanal = img[310,289]
        d_smallship_leftcanal = img[310,132]
        return first_pass, img, d_smallship_leftcanal, d_smallship_rightcanal

    else:
        return first_pass, img


def distance_transform(img, distance_measure):
    # pre-processing 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (3,3), 0)
    img = cv2.Canny(img, 100, 200)
    #img = cv2.threshold(img, 170, 255, cv2.THRESH_BINARY)[1]
    h,w = img.shape
    img0 = img.copy()

    for i in range(0,h):
        for j in range(0,w):
            if j in range(0,125) or j in range(300,w):
                img0[i,j] = 0

    first_pass, Final_output = distance_transform_helper(img0, distance_measure,'')

    #get points of interest
    leftcanal_bigship = 0
    rightcanal_bigship = 0
    leftcanal_smallship = 0
    rightcanal_smallship = 0
    leftside_bigship = 0
    rightside_bigship = 0
    leftside_smallship = 0
    rightside_smallship = 0

    big_ship = img.copy()
    small_ship = img.copy()

    for j in range(200,w):
        if j in range(205,215) and big_ship[150,j] == 255:
            rightside_bigship = (150,j)
            print("Point of the right side of the bigship", rightside_bigship)
        if j in range(220,300) and big_ship[150,j] == 255:
            rightcanal_bigship = (150,j)
            print("Point of the right side of the canal w.r.t bigship",rightcanal_bigship)

    for j in range(200,0,-1):
        if j in range(160,194) and big_ship[150,j] == 255:
            leftside_bigship = (150,j)
            print("Point of the left side of the bigship",leftside_bigship)
        if j in range(150,159) and big_ship[150,j] == 255:
            leftcanal_bigship = (150,j)
            print("Point of the left side of the canal w.r.t bigship",leftcanal_bigship)

    for j in range(175,w):
        if j in range(180,200) and small_ship[310,j] == 255:
            rightside_smallship = (310,j)
            print("Point of the right side of the smallship",rightside_smallship)
        if j in range(210,290) and small_ship[310,j] == 255:
            rightcanal_smallship = (310,j)
            print("Point of the right side of the canal w.r.t smallship",rightcanal_smallship)

    for j in range(175,0,-1):
        if j in range(150,175) and small_ship[310,j] == 255:
            leftside_smallship = (310,j)
            print("Point of the left side of the smallship",leftside_smallship)
        if j in range(130,140) and small_ship[310,j] == 255:
            leftcanal_smallship = (310,j)
            print("Point of the left side of the canal w.r.t smallship",leftcanal_smallship)

    #isolate the big ship alone
    for i in range(0,h):
        for j in range(0,w):
            if j in range(0,190) or j in range(280,w):
                big_ship[i,j] = 0

    bigship_firstpass,bigship_output,d_twoships,d_bigship_leftcanal,d_bigship_rightcanal = distance_transform_helper(big_ship, distance_measure, 'bigship')
    print(d_twoships, d_bigship_leftcanal, d_bigship_rightcanal)
    
    # Isolate the small ship alone in the image
    for i in range(0,h):
        for j in range(0,w):
            if j in range(0,172) or j in range(280,w):
                small_ship[i,j] = 0
            if i in range(0,200) and j in range(165,280):
                small_ship[i,j] = 0
    smallship_firstpass,smallship_output,d_smallship_leftcanal,d_smallship_rightcanal = distance_transform_helper(small_ship, distance_measure, 'smallship')
    print(d_smallship_leftcanal, d_smallship_rightcanal)

    # cv2.imwrite('final_smallship.bmp', smallship_output)

    return first_pass, Final_output

first_pass1, city = distance_transform(img, 'cityblock')
# cv2.imwrite('Suez_1_City.bmp', first_pass1)
# cv2.imwrite('Suez_final_City.bmp', city)

first_pass2, chess = distance_transform(img, 'chessboard')
# cv2.imwrite('Suez_1_Chess.bmp', first_pass2)
# cv2.imwrite('Suez_final_Chess.bmp', chess)

first_pass3, euc = distance_transform(img, 'euclidean')
# cv2.imwrite('Suez_1_Euclidean.bmp', first_pass3)
# cv2.imwrite('Suez_final_Euclidean.bmp', euc) 