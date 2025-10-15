from tkinter import *
from tkinter import ttk
from functions import get_random_words, GW, get_dict, speak_word, switch_keyboard_layout, async_beep, keyboard_layout
import winsound
from time import sleep
import random
from datetime import datetime


class UpstairsGame:
    def __init__(self, root):
        self.root = root
        self.create_interface()

    def create_interface(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)

        self.frame_1_1 = ttk.Frame(self.main_frame, borderwidth=1, relief=SOLID, padding=10)
        self.progress = ttk.Progressbar(self.frame_1_1, mode='determinate')
        self.progress.pack(fill='x')
        self.frame_1_1.pack(anchor=NW, fill=X, padx=5, pady=5)

        ###
        self.frame_2_1 = ttk.Frame(self.main_frame, borderwidth=1, relief=SOLID, padding=10, height=40)
        self.key_layout = ttk.Label(self.frame_2_1, text=f"{keyboard_layout()}", font=("Arial", 15))
        self.key_layout.pack(fill='both', anchor=W, side='right')
        self.frame_2_1.pack(anchor=N, fill=X, padx=5, pady=5)

        ###
        self.frame_3 = ttk.Frame(self.main_frame, borderwidth=1, relief=SOLID, padding=10)
        self.frame_3_1 = ttk.Frame(self.frame_3, borderwidth=1, relief=SOLID, padding=10)
        self.title_label_counter = ttk.Label(self.frame_3_1, text="Кругов осталось:", font=("Arial", 10))
        self.title_label_counter.pack()
        self.label_counter = ttk.Label(self.frame_3_1, text="0", font=("Arial", 15))
        self.label_counter.pack(fill='both', anchor=N)
        self.frame_3_1.pack(anchor=N, fill="both", side="left", padx=5, pady=5)
        self.frame_3.pack()

        #
        self.frame_3_2 = ttk.Frame(self.frame_3, borderwidth=1, relief=SOLID, padding=10)
        self.label_exercise = ttk.Label(self.frame_3_2, text="Напиши перевод слова", font=("Arial", 20)) 
        self.label_eng_word = ttk.Label(self.frame_3_2, text=f"{GW.rus_word}", font=("Arial", 30), anchor=N)
        self.label_exercise.pack(fill=X)
        self.label_eng_word.pack(fill=X)
        self.frame_3_2.pack(anchor=N, fill="both", side="left", padx=5, pady=5)

        #
        self.frame_3_3 = ttk.Frame(self.frame_3, borderwidth=1, relief=SOLID, padding=10)
        self.frame_3_3_1 = ttk.Frame(self.frame_3_3, borderwidth=1, relief=SOLID)
        self.input_field = ttk.Entry(self.frame_3_3_1, font=("Cascadia Code", 30), justify="center")
        self.input_field.bind('<KeyRelease>', self.on_input_change)
        self.input_field.pack(fill="both")
        self.input_field.focus()


        self.submit_btn = ttk.Button(self.frame_3_3_1, text="Отправить", command=self.click_submit_button)
        self.submit_btn.pack(fill='both')

        self.frame_3_3_1.pack(anchor=NE, fill="both", side="left", padx=5, pady=5)

        self.frame_3_3_2 = ttk.Frame(self.frame_3_3, borderwidth=0, relief=SOLID)
        self.voice_btn = ttk.Button(self.frame_3_3_2, text="Звук", command=self.click_voice_button)
        self.voice_btn.pack(fill='both', expand=True)
        self.advise_btn = ttk.Button(self.frame_3_3_2, text="Буква", command=self.some_letter_advise)
        self.advise_btn.pack(fill='both', expand=True)
        self.frame_3_3_2.pack(anchor=NE, fill="both", side="left", padx=5, pady=5)

        self.frame_3_3.pack(anchor=NE, fill="both", side="left", padx=5, pady=5)

        #
        self.frame_3_4 = ttk.Frame(self.frame_3, borderwidth=1, relief=SOLID, padding=10)
        self.label_prev_result = ttk.Label(self.frame_3_4, text="ПРЕДЫДУЩАЯ ПАРА", font=("Arial", 9))
        self.label_prev_result.pack(fill=X)
        self.label_prev_world = ttk.Label(self.frame_3_4, text="", font=("Arial", 10))
        self.label_prev_world.pack(fill=X)
        self.label_prev_answer = ttk.Label(self.frame_3_4, text="", font=("Arial", 10))
        self.label_prev_answer.pack(fill=X)
        self.frame_3_4.pack(anchor=NE, fill="both", side="left", padx=5, pady=5)
        self.frame_3.pack(fill=X, padx=5, pady=5)

        ###
        self.frame_4 = ttk.Frame(self.main_frame, borderwidth=1, relief=SOLID, padding=10)
        self.great_lbl = ttk.Label(self.frame_4, text="")
        self.great_lbl.pack()
        self.title_words_with_mistakes_lbl = ttk.Label(self.frame_4, text="Слова с ошибками:", font=("Arial", 10))
        self.words_with_mistakes_lbl = ttk.Label(self.frame_4, text="",font=("Arial", 15), justify="left")
        self.title_words_with_mistakes_lbl.pack()
        self.words_with_mistakes_lbl.pack()
        self.frame_4.pack(fill=X, padx=5, pady=5)

        self.frame_5 = ttk.Frame(self.main_frame, borderwidth=1, relief=SOLID, padding=10)
        self.finish_game_lbl = ttk.Label(self.frame_5, text="", font=("Arial", 20))
        self.finish_game_lbl.pack()
        self.finish_btn = ttk.Button(self.frame_5, text="НАЧАТЬ ЗАНОВО", command=self.start_game)
        self.finish_btn.pack(fill='both')
        self.finish_btn["state"] = "disabled"
        self.frame_5.pack(fill=X, padx=5, pady=5)

        self.root.bind('<Return>', func=self.click_submit_button)

        self.root.update()

        self.start_game()

    def start_game(self) -> None:
        GW.output_file_name = datetime.now().strftime('%d%m%Y_%H%M%S')
        global words_dict
        words_dict, _ = get_dict()  # I hope garbage collection works in this case
        GW.total_words = len(get_dict()[0])

        GW.eng_word, GW.rus_word = list(words_dict[0])
        GW.word_to_speak = random.choice(list(GW.rus_word))
        self.label_eng_word['text'] = GW.word_to_speak
        self.great_lbl['text'] = ''
        self.label_counter['text'] = len(words_dict)
        self.input_field.focus()
        GW.words_with_mistakes = set()
        self.submit_btn["state"] = "normal"
        self.input_field["state"] = "normal"
        self.input_field.insert(0, f"{'_' * len(list(GW.eng_word)[0])}")
        self.finish_game_lbl['text'] = ''
        self.update_progress(GW.total_words)
        self.key_layout['text'] = f"{keyboard_layout()}"
        speak_word(GW.eng_word)

    def click_submit_button(self, event=None):
        global words_dict
        input_word = self.input_field.get().strip().lower().replace('  ', ' ').replace("_", "")
        if input_word:  # if something is typed
            if input_word in GW.eng_word:
                
                self.submit_btn["state"] = "enabled"
                self.input_field["state"] = "enabled"
                self.voice_btn["state"] = "enabled"
                self.advise_btn["state"] = "enabled"
                self.great_lbl['text'] = "МОЛОДЕЦ! Идем дальше!"
                winsound.PlaySound("MailBeep", winsound.SND_ALIAS | winsound.SND_ASYNC)
                sleep(0.5)

                if GW.upst_current == GW.upst_limit_for_circle: # next iteration
                    GW.upst_current = 0
                    GW.upst_limit_for_circle += 1

                else:   # inside one iteration
                    GW.upst_current += 1
                
                
                
            else:
                self.great_lbl['text'] = "НЕПРАВИЛЬНО"
                async_beep()
                sleep(0.5)
                GW.words_with_mistakes.add(GW.word_to_speak)

            with open(f"Output_{GW.output_file_name}.txt", "a", encoding='utf-8') as text_file: # encoding is MUST or you will get error during writing cp1252
                    text_file.write(f'{GW.eng_word} - {input_word}\n')

            self.label_prev_world['text'] = f'Искомое слово:\n   {GW.word_to_speak}'
            self.label_prev_answer['text'] = f'Написанное слово:\n   {input_word}'

            self.label_counter['text'] = len(words_dict) - GW.upst_limit_for_circle
            
            self.update_progress(left_words = len(words_dict))
   
            try:
                GW.eng_word, GW.rus_word = list(words_dict[GW.upst_current])
                GW.word_to_speak = random.choice(list(GW.rus_word))
                self.label_eng_word['text'] = GW.word_to_speak
                self.great_lbl['text'] = ''
                self.input_field.focus()
                GW.words_with_mistakes = set()
                self.submit_btn["state"] = "normal"
                self.input_field["state"] = "normal"
                self.input_field.insert(0, f"{'_' * len(list(GW.eng_word)[0])}")
                self.finish_game_lbl['text'] = ''
                self.update_progress(GW.total_words)
                self.key_layout['text'] = f"{keyboard_layout()}"

                self.input_field.delete(0, 'end')
                self.input_field.insert(0, f"{'_' * len(list(GW.eng_word)[0])}")
                GW.position_count = 0

                self.root.update()
                self.key_layout['text'] = f"{keyboard_layout()}" # windows update language input only after root.update
                self.root.update()

                speak_word(GW.eng_word)

            except KeyError:
                self.finish_game_lbl['text'] = 'ТЫ ДОШЁЛ ДО КОНЦА! МОЛОДЕЦ!'
                self.submit_btn["state"] = "disabled"
                self.input_field["state"] = "disabled"
                self.advise_btn["state"] = "disabled"
                self.root.update()
            
    
    def update_progress(self, left_words):
        self.progress['value'] = (left_words / GW.total_words) * 100

    def click_voice_button(self):
        speak_word(GW.rus_word) if GW.second_pass_check else speak_word(GW.eng_word)  # on 2nd iteration rus_word contains ENG word
        self.input_field.focus()

    def some_letter_advise(self):
        input_part_of_world = self.input_field.get().replace("_", "")
        len_of_input_text = len(input_part_of_world)
        self.input_field.delete(0, 'end')
        try:
            self.input_field.insert(0, f"{input_part_of_world}{list(GW.eng_word)[0][len_of_input_text]}")
        except IndexError:
            self.input_field.insert(0, input_part_of_world)
        
        self.input_field.focus()
        self.advise_btn["state"] = "disabled"

    def on_input_change(self, event) -> None:
        """Catch letters and Backspace to show correct numbers of _ _ _ instead of symbols"""
        # _ _ _ _ only for eng words as tkinter doesn't like cyrillic
        if GW.second_pass_check == False:
            if (event.keysym == 'BackSpace' or event.keycode == 8 or event.char == '\x08'):
                current_word = self.input_field.get()
                GW.position_count = GW.position_count - 1 if GW.position_count > 0 else 0
                current_word = current_word[:GW.position_count] + "_" * (len(list(GW.eng_word)[0]) - len(current_word[:GW.position_count]))  

                self.input_field.delete(0, 'end')
                self.input_field.insert(0, f"{current_word}")     

            elif event.char:
                GW.position_count = GW.position_count + 1
                current_word = self.input_field.get().replace("_", "")
                current_word = current_word + "_" * (len(list(GW.eng_word)[0]) - len(current_word))

                self.input_field.delete(0, 'end')
                self.input_field.insert(0, f"{current_word}")    