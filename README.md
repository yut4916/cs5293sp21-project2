# Project 2 - The Unredactor
Written by Katy Yut  
April 24, 2021

## How to Install and Use This Package

The steps below will set the environment variable, run the training steps, and unredact names.


### Virtual Environment Setup

#### Install and set Python 3.8.6

    pyenv install 3.8.6
    pyenv local 3.8.6

#### Create virtual environment

    python -m venv ~/.virtualenvs/project2
    (env is at ~/.virtualenvs/project2)

#### Activate virtual environment

    source ~/.virtualenvs/project2/bin/activate

#### Deactivate virtual environment

    deactivate

### Install packages one-by-one (or just install requirements.txt below)

    python -m pip install argparse
    python -m pip install glob2
    python -m pip install nltk
    python -m pip install pandas
    python -m pip install pytest
    python -m pip install regex
    python -m pip install setuptools wheel
    python -m pip install spacy

#### Capture all of the required packages in requirements.txt

    python -m pip freeze > requirements.txt

#### Install all packages in requirements.txt

    python -m pip install -r requirements.txt

---

Set `PJ_HOME` to the location of the project directory.

    export PJ_HOME=~/projects/cs5293sp21-project2 (or wherever the project is)

### Training

    cd $PJ_HOME/project2
    python extract_names.py

---

### Unredact a Review

- Given a redacted review, unredact using name features, etc.
- Print redaction pattern and name options in output directory.

    cd $PJ_HOME
    pipenv run python project2/unredactor.py -i "input/*.txt"

---

### Testing
lol you can run the tests all you want, but I didn't actually write any. I tend to do my testing in my main.py file as I go. Something to work on if I ever decide to be a programmer and write code for realsies. 

    # Run pytest
    cd $PJ_HOME/tests
    pytest

Some testing that I did that's now obsolete was manually create redacted reviews for six actors I picked arbitrarily. Now my code reads text files of reviews that I redacted, but here's what it looked like before: 
 
Redacted character is (█). (See $PJ_HOME/redacted_reviews.)

    cd $PJ_HOME/aclImdb/train/unsup
    grep -rwl . -e 'Anthony Hopkins'

Redacted Actors
  - Anthony Hopkins
  - Cuba Gooding Jr.
  - Denzel Washington
  - Gabrielle Union
  - Meryl Streep
  - Robin Williams

---

## Assumptions/Simplifications
* Names are in the format FirstName LastName, with a space separating two blocks of redaction characters, each the same length as the corresponding name. 
* Input files will be in .txt format
* Only use a small subset of the IMDB dataset
* Start simple (just length of names/position of spaces) and build from there
* One major limitation, of course, is that we're relying on spacy's named entity recognition tool to locate names.

---

## Function Descriptions

### compute_training_entities_by_name()

### get_names_from_file()

Extracts all names from the extracted_names file, which contains all names in the training dataset. 

### create_entity_from_name(name)

Takes a string (name) and creates an entity named "name" in the format: {'name': name}

### compute_entity_features(entities)


### compute_name_pattern(name)


### find_matching_entities(entities_by_name, target_entity)


### capture_entities(entities_by_name, more_entities)

lol sorry you'll just have to figure it out. they do stuff to make the function work

---

## Approach/Steps/Inner Monologue/Project Diary
1. Got my files/folder structure/git repo all set up.
	* Gameplan:
		+ Use the length of the redaction as a pattern for name length
		+ Generate a list of possible matches
		+ Add various features to enhance model accuracy
	* Available tools/resources:
		+ sklearn DictVectorizer
		+ bag of words
		+ training/testing - ML
		+ sentiment/related words/similarity
	* Setup to-dos:
		+ Edit proj1 name redactor (preserve space)
		+ Watch lectures/videos on Canvas
		+ Grab small subset of imdb dataset (13,000 instead of 100,000)
2. Now that I'm all set up and have a manageable dataset, I can start writing a simple framework. 
	* I've pasted the code from the class lecture, so I'm also trying to incorporate some of that.
	* Using the code provided in the proj2 outline, I scraped all of the names from my mini sample of movie reviews. This will be my bank of all possible actor names
3. I've written a function (compute_name_pattern) that takes a name string and computes its "pattern", which will be a string of numbers indicating the lengths of the name components. 
	* For example, if the name is Meryl Streep, the function will return the pattern string 506, because "Meryl" is 5 characters long and "Streep" is 6 characters long, separated by a space (0). This pattern will be computed on all of the names and used as the primary rule for generating potential matches
	* Note: some patterns are more unique than others--Cuba Gooding Jr., for instance, is a 40703 pattern, which is much less common than other patterns, such as 508 (Robin Williams, among many others)
4. Okay, I've got a basic functioning un-redactor, but some names still return way too many options (Meryl Streep matches 170 other names). Some tweaks to make:
	* Rank possible matches by popularity instead of alphabetically so that we're picking the most likely actors
	* Incoporate gender? Would need to use surrounding text (not just the name itself), but this should definitely be possible, especially using the sentence diagram--it should be able to link pronouns with their associated nouns. Not sure how to go about this though, so probably out of the scope of this project.
	* Also, currently just hardcoding the redacted examples into my function, instead of taking input files and reading through them to find unredacted portions. That could definitely be changed
5. Adding frequency -- I tweaked the extraction code provided in the project outline so that it generates two files: one that has just a list of all unique names (extracted_names) and another that has each unique name and its total number of occurrences. This will let me use frequency as an additional feature, so I can select the names that occur more often.
	* Okay I ended up tweaking my frequency code so that the second file is non-unique names and their total number of occurrences aren't computed until the main.py function is run--I was having formatting issues. 
6. Starting to come together! Is my code a mess? Yes. Is my readme sparse? Also yes. But the damn thing works decently!
	* Still haven't added code to read through input files
	* Just did it! Wasn't even too hard. Just a couple loops and a simple regex (r'([█]+[ ][█]+)+')
7. Okay, well, my documentation is spotty at best, but I'm gonna call this finished. Good enough!

# Citations
Throughout the project my dad, Greg Yut, helped me understand the nuts and bolts, presumably all the stuff I should've known prior to taking this class but didn't learn because I'm not a C S student (i.e. Linux syntax/quirks, troubleshooting tips, etc).

While troubleshooting, I used the following resources:
* [How to convert Python Dictionary to a list?](https://www.tutorialspoint.com/How-to-convert-Python-Dictionary-to-a-list)
* [sklearn.model_selection.train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)
* [Wihat's a quick way to comment/uncomment lines in Vim?](https://stackoverflow.com/questions/1676632/whats-a-quick-way-to-comment-uncomment-lines-in-vim)
	+ Use Shift+V to start visual block mode, select the lines you want to comment out, then type : s/^/# and hit Enter
* [How can I count the occurrences of a list item?](https://stackoverflow.com/questions/2600191/how-can-i-count-the-occurrences-of-a-list-item)
* [How to Convert Nested List into dictionary in Python where lst[0][0] is the key](https://stackoverflow.com/questions/16359052/how-to-convert-nested-list-into-dictionary-in-python-where-lst00-is-the-key)
* [collections — Container datatypes](https://docs.python.org/3/library/collections.html#collections.Counter)
* [Sorting HOW TO](https://docs.python.org/3/howto/sorting.html)
* [re — Regular expression operations](https://docs.python.org/3/library/re.html)
* [How to get the first element of each tuple in a list in Python](https://www.kite.com/python/answers/how-to-get-the-first-element-of-each-tuple-in-a-list-in-python)
* [Python Dictionary Append: How to Add Key/Value Pair](https://www.guru99.com/python-dictionary-append.html)
* [Python Convert List to Dictionary: A Complete Guide](https://careerkarma.com/blog/python-convert-list-to-dictionary/)
* [Reading and Writing Lists to a File in Python](https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/)

