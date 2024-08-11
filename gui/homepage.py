import tkinter as tk

from .mytheme import Colors
from tkinter import ttk

from database import accounts, database, krar

# import accounts
# import inventory
# import database
# import krar
# import datetime
# import time

# import mypandasfile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt




class HomePage(tk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.Colors = Colors

        # img = tk.PhotoImage(file="myicons\\framebg2.png")

        # self.background_title = tk.Label(self, image=img)
        # self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)

        # self.img = img

        self.karar_data_frame = KrarData(self)
        self.karar_data_frame.place(relx=0.78, rely=0.01, relheight=0.98, relwidth=0.21)
    

    def all_graphs_function(self, accounts_df):
        for widget in self.winfo_children():
            widget.destroy()
        
        # self.background_title = tk.Label(self, image=self.img)
        # self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.karar_data_frame = KrarData(self)
        self.karar_data_frame.place(relx=0.78, rely=0.01, relheight=0.98, relwidth=0.21)

        self.all_positive_df = accounts_df.loc[accounts_df['Amount'] >=0]
        self.all_negative_df = accounts_df.loc[accounts_df['Amount'] <0]

        self.sales_data_frame = SalesData(self)
        self.sales_data_frame.place(relx=0.01, rely=0.01, relheight=0.485, relwidth=0.4)
        self.recieve_data_frame = RecieceData(self)
        self.recieve_data_frame.place(relx=0.42, rely=0.01, relheight=0.485, relwidth=0.35)
        self.items_data_frame = ItemsData(self)
        self.items_data_frame.place(relx=0.01, rely=0.505, relheight=0.485, relwidth=0.35)
        self.account_data_frame = AccountsData(self)
        self.account_data_frame.place(relx=0.37, rely=0.505, relheight=0.485, relwidth=0.4)
        
    def redraw_graphs(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        # self.background_title = tk.Label(self, image=self.img)
        # self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.karar_data_frame = KrarData(self)
        self.karar_data_frame.place(relx=0.78, rely=0.01, relheight=0.98, relwidth=0.21)
        self.sales_data_frame = SalesData(self)
        self.sales_data_frame.place(relx=0.01, rely=0.01, relheight=0.485, relwidth=0.4)
        self.recieve_data_frame = RecieceData(self)
        self.recieve_data_frame.place(relx=0.42, rely=0.01, relheight=0.485, relwidth=0.35)
        self.items_data_frame = ItemsData(self)
        self.items_data_frame.place(relx=0.01, rely=0.505, relheight=0.485, relwidth=0.35)
        self.account_data_frame = AccountsData(self)
        self.account_data_frame.place(relx=0.37, rely=0.505, relheight=0.485, relwidth=0.4)


class SalesData(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.Colors = self.master.Colors
        self.config(background=self.Colors.BACKGROUND)
        self.debit_credit_bar_graph()
        

    def debit_credit_bar_graph(self):
        data = database.last_7_day_report()
        names = [item[0] for item in data]
        values = [item[1] for item in data]

        fig = Figure(figsize=(5, 3), dpi=100, facecolor=self.Colors.BACKGROUND)

        ax = fig.add_subplot(111)
        ax.set_facecolor(self.Colors.BACKGROUND)

        markerline, stemline, baseline = ax.stem(names, values, linefmt='-', markerfmt='o', basefmt=' ')

        plt.setp(markerline, color=self.Colors.ACTIVE_FOREGROUND)
        plt.setp(stemline, color=self.Colors.ACTIVE_FOREGROUND)
        plt.setp(baseline, visible=False)

        # ax.set_title(total_diffrence_value)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

class RecieceData(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.Colors = self.master.Colors
        self.config(background=self.Colors.BACKGROUND)
        self.total_pie_graph()

    def total_pie_graph(self):
        # values
        total_debit_value = self.master.all_positive_df.shape[0]
        total_credit_value = self.master.all_negative_df.shape[0]
        total_sum_value = total_debit_value+total_credit_value
        # print(total_debit_value)

        fig = Figure(figsize=(5,4), dpi=100, facecolor=self.Colors.BACKGROUND)
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.Colors.BACKGROUND)


        categories = ['Dr', 'Cr']
        amounts = [total_debit_value, total_credit_value]
        mycolors = [self.Colors.FG_SHADE_1, self.Colors.FG_SHADE_3]
        ax.pie(amounts, labels=categories, colors=mycolors, autopct='%1.1f%%')
        ax.set_title(total_sum_value)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

class AccountsData(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.Colors = self.master.Colors
        self.config(background=self.Colors.BACKGROUND)
        self.positive_scater_plot()

    def positive_scater_plot(self):
        # values
        df = self.master.all_positive_df
        
        fig = Figure(figsize=(5,4), dpi=100, facecolor=self.Colors.BACKGROUND)
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.Colors.BACKGROUND)


        ax.scatter(df['Amount'], df['Days'])

        # ax.set_xlabel("Amount")
        # ax.set_ylabel("Days")
        # ax.set_title(total_diffrence_value)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

class ItemsData(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.Colors = self.master.Colors
        self.config(background=self.Colors.BACKGROUND)
        self.total_pie_graph()

    def total_pie_graph(self):
        # values
        total_debit_value = self.master.all_positive_df['Amount'].sum()
        total_credit_value = self.master.all_negative_df['Amount'].sum()*(-1)
        total_sum_value = round(total_debit_value-total_credit_value, 2)

        fig = Figure(figsize=(5,4), dpi=100, facecolor=self.Colors.BACKGROUND)
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.Colors.BACKGROUND)


        categories = ['Dr', 'Cr']
        amounts = [total_debit_value, total_credit_value]
        mycolors = [self.Colors.FG_SHADE_1, self.Colors.FG_SHADE_3]
        ax.pie(amounts, labels=categories, colors=mycolors, autopct='%1.1f%%')
        ax.set_title(total_sum_value)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()



class KrarData(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.Colors = self.master.Colors
        self.config(background=self.Colors.BACKGROUND)

        self.todo_title = tk.Label(self, text='Today', font="Consolas 16", bg=self.Colors.BACKGROUND, fg=self.Colors.FG_SHADE_3, anchor='center')
        self.todo_title.pack(fill='x')

        self.table_frame = tk.Frame(self, bg=self.Colors.BACKGROUND)
        self.table_frame.pack(fill="x", expand=1)
        self.show_table(self.table_frame,krar.get_customers_with_last_krar_today())

        self.todo_title2 = tk.Label(self, text='Past', font="Consolas 14", bg=self.Colors.BACKGROUND, fg=self.Colors.FG_SHADE_3, anchor='center')
        self.todo_title2.pack(fill='x')

        self.table_frame2 = tk.Frame(self, bg=self.Colors.BACKGROUND)
        self.table_frame2.pack(fill="x", expand=1)
        self.show_table(self.table_frame2,krar.get_customers_with_last_krar_past())

        self.todo_title3 = tk.Label(self, text='Upcoming', font="Consolas 14", bg=self.Colors.BACKGROUND, fg=self.Colors.FG_SHADE_3, anchor='center')
        self.todo_title3.pack(fill='x')

        self.table_frame3 = tk.Frame(self, bg=self.Colors.BACKGROUND)
        self.table_frame3.pack(fill="x", expand=1)
        self.show_table(self.table_frame3,krar.get_customers_with_last_krar_future())
        

    def set_undue_krar(self):
        customer_name = self.table_dropdown.get()
        if customer_name:
            krar.update_krar_tag_by_name(customer_name, 0)

    def show_data(self, accounts_id_list):
        # unsettled_accounts = krar.get_accounts_with_unsettled_krars()
        table_data = []

        for idx, account_id in enumerate(accounts_id_list):
            customer_details = accounts.get_customer_details(account_id)

            customer_name = f"{customer_details[0]} {customer_details[1]}"
            temp = []
            temp.append(customer_details[2])
            temp.extend(krar.get_unsettled_krar_dates(account_id))
            table_data.append([customer_name, temp])
        
        return table_data
        
    def show_table(self, root, x):
        table_data = self.show_data(x)
        column_name = ["Name",]
        # print(table_data)
        
        if column_name and table_data:
            for widget in root.winfo_children():
                widget.destroy()
                
            tree = ttk.Treeview(root, columns=column_name, show='tree')
            # tree['columns'] = column_name
            tree.heading("#0", text="")
            tree.column('#0', width=0)#, stretch="no")

            c = 0
            for i in table_data:
                c += 1
                tg = 'odd'
                if c%2 == 0:
                    tg = "even"
                tree.insert('', 'end', iid=c, text="", values=i, tags = tg )
                for j in i[1]:
                    tree.insert(c, 'end', text=c, values=[j,0], tags = tg )


            tree.tag_configure('odd', background=self.Colors.ACTIVE_BACKGROUND)
            tree.tag_configure('even', background=self.Colors.ACTIVE_FOREGROUND)
            tree.pack(fill="x", expand=True)




if __name__ == "__main__":
    app = tk.Tk()
    app.state("zoomed")
    h = HomePage(app)
    h.pack(expand=1, fill="both")
    app.mainloop()
