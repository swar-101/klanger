
# Best practices 

- think in layers, then phases
- Observability first
- First make it correct, then make it fast, then make it fancy
- 

### How do we test against the auto-tagging our system does? 

A : 
- We do non-destructive evaluation 
- For each track we store 
  - Original metadata
  - Predicted metadata
  - Ground truth metadata
- Then we ask 
  - Did artist match 
  - Did title match 
  - Did album match

"Wrong tag is worse than missing tag."
"A DJ would rather see blank than wrong."
"No false positives."


For DJ-only tracks, unreleased stuff 
    --> do not auto apply 
    --> Surface in UI
    --> Let user input
    --> Mark as "user authoritative"


Over time 
These tracks become part of the system's knowledge base. 
This is how the system will learn without hallucinating. 


# v0 architecture refinement 

Fingerprint --> Candidate Resolver --> Confidence Scorer 

- Library stores 
  - audio file references
  - metadata layers 
  - confidence
  - source

- UI shows 
  - green auto applied
  - yellow suggested 
  - red needs input 

No magic... just honesty.


- Filename and metadata 
  - Not just text; human compressed intent
  - Example: 
    - `Daft Punk - Harder Better Faster Stronger (Live Edit).mp3`
  - From this **alone** you get probabilistic hints 
    - Artist tokens 
    - Title tokens
    - Version info 
    - Confidence clues 
  
  - This info could be messy, but predictable, if not wrong. 


# Thinking in stages, not features

Stage 1 
- Text based inference
- Filename parsing 
- Existing tag normalization 
- Heuristics + regex + vocab 

Stage 2
Cross check with third pary metadata 
- Does candidate exist?
- Do tokens align? 
- Do durations match? 

Stage 3 
Audio fingerprint only if ambiguity remains 

Cheap --> expensive --> expensive emotionally 


## What is a fingerprint? 

A fingerprint is a compact, noise resistant signature of audio. 
- Not the whole song
- Not waveform 
- Not MP3 bits 

Just --> "these frequency peaks happened at these relative times"


Even if 
  volume changes 
  compression changes 
  background noise exists

  It still matches. 
  

## Why fingerprints are perfect? 

- Because we don't want opinions. 
- We want identity verification 

Fingerprint answers 
  - "Is this that song?"

Not 
"What genre is this?"
"What vibe is this?"

Just identity. 


## We text guess who it might be, Fingerprint confirms who it is, if not unknown. 

## Where fingerprints fail 
- They don't help with 
  - Unreleased tracks
  - DJ edits 
  - Like mashups 
  - Stems
  - Bootlegs 

For these user input becomes the authoritative truth. 



## Think in layers

Things I already have

### Layer 1. Signals
filename 
existing metadata
duration 
bitrate 

### Layer 2. Hypothesis

"What could this track be?"
Generated from text parsing 
Maybe multiple candidates 
Each with weak scores
No truth claims yet. 


### Layer 3. Evidence

Cross checks
Duration match
Token overlap 
Later fingerprint match 

This strengthens or weakens hypotheses. 

Currently we need a **confidence score**, not a matrix. 

Example: 
  Filename contains artist name -> +0.3
  Title token overlap -> +0.2
  Duration within 2 sec -> +0.2
  Fingerprint mathc -> +0.8

  Clamp at 1.0
  Set thresholds. 

Linear scoring. Old school. Reliable. Explainable.



## Lightweight Inference

Lightweight inference is not "decide the correct tags"

It is "general plausible guesses + explain why"

So the output of inference is 
enriched data, not mutated data. 

Think annotate, not overwrite. 

for v0, let's infer 

Artist
Title 

Ignore album, year, genre, etc. 

Less surface area = fewer bugs = more trust

Step 1: define what we infer (limit scope)

Step 2: inputs to inference 

Step 3: 
  Rule 1: Token overlap check 
      Simple, powerful 
      - take metadata 
      - split them into lower case tokens
      - count overlap 
      - scoring idea
          O overlaps - confidence 0
          1 token overlap - confidence .4
          full overlap - confidence .7
      - this tells us "metadata agrees with filename" or not
  
Step 4: 
  Rule 2: Positional heuristics 

  Rules 
  Early tokens are more likely artist
  Middle tokens are likely the title 
  Parentheses usually version info, remixes, remastered, etc. 
  
  Example: 
    daft punk - harder better faster stronger (live edit)
  
    inference: Artist candidate - first 1-2 tokens 
    title candidates: tokens until (

  "This gives us a fallback when metadata is missing."
  
Step 5. Generate hypotheses, not answers 
  Instead of `artist = "Daft Punk"` 
  We produce
  `artist_candidate = DaftPunk, confidence 0.7, source filename+metadata`
  Basically we store why. 


Step 6. Extend the data structure 
  Extractor output becomes enriched, not replaced. 
  Conceptually:

```json
{
  "filename": "...",
  "tokens": [...],
  "tags": {...},
  "inference": {
    "artist": {
      "value": "Daft Punk",
      "confidence": 0.7,
      "source": "filename+metadata"
    },
    "title": {
      "value": "Harder Better Faster Stronger",
      "confidence": 0.6,
      "source": "filename"
    }
  }
}
```

Nothing applied yet. 
Nothing destructive. 

This is why our system will be trustworthy. 

Step 7: No thresholds yet

Important discipline 

Do not decide 
"if confidence > X, apply"

Right now we just 
  - Observe 
  - Compare 
  - Learn patterns

Thresholds come after you've seen failures. 


Simply put 
  Extractor sees. 
  Inference reasons. 

Seperation = sanity 

