import os
import customtkinter
import pygame
from tkinter import filedialog
from gtts import gTTS
from pygame import mixer
import tempfile

# Initialize pygame and pygame.mixer
pygame.init()
pygame.mixer.init()

# Set the appearance mode and default color theme (customtkinter)
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# define number of columns
num_cols = 4

# Get all files in the sounds directory
sound_files = os.listdir("sounds")

# Filter out non-wav files
sound_files = [file for file in sound_files if os.path.splitext(file)[1] == ".wav"]

# Build a dictionary where the keys are the file names without the extension
# and the values are the file paths
audio_files = {os.path.splitext(file)[0]: f"sounds/{file}" for file in sound_files}

# Create the GUI with buttons for each sound
root = customtkinter.CTk()
root.geometry("500x720")
root.title("Dreaddy Bear's Sound Bored")

# Create an empty frame that takes up the entire root window
drag_frame = customtkinter.CTkFrame(root, width=500, height=620)
drag_frame.pack_propagate(False) # prevent the frame from shrinking
drag_frame.pack()

# Create a frame for the grid
grid_frame = customtkinter.CTkFrame(drag_frame)
grid_frame.place(relx=0.5, rely=0.5, anchor='c',) # place the frame at the center of drag_frame

# Define the functions
# function to choose a file
def choose_file(sound_index):
    file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=(("Audio Files", "*.wav *.mp3"),))
    if file_path:
        audio_files[sound_index] = file_path
        button[sound_index].configure(text=os.path.basename(file_path))
# function to stop all sounds
def stop_sounds():
    pygame.mixer.music.stop()
    pygame.mixer.stop()
# function to play a sound
def play_sound(file_path, volume_slider_index):
    if isRetrigger.get() == True:
        pygame.mixer.music.load(file_path)
        volume = volume_sliders[volume_slider_index].get()
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()
    else:    
        sound = pygame.mixer.Sound(file_path)
        volume = volume_sliders[volume_slider_index].get()
        sound.set_volume(volume)
        sound.play()
# function to print the volumes (for debugging)
def print_volumes():
    for i, volume_slider in enumerate(volume_sliders):
        volume = volume_slider.get()
        print(f"Sound {i+1} volume: {volume:.2f}")
# function to show the settings window
def show_settings():
    settings_window = customtkinter.CTkToplevel(root)
    settings_window.title("Settings")

    # Create a frame for the choose file buttons
    choose_file_frame = customtkinter.CTkFrame(settings_window)
    choose_file_frame.pack(padx=10, pady=10)

    # create a choose file button for each sound file
    for i, (sound_name, file_path) in enumerate(audio_files.items()):
        choose_button = customtkinter.CTkButton(choose_file_frame, text="Choose File", command=lambda index=sound_name: choose_file(index))
        choose_button.pack(padx=10, pady=5)

    # Create a master volume slider
    volume_label = customtkinter.CTkLabel(settings_window, text="Master Volume")
    volume_label.pack(padx=10, pady=10)

    volume_slider = customtkinter.CTkSlider(settings_window, from_=0.0, to=1.0, orientation="horizontal")
    volume_slider.pack(padx=10, pady=10)
    volume_slider.set(1.00)

    # Create a button to save settings
    save_button = customtkinter.CTkButton(settings_window, text="Save", command=save_settings)
    save_button.pack(padx=10, pady=10)

    def save_settings():
        # code to save settings goes here
        settings_window.withdraw()



def show_roboSpeak():
    robo_speak = customtkinter.CTkToplevel(root)
    robo_speak.title("Talk to me")
    enterSpeak = customtkinter.CTkTextbox(robo_speak, width=300, height=300)
    enterSpeak.pack(padx=10, pady=10)
    
    # create a new function that gets the current text and speaks it
    def speak_current_text():
        text_to_speech(enterSpeak.get("1.0", "end-1c"))
        enterSpeak.delete("1.0", "end-1c")

    sendSpeak = customtkinter.CTkButton(robo_speak, text="Send", command=speak_current_text)
    sendSpeak.pack(padx=10, pady=10)
    # save_button = customtkinter.CTkButton(settings_window, text="Save", command=save_settings)
    # save_button.pack(padx=10, pady=10)

    # add an action listener to the enterSpeak textbox that calls speak_current_text when the user presses enter
    enterSpeak.bind("<Return>", lambda event: speak_current_text())


def text_to_speech(text):
    # tts using gTTS
    tts = gTTS(text=text, lang='en') # adjust lang parameter as needed
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        temp_filename = fp.name + '.mp3'
    tts.save(temp_filename)
    mixer.music.load(temp_filename)
    mixer.music.play()

# Create a check box to toggle retrigger
isRetrigger = customtkinter.BooleanVar()
isRetrigger.set(True)
retrigger_checkbox = customtkinter.CTkCheckBox(grid_frame, text="Retrigger", variable=isRetrigger)
retrigger_checkbox.grid(row=len(audio_files) // num_cols + 3, column=num_cols - 1, sticky="SE", padx=10, pady=10)

# Create the sound buttons and volume sliders
volume_sliders = []
for i, (sound_name, file_path) in enumerate(audio_files.items()):
    # Create a frame for the sound
    sound_frame = customtkinter.CTkFrame(master=grid_frame)
    sound_frame.grid(row=i // num_cols, column=i % num_cols, padx=5, pady=5)
    
    # Create a button for the sound
    button = customtkinter.CTkButton(sound_frame, width=100, text=sound_name, command=lambda file_path=file_path, volume_slider_index=i: play_sound(file_path, volume_slider_index))
    button.pack(padx=5, pady=5)
    
    volume_slider = customtkinter.CTkSlider(sound_frame, from_=0.0, to=1.0, width=100, orientation="horizontal")
    volume_slider.pack(padx=5, pady=(0, 5))
    volume_slider.set(1.00)
    volume_sliders.append(volume_slider)

# Create a button to show the settings window
settings_button = customtkinter.CTkButton(grid_frame, text="Settings", command=show_settings, width=80)
settings_button.grid(row=len(audio_files) // num_cols + 1, column=num_cols - 1, sticky="SE", padx=4, pady=4)

# Create a button to stop all sounds
stop_button = customtkinter.CTkButton(grid_frame, text="STFU", command=stop_sounds, width=80)
stop_button.grid(row=len(audio_files) // num_cols + 2, column=num_cols - 1, sticky="SE", padx=4, pady=4)

# add an action listener to allow user to drag the window from the negative space on the frame
def start_move(event):
    root.x = event.x_root - root.winfo_rootx()
    root.y = event.y_root - root.winfo_rooty()

def move_window(event):
    x = event.x_root - root.x
    y = event.y_root - root.y
    root.geometry("+%s+%s" % (x, y))

# bind the action listeners to the root
drag_frame.bind('<ButtonPress-1>', start_move)
drag_frame.bind('<B1-Motion>', move_window)

# Empty bindings for the grid_frame and its children
def dummy(event):
    pass

drag_area = customtkinter.CTkFrame(root, width=500, height=200)  # adjust dimensions as needed
drag_area.pack(side='bottom', fill='x')  # pack the frame at the bottom of the root window

drag_area.bind('<ButtonPress-1>', start_move)
drag_area.bind('<B1-Motion>', move_window)


grid_frame.bind('<ButtonPress-1>', dummy)
grid_frame.bind('<B1-Motion>', dummy)

robotspeak = customtkinter.CTkButton(grid_frame, text="Robot Speak", command=show_roboSpeak, width=80)
robotspeak.grid(row=len(audio_files) // num_cols + 4, column=num_cols - 1, sticky="SE", padx=4, pady=4)

root.mainloop()

