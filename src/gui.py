import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk


class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")

        # Загрузка изображений
        self.load_images()

        self.first_page()

    def load_images(self):
        """Загрузка и изменение размера изображений."""
        self.back_image = Image.open("back.png")  # Замените на путь к вашему изображению
        self.back_image = self.back_image.resize((50, 30), Image.LANCZOS)
        self.back_photo = ImageTk.PhotoImage(self.back_image)

        self.santa_image = Image.open("santa.png")  # Замените на путь к вашему изображению
        self.santa_image = self.santa_image.resize((500, 500), Image.LANCZOS)
        self.santa_photo = ImageTk.PhotoImage(self.santa_image)

        self.child_image = Image.open("child.png")  # Замените на путь к вашему изображению
        self.child_image = self.child_image.resize((600, 300), Image.LANCZOS)
        self.child_photo = ImageTk.PhotoImage(self.child_image)

        self.newYear_image = Image.open("newYear.png")  # Замените на путь к вашему изображению
        self.newYear_image = self.newYear_image.resize((500, 400), Image.LANCZOS)
        self.newYear_photo = ImageTk.PhotoImage(self.newYear_image)

        self.bag_image = Image.open("bag.png")  # Замените на путь к вашему изображению
        self.bag_image = self.bag_image.resize((110, 110), Image.LANCZOS)
        self.bag_photo = ImageTk.PhotoImage(self.bag_image)

        self.deer_image = Image.open("deer.png")  # Замените на путь к вашему изображению
        self.deer_image = self.deer_image.resize((200, 300), Image.LANCZOS)
        self.deer_photo = ImageTk.PhotoImage(self.deer_image)

    def first_page(self):
        self.clear_frame()
        self.root.title("Авторизация")

        self.first_page_frame = tk.Frame(self.root)
        self.first_page_frame.pack(fill=tk.BOTH, expand=True)

        self.register_button = tk.Button(self.first_page_frame, text="Зарегистрироваться", command=self.open_registration)
        self.register_button.pack(pady=10)

        self.login_button = tk.Button(self.first_page_frame, text="Войти", command=self.open_login)
        self.login_button.pack(pady=10)

        self.newYear_label = tk.Label(self.first_page_frame, image=self.newYear_photo)
        self.newYear_label.place(x=150, y=150)

        self.bag_button = tk.Button(self.first_page_frame, image=self.bag_photo, command=self.open_login_for_santas, borderwidth=0,
                                    highlightthickness=0, bg=self.first_page_frame.cget("bg"))
        self.bag_button.place(x=578, y=440)

    def open_registration(self):
        self.clear_frame()
        self.root.title("Регистрация")

        self.registration_frame = tk.Frame(self.root)
        self.registration_frame.pack(padx=20, pady=20)

        tk.Label(self.registration_frame, text="Логин:").grid(row=0, column=0)
        self.reg_login_entry = tk.Entry(self.registration_frame)
        self.reg_login_entry.grid(row=0, column=1)

        tk.Label(self.registration_frame, text="Пароль:").grid(row=1, column=0)
        self.reg_password_entry = tk.Entry(self.registration_frame, show='*')
        self.reg_password_entry.grid(row=1, column=1)

        tk.Label(self.registration_frame, text="Повторите пароль:").grid(row=2, column=0)
        self.reg_password_confirm_entry = tk.Entry(self.registration_frame, show='*')
        self.reg_password_confirm_entry.grid(row=2, column=1)

        self.register_submit_button = tk.Button(self.registration_frame, text="Зарегистрироваться",
                                                command=self.register)
        self.register_submit_button.grid(row=3, columnspan=2, pady=10)

        self.deer_label = tk.Label(self.root, image=self.deer_photo)
        self.deer_label.place(x=570, y=250)

        self.back_button = tk.Button(self.root, image=self.back_photo, command=self.first_page)
        self.back_button.place(relx=0.0, rely=0.0, anchor='nw')

    def open_login(self):
        self.clear_frame()
        self.root.title("Вход")

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=20, pady=20)

        tk.Label(self.login_frame, text="Логин:").grid(row=0, column=0)
        self.login_entry = tk.Entry(self.login_frame)
        self.login_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Пароль:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=1)

        self.login_submit_button = tk.Button(self.login_frame, text="Войти", command=self.login)
        self.login_submit_button.grid(row=2, columnspan=2, pady=10)

        self.child_label = tk.Label(self.root, image=self.child_photo)
        self.child_label.pack(pady=50)

        self.back_button = tk.Button(self.root, image=self.back_photo, command=self.first_page)
        self.back_button.place(relx=0.0, rely=0.0, anchor='nw')

    def open_child_main_menu(self):
        self.clear_frame()
        self.root.title("Аккаунт")

        self.open_child_main_menu_frame = tk.Frame(self.root)
        self.open_child_main_menu_frame.pack(fill=tk.BOTH, expand=True)

        # Создание таблицы для отображения писем
        self.tree = ttk.Treeview(self.open_child_main_menu_frame, columns=("Year", "Topic", "Description"), show='headings')
        self.tree.heading("Year", text="Год")
        self.tree.heading("Topic", text="Тема")
        self.tree.heading("Description", text="Описание")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Обработчик события для клика по строке
        self.tree.bind("<Double-1>", self.on_item_double_click)

        # Кнопка для добавления нового письма
        self.add_email_button = tk.Button(self.open_child_main_menu_frame, text="Отправить новое письмо", command=self.write_email)
        self.add_email_button.pack(pady=10)

        # Отображение писем в таблице
        self.display_emails()

    def on_item_double_click(self, event):
        # Получаем выбранный элемент
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')
            self.show_email(item_values)

    def show_email(self, email_data):
        # Создаем новое окно для отображения письма
        email_window = tk.Toplevel(self.root)
        email_window.title("Просмотр письма")

        # Устанавливаем размер окна
        email_window.geometry("400x200")  # Ширина x Высота

        # Центрируем окно на экране
        self.center_window(email_window)

        tk.Label(email_window, text="Год:").grid(row=0, column=0)
        tk.Label(email_window, text=email_data[0]).grid(row=0, column=1)

        tk.Label(email_window, text="Тема:").grid(row=1, column=0)
        topic_entry = tk.Entry(email_window)
        topic_entry.grid(row=1, column=1)
        topic_entry.insert(0, email_data[1])  # Заполнение текущей темы

        tk.Label(email_window, text="Описание:").grid(row=2, column=0)
        description_entry = tk.Entry(email_window)
        description_entry.grid(row=2, column=1)
        description_entry.insert(0, email_data[2])  # Заполнение текущего описания

        # Кнопка для сохранения изменений
        save_button = tk.Button(email_window, text="Сохранить изменения",
                                command=lambda: self.save_email(email_data[0], topic_entry.get(),
                                                                description_entry.get()))
        save_button.grid(row=3, columnspan=2)

    def center_window(self, window):
        # Получаем размеры экрана
        width = 400  # Ширина окна
        height = 200  # Высота окна
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Вычисляем координаты для центрирования
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Устанавливаем размеры и положение окна
        window.geometry(f"{width}x{height}+{x}+{y}")

    def save_email(self, year, topic, description):
        # Здесь вы можете добавить логику для сохранения изменений
        print ("поменял в бд письмо")
        messagebox.showinfo("Сохранение", f"Письмо с годом '{year}' изменено:\nТема: {topic}\nОписание: {description}")
        # Обновите данные в self.emails и таблице, если необходимо

    def display_emails(self):
        # Пример данных для писем

        self.emails = [
            {"Year": "2024", "Topic": "cat", "Description": "cute small kitten"},
            {"Year": "2024", "Topic": "ball", "Description": "i would like to play football, but i haven't a ball"},
        ]
        for _ in range(100):
            email =  {"Year": "2024", "Topic": "cat", "Description": "cute small kitten"}
            self.emails.append(email)

        # Очищаем таблицу перед добавлением новых данных
        # for row in self.tree.get_children():
        #     self.tree.delete(row)

        # Добавление писем в таблицу
        for email in self.emails:
            self.tree.insert("", "end", values=(email["Year"], email["Topic"], email["Description"]))

    def write_email(self):
        self.clear_frame()
        self.root.title("Отправка письма")

        self.add_email_frame = tk.Frame(self.root)
        self.add_email_frame.pack(padx=20, pady=20)

        tk.Label(self.add_email_frame, text="Тема:").grid(row=0, column=0)
        self.email_entry = tk.Entry(self.add_email_frame)
        self.email_entry.grid(row=1, column=0)

        tk.Label(self.add_email_frame, text="Описание:").grid(row=2, column=0)
        self.email_text = tk.Text(self.add_email_frame, wrap=tk.WORD, width=50, height=15)
        self.email_text.grid(row=3, column=0)

        self.send_button = tk.Button(self.root, text="Отправить", command=self.send_email)
        self.send_button.place(x = 535, y = 333)

    def send_email(self):
        messagebox.showinfo("Успех", "Письмо отправлено санте!")
        print("записал письмо в базу данных")

        self.open_child_main_menu()

    def open_login_for_santas(self):
        self.clear_frame()

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=20, pady=20)

        tk.Label(self.login_frame, text="Логин:").grid(row=0, column=0)
        self.login_entry = tk.Entry(self.login_frame)
        self.login_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Пароль:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=1)

        self.login_submit_button = tk.Button(self.login_frame, text="Войти", command=self.login_for_santas)
        self.login_submit_button.grid(row=2, columnspan=2, pady=10)

        # Создание метки для отображения изображения
        self.santa_label = tk.Label(self.root, image=self.santa_photo)
        self.santa_label.pack(pady=10)  # Используем pack для метки с изображением

    def open_santa_main_menu(self):
        self.clear_frame()
        self.root.title("Аккаунт")

        self.open_santa_main_menu_frame = tk.Frame(self.root)
        self.open_santa_main_menu_frame.pack(fill=tk.BOTH, expand=True)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def register(self):
        login = self.reg_login_entry.get()
        password = self.reg_password_entry.get()
        password_confirm = self.reg_password_confirm_entry.get()

        if password != password_confirm:
            messagebox.showerror("Ошибка", "Пароли не совпадают!")
        else:
            # Здесь можно добавить логику для сохранения данных
            messagebox.showinfo("Успех", "Регистрация успешна!")
            self.open_login()

    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        # Здесь можно добавить логику для проверки логина и пароля
        messagebox.showinfo("Успех", "Вы вошли в систему!")

        self.open_child_main_menu()

    def login_for_santas(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        # Здесь можно добавить логику для проверки логина и пароля
        messagebox.showinfo("Успех", "Вы вошли в систему!")

        self.open_santa_main_menu()


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = App(root)
    root.mainloop()
