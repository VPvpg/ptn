# Переводит файлы или вставленный текст с сохранением форматирования.
# pip install deep-translator

import tkinter as tk
from deep_translator import GoogleTranslator
from tkinter import filedialog
import time

def translate_text():
    text = english_text.get("1.0", tk.END).strip()
    lines = text.splitlines()
    translated_lines = []

    try:
        translator = GoogleTranslator(source='auto', target='ru')
        for line in lines:
            indent = len(line) - len(line.lstrip())
            if line.strip():
                for _ in range(3):
                    try:
                        translated_text = translator.translate(line.lstrip())
                        translated_text = translated_text if translated_text is not None else "Ошибка: перевод не выполнен"
                        break
                    except Exception as e:
                        if _ == 2:
                            translated_text = f"Ошибка: {str(e)}"
                            break
                        time.sleep(1)
            else:
                translated_text = ""
            translated_line = " " * indent + translated_text
            translated_lines.append(translated_line)
        translated_text = "\n".join(translated_lines)
        russian_text.delete("1.0", tk.END)
        russian_text.insert("1.0", translated_text if translated_text else "Пустой ввод")
    except Exception as e:
        russian_text.delete("1.0", tk.END)
        russian_text.insert("1.0", f"Ошибка перевода: {e}")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            english_text.delete("1.0", tk.END)
            english_text.insert("1.0", content)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            content = russian_text.get("1.0", tk.END).strip()
            file.write(content)

def increase_font():
    global font_size
    font_size = min(font_size + 2, 24)
    update_font()

def decrease_font():
    global font_size
    font_size = max(font_size - 2, 8)
    update_font()

def update_font():
    new_font = ("Arial", font_size)
    english_text.config(font=new_font)
    russian_text.config(font=new_font)
    left_label.config(font=new_font)
    right_label.config(font=new_font)
    translate_button.config(font=("Arial", font_size - 2))
    font_size_label.config(text=f"Размер шрифта: {font_size}", font=("Arial", font_size - 2))
    increase_button.config(font=("Arial", font_size - 2))
    decrease_button.config(font=("Arial", font_size - 2))
    clear_button.config(font=("Arial", font_size - 2))

def clear_fields():
    english_text.delete("1.0", tk.END)
    russian_text.delete("1.0", tk.END)

root = tk.Tk()
root.title("Переводчик")
root.state("zoomed")

font_size = 14

main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

left_frame = tk.Frame(main_frame)
right_frame = tk.Frame(main_frame)
left_frame.grid(row=0, column=0, sticky="nsew")
right_frame.grid(row=0, column=1, sticky="nsew")
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)

left_label = tk.Label(left_frame, text="Английский текст:", font=("Arial", font_size))
left_label.grid(row=0, column=0, pady=(0, 5), sticky="ew")

english_text = tk.Text(left_frame, wrap=tk.WORD, font=("Arial", font_size))
english_text.grid(row=1, column=0, sticky="nsew")
left_frame.grid_rowconfigure(1, weight=1)
left_frame.grid_columnconfigure(0, weight=1)

right_label = tk.Label(right_frame, text="Русский перевод:", font=("Arial", font_size))
right_label.grid(row=0, column=0, pady=(0, 5), sticky="ew")

russian_text = tk.Text(right_frame, wrap=tk.WORD, font=("Arial", font_size))
russian_text.grid(row=1, column=0, sticky="nsew")
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

translate_button = tk.Button(button_frame, text="Перевести", command=translate_text, font=("Arial", font_size - 2))
translate_button.grid(row=0, column=0, padx=5)

font_size_label = tk.Label(button_frame, text=f"Размер шрифта: {font_size}", font=("Arial", font_size - 2))
font_size_label.grid(row=0, column=1, padx=5)

increase_button = tk.Button(button_frame, text="+", command=increase_font, font=("Arial", font_size - 2))
increase_button.grid(row=0, column=2, padx=5)

decrease_button = tk.Button(button_frame, text="-", command=decrease_font, font=("Arial", font_size - 2))
decrease_button.grid(row=0, column=3, padx=5)

clear_button = tk.Button(button_frame, text="Очистить", command=clear_fields, font=("Arial", font_size - 2))
clear_button.grid(row=0, column=4, padx=5)

menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar)
menubar.add_cascade(label="Файл", menu=file_menu)

file_menu.add_command(label="Открыть", command=open_file)
file_menu.add_command(label="Сохранить", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=root.quit)

root.mainloop()