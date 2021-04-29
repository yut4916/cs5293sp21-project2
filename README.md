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
		+ Grab small subset of imdb dataset
2. Now that I'm all set up and have a manageable dataset, I can start writing a simple framework. 
	* I've pasted the code from the class lecture, so I'm also trying to incorporate some of that.

# Citations
Throughout the project my dad, Greg Yut, helped me understand the nuts and bolts, presumably all the stuff I should've known prior to taking this class but didn't learn because I'm not a C S student (i.e. Linux syntax/quirks, troubleshooting tips, etc).

While troubleshooting, I used the following resources:
* []()
