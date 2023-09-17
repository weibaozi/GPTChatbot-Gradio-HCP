import json
import os
def are_strings_similar(s1, s2):
    # Convert both strings to lowercase for case-insensitive comparison
    if not (isinstance(s1, str) and isinstance(s2, str)):
        return False
    s1 = s1.lower()
    s2 = s2.lower()

    # If the strings are exactly the same, return True
    if s1 == s2:
        return True

    # If the lengths of the strings differ by more than 1, return False
    if abs(len(s1) - len(s2)) > 1:
        return False

    # Find the index of the first mismatched character
    idx = 0
    while idx < min(len(s1), len(s2)) and s1[idx] == s2[idx]:
        idx += 1

    # Check if the strings are similar with a one-letter mistake
    return s1[idx + 1:] == s2[idx:] or s1[idx:] == s2[idx + 1:]

def list_to_string(l):
    #type check
    if not isinstance(l,list):
        return "Error: input is not a list"
    s = ""
    for i in l:
        s+=i+","
    return s[:-1]

def format_json(json_data, indent=0,persona={}):
    #assert isinstance(json_data, (dict, list))
    formatted_str = ""
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            for p in persona:
                if are_strings_similar(p,key):
                    print("found key",key)
                    persona[p]=value
            formatted_str += "\n"+" "* indent + f"{key}:"
            formatted_str += format_json(value, indent + 2,persona=persona)
    elif isinstance(json_data, list):
        for item in json_data:
            formatted_str += "" * indent
            formatted_str += format_json(item, indent + 2,persona=persona)
    else:
        formatted_str += " " * indent + str(json_data) + ""
    return formatted_str

def get_tones():
    #search all tones txt file in folder tones, make a dictionary of tone name and the tone content
    tones = {}
    for filename in os.listdir("tones"):
        if filename.endswith(".txt"):
            with open("tones/"+filename) as f:
                tones[filename[:-4]] = f.read()
    return tones
