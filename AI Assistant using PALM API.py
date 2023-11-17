import tkinter as tk
import pygame
from gtts import gTTS
import os
import time
import speech_recognition as sr
import whisper
import warnings
import google.generativeai as palm

pygame.mixer.init()
palm.configure(api_key="AIzaSyB6D_z_aH6b4JsJJf5aWL-j1hMZbaW9nGQ")


speak_text = ''  # Declare speak_text as a global variable

# Specify the directory where you have write permissions (e.g., user's home directory)
audio_directory = os.path.expanduser("~")
r = sr.Recognizer()
tiny_model = whisper.load_model('tiny')
base_model = whisper.load_model('base')
warnings.filterwarnings('ignore', message="FP16 is not supported on CPU; using FP32 instead")

def send_prompt():
    global speak_text  # Declare that you want to use the global speak_text variable
    prompt = prompt_var.get()
    response_ = palm.chat(messages=[prompt])
    speak_text = response_.last
    response.delete('1.0', 'end')
    response.insert('1.0', response_.last)
    root.update()
    root.update_idletasks()

def speak():
    tts = gTTS(text=speak_text, lang='en')
    audio_file = os.path.join(audio_directory, "temp.mp3")
    tts.save(audio_file)
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.music.unload()
    os.remove(r"C:\Users\vmaha\temp.mp3")

def hear_text():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = r.listen(source, timeout=2, phrase_time_limit=3)
            with open("prompt.wav", "wb") as f:
                f.write(audio.get_wav_data())
            result = base_model.transcribe('prompt.wav')
            prompt_text = result['text']
            print("Heard:", prompt_text)
            prompt_var.set(prompt_text)
        except sr.WaitTimeoutError:
            print("Listening timeout. No speech detected.")


root = tk.Tk(screenName="AI assistant")
root.geometry("600x500")

prompt_var = tk.StringVar()
response_var = tk.StringVar()
prompt_entry = tk.Entry(root, textvariable=prompt_var, font=('calibre', 10, 'normal'), width=30)
prompt_entry.place(x=10, y=10)

send = tk.Button(root, text="Send", command=send_prompt, font=('calibre', 10, 'normal'))
send.place(x=230, y=10)

response = tk.Text(root, font=('calibre', 10, 'normal'))
response.place(x=10, y=50)

speak_button = tk.Button(root, text="Speak", font=('calibre', 10, 'normal'), command=speak)
speak_button.place(x=300, y=10)

voice_button = tk.Button(root, text="Voice", font=('calibre', 10, 'normal'), command=hear_text)
voice_button.place(x=370, y=10)

root.mainloop()
