# https://poe.com/s/Fm2aIqyMN5HqhSpFdFRv
import tkinter as tk
from datetime import datetime

def send_message(event=None):
    text = entry.get()  # Получаем текст из поля ввода
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")  # Получаем текущую дату и время
    message = f"{timestamp}  {text}\n"  # Формируем сообщение с датой, временем и текстом
    log.insert(tk.END, message)  # Добавляем сообщение к логу
    entry.delete(0, tk.END)  # Очищаем поле ввода
    save_message(message)  # Сохраняем сообщение в файл

def save_message(message):
    filename = "log.txt"  # Имя файла, в который будем сохранять сообщения
    with open(filename, "a") as file:  # Открываем файл для добавления сообщения
        file.write(message)  # Записываем сообщение в файл

# Создаем окно
window = tk.Tk()
window.geometry("600x400")  # Изменим ширину окна на 600 пикселей
window.title("Записнычок событий.")

# Создаем поле для ввода текста
entry = tk.Entry(window, width=100)  # Изменим ширину поля на ... символов
entry.pack()
entry.bind("<Return>", send_message)  # Привязываем отправку к нажатию Enter
entry.focus()  # Устанавливаем фокус на поле ввода

# Создаем кнопку "отправить"
button = tk.Button(window, text="Отправить", command=send_message)
button.pack()

# Создаем лог
log = tk.Text(window)
log.pack()

# Запускаем главный цикл обработки событий
window.mainloop()