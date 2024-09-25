import wave

obj=wave.open("wav-audio.wav","rb")

print("Number of Channels",obj.getnchannels())
print("Sample width",obj.getsampwidth())
print("frame rate",obj.getframerate())
print("Number of frames",obj.getnframes())
print("parameters",obj.getparams())

t_audio = obj.getnframes()/obj.getframerate()
print(t_audio)

frames=obj.readframes(-1)
print(type(frames),type(frames[0]))
print(len(frames)/4)

obj.close()

obj_new=wave.open("wav-audio_new.wav","wb")

obj_new.setnchannels(2)
obj_new.setsampwidth(2)
obj_new.setframerate(48000)

obj_new.writeframes(frames)

obj_new.close()
