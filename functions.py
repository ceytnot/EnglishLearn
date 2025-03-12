import random
from datetime import datetime

import pyttsx3


"""VOICE for word"""
engine = pyttsx3.init() # object creation
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 110)

def get_dict():
    words_dict_origin = {}
    with open("dictionary.txt", "r", encoding="utf-8") as file:
        for line in file:
            words_dict_origin[line.strip().split('#')[0]] = line.strip().split('#')[1]
    return words_dict_origin


def get_random_words(words_dict: dict) -> str:
    """Returns random pair key and value from words dictionary"""
    return random.choice(list(words_dict.items()))

class GW():
    """For GLOBAL variables"""
    eng_word = ''
    rus_word = ''
    correct_counter = 0
    words_with_mistakes = set()
    output_file_name = datetime.now().strftime('%d%m%Y_%H%M%S')

def speak_word(word: str) -> None:
    """Speak word with Windows app if some voices are available"""
    try:
        engine.say(word)
        engine.runAndWait()
    except:
        pass
    
