# TO RUN: 

import os
from os import listdir
from os.path import join
from random import sample

import argparse # Function arguments
import glob # Reading in file names
import re
import spacy
#import sklearn

from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.model_selection import cross_val_score

# Define global variables
nlp = spacy.load("en_core_web_sm")
NAME_PATH = os.path.expandvars('$PJ_HOME/extracted_names')
OUTPUT_DIR = './output'
REDACTED_REVIEW_DIR = './p2/redacted_reviews'

def main(): #docList
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
    print('\n')
    print('Predicting')
    redactions = {
        'Anthony Hopkins': '███████ ███████',
        'Cuba Gooding Jr.': '████ ███████ ███',
        'Denzel Washington': '██████ ██████████',
        'Gabrielle Union': '█████████ █████',
        'Meryl Streep': '█████ ██████ ',
        'Robin Williams': '█████ ████████',
    }

    # redactions = [anthony_hopkins, cuba_gooding_jr, denzel_washington, gabrielle_union, robin_williams]
    for name, redaction in redactions.items():
        print("\n" + "-" * 33)
        print(f"Name: {name}")
        redacted_entities = [create_entity_from_name(redaction)]
        compute_entity_features(redacted_entities)
        for entity in redacted_entities:
            print(f"target_entity: {entity}")
            matching_entities = find_matching_entities(training_entities_by_name, entity)
            print(f"matching_entities: {matching_entities}")

    # Predicting
    # print('\n')
    # print('Predicting')
    # redacted_reviews = listdir(REDACTED_REVIEW_DIR)
    # for review in redacted_reviews:
    #     review_path = join(REDACTED_REVIEW_DIR, review)
    #     review_file = open(review_path, "r")
    #     review_text = review_file.read()
    #     redacted_entities = extract_redacted_entities(review_text)
    #     compute_entity_features(redacted_entities)
    #     for entity in redacted_entities:
    #         print("\n" + "-" * 33)
    #         print(f"target_entity: {entity}")
    #         matching_entities = find_matching_entities(training_entities_by_name, entity)
    #         print(f"matching_entities: {matching_entities}")


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



if __name__ == '__main__':
    projURL = "https://github.com/yut4916/cs5293sp21-project2.git"

    # Set up argument parsing
    epilog = "\nFor full information, see:\n" + projURL
    parser = argparse.ArgumentParser(epilog=epilog)
             
    # Set up arguments
    parser.add_argument("-i", "--input", type=str, required=False,
                        help="Glob for valid text file(s)")

#    args = parser.parse_args()
#    if args.input:
#        docList = glob.glob(args.input)
#        main(docList)

    main()

# =========== FROM CLASS =======================================================

def make_features(sentence, ne="PERSON"):    
    doc = nlp(sentence)    
    D = []    
    for e in doc.ents:        
        if e.label_ == ne:            
            d = {}            
            # d["name"] = e.text # We want to predict this            
            d["length"] = len(e.text)            
            d["word_idx"] = e.start            
            d["char_idx"] = e.start_char            
            d["spaces"] = 1 if " " in e.text else 0            
            # gender?            
            # Number of occurences?
            D.append((d, e.text))    
    return D


def main2():
    # print(len(sample))
    features = []
    for s in sample:
        features.extend(make_features(s))
    
    # print(features)
    v = DictVectorizer(sparse=False)
    train_X = v.fit_transform([x for (x,y) in features[:-1]])
    train_y = [y for (x,y) in features[:-1]]
    test_X = v.fit_transform([x for (x,y) in features[-1:]])
    test_y = [y for (x,y) in features[-1:]]
    #clf = DecisionTreeClassifier(criterion="entropy")
    clf = KNeighborsClassifier(n_neighbors=3)
    clf.fit(train_X, train_y)
    print("Decison Tree: ", clf.predict(test_X), clf.predict_proba(test_X), test_y)
    print("Cross Val Score: ", cross_val_score(clf, v.fit_transform([x for (x,y) in features]), [y for (x,y) in features], cv=2))

