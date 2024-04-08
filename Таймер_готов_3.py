# таймер для винды
# https://poe.com/s/9LmNEm2B6EcTfomvAAWP

import tkinter as tk
import winsound

def start_timer():
    minutes = int(entry_minutes.get())
    seconds = int(entry_seconds.get())
    total_seconds = minutes * 60 + seconds
    remaining_time.set(total_seconds)
    update_timer()

def update_timer():
    if remaining_time.get() > 0:
        remaining_time.set(remaining_time.get() - 1)
        window.after(1000, update_timer)
    else:
        play_sound()

def play_sound():
      # Воспроизводим звуковой сигнал
    winsound.Beep(440, 500)
    winsound.Beep(220, 500)
    winsound.Beep(660, 500)
    winsound.Beep(440, 500)
    winsound.Beep(1000, 500)
    winsound.Beep(330, 500)
    winsound.Beep(440, 1000)

# Создаем главное окно
window = tk.Tk()

# Устанавливаем заголовок окна
window.title("Таймер обратного отсчета")

# Устанавливаем размеры окна
window.geometry("400x450")

# Создаем переменную для хранения оставшегося времени
remaining_time = tk.IntVar()

# Создаем метку для отображения оставшегося времени
label = tk.Label(window, textvariable=remaining_time, font=("Helvetica", 36))
label.pack(pady=50)

# Создаем поля ввода для минут и секунд
label_minutes = tk.Label(window, text="Минуты:")
label_minutes.pack()
entry_minutes = tk.Entry(window)
entry_minutes.pack()

label_seconds = tk.Label(window, text="Секунды:")
label_seconds.pack()
entry_seconds = tk.Entry(window)
entry_seconds.pack()

# Создаем текстовое окно для ввода текста
label_text = tk.Label(window, text="Введите текст:")
label_text.pack()
text_input = tk.Text(window, height=5, width=30, font=("Helvetica", 14))  # Увеличиваем размер шрифта
text_input.pack()

# Создаем кнопку для запуска таймера
start_button = tk.Button(window, text="Старт", command=start_timer)
start_button.pack(pady=10)

# Запускаем главный цикл обработки событий
window.mainloop()