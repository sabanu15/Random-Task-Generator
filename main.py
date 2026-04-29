import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

DATA_FILE = "tasks.json"

DEFAULT_TASKS = [
    {"text": "Прочитать статью", "type": "учёба"},
    {"text": "Сделать зарядку", "type": "спорт"},
    {"text": "Написать отчёт", "type": "работа"},
    {"text": "Повторить Python", "type": "учёба"},
    {"text": "Пробежка 20 минут", "type": "спорт"},
    {"text": "Ответить на письма", "type": "работа"},
]

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("650x500")

        self.tasks = DEFAULT_TASKS.copy()
        self.history = []
        self.current_filter = tk.StringVar(value="все")

        self.load_data()
        self.build_ui()
        self.refresh_history()

    def build_ui(self):
        frame_top = ttk.Frame(self.root, padding=10)
        frame_top.pack(fill="x")

        ttk.Button(frame_top, text="Сгенерировать задачу", command=self.generate_task).pack(side="left", padx=5)

        ttk.Label(frame_top, text="Фильтр:").pack(side="left", padx=(20, 5))
        filter_box = ttk.Combobox(
            frame_top,
            textvariable=self.current_filter,
            values=["все", "учёба", "спорт", "работа"],
            state="readonly",
            width=12
        )
        filter_box.pack(side="left")
        filter_box.bind("<<ComboboxSelected>>", lambda e: self.refresh_history())

        self.result_label = ttk.Label(self.root, text="Здесь будет показана случайная задача", padding=10)
        self.result_label.pack(fill="x")

        add_frame = ttk.LabelFrame(self.root, text="Добавить задачу", padding=10)
        add_frame.pack(fill="x", padx=10, pady=10)

        self.new_task_text = tk.StringVar()
        self.new_task_type = tk.StringVar(value="учёба")

        ttk.Entry(add_frame, textvariable=self.new_task_text, width=40).grid(row=0, column=0, padx=5, pady=5)
        ttk.Combobox(add_frame, textvariable=self.new_task_type, values=["учёба", "спорт", "работа"], state="readonly", width=12).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(add_frame, text="Добавить", command=self.add_task).grid(row=0, column=2, padx=5, pady=5)

        history_frame = ttk.LabelFrame(self.root, text="История", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.listbox = tk.Listbox(history_frame)
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        ttk.Button(self.root, text="Сохранить", command=self.save_data).pack(pady=5)

    def generate_task(self):
        if not self.tasks:
            messagebox.showwarning("Внимание", "Список задач пуст.")
            return

        task = random.choice(self.tasks)
        record = f"{task['text']} [{task['type']}]"
        self.result_label.config(text=record)
        self.history.append(task.copy())
        self.save_data()
        self.refresh_history()

    def add_task(self):
        text = self.new_task_text.get().strip()
        task_type = self.new_task_type.get().strip()

        if not text:
            messagebox.showerror("Ошибка", "Название задачи не может быть пустым.")
            return

        self.tasks.append({"text": text, "type": task_type})
        self.new_task_text.set("")
        self.save_data()
        messagebox.showinfo("Готово", "Задача добавлена.")

    def refresh_history(self):
        self.listbox.delete(0, tk.END)
        flt = self.current_filter.get()

        for task in self.history:
            if flt == "все" or task["type"] == flt:
                self.listbox.insert(tk.END, f"{task['text']} [{task['type']}]")

    def save_data(self):
        data = {
            "tasks": self.tasks,
            "history": self.history
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = data.get("tasks", DEFAULT_TASKS.copy())
                self.history = data.get("history", [])

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
