from AVA.utils import Environment
from AVA.model import OpenAI
from pydub import AudioSegment
import pyaudio
import io
import sounddevice as sd
import soundfile as sf

env = Environment()

llm = OpenAI(env.OPENAI_API_KEY, env.OPENAI_ENGINE, env.OPENAI_EMBEDDINGS)

audio_content = llm.generate_tts("Hello")

buffer = io.BytesIO()
for chunk in audio_content.iter_bytes(chunk_size=4096):
    buffer.write(chunk)
buffer.seek(0)

print("Buffer done")

from AVA.utils import Environment
from AVA.model import OpenAI
from pydub import AudioSegment
import pyaudio
import io
import sounddevice as sd
import soundfile as sf

env = Environment()

llm = OpenAI(env.OPENAI_API_KEY, env.OPENAI_ENGINE, env.OPENAI_EMBEDDINGS)

audio_content = llm.generate_tts(
    "CSI exhibits various prominent features as compared to RSSI offering more unique location signatures. Traditional RSSI presents an aggregated scalar value at the packet level, whereas CSI indicates the channel information at sub-carrier level. In addition, CSI provides complex channel information that includes magnitude and phase information for each sub-carrier, and for each transmit and receive antenna. Multiple sub-carriers attenuate differently when traveled through various traveling paths, thus resulting in variation of amplitude and phase of each sub-carrier. The fine-granularity of CSI in terms of frequency and spatial diversity makes it suitable metric to represent a location uniquely and to enhance the localization accuracy. Recently, the CSI is extractable using the Linux tool using off-the-shelf Intel 5300 Network Interface Card (NIC) [5]."
)

buffer = io.BytesIO()
for chunk in audio_content.iter_bytes(chunk_size=4096):
    buffer.write(chunk)
buffer.seek(0)

print("Buffer done")

data, samplerate = sf.read(buffer, dtype="int16")
print("Data done")
try:
    sd.play(data, samplerate)
    sd.wait()
except Exception as e:
    print(f"Error during playback: {e}")
