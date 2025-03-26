import os
import wave
import pyaudio
import threading
import time


class AudioHandler:
    def __init__(self):
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 2
        self.fs = 44100
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False
        self.stream = None
        self.recording_thread = None

    def start_recording(self):
        self.frames = []
        self.is_recording = True
        self.stream = self.p.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.fs,
            frames_per_buffer=self.chunk,
            input=True,
        )

        # Start recording in a separate thread
        self.recording_thread = threading.Thread(target=self._record)
        self.recording_thread.start()
        print("Recording started...")

    def _record(self):
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def stop_recording(self):
        self.is_recording = False
        if self.recording_thread:
            self.recording_thread.join()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        print("Recording stopped.")

    def save_recording(self, filename):
        if not self.frames:
            print("No recording to save.")
            return

        with wave.open(filename, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b"".join(self.frames))
        print(f"Recording saved as {filename}.")

    def play_recording(self, filename):
        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            return

        wf = wave.open(filename, "rb")
        stream = self.p.open(
            format=self.p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
        )

        data = wf.readframes(self.chunk)
        while data:
            stream.write(data)
            data = wf.readframes(self.chunk)

        stream.stop_stream()
        stream.close()
        print(f"Playback finished for {filename}.")

    def __del__(self):
        self.p.terminate()
