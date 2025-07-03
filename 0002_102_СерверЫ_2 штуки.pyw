import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import threading
import socket
import os
import pyperclip

# Импортируем компоненты pyftpdlib
try:
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib.servers import FTPServer
    import logging
    PYFTPDLIB_INSTALLED = True
except ImportError:
    PYFTPDLIB_INSTALLED = False
    logging = None

class HttpServerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Простой HTTP и FTP сервер")

        # Переменные для HTTP сервера
        self.http_port = tk.StringVar(value="8000")
        self.http_directory = tk.StringVar(value=os.getcwd())
        self.http_status = tk.StringVar(value="Остановлен")
        self.http_process = None
        
        # Переменные для FTP сервера
        self.ftp_port = tk.StringVar(value="2121")
        self.ftp_status = tk.StringVar(value="Остановлен")
        self.ftp_server_instance = None
        self.ftp_thread = None

        self.ip_address = self.get_local_ip()
        self.http_server_address = tk.StringVar(value=f"http://{self.ip_address}:{self.http_port.get()}")
        self.ftp_server_address = tk.StringVar(value=f"ftp://{self.ip_address}:{self.ftp_port.get()}")

        # Переменные для статуса установки библиотек
        self.pyftpdlib_status = tk.StringVar()
        self.pyperclip_status = tk.StringVar()

        self.create_widgets()
        self.check_dependencies()

        if PYFTPDLIB_INSTALLED:
            logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    def create_widgets(self):
        # --- Секция HTTP сервера ---
        http_frame = ttk.LabelFrame(self.master, text="HTTP Сервер")
        http_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        ttk.Label(http_frame, text="Порт:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.http_port_entry = ttk.Entry(http_frame, textvariable=self.http_port, validate="key", validatecommand=(self.master.register(self.validate_port), '%P'))
        self.http_port_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.http_port_entry.bind("<FocusOut>", self.update_http_server_address)

        ttk.Label(http_frame, text="Каталог:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.http_directory_entry = ttk.Entry(http_frame, textvariable=self.http_directory)
        self.http_directory_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.browse_http_button = ttk.Button(http_frame, text="Выбрать папку", command=self.browse_http_directory)
        self.browse_http_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        self.start_http_button = ttk.Button(http_frame, text="Запустить HTTP", command=self.start_http_server)
        self.start_http_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.stop_http_button = ttk.Button(http_frame, text="Остановить HTTP", command=self.stop_http_server, state="disabled")
        self.stop_http_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(http_frame, text="Статус:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.http_status_label = ttk.Label(http_frame, textvariable=self.http_status)
        self.http_status_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(http_frame, text="Адрес HTTP:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.http_address_label = ttk.Label(http_frame, textvariable=self.http_server_address)
        self.http_address_label.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.copy_http_button = ttk.Button(http_frame, text="Копировать HTTP адрес", command=self.copy_http_address)
        self.copy_http_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        http_frame.grid_columnconfigure(1, weight=1)

        # --- Секция FTP сервера ---
        ftp_frame = ttk.LabelFrame(self.master, text="FTP Сервер")
        ftp_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        ttk.Label(ftp_frame, text="Порт:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ftp_port_entry = ttk.Entry(ftp_frame, textvariable=self.ftp_port, validate="key", validatecommand=(self.master.register(self.validate_port), '%P'))
        self.ftp_port_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.ftp_port_entry.bind("<FocusOut>", self.update_ftp_server_address)

        self.start_ftp_button = ttk.Button(ftp_frame, text="Запустить FTP", command=self.start_ftp_server)
        self.start_ftp_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.stop_ftp_button = ttk.Button(ftp_frame, text="Остановить FTP", command=self.stop_ftp_server, state="disabled")
        self.stop_ftp_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(ftp_frame, text="Статус:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.ftp_status_label = ttk.Label(ftp_frame, textvariable=self.ftp_status)
        self.ftp_status_label.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(ftp_frame, text="Адрес FTP:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.ftp_address_label = ttk.Label(ftp_frame, textvariable=self.ftp_server_address)
        self.ftp_address_label.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.copy_ftp_button = ttk.Button(ftp_frame, text="Копировать FTP адрес", command=self.copy_ftp_address)
        self.copy_ftp_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        ftp_frame.grid_columnconfigure(1, weight=1)

        # --- Общая информация ---
        info_frame = ttk.LabelFrame(self.master, text="Информация")
        info_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        ttk.Label(info_frame, text="Ваш IP-адрес:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ip_label = ttk.Label(info_frame, text=self.ip_address)
        self.ip_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(info_frame, text="pyftpdlib:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.pyftpdlib_status_label = ttk.Label(info_frame, textvariable=self.pyftpdlib_status)
        self.pyftpdlib_status_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(info_frame, text="pyperclip:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.pyperclip_status_label = ttk.Label(info_frame, textvariable=self.pyperclip_status)
        self.pyperclip_status_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        info_frame.grid_columnconfigure(1, weight=1)

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=0)

    # --- Методы HTTP сервера ---
    def start_http_server(self):
        port = self.http_port.get()
        directory = self.http_directory.get()

        try:
            port = int(port)
            if not 1 <= port <= 65535:
                raise ValueError("Порт должен быть в диапазоне от 1 до 65535.")
        except ValueError as e:
            self.http_status.set(f"Ошибка: {e}")
            return

        if not os.path.isdir(directory):
            self.http_status.set("Ошибка: Некорректный каталог.")
            return

        # Запуск HTTP-сервера без консольного окна
        command = ["python", "-m", "http.server", str(port)]
        if os.name == 'nt':  # Для Windows
            self.http_process = subprocess.Popen(
                command, 
                cwd=directory, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:  # Для других ОС
            self.http_process = subprocess.Popen(
                command, 
                cwd=directory, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
        
        self.http_status.set("Запущен")
        self.start_http_button["state"] = "disabled"
        self.stop_http_button["state"] = "normal"

        threading.Thread(target=self.read_http_output, daemon=True).start()

    def stop_http_server(self):
        if self.http_process:
            self.http_process.terminate()
            self.http_process.wait()
            self.http_status.set("Остановлен")
            self.start_http_button["state"] = "normal"
            self.stop_http_button["state"] = "disabled"

    def read_http_output(self):
        while True:
            if self.http_process:
                line = self.http_process.stdout.readline()
                if line:
                    print(f"[HTTP] {line.decode().strip()}")
                else:
                    break
            else:
                break

    def browse_http_directory(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.http_directory.set(folder_selected)

    def update_http_server_address(self, event=None):
        self.http_server_address.set(f"http://{self.ip_address}:{self.http_port.get()}")

    def copy_http_address(self):
        pyperclip.copy(self.http_server_address.get())
        print("HTTP адрес скопирован в буфер обмена.")

    # --- Методы FTP сервера ---
    def start_ftp_server(self):
        if not PYFTPDLIB_INSTALLED:
            self.ftp_status.set("Ошибка: pyftpdlib не установлен.")
            return

        port = self.ftp_port.get()
        directory = self.http_directory.get()

        try:
            port = int(port)
            if not 1 <= port <= 65535:
                raise ValueError("Порт должен быть в диапазоне от 1 до 65535.")
        except ValueError as e:
            self.ftp_status.set(f"Ошибка: {e}")
            return

        if not os.path.isdir(directory):
            self.ftp_status.set("Ошибка: Некорректный каталог.")
            return

        authorizer = DummyAuthorizer()
        authorizer.add_anonymous(directory, perm='elr')

        handler = FTPHandler
        handler.authorizer = authorizer
        handler.banner = "pyftpdlib based ftpd ready."

        address = ('', port)
        self.ftp_server_instance = FTPServer(address, handler)

        self.ftp_thread = threading.Thread(target=self.run_ftp_server, daemon=True)
        self.ftp_thread.start()

        self.ftp_status.set("Запущен")
        self.start_ftp_button["state"] = "disabled"
        self.stop_ftp_button["state"] = "normal"

    def run_ftp_server(self):
        try:
            self.ftp_server_instance.serve_forever()
        except Exception as e:
            self.master.after(0, lambda: self.ftp_status.set(f"Ошибка FTP: {e}"))
        finally:
            self.master.after(0, self.stop_ftp_server)

    def stop_ftp_server(self):
        if self.ftp_server_instance:
            self.ftp_server_instance.close_all()
            self.ftp_server_instance = None
            self.ftp_status.set("Остановлен")
            self.start_ftp_button["state"] = "normal"
            self.stop_ftp_button["state"] = "disabled"

    def update_ftp_server_address(self, event=None):
        self.ftp_server_address.set(f"ftp://{self.ip_address}:{self.ftp_port.get()}")

    def copy_ftp_address(self):
        try:
            pyperclip.copy(self.ftp_server_address.get())
            print("FTP адрес скопирован в буфер обмена.")
        except NameError:
            print("Ошибка: pyperclip не установлен. Невозможно скопировать адрес.")

    # --- Общие методы ---
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except Exception:
            return "Невозможно определить"

    def validate_port(self, new_value):
        if not new_value:
            return True
        try:
            port = int(new_value)
            return 1 <= port <= 65535
        except ValueError:
            return False

    def check_dependencies(self):
        if PYFTPDLIB_INSTALLED:
            self.pyftpdlib_status.set("Установлен")
            self.pyftpdlib_status_label.config(foreground="green")
        else:
            self.pyftpdlib_status.set("Не установлен (pip install pyftpdlib)")
            self.pyftpdlib_status_label.config(foreground="red")
            self.start_ftp_button["state"] = "disabled"

        try:
            import pyperclip
            self.pyperclip_status.set("Установлен")
            self.pyperclip_status_label.config(foreground="green")
        except ImportError:
            self.pyperclip_status.set("Не установлен (pip install pyperclip)")
            self.pyperclip_status_label.config(foreground="red")
            self.copy_http_button["state"] = "disabled"
            self.copy_ftp_button["state"] = "disabled"

root = tk.Tk()
app = HttpServerGUI(root)
root.mainloop()