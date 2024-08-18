# Medical Term Normalization

Python pipeline for medical term normalization in patient notes.
Utilizes the UMLS-api developed by Richard Odwyer at https://github.com/odwyersoftware/umls-api/blob/master/README.md/ 

## Installation

Download the folder.

## Example Usage

Add a text file to the downloaded folder with the text you want to normalize.
```bash
$ /usr/local/bin/python3 medical_term_normalization.py "UMLS API KEY" "PATH OF TEXT TO NORMALIZE" "MEDICAL TERM"
```
Set the directory of the console to the PATH of the downloaded folder. Replace the text in quotes with the actual PATH and term to normalize.

Paste in the UMLS API key into the first argument.

You can apply for a UMLS API key at this link: https://uts.nlm.nih.gov/uts/login

It takes approximately 1-2 business to acquire one.

## Test Usage
```bash
$ /usr/local/bin/python3 medical_term_normalization.py "sample_text.txt" "weight loss"
admission:        i/o:  no intake or output data in the 24 hours ending 1/1/2035 1400      physical exam:  gen: elderly woman, some normalized weight loss, nad, pleasant, speaks tigrinya  heent: perrl, no lad, mmm  cv: nl s1 and s2, rrr, no m/r/g  pulm: ctab, no wheezes, rales or ronchi. breathing comfortably on room air.   gi: soft, nt, nd, +bs. no guarding or rebound tenderness.   ext: no peripheral edema, wwp  neuro: a&o x 3, eom intact, face symmetric     labs/data:   bmp        1/1/2035  1433 
```

## Python Package Dependencies

The following packages need to be pip installed in order to ensure the pipeline functions.
```bash
$ pip3 install nltk
$ pip3 install requests
$ pip3 install nltk
$ pip3 install argparse
$ pip3 install numpy
$ pip3 install umls-api
$ pip3 install spacy
```
