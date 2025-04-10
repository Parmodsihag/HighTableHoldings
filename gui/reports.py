        
import tkinter as tk

from .mytheme import Colors
from tkinter import ttk
from tkinter import filedialog, messagebox

import openpyxl
import calendar
import datetime
import os
import re
import sqlite3
import sys

import numpy as np
# import pandas as pd

from database import accounts, inventory, database, krar, crop_database
# import accounts
# import inventory
# import database
# import krar
import numpy as np
import pandas as pd

db_name = "C://JBB//data//bills.db"
bill_cursor = sqlite3.connect(db_name).cursor()
# import mypandasfile

class ReportsPage(tk.Frame):
    # accounts_df = mypandasfile.customer_df

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.Colors = Colors

        # img = tk.PhotoImage(file="myicons\\framebg2.png")

        # self.background_title = tk.Label(self, image=img)
        # self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)

        # self.img = img

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
        self.db_dropdown = ttk.Combobox(self.upper_frame, values=database_names, width=12, font=font)
        self.db_dropdown.pack(side="left", padx=5, pady=5)
        self.db_dropdown.bind('<<ComboboxSelected>>', lambda e : self.update_table_names())


        # self.db_dropdown.bind('<Enter>', lambda e: db_dropdown.config(values=get_item_list()))
        # self.db_dropdown.bind('<Down>', lambda e: update_listbox_items(db_dropdown, get_item_list(), b_in1.get()))


        # Create table dropdown
        self.table_list = []
        table_label = tk.Label(self.upper_frame, text="Table:", bg=self.Colors.BACKGROUND, fg=self.Colors.ACTIVE_FOREGROUND, font=font)
        table_label.pack(side="left", padx=5, pady=5)
        # self.table_dropdown = SearchBar(self.upper_frame, data=self.table_list)
        # self.table_dropdown.pack(padx=40, pady=(0, 10), fill='x')
        # self.table_dropdown.search_bar.bind('<Enter>', lambda e: self.table_dropdown.set_data(self.table_list))

        self.table_dropdown = ttk.Combobox(self.upper_frame, values= self.table_list, width=20, font=font)
        self.table_dropdown.pack(side="left", padx=5, pady=5)
        self.table_dropdown.bind('<Down>', lambda e: self.update_listbox_items(self.table_dropdown, self.table_list, self.table_dropdown.get().upper()))
        self.table_dropdown.bind('<<ComboboxSelected>>', lambda e: self.show_table())
        # self.table_dropdown.bind('<<ComboboxSelected>>', lambda e : self.update_table_names())

        # Create button
        # show_button = tk.Button(self.upper_frame, text="Show", command=self.show_table, bg=self.Colors.BACKGROUND3, fg=self.Colors.FG_SHADE_3, relief='solid', font="Consolas 14")
        # show_button.pack(side="left", padx=5, pady=5)

        export_button = tk.Button(self.upper_frame, text="Export", command=self.export_to_excel, bg=self.Colors.BACKGROUND, fg=self.Colors.FG_SHADE_3, relief='solid', font="Consolas 14")
        export_button.pack(side="left", padx=30, pady=5)

    def parallel_process_combo(self, accounts_df):
        for widget in self.upper_frame.winfo_children():
            widget.destroy()
        # sort by
        self.table_selector()
        self.accounts_df = accounts_df
        self.accounts_df = self.calculate_account_score(self.accounts_df)
        self.accounts_df = self.accounts_df[['customer_id', 'name', 'detail', 'Amount', 'Days', 'account_score']]
        sort_options_list = ['Customer Id', 'Amount', 'Days', 'Customer Id R', 'Amount R', "Days R", "Score"]
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
        elif value == "Score":
            self.make_my_table(self.accounts_df.sort_values('account_score', ascending=False))
        else:
            self.make_my_table(self.accounts_df)
    
    
    def calculate_account_score(self, df, alpha=0.6, beta=0.4):
        """
        Calculates an account score based on log-transformed amount and days,
        and adds it as a new 'account_score' column to the DataFrame.
        """
        # Avoid modifying the original DataFrame in place
        df_copy = df.copy()

        # Handle cases where amount is zero or negative to avoid log(0) or log(negative)
        df_copy['log_amount'] = df_copy['Amount'].apply(lambda x: np.log(x + 1) if x > 0 else 0)
        df_copy['log_days'] = df_copy['Days'].apply(lambda x: np.log(x + 1) if x > 0 else 0)

        # Normalize log_amount and log_days
        min_log_amount = df_copy['log_amount'].min()
        max_log_amount = df_copy['log_amount'].max()
        min_log_days = df_copy['log_days'].min()
        max_log_days = df_copy['log_days'].max()

        if max_log_amount - min_log_amount != 0:
          df_copy['normalized_log_amount'] = (df_copy['log_amount'] - min_log_amount) / (max_log_amount - min_log_amount)
        else:
          df_copy['normalized_log_amount'] = 0

        if max_log_days - min_log_days != 0:
          df_copy['normalized_log_days'] = (df_copy['log_days'] - min_log_days) / (max_log_days - min_log_days)
        else:
          df_copy['normalized_log_days'] = 0

        # Calculate the account score
        df_copy['account_score'] = (alpha * df_copy['normalized_log_amount']) + (beta * df_copy['normalized_log_days'])
        return df_copy

    def make_my_table(self, df):
        self.db_dropdown.set("Root")
        for widget in self.table_frame.winfo_children():
                widget.destroy()
        # columns = df.columns.tolist()
        column_name = ["ID", "Name", "Details", "Amount", "Active", "Score", "-"]
            
        self.tree = ttk.Treeview(self.table_frame)
        self.tree['columns'] = column_name
        self.tree.heading("#0", text="")
        self.tree.column('#0', width=20, stretch="no")
        column_width_list = [45, 300, 300, 120, 120, 100, 120]
        # for column in columns:
        #     self.tree.heading(column, text=column)
        
        for i in range(len(column_name)):
            self.tree.column(column_name[i], width=column_width_list[i], anchor='w')
            self.tree.heading(column_name[i], text=column_name[i], anchor="w")
        
        
        c = 0
        for index, row in df.iterrows():
            score = int(round(row.tolist()[5], 2) * 100)
            tg= f'e{score}' if c%2 else f'o{score}'
            c += 1
            parent_id = self.tree.insert("", 'end', text=c, values=row.tolist(), tags=tg)
            self.tree.tag_configure(tg, background=self.calculate_color_value(tg), foreground="#FFF")

            c2 = 0
            for row in self.tree_subtree_accounts(row.tolist()[0]):
                tg1 = 'even1' if c2%2 else "odd1"
                self.tree.insert(parent_id, 'end', values=row, tags=tg1)
                c2 += 1
            
        # self.tree.tag_configure('odd', background=self.Colors.BACKGROUND, foreground=self.Colors.ACTIVE_FOREGROUND)
        # self.tree.tag_configure('even', background=self.Colors.BACKGROUND1, foreground=self.Colors.ACTIVE_FOREGROUND)
        self.tree.tag_configure('odd1', background=self.Colors.BACKGROUND4, foreground=self.Colors.ACTIVE_FOREGROUND)
        self.tree.tag_configure('even1', background=self.Colors.BACKGROUND5, foreground=self.Colors.ACTIVE_FOREGROUND)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        
        # self.tree.bind("<Double-1>", self.on_double_click1)

    def calculate_color_value(self, tg):
        tag =  tg[0]
        score = int(tg[1:])/100
        hex_val = int(60*score)
        red_hex = hex(196+hex_val)[2:].zfill(2) 
        red = hex(int(score*255))[2:].zfill(2)
        green = hex(int((1-score)*255))[2:].zfill(2)

        # return f"#{red}{green}CC"
        return f"#88{green}{red}"

        # if score < .5:
        #     return f"#00{red_hex}00"
        # else:
        #     return f"#{red_hex}0000"
        # if tag == "e":
        #     return f"#{red_hex}CCCC"
        # else:
        #     return f"#{red_hex}CCCC"

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
    
    def on_double_click1(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            item_id = self.tree.identify_row(event.y)
            # print(f"Double-clicked item ID: {item_id}") 
            row_data = self.tree.item(item_id)['values']
            self.db_dropdown.set("accounts.db")
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

    def make_table_accounts1(self, column_list, table_data):
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
    

    def make_table_accounts(self, column_list, table_data):
        """Prepares account transaction data for display, 
            including interest and settlement handling.
        """
        total_sum_without_interest = 0.0
        total_interest = 0.0
        updated_column_list = []
        updated_table_data = []

        for i in column_list:
            updated_column_list.append(i[1])

        if len(column_list) == 3:  # Assuming 'customers' table
            updated_table_data = table_data
            column_width_list = [10, 400, 400]
        else:
            column_width_list = [10, 50, 400, 10, 40, 40, 50]
            updated_column_list = ['ID', 'Date', 'Particulars', 'Interest', 'Debit', 'Credit', 'Balance']

            current_balance = 0.0
            last_settlement_date, last_settlement_id = self._find_last_settlement_date(table_data)
            # Keep track of the last settlement transaction ID

            for row in table_data:
                id, date, particulars, amount, transaction_type, tag = row
                date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                interest = 0.0
                debit = amount if transaction_type.upper() == "P" else ""
                credit = amount if transaction_type.upper() == "M" else ""

                if tag == '0':  # Settlement transaction
                    current_balance = 0.0
                    total_interest = 0.0
                    total_sum_without_interest = 0.0
                    last_settlement_date = date_obj

                else: 
                    # Calculate interest only if transaction is after the last settlement
                    if (tag == '1' and 
                        (last_settlement_date is None or 
                            date_obj > last_settlement_date or 
                            (date_obj == last_settlement_date and id > last_settlement_id))
                    ):
                        interest = self.calculate_interest(amount, date)
                        total_interest += (interest if transaction_type.upper() == "P" else -interest)

                    current_balance += (amount if transaction_type.upper() == "P" else -amount)
                    total_sum_without_interest += (amount if transaction_type.upper() == "P" else -amount)

                temp_list = [id, date, particulars, interest, debit, credit, current_balance] 
                updated_table_data.append(temp_list)

            if __name__ != "__main__" and self.db_dropdown.get() != "Root":
                table_id = self.table_dropdown.get().split()[0]
                customer_name = accounts.get_customer_details(table_id)
                status = (
                    f"{customer_name}    "
                    f"{round(total_sum_without_interest, 2)} + "
                    f"{round(total_interest, 2)} = "
                    f"{round(total_sum_without_interest + total_interest, 2)}"
                )
                self.master.master.set_status(status)

        return updated_column_list, updated_table_data, column_width_list

    def calculate_total123(self):
        t1 = 0
        t2 = 0
        t3 = 0
        t4 = 0
        t5 = 0
        t6 = 0
        for account in accounts.get_all_customers_name_and_id():
            selected_table = f"customer_{account[0]}"
            table_data = accounts.get_table(selected_table)
            x,y,z = self.get_total_amount123(table_data)
            if z>0:
                t1 += x
                t2 += y
                t3 += z
            else:
                t4 += x
                t5 += y
                t6 += z
                
            print(account[0], account[1], x, y, z)
        
        print()
        print(t1, t2, t3)
        print()
        print(t4, t5, t6)
        print()
        print()
        print(t1+t4, t2+t5, t6+t3)

    def get_total_amount123(self, table_data):
        total_sum_without_interest = 0.0
        total_interest = 0.0

        # for i in column_list:
        #     updated_column_list.append(i[1])
        # updated_column_list = ['ID', 'Date', 'Particulars', 'Interest', 'Debit', 'Credit', 'Balance']
        current_balance = 0.0
        last_settlement_date, last_settlement_id = self._find_last_settlement_date(table_data)
        # Keep track of the last settlement transaction ID
        for row in table_data:
            id, date, particulars, amount, transaction_type, tag = row
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            interest = 0.0
            debit = amount if transaction_type.upper() == "P" else ""
            credit = amount if transaction_type.upper() == "M" else ""
            if tag == '0':  # Settlement transaction
                current_balance = 0.0
                total_interest = 0.0
                total_sum_without_interest = 0.0
                last_settlement_date = date_obj
            else: 
                # Calculate interest only if transaction is after the last settlement
                if (tag == '1' and 
                    (last_settlement_date is None or 
                        date_obj > last_settlement_date or 
                        (date_obj == last_settlement_date and id > last_settlement_id))
                ):
                    interest = self.calculate_interest(amount, date)
                    total_interest += (interest if transaction_type.upper() == "P" else -interest)
                current_balance += (amount if transaction_type.upper() == "P" else -amount)
                total_sum_without_interest += (amount if transaction_type.upper() == "P" else -amount)
            # temp_list = [id, date, particulars, interest, debit, credit, current_balance] 
            # updated_table_data.append(temp_list)

        return [total_sum_without_interest, total_interest, total_sum_without_interest + total_interest]

    def _find_last_settlement_date(self, table_data):
        """Finds the date of the last settled transaction from the provided data.

        Args:
            table_data (list): List of transaction rows.

        Returns:
            datetime.date or None: Date of the last settlement or None if no settlements found.
        """
        last_settlement_date = None
        last_settlement_id = -1
        for row in reversed(table_data):  # Iterate in reverse to find the last settlement quickly 
            if row[5] == '0': 
                last_settlement_date = datetime.datetime.strptime(row[1], "%Y-%m-%d").date()
                last_settlement_id = row[0]
                break
        return last_settlement_date , last_settlement_id

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
            column_width_list = [10,200,1,1,1,1,1,1,1,1,1,1]
            updated_column_list.append("In Stock")
            updated_column_list.append("Total Value")
            # updated_column_list.append("Stock Value")
            # updated_column_list.append("Last Value")
            all_items_stock_value = 0.0
            for row in table_data:
                # print(row)
                item_id = int(row[0])
                temp_list = []
                for i in row:
                    temp_list.append(i)

                in_stock = inventory.get_item_quantity(item_id)
                total_stock_value = round(in_stock * float(row[3]), 2)
                all_items_stock_value += total_stock_value
                # total_stock_value = inventory.get_item_value(item_id)
                # last_value = inventory.get_last_value(item_id)
                temp_list.append(in_stock)
                temp_list.append(total_stock_value)
                # temp_list.append(total_stock_value)
                # temp_list.append(last_value)
                updated_table_data.append(temp_list)
            if __name__ != "__main__":
                status = f"{all_items_stock_value} "
                self.master.master.set_status(status)

            

        return updated_column_list, updated_table_data, column_width_list

    def export_to_excel(self):
        """Exports the Treeview data to an Excel file and asks the user if they want to open it."""
        try:
            # Get data from Treeview
            data = []
            for item in self.tree.get_children():
                row = self.tree.item(item)['values']
                data.append(row)

            # Get column names from Treeview
            column_names = self.tree["columns"]

            # Create a new workbook and worksheet
            workbook = openpyxl.Workbook()
            worksheet = workbook.active

            # Write the header row
            worksheet.append(column_names)

            # Write the data rows
            for row in data:
                worksheet.append(row)

            # Get filename using a file dialog
            file_name = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialdir="C:/JBBExcel",
                initialfile = 'temp',
                confirmoverwrite = False,
                title="Save Report as Excel"
                
            )

            if file_name:
                # Save the workbook
                workbook.save(file_name)

                if __name__ != "__main__":
                    self.master.master.set_status(f"Data exported to {file_name}")

                # Ask the user if they want to open the file
                if messagebox.askyesno("Open File", "Do you want to open the exported Excel file?"):
                    os.startfile(file_name)  # Open for Windows
            else:
                if __name__ != "__main__":
                    self.master.master.set_status("Export cancelled")

        except Exception as e:
            if __name__ != "__main__":
                self.master.master.set_status(f"Error exporting to Excel: {e}")
            print(f"Error exporting to Excel: {e}")

    def tree_subtree_accounts(self, account_id):
        selected_table = f"customer_{account_id}"
        accounts.accounts_cursor.execute(f"PRAGMA table_info({selected_table})")
        column_list = accounts.accounts_cursor.fetchall()
        table_data = accounts.get_table(selected_table)
        column_names, table_data, column_width_list = self.make_table_accounts(column_list, table_data)
        return table_data
                


if __name__ == "__main__":
    app = tk.Tk()
    app.state("zoomed")
    h = ReportsPage(app)
    h.pack(expand=1, fill="both")
    # h.calculate_total123()
    app.mainloop()

