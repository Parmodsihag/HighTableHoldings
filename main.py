import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from datetime import datetime

from mytheme import Colors
from homepage import HomePage
from sales import SalesPage
from accountpage import AccountPage
from reports import ReportsPage
from add_items import AddItemsPage
from modifypage import ModifyPage
from kararpage import KararPage

from mypandasfile import get_all_list

class CustomLabel(tk.Label):
    def __init__(self, master, text, frame_to_link, **kwargs):
        super().__init__(master, text=text, font=("Consolas", 14), padx=20, pady=10, anchor="w", highlightthickness=0, highlightbackground=Colors.ACTIVE_FOREGROUND, **kwargs)

        self.frame1 = frame_to_link
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        
        self.normal_bg = Colors.BACKGROUND1
        self.normal_fg = Colors.FOREGROUND
        self.hover_bg = Colors.LIGHT_BG
        self.hover_fg = Colors.FOREGROUND
        self.active_bg = Colors.ACTIVE_BACKGROUND
        self.active_fg = Colors.FG_SHADE_1
        
        self.is_active = False
        self.is_hovering = False
        self.configure(background=self.normal_bg, foreground=self.normal_fg)

        
    def on_enter(self, event):
        if not self.is_active:
            self.configure(background=self.hover_bg, foreground=self.hover_fg)
            self.is_hovering = True
            
    def on_leave(self, event):
        if not self.is_active:
            self.configure(background=self.normal_bg, foreground=self.normal_fg)
            self.is_hovering = False
            
    def on_click(self, event):
        for  i in self.master.winfo_children():
            i.set_inactive()
    
        self.is_active = True
        self.is_hovering = False
        self.configure( foreground=self.active_fg)#, relief='groove')
        self.frame1.tkraise()
        
    def set_inactive(self):
        self.is_active = False
        self.is_hovering = False
        self.configure(background=self.normal_bg, foreground=self.normal_fg)#
    def set_active(self):
        self.is_active = True
        self.is_hovering = False
        self.configure(foreground=self.active_fg)#, relief='groove')
        self.frame1.tkraise()
    


class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("My App")
        self.state("zoomed")
        self.config(background=Colors.BACKGROUND1)

        style=ttk.Style()
        style.theme_create('mytheme', parent='alt', 
                        settings={
                            'TCombobox':
                            {
                                'configure':
                                {
                                'selectbackground': "#4EC5F1",
                                'fieldbackground': Colors.BACKGROUND3,
                                'background': Colors.BACKGROUND3,
                                'foreground': Colors.FG_SHADE_1,
                                'arrowcolor':Colors.FOREGROUND,
                                'arrowsize': 18,
                                'font':"Consolas 14"
                                }
                            },
                            'Treeview':{
                                'configure':
                                {
                                    'rowheight': 30,
                                    'fieldbackground': Colors.BACKGROUND,
                                    'font': 'Ubantu 10'
                                }
                            }
                        }
                    )
        style.theme_use('mytheme')
        style.configure("Treeview.Heading", foreground='#a0dad0', background=Colors.BACKGROUND1, font='Consolas 12')
        
        # main 4 parts 
        self.title_bar = tk.Frame(self, bg=Colors.BG_SHADE_1)
        self.title_bar.place(relx=0, rely=0, relheight=0.04, relwidth=1)

        self.menu_frame = tk.Frame(self, bg=Colors.BACKGROUND1)
        self.menu_frame.place(relx=0, rely=0.24, relheight=0.5, relwidth=0.1)
        self.action_frame = tk.Frame(self, bg=Colors.BACKGROUND1, padx=10, pady=10)
        self.action_frame.place(relx=0.1, rely=0.04, relheight=0.9, relwidth=0.9)
        self.status_bar = tk.Frame(self, bg=Colors.BG_SHADE_1)
        self.status_bar.place(relx=0, rely=0.94, relheight=0.06, relwidth=1)
        
        # logo
        self.logo_frame = tk.Frame(self)
        self.logo_frame.place(relx=0, rely=0.04, relheight=0.2, relwidth=0.1)
        self.logo_image = PhotoImage(file="myicons/logo.png")
        logo_image_label = tk.Label(self.logo_frame, image=self.logo_image, background=Colors.BACKGROUND1)
        logo_image_label.pack( fill="both", expand=1)
        
        self.title_bar_f(self.title_bar)
        
        self.status = tk.StringVar()
        self.statusl = tk.Label(self.status_bar, textvariable=self.status, font="Consolas 18", background=Colors.BG_SHADE_1, fg=Colors.ACTIVE_FOREGROUND)
        self.statusl.pack(anchor="e")
        self.status.set("|Status Bar|")
        

        # adding other views frames
        # self.homeframe = tk.Frame(self.action_frame, bg=Colors.ACTIVE_BACKGROUND)
        self.homeframe = HomePage(self.action_frame)
        self.homeframe.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.saleframe = SalesPage(self.action_frame)
        self.saleframe.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.accountframe = AccountPage(self.action_frame)
        self.accountframe.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.additemframe = AddItemsPage(self.action_frame)
        self.additemframe.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.reportframe = ReportsPage(self.action_frame)
        self.reportframe.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.modifyframe = ModifyPage(self.action_frame)
        self.modifyframe.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.kararframe = KararPage(self.action_frame)
        self.kararframe.place(relx=0, rely=0, relheight=1, relwidth=1)

        # adding labels in menu
        self.home_page_label = CustomLabel(self.menu_frame, "Home",self.homeframe)
        self.home_page_label.pack( fill="x")
        self.sale_page_label = CustomLabel(self.menu_frame, "Sale", self.saleframe)
        self.sale_page_label.pack( fill="x")
        self.account_page_label = CustomLabel(self.menu_frame, "Account", self.accountframe)
        self.account_page_label.pack( fill="x")
        self.add_item_page_label = CustomLabel(self.menu_frame, "Add Items", self.additemframe)
        self.add_item_page_label.pack( fill="x")
        self.report_frame_label = CustomLabel(self.menu_frame, "Reports", self.reportframe)
        self.report_frame_label.pack( fill="x")
        self.modify_frame_label = CustomLabel(self.menu_frame, "Modify", self.modifyframe)
        self.modify_frame_label.pack( fill="x")
        self.karar_frame_label = CustomLabel(self.menu_frame, "Karar", self.kararframe)
        self.karar_frame_label.pack( fill="x")

        # activating home page
        self.home_page_label.set_active()
        # self.sale_page_label.set_active()
        # self.account_page_label.set_active()
        # self.report_frame_label.set_active()
        # self.modify_frame_label.set_active()
        # self.karar_frame_label.set_active()

        # data_process = multiprocessing.Process(target=self.my_parallel_processes, args=(1,2))
        # data_process.start()

        # data_process.join()

    def title_bar_f(self, master):
        today = datetime.now().strftime('%d %m|%Y')
        company_name = tk.Label(master, text="JAAT BEAJ BHANDER", font="Consolas 16", bg= Colors.BG_SHADE_1, fg=Colors.FG_SHADE_3)
        company_name.place(relx=0.01, rely=0)
        today_date = tk.Label(master, text=today, font="Consolas 16", bg= Colors.BG_SHADE_1, fg=Colors.FG_SHADE_1)
        today_date.place(relx=0.9, rely=0)

        show_graph_label = tk.Label(master, text="#", font="Consolas 16", bg= Colors.BG_SHADE_1, fg=Colors.FG_SHADE_1)
        show_graph_label.place(relx=0.8, rely=0)
        show_graph_label.bind("<Button-1>",lambda e: self.my_parallel_processes())

    def set_status(self,s):
        self.status.set(s)

    def my_parallel_processes(self):
        accounts_df = get_all_list()
        self.homeframe.all_graphs_function(accounts_df)
        self.reportframe.parallel_process_combo(accounts_df)
    
    # def start_processing(self):
    #     with ThreadPoolExecutor() as executor:
    #         executor.submit(self.my_parallel_processes)


if __name__ == "__main__":
    # accounts_df = get_all_list()
    app = MyApp()
    # app.start_processing()
    # data_process = multiprocessing.Process(target=app.my_parallel_processes, args=(1,))
    # data_process.start()
    app.mainloop()
    # page 52 clouse 6.3
    # app.my_parallel_processes(1)
