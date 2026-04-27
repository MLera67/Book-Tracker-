Разберу задачу пошагово — вот полная инструкция по созданию Book Tracker.

## Шаг 1. Подготовка окружения

**Требования:**
* Python 3.6+;
* библиотека Tkinter (обычно идёт в комплекте с Python);
* Git для контроля версий.

**Создайте структуру проекта:**
```
bookTracker/
├── main.py          # Основной файл приложения
├── README.md        # Документация проекта
├── .gitignore       # Файл игнорирования для Git
└── books_data.json  # Файл данных (создаётся автоматически)
```

## Шаг 2. Создание GUI-формы

Код для формы с полями и кнопкой «Добавить книгу»:

```python
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

        # Создаём виджеты формы
        tk.Label(root, text="Название книги:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Автор:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.author_entry = tk.Entry(root, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.genre_var = tk.StringVar()
        self.genre_combo = ttk.Combobox(root, textvariable=self.genre_var,
                                      values=["Роман", "Фантастика", "Детектив", "Биография", "Поэзия", "Другое"])
        self.genre_combo.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Количество страниц:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.pages_entry = tk.Entry(root, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления книги
        tk.Button(root, text="Добавить книгу", command=self.add_book).grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица для отображения книг
        self.tree = ttk.Treeview(root, columns=("Title", "Author", "Genre", "Pages"), show="headings")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страниц")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры
        tk.Label(root, text="Фильтр по жанру:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.filter_genre_var = tk.StringVar()
        self.filter_genre_combo = ttk.Combobox(root, textvariable=self.filter_genre_var,
                                          values=["Все", "Роман", "Фантастика", "Детектив", "Биография", "Поэзия", "Другое"])
        self.filter_genre_combo.set("Все")
        self.filter_genre_combo.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(root, text="Фильтр по страницам:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.filter_pages_var = tk.StringVar()
        self.filter_pages_combo = ttk.Combobox(root, textvariable=self.filter_pages_var,
                                  values=["Все", ">100", ">200", ">300", ">500"])
        self.filter_pages_combo.set("Все")
        self.filter_pages_combo.grid(row=7, column=1, padx=5, pady=5)

        # Кнопки фильтров
        tk.Button(root, text="Применить фильтр", command=self.apply_filter).grid(row=8, column=0, pady=10)
        tk.Button(root, text="Сбросить фильтр", command=self.reset_filter).grid(row=8, column=1, pady=10)

        # Кнопки сохранения и загрузки
        tk.Button(root, text="Сохранить в JSON", command=self.save_data).grid(row=9, column=0, pady=10)
        tk.Button(root, text="Загрузить из JSON", command=self.load_data).grid(row=9, column=1, pady=10)

        self.update_table()
```

## Шаг 3. Реализация добавления книг

Метод для добавления книги с валидацией данных:

```python
    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_var.get().strip()
        pages_text = self.pages_entry.get().strip()

        # Валидация данных
        if not title or not author or not genre or not pages_text:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            pages = int(pages_text)
            if pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
            return

        # Добавляем книгу в список
        book = {"title": title, "author": author, "genre": genre, "pages": pages}
        self.books.append(book)

        # Очищаем поля формы
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_combo.set("")
        self.pages_entry.delete(0, tk.END)

        # Обновляем таблицу
        self.update_table()
```

## Шаг 4. Реализация фильтрации

Методы для фильтрации и сброса фильтров:

```python
    def apply_filter(self):
        filtered_books = self.books

        # Фильтр по жанру
        selected_genre = self.filter_genre_var.get()
        if selected_genre != "Все":
            filtered_books = [book for book in filtered_books if book["genre"] == selected_genre

        # Фильтр по страницам
        selected_pages = self.filter_pages_var.get()
        if selected_pages != "Все":
            min_pages = int(selected_pages[1:])  # Убираем символ > и преобразуем в число
            filtered_books = [book for book in filtered_books if book["pages"] >= min_pages

        # Обновляем таблицу с отфильтрованными данными
        self.update_table(filtered_books)

    def reset_filter(self):
        # Сбрасываем фильтры и показываем все книги
        self.filter_genre_combo.set("Все")
        self.filter_pages_combo.set("Все")
        self.update_table()
```

## Шаг 5. Сохранение и загрузка данных в JSON

Методы для работы с JSON-файлом:

```python
    def save_data(self):
        with open("books_data.json", "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены в books_data.json")

    def load_data(self):
        if os.path.exists("books_data.json"):
            with open("books_data.json", "r", encoding="utf-8") as f:
                self.books = json.load(f)
            self.update_table()
        else:
            messagebox.showwarning("Предупреждение", "Файл books_
