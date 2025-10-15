import random
from datetime import datetime
import ctypes
import pyttsx3
import winsound
import threading
import ctypes.wintypes


"""VOICE for word"""
def init_speech_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 90)

    return engine

def get_dict() -> dict:
    """Return 2 dicts - second with reverse words"""
    words_dict_origin = {}
    words_dict_reverse = {}
    with open("dictionary.txt", "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            words_dict_origin[i] = (set([x.strip().lower().replace('  ', ' ') for x in line.strip().split('#')[0].split(',') if x]), 
                                    set([x.strip().lower().replace('  ', ' ') for x in line.strip().split('#')[1].split(',') if x]))
            
            words_dict_reverse[i] = (set([x.strip().lower().replace('  ', ' ') for x in line.strip().split('#')[1].split(',') if x]), 
                                     set([x.strip().lower().replace('  ', ' ') for x in line.strip().split('#')[0].split(',') if x]))
    
    return words_dict_origin, words_dict_reverse


def get_random_words(words_dict: dict) -> str:
    """Returns random pair key and value from words dictionary"""
    random_choice = random.choice(list(words_dict.items()))
    return random_choice[0], random_choice[1][0], (random_choice[1][1])


class GW():
    """For GLOBAL variables"""
    id = ''
    eng_word = ''
    rus_word = ''
    word_to_speak = ''
    second_pass_check = False
    words_with_mistakes = set()
    output_file_name = datetime.now().strftime('%d%m%Y_%H%M%S')
    total_words = 0
    position_count = 0
    upst_current = 0
    upst_limit_for_circle = 1

def speak_word(word):
    """Speak word with Windows app if some voices are available""" 

    if isinstance(word, set):
        word = ' '.join(word)

    def run_speech():
        try:
            engine = init_speech_engine()
            engine.say(word)
            engine.runAndWait()
            engine.stop()
        except RuntimeError:
            pass


    thread = threading.Thread(target=run_speech)
    thread.daemon = True
    thread.start()
    
    

def switch_keyboard_layout():
    """Swith to next keyboard layout: eng -> rus"""
    ctypes.windll.user32.PostMessageW(0xFFFF, 0x0050, 0, 0)

def async_beep(frequency=300, duration=800):
    thread = threading.Thread(target=winsound.Beep, args=(frequency, duration))
    thread.daemon = True
    thread.start()


def keyboard_layout():
    """Check code of current layout"""

    languages = {
        0x409: "Английский",
        0x419: "Русский"
    }

    try:
        # get active window
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        # get ID of window
        thread_id = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, 0)
        # get layout
        layout_id = ctypes.windll.user32.GetKeyboardLayout(thread_id)
        
        # beleive me this is necessary
        lang_id = layout_id & 0xFFFF
        
        return languages[lang_id]
    
    except Exception as e:
        return e


    
