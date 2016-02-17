#import the necessary modules
import freenect
import cv2
import numpy as np
threshold = 100
current_depth = 650
adj = 8

params = cv2.SimpleBlobDetector_Params()
 
# Change thresholds
params.minThreshold = 10;
params.maxThreshold = 255;
# Filter by Area.
params.filterByArea = True
params.minArea = 150
 
# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
	detector = cv2.SimpleBlobDetector(params)
else : 
	detector = cv2.SimpleBlobDetector_create(params)

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

def check_opencv_version(major, lib=None):
    # if the supplied library is None, import OpenCV
    if lib is None:
        import cv2 as lib
        
    # return whether or not the current OpenCV version matches the
    # major version number
    return lib.__version__.startswith(major)
    
if __name__ == "__main__":
    while 1:
        #get a frame from RGB camera
        # Setup SimpleBlobDetector parameters.
		img = np.zeros((1080, 1920))	
		frame = get_video()
		frame=cv2.flip(frame,1)
		
		cv2.namedWindow("RGB image", cv2.WND_PROP_FULLSCREEN)
		cv2.setWindowProperty("RGB image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
		
		cv2.rectangle(frame,(200,250),(300,350),(0,255,0),1)
        #cv2.imshow('RGB image',frame)
        
        #get a frame from depth sensor
		depth = get_depth()
		depth=cv2.flip(depth,1)
		depth = 255 * np.logical_and(depth >= current_depth - threshold, depth <= current_depth + threshold)    
		depth = depth.astype(np.uint8)   
		#adject depth data
		blurred = cv2.GaussianBlur(depth, (5, 5), 0)
		thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
		
		#find contours form thresh
		(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
		#cnts = cnts[1]
		for c in cnts:
			#find hand and draw rect around hand
			epsilon = 0.1*cv2.arcLength(c,True)
			approx = cv2.approxPolyDP(c,epsilon,True)
			print approx
			x,y,w,h = cv2.boundingRect(c)
			cv2.rectangle(img,(x-adj,y-adj),(x+w-adj,y+h-adj),(255,255,0),3)
			# compute the center of the contour
			M = cv2.moments(c)
			if M["m00"] > 0:
				cX = int(M["m10"] / M["m00"])-8
				cY = int(M["m01"] / M["m00"])-8
				cv2.circle(frame, (cX, cY), 50, (255, 255, 255), 1)
				
		
		cv2.imshow('RGB image',frame)
        # quit program when 'esc' key is pressed
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			#cv2.imwrite("test_write.jpg", frame)
			cv2.destroyAllWindows()
			break
