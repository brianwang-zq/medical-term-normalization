# Medical Term Normalization

Python pipeline for medical term normalization in patient notes.
Utilizes the UMLS-api developed by Richard Odwyer at https://github.com/odwyersoftware/umls-api/blob/master/README.md/ 

## Installation

Just download the file and run it in terminal.

## Example Usage

```bash
/usr/local/bin/python3 medical_term_normalization.py "PATH" "MEDICAL TERM"
```
Replace the text in quotes with the actual PATH and term to normalize.

## Test

```bash
pip install -r requirements-dev.txt
pytest src/tests
flake8
```
