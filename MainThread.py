import cv2
import numpy as np
import sys
import threading

from CameraThread import CameraThread


class MainThread():

	def __init__(self, thread_id, thread_name):
		# display title
		self.print_text("[ barcode detection ]")
		
		# get parameters
		self.thread_id = thread_id
		self.thread_name = thread_name
		
		# calculate morphological kernel
		self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 5))
		
		# create thread
		self.camera_thread = CameraThread(1, "camera_thread", self)

	# start thread
	def start(self):
		self.print_text("starting thread: id (%d), name (%s)" %
			(self.thread_id, self.thread_name))
		self.camera_thread.start()

	# stop thread
	def stop(self):
		self.print_text("stopping thread: id (%d), name (%s)" %
			(self.thread_id, self.thread_name))
		cv2.destroyAllWindows()
		sys.exit()

	# display text on terminal
	def print_text(self, text):
		print text

	# detect barcode in image
	def _detect_barcode(self, img):
		# convert image to grayscale
		gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# calculate Sobel X gradient
		grad_x = cv2.Sobel(
			gray_img, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
		grad_img = cv2.convertScaleAbs(grad_x)

		# remove noise by blurring and extract barcode by thresholding
		blur_img = cv2.blur(grad_img, (9,9))
		(_, thresh_img) = cv2.threshold(
			blur_img, 225, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

		# enhance barcode region by morphology
		morph_img = cv2.morphologyEx(
			thresh_img, cv2.MORPH_CLOSE, self.kernel, iterations=1)
		morph_img = cv2.erode(morph_img, None, iterations=8)

		# find largest contour and calculate bounding box
		(_, contours, _) = cv2.findContours(morph_img.copy(), 
			cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		if len(contours) > 0:
			cnt = sorted(
				contours, key=cv2.contourArea, reverse=True)[0]
			rect = cv2.minAreaRect(cnt)
			bbox = np.int0(cv2.boxPoints(rect))
			return rect, bbox
		else:
			return None

	''' WORK IN PROGRESS
	def _scan_barcode(self, img, rect):
		if rect is None:
			return None
		gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		(x, y) = np.int0(rect[0])
		(w, h) = np.int0(rect[1])
		angle = rect[2]
		if angle < -45.0:
			angle += 90.0
			w, h = h, w
		M = cv2.getRotationMatrix2D((x,y), angle, 1.0)
		rot_img = cv2.warpAffine(img, M, gray_img.shape)
		barcode_img = cv2.getRectSubPix(rot_img, (w,h), (x,y))
		return barcode_img
	'''

	def process(self, frame):
		# mirror the camera frame
		frame = cv2.flip(frame, 1)

		# detect barcode in image
		rect, bbox = self._detect_barcode(frame)

		# draw barcode bounding box on frame
		bbox_img = frame.copy()
		if bbox is not None: 
			cv2.drawContours(bbox_img, [bbox], -1, (0,255,0), 2)

		''' WORK IN PROGRESS		
		barcode_img = self._scan_barcode(frame, rect)
		bg_img = np.zeros(frame.shape, dtype=frame.dtype)
		if barcode_img is not None:
			(w, h, _) = barcode_img.shape
			bg_img[:w, :h, :] = barcode_img

		result_img = np.hstack([bbox_img, bg_img])
		result_img = cv2.resize(result_img, dsize=(0,0), fx=0.5, fy=0.5)
		'''

		# display result
		cv2.imshow("result", bbox_img)
