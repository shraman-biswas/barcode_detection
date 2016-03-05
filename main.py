from MainThread import MainThread


def main():

	# create and start main thread
	main_thread = MainThread(0, "main_thread")
	main_thread.start()

if __name__ == "__main__":
	main()
