
# A range of color values is determined for the desired object
color_lower = (110, 50, 50)  #BGR
color_upper = (130, 255, 255) #RGB

#The video feed from the drone is then convereted, frame by frame, into an array of RGB values.
frame = get_frame(vid_stream, stream)
height, width = frame.shape[0], frame.shape[1]
colortracker = Tracker(height, width, color_lower, color_upper)
def get_frame(vid_stream, stream):
	"""grab the current video frame"""
	frame = vid_stream.read()
	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if stream else frame
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		return None
	else:
		frame = imutils.resize(frame, width=600)
		return frame
def track(self, frame):
	"""Simple HSV color space tracking"""
	# resize the frame, blur it, and convert it to the HSV
	# color space
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# construct a mask for the color then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, self.color_lower, self.color_upper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
							cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
# Once the center of the object is determined, its distance from the center of the frame is calculated. 

for c in cnts: #iterate through every contour
				#c = max(cnts, key=cv2.contourArea)
				((x, y), radius) = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

				# only proceed if the radius meets a minimum size
				if radius > 10:
					

					temp_xoffset = int(center[0] - self.midx) #store the xoffset and yoffset for each iteration of the loop
					temp_yoffset = int(self.midy - center[1])

					#calculate the distance from the previous x and y by finding the squared error
					sqrd_error = ((temp_xoffset-self.xoffset)**2) + ((temp_yoffset - self.yoffset)**2)

					#Set xoffset and yoffset for the lowest possible distance
					if lowest_error is None or sqrd_error < lowest_error:
						lowest_error = sqrd_error
						best_xoffset = temp_xoffset
						best_yoffset = temp_yoffset
						best_x = x
						best_y = y
						best_radius = radius
						best_center = center


			#Set xoffset and yoffset to the best values calculated in the for loop		
			self.xoffset = best_xoffset
			self.yoffset = best_yoffset
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(best_x), int(best_y)), int(best_radius), # Draws the yellow circle on video stream
					(0, 255, 255), 2)
			cv2.circle(frame, best_center, 5, (0, 0, 255), -1) # Draws a red dot in the center of the yellow circle
		else:
			self.xoffset = 0
			self.yoffset = 0

		return self.xoffset, self.yoffset #feed the optimized xoffset and yoffset to telloCV.py