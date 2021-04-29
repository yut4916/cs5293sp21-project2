# TO RUN: 

import argparse # Function arguments
import glob # Reading in file names
import re
import spacy
import sklearn

from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.model_selection import cross_val_score

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

