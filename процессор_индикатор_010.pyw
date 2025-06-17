import tkinter as tk
import psutil
import time

# Инициализация прошлых значений для диска и сети
prev_net = psutil.net_io_counters()
prev_disk = psutil.disk_io_counters()
prev_time = time.time()

# Главное окно
root = tk.Tk()
root.title("Системные индикаторы")
root.geometry("800x250+100+100")
root.attributes("-topmost", True)  # стартовать поверх всех окон

# Создание холстов для индикаторов
cpu_bar = tk.Canvas(root, height=50, bg="white", highlightthickness=0)
ram_bar = tk.Canvas(root, height=50, bg="white", highlightthickness=0)
disk_bar = tk.Canvas(root, height=50, bg="white", highlightthickness=0)
net_bar = tk.Canvas(root, height=50, bg="white", highlightthickness=0)

cpu_bar.pack(fill='x')
ram_bar.pack(fill='x')
disk_bar.pack(fill='x')
net_bar.pack(fill='x')

# Кнопка "поверх всех окон"
def update_topmost_button():
    topmost = root.attributes("-topmost")
    if topmost:
        top_btn.config(text="✔ Поверх всех", bg="#444", fg="white", activebackground="#666")
    else:
        top_btn.config(text="✘ Не поверх", bg="#ccc", fg="black", activebackground="#eee")

def toggle_topmost():
    current = root.attributes("-topmost")
    root.attributes("-topmost", not current)
    update_topmost_button()

top_btn = tk.Button(root, font=("Arial", 12), command=toggle_topmost)
top_btn.pack(fill='x')
update_topmost_button()

# Основная функция обновления всех индикаторов
def update_bars():
    global prev_net, prev_disk, prev_time

    now_time = time.time()
    dt = now_time - prev_time
    prev_time = now_time

    # CPU
    cpu = psutil.cpu_percent(interval=0.5)

    # RAM
    ram = psutil.virtual_memory().percent

    # Диск
    disk_now = psutil.disk_io_counters()
    disk_r = disk_now.read_bytes - prev_disk.read_bytes
    disk_w = disk_now.write_bytes - prev_disk.write_bytes
    prev_disk = disk_now
    disk_MBps = (disk_r + disk_w) / dt / (1024 * 1024)
    max_disk_speed = 500  # предел шкалы, МБ/с

    # Сеть
    net_now = psutil.net_io_counters()
    down = (net_now.bytes_recv - prev_net.bytes_recv) / dt / 1024
    up = (net_now.bytes_sent - prev_net.bytes_sent) / dt / 1024
    prev_net = net_now
    max_net_speed = 1000  # предел шкалы, KB/s

    # Функция отрисовки шкалы
    def draw_bar(canvas, percent, color, label):
        width = canvas.winfo_width()
        canvas.delete("bar")
        canvas.create_rectangle(0, 0, percent / 100 * width, 50, fill=color, tags="bar")
        canvas.create_text(10, 25, anchor='w', text=label, font=("Arial", 14), fill="black", tags="bar")

    draw_bar(cpu_bar, cpu, "green", f"CPU: {cpu:.1f}%")
    draw_bar(ram_bar, ram, "blue", f"RAM: {ram:.1f}%")
    disk_percent = min(disk_MBps / max_disk_speed * 100, 100)
    draw_bar(disk_bar, disk_percent, "orange", f"Disk IO: {disk_MBps:.1f} MB/s")

    # Отрисовка сетевого индикатора
    net_bar.delete("bar")
    width = net_bar.winfo_width()
    half = width // 2
    down_w = min(down / max_net_speed, 1.0) * half
    up_w = min(up / max_net_speed, 1.0) * half
    net_bar.create_rectangle(0, 0, down_w, 50, fill="purple", tags="bar")
    net_bar.create_rectangle(half, 0, half + up_w, 50, fill="red", tags="bar")
    net_bar.create_text(10, 25, anchor='w',
                        text=f"↓ {down:.1f} KB/s   ↑ {up:.1f} KB/s",
                        font=("Arial", 14), fill="black", tags="bar")

    root.after(1000, update_bars)

# Старт обновления
root.after_idle(update_bars)
root.mainloop()
