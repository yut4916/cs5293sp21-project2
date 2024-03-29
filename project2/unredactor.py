# TO RUN: pipenv run python project2/unredactor.py -i "input/*.txt"

import os
from os import listdir
from os.path import join
from random import sample

import argparse # Function arguments
import glob # Reading in file names
import re

from collections import Counter # for counting occurrences of all elements in a list

# Define global variables
NAME_PATH = os.path.expandvars('$PJ_HOME/extracted_names')
FREQ_PATH = os.path.expandvars('$PJ_HOME/extracted_names_freq')
OUTPUT_DIR = './output/'

def main(docList):
    print("Initiating Project 2...")
    #print("Un-redacting the following documents:\n", docList)

    args = parser.parse_args()

    # --------------------------------------------
    # Training
    # Extract names from reviews. (See extract_names.py)

    # Convert names into entities and compute features for entities.
    print('\nTraining')
    training_entities_by_name = compute_training_entities_by_name()
    print(f"Training Entity Count: {len(training_entities_by_name)}")

    # --------------------------------------------
    # Predicting

    # Get redaction strings
    redactionsL = []
    for doc in docList:
        # Open ith file
        txt = open(doc, "r")
        txt = txt.read()
        redacted = re.findall(r'([█]+([ ][█]+)+)', txt)
        redacted = [tup[0] for tup in redacted] # Just get the first element of each tuple (The full redaction)
        #print(redacted)
        redactionsL.append(redacted)
    
    redactions = {}
    i = 0
    for tup in redactionsL:
        for block in tup:
            redactions[f'Unknown{i}'] = block
            i = i + 1

    print('\n')
    print('Predicting')
#    redactions = {
#        'Anthony Hopkins': '███████ ███████',
#        'Cuba Gooding Jr.': '████ ███████ ███',
#        'Denzel Washington': '██████ ██████████',
#        'Gabrielle Union': '█████████ █████',
#        'Meryl Streep': '█████ ██████ ',
#        'Robin Williams': '█████ ████████',
#    }

    for name, redaction in redactions.items():
        print("\n" + "-" * 33)
        print(f"Correct name: {name}")
        redacted_entities = [create_entity_from_name(redaction)]
        compute_entity_features(redacted_entities)
        for entity in redacted_entities:
            print(f"Target pattern: {entity['pattern']} {entity['name']}")
            matching_entities = find_matching_entities(training_entities_by_name, entity)
            n = len(matching_entities)
            print("There are", n, "total matching entities.\n")
            
            # Assign frequency
            for entity in matching_entities:
                assign_freq(entity)
            
            # Sort by most frequent
            matching_entities = sorted(matching_entities, key=lambda elem: elem["frequency"], reverse=True)
            
            # Write list of all matches to file
            with open(OUTPUT_DIR + name, "w") as output_file:
                output_file.writelines("%s\n" % line for line in matching_entities)
            output_file.close()

            # Just print the top 10 (unless there are <10 matches)
            if n < 10:
                n_top = n
            else:
                n_top = 10

            winners = matching_entities[:n_top]

            print("The", n_top, "most likely contenders are:")
            for match in winners: 
                print(match)
                #print(match['name'])
            
    print("\n" + "-" * 33)
    print(f"For full lists of matches, see output directory.")
    print("Project 2 unredaction process complete.")
    print("\n" + "-" * 33)

def compute_training_entities_by_name():
    training_entities_by_name = {}
    for name in get_names_from_file():
        review_entities = [create_entity_from_name(name)]
        compute_entity_features(review_entities)
        capture_entities(training_entities_by_name, review_entities)
    return training_entities_by_name

def get_names_from_file():
    names = []
    with open(NAME_PATH) as f:
        names = f.read().splitlines()
    return names

def create_entity_from_name(name):
    return {'name': name}

def compute_entity_features(entities): 
    for entity in entities:
        # Pattern for name lengths
        pattern = compute_name_pattern(entity['name'])
        entity['pattern'] = pattern

def compute_name_pattern(name):
    word_lengths = list(map(lambda element: str(len(element)), name.split()))
    pattern = '0'.join(word_lengths)
    return pattern

def capture_entities(entities_by_name, more_entities):
    for entity in more_entities:
        name = entity['name']
        if name not in entities_by_name:
            entities_by_name[name] = entity

def find_matching_entities(entities_by_name, target_entity):
    matching_entities = []
    for name, entity in entities_by_name.items():
        if(entity['pattern'] == target_entity['pattern']):
            matching_entities.append(entity)
    return matching_entities

def get_freq_from_file():
    names = []
    with open(FREQ_PATH) as f:
        names = f.read().splitlines()

    # Count number of occurrences for each name
    counts = Counter(names)
    counts = counts.items() # convert to list
    counts = sorted(counts, key=lambda elem: elem[1], reverse=True)

    # Convert from list to dictionary
    freq_dict = {elem[0] : elem[1] for elem in counts}
    return freq_dict

def assign_freq(entity):
    name = entity['name']
    freq_dict = get_freq_from_file()

    # Frequency of name in training dataset
    frequency = freq_dict[name] 
    entity['frequency'] = frequency


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

