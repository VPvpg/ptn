import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog
import json
import os
import uuid

DEFAULT_SAVE_FILE = "mindmap_save_0.json"
NODE_MIN_WIDTH = 120
NODE_MIN_HEIGHT = 60
DEFAULT_NODE_COLOR = "lightblue"
COMMENT_COLOR = "gold"
HOVER_COLOR = "lightgreen"
SELECTED_LINE_COLOR = "red"
NODE_PADDING = 10
LINE_SPACING = 2
EDIT_WINDOW_MIN_WIDTH = 400
EDIT_WINDOW_MIN_HEIGHT = 200
COMMENT_MARK_SIZE = 10


class MindMapApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Ментальная карта с комментариями")
        self.root.state("zoomed")
        
        self.current_file = DEFAULT_SAVE_FILE
        self.update_window_title()
        self.create_menu()
        
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.nodes = []
        self.comments = []
        self.connections = []
        self.selected_node = None
        self.hovered_node = None
        self.selected_connection = None
        self.drag_start = None
        self.scale_factor = 1.0
        self.context_menu_node = None
        
        # Контекстное меню для узлов
        self.node_context_menu = tk.Menu(self.root, tearoff=0)
        self.node_context_menu.add_command(label="Создать новый узел", command=self.create_new_node)
        self.node_context_menu.add_command(label="Добавить связь", command=self.start_connection_mode)
        self.node_context_menu.add_command(label="Изменить текст", command=self.edit_selected_node_text)
        self.node_context_menu.add_command(label="Изменить цвет", command=self.change_node_color_dialog)
        
        # Подменю для работы с комментариями
        self.comment_menu = tk.Menu(self.node_context_menu, tearoff=0)
        self.comment_menu.add_command(label="Добавить комментарий", command=self.add_comment_to_node)
        self.comment_menu.add_command(label="Изменить комментарий", command=self.edit_node_comment)
        self.comment_menu.add_command(label="Показать комментарий", command=self.show_node_comment)
        self.comment_menu.add_command(label="Удалить комментарий", command=self.delete_node_comment)
        
        self.node_context_menu.add_cascade(label="Комментарий", menu=self.comment_menu)
        self.node_context_menu.add_separator()
        self.node_context_menu.add_command(label="Удалить узел", command=self.delete_selected_node)
        
        # Контекстное меню для связей
        self.connection_context_menu = tk.Menu(self.root, tearoff=0)
        self.connection_context_menu.add_command(label="Удалить связь", command=self.delete_selected_connection)
        
        self.load_data()
        self.draw_map()
        self.bind_events()
    
    def update_window_title(self):
        """Обновляет заголовок окна с указанием текущего файла"""
        base_title = "Ментальная карта с комментариями"
        if self.current_file:
            filename = os.path.basename(self.current_file)
            self.root.title(f"{base_title} - {filename}")
        else:
            self.root.title(base_title)
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Новый", command=self.new_file)
        file_menu.add_command(label="Открыть...", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Сохранить", command=self.save_data, accelerator="Ctrl+S")
        file_menu.add_command(label="Сохранить как...", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.on_close)
        
        menubar.add_cascade(label="Файл", menu=file_menu)
        self.root.config(menu=menubar)
        self.root.bind("<Control-s>", lambda event: self.save_data())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-n>", lambda event: self.new_file())
    
    def new_file(self):
        """Создает новую пустую карту"""
        if messagebox.askyesno("Новый файл", "Создать новую ментальную карту? Несохраненные изменения будут потеряны."):
            self.current_file = DEFAULT_SAVE_FILE
            self.update_window_title()
            self.nodes = []
            self.comments = []
            self.connections = []
            self.draw_map()
    
    def save_as(self):
        """Сохраняет файл с новым именем"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            initialfile="mindmap_save.json"
        )
        
        if file_path:
            self.current_file = file_path
            self.update_window_title()
            self.save_data()
            messagebox.showinfo("Сохранение", f"Файл успешно сохранен как:\n{file_path}")
    
    def open_file(self):
        """Открывает файл ментальной карты"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            initialdir=os.path.dirname(self.current_file) if self.current_file else os.getcwd()
        )
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.nodes = data.get("nodes", [])
                    self.connections = data.get("connections", [])
                    self.comments = data.get("comments", [])
                
                # Восстанавливаем переносы строк
                for node in self.nodes:
                    node["text"] = node["text"].replace('\\n', '\n')
                for comment in self.comments:
                    comment["text"] = comment["text"].replace('\\n', '\n')
                
                self.current_file = file_path
                self.update_window_title()
                self.draw_map()
                messagebox.showinfo("Открытие файла", f"Файл успешно загружен:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{str(e)}")
    
    def update_comment_menu_state(self):
        """Обновляет состояние пунктов меню комментариев"""
        if not self.context_menu_node:
            return
            
        has_comment = any(c["node_id"] == self.context_menu_node["id"] for c in self.comments)
        
        self.comment_menu.entryconfig("Изменить комментарий", state=tk.NORMAL if has_comment else tk.DISABLED)
        self.comment_menu.entryconfig("Показать комментарий", state=tk.NORMAL if has_comment else tk.DISABLED)
        self.comment_menu.entryconfig("Удалить комментарий", state=tk.NORMAL if has_comment else tk.DISABLED)
    
    def add_comment_to_node(self):
        """Добавляет комментарий к выбранному узлу"""
        if not self.context_menu_node:
            return
            
        existing_comment = next((c for c in self.comments if c["node_id"] == self.context_menu_node["id"]), None)
        
        if existing_comment:
            if not messagebox.askyesno("Комментарий существует", "У этого узла уже есть комментарий. Заменить его?"):
                return
            self.edit_comment_text(existing_comment)
            return
            
        comment_id = str(uuid.uuid4())
        
        new_comment = {
            "id": comment_id,
            "node_id": self.context_menu_node["id"],
            "text": "Новый комментарий",
            "color": COMMENT_COLOR
        }
        
        self.comments.append(new_comment)
        self.draw_map()
        self.edit_comment_text(new_comment)
        self.save_data()
    
    def edit_node_comment(self):
        """Редактирует комментарий выбранного узла"""
        if not self.context_menu_node:
            return
            
        comment = next((c for c in self.comments if c["node_id"] == self.context_menu_node["id"]), None)
        if comment:
            self.edit_comment_text(comment)
    
    def show_node_comment(self):
        """Показывает комментарий выбранного узла"""
        if not self.context_menu_node:
            return
            
        comment = next((c for c in self.comments if c["node_id"] == self.context_menu_node["id"]), None)
        if comment:
            self.show_comment(comment)
    
    def delete_node_comment(self):
        """Удаляет комментарий выбранного узла"""
        if not self.context_menu_node:
            return
            
        comment = next((c for c in self.comments if c["node_id"] == self.context_menu_node["id"]), None)
        if comment:
            if messagebox.askyesno("Удаление комментария", "Вы уверены, что хотите удалить комментарий к этому узлу?"):
                self.comments.remove(comment)
                self.draw_map()
                self.save_data()
    
    def edit_comment_text(self, comment):
        """Открывает окно редактирования комментария"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактирование комментария")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        main_frame = tk.Frame(edit_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_scroll = tk.Scrollbar(main_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_area = tk.Text(
            main_frame, 
            wrap=tk.WORD,
            yscrollcommand=text_scroll.set,
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        text_area.pack(fill=tk.BOTH, expand=True)
        text_area.insert(tk.END, comment["text"])
        
        text_scroll.config(command=text_area.yview)
        
        button_frame = tk.Frame(edit_window)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        save_button = tk.Button(
            button_frame, 
            text="Сохранить", 
            command=lambda: self.save_comment_text(comment, text_area.get("1.0", tk.END).strip(), edit_window),
            width=10
        )
        save_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = tk.Button(
            button_frame, 
            text="Отмена", 
            command=edit_window.destroy,
            width=10
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
        
        self.adjust_edit_window_size(edit_window, text_area)
        text_area.bind("<KeyRelease>", lambda e: self.adjust_edit_window_size(edit_window, text_area))
        text_area.focus_set()
        self.center_window(edit_window)
    
    def show_comment(self, comment):
        """Показывает комментарий в отдельном окне"""
        view_window = tk.Toplevel(self.root)
        view_window.title("Комментарий к узлу")
        
        text_frame = tk.Frame(view_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_scroll = tk.Scrollbar(text_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_area = tk.Text(
            text_frame, 
            wrap=tk.WORD,
            yscrollcommand=text_scroll.set,
            font=("Arial", 12),
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        text_area.pack(fill=tk.BOTH, expand=True)
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, comment["text"])
        text_area.config(state=tk.DISABLED)
        
        text_scroll.config(command=text_area.yview)
        
        button_frame = tk.Frame(view_window)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        edit_button = tk.Button(
            button_frame, 
            text="Редактировать", 
            command=lambda: [view_window.destroy(), self.edit_comment_text(comment)],
            width=10
        )
        edit_button.pack(side=tk.LEFT, padx=5)
        
        close_button = tk.Button(
            button_frame, 
            text="Закрыть", 
            command=view_window.destroy,
            width=10
        )
        close_button.pack(side=tk.RIGHT, padx=5)
        
        self.center_window(view_window)
    
    def save_comment_text(self, comment, text, window):
        """Сохраняет текст комментария"""
        comment["text"] = text
        window.destroy()
        self.draw_map()
        self.save_data()
    
    def change_node_color_dialog(self):
        """Открывает диалог выбора цвета для узла"""
        if not self.context_menu_node:
            return
            
        current_color = self.context_menu_node.get("color", DEFAULT_NODE_COLOR)
        
        color = colorchooser.askcolor(
            title="Выберите цвет узла",
            initialcolor=current_color
        )
        
        if color[1]:
            self.change_node_color(self.context_menu_node, color[1])
    
    def change_node_color(self, node, color):
        """Изменяет цвет указанного узла"""
        node["color"] = color
        self.draw_map()
        self.save_data()
    
    def create_new_node(self):
        """Создает новый узел, связанный с текущим"""
        if not self.context_menu_node:
            return
            
        new_id = str(uuid.uuid4())
        
        new_node = {
            "id": new_id,
            "text": "Новый узел",
            "x": self.context_menu_node["x"] + 150,
            "y": self.context_menu_node["y"],
            "color": DEFAULT_NODE_COLOR
        }
        
        self.nodes.append(new_node)
        
        new_connection = {
            "from": self.context_menu_node["id"],
            "to": new_id
        }
        
        self.connections.append(new_connection)
        self.draw_map()
        self.edit_node_text(new_node)
    
    def bind_events(self):
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_hover)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)
        self.canvas.bind("<Button-3>", self.show_context_menu)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
    
    def show_context_menu(self, event):
        """Показывает контекстное меню по ПКМ"""
        self.selected_connection = self.get_connection_at(event.x, event.y)
        
        if self.selected_connection:
            try:
                self.connection_context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.connection_context_menu.grab_release()
            return
        
        node = self.get_node_at(event.x, event.y)
        self.context_menu_node = node
        
        if node:
            self.selected_node = node
            self.update_comment_menu_state()
            try:
                self.node_context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.node_context_menu.grab_release()
    
    def get_connection_at(self, x, y):
        """Находит связь рядом с указанными координатами"""
        for conn in self.connections:
            from_node = next((n for n in self.nodes if n["id"] == conn["from"]), None)
            to_node = next((n for n in self.nodes if n["id"] == conn["to"]), None)
            
            if from_node and to_node:
                x1, y1 = self.get_connection_point(from_node, to_node)
                x2, y2 = self.get_connection_point(to_node, from_node)
                
                if self.point_near_line(x, y, x1, y1, x2, y2, threshold=5):
                    return conn
        return None
    
    def point_near_line(self, px, py, x1, y1, x2, y2, threshold):
        """Проверяет, находится ли точка рядом с линией"""
        numerator = abs((y2 - y1) * px - (x2 - x1) * py + x2*y1 - x1*y2)
        denominator = ((y2 - y1)**2 + (x2 - x1)**2)**0.5
        
        if denominator == 0:
            return False
            
        distance = numerator / denominator
        
        dot_product = (px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)
        squared_length = (x2 - x1)**2 + (y2 - y1)**2
        
        if dot_product < 0 or dot_product > squared_length:
            return False
            
        return distance <= threshold
    
    def delete_selected_connection(self):
        """Удаляет выбранную связь"""
        if self.selected_connection:
            self.connections.remove(self.selected_connection)
            self.selected_connection = None
            self.draw_map()
            self.save_data()
    
    def start_connection_mode(self):
        """Режим создания связи между узлами"""
        if not self.context_menu_node:
            return
            
        messagebox.showinfo("Создание связи", "Кликните ЛКМ на узел, с которым нужно создать связь")
        self.canvas.bind("<Button-1>", self.finish_connection)
    
    def finish_connection(self, event):
        """Завершает создание связи"""
        target_node = self.get_node_at(event.x, event.y)
        
        if target_node and self.context_menu_node and target_node != self.context_menu_node:
            new_conn = {"from": self.context_menu_node["id"], "to": target_node["id"]}
            reverse_conn = {"from": target_node["id"], "to": self.context_menu_node["id"]}
            
            if new_conn not in self.connections and reverse_conn not in self.connections:
                self.connections.append(new_conn)
                self.draw_map()
                self.save_data()
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.context_menu_node = None
    
    def edit_selected_node_text(self):
        """Редактирование текста выбранного узла"""
        if self.context_menu_node:
            self.edit_node_text(self.context_menu_node)
    
    def delete_selected_node(self):
        """Удаление выбранного узла"""
        if not self.context_menu_node:
            return
            
        if messagebox.askyesno(
            "Удаление узла",
            f"Вы уверены, что хотите удалить узел '{self.context_menu_node['text']}'? "
            "Все связанные связи и комментарии также будут удалены."
        ):
            node_id = self.context_menu_node["id"]
            self.nodes = [n for n in self.nodes if n["id"] != node_id]
            self.connections = [
                conn for conn in self.connections 
                if conn["from"] != node_id and conn["to"] != node_id
            ]
            self.comments = [c for c in self.comments if c["node_id"] != node_id]
            self.draw_map()
            self.context_menu_node = None
            self.save_data()
    
    def load_data(self):
        """Загружает данные из текущего файла"""
        if os.path.exists(self.current_file):
            try:
                with open(self.current_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.nodes = data.get("nodes", [])
                    self.connections = data.get("connections", [])
                    self.comments = data.get("comments", [])
                
                # Восстанавливаем переносы строк
                for node in self.nodes:
                    if "text" in node:
                        node["text"] = node["text"].replace('\\n', '\n')
                for comment in self.comments:
                    if "text" in comment:
                        comment["text"] = comment["text"].replace('\\n', '\n')
                        
            except Exception as e:
                print(f"Ошибка загрузки файла: {e}")
                self.create_sample_nodes()
        else:
            self.create_sample_nodes()
    
    def create_sample_nodes(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        central_node = {
            "id": str(uuid.uuid4()), 
            "text": "Центральный узел\n(ПКМ для меню)", 
            "x": screen_width//2, 
            "y": screen_height//2, 
            "color": DEFAULT_NODE_COLOR
        }
        
        self.nodes = [
            central_node,
            {"id": str(uuid.uuid4()), "text": "Идея 1", "x": screen_width//3, "y": screen_height//3, "color": DEFAULT_NODE_COLOR},
            {"id": str(uuid.uuid4()), "text": "Идея 2", "x": 2*screen_width//3, "y": screen_height//3, "color": DEFAULT_NODE_COLOR}
        ]
        
        self.connections = [
            {"from": central_node["id"], "to": self.nodes[1]["id"]},
            {"from": central_node["id"], "to": self.nodes[2]["id"]}
        ]
        
        # Пример комментария для центрального узла
        self.comments = [
            {
                "id": str(uuid.uuid4()),
                "node_id": central_node["id"],
                "text": "Это пример комментария к центральному узлу",
                "color": COMMENT_COLOR
            }
        ]
    
    def calculate_text_dimensions(self, text, font):
        lines = text.split('\n')
        max_line_width = 0
        total_height = 0
        
        temp_canvas = tk.Canvas(self.root)
        temp_text_id = temp_canvas.create_text(0, 0, text="", font=font, anchor="nw")
        
        for line in lines:
            temp_canvas.itemconfigure(temp_text_id, text=line)
            line_width = temp_canvas.bbox(temp_text_id)[2]
            
            temp_canvas.itemconfigure(temp_text_id, text="Hg")
            line_height = temp_canvas.bbox(temp_text_id)[3]
            
            if line_width > max_line_width:
                max_line_width = line_width
            total_height += line_height + LINE_SPACING
        
        temp_canvas.destroy()
        return max_line_width, total_height
    
    def draw_map(self):
        self.canvas.delete("all")
        
        # Рисуем связи
        for conn in self.connections:
            from_node = next((n for n in self.nodes if n["id"] == conn["from"]), None)
            to_node = next((n for n in self.nodes if n["id"] == conn["to"]), None)
            
            if from_node and to_node:
                x1, y1 = self.get_connection_point(from_node, to_node)
                x2, y2 = self.get_connection_point(to_node, from_node)
                
                line_color = SELECTED_LINE_COLOR if conn == self.selected_connection else "gray"
                
                self.canvas.create_line(
                    x1, y1, x2, y2,
                    width=2 * self.scale_factor,
                    fill=line_color, 
                    arrow=tk.LAST,
                    smooth=True,
                    tags="connection"
                )
        
        # Рисуем узлы
        for node in self.nodes:
            fill_color = HOVER_COLOR if node == self.hovered_node else node.get("color", DEFAULT_NODE_COLOR)
            
            font_size = int(10 * self.scale_factor)
            font = ("Arial", font_size)
            text = node["text"]
            
            text_width, text_height = self.calculate_text_dimensions(text, font)
            node_width = max(NODE_MIN_WIDTH * self.scale_factor, text_width + 2*NODE_PADDING)
            node_height = max(NODE_MIN_HEIGHT * self.scale_factor, text_height + 2*NODE_PADDING)
            
            node["width"] = node_width
            node["height"] = node_height
            
            # Рисуем прямоугольник узла
            self.canvas.create_rectangle(
                node["x"] - node_width/2,
                node["y"] - node_height/2,
                node["x"] + node_width/2,
                node["y"] + node_height/2,
                fill=fill_color,
                outline="black",
                width=2 * self.scale_factor,
                tags="node"
            )
            
            # Рисуем текст узла
            lines = text.split('\n')
            temp_text = self.canvas.create_text(0, 0, text="Hg", font=font, anchor="nw")
            line_height = self.canvas.bbox(temp_text)[3] + LINE_SPACING
            self.canvas.delete(temp_text)
            
            y_offset = node["y"] - (len(lines) * line_height)/2 + line_height/2
            
            for line in lines:
                self.canvas.create_text(
                    node["x"],
                    y_offset,
                    text=line,
                    font=font,
                    tags="node",
                    width=node_width - 2*NODE_PADDING
                )
                y_offset += line_height
            
            # Рисуем отметку о наличии комментариев
            if any(c["node_id"] == node["id"] for c in self.comments):
                mark_size = COMMENT_MARK_SIZE * self.scale_factor
                self.canvas.create_oval(
                    node["x"] + node_width/2 - mark_size,
                    node["y"] - node_height/2,
                    node["x"] + node_width/2,
                    node["y"] - node_height/2 + mark_size,
                    fill=COMMENT_COLOR,
                    outline="black",
                    width=1
                )
    
    def get_connection_point(self, from_node, to_node):
        dx = to_node["x"] - from_node["x"]
        dy = to_node["y"] - from_node["y"]
        
        length = (dx**2 + dy**2)**0.5
        if length == 0:
            return from_node["x"], from_node["y"]
        
        dx /= length
        dy /= length
        
        node_width = from_node.get("width", NODE_MIN_WIDTH * self.scale_factor)
        node_height = from_node.get("height", NODE_MIN_HEIGHT * self.scale_factor)
        
        x = from_node["x"] + dx * node_width/2
        y = from_node["y"] + dy * node_height/2
        
        return x, y
    
    def get_node_at(self, x, y):
        for node in self.nodes:
            node_width = node.get("width", NODE_MIN_WIDTH * self.scale_factor)
            node_height = node.get("height", NODE_MIN_HEIGHT * self.scale_factor)
            
            if (node["x"] - node_width/2 <= x <= node["x"] + node_width/2 and
                node["y"] - node_height/2 <= y <= node["y"] + node_height/2):
                return node
        return None
    
    def on_click(self, event):
        self.selected_connection = self.get_connection_at(event.x, event.y)
        
        if self.selected_connection:
            self.draw_map()
            return
        
        self.selected_node = self.get_node_at(event.x, event.y)
        self.drag_start = (event.x, event.y)
    
    def on_drag(self, event):
        if self.selected_node:
            # Непосредственно устанавливаем координаты узла в позицию курсора
            self.selected_node["x"] = event.x
            self.selected_node["y"] = event.y
            self.draw_map()
        elif self.drag_start:
            dx = event.x - self.drag_start[0]
            dy = event.y - self.drag_start[1]
            for node in self.nodes:
                node["x"] += dx
                node["y"] += dy
            self.drag_start = (event.x, event.y)
            self.draw_map()
    
    def on_release(self, event):
        if self.selected_node and self.drag_start:
            target_node = self.get_node_at(event.x, event.y)
            
            # Если перетащили узел на другой узел (и это не тот же самый узел)
            if target_node and target_node != self.selected_node:
                # Удаляем все связи, где текущий узел был источником или целью
                self.connections = [
                    conn for conn in self.connections 
                    if conn["from"] != self.selected_node["id"] and conn["to"] != self.selected_node["id"]
                ]
                
                # Создаем новую связь между целевым узлом и перетащенным узлом
                new_connection = {
                    "from": target_node["id"],
                    "to": self.selected_node["id"]
                }
                
                # Проверяем, что такая связь еще не существует
                reverse_connection = {"from": self.selected_node["id"], "to": target_node["id"]}
                if new_connection not in self.connections and reverse_connection not in self.connections:
                    self.connections.append(new_connection)
                
                # Сохраняем новое положение узла
                self.selected_node["x"] = event.x
                self.selected_node["y"] = event.y
                
            self.draw_map()
            self.save_data()
        
        self.drag_start = None
        self.selected_node = None
    
    def on_hover(self, event):
        self.hovered_node = self.get_node_at(event.x, event.y)
        self.draw_map()
    
    def on_double_click(self, event):
        clicked_node = self.get_node_at(event.x, event.y)
        if clicked_node:
            self.edit_node_text(clicked_node)
    
    def edit_node_text(self, node):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактирование узла")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        main_frame = tk.Frame(edit_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_scroll = tk.Scrollbar(main_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_area = tk.Text(
            main_frame, 
            wrap=tk.WORD,
            yscrollcommand=text_scroll.set,
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.insert(tk.END, node["text"])
        
        text_scroll.config(command=self.text_area.yview)
        
        button_frame = tk.Frame(edit_window)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        save_button = tk.Button(
            button_frame, 
            text="Сохранить", 
            command=lambda: self.save_node_text(node, edit_window),
            width=10
        )
        save_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = tk.Button(
            button_frame, 
            text="Отмена", 
            command=edit_window.destroy,
            width=10
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
        
        self.adjust_edit_window_size(edit_window, self.text_area)
        self.text_area.bind("<KeyRelease>", lambda e: self.adjust_edit_window_size(edit_window, self.text_area))
        self.text_area.focus_set()
        self.center_window(edit_window)
    
    def adjust_edit_window_size(self, window, text_area):
        window.update_idletasks()
        lines = text_area.get("1.0", "end-1c").split('\n')
        font = tk.font.Font(font=text_area['font'])
        
        max_line_width = max(font.measure(line) for line in lines) if lines else 0
        total_lines = len(lines)
        
        new_width = max(EDIT_WINDOW_MIN_WIDTH, min(800, max_line_width + 100))
        new_height = max(EDIT_WINDOW_MIN_HEIGHT, min(600, total_lines * font.metrics("linespace") + 100))
        
        window.geometry(f"{new_width}x{new_height}")
        text_area.see("end")
    
    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'+{x}+{y}')
    
    def save_node_text(self, node, window):
        node["text"] = self.text_area.get("1.0", tk.END).strip()
        window.destroy()
        self.draw_map()
        self.save_data()
    
    def on_mousewheel(self, event):
        scale_direction = 1 if event.delta > 0 else -1
        scale_factor_change = 0.1 * scale_direction
        new_scale = self.scale_factor + scale_factor_change
        if 0.5 <= new_scale <= 3.0:
            self.scale_factor = new_scale
            self.draw_map()
    
    def save_data(self):
        """Сохраняет данные в текущий файл в удобочитаемом формате"""
        try:
            data = {
                "_comment": "Файл ментальной карты (можно редактировать вручную)",
                "nodes": [
                    {
                        "id": node["id"],
                        "text": node["text"].replace('\n', '\\n'),  # Экранируем переносы строк
                        "x": node["x"],
                        "y": node["y"],
                        "color": node.get("color", DEFAULT_NODE_COLOR)
                    } 
                    for node in self.nodes
                ],
                "connections": [
                    {"from": conn["from"], "to": conn["to"]} 
                    for conn in self.connections
                ],
                "comments": [
                    {
                        "id": comment["id"],
                        "node_id": comment["node_id"],
                        "text": comment["text"].replace('\n', '\\n'),  # Экранируем переносы
                        "color": comment.get("color", COMMENT_COLOR)
                    }
                    for comment in self.comments
                ]
            }

            with open(self.current_file, "w", encoding="utf-8") as f:
                json.dump(
                    data,
                    f,
                    ensure_ascii=False,  # Сохраняем кириллицу как есть
                    indent=2,           # Читаемые отступы
                    separators=(", ", ": "),  # Убираем лишние пробелы
                )
                f.write("\n")  # Перенос строки в конце файла

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")
    
    def on_close(self):
        self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MindMapApp(root)
    root.mainloop()