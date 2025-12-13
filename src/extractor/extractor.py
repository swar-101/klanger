import os.path
import re
import json

# read each file
# split on -, _, (, ), [, ]
# store token as a list
# create a simple JSON per file

DATA_DIR = r"D:\personal\projects\klanger\data\klanger-v0.0-test-data"
OUTPUT_DIR = "..\..\outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "observations.json")

filename = "Daft Punk - Harder Better Faster Stronger (Live Edit).mp3"

def extract(filename):
    print("Reading file: ", filename)

    # remove extension
    name, _ = os.path.splitext(filename)
    # lowercase so that there's less entropy
    name = name.lower()

    # tokenize file data
    tokens = re.split(r"[-_()\[\]]+", name)
    tokens = [t.strip() for token in tokens for t in token.split()]
    tokens = [t for t in tokens if t]

    data = {
        "filename" : filename,
        "tokens": tokens,
        "tags": {
            "artist": None,
            "title": None,
            "album": None
        }
    }
    return data


def run():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    observations = []

    for file in os.listdir(DATA_DIR):
        if not file.lower().endswith((".mp3", ".wav", ".flac", ".m4a")):
            continue

        data = extract(file)
        observations.append(data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(observations, f, indent=2)
    print(f"\nWrote {len(observations)} observations to {OUTPUT_FILE}")
   
   
if __name__ == "__main__":
          run()
   
    
"""
expected : 
{
  "filename": "Daft Punk - Harder Better Faster Stronger (Live Edit).mp3",
  "tokens": ["daft", "punk", "harder", "better", "faster", "stronger", "live", "edit"],
  "tags": {
    "artist": "Daft Punk",
    "title": "HBFS",
    "album": ""
  }
}

"""
"""
later when auto tagging fails
we'll know why

- Bad tokenization
- Missing artist
- Ambiguous remix name, etc.
"""