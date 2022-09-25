import os

def extract_text(file):
    try:
        file = open(file, "r", encoding="utf-8").readlines()
    except Exception as e:
        file = str(e)
    return file

def format_text(text, list_of_removals=("(informal)", "(formal)", "\n")):
    # Removes things like (informal), (formal), \n, ; etc
    # Split answers from questions by double space instead of one
    full_text = []
    for line in text:
        for removal in list_of_removals:
            line = line.replace(removal, "")
        full_text.append(line.split("  "))
    print(full_text)
    return full_text
