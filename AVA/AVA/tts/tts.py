from AVA.utils import Environment
from AVA.model import OpenAI
from AVA.audio import AudioDriver, AudioUtility
import time
import threading


env = Environment()
llm = OpenAI(env.OPENAI_API_KEY, env.OPENAI_ENGINE, env.OPENAI_EMBEDDINGS)

print("Getting tts")
audio_content = llm.generate_tts(
    "CSI exhibits various prominent ",
    speed=1.2,
)
print(f"tts response {audio_content}")


utility = AudioUtility()
driver = AudioDriver()

buffer, samplerate = utility.openai_to_audio(audio_content)
driver.play(buffer, samplerate)
time.sleep(1)
driver.stop()
time.sleep(1)
# driver.resume()

buffer2, samplerate2 = utility.openai_to_audio(audio_content)
driver.play(buffer2, samplerate2)

time.sleep(8)
