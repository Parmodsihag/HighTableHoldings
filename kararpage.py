import tkinter as tk
# import sqlite3

import accounts
import krar

from tkinter import ttk
from mytheme import Colors
from datetime import datetime




class KararPage(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=Colors.BACKGROUND1, **kwargs)

        img = tk.PhotoImage(file="myicons\\framebg2.png")

        self.background_title = tk.Label(self, image=img)
        self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.img = img

        # main frame to include all frames
        self.main_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        self.main_frame.place(relx=0.3, rely=0.01, relwidth=.4, relheight=.98)

        self.background_title = tk.Label(self.main_frame, image=img)
        self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)



        # title frame
        title_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND1)
        title_frame.pack(fill='x', pady=2, padx=10)
        title_name_label = tk.Label(title_frame, text="Krar", font="Consolas 18", bg=Colors.BACKGROUND1, fg=Colors.FG_SHADE_3, anchor='center')
        title_name_label.pack(padx=40, fill='x')

        # Date Entry Box
        date_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        date_frame.pack(fill='x', pady=10, padx=10)
        date_label = tk.Label(date_frame, text="Date", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        date_label.pack(padx=40, fill='x')
        today_date = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.date_entry = tk.Entry(date_frame, textvariable=today_date, font="Consolas 14", bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='flat')
        self.date_entry.pack(padx=40, pady=(0,10), fill='x')

        # Account Dropdown Menu
        account_frame  = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        account_frame.pack( fill='x', pady=10, padx=10)
        account_label = tk.Label(account_frame, text="Account", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        account_label.pack(padx=40, fill='x')
        account_choices = self.get_accounts()
        self.account_dropdown = ttk.Combobox(account_frame, values=account_choices, font="Consolas 14")
        self.account_dropdown.pack(padx=40, pady=(0,10), fill='x')
        self.account_dropdown.bind('<Enter>', lambda e: self.account_dropdown.config(values=self.get_accounts()))


        # button frame
        button_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        button_frame.pack(fill='x', pady=(10,0), padx=10)
        sale_button = tk.Button(button_frame, text="Add krar", font="Consolas 14", command=self.add_krar, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_3, relief='groove')
        sale_button.pack(padx=40, fill='x', pady=(10, 10))

    def get_accounts(self):
        accoount_list = accounts.get_all_customers()
        return accoount_list

    def add_krar(self):
        customer_name = self.account_dropdown.get()
        krar_date = self.date_entry.get()
        if customer_name and krar_date:
            krar_id = krar.create_krar(customer_name, krar_date)
            if __name__ != "__main__":
                self.master.master.set_status(f"Krar Id : {krar_id}")


if __name__ == "__main__":
    app = tk.Tk()
    app.state("zoomed")
    h = KararPage(app)
    h.pack(expand=1, fill="both")
    app.mainloop()
