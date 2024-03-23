import tkinter as tk
import tkinter.ttk as ttk
import re
from mytheme import Colors
from datetime import datetime


import accounts
import inventory
import database

class SalesPage(tk.Frame):
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
        title_name_label = tk.Label(title_frame, text="Sales", font="Consolas 18", bg=Colors.BACKGROUND1, fg=Colors.FG_SHADE_3, anchor='center')
        title_name_label.pack(padx=40, fill='x')

        # Date Entry Box
        date_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        date_frame.pack( fill='x', pady=10, padx=10)
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
        self.account_dropdown.pack(padx=40, pady=(0, 10), fill='x')
        self.account_dropdown.bind('<Enter>', lambda e: self.account_dropdown.config(values=self.get_accounts()))
        self.account_dropdown.bind('<Down>', lambda e: self.update_listbox_items(self.account_dropdown, self.get_accounts(), self.account_dropdown.get().upper()))

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
        self.item_dropdown.bind('<<ComboboxSelected>>', lambda e : self.set_price())

        # Quantity Entry Box
        quantity_frame  = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        quantity_frame.pack( fill='x', pady=10, padx=10)
        quantity_label = tk.Label(quantity_frame, text="Quantity", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        quantity_label.pack(padx=40, fill='x')
        self.quantity_entry = tk.Entry(quantity_frame, font="Consolas 14", bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='flat')
        self.quantity_entry.pack(padx=40, pady=(0, 10), fill='x')

        # Price Entry Box
        price_frame  = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        price_frame.pack( fill='x', pady=10, padx=10)
        price_label = tk.Label(price_frame, text="Price", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        price_label.pack(padx=40, fill='x')
        self.price_entry = tk.Entry(price_frame, font="Consolas 14", bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='flat')
        self.price_entry.pack(padx=40, pady=(0, 10), fill='x')


        # Item Dropdown Menu
        tag_frame  = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        tag_frame.pack( fill='x', pady=10, padx=10)
        tag_label = tk.Label(tag_frame, text="Tag", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        tag_label.pack(padx=40, fill='x')
        tag_choices = ["0 Set Nill", "1 Normal", "2 No interest"]
        self.tag_dropdown = ttk.Combobox(tag_frame, values=tag_choices, font="Consolas 14")
        self.tag_dropdown.pack(padx=40, pady=(0, 10), fill='x')
        self.tag_dropdown.set("1 Normal")


        # Sale recieve Button
        sale_button_frame  = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        sale_button_frame.pack( fill='x', pady=10, padx=10)
        sale_button = tk.Button(sale_button_frame, text="Sale", font="Consolas 14", command=self.sale, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_3, relief='groove')
        sale_button.pack(padx=40, fill='x', pady=(10, 20))
        recieve_button = tk.Button(sale_button_frame, text="Recieve", font="Consolas 14", command=self.recieve, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_3, relief='groove')
        recieve_button.pack(padx=40, fill='x', pady=(0, 10))

    def update_listbox_items(self, lb, lst, pat):
        lsts = []
        # print(lb,lst, pat)
        for i in lst:
            if re.search(pat, f"{i[0]} {i[1]}"):
                lsts.append(i)
        lb.config(values=lsts)

    def get_items_from_inventory(self):
        item_list = inventory.get_all_items()
        # code to fetch items from inventory database
        # replace this with actual code to fetch items from your database
        return item_list

    def get_accounts(self):
        accoount_list = accounts.get_all_customers()
        # code to fetch accounts from accounts database
        # replace this with actual code to fetch accounts from your database
        return accoount_list
    
    def set_price(self):
        item_name = self.item_dropdown.get()
        last_value = item_name.split()[-1]
        self.price_entry.delete(0, tk.END) 
        self.price_entry.insert(0, last_value)
        # self.price_entry.setvar(last_value)
        # print(last_value)

    def sale(self):
        # date item account quatity price
        date = self.date_entry.get()
        item_name = self.item_dropdown.get()
        account_name = self.account_dropdown.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        tag_value = self.tag_dropdown.get()
        # print(date, item_id,account_id, quantity, price)
        if date and item_name and account_name and quantity and price and tag_value:
            item_id = item_name.split()[0]
            account_id = account_name.split()[0]
            if "{" in account_name:
                aname = account_name.split("{")[1].split("}")[0]
            else:
                aname = account_name
            if "{" in item_name:    
                iname = item_name.split("{")[1].split("}")[0]
            else:
                iname = item_name

            
            # to account
            tagint = tag_value[0]
            detail = f"{quantity} = {iname}"
            amount = int(price) * float(quantity)
            if tagint == "0":pass
            
            else:
                accounts.add_customer_transaction(account_id, date, detail, amount, "P" , tagint)

            
            # update inventory
            inventory.add_item_transaction(item_id, date, 0, int(float(quantity)), aname)
            inventory.set_last_value(item_id, price)

            # daily note
            note = f"03 = {date}, {iname}, {aname}, {quantity}, {price}, {tagint}"
            note_id = database.add_note_to_date(note)

            if __name__ != "__main__":
                self.master.master.set_status(f"{note_id} Note {note}")
        else:
            pass
    
    def recieve(self):
        # date item account quatity price
        date = self.date_entry.get()
        item_name = self.item_dropdown.get()
        account_name = self.account_dropdown.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        # print(date, item_id,account_id, quantity, price)
        if date and item_name and account_name and quantity and price:
            item_id = item_name.split()[0]
            account_id = account_name.split()[0]
            # aname = account_name.split("{")[1].split("}")[0]
            # iname = item_name.split("{")[1].split("}")[0]

            if "{" in account_name:
                aname = account_name.split("{")[1].split("}")[0]
            else:
                aname = account_name
            if "{" in item_name:    
                iname = item_name.split("{")[1].split("}")[0]
            else:
                iname = item_name
            
            # to account
            detail = f"{quantity} = {iname}"
            amount = int(price) * float(quantity)
            accounts.add_customer_transaction(account_id, date, detail, amount, "M" )
            
            # update inventory
            inventory.add_item_transaction(item_id, date, int(float(quantity)), 0, aname)
            inventory.set_last_value(item_id, price)

            # daily note
            note = f"04 = {date}, {iname}, {aname}, {quantity}, {price}"
            note_id = database.add_note_to_date(note)

            if __name__ != "__main__":
                self.master.master.set_status(f"{note_id} Note {note}")
        else:
            pass
        
            


if __name__ == "__main__":
    app = tk.Tk()
    app.state("zoomed")
    h = SalesPage(app)
    h.pack(expand=1, fill="both")
    app.mainloop()
