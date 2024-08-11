        
import tkinter as tk

from .mytheme import Colors
from tkinter import ttk
from database import accounts, inventory, database, krar
# import accounts
# import inventory
# import database
# import krar
import sqlite3
from bills import bill_db

class ModifyPage(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        font = "Consolas 16"

        self.main_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        self.main_frame.place(relx=0.3, rely=0.01, relwidth=.4, relheight=.98)

        # title frame
        title_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND1)
        title_frame.pack(fill='x', pady=2, padx=10)
        title_name_label = tk.Label(title_frame, text="Modify Details", font="Consolas 18", bg=Colors.BACKGROUND1, fg=Colors.FG_SHADE_3, anchor='center')
        title_name_label.pack(padx=40, fill='x')

        # Database Dropdown Menu
        database_names = ["accounts.db", "daily_notes.db", "inventory.db", "krar.db", "bills.db"]
        account_frame  = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        account_frame.pack( fill='x', pady=10, padx=10)
        account_label = tk.Label(account_frame, text="Database", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        account_label.pack(padx=40, fill='x')
        self.db_dropdown = ttk.Combobox(account_frame, values=database_names, font="Consolas 14")
        self.db_dropdown.pack(padx=40, pady=(0, 10), fill='x')
        self.db_dropdown.bind('<<ComboboxSelected>>', lambda e : self.update_table_names())
        # self.account_dropdown.bind('<Enter>', lambda e: self.account_dropdown.config(values=self.get_accounts()))
        # self.account_dropdown.bind('<Down>', lambda e: self.update_listbox_items(self.account_dropdown, self.get_accounts(), self.account_dropdown.get().upper()))

        # Table Dropdown Menu
        self.table_list = []
        account_frame  = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        account_frame.pack( fill='x', pady=10, padx=10)
        account_label = tk.Label(account_frame, text="Table", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        account_label.pack(padx=40, fill='x')
        self.table_dropdown = ttk.Combobox(account_frame, values=self.table_list, font="Consolas 14")
        self.table_dropdown.pack(padx=40, pady=(0, 10), fill='x')


        # Row Entry
        date_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        date_frame.pack( fill='x', pady=10, padx=10)
        date_label = tk.Label(date_frame, text="Row ID", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        date_label.pack(padx=40, fill='x')
        self.row_id_var = tk.IntVar()
        self.row_id_entry = tk.Entry(date_frame, font="Consolas 14", textvariable=self.row_id_var, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.row_id_entry.pack(padx=40, pady=(0,10), fill='x')

        # Show Button
        sale_button_frame  = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        sale_button_frame.pack( fill='x', pady=10, padx=10)
        sale_button = tk.Button(sale_button_frame, text="Show", font="Consolas 14", command=self.show_row, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_3, relief='solid')
        sale_button.pack(padx=40, fill='x', pady=(10, 10))

        # modify row entry
        self.table_row = tk.StringVar()
        date_frame = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        date_frame.pack( fill='x', pady=10, padx=10)
        date_label = tk.Label(date_frame, text="Modify Row", font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        date_label.pack(padx=40, fill='x')
        self.modify_row_entry = tk.Entry(date_frame, font="Consolas 14", textvariable=self.table_row, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_1, relief='solid')
        self.modify_row_entry.pack(padx=40, pady=(0,10), fill='x')

        # Modify Button
        sale_button_frame  = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        sale_button_frame.pack( fill='x', pady=10, padx=10)
        sale_button = tk.Button(sale_button_frame, text="Modify", font="Consolas 14", command=self.modify_row_function, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_3, relief='solid')
        sale_button.pack(padx=40, fill='x', pady=(10, 10))

        # Delete Button
        sale_button_frame  = tk.Frame(self.main_frame, bg=Colors.BACKGROUND)
        sale_button_frame.pack( fill='x', pady=10, padx=10)
        sale_button = tk.Button(sale_button_frame, text="Delete", font="Consolas 14", command=self.delete_row_function, bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_3, relief='solid')
        sale_button.pack(padx=40, fill='x', pady=(10, 10))

        # # --------------------------------------------------------
        # self.upper_frame = tk.Frame(self, bg=Colors.ACTIVE_BACKGROUND)
        # # self.upper_frame.place(relx=0, rely=0, relheight=0.2, relwidth=1)
        # # self.table_selector()

        # self.table_frame = tk.Frame(self, bg=Colors.ACTIVE_BACKGROUND)
        # # self.table_frame.place(relx=0, rely=0.2, relheight=0.8, relwidth=1)

        # # self.table_row = tk.StringVar()

        # row_label = tk.Label(self.table_frame, text="Table Row", bg=Colors.ACTIVE_BACKGROUND, font=font)
        # row_label.place(relx=0.1, rely=0.1, relheight=0.1, relwidth=0.8)
        # row_entry = tk.Entry(self.table_frame, textvariable=self.table_row, font=font, bg=Colors.ACTIVE_BACKGROUND)
        # row_entry.place(relx=0.1, rely=0.2, relheight=0.1, relwidth=0.8)

        # # Create button
        # modify_row_button = tk.Button(self.table_frame, text="Modify Data", command=self.modify_row_function, bg=Colors.ACTIVE_BACKGROUND, font=font)
        # modify_row_button.place(relx=0.18, rely=0.4, relheight=0.1, relwidth=0.3)
        # delete_row_button = tk.Button(self.table_frame, text="Delete Data", command=self.delete_row_function, bg=Colors.ACTIVE_BACKGROUND, font=font)
        # delete_row_button.place(relx=0.52, rely=0.4, relheight=0.1, relwidth=0.3)




        # self.default_lable = tk.Label(self.table_frame, bg=Colors.ACTIVE_BACKGROUND, text="Select a table", font="Consolas 36")
        # self.default_lable.pack(expand=1, fill=tk.BOTH)


    
    # def table_selector(self):
    #     font = "Consolas 16"
    #     database_names = ["accounts.db", "daily_notes.db", "inventory.db", "krar.db"]
    #     labels_top_frame = tk.Frame(self.upper_frame, bg=Colors.ACTIVE_BACKGROUND)
    #     labels_top_frame.pack(side="top", fill=tk.BOTH)
    #     labels_bottom_frame = tk.Frame(self.upper_frame, bg=Colors.ACTIVE_BACKGROUND)
    #     labels_bottom_frame.pack(side="top", fill=tk.BOTH)
        
        
    #     db_label = tk.Label(labels_top_frame, text="Select database:", bg=Colors.ACTIVE_BACKGROUND, font=font)
    #     db_label.pack(side="left", padx=5, pady=5)
    #     self.db_dropdown = ttk.Combobox(labels_bottom_frame, values=database_names, font=font)
    #     self.db_dropdown.pack(side="left", padx=5, pady=5)
    #     self.db_dropdown.bind('<<ComboboxSelected>>', lambda e : self.update_table_names())


    #     # self.db_dropdown.bind('<Enter>', lambda e: db_dropdown.config(values=get_item_list()))
    #     # self.db_dropdown.bind('<Down>', lambda e: update_listbox_items(db_dropdown, get_item_list(), b_in1.get()))


    #     # Create table dropdown
    #     self.table_list = []
    #     table_label = tk.Label(labels_top_frame, text="Select table:", bg=Colors.ACTIVE_BACKGROUND, font=font)
    #     table_label.pack(side="left", padx=80, pady=5)
    #     self.table_dropdown = ttk.Combobox(labels_bottom_frame, values= self.table_list, width=20, font=font)
    #     self.table_dropdown.pack(side="left", padx=5, pady=5)
    #     # self.table_dropdown.bind('<<ComboboxSelected>>', lambda e : self.update_table_names())

    #     row_label = tk.Label(labels_top_frame, text="Row id:", bg=Colors.ACTIVE_BACKGROUND, font=font)
    #     row_label.pack(side="left", padx=50, pady=5)
    #     self.row_id_entry = tk.Entry(labels_bottom_frame, font=font, bg=Colors.ACTIVE_BACKGROUND)
    #     self.row_id_entry.pack(side="left", padx=5, pady=5)

    #     # Create button
    #     show_button = tk.Button(labels_bottom_frame, text="Show Data", command=self.show_row, bg=Colors.ACTIVE_BACKGROUND, font=font)
    #     show_button.pack(side="left", padx=5, pady=5)

    def update_table_names(self):
        selected_db = self.db_dropdown.get()
        if selected_db:
            if selected_db == "accounts.db":
                accounts.accounts_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                self.table_list = accounts.accounts_cursor.fetchall()
            if selected_db == "inventory.db":
                inventory.inventory_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                self.table_list = inventory.inventory_cursor.fetchall()
            if selected_db == "daily_notes.db":
                database.daily_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                self.table_list = database.daily_cursor.fetchall()
            if selected_db == "krar.db":
                krar.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                self.table_list = krar.cursor.fetchall()
            if selected_db == "bills.db":
                conn = sqlite3.connect(bill_db.db_name)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                self.table_list = cursor.fetchall()
                conn.close()
            
            self.table_dropdown.config(values=self.table_list)
            
            # print(selected_db, self.table_list)

    def show_row(self):
        # Get selected database and table
        selected_db = self.db_dropdown.get()
        selected_table = self.table_dropdown.get()
        row_id = self.row_id_entry.get()
        
        row = []
        if selected_db and selected_table:
            if selected_db == "accounts.db":
                row = accounts.get_transaction_by_id(selected_table, int(row_id) )

            if selected_db == "inventory.db":
                row = inventory.get_transaction_by_id(selected_table, row_id)

            if selected_db == "daily_notes.db":
                if __name__ == "__main__":
                    print("cannot modify daily_note")
                
                else:
                    self.master.master.set_status("[-] Cannot modify daily_notes")
            
            if selected_db == "krar.db":
                if selected_table == "all_krar":
                    x = 'krar_id'
                else:
                    x = 'uid'
                row = krar.cursor.execute(f"SELECT * FROM {selected_table} where {x} = {row_id}").fetchone()

            if selected_db == "bills.db":
                conn = sqlite3.connect(bill_db.db_name)
                cursor = conn.cursor()
                row = cursor.execute(f"SELECT * FROM {selected_table} where id = {row_id}").fetchone()
                conn.close()

        new_row = "|".join(map(str, row))
        self.table_row.set(new_row)
    
    def modify_row_function(self):
        table_row = self.table_row.get().upper()
        selected_db = self.db_dropdown.get()
        selected_table = self.table_dropdown.get()
        row_id = self.row_id_entry.get()
        if table_row and selected_db and selected_table and row_id:
            row_list = table_row.split("|")
            if selected_db == "accounts.db":
                if selected_table == "customers":
                    accounts.update_customer_details(row_id, row_list[1], row_list[2])
                                        
                else:
                    accounts.update_customer_transaction(selected_table, row_id, row_list[1], row_list[2], row_list[3], row_list[4], row_list[5])
                    
            if selected_db == "inventory.db":
                if selected_table == "items":
                    inventory.modify_item(row_id, row_list[1], row_list[2], row_list[3], row_list[4], row_list[5], row_list[6], row_list[7], row_list[8], row_list[9])
                                        
                else:
                    item_id  = int(selected_table.split("_")[1])
                    inventory.modify_transaction(item_id, row_id, row_list[1], row_list[2], row_list[3], row_list[4], row_list[5])

            if selected_db == "krar.db":
                if selected_table == "all_krar":
                    krar.modify_krar_customer_and_status(int(row_id), row_list[1], row_list[2])
                else:
                    krar.modify_by_krar_id(int(row_id), row_list[1], row_list[2])

            if selected_db == 'bills.db':
                conn = sqlite3.connect(bill_db.db_name)
                cursor = conn.cursor()
                if selected_table == "item_details":
                    bill_db.modify_item_details(int(row_id), tuple(row_list[1:]))
                
                elif selected_table == "bill_details":
                    bill_db.modify_bill_details(int(row_list[1]), tuple(row_list[2:]))
                
                else:
                    bill_db.modify_bill_item(int(row_list[1]), int(row_list[2]), int(row_list[3]))

            note = f"05 = {selected_db}, {selected_table}, {row_id}, {table_row}"
            database.add_note_to_date(note)

            
            if __name__ != "__main__":
                self.master.master.set_status(f"Row updated: {row_id}")
                    
                    

    def delete_row_function(self):
        table_row = self.table_row.get().upper()
        selected_db = self.db_dropdown.get()
        selected_table = self.table_dropdown.get()
        row_id = self.row_id_entry.get()
        if selected_db and selected_table and row_id:
            if selected_db == "accounts.db":
                if selected_table == "customers":
                    accounts.delete_customer(row_id)
                
                else:
                    customer_id = int(selected_table.split("_")[1])
                    accounts.delete_customer_transaction(customer_id, row_id)

            if selected_db == "inventory.db":
                if selected_table == "items":
                    inventory.delete_item(row_id)
                
                else:
                    item_id = int(selected_table.split("_")[1])
                    inventory.delete_transaction(item_id, row_id)

            if selected_db == "krar.db":
                if selected_table == "all_krar":
                    krar.delete_from_all_krar(int(row_id))
                else:
                    krar.delete_from_by_krar_id(int(row_id))
            
            if selected_db == 'bills.db':
                bill_db.delete_row(selected_table, row_id)


            note = f"06 = {selected_db}, {selected_table}, {row_id}, {table_row}"
            database.add_note_to_date(note)
            if __name__ != "__main__":
                self.master.master.set_status(f"Row deleted: {row_id}")
                


if __name__ == "__main__":
    app = tk.Tk()
    app.state("zoomed")
    h = ModifyPage(app)
    h.pack(expand=1, fill="both")
    app.mainloop()
