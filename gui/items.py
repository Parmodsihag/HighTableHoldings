import tkinter as tk
# from tkinter import ttk
from datetime import datetime

from .mytheme import Colors

from database import inventory, database
# import accounts
# import inventory
# import database
# from inventory import
# from sales import Sales

class AddItemsPage(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        APP_FONT = "Consolas 12"
        APP_FONT1 = "Consolas 14"

        # img = tk.PhotoImage(file="myicons\\framebg2.png")

        # self.background_title = tk.Label(self, image=img)
        # self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)

        # self.img = img


        # main frame to include all frames
        self.main_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        self.main_frame.place(relx=0.2, rely=0.01, relwidth=.6, relheight=.98)


        # self.background_title = tk.Label(self.main_frame, image=img)
        # self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)


        # title frame
        title_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND1)
        title_frame.pack(fill='x', pady=2, padx=10)
        title_name_label = tk.Label(title_frame, text="Items", font="Consolas 18", bg=Colors.BACKGROUND1, fg=Colors.FG_SHADE_3, anchor='center')
        title_name_label.pack(padx=40, fill='x')

        # GROUP 1
        frame1 = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        frame1.pack(fill='x', pady=(10,0), padx=10)
        # Name Entry Box
        name_frame = tk.Frame(frame1, bg=Colors.BACKGROUND)
        name_frame.pack(fill='x', side='left', expand=1)
        name_label = tk.Label(name_frame, text="Item Name: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        name_label.pack(fill='x', padx=(40, 10), pady=(10,0))
        self.name_entry = tk.Entry(name_frame, font=APP_FONT1, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.name_entry.pack(fill='x', padx=(40, 10), pady=(0,10))
        # Other Details Entry Box
        details_frame = tk.Frame(frame1, bg=Colors.BACKGROUND)
        details_frame.pack(fill='x', side='left', expand=1)
        details_label = tk.Label(details_frame, text="Source: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        details_label.pack(fill='x')
        self.details_entry = tk.Entry(details_frame, font=APP_FONT1, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.details_entry.pack(fill='x', padx=(0,40))

        # GROUP 2
        frame2 = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        frame2.pack(fill='x', pady=0, padx=10)
        # Date Entry Box
        date_frame = tk.Frame(frame2, bg=Colors.BACKGROUND)
        date_frame.pack(fill='x', side='left', expand=1)
        date_label = tk.Label(date_frame, text="Date: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        date_label.pack(fill='x', padx=(40,10), pady=(10,0))
        self.date_entry = tk.Entry(date_frame, font=APP_FONT1, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.date_entry.pack(fill='x', padx=(40,10), pady=(0,10))
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        # Opening Balance Entry Box
        balance_frame = tk.Frame(frame2, bg=Colors.BACKGROUND)
        balance_frame.pack(fill='x', side='left', expand=1)
        balance_label = tk.Label(balance_frame, text="Opening Balance: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        balance_label.pack(fill='x')
        self.balance_entry = tk.Entry(balance_frame, font=APP_FONT1, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.balance_entry.pack(padx=(0, 40), fill='x')

        # GROUP 3
        frame3 = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        frame3.pack(fill='x', pady=0, padx=10)
        # stock value
        stock_value_frame = tk.Frame(frame3, bg=Colors.BACKGROUND)
        stock_value_frame.pack(fill='x', side='left', expand=1)
        stock_value_label = tk.Label(stock_value_frame, text="Stock Value: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        stock_value_label.pack(fill='x', padx=(40, 10), pady=(10, 0))
        self.stock_value_entry = tk.Entry(stock_value_frame, font=APP_FONT1, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.stock_value_entry.pack(fill='x', padx=(40, 10), pady=(0,10))
        # Last Value Entry Box
        last_value_frame = tk.Frame(frame3, bg=Colors.BACKGROUND)
        last_value_frame.pack(fill='x', side='left', expand=1)
        last_value_label = tk.Label(last_value_frame, text="Last Value: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        last_value_label.pack(fill='x')
        self.last_value_entry = tk.Entry(last_value_frame, font=APP_FONT1, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.last_value_entry.pack(padx=(0, 40), fill='x')

        # GROUP 4
        frame4 = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        frame4.pack(fill='x', pady=0, padx=10)
        # pakka kacha
        pk_frame = tk.Frame(frame4, bg=Colors.BACKGROUND)
        pk_frame.pack(fill='x', side='left', expand=1)
        pk_label = tk.Label(pk_frame, text="Pakka Kacha: [P/K] ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        pk_label.pack(fill='x', padx=(40, 10), pady=(10, 0))
        self.pk_entry = tk.Entry(pk_frame, font=APP_FONT1, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.pk_entry.pack(fill='x', padx=(40, 10), pady=(0,10))
        self.pk_entry.insert(0, 'P')
        # GST Value Entry Box
        gst_value_frame = tk.Frame(frame4, bg=Colors.BACKGROUND)
        gst_value_frame.pack(fill='x', side='left', expand=1)
        gst_value_label = tk.Label(gst_value_frame, text="GST Value: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        gst_value_label.pack(fill='x')
        self.gst_value_entry = tk.Entry(gst_value_frame, font=APP_FONT1, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.gst_value_entry.pack(padx=(0, 40), fill='x')

        # GROUP 5
        frame5 = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        frame5.pack(fill='x', pady=0, padx=10)
        # pakka kacha
        batch_frame = tk.Frame(frame5, bg=Colors.BACKGROUND)
        batch_frame.pack(fill='x', side='left', expand=1)
        batch_label = tk.Label(batch_frame, text="Batch: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        batch_label.pack(fill='x', padx=(40, 10), pady=(10, 0))
        self.batch_entry = tk.Entry(batch_frame, font=APP_FONT1, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.batch_entry.pack(fill='x', padx=(40, 10), pady=(0,10))
        self.batch_entry.insert(0, 'NA')
        # GST Value Entry Box
        expiry_frame = tk.Frame(frame5, bg=Colors.BACKGROUND)
        expiry_frame.pack(fill='x', side='left', expand=1)
        expiry_label = tk.Label(expiry_frame, text="Expiry: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        expiry_label.pack(fill='x')
        self.expiry_value_entry = tk.Entry(expiry_frame, font=APP_FONT1, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.expiry_value_entry.pack(padx=(0, 40), fill='x')
        self.expiry_value_entry.insert(0, 'NA')

        # GROUP 6
        frame6 = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        frame6.pack(fill='x', pady=0, padx=10)
        # pakka kacha
        unit_frame = tk.Frame(frame6, bg=Colors.BACKGROUND)
        unit_frame.pack(fill='x', side='left', expand=1)
        unit_label = tk.Label(unit_frame, text="Unit: ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        unit_label.pack(fill='x', padx=(40, 10), pady=(10, 0))
        self.unit_entry = tk.Entry(unit_frame, font=APP_FONT1, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.unit_entry.pack(fill='x', padx=(40, 10), pady=(0,10))
        self.unit_entry.insert(0, 'PCS')
        # GST Value Entry Box
        type_value_frame = tk.Frame(frame6, bg=Colors.BACKGROUND)
        type_value_frame.pack(fill='x', side='left', expand=1)
        type_value_label = tk.Label(type_value_frame, text="Type: [F, P, S, O] ", font=APP_FONT, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        type_value_label.pack(fill='x')
        self.type_value_entry = tk.Entry(type_value_frame, font=APP_FONT1, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.type_value_entry.pack(padx=(0, 40), fill='x')
        self.type_value_entry.insert(0, 'O')


        # Add Item Button
        button_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        button_frame.pack(fill='x', pady=(10,0), padx=10)
        self.add_button = tk.Button(button_frame, text="Add Item", font=APP_FONT, command=self.add_item, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_3, relief='solid')
        self.add_button.pack(padx=40, fill='x', pady=(10, 10))


    def add_item(self):
        name = self.name_entry.get().upper()
        date = self.date_entry.get().upper()
        details = self.details_entry.get().upper()
        opening_balance = self.balance_entry.get()
        stock_value = self.stock_value_entry.get()
        last_value = self.last_value_entry.get()
        pk_value = self.pk_entry.get().upper()
        gst_value = self.gst_value_entry.get()
        batch_value = self.batch_entry.get().upper()
        expiry_date = self.expiry_value_entry.get()
        unit_value = self.unit_entry.get().upper()
        type_value = self.type_value_entry.get().upper()

        # verify entry
        if name and date and details and pk_value and batch_value and expiry_date and unit_value and type_value:
            item_id = inventory.add_new_item(name, stock_value,last_value, unit_value, batch_value, expiry_date, gst_value, type_value, pk_value)
            inventory.add_item_transaction(item_id,date, opening_balance, 0, details)

            dailynote = f"02 = {name}, {date}, {stock_value}, {details}, {opening_balance}, {last_value} , {unit_value}, {batch_value}, {expiry_date}, {gst_value}, {type_value}, {pk_value}"
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
