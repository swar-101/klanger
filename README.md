
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



