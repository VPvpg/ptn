import tkinter as tk
import time
import math
import locale

# Устанавливаем локаль для получения названий дней недели на нужном языке
locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')

class AnalogClock(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.radius = min(self.center_x, self.center_y) - 10

        # Draw the clock face
        self.create_oval(self.center_x - self.radius, self.center_y - self.radius, 
                         self.center_x + self.radius, self.center_y + self.radius, outline="black", width=2)
        self.draw_clock_face()

        # Draw hands
        self.hour_hand = self.create_line(self.center_x, self.center_y, 
                                          self.center_x, self.center_y - self.radius + 50, 
                                          width=4, fill='black')
        self.minute_hand = self.create_line(self.center_x, self.center_y, 
                                            self.center_x, self.center_y - self.radius + 20, 
                                            width=2, fill='blue')
        self.second_hand = self.create_line(self.center_x, self.center_y, 
                                            self.center_x, self.center_y - self.radius + 10, 
                                            width=1, fill='red')
        
        # Draw date and day of the week
        self.date_text = self.create_text(self.center_x, self.center_y + self.radius - 30, text="", font=("Arial", 12, "bold"))
        self.day_text = self.create_text(self.center_x, self.center_y + self.radius - 10, text="", font=("Arial", 12, "bold"))

        self.update_clock()

    def draw_clock_face(self):
        for i in range(12):
            angle = math.pi/2 - i * (2*math.pi / 12)
            x_start = self.center_x + self.radius * 0.9 * math.cos(angle)
            y_start = self.center_y - self.radius * 0.9 * math.sin(angle)
            x_end = self.center_x + self.radius * math.cos(angle)
            y_end = self.center_y - self.radius * math.sin(angle)
            self.create_line(x_start, y_start, x_end, y_end, width=2)

            # Draw hour numbers
            x_text = self.center_x + self.radius * 0.75 * math.cos(angle)
            y_text = self.center_y - self.radius * 0.75 * math.sin(angle)
            self.create_text(x_text, y_text, text=str(i if i != 0 else 12), font=("Arial", 12, "bold"))

    def update_clock(self):
        now = time.localtime()
        hours = now.tm_hour % 12
        minutes = now.tm_min
        seconds = now.tm_sec

        hour_angle = math.pi/2 - (2*math.pi * (hours + minutes/60) / 12)
        minute_angle = math.pi/2 - (2*math.pi * (minutes + seconds/60) / 60)
        second_angle = math.pi/2 - (2*math.pi * seconds / 60)

        self.coords(self.hour_hand, self.center_x, self.center_y, 
                    self.center_x + self.radius*0.5*math.cos(hour_angle), 
                    self.center_y - self.radius*0.5*math.sin(hour_angle))
        self.coords(self.minute_hand, self.center_x, self.center_y, 
                    self.center_x + self.radius*0.75*math.cos(minute_angle), 
                    self.center_y - self.radius*0.75*math.sin(minute_angle))
        self.coords(self.second_hand, self.center_x, self.center_y, 
                    self.center_x + self.radius*0.9*math.cos(second_angle), 
                    self.center_y - self.radius*0.9*math.sin(second_angle))

        # Update date and day of the week
        date_str = time.strftime("%d %B %Y", now)
        day_str = time.strftime("%A", now)
        self.itemconfig(self.date_text, text=date_str)
        self.itemconfig(self.day_text, text=day_str)

        self.after(1000, self.update_clock)

root = tk.Tk()
root.title("Analog Clock")
clock = AnalogClock(root, width=400, height=400)
clock.pack()
root.mainloop()
