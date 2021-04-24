# TO RUN: 

import argparse # Function arguments
import glob # Reading in file names
import re
import spacy

nlp = spacy.load("en_core_web_sm")

def main(docList):
    print("Initiating Project 2...")
    print("Un-redacting the following documents:\n", docList)

    args = parser.parse_args()

if __name__ == '__main__':
    projURL = "https://github.com/yut4916/cs5293sp21-project2.git"

    # Set up argument parsing
    epilog = "\nFor full information, see:\n" + projURL
    parser = argparse.ArgumentParser(epilog=epilog)
             
    # Set up arguments
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="Glob for valid text file(s)")

    args = parser.parse_args()
    if args.input:
        docList = glob.glob(args.input)
        main(docList)
