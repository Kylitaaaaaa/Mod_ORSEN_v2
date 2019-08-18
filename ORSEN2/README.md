# ORSEN_Processor
The python code for the input processing / output generator for ORSEN (Oral Storytelling Entitiy)

## Dependencies
- PyMySQL
- spaCy
- neural Coref ( https://github.com/huggingface/neuralcoref ) V 0.2
  - Changes
    - data.py : line 338 
        ```
        with open(name + "_vocabulary.txt", encoding="utf8") as f:
        ```
    - algorithm.py : after line 331
        ```
        \
        mention.mention_type == MENTION_TYPE["LIST"]: #EDITED: added List to show They/Them pronouns
        ```
- Flask
- inflect

## Modules
- Text Understanding
  - Preprocessing
  - Character/Object Extraction
  - Character/Object Attribute Extraction 
  - Setting Detail Extraction
  - Event Extraction
  
- Dialogue Manager
  - Dialogue Planner
  - Content Determination
  - Sentence Planning
  - Linguistic Realization

- Story Generation
