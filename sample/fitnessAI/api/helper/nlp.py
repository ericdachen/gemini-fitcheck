import nltk
from nltk.corpus import wordnet as wn

# Ensure that relevant nltk resources are downloaded
nltk.download('wordnet')

def find_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

def map_body_parts(input_parts, body_parts_dict):
    # Create a dictionary to hold the mapping of body parts to their synonyms
    body_parts_synonyms = {key: set() for key in body_parts_dict.keys()}
    for key, parts in body_parts_dict.items():
        for part in parts:
            # Add direct synonyms
            body_parts_synonyms[key].update(find_synonyms(part))

    output_keys = set()
    for input_part in input_parts:
        input_synonyms = find_synonyms(input_part)
        for key, synonyms in body_parts_synonyms.items():
            # Check if any input synonym matches the dictionary synonyms
            if input_synonyms.intersection(synonyms):
                output_keys.add(key)

    return list(output_keys)

# # Dictionary mapping
# body_parts = {
#     'shoulders': ['shoulders'],
#     'elbows': ['elbows'],
#     'wrists': ['wrists'],
#     'hips': ['hips'],
#     'knees': ['knees'],
#     'ankles': ['ankles'], 
#     'feet': ['feet'],
#     'body': ['shoulders', 'hips'],
#     'back': ['shoulders', 'hips'],
#     'legs': ['hips', 'knees', 'ankles'],
#     'calves': ['knees', 'ankles'],
#     'arms': ['shoulders', 'elbows', 'wrists']
# }

# # Example input
# input_parts = ['lower back', 'hips']
# output_keys = map_body_parts(input_parts, body_parts)
# print("Output keys:", output_keys)
