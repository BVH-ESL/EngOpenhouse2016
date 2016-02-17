#import the necessary modules
import freenect
import cv2
import time
import numpy as np
threshold = 300
current_depth = 1170

#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    #array = array.astype(np.uint8)
    return array
 
'''
 def captureCam(depth):
	 depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
                                 '''
                                 
if __name__ == "__main__":
    while 1:
        #get a frame from RGB camera
        frame = get_video()
        #get a frame from depth sensor
        depth = get_depth()
        depth = 255 * np.logical_and(depth >= current_depth - threshold, depth <= current_depth + threshold)    
        depth = depth.astype(np.uint8)   
        #display RGB image
        cv2.imshow('RGB image',frame)
	#backtorgb = cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
        cv2.imshow('Depth image', depth)
        #print np.mean(depth)
        
        #if np.mean(depth) < 240 and np.mean(depth) > 235:1
		#	print "Capture"
			#cv2.imwrite("test_write.jpg", frame)
			
		#if(np.mean(depth))
        # quit program when 'esc' key is pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
			#cv2.imwrite("test_write.jpg", frame)
			break
    cv2.destroyAllWindows()
