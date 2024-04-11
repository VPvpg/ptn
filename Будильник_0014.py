#будильник с "мелодией" с защитой от букв. С выходом по кнопке

import tkinter as tk
import datetime
import winsound

def Музон():

   winsound.Beep(3456, 1000)
   winsound.Beep(864, 1000)
   winsound.Beep(216, 1000)
   winsound.Beep(1728, 1000)
   winsound.Beep(432, 1000)
   winsound.Beep(99, 1000)
   winsound.Beep(3456, 2000)

def set_alarm():
    try:
        hours = int(hour_entry.get())
        minutes = int(minute_entry.get())

        alarm_time = datetime.datetime.now().replace(hour=hours, minute=minutes, second=0)
        current_time = datetime.datetime.now()

        while current_time < alarm_time:
            current_time = datetime.datetime.now()
            time_left = alarm_time - current_time

            hours_left = time_left.seconds // 3600
            minutes_left = (time_left.seconds % 3600) // 60
            seconds_left = time_left.seconds % 60

            time_left_str = f"Осталось: {hours_left:02d}:{minutes_left:02d}:{seconds_left:02d}"
            label.config(text=time_left_str, font=("Arial", 24), fg="red")
            label.update()

        label.config(text="Время истекло!")
        #winsound.Beep(1000, 1000)
        Музон()
        button.config(text="Выход", command=root.destroy)

    except ValueError:
        label.config(text="Пожалуйста, введите цифры!", font=("Arial", 16), fg="red")

def submit():
    event_text = text_entry.get("1.0", "end-1c")
    label.config(text=f"Событие: {event_text}!")

root = tk.Tk()
root.title("Будильник")
root.geometry("300x180")

frame = tk.Frame(root)
frame.pack()

hour_label = tk.Label(frame, text="Часы:", font=("Arial", 16))
hour_label.pack(side="left")

hour_entry = tk.Entry(frame, width=4, font=("Arial", 16))
hour_entry.pack(side="left")

minute_label = tk.Label(frame, text="Минуты:", font=("Arial", 16))
minute_label.pack(side="left")

minute_entry = tk.Entry(frame, width=4, font=("Arial", 16))
minute_entry.pack(side="left")

button = tk.Button(root, text="Установить", command=set_alarm, fg="blue")
button.pack(fill=tk.X)

text_label = tk.Label(root, text="Событие:", font=("Arial", 16))
text_label.pack()

text_entry = tk.Text(root, height=2, font=("Arial", 16))
text_entry.pack(fill=tk.X)

label = tk.Label(root, text="", font=("Arial", 24), wraplength=300)
label.pack()

root.mainloop()