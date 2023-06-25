import json
import os
import customtkinter
import pygame
from tkinter import filedialog
from gtts import gTTS
from pygame import mixer
import tempfile
import shutil
from tkinterdnd2 import DND_FILES, TkinterDnD



# Initialize pygame and pygame.mixer
pygame.init()
pygame.mixer.init()

# Set the appearance mode and default color theme (customtkinter)
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# define number of columns
num_cols = 4

new_sounds = []
new_sound_files = []
save_button = None  # Global variable to store the save button
try:
    with open('config.json', 'r') as file:
        json_string = file.read()
except FileNotFoundError:
    # open config.json from /default_settings
    with open('default_settings/config.json', 'r') as file:
        json_string = file.read()

# convert the JSON string to a Python dictionary
try:
    sound_files = json.loads(json_string)
except json.JSONDecodeError:
    print("Error: Config file is not valid JSON.")
    sound_files = {}

# define a list for accents to choose from
choose_accent = {
    "Australian": ("en", "com.au"),
    "British": ("en", "co.uk"),
    "American": ("en", "us"),
    "Canadian": ("en", "ca"),
    "Indian": ("en", "co.in"),
    "Irish": ("en", "ie"),
    "South African": ("en", "co.za")
}

ui_accent = list(choose_accent.keys())


# Define class Robot
class Robot:
    def __init__(self):
        self.accent = "Choose an accent"

class BoredObj:
    def __init__(self):
        self.isDirty = False

speakerBot = Robot()
mySoundBored = BoredObj()

# # Filter out non-wav files
# sound_files = [file for file in sound_files if os.path.splitext(file)[1] == ".wav"]

# Build a dictionary where the keys are the file names without the extension
# and the values are the file paths
audio_files = {os.path.splitext(file)[0]: f"sounds/{file}" for file in sound_files}

# Create the GUI with buttons for each sound
root = TkinterDnD.Tk()
root.geometry("380x720")
root.title("Dreaddy Bear's Sound Bored")

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
# show save button function
def show_save_button():
    global save_button  # Declare the save_button as global to modify it
    save_button = customtkinter.CTkButton(grid_frame, text="Save", command=save_sounds)
    save_button.grid(row=(len(audio_files) // num_cols) + 2, column=num_cols - 3, sticky="E", padx=4, pady=4)
    
def save_sounds():
    with open('config.json', 'r') as f:
        sounds = json.load(f)

    # Add new sounds to the list
    for file_path in new_sound_files:
        sound_name = os.path.basename(file_path)
        sounds.append(sound_name)
    
    # Save updated list to config.json
    with open('config.json', 'w') as f:
        json.dump(sounds, f)
    
    # Copy each sound file to /sounds/ (ensure /sounds/ directory exists)
    os.makedirs('sounds', exist_ok=True)
    tmp_directory = 'tmp/'  # Update the directory path accordingly

    for file_name in os.listdir(tmp_directory):
        if os.path.splitext(file_name)[1] in ['.wav', '.mp3']:
            file_path = os.path.join(tmp_directory, file_name)
            shutil.copy(file_path, 'sounds/')

    # Clear the tmp/ directory
    for file_name in os.listdir(tmp_directory):
        file_path = os.path.join(tmp_directory, file_name)
        os.remove(file_path)
    hide_save_button()
    mySoundBored.isDirty = False

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

    # # create a choose file button for each sound file 
    # for i, (sound_name, file_path) in enumerate(audio_files.items()):
    #     choose_button = customtkinter.CTkButton(choose_file_frame, text="Choose File", command=lambda index=sound_name: choose_file(index))
    #     choose_button.pack(padx=10, pady=5)

    # Create a master volume slider
    volume_label = customtkinter.CTkLabel(settings_window, text="Master Volume")
    volume_label.pack(padx=10, pady=10)

    sound_volume_slider = customtkinter.CTkSlider(settings_window, from_=0, to=1, orientation="horizontal")
    sound_volume_slider.pack(padx=10, pady=10)
    sound_volume_slider.set(1.00)

    # # Create a button to save settings
    # save_button = customtkinter.CTkButton(settings_window, text="Save", command=save_settings)
    # save_button.pack(padx=10, pady=10)


    def save_settings():
        # code to save settings goes here
        settings_window.withdraw()
# function to hide the save button
def hide_save_button():
    global save_button  # Declare the save_button as global to modify it
    if save_button:
        save_button.grid_forget()

# function to show the roboSpeak window
def show_roboSpeak():
    robo_speak = customtkinter.CTkToplevel(root)
    robo_speak.title("Talk to me")
    robo_speak.lift()
    robo_speak.attributes('-topmost', True) # This line keeps the robo_speak window always on top

    # Create a frame that takes up the entire robo_speak window
    robo_drag_frame = customtkinter.CTkFrame(robo_speak, width=300, height=120)
    robo_drag_frame.pack_propagate(False) # prevent the frame from shrinking
    

     # Add an action listener to allow the user to drag the window from the negative space on the frame
    def start_move_robo(event):
        robo_speak.x = event.x_root - robo_speak.winfo_rootx()
        robo_speak.y = event.y_root - robo_speak.winfo_rooty()

    def move_robo_window(event):
        x = event.x_root - robo_speak.x
        y = event.y_root - robo_speak.y
        robo_speak.geometry("+%s+%s" % (x, y))

    # Bind the action listeners to the robo_speak window
    robo_drag_frame.bind('<ButtonPress-1>', start_move_robo)
    robo_drag_frame.bind('<B1-Motion>', move_robo_window)

    enterSpeak = customtkinter.CTkTextbox(robo_speak, width=300, height=300)
    enterSpeak.pack(padx=10, pady=10)
    
    robo_drag_frame.pack()

    def optionmenu_callback(choice):
        if choice == "Choose an accent":
            speakerBot.accent = choose_accent["American"]
        else:
            speakerBot.accent = choose_accent[choice]
        print("optionmenu dropdown clicked:", choice)

    optionmenu_var = customtkinter.StringVar(value="Choose an accent")
    optionmenu = customtkinter.CTkOptionMenu(
        robo_speak,
        values=["Choose an accent"] + ui_accent,
        command=optionmenu_callback,
        variable=optionmenu_var
    )
    
    optionmenu.pack()

    # create a new function that gets the current text and speaks it
    def speak_current_text():
        text_to_speech(enterSpeak.get("1.0", "end-1c"), speakerBot.accent)
        enterSpeak.delete("1.0", "end-1c")

    sendSpeak = customtkinter.CTkButton(robo_speak, text="Send", command=speak_current_text)
    sendSpeak.pack(padx=10, pady=10)

    # add an action listener to the enterSpeak textbox that calls speak_current_text when the user presses enter
    enterSpeak.bind("<Return>", lambda event: speak_current_text())


def text_to_speech(text, accent):
    if accent == "Choose an accent":
        lang = "en"
        tld = "us"
    else:
        lang, tld = accent

    tts = gTTS(text=text, lang=lang, tld=tld)
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        temp_filename = fp.name + '.mp3'
    tts.save(temp_filename)
    print(lang, tld, temp_filename)
    mixer.music.load(temp_filename)
    mixer.music.play()

# Create an empty frame that takes up the entire root window
drag_frame = customtkinter.CTkFrame(root, width=360, height=820)


# Create a frame for the grid
grid_frame = customtkinter.CTkFrame(drag_frame)
grid_frame.pack(fill="both", expand=True)  # fill the parent frame and allow expanding
drag_frame.pack()

# Create the sound buttons and volume sliders
volume_sliders = []
for i, (sound_name, file_path) in enumerate(audio_files.items()):
    # Create a frame for the sound
    sound_frame = customtkinter.CTkFrame(master=grid_frame)
    sound_frame.grid(row=i // num_cols, column=i % num_cols, padx=5, pady=5)

    # Configure the row and column to be stretchable
    grid_frame.grid_rowconfigure(i // num_cols, weight=1)
    grid_frame.grid_columnconfigure(i % num_cols, weight=1)
    
    # Create a button for the sound
    button = customtkinter.CTkButton(sound_frame, width=100, text=sound_name, command=lambda file_path=file_path, volume_slider_index=i: play_sound(file_path, volume_slider_index))
    button.pack(fill="both", expand=True, padx=5, pady=5)
    
    volume_slider = customtkinter.CTkSlider(sound_frame, from_=0.0, to=1.0, width=100, orientation="horizontal")
    volume_slider.pack(fill="both", expand=True, padx=5, pady=(0, 5))
    volume_slider.set(1.00)
    volume_sliders.append(volume_slider)

# Create a button to show the settings window
settings_button = customtkinter.CTkButton(grid_frame, text="Settings", command=show_settings, width=80)
settings_button.grid(row=(len(audio_files) // num_cols) + 2, column=num_cols - 1, sticky="E", padx=4, pady=4)

# Create a button to stop all sounds
stop_button = customtkinter.CTkButton(grid_frame, text="STFU", command=stop_sounds, width=80)
stop_button.grid(row=(len(audio_files) // num_cols) + 1, column=num_cols - 1, sticky="E", padx=4, pady=4)

# Create a check box to toggle retrigger
isRetrigger = customtkinter.BooleanVar()
isRetrigger.set(True)
retrigger_checkbox = customtkinter.CTkCheckBox(grid_frame, text="Retrigger", variable=isRetrigger)
retrigger_checkbox.grid(row=(len(audio_files) // num_cols) + 2, column=num_cols - 2, sticky="E", padx=4, pady=4)

# Create a button to show the roboSpeak window
robotspeak = customtkinter.CTkButton(grid_frame, text="Robot Speak", command=show_roboSpeak, width=80)
robotspeak.grid(row=(len(audio_files) // num_cols) , column=num_cols - 1, sticky="E", padx=4, pady=4)




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

drag_area = customtkinter.CTkFrame(root, width=500, height=444)  # adjust dimensions as needed
drag_area.pack(side='bottom', fill='x')  # pack the frame at the bottom of the root window

drag_me_label = customtkinter.CTkLabel(drag_area, text="Drag me!", width=10, height=10)
drag_me_label.place(relx=0.5, rely=0.5, anchor='s')

drag_area.bind('<ButtonPress-1>', start_move)
drag_area.bind('<B1-Motion>', move_window)


grid_frame.bind('<ButtonPress-1>', dummy)
grid_frame.bind('<B1-Motion>', dummy)

# handle file drop
def drop(event):
    print("attempting drop.")
    dropped_file_path = event.data
    file_extension = os.path.splitext(dropped_file_path)[1]
    if file_extension in [".wav", ".mp3}"]:
        if file_extension == ".mp3}":
            dropped_file_path = dropped_file_path[1:-1]
        print("test1: " + dropped_file_path)
        print("test2: " + file_extension)
        new_sound_files.append(dropped_file_path)
        sound_name = os.path.splitext(os.path.basename(dropped_file_path))[0]
        new_sounds.append(sound_name)
        
        print("Sound name: " + sound_name)
        # Create a frame for the sound
        sound_frame = customtkinter.CTkFrame(master=grid_frame)
        sound_frame.grid(row=i // num_cols, column=i % num_cols + 1, padx=5, pady=5)
        # Create a button for the sound
        button = customtkinter.CTkButton(sound_frame, width=100, text=sound_name, command=lambda file_path=dropped_file_path, volume_slider_index=i: play_sound(file_path, volume_slider_index))
        button.pack(padx=5, pady=5)
        volume_slider = customtkinter.CTkSlider(sound_frame, from_=0.0, to=1.0, width=100, orientation="horizontal")
        volume_slider.pack(padx=5, pady=(0, 5))
        volume_slider.set(1.00)
        volume_sliders.append(volume_slider)

        print("Sound name: " + sound_name)
        if mySoundBored.isDirty == False:
            mySoundBored.isDirty = True
            root.title(root.title() + "*")
            show_save_button()

        # create a file object to read the dropped file
        with open(dropped_file_path, 'rb') as file:
            # copy the file object to /tmp/
            with open('tmp/' + os.path.basename(dropped_file_path), 'wb') as new_file:
                shutil.copyfileobj(file, new_file)

# make root a drop target
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)


root.mainloop()

