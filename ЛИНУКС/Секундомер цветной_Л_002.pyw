#!/usr/bin/env python3

import tkinter as tk
import time

class StopwatchApp:
    def __init__(self, master, bg_color):
        self.master = master
        self.master.title("Секундомер")
        self.master.configure(bg=bg_color)

        self.is_running = False
        self.start_time = None

        self.frame = tk.Frame(self.master, bg=bg_color, pady=10, bd=1, relief=tk.SUNKEN)
        self.frame.pack()

        self.time_var = tk.StringVar()
        self.time_var.set("00:00:00")

        self.time_label = tk.Label(self.frame, textvariable=self.time_var, font=("Arial", 36))
        self.time_label.pack()

        self.start_button = tk.Button(self.frame, text="Старт", font=("Arial", 18), command=self.start_stop)
        self.start_button.pack()

        self.reset_button = tk.Button(self.frame, text="Сброс", font=("Arial", 18), command=self.reset)
        self.reset_button.pack()

        self.label_entry = tk.Entry(self.frame, font=("Arial", 18))
        self.label_entry.pack()

        self._timer_id = None  # Для хранения id after

        self.update_clock()

    def update_clock(self):
        if self.is_running:
            elapsed_time = time.time() - self.start_time
            formatted_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
            self.time_var.set(formatted_time)
        # Запускаем следующий вызов update_clock через 1000 мс и сохраняем id
        self._timer_id = self.master.after(1000, self.update_clock)

    def start_stop(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="Старт")
        else:
            self.is_running = True
            self.start_button.config(text="Стоп")
            if not self.start_time:
                self.start_time = time.time()
            else:
                # Корректируем стартовое время, чтобы продолжить с текущего времени
                self.start_time = time.time() - (self.elapsed_time if hasattr(self, 'elapsed_time') else 0)

    def reset(self):
        self.is_running = False
        self.start_time = None
        self.time_var.set("00:00:00")
        self.start_button.config(text="Старт")

    def stop_timer(self):
        # Отменяем запланированный вызов update_clock
        if self._timer_id is not None:
            self.master.after_cancel(self._timer_id)
            self._timer_id = None

def on_closing():
    # Отменяем таймеры у всех приложений перед закрытием
    app1.stop_timer()
    app2.stop_timer()
    app3.stop_timer()
    root.destroy()

root = tk.Tk()

app1 = StopwatchApp(root, "white")
separator1 = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
separator1.pack(fill=tk.X, padx=5, pady=10)

app2 = StopwatchApp(root, "yellow")
separator2 = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
separator2.pack(fill=tk.X, padx=5, pady=10)

app3 = StopwatchApp(root, "green")

root.protocol("WM_DELETE_WINDOW", on_closing)  # Обработчик закрытия окна

root.mainloop()
