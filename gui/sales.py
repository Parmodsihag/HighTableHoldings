import tkinter as tk
import tkinter.ttk as ttk
import re
from .mytheme import Colors
from datetime import datetime
from .searchbar import SearchBar

from database import accounts, inventory, database
# import accounts
# import inventory
# import database

class SalesPage(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # main frame to include all frames
        self.main_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        self.main_frame.place(relx=0.3, rely=0.01, relwidth=.4, relheight=.98)

        # title frame
        title_name_label = tk.Label(self.main_frame, text="Sales", font="Consolas 18", bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_3, anchor='center')
        title_name_label.pack(pady=10, fill='x')

        # Date Entry Box
        date_label = tk.Label(self.main_frame, text="Date", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        date_label.pack(padx=40, fill='x')
        today_date = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.date_entry = tk.Entry(self.main_frame, textvariable=today_date, font="Consolas 14", bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.date_entry.pack(padx=40, pady=(0,10), fill='x')

        # Account Dropdown Menu
        account_label = tk.Label(self.main_frame, text="Account", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        account_label.pack(padx=40, pady=(20,0), fill='x')
        account_choices = self.get_accounts()
        self.account_dropdown = SearchBar(self.main_frame, data=account_choices)
        self.account_dropdown.pack(padx=40, pady=(0, 10), fill='x')
        self.account_dropdown.search_bar.bind('<Enter>', lambda e: self.account_dropdown.set_data(self.get_accounts()))

        # Item Dropdown Menu
        item_label = tk.Label(self.main_frame, text="Item", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        item_label.pack(padx=40, pady=(20, 0), fill='x')
        self.item_choices = self.get_items_from_inventory()
        self.item_dropdown = SearchBar(self.main_frame, data=self.item_choices)
        self.item_dropdown.pack(padx=40, pady=(0, 10), fill='x')
        self.item_dropdown.search_bar.bind('<Enter>', lambda e: self.item_dropdown.set_data(self.get_items_from_inventory()))
        self.item_dropdown.search_bar.bind('<FocusOut>', lambda e: self.set_price())

        # Quantity Entry Box
        quantity_label = tk.Label(self.main_frame, text="Quantity", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        quantity_label.pack(padx=40, pady=(20,0), fill='x')
        self.quantity_entry = tk.Entry(self.main_frame, font="Consolas 14", bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.quantity_entry.pack(padx=40, pady=(0, 10), fill='x')

        # Price Entry Box
        price_label = tk.Label(self.main_frame, text="Price", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        price_label.pack(padx=40, pady=(20,0), fill='x')
        self.price_entry = tk.Entry(self.main_frame, font="Consolas 14", bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.price_entry.pack(padx=40, pady=(0, 10), fill='x')


        # Item Dropdown Menu
        tag_label = tk.Label(self.main_frame, text="Tag", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        tag_label.pack(padx=40, pady=(20,0), fill='x')
        tag_choices = ["0 Set Nill", "1 Normal", "2 No interest"]
        self.tag_dropdown = ttk.Combobox(self.main_frame, values=tag_choices, font="Consolas 14")
        self.tag_dropdown.pack(padx=40, pady=(0, 10), fill='x')
        self.tag_dropdown.set("1 Normal")


        # Sale recieve Button
        sale_button_frame  = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        sale_button_frame.pack( fill='x', pady=10, padx=0)
        sale_button = tk.Button(sale_button_frame, text="Sale", font="Consolas 14", command=self.sale, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_3, relief='solid')
        sale_button.pack(padx=(40,5), fill='x', pady=20, side='left', expand=1)
        recieve_button = tk.Button(sale_button_frame, text="Recieve", font="Consolas 14", command=self.receive, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_3, relief='solid')
        recieve_button.pack(padx=(5, 40), fill='x', pady=20, side='right', expand=1)

    def update_listbox_items(self, lb, lst, pat):
        lsts = []
        # print(lb,lst, pat)
        for i in lst:
            if re.search(pat, f"{i[0]} {i[1]}"):
                lsts.append(i)
        lb.config(values=lsts)

    def get_items_from_inventory(self):
        """Fetches items from the inventory, formatting for the search bar."""
        item_list = inventory.get_all_items()
        return [f"{i[0]} {i[1]} {i[5]}" for i in item_list]  # Format for SearchBar 

    def get_accounts(self):
        """Fetches accounts, formatting them for the search bar."""
        account_list = accounts.get_all_customers()
        return [f"{i[0]} {i[1]} {i[2]}" for i in account_list] 
    
    def set_price(self):
        self.item_dropdown.hide_listbox(1)
        item_name = self.item_dropdown.get_text()
        if item_name in self.item_choices:
            item_id = item_name.split()[0]
            last_value = inventory.get_last_value(item_id)
            self.price_entry.delete(0, tk.END) 
            self.price_entry.insert(0, last_value)

    def _get_transaction_data(self):
        """Retrieves and validates transaction data from input fields."""
        date = self.date_entry.get()
        item_name = self.item_dropdown.get_text().strip()
        account_name = self.account_dropdown.get_text()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        tag_value = self.tag_dropdown.get()

        if not all([date, item_name, account_name, quantity, price, tag_value]):
            return None  # Indicate missing data 

        item_exists = self._check_item_exists(item_name)
        if item_exists:
            item_id, iname = item_name.split(" ", 1) # Split and unpack
            item_id = int(item_id)
        else:
            item_id = -1
            iname = item_name
        account_id, aname = account_name.split(" ", 1)
        account_id = int(account_id)

        tagint = int(tag_value[0])  # Convert to integer
        amount = float(price) * float(quantity)
        detail = f"{quantity} = {iname}"

        return date, item_id, account_id, iname, aname, quantity, price, tagint, amount, detail

    def _process_transaction(self, transaction_type): 
        """Processes sales (P) or receive (M) transactions."""

        data = self._get_transaction_data()
        if data is None:
            if __name__ != "__main__":
                self.master.master.set_status("[-]|Some fields are empty|")
            return 

        date, item_id, account_id, iname, aname, quantity, price, tagint, amount, detail = data

        if tagint == 0:
            self._handle_settlement(account_id, date, detail, amount, transaction_type) 
        else:
            accounts.add_customer_transaction(account_id, date, detail, amount, transaction_type, tagint)

        if item_id != -1:  # Update inventory only if the item exists
            inventory.add_item_transaction(item_id, date,
                                        int(float(quantity)) if transaction_type == "M" else 0,
                                        int(float(quantity)) if transaction_type == "P" else 0,
                                        aname)
            inventory.set_last_value(item_id, int(price)) 

        note_id = self._add_daily_note(date, iname, aname, quantity, price, tagint, transaction_type)

        if __name__ != "__main__":
            if item_id == -1:
                self.master.master.set_status(f"Success (inventory may not be updated). Note ID: {note_id}")
            else:
                self.master.master.set_status(f"Success! Note ID: {note_id}")


    def _handle_settlement(self, account_id, date, detail, amount, transaction_type):
        """Handles account settlements (Tag = 0)."""
        total_amount = accounts.get_account_balance(account_id)  # Before adding new transaction
        discount = total_amount + amount if transaction_type == "P" else (total_amount - amount) 

        accounts.add_customer_transaction(account_id, date, detail, amount, transaction_type, 0) # original transaction
        accounts.add_customer_transaction(account_id, date, "Settled Amount", total_amount, "M" , 0)  # record settled amount 
        accounts.add_customer_transaction(account_id, date, "Discount", discount, "M", 0)  # record discount (if any)

    def _check_item_exists(self, item_name):
        """Checks if the complete item string exists in the choices."""
        return item_name in self.item_choices  


    def _add_daily_note(self, date, iname, aname, quantity, price, tagint, transaction_type):
        """Adds a note to the daily_notes database."""
        note = (
            f"03 = {date}, {iname}, {aname}, {quantity}, {price}, {tagint}"
            if transaction_type == "P" 
            else f"04 = {date}, {iname}, {aname}, {quantity}, {price}, {tagint}"
        )
        return database.add_note_to_date(note)

    def sale(self):
        """Handles sale transactions."""
        self._process_transaction("P")

    def receive(self):
        """Handles receive transactions."""
        self._process_transaction("M") 
            


if __name__ == "__main__":
    app = tk.Tk()
    app.state("zoomed")
    h = SalesPage(app)
    h.pack(expand=1, fill="both")
    app.mainloop()
