import tkinter as tk
from tkinter import messagebox, filedialog
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
    try:
        with open(filename, "a") as file:  # Открываем файл для добавления сообщения
            file.write(message)  # Записываем сообщение в файл
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить сообщение в файл: {e}")

def view_log_file():
    filename = "log.txt"
    try:
        with open(filename, "r") as file:
            log_content = file.read()
        # Создаем новое окно для отображения содержимого файла
        view_window = tk.Toplevel(window)
        view_window.state('zoomed') # Изменяем размер окна на весь экран
        view_window.title("Содержимое файла log.txt")
        text_area = tk.Text(view_window, font=("Arial", 14))  # Увеличиваем шрифт
        text_area.insert(tk.END, log_content)
        text_area.config(state=tk.DISABLED)  # Делаем текстовое поле только для чтения
        text_area.pack(expand=True, fill=tk.BOTH)
    except FileNotFoundError:
        messagebox.showinfo("Файл не найден", "Файл log.txt не существует.")
    except Exception as e:
        messagebox.showerror("Ошибка чтения", f"Не удалось прочитать файл: {e}")

# Создаем окно
window = tk.Tk()
window.geometry("600x400+300+100")  # Изменим ширину окна на 600 пикселей
window.title("Записнычок событий.")

# Создаем поле для ввода текста
entry = tk.Entry(window, width=100, font=("Arial", 12))  # Изменим ширину поля на ... символов и шрифт
entry.pack()
entry.bind("<Return>", send_message)  # Привязываем отправку к нажатию Enter
entry.focus()  # Устанавливаем фокус на поле ввода

# Создаем кнопку "отправить"
button = tk.Button(window, text="Отправить", command=send_message, font=("Arial", 12)) # Изменим шрифт
button.pack()

# Создаем кнопку "посмотреть файл"
view_button = tk.Button(window, text="Посмотреть сохранённый файл", command=view_log_file, font=("Arial", 14)) # Изменим шрифт
view_button.pack()

# Создаем лог
log = tk.Text(window, font=("Arial", 14))  # Увеличиваем шрифт
log.pack()

# Запускаем главный цикл обработки событий
window.mainloop()