from MainThread import MainThread


def main():

	main_thread = MainThread(0, "main_thread")
	main_thread.start()

if __name__ == "__main__":
	main()
