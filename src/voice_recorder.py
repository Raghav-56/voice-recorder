import os
import time
import audio_handler
import utils
import msvcrt  # Windows-specific module for keyboard input


def input_ready():
    # Check if a key was pressed
    if msvcrt.kbhit():
        # Check if Enter key was pressed
        key = msvcrt.getch()
        return key in [b"\r", b"\n"]
    return False


def main():
    # Create an instance of AudioHandler
    recorder = audio_handler.AudioHandler()

    while True:
        print("\nVoice Recorder Menu:")
        print("1. Start Recording")
        print("2. Stop Recording & Save")
        print("3. List Available Recordings")
        print("4. Play a Selected Recording")
        print("5. Exit")

        choice = input("Select an option (1-5): ")

        if choice == "1":
            recorder.start_recording()
            print("Recording started... Press Enter to stop.")
            start_time = time.time()
            try:
                while True:
                    elapsed = time.time() - start_time
                    print(f"\rRecording: {elapsed:.1f} seconds", end="")
                    time.sleep(0.1)
                    if input_ready():
                        break
            except KeyboardInterrupt:
                pass
            print("\nRecording stopped.")
        elif choice == "2":
            recorder.stop_recording()
            filename = utils.generate_filename()
            file_path = os.path.join("recordings", filename)
            recorder.save_recording(file_path)
        elif choice == "3":
            recordings = utils.list_recordings()
            print("\nAvailable Recordings:")
            for idx, recording in enumerate(recordings):
                print(f"{idx + 1}. {recording}")
        elif choice == "4":
            recordings = utils.list_recordings()
            if recordings:
                print("\nAvailable Recordings:")
                for idx, recording in enumerate(recordings):
                    print(f"{idx + 1}. {recording}")
                idx = int(input("Select a recording number to play: ")) - 1
                if 0 <= idx < len(recordings):
                    file_path = os.path.join("recordings", recordings[idx])
                    recorder.play_recording(file_path)
                else:
                    print("Invalid selection.")
            else:
                print("No recordings available.")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    if not os.path.exists("recordings"):
        os.makedirs("recordings")
    main()
