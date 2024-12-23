import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class Child:
    def __init__(self, root, app, birth_certificate):
        self.emails_by_search = []
        self.root = root
        self.app = app
        self.emails = []
        self.birth_certificate = birth_certificate

        self.load_images()
        self.open_child_main_menu()

    def load_images(self):
        """Загрузка и изменение размера изображений."""
        self.back_image = Image.open("../images/back.png")  # Замените на путь к вашему изображению
        self.back_image = self.back_image.resize((50, 30), Image.LANCZOS)
        self.back_photo = ImageTk.PhotoImage(self.back_image)

    def open_child_main_menu(self):
        self.app.clear_frame()
        self.root.title("Аккаунт")

        child_main_menu_frame = tk.Frame(self.root)
        child_main_menu_frame.pack(fill=tk.BOTH, expand=True)

        # Создание таблицы для отображения писем
        self.tree = ttk.Treeview(child_main_menu_frame, columns=("Year", "Topic", "Description"), show='headings')
        self.tree.heading("Year", text="Год")
        self.tree.heading("Topic", text="Тема")
        self.tree.heading("Description", text="Описание")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Обработчик события для клика по строке
        self.tree.bind("<Double-1>", self.on_item_double_click)

        settings_button = tk.Button(child_main_menu_frame, text="Настройки", command=self.open_settings)
        settings_button.pack(pady=10, side='left')

        find_email_button = tk.Button(child_main_menu_frame, text="Найти письмо", command=self.open_finder)
        find_email_button.place(x = 355, y = 565)

        # Кнопка для добавления нового письма
        add_email_button = tk.Button(child_main_menu_frame, text="Отправить новое письмо", command=self.write_email)
        add_email_button.pack(side = 'right')

        # Отображение писем в таблице
        self.show_emails()

    def open_finder(self):
        # Создаем новое окно для поиска

        self.app.clear_frame()
        self.root.title("Поиск писем")

        finder_frame = tk.Frame(self.root)
        finder_frame.pack(fill=tk.BOTH, expand=True)

        back_button = tk.Button(self.root, image=self.back_photo, borderwidth=0, highlightthickness=0, bg=finder_frame.cget("bg"), command=self.open_child_main_menu)
        back_button.place(relx=0.01, rely=0.01, anchor='nw')

        # Переменная для хранения выбранного типа поиска
        self.search_type = tk.StringVar(value="topic")

        # Радиокнопки для выбора типа поиска
        tk.Radiobutton(finder_frame, text="По теме", variable=self.search_type, value="topic").pack(pady = 1)
        tk.Radiobutton(finder_frame, text="По году", variable=self.search_type, value="year").pack(pady = 1)

        # Поле для ввода поиска
        self.search_entry = tk.Entry(finder_frame)
        self.search_entry.pack(pady=10)

        # Кнопка для выполнения поиска
        search_button = tk.Button(finder_frame, text="Поиск", command=self.perform_search)
        search_button.pack(pady=10)

        # Таблица для отображения результатов
        self.results_tree = ttk.Treeview(finder_frame, columns=("Year", "Topic", "Description"), show='headings')
        self.results_tree.heading("Year", text="Год")
        self.results_tree.heading("Topic", text="Тема")
        self.results_tree.heading("Description", text="Описание")
        self.results_tree.pack(fill=tk.BOTH, expand=True, pady=10)

        delete_button = tk.Button(finder_frame, text="Удалить все", command=self.delete_emails_by_search)
        delete_button.pack(pady = 10, side = "right")

    def delete_emails_by_search(self):
        if self.search_type.get() == "topic":
            self.emails_by_search = self.app.db_ctrl.deleteLettersByChildAndTopic(self.birth_certificate, self.search_entry.get())
        else:
            self.emails_by_search = self.app.db_ctrl.deleteLettersByChildAndYear(self.birth_certificate,
                                                                               self.search_entry.get())

        self.show_emails_by_search()


    def perform_search(self):
        if self.search_type.get() == "topic":
            self.emails_by_search = self.app.db_ctrl.getLettersByChildAndTopic(self.birth_certificate, self.search_entry.get())
        else:
            self.emails_by_search = self.app.db_ctrl.getLettersByChildAndYear(self.birth_certificate,
                                                                               self.search_entry.get())

        self.show_emails_by_search()

    def show_emails_by_search(self):
        # Очищаем таблицу перед добавлением новых данных
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)

        # Добавление писем в таблицу
        if len(self.emails_by_search) > 0:
            for email in self.emails_by_search:
                self.results_tree.insert("", "end", values=(email["year"], email["topic"], email["description"]))

    def open_settings(self):
        self.app.clear_frame()
        self.root.title("Настройки")

        settings_frame = tk.Frame(self.root)
        settings_frame.pack(padx=20, pady=20)

        child_info = {}

        self.get_child_info(self.birth_certificate, child_info)

        # Отображаем данные пользователя
        tk.Label(settings_frame, text="Полное имя:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(settings_frame, text=child_info["full_name"]).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(settings_frame, text="Дата рождения:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(settings_frame, text=child_info["birth_date"]).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(settings_frame, text="Свидетельство о рождении:").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(settings_frame, text=self.birth_certificate).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(settings_frame, text="Посткод:").grid(row=3, column=0, padx=10, pady=5)
        tk.Label(settings_frame, text=child_info["postcode"]).grid(row=3, column=1, padx=10, pady=5)

        # Кнопка для выхода из профиля
        logout_button = tk.Button(settings_frame, text="Выйти", command=self.sign_out)
        logout_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Кнопка для удаления профиля
        delete_button = tk.Button(settings_frame, text="Удалить профиль", command=self.delete_profile)
        delete_button.grid(row=5, column=0, columnspan=2, pady=5)

        back_button = tk.Button(self.root, image=self.back_photo, borderwidth=0, highlightthickness=0, bg=settings_frame.cget("bg"), command=self.open_child_main_menu)
        back_button.place(relx=0.01, rely=0.01, anchor='nw')

    def get_child_info(self, birth_certificate, child_info):
        child_info.update(self.app.db_ctrl.getChildById(birth_certificate))

    def delete_profile(self):
        self.app.db_ctrl.deleteChild(self.birth_certificate)
        self.app.authorization.first_page()

    def sign_out(self):
        self.app.authorization.first_page()

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

        tk.Label(email_window, text="Год:").grid(row=0, column=2, pady=5)
        tk.Label(email_window, text=email_data[0]).grid(row=0, column=3, sticky='w')

        tk.Label(email_window, text="Тема:").grid(row=1, column=2)
        topic_entry = tk.Entry(email_window)
        topic_entry.grid(row=1, column=3, sticky='w')
        topic_entry.insert(0, email_data[1])  # Заполнение текущей темы

        tk.Label(email_window, text="Описание:").grid(row=2, column=2)
        description_text = tk.Text(email_window, wrap=tk.WORD, width=40, height=5)
        description_text.grid(row=2, column=3)
        description_text.insert(tk.END, email_data[2])  # Заполнение текущего описания

        # Кнопка для сохранения изменений
        save_button = tk.Button(email_window, text="Сохранить изменения", command=lambda: self.save_email(email_data[0], topic_entry.get(), description_text.get("1.0", tk.END), email_window))
        save_button.grid(row=3, column=3, sticky='e', pady=3)

        # Кнопка для удаления письма
        delete_button = tk.Button(email_window, text="Удалить письмо",
                                  command=lambda: self.delete_email(email_data[0], email_window))
        delete_button.grid(row=4, column=3, sticky='e')

        email_window.mainloop()

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

    def delete_email(self, year, email_window):
        self.app.db_ctrl.deleteLetterByChildAndYear(self.birth_certificate, year)
        messagebox.showinfo("Удаление", f"Письмо с годом '{year}' удалено")
        email_window.destroy()

    def save_email(self, year, topic, description, email_window):
        # Здесь вы можете добавить логику для сохранения изменений
        self.app.db_ctrl.updateLetter(self.birth_certificate, year, topic, description)
        messagebox.showinfo("Сохранение", f"Письмо с годом '{year}' изменено:\nТема: {topic}\nОписание: {description}")
        # Обновите данные в self.emails и таблице, если необходимо
        #TODO
        self.show_emails()
        email_window.destroy()

    def show_emails(self):
        self.emails = self.app.db_ctrl.getLettersByChild(self.birth_certificate)

        # Очищаем таблицу перед добавлением новых данных
        for row in self.tree.get_children():
             self.tree.delete(row)
        # Добавление писем в таблицу
        for email in self.emails:
            self.tree.insert("", "end", values=(email["year"], email["topic"], email["description"]))

    def write_email(self):
        self.app.clear_frame()
        self.root.title("Отправка письма")

        add_email_frame = tk.Frame(self.root)
        add_email_frame.pack(padx=20, pady=20)

        tk.Label(add_email_frame, text="Тема:").grid(row=0, column=0)
        email_topic = tk.Entry(add_email_frame)
        email_topic.grid(row=1, column=0)

        tk.Label(add_email_frame, text="Описание:").grid(row=2, column=0)
        email_description = tk.Text(add_email_frame, wrap=tk.WORD, width=50, height=15)
        email_description.grid(row=3, column=0)

        send_button = tk.Button(self.root, text="Отправить", command=lambda: self.send_email(email_topic.get(), email_description.get("1.0", tk.END)))
        send_button.place(x=535, y=333)

        back_button = tk.Button(self.root, image=self.back_photo, borderwidth=0, highlightthickness=0, bg=add_email_frame.cget("bg"), command=self.open_child_main_menu)
        back_button.place(relx=0.01, rely=0.01, anchor='nw')

    def send_email(self, topic, description):
        messagebox.showinfo("Успех", "Письмо отправлено санте!")
        self.app.db_ctrl.addLetter(self.birth_certificate, topic, description)

        self.open_child_main_menu()