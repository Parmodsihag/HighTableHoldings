import tkinter as tk
import re
# import sqlite3
# import bills.bill_db as bill_db
from bills import bill_db
# import inventory

from tkinter import ttk
from mytheme import Colors
from datetime import datetime

# class Colors:
#     BACKGROUND = "#2C3333"
#     BACKGROUND1 = "#1C2323"
#     BACKGROUND2 = "#2f3636"
#     BACKGROUND3 = "#353c3c"
#     ACTIVE_BACKGROUND = "#2E4F4F"
#     ACTIVE_FOREGROUND = "#0E8388"
#     FOREGROUND = "#CBE4D0"
    
#     BG_SHADE_1 = "#1b2222"
#     BG_SHADE_2 = "#1b2232"
#     BG_SHADE_3 = "#475151"
    
#     FG_SHADE_1 = "#1cb9c8"
#     FG_SHADE_2 = "#ffffff"
#     FG_SHADE_3 = "#22c95a"
    
#     LIGHT_BG = "#354040"
#     LIGHT_FG = "#D2E7E0"
    
#     SUCCESS = "#7CB342"
#     ERROR = "#E53935"
#     REMINDER = "#FB8C00"

class BillShowPage(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        img = tk.PhotoImage(file="myicons\\framebg2.png")

        self.background_title = tk.Label(self, image=img)
        self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.img = img

        self.bill_number = tk.StringVar()
        self.bill_date = tk.StringVar()
        self.customer_name = tk.StringVar()
        self.customer_address = tk.StringVar()

        self.total_amount = tk.StringVar()

        self.bill_number_list = bill_db.get_all_bill_numbers()
        self.bill_number_dropdown = ttk.Combobox(self, textvariable=self.bill_number, values=self.bill_number_list, font="Consolas 14")
        self.bill_number_dropdown.place(relx=0.1, rely=.04, relwidth=.3)#pack(padx=40, pady=(10,10), fill='x')
        self.bill_number_dropdown.bind('<<ComboboxSelected>>', lambda e : self.show_bill())
        self.bill_number_dropdown.bind('<Enter>', lambda e: self.bill_number_dropdown.config(values=bill_db.get_all_bill_numbers()))

        bill_date_label = tk.Label(self, textvariable=self.bill_date, font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        bill_date_label.place(relx=0.1, rely=.1,relwidth=0.3)        

        customer_name_label = tk.Label(self, textvariable=self.customer_name, font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        customer_name_label.place(relx=0.64, rely=.04,relwidth=0.3)

        customer_address_label = tk.Label(self, textvariable=self.customer_address, font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        customer_address_label.place(relx=0.64, rely=.1,relwidth=0.3)

        
        self.table_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        self.table_frame.place(relx=0.05, rely=.16, relwidth=.9, relheight=.7)

        total_amount_label = tk.Label(self, textvariable=self.total_amount, font="Consolas 12", bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND, anchor='w')
        total_amount_label.place(relx=0.64, rely=.9,relwidth=0.3)

    

    def show_bill(self):
        bill_number = self.bill_number.get()
        bill_details = bill_db.get_all_details_bill_numbers(bill_number)
        self.bill_date.set(bill_details[2])
        self.customer_name.set(bill_details[3])
        self.customer_address.set(bill_details[4])
        # print(bill_details)
        bill_items = bill_db.get_bill_items(bill_number)
        # print(bill_items)
        self.show_table(bill_items)
        # for i in bill_items:
        #     print(i)

    def show_data(self, bill_items):
        column_name = ['Name', 'Quantity', 'Unit', 'Batch', 'Expiry Date', 'Rate', 'Total', 'Cgst Rate', 'CGST Cost']
        table_data = []
        grand_total = 0
        for item in bill_items:
            item_id = item[2]
            quantity = item[3]
            item_details = bill_db.get_item_by_id(item_id)
            item_name = item_details[1]
            unit = item_details[2]
            rate = item_details[4]
            item_type = item_details[5]
            batch = item_details[7]
            exp = item_details[8]
            total = int(quantity) * int(rate)
            if item_type == "P": gst_rate = 9
            elif item_type == "F": gst_rate = 2.5
            else:gst_rate = 0

            gst_cost = total * gst_rate/100
            grand_total += total + (2*gst_cost)
            temp = [item_name, quantity, unit, batch, exp, rate, total, gst_rate, gst_cost]
            table_data.append(temp)

        self.total_amount.set(grand_total)

        return column_name, table_data

    def show_table(self, bill_items):
        column_name, table_data = self.show_data(bill_items)
        if column_name and table_data:
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

            # tree.tag_configure('odd', background=Colors.ACTIVE_BACKGROUND, foreground=Colors.FG_SHADE_1)
            # tree.tag_configure('even', background=Colors.ACTIVE_FOREGROUND, foreground=Colors.BG_SHADE_2)
            tree.tag_configure('odd', background=Colors.BACKGROUND, foreground=Colors.ACTIVE_FOREGROUND)
            tree.tag_configure('even', background=Colors.BACKGROUND1, foreground=Colors.ACTIVE_FOREGROUND)
            tree.pack(fill=tk.BOTH, expand=True, side=tk.TOP) 
        else:
            print("Empty fields for reports")

    
  
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
    h = BillShowPage(app)
    h.pack(expand=1, fill="both")
    app.mainloop()
