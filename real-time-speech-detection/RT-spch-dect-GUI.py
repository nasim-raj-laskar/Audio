#prerequisite labraies
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import pyaudio
import json
from vosk import Model, KaldiRecognizer
from threading import Thread, Event
from queue import Queue

#audio parameters
CHANNELS = 1
FRAME_RATE = 16000
RECORD_SECONDS = 2
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2

#load the model(light weight model....u can use a heavy model for better recognition)
model = Model(model_name="vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, FRAME_RATE)
rec.SetWords(True)

messages = Queue()
recordings = Queue()
stop_event = Event()

def record_microphone(chunk=512):
    p = pyaudio.PyAudio()
    stream = p.open(format=AUDIO_FORMAT,
                    channels=CHANNELS,
                    rate=FRAME_RATE,
                    input=True,
                    input_device_index=2, 
                    frames_per_buffer=chunk)
    
    frames = []
    
    while not stop_event.is_set():
        data = stream.read(chunk)
        frames.append(data)
        
        if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk:
            recordings.put(frames.copy())
            frames = []  

    stream.stop_stream()
    stream.close()
    p.terminate()

def speech_recognition(output_widget):
    while not stop_event.is_set() or not recordings.empty():
        if not recordings.empty():
            frames = recordings.get()
            print("Received frames for transcription")
            
            if rec.AcceptWaveform(b''.join(frames)):
                result = rec.Result()
                text = json.loads(result)["text"]
                print("Recognized TEXT:==>", text)
                
                output_widget.insert(tk.END, f"Recognized: {text}\n")
                output_widget.see(tk.END)

def start_recording(output_widget):
    messages.put(True)
    output_widget.insert(tk.END, "Starting recording...\n")
    output_widget.see(tk.END)
    
    stop_event.clear() 
    
    record_thread = Thread(target=record_microphone)
    record_thread.start()  
    transcribe_thread = Thread(target=speech_recognition, args=(output_widget,))
    transcribe_thread.start()

def stop_recording(output_widget):
    stop_event.set() 
    output_widget.insert(tk.END, "Stopped recording.\n")
    output_widget.see(tk.END)

def insert_image(output_widget, image_path):
    img = Image.open(image_path)
    img = img.resize((700, 700), Image.LANCZOS)  
    img_tk = ImageTk.PhotoImage(img)
    output_widget.image_create(tk.END, image=img_tk)
    output_widget.image = img_tk

# GUI 
def create_gui():
    root = tk.Tk()
    root.title("Speech Recog gok gok")
    root.configure(bg="#141414")

    output_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=72, height=21, bg="#000000", fg="white", font=("Helvetica", 12))
    output_widget.pack(pady=10)

     
    record_button = tk.Button(root, text="Start Recording ▶", command=lambda: start_recording(output_widget), bg="green", fg="white", font=("Helvetica", 15, "bold"), padx=20, pady=10)
    record_button.pack(side=tk.LEFT, padx=20, pady=20)

     
    stop_button = tk.Button(root, text="Stop Recording ■ ", command=lambda: stop_recording(output_widget), bg="red", fg="white", font=("Helvetica", 15, "bold"), padx=20, pady=10)
    stop_button.pack(side=tk.RIGHT, padx=20, pady=20)

    insert_image(output_widget, "35.jpg")

    root.geometry("700x500+300+100")

    root.mainloop()

if __name__ == "__main__":
    create_gui()
