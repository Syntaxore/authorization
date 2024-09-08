import tkinter as tk
import sqlite3
import bcrypt
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo, showwarning

tkbtn = ttk.Button
tklabel = ttk.Label
tkentry = ttk.Entry

# Создание или подключение к базе данных
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Создание таблицы, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Программа")
        self.geometry("400x500")

        self.frames = {}
        for F in (Page1, Page2):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Page1")  # Показываем первую страницу при запуске

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Создаем виджеты
        label0 = tklabel(self, text="Вход", font=("Arial", 16))
        login_text = tklabel(self, text="Логин", font=("Arial", 12))
        password_login = tklabel(self, text="Пароль", font=("Arial", 12))

        self.login_entry = tkentry(self)
        self.password_entry = tkentry(self, show="*")

        # Упаковка заголовка
        label0.grid(row=0, column=0, columnspan=2, pady=20)

        # Упаковка меток и полей ввода
        login_text.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.login_entry.grid(row=1, column=1, padx=10, pady=5)

        password_login.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Кнопки
        button_frame = tk.Frame(self)
        create_account = tkbtn(button_frame, text="Войти", command=self.checklogin)
        slide = tkbtn(button_frame, text="Регистрация", command=lambda: controller.show_frame("Page2"))

        # Упаковка кнопок в горизонтальном фрейме
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        create_account.pack(side="left", padx=5)
        slide.pack(side="left", padx=5)

        # Установка фокуса на поле логина
        self.login_entry.focus()

        # Центрирование элементов
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
    def checklogin(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if not login or not password:
            showerror(title="Ошибка!", message="Ошибка входа!")
            return

        # Проверка логина и пароля
        cursor.execute('SELECT password FROM users WHERE username = ?', (login,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
            done = tklabel(self, text="Вход прошел успешно!", font=("Arial", 12))
            done.grid(row=4, column=0, columnspan=2, pady=5)
            self.after(5000, done.destroy)
        else:
            deny = tklabel(self, text="Неверный логин или пароль!", font=("Arial", 12))
            deny.grid(row=4, column=0, columnspan=2, pady=5)
            self.after(5000, deny.destroy)


class Page2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Создаем виджеты
        label0 = tklabel(self, text="Регистрация", font=("Arial", 16))
        login_text = tklabel(self, text="Логин", font=("Arial", 12))
        password_login = tklabel(self, text="Пароль", font=("Arial", 12))

        self.login_entry = tkentry(self)
        self.password_entry = tkentry(self, show="*")

        # Упаковка заголовка
        label0.grid(row=0, column=0, columnspan=2, pady=20)

        # Упаковка меток и полей ввода
        login_text.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.login_entry.grid(row=1, column=1, padx=10, pady=5)

        password_login.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Кнопки
        button_frame = tk.Frame(self)
        create_account = tkbtn(button_frame, text="Создать", command=self.register_user)
        slide = tkbtn(button_frame, text="Назад", command=lambda: controller.show_frame("Page1"))

        # Упаковка кнопок в горизонтальном фрейме
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        create_account.pack(side="left", padx=5)
        slide.pack(side="left", padx=5)

        # Установка фокуса на поле логина
        self.login_entry.focus()

        # Центрирование элементов
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
    def register_user(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if not login or not password:
            showerror(title="Ошибка!", message="Ошибка в регистрации!")
            return

        # Хеширование пароля
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (login, hashed_password))
            conn.commit()
            done = tklabel(self, text="Регистрация прошла успешно!", font=("Arial", 12))
            done.grid(row=4, column=0, columnspan=2, pady=5)
            self.after(5000, done.destroy)
        except sqlite3.IntegrityError:
            deny = tklabel(self, text="Пользователь с таким логином уже существует!", font=("Arial", 12))
            deny.grid(row=4, column=0, columnspan=2, pady=5)
            self.after(5000, deny.destroy)


if __name__ == "__main__":
    app = App()
    app.mainloop()

# Закрытие соединения с базой данных
conn.close()
