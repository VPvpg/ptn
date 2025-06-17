import tkinter as tk
import psutil
import time

prev_net = psutil.net_io_counters()
prev_disk = psutil.disk_io_counters()
prev_time = time.time()

root = tk.Tk()
root.title("Системные индикаторы")
root.geometry("300x300+100+100")
root.attributes("-topmost", True)
root.attributes("-alpha", 0.8)

cpu_bar = tk.Canvas(root, height=50, bg="white", highlightthickness=0)
ram_bar = tk.Canvas(root, height=50, bg="white", highlightthickness=0)
disk_bar = tk.Canvas(root, height=50, bg="white", highlightthickness=0)
net_bar = tk.Canvas(root, height=50, bg="white", highlightthickness=0)

cpu_bar.pack(fill='x')
ram_bar.pack(fill='x')
disk_bar.pack(fill='x')
net_bar.pack(fill='x')

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

def set_alpha(new_alpha):
    new_alpha = max(0.3, min(1.0, new_alpha))
    root.attributes("-alpha", new_alpha)
    alpha_label.config(text=f"Прозрачность: {new_alpha:.1f}")

def increase_alpha():
    current = root.attributes("-alpha")
    set_alpha(current + 0.1)

def decrease_alpha():
    current = root.attributes("-alpha")
    set_alpha(current - 0.1)

bottom_frame = tk.Frame(root)
bottom_frame.pack(side='bottom', fill='x', pady=5)

decrease_btn = tk.Button(bottom_frame, text="–", font=("Arial", 14), width=4, command=decrease_alpha)
decrease_btn.pack(side='left', padx=10)

alpha_label = tk.Label(bottom_frame, text=f"Прозрачность: {root.attributes('-alpha'):.1f}", font=("Arial", 12))
alpha_label.pack(side='left', padx=10)

increase_btn = tk.Button(bottom_frame, text="+", font=("Arial", 14), width=4, command=increase_alpha)
increase_btn.pack(side='left', padx=10)

def update_bars():
    global prev_net, prev_disk, prev_time

    now_time = time.time()
    dt = now_time - prev_time
    prev_time = now_time

    cpu = psutil.cpu_percent(interval=0.5)

    width = cpu_bar.winfo_width()
    cpu_bar.delete("bar")
    cpu_bar.create_rectangle(0, 0, cpu / 100 * width, 50, fill="green", tags="bar")
    cpu_bar.create_text(10, 25, anchor='w',
                        text=f"CPU: {cpu:.1f}%",
                        font=("Arial", 14), fill="black", tags="bar")

    ram = psutil.virtual_memory().percent
    width = ram_bar.winfo_width()
    ram_bar.delete("bar")
    ram_bar.create_rectangle(0, 0, ram / 100 * width, 50, fill="blue", tags="bar")
    ram_bar.create_text(10, 25, anchor='w', text=f"RAM: {ram:.1f}%", font=("Arial", 14), fill="black", tags="bar")

    disk_now = psutil.disk_io_counters()
    disk_r = disk_now.read_bytes - prev_disk.read_bytes
    disk_w = disk_now.write_bytes - prev_disk.write_bytes
    prev_disk = disk_now
    disk_MBps = (disk_r + disk_w) / dt / (1024 * 1024)
    max_disk_speed = 500
    disk_percent = min(disk_MBps / max_disk_speed * 100, 100)
    width = disk_bar.winfo_width()
    disk_bar.delete("bar")
    disk_bar.create_rectangle(0, 0, disk_percent / 100 * width, 50, fill="orange", tags="bar")
    disk_bar.create_text(10, 25, anchor='w', text=f"Disk IO: {disk_MBps:.1f} MB/s", font=("Arial", 14), fill="black", tags="bar")

    net_now = psutil.net_io_counters()
    down = (net_now.bytes_recv - prev_net.bytes_recv) / dt / 1024
    up = (net_now.bytes_sent - prev_net.bytes_sent) / dt / 1024
    prev_net = net_now
    max_net_speed = 1000
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

root.after_idle(update_bars)
root.mainloop()
