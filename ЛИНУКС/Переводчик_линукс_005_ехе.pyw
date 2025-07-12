#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox
from googletrans import Translator

font_size = 14

def increase_font():
    global font_size
    font_size += 2
    update_fonts()

def decrease_font():
    global font_size
    if font_size > 6:
        font_size -= 2
        update_fonts()

def update_fonts():
    english_text.config(font=("Arial", font_size))
    russian_text.config(font=("Arial", font_size))
    left_label.config(font=("Arial", font_size))
    right_label.config(font=("Arial", font_size))
    increase_button.config(font=("Arial", font_size - 2))
    decrease_button.config(font=("Arial", font_size - 2))
    clear_button.config(font=("Arial", font_size - 2))
    translate_button.config(font=("Arial", font_size - 2))
    font_size_label.config(text=f"{font_size}")

def clear_fields():
    english_text.delete("1.0", tk.END)
    russian_text.delete("1.0", tk.END)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        english_text.delete("1.0", tk.END)
        english_text.insert(tk.END, content)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        content = english_text.get("1.0", tk.END)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

def translate_text():
    src = english_text.get("1.0", tk.END) # Получаем текст как есть, включая все пробелы и переносы
    if not src.strip(): # Проверяем, есть ли что-то кроме пробелов
        messagebox.showinfo("Перевод", "Введите текст для перевода.")
        return
    try:
        translator = Translator()
        translated_lines = []
        
        # Разделяем текст на строки и обрабатываем каждую
        for line in src.splitlines():
            if line.strip(): # Если строка не пустая (содержит что-то кроме пробелов)
                # Находим начальные пробелы (отступы)
                leading_whitespace = line[:len(line) - len(line.lstrip())]
                # Переводим только саму строку без начальных пробелов
                translated_part = translator.translate(line.lstrip(), dest='ru').text
                # Собираем строку обратно с исходными отступами
                translated_lines.append(leading_whitespace + translated_part)
            else:
                # Если строка пустая или состоит только из пробелов, сохраняем её как есть
                translated_lines.append(line)
        
        # Объединяем переведенные строки обратно в один текст
        final_translated_text = "\n".join(translated_lines)

        russian_text.delete("1.0", tk.END)
        russian_text.insert(tk.END, final_translated_text)
    except Exception as e:
        messagebox.showerror("Ошибка перевода", f"Не удалось перевести текст.\n\n{e}")

root = tk.Tk()
root.title("Tkinter Text Translator")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
root.maxsize(root.winfo_screenwidth(), root.winfo_screenheight())

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

tk.Label(button_frame, text="Размер шрифта:").grid(row=0, column=0)
font_size_label = tk.Label(button_frame, text=f"{font_size}")
font_size_label.grid(row=0, column=1, padx=5)

increase_button = tk.Button(button_frame, text="+", command=increase_font, font=("Arial", font_size - 2))
increase_button.grid(row=0, column=2, padx=5)

decrease_button = tk.Button(button_frame, text="-", command=decrease_font, font=("Arial", font_size - 2))
decrease_button.grid(row=0, column=3, padx=5)

clear_button = tk.Button(button_frame, text="Очистить", command=clear_fields, font=("Arial", font_size - 2))
clear_button.grid(row=0, column=4, padx=5)

translate_button = tk.Button(button_frame, text="Перевести", command=translate_text, font=("Arial", font_size - 2))
translate_button.grid(row=0, column=5, padx=5)

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

menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Файл", menu=file_menu)

file_menu.add_command(label="Открыть", command=open_file)
file_menu.add_command(label="Сохранить", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=root.quit)

root.mainloop()
