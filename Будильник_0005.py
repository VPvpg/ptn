

import tkinter as tk
import datetime
import winsound

def set_alarm():
    hours = int(hour_entry.get())
    minutes = int(minute_entry.get())

    alarm_time = datetime.datetime.now().replace(hour=hours, minute=minutes, second=0)
    current_time = datetime.datetime.now()

    while current_time < alarm_time:
        current_time = datetime.datetime.now()
        time_left = alarm_time - current_time

        hours_left = time_left.seconds // 3600
        minutes_left = (time_left.seconds % 3600) // 60

        time_left_str = f"Осталось: {hours_left:02d}:{minutes_left:02d}"
        label.config(text=time_left_str)
        label.update()

    label.config(text="Время истекло!")
    winsound.Beep(1000, 1000)  # Воспроизведение звука через бип
    winsound.Beep(500, 1000)  # Воспроизведение звука через бип
    winsound.Beep(1000, 2000)  # Воспроизведение звука через бип

def submit():
    user_text = text_entry.get()
    label.config(text=f"Привет, {user_text}!")

root = tk.Tk()
root.title("Будильник")
root.geometry("200x100")  # Установка размера окна

frame = tk.Frame(root)
frame.pack()

hour_label = tk.Label(frame, text="Часы:")
hour_label.pack(side="left")

hour_entry = tk.Entry(frame, width=2)
hour_entry.pack(side="left")

minute_label = tk.Label(frame, text="Минуты:")
minute_label.pack(side="left")

minute_entry = tk.Entry(frame, width=2)
minute_entry.pack(side="left")

button = tk.Button(root, text="Установить", command=set_alarm, width=200)
button.pack()

text_label = tk.Label(root, text="событие")
text_label.pack()

text_entry = tk.Entry(root, width=200)
text_entry.pack()

#submit_button = tk.Button(root, text="Отправить", command=submit)
#submit_button.pack()

label = tk.Label(root, text="")
label.pack()

root.mainloop()