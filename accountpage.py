import tkinter as tk
# from tkinter import ttk
from datetime import datetime

from mytheme import Colors

import accounts
import database
# from inventory import
# from sales import Sales

class AccountPage(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=Colors.BACKGROUND1, **kwargs)

        APP_FONT = "Consolas 12"
        APP_FONT1 = "Consolas 14"

        img = tk.PhotoImage(file="myicons\\framebg2.png")

        self.background_title = tk.Label(self, image=img)
        self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.img = img

        # main frame to include all frames
        self.main_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        self.main_frame.place(relx=0.3, rely=0.01, relwidth=.4, relheight=.98)

        self.background_title = tk.Label(self.main_frame, image=img)
        self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)

        title_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND1)
        title_frame.pack(fill='x', pady=2, padx=10)
        title_name_label = tk.Label(title_frame, text="Account", font="Consolas 18", bg=Colors.BACKGROUND1, fg=Colors.FG_SHADE_3, anchor='center')
        title_name_label.pack(padx=40, fill='x')

        # Name Entry Box
        name_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        name_frame.pack(fill='x', pady=10, padx=10)

        name_label = tk.Label(name_frame, text="Name", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        name_label.pack(padx=40, fill='x')
        self.name_entry = tk.Entry(name_frame, font=APP_FONT1, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='flat')
        self.name_entry.pack(padx=40, pady=(0,10), fill='x')

        # Other Details Entry Box
        details_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        details_frame.pack(fill='x', pady=10, padx=10)
        details_label = tk.Label(details_frame, text="Other Details", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        details_label.pack(padx=40, fill='x')
        self.details_entry = tk.Entry(details_frame, font=APP_FONT1, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='flat')
        self.details_entry.pack(padx=40, pady=(0,10), fill='x')

        # Date Entry Box
        date_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        date_frame.pack(fill='x', pady=10, padx=10)
        date_label = tk.Label(date_frame, text="Date", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        date_label.pack(padx=40, fill='x')
        self.date_entry = tk.Entry(date_frame, font=APP_FONT1, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='flat')
        self.date_entry.pack(padx=40, pady=(0,10), fill='x')
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

        # Opening Balance Entry Box
        balance_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        balance_frame.pack(fill='x', pady=10, padx=10)
        balance_label = tk.Label(balance_frame, text="Opening Balance", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        balance_label.pack(padx=40, fill='x')
        self.balance_entry = tk.Entry(balance_frame, font=APP_FONT1, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='flat')
        self.balance_entry.pack(padx=40, pady=(0,10), fill='x')
        
        # Status Entry Box
        status_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        status_frame.pack(fill='x', pady=10, padx=10)
        status_label = tk.Label(status_frame, text="Status", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        status_label.pack(padx=40, fill='x')
        self.status_entry = tk.Entry(status_frame, font=APP_FONT1, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='flat')
        self.status_entry.insert(0, "New Account")
        self.status_entry.pack(padx=40, pady=(0,10), fill='x')
        self.pm_entry = tk.Entry(status_frame, font=APP_FONT1, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='flat')
        self.pm_entry.insert(0, "p")
        self.pm_entry.pack(padx=40, pady=(0,10), fill='x')

        # Add Account Button
        button_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        button_frame.pack(fill='x', pady=(10,0), padx=10)
        self.add_button = tk.Button(button_frame, text="Add Account", font=APP_FONT1, command=self.add_account, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_3, relief='groove')
        self.add_button.pack(padx=40, fill='x', pady=(10, 10))


    def add_account(self):
        name = self.name_entry.get().upper()
        date = self.date_entry.get().upper()
        details = self.details_entry.get().upper()
        opening_balance = self.balance_entry.get()
        status_entry = self.status_entry.get().upper()
        pm_entry = self.pm_entry.get().upper()

        # verify entry
        if name and date and details and status_entry and pm_entry:
            a = accounts.add_new_customer(name, details)
            accounts.add_customer_transaction(a, date, status_entry, opening_balance, pm_entry)
            dailynote = f"01 = {name}, {date}, {details}, {opening_balance}, {status_entry}, {pm_entry}"
            database.add_note_to_date(dailynote)

            if __name__ != "__main__":
                self.master.master.set_status(f"Account added: {a}")

        else:
            if __name__ == "__main__":
                print("Some fields are empty")
            else:
                self.master.master.set_status("[-]|Some fields are empty|")

        # add account to database
        # (code for this would depend on how you implemented your accounts database)


if __name__ == "__main__":
    app = tk.Tk()
    app.state("zoomed")
    a = AccountPage(app)
    a.pack(expand=1, fill="both")
    app.mainloop()
