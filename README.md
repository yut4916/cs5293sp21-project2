# Project 2 - The Unredactor
Written by Katy Yut  
April 24, 2021

## How to Install and Use This Package

### Virtual Environment

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


## Assumptions/Simplifications
* Names are in the format FirstName LastName, with a space separating two blocks of redaction characters, each the same length as the corresponding name. 
* Input files will be in .txt format
* Only use a small subset of the IMDB dataset
* Start simple (just length of names/position of spaces) and build from there

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
 
# Citations
Throughout the project my dad, Greg Yut, helped me understand the nuts and bolts, presumably all the stuff I should've known prior to taking this class but didn't learn because I'm not a C S student (i.e. Linux syntax/quirks, troubleshooting tips, etc).

While troubleshooting, I used the following resources:
* []()
