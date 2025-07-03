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
        mins, secs = divmod(remaining_time.get(), 60)  # конвертируем секунды в минуты и секунды
        remaining_time.set(remaining_time.get() - 1)
        label.config(text=f"{mins:02d}:{secs:02d}") #  отображаем время в формате MM:SS
        window.after(1000, update_timer)
    else:
        play_sound()
        label.config(text="Время вышло!")

def play_sound():
      # Воспроизводим звуковой сигнал
    winsound.Beep(440, 500)
    winsound.Beep(220, 500)
    winsound.Beep(660, 500)
    winsound.Beep(440, 500)
    winsound.Beep(1000, 500)
    winsound.Beep(330, 500)
    winsound.Beep(440, 1000)

def increase_opacity():
    alpha = window.attributes('-alpha')
    if alpha < 1.0:
        alpha += 0.1
        window.attributes('-alpha', alpha)

def decrease_opacity():
    alpha = window.attributes('-alpha')
    if alpha > 0.15: # Изменено условие
        alpha -= 0.1
        window.attributes('-alpha', alpha)

def toggle_always_on_top():
    global always_on_top  # Используем глобальную переменную
    always_on_top = not always_on_top  # Инвертируем значение
    window.wm_attributes("-topmost", always_on_top)
    if always_on_top:
        top_button.config(text="Не поверх всех окон")
    else:
        top_button.config(text="Поверх всех окон")


# Создаем главное окно
window = tk.Tk()

# Устанавливаем заголовок окна
window.title("Таймер обратного отсчета")

# Устанавливаем размеры окна
window.geometry("400x600+500+100")  # Увеличили высоту с 550 до 600

# Делаем окно полупрозрачным (по умолчанию)
window.attributes('-alpha', 1.0)  # Установите значение от 0.0 (полностью прозрачный) до 1.0 (полностью непрозрачный)

# Переменная для хранения состояния "поверх всех окон"
always_on_top = False

font_size = 16  # Определяем размер шрифта

# КНОПКИ ПРОЗРАЧНОСТИ - ПЕРЕНЕСЕНЫ В НАЧАЛО!!!
opacity_frame = tk.Frame(window)  #  Создаем фрейм для размещения кнопок
opacity_frame.pack(pady=5)

less_transparent_button = tk.Button(opacity_frame, text="[-]", command=increase_opacity, font=("Helvetica", font_size))
less_transparent_button.pack(side=tk.LEFT, padx=5)  # Размещаем слева с небольшим отступом

more_transparent_button = tk.Button(opacity_frame, text="[+]", command=decrease_opacity, font=("Helvetica", font_size))
more_transparent_button.pack(side=tk.LEFT, padx=5)  # Размещаем слева с небольшим отступом

# Кнопка "Поверх всех окон"
top_button = tk.Button(window, text="Поверх всех окон", command=toggle_always_on_top, font=("Helvetica", font_size))
top_button.pack(pady=5)


# Создаем поля ввода для минут и секунд
label_minutes = tk.Label(window, text="Минуты:", font=("Helvetica", font_size))
label_minutes.pack()
entry_minutes = tk.Entry(window, font=("Helvetica", font_size), width=5)  # Установили ширину
entry_minutes.pack()

label_seconds = tk.Label(window, text="Секунды:", font=("Helvetica", font_size))
label_seconds.pack()
entry_seconds = tk.Entry(window, font=("Helvetica", font_size), width=5)  # Установили ширину
entry_seconds.pack()

# Создаем кнопку для запуска таймера
start_button = tk.Button(window, text="Старт", command=start_timer, bg="lightgreen", fg="black", font=("Helvetica", font_size))
start_button.pack(pady=10, fill=tk.X)


# Создаем текстовое окно для ввода текста
label_text = tk.Label(window, text="Введите текст:", font=("Helvetica", font_size))
label_text.pack()
text_input = tk.Text(window, height=5, width=30, font=("Helvetica", font_size))  # Увеличиваем размер шрифта
text_input.pack()

# Создаем переменную для хранения оставшегося времени
remaining_time = tk.IntVar()

# Создаем метку для отображения оставшегося времени
label = tk.Label(window, font=("Helvetica", 48))  # Еще больше шрифт для таймера
label.pack(pady=50)


# Запускаем главный цикл обработки событий
window.mainloop()