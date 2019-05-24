# import the necessary packages
import subprocess
import sys
import cv2
import numpy as np

global points

points = []
def click_image(event, x, y, flags, param):  
    if event == cv2.EVENT_LBUTTONDOWN:
        print ("Here. x =", x, "& y =", y)
        points.append([x,y])
        
def get_region(vid_path):
    vidcap = cv2.VideoCapture(vid_path)
    success,image = vidcap.read()

    out = open("roi.txt", 'w')

    print("Please select points that borders the bus way on the image.")
    
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_image)
    cv2.imshow("image", image)
    
    while True:
    	# display the image and wait for a keypress
        key = cv2.waitKey(1) & 0xFF
        
        if chr(key) == 'q':
            break
    
    print(points)
    
    npArray = np.array(points, np.int32)
    npArray = npArray.reshape((-1, 1, 2))
    cv2.polylines(image,[npArray],True,(0,255,255), 5)
    
    cv2.destroyWindow("image")
    cv2.imshow("image", image)
    print("The detector will run on the selected region.")
    
    cv2.waitKey(5000)
    cv2.destroyWindow("image")
    cv2.waitKey(1)
    
    for node in points:
        out.write(str (node[0]) + ' ' + str (node[1]) +'\n')

    return points

def main():
    get_region(sys.argv[0])
    subprocess.call("./darknet detector demo cfg/coco.data cfg/yolov3.cfgyolov3.weights {} -out_filename out.avi -dont_show -gpus 0,1,2 -thresh {}".format(sys.argv[0], sys.argv[1]), shell=True)
    

if __name__ == "__main__":
    main()