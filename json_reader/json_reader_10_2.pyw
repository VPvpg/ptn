# читалка файлов, сохранённых из тут https://chatgptchatapp.com/ru

import json
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from datetime import datetime


def load_json_file():
    """Открывает диалоговое окно выбора файла, читает JSON и отображает его содержимое."""
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            json_text.delete("1.0", tk.END)  # Очищаем поле текста
            formatted_output = format_json_data(data)  # Форматируем данные
            json_text.insert(tk.END, formatted_output)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл не найден.")
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Некорректный формат JSON.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


def save_to_md_file():
    """Сохраняет содержимое текстового поля в Markdown-файл."""
    file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")])
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json_text.get("1.0", tk.END))
            messagebox.showinfo("Успех", "Файл успешно сохранен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")


def format_json_data(data):
    """Форматирует JSON-данные для читаемого отображения."""
    output = ""
    for chat_id, chat_data in data.items():
        output += f"# Чат ID: {chat_id}\n"
        output += f"**Название:** {chat_data.get('name', 'Не указано')}\n"
        timestamp = chat_data.get('date', 0)
        date = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        output += f"**Дата:** {date}\n\n"
        output += "## Сообщения\n"
        for message in chat_data.get('contents', []):
            role = message.get('role', 'Неизвестно')
            content = message.get('content', 'Пустое сообщение')
            msg_timestamp = message.get('timestamp', 0)
            msg_date = datetime.fromtimestamp(msg_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
            output += f"### [{msg_date}] {role}\n{content}\n\n"
        output += "\n"
    return output


# Создаем основное окно
root = tk.Tk()
root.title("JSON Chat Reader")
#root.geometry("800x600")
root.state("zoomed")

# Кнопка для выбора файла
load_button = tk.Button(root, text="Выбрать JSON файл", command=load_json_file)
load_button.pack(pady=5)

# Кнопка для сохранения в Markdown
save_button = tk.Button(root, text="Сохранить в Markdown", command=save_to_md_file)
save_button.pack(pady=5)

# Текстовое поле для отображения JSON
json_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10))
json_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Запускаем главный цикл обработки событий
root.mainloop()