# main.py
# import time
# st = time.time()
import os
import tkinter as tk
from tkinter import ttk, PhotoImage
from datetime import datetime

# Import color definitions and themes
from gui.mytheme import Colors, Colors1 

# Import your GUI classes (adjust the paths if necessary)
from gui.homepage import HomePage 
from gui.sales import SalesPage
from gui.accounts import AccountPage
from gui.items import AddItemsPage 
from gui.karar import KararPage
from gui.reports import ReportsPage
from gui.modify import ModifyPage
from gui.crop_trading import CropTradingPage 

# Import any necessary utility functions
from mypandasfile import get_all_list

# Import database modules needed for initialization check
from database import crop_database, accounts, inventory, database, krar


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
        self.customlabel.configure( foreground=self.active_fg)#, relief='solid')
        self.customlabel1.configure( background=self.active_fg)#, relief='solid')
        self.frame1.tkraise()
        
    def set_inactive(self):
        self.is_active = False
        self.is_hovering = False
        self.customlabel.configure(background=self.normal_bg, foreground=self.normal_fg)
        self.customlabel1.configure(background=self.normal_bg)

    def set_active(self):
        self.is_active = True
        self.is_hovering = False
        self.customlabel.configure(foreground=self.active_fg)#, relief='solid')
        self.customlabel1.configure(background=self.active_fg)#, relief='solid')
        self.frame1.tkraise()



class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_folder_and_subfolder()
        crop_database.initialize_database()
        self.themeint = 0
        self.is_graph_ready = 0
        self.title("High Table Holdings")
        self.state("zoomed")
        # self.config(background=Colors.BACKGROUND1)
        # self.clrs = Colors
        # img = tk.PhotoImage(file="myicons\\framebg2.png")

        # self.background_title = tk.Label(self, image=img)
        # self.background_title.place(relx=0, rely=0, relheight=1, relwidth=1)

        # self.img = img

        self.style=ttk.Style()
        self.style.theme_create('mytheme', parent='default', 
                        settings={
                            # 'TCombobox':
                            # {
                            #     'configure':
                            #     {
                            #     # 'arrowsize': 12,
                            #     'font':"Consolas 14",
                            #     'relief':'flat'
                            #     }
                            # },
                            'Treeview':{
                                'configure':
                                {
                                    'rowheight': 28,
                                    'font': 'Ubantu 10'
                                }
                            }
                        }
                    )
        # self.style.theme_use('mytheme')
        # self.style.configure('TCombobox', selectbackground=Colors.FG_SHADE_1, 
        #                     fieldbackground=Colors.BACKGROUND, 
        #                     background=Colors.BACKGROUND, 
        #                     foreground=Colors.FG_SHADE_1, 
        #                     arrowcolor=Colors.FOREGROUND,
        #                     borderwidth=1)
        # self.style.configure('Treeview', fieldbackground=Colors.BACKGROUND, font="Consolas 18", rowheight=35)
        # self.style.configure("Treeview.Heading", foreground=Colors.FOREGROUND, background=Colors.BACKGROUND1, font='Consolas 14')

        self.style.configure('Treeview', fieldbackground=Colors.BACKGROUND, font="Consolas 18", rowheight=35)
        self.style.configure("Treeview.Heading", foreground=Colors.FOREGROUND, background=Colors.BACKGROUND1, font='Consolas 14')
        # Configure TCombobox style explicitly here or in toggle_theme
        self.style.map('TCombobox', fieldbackground=[('readonly', Colors.BACKGROUND3)]) # Example for readonly state
        self.style.map('TCombobox', foreground=[('readonly', Colors.FG_SHADE_1)])
        self.style.map('TCombobox', selectbackground=[('readonly', Colors.ACTIVE_BACKGROUND)])
        self.style.map('TCombobox', selectforeground=[('readonly', Colors.ACTIVE_FOREGROUND)])



        # self.chatbot_instance = None


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
        
        # self.croptradeframe = CropTradingPage(self.action_frame) # <--- Create Crop Trading Frame
        # self.croptradeframe.place(relx=0, rely=0, relheight=1, relwidth=1)
        # self.billframe = BillPage(self.action_frame)
        # self.billframe.place(relx=0, rely=0, relheight=1, relwidth=1)
        # self.billshowframe = BillShowPage(self.action_frame)
        # self.billshowframe.place(relx=0, rely=0, relheight=1, relwidth=1)

        # adding labels in menu
        # self.home_page_label = CustomFrame(self.menu_frame, "Home",self.homeframe)
        # self.home_page_label.pack( fill="x")
        # self.sale_page_label = CustomFrame(self.menu_frame, "Sale", self.saleframe)
        # self.sale_page_label.pack( fill="x")
        self.home_page_label = CustomLabel(self.menu_frame, "Home ",self.homeframe, "H")
        self.home_page_label.pack( fill="x")
        self.sale_page_label = CustomLabel(self.menu_frame, "Sale ", self.saleframe, "S")
        self.sale_page_label.pack( fill="x")
        self.account_page_label = CustomLabel(self.menu_frame, "Account ", self.accountframe, 'A')
        self.account_page_label.pack( fill="x")
        self.add_item_page_label = CustomLabel(self.menu_frame, "Items ", self.additemframe, 'I')
        self.add_item_page_label.pack( fill="x")
        self.karar_frame_label = CustomLabel(self.menu_frame, "Karar ", self.kararframe, 'K')
        self.karar_frame_label.pack( fill="x")
        self.modify_frame_label = CustomLabel(self.menu_frame, "Modify ", self.modifyframe, 'M')
        self.modify_frame_label.pack( fill="x")
        self.report_frame_label = CustomLabel(self.menu_frame, "Reports ", self.reportframe, 'R')
        self.report_frame_label.pack( fill="x")
        # self.crop_trading_label = CustomLabel(self.menu_frame, "Crop Trade ", self.croptradeframe, 'C') # <--- Add Label
        # self.crop_trading_label.pack( fill="x") # <--- Pack it
        # self.bill_frame_label = CustomLabel(self.menu_frame, "Bills ", self.billframe, 'B')
        # self.bill_frame_label.pack( fill="x")
        # self.bill_show_frame_label = CustomLabel(self.menu_frame, "Bill ", self.billshowframe, 'T')
        # self.bill_show_frame_label.pack( fill="x")

        self.bind()
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

        show_graph_label = tk.Label(master, text="📊", font="Consolas 16", bg= Colors.BG_SHADE_1, fg=Colors.FG_SHADE_1)
        show_graph_label.place(relx=0.8, rely=0)
        show_graph_label.bind("<Button-1>",lambda e: self.my_parallel_processes())

        change_theme_label = tk.Label(master, text="🎨", font="Consolas 16", bg= Colors.BG_SHADE_1, fg=Colors.FG_SHADE_1)
        change_theme_label.place(relx=0.78, rely=0)
        change_theme_label.bind("<Button-1>",lambda e: self.togle_theme())

    # ---Function to show/hide chatbot ---
    
    def set_status(self,s):
        self.status.set(s)

    def togle_theme(self):
        # ... (your theme toggling logic) ...
        global Colors # Make sure Colors is updated globally if needed by other modules
        if self.themeint:
            Colors = Colors1 # Use Colors1 instance directly
            self.themeint = 0
        else:
            Colors = Colors # Use Colors instance directly
            self.themeint = 1

        # Update styles and widgets recursively
        self.update_widget_colors(self, Colors) # Pass the selected theme instance
        # Update specific pages if they cache Colors
        self.homeframe.Colors = Colors
        self.reportframe.Colors = Colors
        # self.chatbotpage.Colors = Colors # If ChatbotPage uses self.Colors

        # Update styles
        self.style.configure('Treeview', fieldbackground=Colors.BACKGROUND)
        self.style.configure("Treeview.Heading", foreground=Colors.FOREGROUND, background=Colors.BACKGROUND1)
        self.style.map('TCombobox', fieldbackground=[('readonly', Colors.BACKGROUND3)])
        self.style.map('TCombobox', foreground=[('readonly', Colors.FG_SHADE_1)])
        self.style.map('TCombobox', selectbackground=[('readonly', Colors.ACTIVE_BACKGROUND)])
        self.style.map('TCombobox', selectforeground=[('readonly', Colors.ACTIVE_FOREGROUND)])

        if self.is_graph_ready:
            self.homeframe.redraw_graphs()


    def update_widget_colors(self, widget, colors):
        # ... (your recursive color update logic) ...
        # Ensure it handles all widget types correctly based on the 'colors' object passed in
        widget_bg = colors.BACKGROUND
        widget_fg = colors.FOREGROUND
        active_bg = colors.ACTIVE_BACKGROUND
        active_fg = colors.ACTIVE_FOREGROUND
        entry_bg = colors.BACKGROUND3
        entry_fg = colors.FG_SHADE_1
        button_fg = colors.FG_SHADE_3
        label_fg = colors.ACTIVE_FOREGROUND # Or colors.FOREGROUND depending on label type

        config_opts = {}

        # --- Frame / Toplevel ---
        if isinstance(widget, (tk.Frame, tk.Toplevel, tk.PanedWindow)):
             config_opts['bg'] = widget_bg

        # --- Label ---
        elif isinstance(widget, tk.Label):
             # Be careful not to override labels meant to stay a specific color (like titles)
             # Maybe check current bg/fg before changing?
             # Simple approach: change all non-title-bar labels
             if widget.master != self.title_bar and widget.master != self.status_bar:
                  config_opts['background'] = widget_bg
                  # Decide on foreground based on role, default to standard FG
                  config_opts['foreground'] = label_fg if widget.cget('foreground') != colors.FG_SHADE_3 else colors.FG_SHADE_3

        # --- Button ---
        elif isinstance(widget, tk.Button):
             config_opts['background'] = widget_bg # Or BACKGROUND1/3?
             config_opts['foreground'] = button_fg
             config_opts['activebackground'] = active_bg
             config_opts['activeforeground'] = colors.BACKGROUND # Often white/black on active

        # --- Entry ---
        elif isinstance(widget, tk.Entry):
             config_opts['background'] = entry_bg
             config_opts['foreground'] = entry_fg
             config_opts['relief'] = 'solid' # Ensure relief matches theme
             config_opts['bd'] = 1
             config_opts['insertbackground'] = colors.FOREGROUND # Cursor

        # --- Text / ScrolledText ---
        # elif isinstance(widget, (tk.Text, scrolledtext.ScrolledText)):
        #      config_opts['background'] = entry_bg # Often same as Entry
        #      config_opts['foreground'] = entry_fg
        #      config_opts['insertbackground'] = colors.FOREGROUND # Cursor

        # --- Listbox ---
        elif isinstance(widget, tk.Listbox):
             config_opts['background'] = entry_bg
             config_opts['foreground'] = entry_fg
             config_opts['selectbackground'] = active_bg
             config_opts['selectforeground'] = colors.FOREGROUND

        # --- ttk Widgets (Check style configuration first) ---
        elif isinstance(widget, ttk.Combobox):
             # Primarily handled by style, but might set readonly bg/fg if needed
             pass # Rely on self.style updates
        elif isinstance(widget, ttk.Treeview):
             pass # Rely on self.style updates
        elif isinstance(widget, ttk.Scrollbar):
             # Often themed with parent, but might need explicit config
             pass

        # --- Custom Widgets ---
        elif isinstance(widget, CustomLabel):
             widget.normal_bg = colors.BACKGROUND1
             widget.normal_fg = colors.FOREGROUND
             widget.hover_bg = colors.LIGHT_BG
             widget.hover_fg = colors.FOREGROUND
             widget.active_bg = colors.ACTIVE_BACKGROUND
             widget.active_fg = colors.FG_SHADE_1
             # Re-apply current state colors
             if widget.is_active:
                  widget.customlabel.config(fg=widget.active_fg) # Keep bg as frame's bg
                  widget.customlabel1.config(bg=widget.active_fg) # Frame bg remains default
             elif widget.is_hovering:
                  widget.customlabel.config(bg=widget.hover_bg, fg=widget.hover_fg)
                  widget.customlabel1.config(bg=widget.hover_bg)
             else:
                  widget.customlabel.config(bg=widget.normal_bg, fg=widget.normal_fg)
                  widget.customlabel1.config(bg=widget.normal_bg)
             # Configure the frame itself
             config_opts['bg'] = widget_bg # Set frame background

        # Apply collected configurations
        if config_opts:
             try:
                  widget.configure(**config_opts)
             except tk.TclError as e:
                  # Ignore errors for widgets that don't support certain options (like 'bg' for ttk widgets)
                  # print(f"TclError configuring {widget.winfo_class()}: {e}")
                  pass


        # Recursively update children
        for child in widget.winfo_children():
            self.update_widget_colors(child, colors) # Pass the selected theme object 

    def my_parallel_processes(self):
        # ... (load data and update graph/report pages) ...
        # This should ideally run in a separate thread or process
        # to avoid blocking the GUI, especially if data loading is slow.
        # For simplicity now, it runs synchronously.
        print("Starting data processing...")
        self.set_status("Loading dashboard data...")
        try:
             accounts_df = get_all_list() # Fetch fresh data
             self.homeframe.all_graphs_function(accounts_df)
             self.reportframe.parallel_process_combo(accounts_df) # Update reports page combo/data
             self.is_graph_ready = 1
             self.set_status("Dashboard data loaded.")
             print("Data processing finished.")
        except Exception as e:
             self.set_status(f"[Error] Loading dashboard data: {e}")
             print(f"Error in my_parallel_processes: {e}")
    
    # def start_processing(self):
    #     with ThreadPoolExecutor() as executor:
    #         executor.submit(self.my_parallel_processes)


if __name__ == "__main__":
    # accounts_df = get_all_list()
    app = MyApp()
    # app.start_processing()
    # data_process = multiprocessing.Process(target=app.my_parallel_processes, args=(1,))
    # data_process.start()
    # print(time.time()-st)
    app.mainloop()
    # page 52 clouse 6.3
    # app.my_parallel_processes(1)
