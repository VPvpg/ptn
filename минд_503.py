import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QMenu, QInputDialog, QFileDialog, QAction, QMessageBox
)
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint

class MindMapNode:
    def __init__(self, id, text, x, y):
        self.id = id
        self.text = text
        self.x = x
        self.y = y
        self.children = []

class MindMapCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.connections = []
        self.selected_node = None
        self.hovered_node = None
        self.dragging = False
        self.last_mouse_pos = None
        self.setMouseTracking(True)
        self.current_filename = "mindmap_save.json"
        self.load_from_file()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        for from_id, to_id in self.connections:
            from_node = next(n for n in self.nodes if n.id == from_id)
            to_node = next(n for n in self.nodes if n.id == to_id)
            painter.drawLine(from_node.x, from_node.y, to_node.x, to_node.y)
        for node in self.nodes:
            painter.setBrush(QBrush(QColor("lightgreen") if node == self.hovered_node else QColor("lightblue")))
            painter.drawEllipse(QPoint(node.x, node.y), 50, 50)
            painter.setPen(Qt.black)
            painter.drawText(node.x - 50, node.y - 10, 100, 20, Qt.AlignCenter, node.text)

    def mousePressEvent(self, event):
        pos = event.pos()
        self.selected_node = None
        self.last_mouse_pos = pos
        if event.button() == Qt.LeftButton:
            for node in self.nodes:
                if ((node.x - pos.x()) ** 2 + (node.y - pos.y()) ** 2) <= 50 ** 2:
                    self.selected_node = node
                    break
        elif event.button() == Qt.RightButton:
            for node in self.nodes:
                if ((node.x - pos.x()) ** 2 + (node.y - pos.y()) ** 2) <= 50 ** 2:
                    self.show_context_menu(node, event.pos())
                    break
            else:
                self.dragging = True

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            for node in self.nodes:
                if ((node.x - pos.x()) ** 2 + (node.y - pos.y()) ** 2) <= 50 ** 2:
                    self.edit_node(node)
                    break

    def mouseMoveEvent(self, event):
        pos = event.pos()
        self.hovered_node = None
        for node in self.nodes:
            if ((node.x - pos.x()) ** 2 + (node.y - pos.y()) ** 2) <= 50 ** 2:
                self.hovered_node = node
                break
        if self.dragging and self.last_mouse_pos:
            dx = pos.x() - self.last_mouse_pos.x()
            dy = pos.y() - self.last_mouse_pos.y()
            for node in self.nodes:
                node.x += dx
                node.y += dy
            self.last_mouse_pos = pos
        elif self.selected_node:
            self.selected_node.x = pos.x()
            self.selected_node.y = pos.y()
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.dragging = False
        if event.button() == Qt.LeftButton and self.selected_node:
            pos = event.pos()
            for node in self.nodes:
                if node != self.selected_node and ((node.x - pos.x()) ** 2 + (node.y - pos.y()) ** 2) <= 50 ** 2:
                    # Удалить старую связь
                    self.connections = [(f, t) for f, t in self.connections if t != self.selected_node.id]
                    for n in self.nodes:
                        if self.selected_node.id in n.children:
                            n.children.remove(self.selected_node.id)
                    # Добавить новую связь
                    self.connections.append((node.id, self.selected_node.id))
                    node.children.append(self.selected_node.id)
                    break
            self.save_to_file()
        self.selected_node = None
        self.update()

    def show_context_menu(self, node, pos):
        menu = QMenu(self)
        create_action = menu.addAction("Создать узел")
        edit_action = menu.addAction("Редактировать узел")
        delete_action = menu.addAction("Удалить узел")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == create_action:
            self.add_node("Новый узел", node.x + 100, node.y, parent_id=node.id)
        elif action == edit_action:
            self.edit_node(node)
        elif action == delete_action and node.id != 0:
            self.delete_node(node)
        self.save_to_file()
        self.update()

    def add_node(self, text, x=600, y=300, parent_id=0):
        if text:
            new_id = max([n.id for n in self.nodes] + [-1]) + 1
            new_node = MindMapNode(new_id, text, x, y)
            self.nodes.append(new_node)
            self.connections.append((parent_id, new_id))
            parent = next((n for n in self.nodes if n.id == parent_id), None)
            if parent:
                parent.children.append(new_id)
            self.save_to_file()
            self.update()

    def edit_node(self, node):
        text, ok = QInputDialog.getText(self, "Редактировать узел", "Введите новый текст узла:", text=node.text)
        if ok and text:
            node.text = text
            self.save_to_file()
            self.update()

    def delete_node(self, node):
        children_ids = node.children.copy()
        for child_id in children_ids:
            for n in self.nodes:
                if n.id == child_id:
                    self.delete_node(n)
                    break
        self.nodes.remove(node)
        self.connections = [(f, t) for f, t in self.connections if f != node.id and t != node.id]
        for n in self.nodes:
            if node.id in n.children:
                n.children.remove(node.id)
        self.save_to_file()
        self.update()

    def save_to_file(self, filename=None):
        if not filename:
            filename = self.current_filename
        data = {
            "nodes": [{"id": n.id, "text": n.text, "x": n.x, "y": n.y} for n in self.nodes],
            "connections": self.connections
        }
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Сохранено в {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить: {e}")

    def load_from_file(self, filename=None):
        if not filename:
            filename = self.current_filename
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.nodes = [MindMapNode(n["id"], n["text"], n["x"], n["y"]) for n in data["nodes"]]
            self.connections = data.get("connections", [])
            id_to_node = {n.id: n for n in self.nodes}
            for from_id, to_id in self.connections:
                if from_id in id_to_node:
                    id_to_node[from_id].children.append(to_id)
            self.current_filename = filename
            print(f"Загружено из {filename}")
        except FileNotFoundError:
            print("Файл не найден. Загружается дефолтная карта.")
            self.nodes = [
                MindMapNode(0, "Центральная идея", 400, 300),
                MindMapNode(1, "Узел 1", 500, 200),
                MindMapNode(2, "Узел 2", 500, 400)
            ]
            self.nodes[0].children = [1, 2]
            self.connections = [(0, 1), (0, 2)]
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить: {e}")

class MindMapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактор ментальных карт")
        self.setGeometry(100, 100, 800, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.canvas = MindMapCanvas()
        layout.addWidget(self.canvas)
        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Файл")

        save_as_action = QAction("Сохранить как...", self)
        save_as_action.triggered.connect(self.save_as)
        file_menu.addAction(save_as_action)

        load_action = QAction("Загрузить карту...", self)
        load_action.triggered.connect(self.load_map)
        file_menu.addAction(load_action)

    def save_as(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить как", "", "JSON файлы (*.json)")
        if filename:
            self.canvas.save_to_file(filename)

    def load_map(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Загрузить карту", "", "JSON файлы (*.json)")
        if filename:
            self.canvas.load_from_file(filename)
            self.canvas.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MindMapWindow()
    window.show()
    sys.exit(app.exec_())
