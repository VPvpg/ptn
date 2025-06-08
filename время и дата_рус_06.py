import tkinter as tk
from datetime import datetime

def update_time():
    """Функция, обновляющая время и дату в окне"""
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
    time_label.after(1000, update_time)  # Обновляем каждую секунду

root = tk.Tk()
root.title("Часы")

time_label = tk.Label(root, font=("Helvetica", 48))
time_label.pack(pady=20)

update_time()  # Запускаем функцию обновления времени

root.mainloop()