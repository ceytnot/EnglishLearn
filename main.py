# C:\Users\NewHorizon\Documents\PythonProjects\EnglishLearn\venv\Scripts\Activate.ps1
from tkinter import *
from tkinter import ttk
from functions import get_random_words, GW, get_dict, speak_word
from datetime import datetime


def start_game():
    GW.output_file_name = datetime.now().strftime('%d%m%Y_%H%M%S')
    global words_dict
    words_dict = get_dict()
    GW.eng_word, GW.rus_word = get_random_words(words_dict)    
    label_eng_word['text'] = GW.rus_word
    great_lbl['text'] = ''
    label_counter['text'] = len(get_dict())
    GW.correct_counter = len(words_dict)
    input_field.delete(0, 'end')
    input_field.focus()
    GW.words_with_mistakes = set()
    submit_btn["state"] = "normal"
    input_field["state"] = "normal"
    finish_game_lbl['text'] = ''    

# functions
def click_submit_button(event=None):
    input_word = input_field.get().strip().lower()
    if input_word:  # if something is typed
        if input_word == GW.eng_word:
            great_lbl['text'] = "МОЛОДЕЦ! Идем дальше!"

            try:
                del words_dict[GW.eng_word]
            except KeyError:
                pass

            GW.correct_counter = len(words_dict)
            
        else:
            great_lbl['text'] = "НЕПРАВИЛЬНО"

            GW.words_with_mistakes.add(GW.eng_word)

        with open(f"Output_{GW.output_file_name}.txt", "a") as text_file:
                text_file.write(f'{GW.eng_word} - {input_word}\n')

        label_prev_world['text'] = f'Искомое слово:\n   {GW.eng_word}'
        label_prev_answer['text'] = f'Написанное слово:\n   {input_word}'

        label_counter['text'] = str(GW.correct_counter)
        input_field.delete(0, 'end')
        input_field.focus()

        try:
            GW.eng_word, GW.rus_word = get_random_words(words_dict)            
        except IndexError:
                finish_game_lbl['text'] = 'ТЫ ДОШЁЛ ДО КОНЦА! МОЛОДЕЦ!'
                submit_btn["state"] = "disabled"
                input_field["state"] = "disabled"

        label_eng_word['text'] = GW.rus_word
        words_with_mistakes_lbl['text'] = ', '.join(GW.words_with_mistakes)
        root.update()
        speak_word(GW.eng_word)

def click_voice_button():
     speak_word(GW.eng_word)



root = Tk()     # создаем корневой объект - окно
root.title("Учим Английский с папой-программистом")     # устанавливаем заголовок окна
root.geometry("1280x800")    # устанавливаем размеры окна


###
frame_1_1 = ttk.Frame(borderwidth=1, relief=SOLID, padding=10)
label_description = ttk.Label(frame_1_1,text="За каждый правильный ответ тебе будет начисляться один балл, за неправильный - вычитаться один балл", font=("Arial", 10))
label_description.pack()
frame_1_1.pack(anchor=NW, fill=X, padx=5, pady=5)

###
frame_2_1 = ttk.Frame(borderwidth=1, relief=SOLID, padding=10, height=40)
frame_2_1.pack(anchor=N, fill=X, padx=5, pady=5)

###
frame_3 = ttk.Frame(borderwidth=1, relief=SOLID, padding=10)
frame_3_1 = ttk.Frame(frame_3, borderwidth=1, relief=SOLID, padding=10)
title_label_counter = ttk.Label(frame_3_1, text="Слов выучить осталось:", font=("Arial", 10))
title_label_counter.pack()
label_counter = ttk.Label(frame_3_1, text="0", font=("Arial", 15))
label_counter.pack(fill='both', anchor=N)
label_counter['text'] = len(get_dict())
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
input_field = ttk.Entry(frame_3_3_1, font=("Arial", 30), justify="center")
input_field.pack(fill="both")
input_field.focus()

submit_btn = ttk.Button(frame_3_3_1, text="Отправить", command=click_submit_button)
submit_btn.pack(fill='both')

frame_3_3_1.pack(anchor=NE, fill="both", side="left", padx=5, pady=5)

frame_3_3_2 = ttk.Frame(frame_3_3, borderwidth=0, relief=SOLID)
voice_btn = ttk.Button(frame_3_3_2, text="Подсказка", command=click_voice_button)
voice_btn.pack(fill='both', expand=True)
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

start_game()

root.update()   # root update needs to show indow before Text spech is running
speak_word(GW.eng_word)

root.mainloop()