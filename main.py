import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.load_data()
        self.create_widgets()

    def create_widgets(self):
        # Форма добавления книги
        frame_form = ttk.LabelFrame(self.root, text="Добавить книгу")
        frame_form.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame_form, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_entry = ttk.Entry(frame_form, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame_form, text="Автор:").grid(row=1, column=0, sticky="w")
        self.author_entry = ttk.Entry(frame_form, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(frame_form, text="Жанр:").grid(row=2, column=0, sticky="w")
        self.genre_entry = ttk.Combobox(frame_form, values=[
            "Роман", "Фантастика", "Детектив", "Биография", "Поэзия", "Другое"
        ], width=27)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(frame_form, text="Страниц:").grid(row=3, column=0, sticky="w")
        self.pages_entry = ttk.Entry(frame_form, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=2)

        # Кнопка добавления
        ttk.Button(frame_form, text="Добавить книгу", command=self.add_book).grid(
            row=4, column=0, columnspan=2, pady=5
        )

        # Фильтры
        frame_filters = ttk.LabelFrame(self.root, text="Фильтры")
        frame_filters.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame_filters, text="Жанр:").grid(row=0, column=0, sticky="w")
        self.filter_genre = ttk.Combobox(frame_filters, values=["Все"] + [
            "Роман", "Фантастика", "Детектив", "Биография", "Поэзия", "Другое"
        ], width=15)
        self.filter_genre.set("Все")
        self.filter_genre.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame_filters, text="Страниц >").grid(row=0, column=2, sticky="w", padx=(20, 5))
        self.filter_pages = ttk.Combobox(frame_filters, values=["Все", "200", "300", "500"], width=8)
        self.filter_pages.set("Все")
        self.filter_pages.grid(row=0, column=3, padx=5, pady=2)

        ttk.Button(frame_filters, text="Применить фильтр", command=self.apply_filter).grid(
            row=0, column=4, padx=5
        )
        ttk.Button(frame_filters, text="Сбросить", command=self.reset_filter).grid(
            row=0, column=5, padx=5
        )

        # Таблица книг
        frame_table = ttk.Frame(self.root)
        frame_table.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        columns = ("Название", "Автор", "Жанр", "Страниц")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Кнопки сохранения/загрузки
        frame_buttons = ttk.Frame(self.root)
        frame_buttons.grid(row=3, column=0, padx=10, pady=10)

        ttk.Button(frame_buttons, text="Сохранить в JSON", command=self.save_data).pack(side="left", padx=5)
        ttk.Button(frame_buttons, text="Загрузить из JSON", command=self.load_data).pack(side="left", padx=5)

    def validate_input(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_text = self.pages_entry.get().strip()

        if not title or not author or not genre or not pages_text:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return False

        try:
            pages = int(pages_text)
            if pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
            return False

        return True, title, author, genre, pages

    def add_book(self):
        validation_result = self.validate_input()
        if not validation_result:
            return

        is_valid, title, author, genre, pages = validation_result
        book = {"title": title, "author": author, "genre": genre, "pages": pages}
        self.books.append(book)
        self.update_table()
        self.clear_form()

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.set("")
        self.pages_entry.delete(0, tk.END)

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for book in self.books:
            self.tree.insert("", "end", values=(
                book["title"], book["author"], book["genre"], book["pages"]
            ))

    def apply_filter(self):
        selected_genre = self.filter_genre.get()
        selected_pages = self.filter_pages.get()

        filtered_books = self.books

        if selected_genre != "Все":
            filtered_books = [book for book in filtered_books if book["genre"] == selected_genre

        if selected_pages != "Все":
            min_pages = int(selected_pages)
            filtered_books = [book for book in filtered_books if book["pages"] >= min_pages

        for item in self.tree.get_children():
            self.tree.delete(item)

        for book in filtered_books:
            self.tree.insert("", "end", values=(
                book["title"], book["author"], book["genre"], book["pages"]
            ))

    def reset_filter(self