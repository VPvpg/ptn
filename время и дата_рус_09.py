"""
Часы. Выводят время, день недели и год.
Добавлена полоска для наглядности.
И кнопка "поверх всех окон".

"""

import tkinter as tk
from datetime import datetime

def update_time():
    """Обновляет время, дату и индикатор"""
    current_time = datetime.now()
    weekdays = ["_пн_", "_вт_", "_ср_", "_чт.", "_птн_", "_сб_", "_вс_"]
    time_string = current_time.strftime("%H:%M %a %d:%m:%Y")
    time_string = time_string.replace("Mon", weekdays[0])
    time_string = time_string.replace("Tue", weekdays[1])
    time_string = time_string.replace("Wed", weekdays[2])
    time_string = time_string.replace("Thu", weekdays[3])
    time_string = time_string.replace("Fri", weekdays[4])
    time_string = time_string.replace("Sat", weekdays[5])
    time_string = time_string.replace("Sun", weekdays[6])
    time_label.config(text=time_string)

    # Обновление индикатора времени суток
    seconds_today = current_time.hour * 3600 + current_time.minute * 60 + current_time.second
    percent_of_day = seconds_today / 86400  # Всего 86400 секунд в сутках
    
    # Получаем текущую ширину окна
    current_width = root.winfo_width()
    fill_width = int(current_width * percent_of_day)
    
    canvas.delete("all")
    canvas.create_rectangle(0, 0, fill_width, bar_height, fill="darkblue")
    canvas.create_rectangle(fill_width, 0, current_width, bar_height, fill="lightgray")

    time_label.after(1000, update_time)

def toggle_always_on_top():
    global always_on_top
    always_on_top = not always_on_top
    root.attributes("-topmost", always_on_top)
    top_button.config(text="Поверх всех окон: ВКЛ" if always_on_top else "Поверх всех окон: ВЫКЛ")

def on_resize(event):
    # При изменении размера окна перерисовываем индикатор
    update_time()

root = tk.Tk()
root.title("Часы")

always_on_top = False
bar_height = 10

# Делаем окно адаптивным
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

time_label = tk.Label(root, font=("Helvetica", 48))
time_label.pack(pady=10)

# Canvas будет растягиваться вместе с окном
canvas = tk.Canvas(root, height=bar_height, highlightthickness=0)
canvas.pack(fill=tk.X, padx=10, pady=5)  # fill=tk.X растягивает по горизонтали

top_button = tk.Button(root, text="Поверх всех окон: ВЫКЛ", command=toggle_always_on_top)
top_button.pack(pady=10)

# Привязываем обработчик изменения размера окна
root.bind('<Configure>', on_resize)

update_time()

root.mainloop()