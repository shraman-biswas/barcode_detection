import cv2
import numpy as np
import sys
import threading


class CameraThread(threading.Thread):

	def __init__(self, thread_id, thread_name, main_thread):
		threading.Thread.__init__(self)
		self.stopped = False
		
		# get parameters		
		self.thread_id = thread_id
		self.thread_name = thread_name
		self.main_thread = main_thread

	# run thread
	def run(self):
		self.main_thread.print_text("starting thread: id (%d), name (%s)" %
			(self.thread_id, self.thread_name))
		
		# get camera name
		camera_id = 0 if len(sys.argv) == 1 else int(sys.argv[1])
		
		# access camera
		self.camera = cv2.VideoCapture(camera_id)
		self.main_thread.print_text("accessed camera (id: %d)" % camera_id)
		
		# thread loop
		self.main_thread.print_text("press 'q' to quit")
		while not self.stopped:
			ret, frame = self.camera.read()
			if frame.size is None:
				self.stop()
			self.main_thread.process(frame)
			ch = cv2.waitKey(1)
			if ch == ord('q'):
				self.stop()
		
		# stop parent thread (main)
		self.main_thread.stop()

	# stop thread
	def stop(self):
		self.main_thread.print_text("stopping thread: id (%d), name (%s)" %
			(self.thread_id, self.thread_name))
		self.camera.release()
		self.stopped = True