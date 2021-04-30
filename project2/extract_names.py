
# Run it
# cd $PJ_HOME/redactor
# python extract_names.py

import io
import os
import sys
from os import listdir
from os.path import join

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import pos_tag
from nltk import ne_chunk

from collections import Counter # for counting occurrences of all elements in a list

nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('punkt')
nltk.download('words')

REVIEW_DIR = os.path.expandvars('$PJ_HOME/training')
NAME_PATH = os.path.expandvars('$PJ_HOME/extracted_names')
NAME_PATH2 = os.path.expandvars('$PJ_HOME/extracted_names_freq')

def get_entity(text):
    """Prints the entity inside of the text."""
    names = []
    # Extract names
    for sent in sent_tokenize(text):
        for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                if(len(chunk.leaves()) > 1):
                    names.append(' '.join(c[0] for c in chunk.leaves()))
    return names

def doextraction():
    """Get all the files from the review directory and pass them to the extractor."""
    names = []
    review_file_names = listdir(REVIEW_DIR)
    index = 0
    for review_file_name in review_file_names:
        print(f"{index}: extracting names from: {review_file_name}")
        index += 1
        review_path = join(REVIEW_DIR, review_file_name)
        review_file = open(review_path, "r")
        review_text = review_file.read()
        names.extend(get_entity(review_text))
    
    # Count number of occurrences for each name
    #counts = Counter(names)
    #counts = counts.items() # convert to list
    #counts = sorted(counts, key=lambda elem: elem[1], reverse=True)

    #print(counts)
    #print(type(counts))

    # Write non-unique names to file
    with open(NAME_PATH2, 'w') as name_file:    
        for item in names:                                             
            name_file.write(f"{item}\n")
    
    # Write unique names to file
    names = list(dict.fromkeys(names))
    names.sort()
    with open(NAME_PATH, 'w') as name_file:
        for name in names:
            name_file.write(f"{name}\n")

if __name__ == '__main__':
    doextraction()
