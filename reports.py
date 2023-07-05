        
import tkinter as tk

from mytheme import Colors
from tkinter import ttk

import datetime
import accounts
import inventory
import database
import krar
# import mypandasfile

class ReportsPage(tk.Frame):
    # accounts_df = mypandasfile.customer_df

    def __init__(self, master, **kwargs):
        super().__init__(master, bg=Colors.ACTIVE_BACKGROUND, **kwargs)

        self.upper_frame = tk.Frame(self, bg=Colors.ACTIVE_BACKGROUND)
        self.upper_frame.place(relx=0, rely=0, relheight=0.1, relwidth=1)
        self.table_selector()

        self.table_frame = tk.Frame(self, bg=Colors.ACTIVE_BACKGROUND)
        self.table_frame.place(relx=0, rely=0.1, relheight=0.9, relwidth=1)

        # self.default_lable = tk.Label(self.table_frame, bg=Colors.ACTIVE_BACKGROUND, text="Select a table", font="Consolas 36")
        # self.default_lable.pack(expand=1, fill=tk.BOTH)

        # self.sort_by_dropdown.set("Customer Id")
        # self.sort_by_combobox_select()


    
    def table_selector(self):
        font = "Consolas 16"
        database_names = ["accounts.db", "daily_notes.db", "inventory.db", "krar.db"]
        db_label = tk.Label(self.upper_frame, text="Select database:", bg=Colors.ACTIVE_BACKGROUND, font=font)
        db_label.pack(side="left", padx=5, pady=5)
        self.db_dropdown = ttk.Combobox(self.upper_frame, values=database_names, width=20, font=font)
        self.db_dropdown.pack(side="left", padx=5, pady=5)
        self.db_dropdown.bind('<<ComboboxSelected>>', lambda e : self.update_table_names())


        # self.db_dropdown.bind('<Enter>', lambda e: db_dropdown.config(values=get_item_list()))
        # self.db_dropdown.bind('<Down>', lambda e: update_listbox_items(db_dropdown, get_item_list(), b_in1.get()))


        # Create table dropdown
        self.table_list = []
        table_label = tk.Label(self.upper_frame, text="Select table:", bg=Colors.ACTIVE_BACKGROUND, font=font)
        table_label.pack(side="left", padx=5, pady=5)
        self.table_dropdown = ttk.Combobox(self.upper_frame, values= self.table_list, width=20, font=font)
        self.table_dropdown.pack(side="left", padx=5, pady=5)
        # self.table_dropdown.bind('<<ComboboxSelected>>', lambda e : self.update_table_names())

        # Create button
        show_button = tk.Button(self.upper_frame, text="Show Data", command=self.show_table, bg=Colors.ACTIVE_BACKGROUND, font=font)
        show_button.pack(side="left", padx=5, pady=5)

    def parallel_process_combo(self, accounts_df):
        # sort by
        self.accounts_df = accounts_df
        sort_options_list = ['Customer Id', 'Amount', 'Days', 'Customer Id R', 'Amount R', "Days R"]
        self.sort_by_dropdown = ttk.Combobox(self.upper_frame, values=sort_options_list, width=20, font="Consolas 16")
        self.sort_by_dropdown.pack(side="left", padx=5, pady=5)
        self.sort_by_dropdown.bind('<<ComboboxSelected>>', lambda e : self.sort_by_combobox_select())
        self.sort_by_dropdown.set("Customer Id")
        self.sort_by_combobox_select()
        

    def sort_by_combobox_select(self):
        value = self.sort_by_dropdown.get()
        if value == "Amount":
            self.make_my_table(self.accounts_df.sort_values('Amount'))
        elif value == "Days":
            self.make_my_table(self.accounts_df.sort_values('Days'))
        elif value == "Customer Id":
            self.make_my_table(self.accounts_df.sort_values('customer_id'))
        elif value == "Amount R":
            self.make_my_table(self.accounts_df.sort_values('Amount', ascending=False))
        elif value == "Days R":
            self.make_my_table(self.accounts_df.sort_values('Days', ascending=False))
        elif value == "Customer Id R":
            self.make_my_table(self.accounts_df.sort_values('customer_id', ascending=False))
        else:
            self.make_my_table(self.accounts_df)



    def make_my_table(self, df):
        for widget in self.table_frame.winfo_children():
                widget.destroy()
        columns = df.columns.tolist()
            
        tree = ttk.Treeview(self.table_frame)
        tree['columns'] = columns
        for column in columns:
            tree.heading(column, text=column)
        
        c = 0
        for index, row in df.iterrows():
            tg='even'
            if c%2:
                tg='odd'
            c+=1
            tree.insert("", 'end', text=c, values=row.tolist(), tags=tg)

        tree.tag_configure('odd', background=Colors.ACTIVE_BACKGROUND, foreground=Colors.FG_SHADE_1)
        tree.tag_configure('even', background=Colors.ACTIVE_FOREGROUND, foreground=Colors.BG_SHADE_2)
        tree.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

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
                krar.krar_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                self.table_list = krar.krar_cursor.fetchall()
            
            self.table_dropdown.config(values=self.table_list)
            
            # print(selected_db, self.table_list)

    def show_data(self):
        # Get selected database and table
        selected_db = self.db_dropdown.get()
        selected_table = self.table_dropdown.get()
        column_names = []
        column_list = []
        table_data = []
        tag = 0
        if selected_db and selected_table:
            if selected_db == "accounts.db":
                tag = 1
                accounts.accounts_cursor.execute(f"PRAGMA table_info({selected_table})")
                column_list = accounts.accounts_cursor.fetchall()
                table_data = accounts.get_table(selected_table)
                column_names, table_data = self.make_table_accounts(column_list, table_data)
                

            if selected_db == "inventory.db":
                tag = 1
                inventory.inventory_cursor.execute(f"PRAGMA table_info({selected_table})")
                column_list = inventory.inventory_cursor.fetchall()
                table_data = inventory.get_table(selected_table)
                column_names, table_data = self.make_table_items(column_list, table_data)

            if selected_db == "daily_notes.db":
                database.daily_cursor.execute(f"PRAGMA table_info({selected_table})")
                column_list = database.daily_cursor.fetchall()
                table_data = database.get_table(selected_table)

            if selected_db == "krar.db":
                krar.krar_cursor.execute(f"PRAGMA table_info({selected_table})")
                column_list = krar.krar_cursor.fetchall()
                table_data = krar.get_all_krars()

        # print(column_list)
        if tag:
            pass
        else:
            for column in column_list:
                column_names.append(column[1])
        
        return column_names, table_data
    
    def show_table(self):
        column_name, table_data = self.show_data()
        if column_name and table_data:
            # print("emot")

            for widget in self.table_frame.winfo_children():
                    widget.destroy()
                
            tree = ttk.Treeview(self.table_frame)
            tree['columns'] = column_name
            tree.column('#0', width=1, minwidth=1)

            for i in column_name:
                tree.column(i, width=50)#, anchor='center')
                tree.heading(i, text=i)
            
            c = 0
            for i in table_data:
                c += 1
                tg = 'odd'
                if c%2 == 0:
                    tg = "even"
                tree.insert('', c, text=c, values=i, tags = tg )

            tree.tag_configure('odd', background=Colors.ACTIVE_BACKGROUND, foreground=Colors.FG_SHADE_1)
            tree.tag_configure('even', background=Colors.ACTIVE_FOREGROUND, foreground=Colors.BG_SHADE_2)
            tree.pack(fill=tk.BOTH, expand=True, side=tk.TOP) 
        else:
            print("Empty fields for reports")

    
    def calculate_interest(self, amt, from_date, today_date_1=datetime.date.today()):
        interest_rate_one_day = 0.0006575342465753425
        dt2 = from_date.split("-")
        date_of_entry = datetime.date(int(dt2[0]), int(dt2[1]), int(dt2[2]))
        date_difference = today_date_1 - date_of_entry
        interest = amt*date_difference.days*interest_rate_one_day
        return round(interest, 2)
    
    def make_table_accounts(self, column_list, table_data):
            total_sum = 0.0
            total_sum_without_interest = 0.0
            total_interest = 0.0
            updated_column_list = []
            updated_table_data = []
            # print(column_list)
            for i in column_list:
                updated_column_list.append(i[1])
    
            if len(column_list) == 3:
                updated_table_data = table_data
            else:
                updated_column_list.append("Intrest")
                for row in table_data:
                    date = row[1]
                    amount = row[3]
                    transction_type = row[4]
                    intrest = self.calculate_interest(amount, date)
                    # print(date, amount, intrest)
                    ttl = float(amount) + intrest
                    if transction_type.upper() == "P":
                        total_interest += intrest
                        total_sum_without_interest += float(amount)
                        total_sum += ttl
                    else:
                        total_interest -= intrest
                        total_sum_without_interest -= float(amount)
                        total_sum -= ttl
                    temp_list = []
                    for i in row:
                        temp_list.append(i)
                    temp_list.append(intrest)
                    updated_table_data.append(temp_list)
                if __name__ != "__main__":
                    table_id = self.table_dropdown.get().split("_")[1]
                    customer_name = accounts.get_customer_details(table_id)
                    status = f"{customer_name}    {round(total_sum_without_interest,2)} + {round(total_interest, 2)} = {round(total_sum,2)} "
                    self.master.master.set_status(status)

            return updated_column_list, updated_table_data
    
    def make_table_items(self, column_list, table_data):
        updated_column_list = []
        updated_table_data = []
        for i in column_list:
            updated_column_list.append(i[1])

        if len(column_list) != 2:
            updated_table_data = table_data
        else:
            updated_column_list.append("In Stock")
            for row in table_data:
                item_id = int(row[0])
                temp_list = []
                for i in row:
                    temp_list.append(i)

                in_stock = inventory.get_item_quantity(item_id)
                temp_list.append(in_stock)
                updated_table_data.append(temp_list)

        return updated_column_list, updated_table_data








if __name__ == "__main__":
    app = tk.Tk()
    app.state("zoomed")
    h = ReportsPage(app)
    h.pack(expand=1, fill="both")
    app.mainloop()

