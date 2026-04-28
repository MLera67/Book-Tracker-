import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

DATA_FILE = "books.json"


class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Трекер прочитанных книг")
        self.root.geometry("800x500")

        self.books = []
        self.load_books()

        # --- Поля ввода ---
        tk.Label(root, text="Название:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.title_entry = tk.Entry(root, width=40)
        self.title_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        tk.Label(root, text="Автор:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.author_entry = tk.Entry(root, width=40)
        self.author_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        tk.Label(root, text="Жанр:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.genre_entry = tk.Entry(root, width=40)
        self.genre_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        tk.Label(root, text="Страниц:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.pages_entry = tk.Entry(root, width=10)
        self.pages_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # --- Кнопки ---
        self.add_btn = tk.Button(root, text="Добавить книгу", command=self.add_book)
        self.add_btn.grid(row=4, column=1, pady=10)

        # --- Таблица ---
        self.columns = ("Название", "Автор", "Жанр", "Страниц")
        self.tree = ttk.Treeview(root, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=180)
        self.tree.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

        # --- Фильтры ---
        self.filter_genre = tk.StringVar()
        self.filter_pages = tk.IntVar()

        ttk.Combobox(root, textvariable=self.filter_genre,
                     values=["Все"] + sorted(set(b["genre"] for b in self.books)),
                     state="readonly").grid(row=6, column=0, padx=5)

        tk.Entry(root, textvariable=self.filter_pages).grid(row=6, column=1, padx=5)

        tk.Button(root, text="Фильтровать", command=self.apply_filter).grid(row=6, column=2)

        # Привязки
        self.filter_genre.trace_add("write", lambda *args: self.apply_filter())

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_str = self.pages_entry.get().strip()

        if not title or not author or not genre or not pages_str:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
            return

        try:
            pages = int(pages_str)
            if pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
            return

        book = {"title": title, "author": author, "genre": genre, "pages": pages}
        self.books.append(book)
        self.update_tree()
        self.save_books()

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        filtered_books = self.books.copy()

        genre = self.filter_genre.get()
        if genre and genre != "Все":
            filtered_books = [b for b in filtered_books if b["genre"] == genre]

        try:
            pages_val = self.filter_pages.get()
            filtered_books = [b for b in filtered_books if b["pages"] > pages_val]
        except tk.TclError:
            pass

        for book in filtered_books:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

    def apply_filter(self):
        self.update_tree()

    def save_books(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_books(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.books = json.load(f)


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    app.update_tree()  # Загрузка данных при старте
    root.mainloop()