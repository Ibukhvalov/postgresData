import tkinter as tk
from authorization import Authorization
from child import Child
from santa import Santa


class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.authorization = Authorization(self.root, self)

        #self.dbcontroller

    def open_child_main_menu(self, birth_certificate):
        self.child = Child(self.root, self, birth_certificate)

    def open_santa_main_menu(self, nickname):
        self.santa = Santa(self.root, self, nickname)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = App(root)
    root.mainloop()
