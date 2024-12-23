import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry


class Authorization:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.load_images()
        self.first_page()

    def load_images(self):
        """Загрузка и изменение размера изображений."""
        self.back_image = Image.open("../images/back.png")  # Замените на путь к вашему изображению
        self.back_image = self.back_image.resize((50, 30), Image.LANCZOS)
        self.back_photo = ImageTk.PhotoImage(self.back_image)

        self.santa_image = Image.open("../images/santa.png")  # Замените на путь к вашему изображению
        self.santa_image = self.santa_image.resize((500, 500), Image.LANCZOS)
        self.santa_photo = ImageTk.PhotoImage(self.santa_image)

        self.child_image = Image.open("../images/child.png")  # Замените на путь к вашему изображению
        self.child_image = self.child_image.resize((600, 300), Image.LANCZOS)
        self.child_photo = ImageTk.PhotoImage(self.child_image)

        self.newYear_image = Image.open("../images/newYear.png")  # Замените на путь к вашему изображению
        self.newYear_image = self.newYear_image.resize((500, 400), Image.LANCZOS)
        self.newYear_photo = ImageTk.PhotoImage(self.newYear_image)

        self.bag_image = Image.open("../images/bag.png")  # Замените на путь к вашему изображению
        self.bag_image = self.bag_image.resize((110, 110), Image.LANCZOS)
        self.bag_photo = ImageTk.PhotoImage(self.bag_image)

        self.deer_image = Image.open("../images/deer.png")  # Замените на путь к вашему изображению
        self.deer_image = self.deer_image.resize((200, 300), Image.LANCZOS)
        self.deer_photo = ImageTk.PhotoImage(self.deer_image)

    def first_page(self):
        self.app.clear_frame()
        self.root.title("Авторизация")

        first_page_frame = tk.Frame(self.root)
        first_page_frame.pack(fill=tk.BOTH, expand=True)

        register_button = tk.Button(first_page_frame, text="Зарегистрироваться",command=self.open_registration)
        register_button.pack(pady=10)

        login_button = tk.Button(first_page_frame, text="Войти", command=self.open_login)
        login_button.pack(pady=10)

        newYear_label = tk.Label(first_page_frame, image=self.newYear_photo)
        newYear_label.place(x=150, y=150)

        bag_button = tk.Button(first_page_frame, image=self.bag_photo, command=self.open_login_for_santas, borderwidth=0, highlightthickness=0, bg=first_page_frame.cget("bg"))
        bag_button.place(x=578, y=440)

    def open_registration(self):
        self.app.clear_frame()
        self.root.title("Регистрация")

        registration_frame = tk.Frame(self.root)
        registration_frame.pack(padx=20, pady=20)

        tk.Label(registration_frame, text="Свидетельство о рождении:").grid(row=0, column=0, pady = 3)
        self.reg_birth_certificate_entry = tk.Entry(registration_frame)
        self.reg_birth_certificate_entry.grid(row=0, column=1, pady = 3)

        tk.Label(registration_frame, text="ФИО:").grid(row=1, column=0, pady = 3)
        self.reg_full_name_entry = tk.Entry(registration_frame)
        self.reg_full_name_entry.grid(row=1, column=1, pady = 3)

        tk.Label(registration_frame, text="Дата рождения:").grid(row=2, column=0, pady = 3)
        self.reg_date_of_birth_entry = DateEntry(registration_frame)
        self.reg_date_of_birth_entry.grid(row=2, column=1, pady = 3)

        tk.Label(registration_frame, text="Посткод:").grid(row=3, column=0,pady = 3)
        self.reg_postcode_entry = tk.Entry(registration_frame)
        self.reg_postcode_entry.grid(row=3, column=1, pady = 3)

        tk.Label(registration_frame, text="Пароль:").grid(row=4, column=0, pady = (30,0))
        self.reg_password_entry = tk.Entry(registration_frame) #, show='*'
        self.reg_password_entry.grid(row=4, column=1, pady = (30,0))

        tk.Label(registration_frame, text="Повторите пароль:").grid(row=5, column=0, pady = 3)
        self.reg_password_confirm_entry = tk.Entry(registration_frame) # , show='*'
        self.reg_password_confirm_entry.grid(row=5, column=1, pady = 3)

        register_submit_button = tk.Button(registration_frame, text="Зарегистрироваться", command=self.register)
        register_submit_button.grid(row=6, columnspan=2, pady=10)

        deer_label = tk.Label(self.root, image=self.deer_photo)
        deer_label.place(x=570, y=250)

        back_button = tk.Button(self.root, image=self.back_photo, borderwidth=0,  highlightthickness=0, bg=registration_frame.cget("bg"), command=self.first_page)
        back_button.place(relx=0.01, rely=0.01, anchor='nw')

    def open_login(self):
        self.app.clear_frame()
        self.root.title("Вход")

        login_frame = tk.Frame(self.root)
        login_frame.pack(padx=20, pady=20)

        tk.Label(login_frame, text="Логин:").grid(row=0, column=0)
        self.login_entry = tk.Entry(login_frame)
        self.login_entry.grid(row=0, column=1)

        tk.Label(login_frame, text="Пароль:").grid(row=1, column=0)
        self.password_entry = tk.Entry(login_frame, show='*')
        self.password_entry.grid(row=1, column=1)

        login_submit_button = tk.Button(login_frame, text="Войти", command=self.login)
        login_submit_button.grid(row=2, columnspan=2, pady=10)

        child_label = tk.Label(self.root, image=self.child_photo)
        child_label.pack(pady=50)

        back_button = tk.Button(self.root, image=self.back_photo, borderwidth=0, highlightthickness=0, bg=login_frame.cget("bg"), command=self.first_page)
        back_button.place(relx=0.01, rely=0.01, anchor='nw')

    def register(self):
        birth_certificate = self.reg_birth_certificate_entry.get()
        full_name = self.reg_full_name_entry.get()
        birth_date = self.reg_date_of_birth_entry.get_date().strftime('%Y.%m.%d')
        postcode = self.reg_postcode_entry.get()


        password = self.reg_password_entry.get()
        password_confirm = self.reg_password_confirm_entry.get()

        if password != password_confirm:
            messagebox.showerror("Ошибка", "Пароли не совпадают!")
        else:
            # Здесь можно добавить логику для сохранения данных
            messagebox.showinfo("Успех", "Регистрация успешна!")
            self.app.db_ctrl.registerChild(birth_certificate, password, full_name, birth_date, postcode)
            self.open_login()



    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if self.app.db_ctrl.isChildLoggedIn(login, password):
            messagebox.showinfo("Успех", "Вы вошли в систему!")
            self.app.open_child_main_menu(login)
        else:
            messagebox.showinfo("Ошибка", "Вы ввели неверный логин или пароль!")

    def open_login_for_santas(self):
        self.app.clear_frame()
        self.root.title("Вход")

        login_frame = tk.Frame(self.root)
        login_frame.pack(padx=20, pady=20)

        tk.Label(login_frame, text="Логин:").grid(row=0, column=0)
        self.login_entry = tk.Entry(login_frame)
        self.login_entry.grid(row=0, column=1)

        tk.Label(login_frame, text="Пароль:").grid(row=1, column=0)
        self.password_entry = tk.Entry(login_frame, show='*')
        self.password_entry.grid(row=1, column=1)

        login_submit_button = tk.Button(login_frame, text="Войти", command=self.login_for_santas)
        login_submit_button.grid(row=2, columnspan=2, pady=10)

        # Создание метки для отображения изображения
        santa_label = tk.Label(self.root, image=self.santa_photo)
        santa_label.pack(pady=10)  # Используем pack для метки с изображением

        back_button = tk.Button(self.root, image=self.back_photo, borderwidth=0, highlightthickness=0, bg=login_frame.cget("bg"), command=self.first_page)
        back_button.place(relx=0.01, rely=0.01, anchor='nw')

    def login_for_santas(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        print(login , password)
        if self.app.db_ctrl.isSantaLoggedIn(login, password):
            messagebox.showinfo("Успех", "Вы вошли в систему!")
            self.app.open_santa_main_menu(login)
        else:
            messagebox.showinfo("Ошибка", "Вы ввели неверный логин или пароль!")

