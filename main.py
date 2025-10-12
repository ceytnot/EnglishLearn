# C:\Users\NewHorizon\Documents\PythonProjects\EnglishLearn\venv\Scripts\Activate.ps1
# pip freeze > requirements.txt
from tkinter import *
from tkinter import ttk
from functions import get_random_words, GW, get_dict, speak_word, switch_keyboard_layout, async_beep, keyboard_layout
from datetime import datetime
from time import sleep
import random
import winsound


def update_progress(left_words):
    progress['value'] = (left_words / GW.total_words) * 100

def start_choice_game() -> None:
    frames_to_hide = [frame_1_1, frame_2_1, frame_3, frame_4]
    
    for frame in frames_to_hide:
        frame.pack_forget()

def start_game() -> None:
    GW.output_file_name = datetime.now().strftime('%d%m%Y_%H%M%S')
    global words_dict
    global words_dict_reverse 
    GW.second_pass_check = False
    words_dict, words_dict_reverse = get_dict()
    GW.id, GW.eng_word, GW.rus_word = get_random_words(words_dict) 
    GW.word_to_speak = random.choice(list(GW.rus_word))
    label_eng_word['text'] = GW.word_to_speak
    great_lbl['text'] = ''
    label_counter['text'] = len(words_dict) + len(words_dict_reverse)
    GW.total_words = len(words_dict) + len(words_dict_reverse)
    input_field.focus()
    GW.words_with_mistakes = set()
    submit_btn["state"] = "normal"
    input_field["state"] = "normal"
    input_field.insert(0, f"{'_' * len(list(GW.eng_word)[0])}")
    #input_field.icursor(0)
    finish_game_lbl['text'] = ''
    update_progress(GW.total_words)
    key_layout['text'] = f"{keyboard_layout()}"


# functions
def click_submit_button(event=None):
    global words_dict
    input_word = input_field.get().strip().lower().replace('  ', ' ').replace("_", "")
    if input_word:  # if something is typed
        if input_word in GW.eng_word:     

            del words_dict[GW.id]
            
            submit_btn["state"] = "enabled"
            input_field["state"] = "enabled"
            voice_btn["state"] = "enabled"
            advise_btn["state"] = "enabled"
            great_lbl['text'] = "МОЛОДЕЦ! Идем дальше!"
            winsound.PlaySound("MailBeep", winsound.SND_ALIAS | winsound.SND_ASYNC)
            sleep(0.5)
            
        else:
            great_lbl['text'] = "НЕПРАВИЛЬНО"
            async_beep()
            sleep(0.5)
            GW.words_with_mistakes.add(GW.word_to_speak)

        with open(f"Output_{GW.output_file_name}.txt", "a") as text_file:
                text_file.write(f'{GW.eng_word} - {input_word}\n')

        label_prev_world['text'] = f'Искомое слово:\n   {GW.word_to_speak}'
        label_prev_answer['text'] = f'Написанное слово:\n   {input_word}'

        label_counter['text'] = len(words_dict) + len(words_dict_reverse)
        
        update_progress(left_words = len(words_dict) + len(words_dict_reverse))
        

        try:
            GW.id, GW.eng_word, GW.rus_word = get_random_words(words_dict)            
        except IndexError:
                if GW.second_pass_check == True:
                    finish_game_lbl['text'] = 'ТЫ ДОШЁЛ ДО КОНЦА! МОЛОДЕЦ!'
                    submit_btn["state"] = "disabled"
                    input_field["state"] = "disabled"
                    advise_btn["state"] = "disabled"
                else:
                    words_dict = words_dict_reverse
                    GW.second_pass_check = True
                    GW.id, GW.eng_word, GW.rus_word = get_random_words(words_dict)
                    switch_keyboard_layout()
                    key_layout['text'] = f"{keyboard_layout()}"
                    input_field.delete(0, 'end')

        GW.word_to_speak = random.choice(list(GW.rus_word))
        label_eng_word['text'] = GW.word_to_speak
        words_with_mistakes_lbl['text'] = ', '.join(GW.words_with_mistakes)

        if GW.second_pass_check == False:
            input_field.delete(0, 'end')
            input_field.insert(0, f"{'_' * len(list(GW.eng_word)[0])}")
            GW.position_count = 0
        
        root.update()
        key_layout['text'] = f"{keyboard_layout()}" # windows update language input only after root.update
        root.update()

        speak_word(GW.eng_word)

def click_voice_button():
     speak_word(GW.rus_word) if GW.second_pass_check else speak_word(GW.eng_word)  # on 2nd iteration rus_word contains ENG word
     input_field.focus()

def some_letter_advise():
    input_part_of_world = input_field.get().replace("_", "")
    len_of_input_text = len(input_part_of_world)
    input_field.delete(0, 'end')
    try:
        input_field.insert(0, f"{input_part_of_world}{list(GW.eng_word)[0][len_of_input_text]}")
    except IndexError:
         input_field.insert(0, input_part_of_world)
    
    input_field.focus()
    advise_btn["state"] = "disabled"

def on_input_change(event) -> None:
    """Catch letters and Backspace to show correct numbers of _ _ _ instead of symbols"""
    # _ _ _ _ only for eng words as tkinter doesn't like cyrillic
    if GW.second_pass_check == False:
        if (event.keysym == 'BackSpace' or event.keycode == 8 or event.char == '\x08'):
            current_word = input_field.get()
            GW.position_count = GW.position_count - 1 if GW.position_count > 0 else 0
            current_word = current_word[:GW.position_count] + "_" * (len(list(GW.eng_word)[0]) - len(current_word[:GW.position_count]))  

            input_field.delete(0, 'end')
            input_field.insert(0, f"{current_word}")     

        elif event.char:
            GW.position_count = GW.position_count + 1
            current_word = input_field.get().replace("_", "")
            current_word = current_word + "_" * (len(list(GW.eng_word)[0]) - len(current_word))

            input_field.delete(0, 'end')
            input_field.insert(0, f"{current_word}")    


# ###############################################
root = Tk() 
root.title("Учим Английский (и немного Русский)")
root.geometry("1300x800")

###
frame_1_1 = ttk.Frame(borderwidth=1, relief=SOLID, padding=10)
progress = ttk.Progressbar(frame_1_1, mode='determinate')
progress.pack(fill='x')
frame_1_1.pack(anchor=NW, fill=X, padx=5, pady=5)
###
frame_select_game = ttk.Frame(borderwidth=1, relief=SOLID, padding=10, height=40)
voice_btn = ttk.Button(frame_select_game, text="Словарь", command='learn_dictionary')
voice_btn.pack(fill='both', expand=True)
advise_btn = ttk.Button(frame_select_game, text="Лесенка", command='learn_upstairs')
advise_btn.pack(fill='both', expand=True)

###
frame_2_1 = ttk.Frame(borderwidth=1, relief=SOLID, padding=10, height=40)
key_layout = ttk.Label(frame_2_1, text=f"{keyboard_layout()}", font=("Arial", 15))
key_layout.pack(fill='both', anchor=W, side='right')
frame_2_1.pack(anchor=N, fill=X, padx=5, pady=5)

###
frame_3 = ttk.Frame(borderwidth=1, relief=SOLID, padding=10)
frame_3_1 = ttk.Frame(frame_3, borderwidth=1, relief=SOLID, padding=10)
title_label_counter = ttk.Label(frame_3_1, text="Слов выучить осталось:", font=("Arial", 10))
title_label_counter.pack()
label_counter = ttk.Label(frame_3_1, text="0", font=("Arial", 15))
label_counter.pack(fill='both', anchor=N)
label_counter['text'] = len(get_dict()[0]) + len(get_dict()[1]) # rus + eng dicts
frame_3_1.pack(anchor=N, fill="both", side="left", padx=5, pady=5)

#
frame_3_2 = ttk.Frame(frame_3, borderwidth=1, relief=SOLID, padding=10)
label_exercise = ttk.Label(frame_3_2, text="Напиши перевод слова", font=("Arial", 20)) 
label_eng_word = ttk.Label(frame_3_2, text=f"{GW.rus_word}", font=("Arial", 30), anchor=N)
label_exercise.pack(fill=X)
label_eng_word.pack(fill=X)
frame_3_2.pack(anchor=N, fill="both", side="left", padx=5, pady=5)

#
frame_3_3 = ttk.Frame(frame_3, borderwidth=1, relief=SOLID, padding=10)
frame_3_3_1 = ttk.Frame(frame_3_3, borderwidth=1, relief=SOLID)
input_field = ttk.Entry(frame_3_3_1, font=("Cascadia Code", 30), justify="center")
input_field.bind('<KeyRelease>', on_input_change)
input_field.pack(fill="both")
input_field.focus()

submit_btn = ttk.Button(frame_3_3_1, text="Отправить", command=click_submit_button)
submit_btn.pack(fill='both')

frame_3_3_1.pack(anchor=NE, fill="both", side="left", padx=5, pady=5)

frame_3_3_2 = ttk.Frame(frame_3_3, borderwidth=0, relief=SOLID)
voice_btn = ttk.Button(frame_3_3_2, text="Звук", command=click_voice_button)
voice_btn.pack(fill='both', expand=True)
advise_btn = ttk.Button(frame_3_3_2, text="Буква", command=some_letter_advise)
advise_btn.pack(fill='both', expand=True)
frame_3_3_2.pack(anchor=NE, fill="both", side="left", padx=5, pady=5)

frame_3_3.pack(anchor=NE, fill="both", side="left", padx=5, pady=5)

#
frame_3_4 = ttk.Frame(frame_3, borderwidth=1, relief=SOLID, padding=10)
label_prev_result = ttk.Label(frame_3_4, text="ПРЕДЫДУЩАЯ ПАРА", font=("Arial", 9))
label_prev_result.pack(fill=X)
label_prev_world = ttk.Label(frame_3_4, text="", font=("Arial", 10))
label_prev_world.pack(fill=X)
label_prev_answer = ttk.Label(frame_3_4, text="", font=("Arial", 10))
label_prev_answer.pack(fill=X)
frame_3_4.pack(anchor=NE, fill="both", side="left", padx=5, pady=5)
frame_3.pack(fill=X, padx=5, pady=5)

###
frame_4 = ttk.Frame(borderwidth=1, relief=SOLID, padding=10)
great_lbl = ttk.Label(frame_4, text="")
great_lbl.pack()
title_words_with_mistakes_lbl = ttk.Label(frame_4, text="Слова с ошибками:", font=("Arial", 10))
words_with_mistakes_lbl = ttk.Label(frame_4, text="",font=("Arial", 15), justify="left")
title_words_with_mistakes_lbl.pack()
words_with_mistakes_lbl.pack()
frame_4.pack(fill=X, padx=5, pady=5)

frame_5 = ttk.Frame(borderwidth=1, relief=SOLID, padding=10)
finish_game_lbl = ttk.Label(frame_5, text="", font=("Arial", 20))
finish_game_lbl.pack()
finish_btn = ttk.Button(frame_5, text="НАЧАТЬ ЗАНОВО", command=start_game)
finish_btn.pack(fill='both')
finish_btn["state"] = "disabled"
frame_5.pack(fill=X, padx=5, pady=5)

root.bind('<Return>', func=click_submit_button)

start_choice_game()



root.update()   # root update needs to show window before Text spech is running
speak_word(GW.eng_word)

root.mainloop()