from pydub import AudioSegment

audio=AudioSegment.from_wav("wav-audio.wav")

audio=audio+6

audio=audio*2

audio=audio.fade_in(2000)

audio.export("awaz.mp3",format="mp3")

audio2=AudioSegment.from_mp3("awaz.mp3")
print("done")
