# Sound Bored
Sound Bored is a fully customizable sound board for streamers, pranksters, and goofballs alike.  Built with Python, this application lets users play various sound effects, customize settings, and utilize Google's text to speech (via gtts) to turn text prompts into robot speak.

## Features

- **Play Sound Effects**: Click buttons to play different sounds from a customizable list.
- **Drag-and-Drop Sound Files**: Easily add new sound files by dragging and dropping them into the application.
- **Customizable Settings**: Adjust master volume, individual sound volumes, and more.
- **Text-to-Speech**: Input text and hear it spoken in different accents.
- **Dynamic Interface**: Move around the sound buttons and resize the window as you like.
- **Save Your Settings**: Save your configurations and sound additions seamlessly.

## Installation

To get started with Sound Bored, follow these steps:

1.  **Install Python**: Ensure you have Python 3.11 installed on your system. If you do not have Python installed or have an older version, download and install it from the [official Python website](https://www.python.org/downloads/).

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ParkerTonra/SoundBored.git
   cd soundbored
2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
3. **Run the application:**
    ```bash
        python soundbored.py
## Usage

Upon launching the Sound Bored, you will see a grid of sound buttons each associated with a sound file. Below are some functionalities you can use:

- **Playing Sounds:** Click any button to play the associated sound.
    - Enable **Retrigger** to prevent sounds from overlapping.
- **Adjusting Volume:** Use the slider below each button to adjust the sound's volume.
- **Adding Sounds:** Drag and drop .wav or .mp3 files onto the app to add them to your soundboard.
- **Using Text-to-Speech:** Click the "Robot Speak" button, type your text, and select an accent for the application to speak back to you.
- **Accessing Settings:** Click the "Settings" button to open the settings window where you can adjust the master volume. (work in progress)

## Customization

Modify config.json in the default_settings directory to add or change the preloaded sound files and settings. Here's an example of what the configuration might look like, with "new_sound.mp3" being a new sound placed in the 'sounds' folder:

    {
        "sounds": ["AIRHORN.wav", "laugh.mp3", "new_sound.mp3"]
    }

## Contributing

Contributions to Dreaddy Bear's Sound Bored are welcome! Here are a few ways you can help:
- Report Bugs
- Suggest New Features
- Improve the Documentation
- Submit Pull Requests

Thanks for checking out my repo! I hope you have some fun with Sound Bored! :)
