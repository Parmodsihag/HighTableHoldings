import tkinter as tk
# from tkinter import ttk
from datetime import datetime

from mytheme import Colors

# import accounts
import inventory
import database
# from inventory import
# from sales import Sales

class AddItemsPage(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=Colors.BACKGROUND1, **kwargs)

        APP_FONT = "Consolas 12"
        APP_FONT1 = "Consolas 14"

        img = tk.PhotoImage(file="myicons\\framebg2.png")

        self.background_title = tk.Label(self, image=img)
        self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.img = img


        # main frame to include all frames
        self.main_frame = tk.Frame(self, bg=Colors.BACKGROUND1)
        self.main_frame.place(relx=0.3, rely=0.01, relwidth=.4, relheight=.98)


        self.background_title = tk.Label(self.main_frame, image=img)
        self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)


        # title frame
        title_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND1)
        title_frame.pack(fill='x', pady=2, padx=10)
        title_name_label = tk.Label(title_frame, text="Items", font="Consolas 18", bg=Colors.BACKGROUND1, fg=Colors.FG_SHADE_3, anchor='center')
        title_name_label.pack(padx=40, fill='x')

        # Name Entry Box
        name_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        name_frame.pack(fill='x', pady=10, padx=10)

        name_label = tk.Label(name_frame, text="Item Name: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        name_label.pack(padx=40, fill='x')
        self.name_entry = tk.Entry(name_frame, font=APP_FONT1, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='flat')
        self.name_entry.pack(padx=40, pady=(0,10), fill='x')

        # Other Details Entry Box
        details_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        details_frame.pack(fill='x', pady=10, padx=10)
        details_label = tk.Label(details_frame, text="Source: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        details_label.pack(padx=40, fill='x')
        self.details_entry = tk.Entry(details_frame, font=APP_FONT1, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='flat')
        self.details_entry.pack(padx=40, pady=(0,10), fill='x')

        # Date Entry Box
        date_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        date_frame.pack(fill='x', pady=10, padx=10)
        date_label = tk.Label(date_frame, text="Date: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        date_label.pack(padx=40, fill='x')
        self.date_entry = tk.Entry(date_frame, font=APP_FONT1, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='flat')
        self.date_entry.pack(padx=40, pady=(0,10), fill='x')
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

        # Opening Balance Entry Box
        balance_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        balance_frame.pack(fill='x', pady=10, padx=10)
        balance_label = tk.Label(balance_frame, text="Opening Balance: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        balance_label.pack(padx=40, fill='x')
        self.balance_entry = tk.Entry(balance_frame, font=APP_FONT1, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='flat')
        self.balance_entry.pack(padx=40, pady=(0,10), fill='x')

        # Stock Value Entry Box
        stock_value_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        stock_value_frame.pack(fill='x', pady=10, padx=10)
        stock_value_label = tk.Label(stock_value_frame, text="Stock Value: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        stock_value_label.pack(padx=40, fill='x')
        self.stock_value_entry = tk.Entry(stock_value_frame, font=APP_FONT1, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='flat')
        self.stock_value_entry.pack(padx=40, pady=(0,10), fill='x')

        # Last Value Entry Box
        last_value_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        last_value_frame.pack(fill='x', pady=10, padx=10)
        last_value_label = tk.Label(last_value_frame, text="Last Value: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        last_value_label.pack(padx=40, fill='x')
        self.last_value_entry = tk.Entry(last_value_frame, font=APP_FONT1, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='flat')
        self.last_value_entry.pack(padx=40, pady=(0,10), fill='x')
        
        # Status Entry Box
        # status_frame = tk.Frame(self, bg=Colors.ACTIVE_BACKGROUND)
        # status_frame.pack(pady=10)
        # status_label = tk.Label(status_frame, text="Status: ", font=APP_FONT, bg=Colors.ACTIVE_BACKGROUND)
        # status_label.pack(side="left")
        # self.status_entry = tk.Entry(status_frame, font=APP_FONT, bg=Colors.ACTIVE_BACKGROUND)
        # self.status_entry.insert(0, "New Account")
        # self.status_entry.pack(side="left")
        # self.pm_entry = tk.Entry(status_frame, font=APP_FONT, bg=Colors.ACTIVE_BACKGROUND)
        # self.pm_entry.insert(0, "p")
        # self.pm_entry.pack(side="left")

        # Add Item Button
        button_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        button_frame.pack(fill='x', pady=(10,0), padx=10)
        self.add_button = tk.Button(button_frame, text="Add Item", font=APP_FONT, command=self.add_item, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_3, relief='groove')
        self.add_button.pack(padx=40, fill='x', pady=(10, 10))


    def add_item(self):
        name = self.name_entry.get().upper()
        date = self.date_entry.get().upper()
        details = self.details_entry.get().upper()
        opening_balance = self.balance_entry.get()
        stock_value = self.stock_value_entry.get()
        last_value = self.last_value_entry.get()

        # verify entry
        if name and date and details:
            item_id = inventory.add_new_item(name, stock_value,last_value)
            inventory.add_item_transaction(item_id,date, opening_balance, 0, details)

            dailynote = f"02 = {name}, {date}, {stock_value}, {details}, {opening_balance}, {last_value}"
            database.add_note_to_date(dailynote)

            if __name__ != "__main__":
                self.master.master.set_status(f"Item added: {item_id}")

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
    a = AddItemsPage(app)
    a.pack(expand=1, fill="both")
    app.mainloop()
