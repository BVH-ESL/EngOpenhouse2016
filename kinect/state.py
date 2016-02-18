#import the necessary modules
import freenect
import cv2
import numpy as np
threshold = 100
current_depth = 650
adj = 8
state = 0
bg = np.zeros([1080, 1920, 3], np.uint8)
W = bg.shape[1]
H = bg.shape[0]
min_contours = 5000
max_contours = 10000
count = 0
cap = cv2.VideoCapture("video0")

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

if __name__ == "__main__":
    while 1:
		ret, cam = cap.read()
		#set full screen mode
		cv2.namedWindow("RGB image", cv2.WND_PROP_FULLSCREEN)
		cv2.setWindowProperty("RGB image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
		
		frame = get_video()
		frame = cv2.flip(frame,1)
		
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
		for c in cnts:
			area = cv2.contourArea(c)
			if area > min_contours and area < max_contours:
				# compute the center of the contour
				M = cv2.moments(c)
				if M["m00"] > 0:
					cX = int(M["m10"] / M["m00"])-8
					cY = int(M["m01"] / M["m00"])-8
					#cv2.circle(frame, (cX, cY), 50, (255, 255, 255), 1)
					cv2.rectangle(frame,(cX-50,cY-50),(cX+50,cY+50),(255,255,0),1)
					if count < 50:
						count+=1
					else:
						count = 0
						cv2.imwrite("test_cap.jpg", cam)
				else:
					count = 0
		
		#insert video to bg
		h, w, c = frame.shape
		bg[H/2-h/2:(H/2-h/2)+h, W/2-w/2:(W/2-w/2)+w] = frame
		cv2.imshow('RGB image',bg)
		
        # quit program when 'esc' key is pressed
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			#cv2.imwrite("test_write.jpg", frame)
			cv2.destroyAllWindows()
			break
