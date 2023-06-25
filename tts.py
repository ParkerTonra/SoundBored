import subprocess

def execute_command(inputcommand):
    process = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
    output, err = process.communicate()
    return output

def text_to_speech(text):
    # tts using espeak
    command = f'espeak -ven+f3 -k5 -s150 "{text}"'
    execute_command(command)

# example usage
text_to_speech("Hello, this is a test.")