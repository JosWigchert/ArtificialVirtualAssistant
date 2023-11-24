from pydub import AudioSegment
import pyaudio
import io
import sounddevice as sd
import soundfile as sf


class AudioUtility:
    def openai_to_audio(self, response):
        buffer = io.BytesIO()
        for chunk in response.iter_bytes(chunk_size=1024):
            buffer.write(chunk)
        buffer.seek(0)

        data, samplerate = sf.read(buffer, dtype="int16")
        buffer = io.BytesIO()
        sf.write(buffer, data, samplerate, format="WAV")

        # seek to 1024 to remove the click heared in the beginning of the clip
        buffer.seek(1024)

        return buffer, samplerate
