import cv2
import numpy as np
from edge_detection import *
import os
from tqdm import tqdm


if __name__ == '__main__':
    #specify source folder path
    path = r'c:\Users\omaro\Desktop\codes\EDGE DETECTION_FINAL\src'

    file_count = 1
    for i in tqdm(os.listdir(path)):

        folder  = r'c:\Users\omaro\Desktop\codes\EDGE DETECTION_FINAL\output'
        
        if not os.path.exists(folder):
            os.mkdir(folder)


        file_path = os.path.join(folder, 'membrane#' + str(file_count))
        
        raw = cv2.imread(os.path.join(path, i))


        if not os.path.exists(file_path):
            os.mkdir(file_path)


        raw = preprocessing(raw)
        cv2.imwrite(os.path.join(file_path, 'original.png') , raw)

        img = denoising(raw ,  lower = 22)
        cv2.imwrite(os.path.join(file_path, 'denoised.png') , img)
    
        y,x = membrane_detection(img)

        img , m , b  = crop_line(img , y , x)
        cv2.imwrite(os.path.join(file_path, 'membrane_detected.png') , img)
        
        T1 = 80 
        T2 = 50
        
        img[img!=0] = 255
    
        edge = cv2.Canny(img, T1, T2 , apertureSize=3)
        
        cv2.imwrite(os.path.join(file_path, 'edge_detected.png'),edge)

        average_dists , edge_with_avg_line = calc_dist(edge , m , b , raw)
 
        #CONCATENTE THE AVERAGE VALUE TO BE THE LAST VALUE IN THE FILE, THIS FILE CONTAINCS THE THICKNESS FOR EACH PIXEL
        np.savetxt(os.path.join(file_path, 'average_dists.txt'),np.concatenate((average_dists , np.array([average_dists.mean()]))))


        cv2.imwrite(os.path.join(file_path, 'edge_with_line_detected.png'),edge_with_avg_line)



        file_count+=1
        
        del img
        del edge


