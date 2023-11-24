from pydub import AudioSegment
import pyaudio
import io
import threading
import time


class AudioDriver:
    def __init__(self) -> None:
        self.p = pyaudio.PyAudio()
        self.stream: pyaudio.Stream = None
        self.writing = False

    def __del__(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()

    def play(self, buffer: io.BytesIO, sample_rate: int):
        if not self.stream:
            print("Starting stream")
            self.stream = self.p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                output=True,
            )

        stream_thread = threading.Thread(
            target=self.play_thread,
            args=(buffer,),
            daemon=True,
        )
        stream_thread.start()

    def play_thread(self, buffer: io.BytesIO):
        while self.writing:
            time.sleep(0.01)
            pass

        self.writing = True
        data = buffer.read(1024)
        while data:
            try:
                self.stream.write(data)
            except:
                print("Error writing to stream")
                break
            data = buffer.read(1024)
        self.writing = False

    def set_speed(self, speed):
        if not self.stream:
            return

    def resume(self):
        if not self.stream:
            return
        try:
            self.stream.start_stream()
        except:
            pass

    def pause(self):
        if not self.stream:
            return

        self.stream.stop_stream()

    def stop(self):
        if not self.stream:
            return

        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
