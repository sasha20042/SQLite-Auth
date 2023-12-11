import sqlite3
from hashlib import sha256
import tkinter as tk
from tkinter import messagebox

# Підключення до бази даних
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Створення таблиці для збереження користувачів (якщо вона ще не існує)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL
    );
''')

# Функція для перевірки існування користувача за ім'ям
def user_exists(username):
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    return cursor.fetchone() is not None

# Функція для створення нового користувача
def create_user(username, password, name):
    hashed_password = sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)", (username, hashed_password, name))
    conn.commit()

# Функція для перевірки існування користувача та вірності пароля
def authenticate_user(username, password):
    hashed_password = sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    return cursor.fetchone() is not None

# Функція, яка викликається при успішній реєстрації
def on_registration_success():
    messagebox.showinfo("Реєстрація", f"Вітаємо, {entry_name.get()}! Ви успішно зареєструвалися!")
    show_login_frame()

# Функція для відображення вікна логіну
def show_login_frame():
    frame_registration.pack_forget()
    frame_welcome.pack_forget()  # Додано для видалення вікна ласування
    frame_login.pack()

# Функція для відображення вікна ласування
def show_welcome_frame(username):
    frame_login.pack_forget()
    frame_welcome.pack()
    label_welcome.config(text=f"Вітаємо, {username}! Ви успішно увійшли в систему.")

# Функція для відображення вікна реєстрації
def show_registration_frame():
    frame_login.pack_forget()
    frame_welcome.pack_forget()  # Додано для видалення вікна ласування
    frame_registration.pack()

# Функція для обробки події натискання кнопки "Увійти"
def login():
    username = entry_login_username.get()
    password = entry_login_password.get()

    if authenticate_user(username, password):
        show_welcome_frame(username)
    else:
        messagebox.showwarning("Помилка", "Не вдалося автентифікувати користувача.")

# Функція для обробки події натискання кнопки "Зареєструватися"
def register_user():
    username = entry_reg_username.get()
    password = entry_reg_password.get()
    name = entry_name.get()

    if user_exists(username):
        messagebox.showwarning("Помилка", "Користувач з таким ім'ям вже існує.")
    else:
        create_user(username, password, name)
        on_registration_success()

# Створення головного вікна
main_window = tk.Tk()
main_window.title("Аутентифікація")

# Створення рамок для відображення різних частин інтерфейсу
frame_registration = tk.Frame(main_window)
frame_login = tk.Frame(main_window)
frame_welcome = tk.Frame(main_window)

# Створення та розміщення елементів на рамці реєстрації
tk.Label(frame_registration, text="Ім'я користувача:").pack()
entry_reg_username = tk.Entry(frame_registration)
entry_reg_username.pack()

tk.Label(frame_registration, text="Пароль:").pack()
entry_reg_password = tk.Entry(frame_registration, show="*")
entry_reg_password.pack()

tk.Label(frame_registration, text="Ім'я:").pack()
entry_name = tk.Entry(frame_registration)
entry_name.pack()

tk.Button(frame_registration, text="Зареєструватися", command=register_user).pack()

# Створення та розміщення елементів на рамці логіну
tk.Label(frame_login, text="Ім'я користувача:").pack()
entry_login_username = tk.Entry(frame_login)
entry_login_username.pack()

tk.Label(frame_login, text="Пароль:").pack()
entry_login_password = tk.Entry(frame_login, show="*")
entry_login_password.pack()

tk.Button(frame_login, text="Увійти", command=login).pack()
tk.Button(frame_login, text="Зареєструватися", command=show_registration_frame).pack()

# Створення та розміщення елементів на рамці вітання
label_welcome = tk.Label(frame_welcome, text="")
label_welcome.pack()

tk.Button(frame_welcome, text="Вийти", command=show_login_frame).pack()

# Початкове відображення рамки логіну
show_login_frame()

# Запуск головного вікна
main_window.mainloop()
