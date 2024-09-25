import wave
import matplotlib.pyplot as plt
import numpy as np

obj=wave.open("wav-audio.wav","rb")

sample_freq=obj.getframerate()
n_samples=obj.getnframes()
signal_wave=obj.readframes(-1)

obj.close()

t_audio=n_samples/sample_freq

print(t_audio)

signal_array=np.frombuffer(signal_wave,dtype=np.int16)

times=np.linspace(0,t_audio,num=n_samples)

plt.figure(figsize=(15,5))
plt.plot(times, signal_array)
plt.title("Audio Signal")
plt.ylabel("Siganl wave")
plt.xlabel("TIme (S)")
plt.xlim(0,t_audio)
plt.show()