import tkinter as tk
import re
# import sqlite3

from bills import bill_db
# import inventory
import inventory
from bills import randombillgen

from tkinter import ttk
from mytheme import Colors
from datetime import datetime

class BillPage(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.Colors = Colors

        # img = tk.PhotoImage(file="myicons\\framebg2.png")

        # self.background_title = tk.Label(self, image=img)
        # self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)

        # self.img = img

        # main frame to include all frames
        self.main_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        self.main_frame.place(relx=0.1, rely=0.01, relwidth=.4, relheight=.98)

        # self.background_title = tk.Label(self.main_frame, image=img)
        # self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)



        # title frame
        title_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND1)
        title_frame.pack(fill='x', pady=2, padx=10)
        title_name_label = tk.Label(title_frame, text="Bills", font="Consolas 18", bg=Colors.BACKGROUND1, fg=Colors.FG_SHADE_3, anchor='center')
        title_name_label.pack(padx=40, fill='x')

        # Date Entry Box
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        month_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        month_frame.pack(fill='x', pady=10, padx=10)
        month_label = tk.Label(month_frame, text="Month", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        month_label.pack(padx=40, fill='x')
        self.month_dropdown = ttk.Combobox(month_frame, values=months, font="Consolas 14")
        self.month_dropdown.pack(padx=40, pady=(0,10), fill='x')
        self.month_dropdown.bind('<<ComboboxSelected>>', lambda e : self.set_start_date())

        
        year_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        year_frame.pack(fill='x', pady=10, padx=10)
        year_label = tk.Label(year_frame, text="Year", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        year_label.pack(padx=40, fill='x')
        self.year_entry = tk.Entry(year_frame, font="Consolas 14", bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.year_entry.pack(padx=40, pady=(0,10), fill='x')
        self.year_entry.insert(0, 2024)

        # Item Dropdown Menu
        item_frame  = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        item_frame.pack( fill='x', pady=10, padx=10)
        item_label = tk.Label(item_frame, text="Item", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        item_label.pack(padx=40, fill='x')
        item_choices = self.get_items_from_inventory()
        self.item_dropdown = ttk.Combobox(item_frame, values=item_choices, font="Consolas 14")
        self.item_dropdown.pack(padx=40, pady=(0, 10), fill='x')
        self.item_dropdown.bind('<Enter>', lambda e: self.item_dropdown.config(values=self.get_items_from_inventory()))
        self.item_dropdown.bind('<Down>', lambda e: self.update_listbox_items(self.item_dropdown, self.get_items_from_inventory(), self.item_dropdown.get().upper()))
        # self.item_dropdown.bind('<<ComboboxSelected>>', lambda e : self.set_start_date())

        quantity_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        quantity_frame.pack(fill='x', pady=10, padx=10)
        quantity_label = tk.Label(quantity_frame, text="Quantity", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        quantity_label.pack(padx=40, fill='x')
        self.quantity_entry = tk.Entry(quantity_frame, font="Consolas 14", bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.quantity_entry.pack(padx=40, pady=(0,10), fill='x')

        start_date_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        start_date_frame.pack(fill='x', pady=10, padx=10)
        start_date_label = tk.Label(start_date_frame, text="Start Date", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        start_date_label.pack(padx=40, fill='x')
        self.start_date = tk.StringVar()
        self.start_date_entry = tk.Entry(start_date_frame, textvariable=self.start_date, font="Consolas 14", bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.start_date_entry.pack(padx=40, pady=(0,10), fill='x')

        # button frame
        button_frame2 = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        button_frame2.pack(fill='x', pady=(10,0), padx=10)
        add_button = tk.Button(button_frame2, text="Add", font="Consolas 14", command=self.add_item, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_3, relief='solid')
        add_button.pack(padx=40, fill='x', pady=(10, 10))


        self.main_frame2 = tk.Frame(self, bg=Colors.BACKGROUND)
        self.main_frame2.place(relx=0.5, rely=0.01, relwidth=.4, relheight=.98)
        
        # self.background_title = tk.Label(self.main_frame2, image=img)
        # self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)
        
        # title frame2
        title_frame2 = tk.Frame(self.main_frame2, bg=Colors.BACKGROUND1)
        title_frame2.pack(fill='x', pady=2, padx=10)
        title_name_label2 = tk.Label(title_frame2, text="SHOW", font="Consolas 18", bg=Colors.BACKGROUND1, fg=Colors.FG_SHADE_3, anchor='center')
        title_name_label2.pack(padx=40, fill='x')

        show_frame  = tk.Frame(self.main_frame2, bg=Colors.BACKGROUND)
        show_frame.pack( fill='x', pady=10, padx=10)
        show_label = tk.Label(show_frame, text="Year Month", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        show_label.pack(padx=40, fill='x')
        show_choices = bill_db.get_all_month_years()
        self.show_dropdown = ttk.Combobox(show_frame, values=show_choices, font="Consolas 14")
        self.show_dropdown.pack(padx=40, pady=(0, 10), fill='x')
        self.show_dropdown.bind('<Enter>', lambda e: self.show_dropdown.config(values=bill_db.get_all_month_years()))
        self.show_dropdown.bind('<Down>', lambda e: self.update_listbox_items(self.show_dropdown, bill_db.get_all_month_years(), self.show_dropdown.get().upper()))
        self.show_dropdown.bind('<<ComboboxSelected>>', lambda e : self.show_table())

        start_bill_frame = tk.Frame(self.main_frame2, bg=Colors.BACKGROUND)
        start_bill_frame.pack(fill='x', pady=10, padx=10)
        start_bill_label = tk.Label(start_bill_frame, text="Start bill number", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        start_bill_label.pack(padx=40, fill='x')
        self.start_bill_entry = tk.Entry(start_bill_frame, font="Consolas 14", bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.start_bill_entry.pack(padx=40, pady=(0,10), fill='x')

        listbox_frame = tk.Frame(self.main_frame2, bg= Colors.BACKGROUND)
        listbox_frame.pack( fill='both', expand=1, pady=10, padx=10)
        # listbox_label = tk.Label(listbox_frame, text="Year Month", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        # listbox_label.pack(padx=40, fill='x')
        self.listbox = tk.Listbox(listbox_frame, bg= Colors.BACKGROUND, font="Ubantu 12", relief='solid', bd=4)
        self.listbox.pack(fill='both', expand=1)

        # button frame
        button_frame3 = tk.Frame(self.main_frame2, bg=Colors.BACKGROUND)
        button_frame3.pack(fill='x', pady=(10,10), padx=10)
        add_button = tk.Button(button_frame3, text="Genrate bills", font="Consolas 14", command=self.genrate_bills, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_3, relief='solid')
        add_button.pack(padx=(40, 10), fill='x', pady=10, side='left', expand=1)
        add_button = tk.Button(button_frame3, text="Delete bills", font="Consolas 14", command=self.delete_bills, bg=Colors.DELETE, fg=Colors.FG_SHADE_3, relief='solid')
        add_button.pack(padx=(10, 40), fill='x', pady=10, side='right', expand=1)

    def genrate_bills(self):
        year_month = self.show_dropdown.get()
        start_bill_number = int(self.start_bill_entry.get())
        if year_month:
            if bill_db.check_bills_exist_for_month_year(year_month):
                print(f'[-] Bills for {year_month} already exists')
            else:
                status = randombillgen.make_bills(year_month, 80, start_bill_number)
                if status:
                    if __name__ != "__main__":
                        self.master.master.set_status(f"Bills genrated sucessfully: {year_month}")
                    print(f'[+] bills for {year_month} genrated sucessfully')
                else:
                    if __name__ != "__main__":
                        self.master.master.set_status(f"Bills not genrated: {year_month}")
                    print(f'[-] bills for {year_month} can not be genrated')


    def delete_bills(self):
        year_month = self.show_dropdown.get()
        if year_month:
            if bill_db.check_bills_exist_for_month_year(year_month):
                bill_db.delete_bills_for_month_year(year_month)
                if __name__ != "__main__":
                    self.master.master.set_status(f"Bills deleted: {year_month}")
                print(f'[-] Bills for {year_month} deleted')
            else:
                if __name__ != "__main__":
                    self.master.master.set_status(f"Bills not exists: {year_month}")
                print(f'[-] Bills for {year_month} not exists')

    def show_table(self):
        self.listbox.delete(0, 'end')
        year_mon = self.show_dropdown.get()
        items_list = bill_db.get_items_by_month_year(year_mon)
        for item_index, item in enumerate(items_list):
            self.listbox.insert('end', item)
            if item_index % 2 == 0:
                self.listbox.itemconfig(item_index, background=self.Colors.BACKGROUND, foreground=self.Colors.ACTIVE_FOREGROUND)
            else:
                self.listbox.itemconfig(item_index, background=self.Colors.BACKGROUND1, foreground=self.Colors.ACTIVE_FOREGROUND)

    def add_item(self):
        month = self.month_dropdown.get()
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        month = months.index(month) + 1
        year = self.year_entry.get()
        item_details = self.item_dropdown.get()
        quantity = self.quantity_entry.get()
        start_date = self.start_date.get()
        if month and year and item_details and quantity and start_date:
            item_id = item_details.split()[0]
            item_details = inventory.get_item_by_id(item_id)
            name = item_details[1]
            unit = item_details[4]
            if month <10:
                month_year = f"{year}-0{month}"
            else:    
                month_year = f"{year}-{month}"
            rate = item_details[7]
            type1 = item_details[8]
            batch = item_details[5]
            exp = item_details[6]
            item_data = (name, unit, month_year, rate, type1, start_date, batch, exp, quantity)
            bill_db.insert_item(item_data)

    def set_start_date(self):
        month = self.month_dropdown.get()
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        month = months.index(month) + 1
        year = self.year_entry.get()

        self.start_date.set(f"{year}-{month}-01")


    def get_items_from_inventory(self):
        item_list = inventory.get_all_items()
        # code to fetch items from inventory database
        # replace this with actual code to fetch items from your database
        return item_list
    
    def update_listbox_items(self, lb, lst, pat):
        lsts = []
        # print(lb,lst, pat)
        for i in lst:
            if re.search(pat, f"{i[0]} {i[1]}"):
                lsts.append(i)
        lb.config(values=lsts)

if __name__ == "__main__":
    app = tk.Tk()
    app.state("zoomed")
    h = BillPage(app)
    h.pack(expand=1, fill="both")
    app.mainloop()
