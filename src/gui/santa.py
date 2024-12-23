import tkinter as tk
from tkinter import ttk, messagebox

class Santa:
    def __init__(self, root, app, nickname):
        self.root = root
        self.app = app
        self.emails = []
        self.nickname = nickname

        self.open_santa_main_menu()

    def open_santa_main_menu(self):
        self.app.clear_frame()
        self.root.title("Аккаунт")

        santa_main_menu_frame = tk.Frame(self.root)
        santa_main_menu_frame.pack(fill=tk.BOTH, expand=True)

        # Создание таблицы для отображения писем
        self.tree = ttk.Treeview(santa_main_menu_frame, columns=("ID", "Topic", "Description"),show='headings')
        self.tree.heading("ID", text="Идентификатор")
        self.tree.heading("Topic", text="Тема")
        self.tree.heading("Description", text="Описание")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Обработчик события для клика по строке
        self.tree.bind("<Double-1>", self.on_item_double_click)

        # Отображение писем в таблице
        self.show_emails()

        # Кнопка для выхода из профиля
        logout_button = tk.Button(santa_main_menu_frame, text="Выйти из аккаунта", command=self.sign_out)
        logout_button.pack(pady=10, side='left')

    def sign_out(self):
        self.app.authorization.first_page()

    def show_emails(self):
        self.emails = self.app.db_ctrl.getCurrentLettersBySantaNickname(self.nickname)

        for email in self.emails:
            self.tree.insert("", "end", values=(email["author_id"], email["topic"], email["description"]))

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

        tk.Label(email_window, text="Тема:").grid(row=1, column=2)
        topic_label = tk.Label(email_window, text=email_data[1])
        topic_label.grid(row=1, column=3, sticky='w')

        tk.Label(email_window, text="Описание:").grid(row=2, column=2)
        description_text = tk.Text(email_window, wrap=tk.WORD, width=40, height=5)
        description_text.grid(row=2, column=3)
        description_text.insert(tk.END, email_data[2])  # Заполнение текущего описания
        description_text.config(state=tk.DISABLED)  # Запрет изменения текста

        # Кнопка для сохранения изменений
        save_button = tk.Button(email_window, text="Посмотреть информацию о ребенке", command=lambda: self.open_information_about_child(email_data[0]))
        save_button.grid(row=3, column=3, pady=20)

        email_window.mainloop()

    def open_information_about_child(self, author_id):
        # Создаем новое окно для отображения письма
        child_window = tk.Toplevel(self.root)
        child_window.title("Просмотр информации о ребенке")

        # Устанавливаем размер окна
        child_window.geometry("400x200")  # Ширина x Высота

        # Центрируем окно на экране
        self.center_window(child_window)

        child_info = {}

        self.get_information_about_child(author_id, child_info)

        # Отображаем данные пользователя
        tk.Label(child_window, text="Полное имя:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        tk.Label(child_window, text = child_info["full_name"]).grid(row=0, column=1, padx=10, pady=5, sticky='we')

        tk.Label(child_window, text="Дата рождения:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        tk.Label(child_window, text = child_info["birth_date"]).grid(row=1, column=1, padx=10, pady=5, sticky='we')

        tk.Label(child_window, text="Посткод:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        tk.Label(child_window, text = child_info["postcode"]).grid(row=2, column=1, padx=10,pady=5, sticky='we')

        tk.Label(child_window, text="Хорошие поступки:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        tk.Label(child_window, text = child_info["number_of_good_deeds"]).grid(row=3, column=1, padx=10, pady=5, sticky='we')

        tk.Label(child_window, text="Плохие поступки:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
        tk.Label(child_window, text = child_info["number_of_misdeeds"]).grid(row=4, column=1, padx=10, pady=5, sticky='we')

        child_window.mainloop()

    def get_information_about_child(self, author_id, child_info):
        child_info.update(self.app.db_ctrl.getChildById(author_id))

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