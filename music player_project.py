import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pygame

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
    if file_path:
        playlist.insert(tk.END, os.path.basename(file_path))
        music_list.append(file_path)

def play_music():
    if not pygame.mixer.music.get_busy():
        selected_song = playlist.curselection()
        if selected_song:
            index = selected_song[0]
            pygame.mixer.music.load(music_list[index])
            pygame.mixer.music.play()
            update_status()

def stop_music():
    pygame.mixer.music.stop()
    status_var.set("Music Stopped")

def pause_music():
    pygame.mixer.music.pause()
    status_var.set("Music Paused")

def resume_music():
    pygame.mixer.music.unpause()
    update_status()

def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

def next_song():
    current_index = playlist.curselection()
    if current_index:
        index = current_index[0]
        next_index = (index + 1) % len(music_list)
        playlist.selection_clear(index)
        playlist.selection_set(next_index)
        play_music()

def prev_song():
    current_index = playlist.curselection()
    if current_index:
        index = current_index[0]
        prev_index = (index - 1) % len(music_list)
        playlist.selection_clear(index)
        playlist.selection_set(prev_index)
        play_music()

def update_status():
    if pygame.mixer.music.get_busy():
        current_song = os.path.basename(music_list[playlist.curselection()[0]])
        status_var.set("Now Playing: " + current_song)
        app.after(1000, update_status)

def set_position(pos):
    pos = int(pos)
    pygame.mixer.music.set_pos(pos / 1000.0)

app = tk.Tk()
app.title("Music Player")
app.geometry("500x500")

music_list = []

playlist = tk.Listbox(app, selectmode=tk.SINGLE, width=40)
playlist.pack(pady=20)

browse_button = tk.Button(app, text="Browse", command=browse_file)
play_button = tk.Button(app, text="Play", command=play_music)
stop_button = tk.Button(app, text="Stop", command=stop_music)
pause_button = tk.Button(app, text="Pause", command=pause_music)
resume_button = tk.Button(app, text="Resume", command=resume_music)
prev_button = tk.Button(app, text="Previous", command=prev_song)
next_button = tk.Button(app, text="Next", command=next_song)

browse_button.pack()
play_button.pack()
stop_button.pack()
pause_button.pack()
resume_button.pack()
prev_button.pack()
next_button.pack()

volume_scale = ttk.Scale(app, from_=0, to=100, orient=tk.HORIZONTAL, command=set_volume)
volume_scale.set(50)  # Set the default volume to 50%
volume_scale.pack(pady=20)

status_var = tk.StringVar()
status_label = tk.Label(app, textvariable=status_var)
status_label.pack()

seek_scale = ttk.Scale(app, from_=0, to=1000, orient=tk.HORIZONTAL, command=set_position)
seek_scale.pack(pady=20)

pygame.mixer.init()

app.after(1000, update_status)  # Update the status label every second

app.mainloop()
