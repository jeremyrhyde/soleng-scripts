import os
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Argument parser")
    parser.add_argument('-msg', "--message", default='', help='Type in a string to be played')
    parser.add_argument('-file', "--file", default='', help='Type in a path to a file to be played')

    return parser.parse_args()

def main():
    if args.message != "" :
        say_command = "say " + args.message
        os.system(say_command)

    if args.file != "":
        play_file_command = "afplay " + args.file
        os.system(play_file_command)

if __name__ == '__main__':
    args = parse_arguments()
    main()