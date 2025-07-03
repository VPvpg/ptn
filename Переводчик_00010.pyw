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
        translator = GoogleTranslator(source='en', target='ru')
        for line in lines:
            indent = len(line) - len(line.lstrip())
            if line.strip():
                for _ in range(3):
                    try:
                        translated_text = translator.translate(line.lstrip())
                        # Проверяем, что translated_text не None
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

root = tk.Tk()
root.title("Переводчик")
root.state("zoomed")

main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

left_label = tk.Label(left_frame, text="Английский текст:")
left_label.pack(pady=(0, 5))

english_text = tk.Text(left_frame, wrap=tk.WORD)
english_text.pack(expand=True, fill=tk.BOTH)

right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.BOTH, expand=True)

right_label = tk.Label(right_frame, text="Русский перевод:")
right_label.pack(pady=(0, 5))

russian_text = tk.Text(right_frame, wrap=tk.WORD)
russian_text.pack(expand=True, fill=tk.BOTH)

translate_button = tk.Button(root, text="Перевести", command=translate_text)
translate_button.pack(pady=10)

menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar)
menubar.add_cascade(label="Файл", menu=file_menu)

file_menu.add_command(label="Открыть", command=open_file)
file_menu.add_command(label="Сохранить", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=root.quit)

root.mainloop()