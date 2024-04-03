import cv2
import numpy as np
import math
np.set_printoptions(threshold=np.inf)

img = cv2.imread('Camera2.jpg')

def LZW_Coding_Compression(img):

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    r,c = img.shape
    img_string = np.zeros((r*c))
    idx = 0

    #Creating a string of all intensity values
    for i in range(0,r): 
        for j in range(0,c):
            img_string[idx] = img[i,j]
            idx = idx+1
            
    #print(len(img_string))

    crs = ""  # current recognized sequence
    current_input = ""  # current_input sequence

    output = {}
    out_idx = 0

    dict_val = {}
    dict_idx = 0

    # Add first 0-255 key/value pairs key is string/ value is integer
    for i in range(0,256):
        dict_val[str(i)] = i

    #print(dict_val)
    #next unused location
    dict_idx = 256

    current_input = img_string[0]

    crs = str(int(current_input))

    for i in range(1,idx):
        current_input = img_string[i]
        
        w = crs + "-" + str(int(current_input))
        
        #print("Current W is " + w)
        
        if w in dict_val:
            #print(w + " Already exists")
            crs = w
        else:
            # if not found in the dictionary
            #print("Creating a new entry for the dictionary ") 
            # append/update/access => dict[key]=value
            output[out_idx] = dict_val[crs]
            #print("Output " , + output[int(out_idx)])
            out_idx = out_idx + 1
            # update the current recognized seq. to be only the current input pixel
            crs = str(int(current_input))
            # add the new code to the dictionary
            dict_val[w] = dict_idx
            dict_idx = dict_idx + 1
        
    #Last entry will always be found in the dictionary
    if crs in dict_val: 
        output[out_idx] = dict_val[crs]
        #print("Output " , + output[int(out_idx)])
        out_idx = out_idx + 1
        
    #printing the encoded output
    #print(len(output))
    #Printing dictionary
    #print(len(dict_val))
    compression_ratio = (8 * len(img_string)) / (math.ceil(math.log(max(output.values()),2)) * len(output))
    #print(compression_ratio) 
    return dict_val, output, compression_ratio

output_dict, output_code, compression_ratio = LZW_Coding_Compression(img)

# Open file in write mode and save dictionary
file = open("Dict.txt", "w")
longest_code = 0
for code in output_dict.keys():
    if len(code) > longest_code:
        longest_code = len(code)

for key,value in output_dict.items():
    # create string in every row with constant length with 
    # left adjusting the key with the longest code length
    file.write(f'{key.ljust(longest_code)}\t{value}\n')
file.close()

# Open file in write mode and save output code
file = open("LZWCode.txt", "w")
for value in output_code.values():
    file.write(str(value) + " ")
file.close()

# Open file in write mode and save output code
file = open("CompRatio.txt", "w")
file.write(str(compression_ratio))
file.close()