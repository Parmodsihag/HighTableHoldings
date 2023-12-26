import tkinter as tk

from mytheme import Colors
from tkinter import ttk


# import accounts
# import inventory
import database
import krar
# import datetime
# import time

# import mypandasfile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt



class HomePage(tk.Frame):
    # accounts_df = mypandasfile.customer_df
    # # accounts_df = mypandasfile.get_all_list()
    # all_positive_df = accounts_df.loc[accounts_df['Amount'] >=0]
    # all_negative_df = accounts_df.loc[accounts_df['Amount'] <0]
    # print(all_positive_df)

    def __init__(self, master, **kwargs):
        super().__init__(master, bg=Colors.BACKGROUND1, **kwargs)

        img = tk.PhotoImage(file="myicons\\framebg2.png")

        self.background_title = tk.Label(self, image=img)
        self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.img = img

        # self.jbb_logo_image = tk.PhotoImage(file='myicons/logonew.png')
        # self.jbb_logo_image_label = tk.Label(self , image=self.jbb_logo_image, bg=Colors.BACKGROUND1)
        # self.jbb_logo_image_label.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=.6)


        self.karar_data_frame = KrarData(self)
        self.karar_data_frame.place(relx=0.78, rely=0.01, relheight=0.98, relwidth=0.21)
        # self.all_graphs_function()
        # self.sales_data_frame = SalesData(self)
        # self.sales_data_frame.place(relx=0.01, rely=0.01, relheight=0.485, relwidth=0.4)
    

    def all_graphs_function(self, accounts_df):
        self.all_positive_df = accounts_df.loc[accounts_df['Amount'] >=0]
        self.all_negative_df = accounts_df.loc[accounts_df['Amount'] <0]
        # self.all_positive_df = []
        # self.all_negative_df = []

        # self.all_graphs_frame = tk.Frame(self, bg=Colors.BACKGROUND1)
        # self.all_graphs_frame.place(relx=0, rely=0, relheight=.5, relwidth=.78)
        # self.all_graphs_frame1 = tk.Frame(self, bg=Colors.BACKGROUND1)
        # self.all_graphs_frame1.place(relx=0, rely=0.5, relheight=.5, relwidth=.78)
        
        # self.sales_data_frame = SalesData(self.all_graphs_frame)
        # self.sales_data_frame.pack( side='left', padx=(0,5), pady=(0,5))
        # self.recieve_data_frame = RecieceData(self.all_graphs_frame)
        # self.recieve_data_frame.pack( side='left', padx=(5,10), pady=(0,5))
        # self.account_data_frame = AccountsData(self.all_graphs_frame1)
        # self.account_data_frame.pack( side='left', padx=(0,5), pady=(5,0))
        # self.items_data_frame = ItemsData(self.all_graphs_frame1)
        # self.items_data_frame.pack( side='left', padx=(5,10), pady=(5,0))

        self.sales_data_frame = SalesData(self)
        self.sales_data_frame.place(relx=0.01, rely=0.01, relheight=0.485, relwidth=0.4)
        self.recieve_data_frame = RecieceData(self)
        self.recieve_data_frame.place(relx=0.42, rely=0.01, relheight=0.485, relwidth=0.35)
        self.items_data_frame = ItemsData(self)
        self.items_data_frame.place(relx=0.01, rely=0.505, relheight=0.485, relwidth=0.35)
        self.account_data_frame = AccountsData(self)
        self.account_data_frame.place(relx=0.37, rely=0.505, relheight=0.485, relwidth=0.4)
        


        

class ScrollableLabelFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure( bg=Colors.ACTIVE_BACKGROUND)

        self.canvas = tk.Canvas(self, bg=Colors.BACKGROUND, highlightthickness=0)
        # self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=Colors.BACKGROUND)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        # self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        # self.scrollbar.pack(side="right", fill="y")

        # Mousewheel scrolling setup
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_label(self, text, evenodd):
        if evenodd:
            bg = Colors.BACKGROUND1
            fg = Colors.ACTIVE_FOREGROUND
        else:
            bg = Colors.BACKGROUND
            fg = Colors.ACTIVE_FOREGROUND
        
        label = tk.Label(self.scrollable_frame, text=text, bg=bg, fg=fg, font='Consolas 12', anchor='w', padx=4, wraplength=250)
        label.pack(fill='x', expand=1, padx=2)

        # Update scroll region
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
        

class SalesData(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=Colors.BACKGROUND, **kwargs)
        self.debit_credit_bar_graph()
        

    def debit_credit_bar_graph(self):
        # values
        # total_debit_value = self.master.all_positive_df['Amount'].sum()
        # total_credit_value = self.master.all_negative_df['Amount'].sum()*(-1)
        # total_diffrence_value = round(total_debit_value-total_credit_value, 2)
        # print(total_debit_value)
        # Extracting names and values from the list
        data = database.last_7_day_report()
        names = [item[0] for item in data]
        values = [item[1] for item in data]

        fig = Figure(figsize=(5, 3), dpi=100, facecolor=Colors.BACKGROUND)

        ax = fig.add_subplot(111)
        ax.set_facecolor(Colors.BACKGROUND)

        markerline, stemline, baseline = ax.stem(names, values, linefmt='-', markerfmt='o', basefmt=' ')

        plt.setp(markerline, color=Colors.ACTIVE_FOREGROUND)
        plt.setp(stemline, color=Colors.ACTIVE_FOREGROUND)
        plt.setp(baseline, visible=False)

        # ax.set_title(total_diffrence_value)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # fig = Figure(figsize=(4,3), dpi=100, facecolor=Colors.BACKGROUND)
        # ax = fig.add_subplot(111)
        # ax.set_facecolor(Colors.BACKGROUND)


        # categories = ['Dr', 'Cr', "Df"]
        # amounts = [total_debit_value, total_credit_value, total_diffrence_value]
        # ax.barh(categories, amounts, color= Colors.ACTIVE_FOREGROUND, height=0.5)

        # # ax.set_xlabel("Cr/Dr")
        # # ax.set_ylabel("Amount")
        # ax.set_title(total_diffrence_value)

        # fig.tight_layout()

        # canvas = FigureCanvasTkAgg(fig, master=self)
        # canvas.draw()
        # canvas.get_tk_widget().pack()


class RecieceData(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=Colors.BACKGROUND, **kwargs)

        self.total_pie_graph()

    def total_pie_graph(self):
        # values
        total_debit_value = self.master.all_positive_df.shape[0]
        total_credit_value = self.master.all_negative_df.shape[0]
        total_sum_value = total_debit_value+total_credit_value
        # print(total_debit_value)

        fig = Figure(figsize=(5,4), dpi=100, facecolor=Colors.BACKGROUND)
        ax = fig.add_subplot(111)
        ax.set_facecolor(Colors.BACKGROUND)


        categories = ['Dr', 'Cr']
        amounts = [total_debit_value, total_credit_value]
        mycolors = [Colors.FG_SHADE_1, Colors.FG_SHADE_3]
        ax.pie(amounts, labels=categories, colors=mycolors, autopct='%1.1f%%')
        ax.set_title(total_sum_value)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()


class AccountsData(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=Colors.BACKGROUND, **kwargs)
        self.positive_scater_plot()

    def positive_scater_plot(self):
        # values
        df = self.master.all_positive_df
        
        fig = Figure(figsize=(5,4), dpi=100, facecolor=Colors.BACKGROUND)
        ax = fig.add_subplot(111)
        ax.set_facecolor(Colors.BACKGROUND)


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
        super().__init__(master, bg=Colors.BACKGROUND, **kwargs)
        
        self.total_pie_graph()

    def total_pie_graph(self):
        # values
        total_debit_value = self.master.all_positive_df['Amount'].sum()
        total_credit_value = self.master.all_negative_df['Amount'].sum()*(-1)
        total_sum_value = round(total_debit_value-total_credit_value, 2)

        fig = Figure(figsize=(5,4), dpi=100, facecolor=Colors.BACKGROUND)
        ax = fig.add_subplot(111)
        ax.set_facecolor(Colors.BACKGROUND)


        categories = ['Dr', 'Cr']
        amounts = [total_debit_value, total_credit_value]
        mycolors = [Colors.FG_SHADE_1, Colors.FG_SHADE_3]
        ax.pie(amounts, labels=categories, colors=mycolors, autopct='%1.1f%%')
        ax.set_title(total_sum_value)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()


class KrarData(tk.Frame):
    def __init__(self, master, **kwargs):
        
        super().__init__(master, bg=Colors.BACKGROUND, **kwargs)


        self.todo_title = tk.Label(self, text='To DO', font="Consolas 16", bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_3, anchor='center')
        self.todo_title.place(relx=0, rely=0,relheight=0.05, relwidth=1)

        self.table_frame = ScrollableLabelFrame(self, bg=Colors.BACKGROUND)
        self.table_frame.place(relx=0, rely=0.05, relwidth=1, relheight=0.7)
        # self.table_frame.pack(fill="both", expand=1)
        self.down_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        self.down_frame.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
        # self.down_frame.pack(fill="both", expand=1)
        # self.show_table()

        # down table
        self.table_list = []
        myset = set()
        all_krars = krar.get_all_due_krars()
        for krar1 in all_krars:
            myset.add(krar1[1])

        self.table_list = list(myset)

        today_krar_list = krar.get_krars_by_date()
        f = 1
        for i in today_krar_list:
            # print(i)
            self.table_frame.add_label(i[1], f)
            # self.table_frame.add_label(i[2], f)
            if f:
                f=0
            else:
                f=1

        # print(all_krars)
        self.table_dropdown = ttk.Combobox(self.down_frame, values= self.table_list, font = "Consolas 12")
        self.table_dropdown.pack(padx=12, ipady=4, fill="x", expand=1)

        save_button = tk.Button(self.down_frame, text="Set Done", font="Consolas 14", command=self.set_undue_krar, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_3, relief='groove')
        save_button.pack(padx=12, pady=12, fill="x", expand=1)
        

    def set_undue_krar(self):
        customer_name = self.table_dropdown.get()
        if customer_name:
            krar.update_krar_tag_by_name(customer_name, 0)

    def show_data(self):
        table_data = set()
        t = krar.get_krars_by_date()
        max_len = 0
        for i in t:
            # print(i)
            if len(i[1]) > max_len:
                max_len = len(i[1])
            krar_count = len(krar.get_due_krars_by_customer_name(i[1]))
            temp = [i[1], krar_count]#, i[2]
            table_data.add(tuple(temp))
            # print(krar_count)
            # table_data.append(temp)
            # table_data.append([])
        
        return table_data, max_len
        
    def show_table(self):
        table_data, max_len = self.show_data()
        column_name = ["Name", "Krar count"]
        
        if column_name and table_data:
            for widget in self.table_frame.winfo_children():
                widget.destroy()
                
            tree = ttk.Treeview(self.table_frame)
            tree['columns'] = column_name
            tree.column('#0', minwidth=5, anchor="w")

            for i in column_name:
                tree.column(i, minwidth=300,  anchor='w')
                tree.heading(i, text=i)
            
            c = 0
            for i in table_data:
                c += 1
                tg = 'odd'
                if c%2 == 0:
                    tg = "even"
                tree.insert('', c, text=c, values=i, tags = tg )

            tree.tag_configure('odd', background=Colors.ACTIVE_BACKGROUND)
            tree.tag_configure('even', background=Colors.ACTIVE_FOREGROUND)
            tree.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        else:
            print("Empty fields : Krar")



if __name__ == "__main__":
    app = tk.Tk()
    app.state("zoomed")
    h = HomePage(app)
    h.pack(expand=1, fill="both")
    app.mainloop()
