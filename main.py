import tkinter as tk
import os
from tkinter import ttk
from tkinter import PhotoImage
from datetime import datetime
# from PIL import Image, ImageTk

from mytheme import Colors, Colors1
from homepage import HomePage
from sales import SalesPage
from accountpage import AccountPage
from reports import ReportsPage
from add_items import AddItemsPage
from modifypage import ModifyPage
from kararpage import KararPage
from bills.billpage import BillPage
from bills.billshowpage import BillShowPage
from mypandasfile import get_all_list


class CustomLabel(tk.Frame):
    def __init__(self, master, text, frame_to_link, x, **kwargs):
        super().__init__(master, highlightbackground=Colors.ACTIVE_FOREGROUND, **kwargs)
        self.customlabel = tk.Label(self, text=text, font=("Consolas", 14), anchor="e")#, pady=10, highlightthickness=0, padx=20, pady=10, anchor="w", highlightthickness=0, highlightbackground=Colors.ACTIVE_FOREGROUND)
        self.customlabel.pack(fill='both', side="right", expand=1)

        self.customlabel1 = tk.Label(self, text="", font=("Consolas", 20), anchor='w')
        self.customlabel1.pack(side='left',fill='x')#, expand=1)

        self.frame1 = frame_to_link
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.customlabel.bind("<Button-1>", self.on_click)
        self.customlabel1.bind("<Button-1>", self.on_click)

        # self.Colors = Colors
        
        self.normal_bg = Colors.BACKGROUND1
        self.normal_fg = Colors.FOREGROUND
        self.hover_bg = Colors.LIGHT_BG
        self.hover_fg = Colors.FOREGROUND
        self.active_bg = Colors.ACTIVE_BACKGROUND
        self.active_fg = Colors.FG_SHADE_1
        
        self.is_active = False
        self.is_hovering = False
        self.customlabel.configure(background=self.normal_bg, foreground=self.normal_fg)
        self.customlabel1.configure(background=self.normal_bg)
        self.master.master.bind(f"<Alt-{x}>", self.alt_key)  # Bind Alt + x key
        self.x = x
        # print(self.x)

    def alt_key(self, event):
        # print(event.char.isdigit())
        if event.char == self.x:
            self.on_click(event)

        # if event.char.isdigit():
        #     key_pressed = int(event.char)
        #     print(key_pressed, self.x, key_pressed== self.x)
        #     if key_pressed == self.x:
        #         self.on_click(event)

        
    def on_enter(self, event):
        if not self.is_active:
            self.customlabel.configure(background=self.hover_bg, foreground=self.hover_fg)
            self.customlabel1.configure(background=self.hover_bg, foreground=self.hover_fg)
            self.is_hovering = True
            
    def on_leave(self, event):
        if not self.is_active:
            self.customlabel.configure(background=self.normal_bg, foreground=self.normal_fg)
            self.customlabel1.configure(background=self.normal_bg, foreground=self.normal_fg)
            self.is_hovering = False
            
    def on_click(self, event):
        # print('click')
        for  i in self.master.winfo_children():
            # print('clicksdf')
            i.set_inactive()
    
        self.is_active = True
        self.is_hovering = False
        self.customlabel.configure( foreground=self.active_fg)#, relief='groove')
        self.customlabel1.configure( background=self.active_fg)#, relief='groove')
        self.frame1.tkraise()
        
    def set_inactive(self):
        self.is_active = False
        self.is_hovering = False
        self.customlabel.configure(background=self.normal_bg, foreground=self.normal_fg)
        self.customlabel1.configure(background=self.normal_bg)

    def set_active(self):
        self.is_active = True
        self.is_hovering = False
        self.customlabel.configure(foreground=self.active_fg)#, relief='groove')
        self.customlabel1.configure(background=self.active_fg)#, relief='groove')
        self.frame1.tkraise()

# class CustomLabel(tk.Label):
#     def __init__(self, master, text, frame_to_link, **kwargs):
#         super().__init__(master, text=text, font=("Consolas", 14), padx=20, pady=10, anchor="w", highlightthickness=0, highlightbackground=Colors.ACTIVE_FOREGROUND, **kwargs)

#         self.frame1 = frame_to_link
#         self.bind("<Enter>", self.on_enter)
#         self.bind("<Leave>", self.on_leave)
#         self.bind("<Button-1>", self.on_click)
        
#         self.normal_bg = Colors.BACKGROUND1
#         self.normal_fg = Colors.FOREGROUND
#         self.hover_bg = Colors.LIGHT_BG
#         self.hover_fg = Colors.FOREGROUND
#         self.active_bg = Colors.ACTIVE_BACKGROUND
#         self.active_fg = Colors.FG_SHADE_1
        
#         self.is_active = False
#         self.is_hovering = False
#         self.configure(background=self.normal_bg, foreground=self.normal_fg)

        
#     def on_enter(self, event):
#         if not self.is_active:
#             self.configure(background=self.hover_bg, foreground=self.hover_fg)
#             self.is_hovering = True
            
#     def on_leave(self, event):
#         if not self.is_active:
#             self.configure(background=self.normal_bg, foreground=self.normal_fg)
#             self.is_hovering = False
            
#     def on_click(self, event):
#         for  i in self.master.winfo_children():
#             i.set_inactive()
    
#         self.is_active = True
#         self.is_hovering = False
#         self.configure( foreground=self.active_fg)#, relief='groove')
#         self.frame1.tkraise()
        
#     def set_inactive(self):
#         self.is_active = False
#         self.is_hovering = False
#         self.configure(background=self.normal_bg, foreground=self.normal_fg)#
#     def set_active(self):
#         self.is_active = True
#         self.is_hovering = False
#         self.configure(foreground=self.active_fg)#, relief='groove')
#         self.frame1.tkraise()
    


class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_folder_and_subfolder()
        self.themeint = 0
        self.is_graph_ready = 0
        self.title("High Table Holdings")
        self.state("zoomed")
        self.config(background=Colors.BACKGROUND1)
        # self.clrs = Colors
        img = tk.PhotoImage(file="myicons\\framebg2.png")

        self.background_title = tk.Label(self, image=img)
        self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.img = img

        self.style=ttk.Style()
        self.style.theme_create('mytheme', parent='alt', 
                        settings={
                            'TCombobox':
                            {
                                'configure':
                                {
                                'arrowsize': 18,
                                'font':"Consolas 14"
                                }
                            },
                            'Treeview':{
                                'configure':
                                {
                                    'rowheight': 20,
                                    'font': 'Ubantu 10'
                                }
                            }
                        }
                    )
        self.style.theme_use('mytheme')
        self.style.configure('TCombobox', selectbackground=Colors.FG_SHADE_1, 
                            fieldbackground=Colors.BACKGROUND3, 
                            background=Colors.BACKGROUND3, 
                            foreground=Colors.FG_SHADE_1, 
                            arrowcolor=Colors.FOREGROUND)
        self.style.configure('Treeview', fieldbackground=Colors.BACKGROUND)
        self.style.configure("Treeview.Heading", foreground=Colors.FOREGROUND, background=Colors.BACKGROUND1, font='Consolas 12')

        # main 4 parts 
        self.title_bar = tk.Frame(self, bg=Colors.BG_SHADE_1)
        self.title_bar.place(relx=0, rely=0, relheight=0.04, relwidth=1)

        self.menu_frame = tk.Frame(self, bg=Colors.BACKGROUND1)
        self.menu_frame.place(relx=0.005, rely=0.255, relheight=0.675, relwidth=0.095)
        self.action_frame = tk.Frame(self, bg=Colors.BACKGROUND1)
        self.action_frame.place(relx=0.1, rely=0.04, relheight=0.9, relwidth=0.9)
        self.status_bar = tk.Frame(self, bg=Colors.BG_SHADE_1)
        self.status_bar.place(relx=0, rely=0.94, relheight=0.06, relwidth=1)


        
        # logo
        self.logo_frame = tk.Frame(self)
        self.logo_frame.place(relx=0.005, rely=0.05, relheight=0.2, relwidth=0.095)
        self.logo_image = PhotoImage(file="myicons/logos.png")
        logo_image_label = tk.Label(self.logo_frame, image=self.logo_image, background=Colors.BACKGROUND1)
        logo_image_label.pack( fill="both", expand=1)
        
        # img = tk.PhotoImage(file="myicons\\framebg2.png")

        # self.background_title = tk.Label(self.logo_frame, image=img)
        # self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)

        # self.img = img

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
        self.kararframe = KararPage(self.action_frame)
        self.kararframe.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.reportframe = ReportsPage(self.action_frame)
        self.reportframe.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.modifyframe = ModifyPage(self.action_frame)
        self.modifyframe.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.billframe = BillPage(self.action_frame)
        self.billframe.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.billshowframe = BillShowPage(self.action_frame)
        self.billshowframe.place(relx=0, rely=0, relheight=1, relwidth=1)

        # adding labels in menu
        # self.home_page_label = CustomFrame(self.menu_frame, "Home",self.homeframe)
        # self.home_page_label.pack( fill="x")
        # self.sale_page_label = CustomFrame(self.menu_frame, "Sale", self.saleframe)
        # self.sale_page_label.pack( fill="x")
        self.home_page_label = CustomLabel(self.menu_frame, "Home ",self.homeframe, "h")
        self.home_page_label.pack( fill="x")
        self.sale_page_label = CustomLabel(self.menu_frame, "Sale ", self.saleframe, "s")
        self.sale_page_label.pack( fill="x")
        self.account_page_label = CustomLabel(self.menu_frame, "Account ", self.accountframe, 'a')
        self.account_page_label.pack( fill="x")
        self.add_item_page_label = CustomLabel(self.menu_frame, "Items ", self.additemframe, 'i')
        self.add_item_page_label.pack( fill="x")
        self.karar_frame_label = CustomLabel(self.menu_frame, "Karar ", self.kararframe, 'k')
        self.karar_frame_label.pack( fill="x")
        self.modify_frame_label = CustomLabel(self.menu_frame, "Modify ", self.modifyframe, 'm')
        self.modify_frame_label.pack( fill="x")
        self.report_frame_label = CustomLabel(self.menu_frame, "Reports ", self.reportframe, 'r')
        self.report_frame_label.pack( fill="x")
        self.bill_frame_label = CustomLabel(self.menu_frame, "Bills ", self.billframe, 'b')
        self.bill_frame_label.pack( fill="x")
        self.bill_show_frame_label = CustomLabel(self.menu_frame, "Bill ", self.billshowframe, 't')
        self.bill_show_frame_label.pack( fill="x")

        # activating home page
        self.home_page_label.set_active()

        self.bind()
        # self.sale_page_label.set_active()
        # self.account_page_label.set_active()
        # self.report_frame_label.set_active()
        # self.modify_frame_label.set_active()
        # self.karar_frame_label.set_active()

        # data_process = multiprocessing.Process(target=self.my_parallel_processes, args=(1,2))
        # data_process.start()

        # data_process.join()

    def create_folder_and_subfolder(self):
        """Creates the folder JBB in the C drive and a subfolder named data,
        if they don't already exist.
        """

        folder_path = "C:/JBB"
        subfolder_path_data = os.path.join(folder_path, "data")
        subfolder_path_bills = os.path.join(folder_path, "bills")
        subfolder_path_pdfs = os.path.join(folder_path, "pdfs")
        subfolder_path_merged_pdfs = os.path.join(folder_path, "merged_pdfs")

        try:
            os.makedirs(folder_path, exist_ok=True)  # Create parent folders if needed
            os.makedirs(subfolder_path_data, exist_ok=True)  # Create parent folders if needed
            os.makedirs(subfolder_path_bills, exist_ok=True)  # Create parent folders if needed
            os.makedirs(subfolder_path_pdfs, exist_ok=True)  # Create parent folders if needed
            os.makedirs(subfolder_path_merged_pdfs, exist_ok=True)  # Create parent folders if needed
            # print(f"Folder structure created successfully: {subfolder_path}")
        except OSError as e:
            print(f"Error creating folder structure: {e}")

    def title_bar_f(self, master):
        today = datetime.now().strftime('%d %m|%Y')
        company_name = tk.Label(master, text="JAAT BEAJ BHANDER", font="Consolas 16", bg= Colors.BG_SHADE_1, fg=Colors.FG_SHADE_3)
        company_name.place(relx=0.01, rely=0)
        today_date = tk.Label(master, text=today, font="Consolas 16", bg= Colors.BG_SHADE_1, fg=Colors.FG_SHADE_1)
        today_date.place(relx=0.9, rely=0)

        show_graph_label = tk.Label(master, text="#", font="Consolas 16", bg= Colors.BG_SHADE_1, fg=Colors.FG_SHADE_1)
        show_graph_label.place(relx=0.8, rely=0)
        show_graph_label.bind("<Button-1>",lambda e: self.my_parallel_processes())

        change_theme_label = tk.Label(master, text="@", font="Consolas 16", bg= Colors.BG_SHADE_1, fg=Colors.FG_SHADE_1)
        change_theme_label.place(relx=0.78, rely=0)
        change_theme_label.bind("<Button-1>",lambda e: self.togle_theme())

    def set_status(self,s):
        self.status.set(s)

    def togle_theme(self):
        if self.themeint:
            colors = Colors
            self.themeint = 0
        else:
            colors = Colors1
            self.themeint = 1

        self.update_widget_colors(widget=self, colors=colors)
        self.homeframe.Colors = colors
        self.reportframe.Colors = colors
        self.billframe.Colors = colors
        self.style.configure('TCombobox', selectbackground=colors.FG_SHADE_1, 
                            fieldbackground=colors.BACKGROUND3, 
                            background=colors.BACKGROUND3, 
                            foreground=colors.FG_SHADE_1, 
                            arrowcolor=colors.FOREGROUND)
        self.style.configure('Treeview', fieldbackground=colors.BACKGROUND)
        self.style.configure("Treeview.Heading", foreground=colors.FOREGROUND, 
                                background=colors.BACKGROUND1)

        if self.is_graph_ready:
            self.homeframe.redraw_graphs()

    def update_widget_colors(self, widget, colors):
        """
        Recursively updates the colors of a widget and its children based on the current theme.

        Args:
            widget (tk.Widget): The widget to start updating colors from.
        """

        if isinstance(widget, CustomLabel):
            # widget.Colors = colors
            widget.normal_bg = colors.BACKGROUND
            widget.normal_fg = colors.FOREGROUND
            widget.hover_bg = colors.LIGHT_BG
            widget.hover_fg = colors.FOREGROUND
            widget.active_bg = colors.ACTIVE_BACKGROUND
            widget.active_fg = colors.FG_SHADE_1
        
        elif isinstance(widget, tk.Listbox):
            widget.config(background=colors.BACKGROUND)
        
        elif isinstance(widget, tk.Frame):
            widget.config(background=colors.BACKGROUND)

        elif isinstance(widget, tk.Label):
            widget.config(background=colors.BACKGROUND,
                foreground=colors.ACTIVE_FOREGROUND)
        
        elif isinstance(widget, ttk.Combobox):
            widget.config(
                          background= colors.BACKGROUND3,
                          foreground= colors.FG_SHADE_1)

        elif isinstance(widget, tk.Button):
            widget.config(activebackground=colors.ACTIVE_BACKGROUND, 
                          activeforeground=colors.ACTIVE_FOREGROUND, 
                          background=colors.BACKGROUND3, 
                          foreground=colors.FG_SHADE_3)

        elif isinstance(widget, tk.Entry):
            widget.config(background=colors.BACKGROUND3, 
                          foreground=colors.FG_SHADE_1)
        

        # Recursively update child widgets
        for child in widget.winfo_children():
            self.update_widget_colors(child, colors)
        
        

    def my_parallel_processes(self):
        if self.themeint:
            colors = Colors1
        else:
            colors = Colors
        
        self.homeframe.Colors = colors
        accounts_df = get_all_list()
        self.homeframe.all_graphs_function(accounts_df)
        self.reportframe.parallel_process_combo(accounts_df)
        self.is_graph_ready = 1

    
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
