import unittest
import json
import os

DATA_FILE = "books.json"

class TestBookTracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаём тестовый JSON для загрузки
        cls.test_data = [
            {"title": "Война и мир", "author": "Л.Н. Толстой", "genre": "Роман", "pages": 1225},
            {"title": "1984", "author": "Дж. Оруэлл", "genre": "Антиутопия", "pages": 328}
        ]

    def test_json_save_load(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.test_data, f)

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        self.assertEqual(self.test_data[0]['title'], loaded_data[0]['title'])

if __name__ == "__main__":
    unittest.main()