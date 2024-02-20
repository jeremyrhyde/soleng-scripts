import os
import time
import argparse
from pygame import mixer
from gtts import gTTS
from io import BytesIO

def parse_arguments():
    parser = argparse.ArgumentParser(description="Argument parser")
    parser.add_argument('-msg', "--message", default='', help='Type in a string to be played')
    parser.add_argument('-file', "--file", default='', help='Type in a path to a file to be played')

    return parser.parse_args()

def main():

    mixer.init()
    mixer.music.set_volume(1.0)

    if args.message != "" :
        # Create audio buffer
        tts = gTTS(text=args.message, lang='en')
        mp3 = BytesIO()
        tts.write_to_fp(mp3)
        mp3.seek(0)

        # Play message
        print("Playing message \'" + args.message + "\'")
        mixer.music.load(mp3)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(1)    


    if args.file != "":
        # Play file
        print("Playing " + args.file)
        mixer.music.load(args.file)
        mixer.music.play()

    # Wait for audio to complete
    while mixer.music.get_busy():
        time.sleep(1)     

if __name__ == '__main__':
    args = parse_arguments()
    main()