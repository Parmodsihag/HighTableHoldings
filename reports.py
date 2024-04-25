        
import tkinter as tk

from mytheme import Colors
from tkinter import ttk

import calendar
import sqlite3
import datetime
import re

import accounts
import inventory
import database
import krar

db_name = "C://JBB//data//bills.db"
bill_cursor = sqlite3.connect(db_name).cursor()
# import mypandasfile

class ReportsPage(tk.Frame):
    # accounts_df = mypandasfile.customer_df

    def __init__(self, master, **kwargs):
        super().__init__(master, bg=Colors.ACTIVE_BACKGROUND, **kwargs)
        self.Colors = Colors

        img = tk.PhotoImage(file="myicons\\framebg2.png")

        self.background_title = tk.Label(self, image=img)
        self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.img = img

        self.upper_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        self.upper_frame.place(relx=0.01, rely=0.01, relheight=0.09, relwidth=0.98)
        self.table_selector()

        self.table_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        self.table_frame.place(relx=0.01, rely=0.11, relheight=0.88, relwidth=0.98)

        # self.default_lable = tk.Label(self.table_frame, bg=Colors.ACTIVE_BACKGROUND, text="Select a table", font="Consolas 36")
        # self.default_lable.pack(expand=1, fill=tk.BOTH)

        # self.sort_by_dropdown.set("Customer Id")
        # self.sort_by_combobox_select()


    
    def table_selector(self):
        font = "Consolas 16"
        database_names = ["accounts.db", "inventory.db", "daily_notes.db", "krar.db", "bills.db"]
        db_label = tk.Label(self.upper_frame, text="Database:", bg=self.Colors.BACKGROUND, fg=self.Colors.ACTIVE_FOREGROUND, font=font)
        db_label.pack(side="left", padx=5, pady=5)
        self.db_dropdown = ttk.Combobox(self.upper_frame, values=database_names, width=20, font=font)
        self.db_dropdown.pack(side="left", padx=5, pady=5)
        self.db_dropdown.bind('<<ComboboxSelected>>', lambda e : self.update_table_names())


        # self.db_dropdown.bind('<Enter>', lambda e: db_dropdown.config(values=get_item_list()))
        # self.db_dropdown.bind('<Down>', lambda e: update_listbox_items(db_dropdown, get_item_list(), b_in1.get()))


        # Create table dropdown
        self.table_list = []
        table_label = tk.Label(self.upper_frame, text="Table:", bg=self.Colors.BACKGROUND, fg=self.Colors.ACTIVE_FOREGROUND, font=font)
        table_label.pack(side="left", padx=5, pady=5)
        self.table_dropdown = ttk.Combobox(self.upper_frame, values= self.table_list, width=20, font=font)
        self.table_dropdown.pack(side="left", padx=5, pady=5)
        self.table_dropdown.bind('<Down>', lambda e: self.update_listbox_items(self.table_dropdown, self.table_list, self.table_dropdown.get().upper()))
        
        # self.table_dropdown.bind('<<ComboboxSelected>>', lambda e : self.update_table_names())

        # Create button
        show_button = tk.Button(self.upper_frame, text="Show Data", command=self.show_table, bg=self.Colors.BACKGROUND3, fg=self.Colors.FG_SHADE_3, relief='groove', font="Consolas 14")
        show_button.pack(side="left", padx=5, pady=5)

    def parallel_process_combo(self, accounts_df):
        for widget in self.upper_frame.winfo_children():
            widget.destroy()
        # sort by
        self.table_selector()
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
        tree.heading("#0", text="")
        tree.column('#0', width=0, stretch="no")
        for column in columns:
            tree.heading(column, text=column)
        
        c = 0
        for index, row in df.iterrows():
            tg='even'
            if c%2:
                tg='odd'
            c+=1
            tree.insert("", 'end', text=c, values=row.tolist(), tags=tg)

        # tree.tag_configure('odd', background=Colors.ACTIVE_BACKGROUND, foreground=Colors.FG_SHADE_1)
        # tree.tag_configure('even', background=Colors.ACTIVE_FOREGROUND, foreground=Colors.BG_SHADE_2)
        tree.tag_configure('odd', background=self.Colors.BACKGROUND, foreground=self.Colors.ACTIVE_FOREGROUND)
        tree.tag_configure('even', background=self.Colors.BACKGROUND1, foreground=self.Colors.ACTIVE_FOREGROUND)
        tree.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

    def update_table_names(self):
        selected_db = self.db_dropdown.get()
        if selected_db:
            if selected_db == "accounts.db":
                self.table_list = ['customers']
                for account in accounts.get_all_customers_name_and_id():
                    self.table_list.append(f"{account[0]} {account[1]}")
                # self.table_list = [f"{i[0]} {i[1]}" for i in table_list]
                # accounts.accounts_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                # self.table_list = accounts.accounts_cursor.fetchall()
                self.table_dropdown.set("customers")
            if selected_db == "inventory.db":
                self.table_list = ['items']
                for item in inventory.get_all_items_id_and_name():
                    self.table_list.append(f"{item[0]} {item[1]}")
                # inventory.inventory_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                # self.table_list = inventory.inventory_cursor.fetchall()
                self.table_dropdown.set("items")
            if selected_db == "daily_notes.db":
                database.daily_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                self.table_list = database.daily_cursor.fetchall()
                today_date = datetime.date.today()
                if today_date.month<10:
                    self.table_dropdown.set(f"d{today_date.year}_0{today_date.month}_{today_date.day}")
                else:
                    self.table_dropdown.set(f"d{today_date.year}_{today_date.month}_{today_date.day}")
            if selected_db == "krar.db":
                krar.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                self.table_list = krar.cursor.fetchall()
                self.table_dropdown.set("all_krar")
            if selected_db == "bills.db":
                bill_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                self.table_list = bill_cursor.fetchall()
                self.table_dropdown.set("item_details")
            
            self.table_dropdown.config(values=self.table_list)
            self.show_table()
            # print(selected_db, self.table_list)

    def show_data(self):
        # Get selected database and table
        selected_db = self.db_dropdown.get()
        selected_table = self.table_dropdown.get()
        column_names = []
        column_list = []
        table_data = []
        column_width_list= [1,1,1,1,1,1,1,1,1,1]
        tag = 0
        if selected_db and selected_table:
            if selected_db == "accounts.db":
                tag = 1
                # table_id = self.table_dropdown.get().split("_")[1]  # Extract customer ID
                # self.generate_compound_interest_report(table_id)
                if selected_table != 'customers':
                    selected_table = f"customer_{selected_table.split()[0]}"
                accounts.accounts_cursor.execute(f"PRAGMA table_info({selected_table})")
                column_list = accounts.accounts_cursor.fetchall()
                table_data = accounts.get_table(selected_table)
                column_names, table_data, column_width_list = self.make_table_accounts(column_list, table_data)
                

            if selected_db == "inventory.db":
                tag = 1
                if selected_table != 'items':
                    selected_table = f"item_{selected_table.split()[0]}"
                inventory.inventory_cursor.execute(f"PRAGMA table_info({selected_table})")
                column_list = inventory.inventory_cursor.fetchall()
                table_data = inventory.get_table(selected_table)
                column_names, table_data, column_width_list = self.make_table_items(column_list, table_data)

            if selected_db == "daily_notes.db":
                database.daily_cursor.execute(f"PRAGMA table_info({selected_table})")
                column_list = database.daily_cursor.fetchall()
                table_data = database.get_table(selected_table)

            if selected_db == "krar.db":
                krar.cursor.execute(f"PRAGMA table_info({selected_table})")
                column_list = krar.cursor.fetchall()
                table_data = krar.cursor.execute(f"SELECT * FROM {selected_table}").fetchall()

            if selected_db == "bills.db":
                bill_cursor.execute(f"PRAGMA table_info({selected_table})")
                column_list = bill_cursor.fetchall()
                table_data = bill_cursor.execute(f"SELECT * FROM {selected_table}").fetchall()

        # print(column_list)
        if tag:
            pass
        else:
            for column in column_list:
                column_names.append(column[1])
        
        return column_names, table_data, column_width_list
    
    def show_table(self):
        column_name, table_data, column_width_list = self.show_data()
        if column_name and table_data:
            for widget in self.table_frame.winfo_children():
                    widget.destroy()
                
            self.tree = ttk.Treeview(self.table_frame)
            self.tree['columns'] = column_name
            self.tree.column('#0', width=0, stretch='no')


            for i in range(len(column_name)):
                self.tree.column(column_name[i], width=column_width_list[i], anchor='w')
                self.tree.heading(column_name[i], text=column_name[i], anchor="w")
            
            c = 0
            for i in table_data:
                c += 1
                tg = 'odd'
                if c%2 == 0:
                    tg = "even"
                self.tree.insert('', c, text=c, values=i, tags = tg)

            # tree.tag_configure('odd', background="#fff")
            # tree.tag_configure('even', background="#fafafa")
            self.tree.tag_configure('odd', background=self.Colors.BACKGROUND, foreground=self.Colors.ACTIVE_FOREGROUND)
            self.tree.tag_configure('even', background=self.Colors.BACKGROUND1, foreground=self.Colors.ACTIVE_FOREGROUND)
            self.tree.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
            if self.table_dropdown.get() in ['customers', 'items']:
                self.tree.bind("<Double-1>", self.on_double_click)
            self.tree.bind("<Control-Button-1>", self.on_control_click)
        else:
            if __name__ != "__main__":
                self.master.master.set_status("Data Not Avilable")
            print("Empty fields for reports")

    def on_double_click(self, event):
        """Handles double-click event on Treeview items and retrieves the ID."""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            item_id = self.tree.identify_row(event.y)
            # print(f"Double-clicked item ID: {item_id}") 
            row_data = self.tree.item(item_id)['values']
            if self.db_dropdown.get() == "accounts.db":
                self.table_dropdown.set(f"{row_data[0]} {row_data[1]}")
            else:
                self.table_dropdown.set(f"{row_data[0]} {row_data[1]}")
            self.show_table()

    def on_control_click(self, event):
        """Handles double-click event on Treeview items and retrieves the ID."""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell" and __name__ != "__main__":
            item_id = self.tree.identify_row(event.y)
            # print(f"Double-clicked item ID: {item_id}")
            row_id = self.tree.item(item_id)['values'][0]
            # print(row_id[0])
            table_name = self.table_dropdown.get()
            db_name = self.db_dropdown.get()
            if db_name == 'accounts.db' and table_name!= 'customers':
                table_name = f'customer_{table_name.split()[0]}'
            elif db_name == 'inventory.db' and table_name != 'items':
                table_name = f'item_{table_name.split()[0]}'
    
            self.master.master.modifyframe.db_dropdown.set(db_name)
            self.master.master.modifyframe.table_dropdown.set(table_name)
            self.master.master.modifyframe.row_id_var.set(row_id)
            self.master.master.modifyframe.show_row()
            self.master.master.modify_frame_label.set_active()
            self.master.master.report_frame_label.set_inactive()

    
    def update_listbox_items(self, lb, lst, pat):
        lsts = []
        if self.db_dropdown.get() in ['inventory.db', 'accounts.db']:
            for i in lst:
                if re.search(pat, i):
                    lsts.append(i)
            lb.config(values=lsts)
        elif self.db_dropdown.get() == "daily_notes.db":
            for i in lst:
                if re.search(pat, i[0]):
                    lsts.append(i)
            lb.config(values=lsts)


    # important funcition for simple intrest
    def calculate_interest1(self, amt, from_date, today_date_1=datetime.date.today()):
        interest_rate_one_day = 0.0006575342465753425
        dt2 = from_date.split("-")
        date_of_entry = datetime.date(int(dt2[0]), int(dt2[1]), int(dt2[2]))
        date_difference = today_date_1 - date_of_entry
        interest = amt*date_difference.days*interest_rate_one_day
        return round(interest, 2)
    
    
    def calculate_interest(self, principle_amount, from_date_str, to_date=datetime.date.today()):
        """
        Calculates interest earned on a principle amount, considering financial year-end (March 31st).

        Args:
            principle_amount (float): The initial amount of money.
            from_date_str (str): The starting date for interest calculation in "YYYY-MM-DD" format.
            to_date (datetime.date, optional): The ending date for interest calculation. Defaults to today.

        Returns:
            float: The calculated interest amount.
        """
        daily_interest_rate = 0.0006575342465753425 
        from_date = datetime.datetime.strptime(from_date_str, "%Y-%m-%d").date()
        total_interest = 0

        while from_date < to_date:
            year_end = datetime.date(from_date.year, 3, 31) 
            if from_date.month > 3:
                year_end = datetime.date(from_date.year + 1, 3, 31)
            end_date = min(year_end, to_date)
            days = (end_date - from_date).days
            interest = principle_amount * days * daily_interest_rate
            total_interest += interest
            principle_amount += interest 
            from_date = end_date + datetime.timedelta(days=1)

        return round(total_interest, 2)

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
            column_width_list = [10, 400, 400]
        else:
            column_width_list = [10, 50, 400, 10, 40, 40, 50]
            updated_column_list = ['ID', 'Date', 'Particulars', 'Intrest', 'Debit', 'Credit', 'Balance']
    
            for row in table_data:
                date = row[1]
                amount = row[3]
                transction_type = row[4]
                tag = row[5]
                if tag == "1":
                    intrest = self.calculate_interest(amount, date)
                elif tag == "0":
                    intrest = 0
                    amount = 0
                else:
                    intrest = 0
                ttl = float(amount) + intrest
                if transction_type.upper() == "P":
                    debit = amount
                    credit =  "" 
                    total_interest += intrest
                    total_sum_without_interest += float(amount)
                    total_sum += ttl
                else:
                    debit = ""
                    credit =  amount
                    total_interest -= intrest
                    total_sum_without_interest -= float(amount)
                    total_sum -= ttl
                temp_list = [row[0], date, row[2], intrest, debit, credit, total_sum_without_interest]
                # for i in row:
                #     temp_list.append(i)
                # temp_list.append(intrest)
                updated_table_data.append(temp_list)
            if __name__ != "__main__":
                table_id = self.table_dropdown.get().split()[0]
                customer_name = accounts.get_customer_details(table_id)
                status = f"{customer_name}    {round(total_sum_without_interest,2)} + {round(total_interest, 2)} = {round(total_sum,2)} "
                self.master.master.set_status(status)
        return updated_column_list, updated_table_data, column_width_list
    
    def make_table_items(self, column_list, table_data):
        updated_column_list = []
        updated_table_data = []
        for i in column_list:
            updated_column_list.append(i[1])
    

        if len(column_list) != 10:
            updated_table_data = table_data
            column_width_list = [1,1,1,1,400,1]
            if __name__ != "__main__":
                table_id = self.table_dropdown.get().split()[0]
                item_name = inventory.get_item_by_id(table_id)[1]
                item_instock = inventory.get_item_quantity(table_id)
                status = f"{item_name}   [{item_instock}] "
                self.master.master.set_status(status)
        else:
            column_width_list = [1,1,1,1,1,1,1,1,1,1,1]
            updated_column_list.append("In Stock")
            # updated_column_list.append("Stock Value")
            # updated_column_list.append("Last Value")
            for row in table_data:
                # print(row)
                item_id = int(row[0])
                temp_list = []
                for i in row:
                    temp_list.append(i)

                in_stock = inventory.get_item_quantity(item_id)
                # total_stock_value = inventory.get_item_value(item_id)
                # last_value = inventory.get_last_value(item_id)
                temp_list.append(in_stock)
                # temp_list.append(total_stock_value)
                # temp_list.append(last_value)
                updated_table_data.append(temp_list)

            

        return updated_column_list, updated_table_data, column_width_list





if __name__ == "__main__":
    app = tk.Tk()
    app.state("zoomed")
    h = ReportsPage(app)
    h.pack(expand=1, fill="both")
    app.mainloop()

