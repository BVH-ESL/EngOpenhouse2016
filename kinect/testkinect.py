#import the necessary modules
import freenect
import cv2
import numpy as np
 
#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    return array
 
if __name__ == "__main__":
    while 1:
        #get a frame from RGB camera
        frame = get_video()
        #get a frame from depth sensor
        depth = get_depth()
        minVal = np.min(depth)
        print minVal
        
        np.where(depth == minVal, depth, 0)
        
        #display RGB image
        cv2.imshow('RGB image',frame)
	#backtorgb = cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
        cv2.imshow('Depth image', depth)
 
        # quit program when 'esc' key is pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
			cv2.imwrite("test_write.jpg", frame)
			break
    cv2.destroyAllWindows()
