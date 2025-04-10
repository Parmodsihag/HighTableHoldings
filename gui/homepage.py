# gui/homepage.py
import tkinter as tk
from tkinter import ttk, font as tkfont
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Assuming these imports are correct relative to homepage.py
from .mytheme import Colors
# Import all needed database modules
from database import accounts, inventory, database as daily_db, krar, crop_database

# Helper function (keep as is)
def create_card_frame(parent, text="", **kwargs):
    frame = ttk.LabelFrame(parent, text=text, padding=(10, 5), style='Card.TLabelframe', **kwargs)
    return frame

class HomePage(tk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, bg=Colors.BACKGROUND, **kwargs) # Set main background
        self.Colors = Colors # Store theme colors
        self.accounts_df = pd.DataFrame() # Initialize empty dataframe

        # --- Configure Styles (Add styles for new elements) ---
        self.style = ttk.Style(self)
        self.style.configure('Card.TLabelframe', background=Colors.BACKGROUND1, borderwidth=1, relief=tk.GROOVE)
        self.style.configure('Card.TLabelframe.Label', background=Colors.BACKGROUND1, foreground=Colors.ACTIVE_FOREGROUND, font=("Consolas", 12, "bold"))
        self.style.configure('KPI.TLabel', background=Colors.BACKGROUND1, foreground=Colors.FG_SHADE_1, font=("Consolas", 16, "bold"), anchor='center', padding=(0, 2)) # Adjusted KPI font/padding
        self.style.configure('KPITitle.TLabel', background=Colors.BACKGROUND1, foreground=Colors.FOREGROUND, font=("Consolas", 9), anchor='center') # Smaller KPI title
        self.style.configure('GraphTitle.TLabel', background=Colors.BACKGROUND1, foreground=Colors.FG_SHADE_3, font=("Consolas", 11, "bold"), anchor='center')

        # Treeview Styles (ensure applied correctly)
        self.style.configure('Treeview', background=Colors.BACKGROUND2, fieldbackground=Colors.BACKGROUND2, foreground=Colors.FOREGROUND, borderwidth=0)
        self.style.configure('Treeview.Heading', background=Colors.BG_SHADE_1, foreground=Colors.FG_SHADE_3, font='Consolas 10 bold', relief='flat')
        self.style.map('Treeview.Heading', relief=[('active','groove')]) # Simple hover effect
        self.style.map('Treeview', background=[('selected', Colors.ACTIVE_BACKGROUND)], foreground=[('selected', Colors.FG_SHADE_1)])

        # Style for the new lists (Low Stock, Crop Stock)
        self.style.configure('List.Treeview', background=Colors.BACKGROUND2, fieldbackground=Colors.BACKGROUND2, foreground=Colors.FOREGROUND)
        self.style.configure('List.Treeview.Heading', background=Colors.BG_SHADE_1, foreground=Colors.ACTIVE_FOREGROUND, font='Consolas 9 bold') # Slightly different heading

        # Notebook style
        self.style.configure("TNotebook", background=Colors.BACKGROUND, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=Colors.BACKGROUND1, foreground=Colors.FOREGROUND, padding=[8, 3], font=('Consolas', 10))
        self.style.map("TNotebook.Tab", background=[("selected", Colors.ACTIVE_BACKGROUND)], foreground=[("selected", Colors.FG_SHADE_1)])

        # Refresh Button Style
        self.style.configure("Refresh.TButton", font=("Consolas", 10), padding=5)
        self.style.map("Refresh.TButton",
                       background=[('active', Colors.LIGHT_BG), ('!active', Colors.BACKGROUND1)],
                       foreground=[('active', Colors.ACTIVE_FOREGROUND)])


        # --- Main Layout Frames ---
        self.grid_rowconfigure(0, weight=0) # Row 0 for KPIs & Refresh (fixed height)
        self.grid_rowconfigure(1, weight=1) # Row 1 expands (Graphs/Activity)
        self.grid_columnconfigure(0, weight=2) # Left column (graphs)
        self.grid_columnconfigure(1, weight=1) # Right column (Krar/Activity)

        # --- Top Bar Frame (KPIs + Refresh) ---
        self.top_bar_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        self.top_bar_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=(5,0))
        # Add Refresh button here
        self.refresh_button = ttk.Button(self.top_bar_frame, text="↻ Refresh",
                                        command=self.trigger_refresh, style="Refresh.TButton")
        self.refresh_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Frame for KPIs within the top bar
        self.kpi_frame = tk.Frame(self.top_bar_frame, bg=Colors.BACKGROUND)
        self.kpi_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)


        # --- Bottom Frames (Graphs/Activity) ---
        self.financial_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        self.financial_frame.grid(row=1, column=0, sticky="nsew", padx=(5,2), pady=5)

        self.activity_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        self.activity_frame.grid(row=1, column=1, sticky="nsew", padx=(2,5), pady=5)

        # --- Initial Loading State ---
        self.loading_label = ttk.Label(self, text="Loading Dashboard Data...",
                                      font="Consolas 24 bold", background=Colors.BACKGROUND,
                                      foreground=Colors.FOREGROUND, anchor='center')
        self.loading_label.place(relx=0.5, rely=0.5, anchor='center') # Centered

    def trigger_refresh(self):
        """Calls the main application's data refresh mechanism."""
        if hasattr(self.master, 'master') and hasattr(self.master.master, 'my_parallel_processes'):
            print("Triggering dashboard refresh...")
            # Show loading label temporarily
            self.loading_label.place(relx=0.5, rely=0.5, anchor='center')
            self.update_idletasks() # Ensure label is shown
            # Call the main app's refresh function (assuming it handles background loading)
            # If my_parallel_processes is blocking, this needs to be run in a thread from main.py
            try:
                self.master.master.my_parallel_processes()
                # Loading label will be hidden by all_graphs_function when data arrives
            except Exception as e:
                 print(f"Error during triggered refresh: {e}")
                 self.loading_label.place_forget() # Hide loading on error too
                 # Optionally show an error message on the dashboard
        else:
            print("Refresh function not found in main application.")

    def _clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def all_graphs_function(self, accounts_df):
        self.loading_label.place_forget()

        if accounts_df.empty:
            self._clear_frame(self.kpi_frame)
            self._clear_frame(self.financial_frame)
            self._clear_frame(self.activity_frame)
            error_label = ttk.Label(self, text="No Account Data Found",
                                   font="Consolas 20", background=Colors.BACKGROUND,
                                   foreground=Colors.ERROR, anchor='center')
            error_label.place(relx=0.5, rely=0.5, anchor='center')
            return

        self.accounts_df = accounts_df

        self.all_positive_df = self.accounts_df.loc[self.accounts_df['Amount'] >= 0].copy()
        self.all_negative_df = self.accounts_df.loc[self.accounts_df['Amount'] < 0].copy()

        # --- Fetch Additional Data ---
        self.inventory_total_value = inventory.get_total_inventory_value()
        self.low_stock_data = inventory.get_low_stock_items(threshold=10) # Example threshold
        self.crop_summary_data = crop_database.get_stock_summary() # Get crop data
        self.today_notes_count = daily_db.get_todays_notes_summary()

        # --- Populate Sections ---
        # Clear only frames that will be repopulated
        self._clear_frame(self.kpi_frame) # KPIs need recalculating
        self._clear_frame(self.financial_frame)
        self._clear_frame(self.activity_frame)

        self.create_kpi_cards()
        self.create_financial_graphs()
        self.create_activity_section() # This now includes Inventory/Crop lists

    def create_kpi_cards(self):
        # Calculate KPIs
        total_receivables = round(self.all_positive_df['Amount'].sum(), 2)
        total_payables = round(self.all_negative_df['Amount'].sum(), 2)
        net_position = round(total_receivables + total_payables, 2)
        krar_today_count = len(krar.get_customers_with_last_krar_today())
        krar_past_count = len(krar.get_customers_with_last_krar_past())

        kpis = [
            ("Receivables", f"₹{total_receivables:,.0f}", Colors.SUCCESS), # Simplified format
            ("Payables", f"₹{abs(total_payables):,.0f}", Colors.ERROR),
            ("Net Position", f"₹{net_position:,.0f}", Colors.FG_SHADE_1 if net_position >= 0 else Colors.REMINDER),
            ("Inventory Value", f"₹{self.inventory_total_value:,.0f}", Colors.ACTIVE_FOREGROUND),
            ("Krars Today", str(krar_today_count), Colors.ACTIVE_FOREGROUND),
            ("Krars Overdue", str(krar_past_count), Colors.REMINDER),
            ("Notes Today", str(self.today_notes_count), Colors.FG_SHADE_3),
        ]

        # Configure grid weights for KPIs dynamically
        num_kpis = len(kpis)
        for i in range(num_kpis):
            self.kpi_frame.grid_columnconfigure(i, weight=1, uniform="kpi_group") # Uniform makes columns equal width

        for i, (title, value, value_color) in enumerate(kpis):
            # Using a standard Frame for more background control if needed
            card = tk.Frame(self.kpi_frame, bg=Colors.BACKGROUND1, bd=1, relief=tk.SOLID)
            card.grid(row=0, column=i, sticky="nsew", padx=3, pady=3) # Reduced padding
            card.grid_rowconfigure(0, weight=1)
            card.grid_rowconfigure(1, weight=1)
            card.grid_columnconfigure(0, weight=1)

            # Use standard tk Labels if ttk style conflicts or for exact bg color
            tk.Label(card, text=title, font=("Consolas", 9), anchor='center',
                     bg=Colors.BACKGROUND1, fg=Colors.FOREGROUND).grid(row=0, column=0, sticky='ew', pady=(2,0))
            value_label = tk.Label(card, text=value, font=("Consolas", 16, "bold"), anchor='center',
                                  bg=Colors.BACKGROUND1, fg=value_color)
            value_label.grid(row=1, column=0, sticky='ew', pady=(0, 2))
            # For ttk:
            # ttk.Label(card, text=title, style='KPITitle.TLabel').grid(row=0, column=0, sticky='ew')
            # value_label = ttk.Label(card, text=value, style='KPI.TLabel', foreground=value_color)
            # value_label.grid(row=1, column=0, sticky='ew', pady=(0, 5))

    def create_financial_graphs(self):
        """Creates the financial graph section (bottom left)."""
        # Keep the 2x2 grid structure
        self.financial_frame.grid_rowconfigure(0, weight=1)
        self.financial_frame.grid_rowconfigure(1, weight=1)
        self.financial_frame.grid_columnconfigure(0, weight=1)
        self.financial_frame.grid_columnconfigure(1, weight=1)

        card1 = create_card_frame(self.financial_frame, text="Account Status (Count)")
        card1.grid(row=0, column=0, sticky="nsew", padx=(0,2), pady=(0,2))
        self.plot_account_count_pie(card1)

        card2 = create_card_frame(self.financial_frame, text="Financial Position (Amount)")
        card2.grid(row=0, column=1, sticky="nsew", padx=(2,0), pady=(0,2))
        self.plot_financial_position_pie(card2)

        card3 = create_card_frame(self.financial_frame, text="Receivables Overview (Amount vs Days)")
        card3.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(0,0), pady=(2,0))
        self.plot_receivables_scatter(card3)

    # --- Plotting functions (plot_account_count_pie, plot_financial_position_pie, plot_receivables_scatter) remain the same ---
    # (Keep implementations from the previous step)
    def plot_account_count_pie(self, parent_frame):
        """Plots the pie chart for Dr/Cr account counts."""
        count_dr = self.all_positive_df.shape[0]
        count_cr = self.all_negative_df.shape[0]
        total_accounts = count_dr + count_cr

        labels = [f'Receivable ({count_dr})', f'Payable ({count_cr})']
        sizes = [count_dr, count_cr]
        plot_colors = [self.Colors.SUCCESS, self.Colors.ERROR] # Green for Dr, Red for Cr
        explode = (0.05, 0) if count_dr > 0 else (0, 0) # Explode only if > 0

        if not any(sizes): # Avoid plotting if no data
            ttk.Label(parent_frame, text="No Account Data", style='KPITitle.TLabel').pack(expand=True)
            return

        fig = Figure(figsize=(4, 3), dpi=75, facecolor=self.Colors.BACKGROUND1) # Use card background
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.Colors.BACKGROUND1)

        wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=plot_colors,
                                          autopct='%1.1f%%', shadow=False, startangle=90,
                                          textprops={'color': self.Colors.FOREGROUND, 'fontsize': 9})
        for autotext in autotexts:
            autotext.set_color(self.Colors.BACKGROUND) # White text on wedges
            autotext.set_fontweight('bold')

        ax.axis('equal')
        fig.tight_layout(pad=0.5)
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_financial_position_pie(self, parent_frame):
        """Plots the pie chart for Dr/Cr total amounts."""
        total_dr = self.all_positive_df['Amount'].sum()
        total_cr = abs(self.all_negative_df['Amount'].sum()) # Use absolute value for size

        labels = [f'Receivables\n(₹{total_dr:,.0f})', f'Payables\n(₹{total_cr:,.0f})']
        sizes = [total_dr, total_cr]
        plot_colors = [self.Colors.SUCCESS, self.Colors.ERROR]
        explode = (0.05, 0) if total_dr > 0 else (0, 0)

        if not any(s > 0 for s in sizes): # Check if any size is positive
            ttk.Label(parent_frame, text="No Financial Data", style='KPITitle.TLabel').pack(expand=True)
            return

        fig = Figure(figsize=(4, 3), dpi=75, facecolor=self.Colors.BACKGROUND1)
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.Colors.BACKGROUND1)

        wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=plot_colors,
                                          autopct='%1.1f%%', shadow=False, startangle=90,
                                          textprops={'color': self.Colors.FOREGROUND, 'fontsize': 9})
        for autotext in autotexts:
             autotext.set_color(self.Colors.BACKGROUND)
             autotext.set_fontweight('bold')

        ax.axis('equal')
        fig.tight_layout(pad=0.5)
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_receivables_scatter(self, parent_frame):
        """Plots the scatter plot for positive balance accounts (Amount vs Days)."""
        df = self.all_positive_df

        if df.empty:
            ttk.Label(parent_frame, text="No Receivables Data", style='KPITitle.TLabel').pack(expand=True)
            return

        fig = Figure(figsize=(6, 3.5), dpi=75, facecolor=self.Colors.BACKGROUND1)
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.Colors.BACKGROUND1)

        amounts = df['Amount']
        days = df['Days']

        ax.scatter(amounts, days, alpha=0.6, edgecolors='w', s=50, color=self.Colors.ACTIVE_FOREGROUND)

        ax.set_xlabel("Amount (₹)", color=self.Colors.FOREGROUND, fontsize=9)
        ax.set_ylabel("Days Outstanding", color=self.Colors.FOREGROUND, fontsize=9)

        ax.tick_params(axis='x', colors=self.Colors.FOREGROUND, labelsize=8)
        ax.tick_params(axis='y', colors=self.Colors.FOREGROUND, labelsize=8)
        ax.grid(True, linestyle='--', alpha=0.3, color=self.Colors.FG_SHADE_3)
        for spine in ax.spines.values():
            spine.set_edgecolor(self.Colors.FG_SHADE_3)

        fig.tight_layout(pad=1.0) # Add padding
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    # --- End of plotting functions ---


    def create_activity_section(self):
        """Creates Krar, Inventory, and Crop sections."""
        # Configure grid layout for activity frame
        self.activity_frame.grid_rowconfigure(0, weight=1) # Krar takes top part
        self.activity_frame.grid_rowconfigure(1, weight=1) # Inventory/Crop takes bottom part
        self.activity_frame.grid_columnconfigure(0, weight=1)

        # Krar Status Card with Tabs
        krar_card = create_card_frame(self.activity_frame, text="Krar Status")
        krar_card.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0, 2)) # Grid placement

        notebook = ttk.Notebook(krar_card, style='TNotebook')
        today_frame = tk.Frame(notebook, bg=self.Colors.BACKGROUND2)
        past_frame = tk.Frame(notebook, bg=self.Colors.BACKGROUND2)
        future_frame = tk.Frame(notebook, bg=self.Colors.BACKGROUND2)
        notebook.add(today_frame, text=f"Today ({len(krar.get_customers_with_last_krar_today())})")
        notebook.add(past_frame, text=f"Overdue ({len(krar.get_customers_with_last_krar_past())})")
        notebook.add(future_frame, text=f"Upcoming ({len(krar.get_customers_with_last_krar_future())})")
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0,5)) # Padding inside card

        # Populate Krar tabs
        self.show_krar_table(today_frame, krar.get_customers_with_last_krar_today())
        self.show_krar_table(past_frame, krar.get_customers_with_last_krar_past())
        self.show_krar_table(future_frame, krar.get_customers_with_last_krar_future())

        # --- Inventory & Crop Section (using another Notebook) ---
        inv_crop_card = create_card_frame(self.activity_frame, text="Stock Overview")
        inv_crop_card.grid(row=1, column=0, sticky="nsew", padx=0, pady=(2, 0)) # Grid placement

        inv_notebook = ttk.Notebook(inv_crop_card, style='TNotebook')

        # Low Stock Tab
        low_stock_frame = tk.Frame(inv_notebook, bg=self.Colors.BACKGROUND2)
        inv_notebook.add(low_stock_frame, text=f"Low Stock ({len(self.low_stock_data)})")
        self.show_low_stock_list(low_stock_frame, self.low_stock_data)

        # Crop Summary Tab
        crop_summary_frame = tk.Frame(inv_notebook, bg=self.Colors.BACKGROUND2)
        inv_notebook.add(crop_summary_frame, text=f"Crop Stock ({len(self.crop_summary_data)})")
        self.show_crop_summary_list(crop_summary_frame, self.crop_summary_data)

        inv_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0,5)) # Padding inside card

    # show_krar_table remains mostly the same, adjust style if needed
    def show_krar_table(self, parent_frame, customer_id_list):
        table_data = self.get_krar_customer_data(customer_id_list)
        column_names = ["ID", "Name"] # Simplified Krar list

        if not table_data:
            tk.Label(parent_frame, text="No Krars.", # Use tk for specific bg
                     bg=self.Colors.BACKGROUND2, fg=self.Colors.FOREGROUND).pack(pady=10)
            return

        tree = ttk.Treeview(parent_frame, columns=column_names, show='headings', height=4, style="List.Treeview") # Apply List style

        tree.column('#0', width=0, stretch='no')
        tree.column("ID", width=40, anchor='e') # Align ID right
        tree.column("Name", width=150, anchor='w')

        for col_name in column_names:
            tree.heading(col_name, text=col_name, anchor='w')

        for i, row in enumerate(table_data):
            tag = 'even_krar' if i % 2 == 0 else 'odd_krar'
            tree.insert('', 'end', values=(row[0], row[1]), tags=(tag,)) # Only ID and Name

        tree.tag_configure('odd_krar', background=self.Colors.BACKGROUND2, foreground=self.Colors.FOREGROUND)
        tree.tag_configure('even_krar', background=self.Colors.BACKGROUND3, foreground=self.Colors.FOREGROUND)

        scrollbar = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,2), pady=2)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(2,0), pady=2)
        tree.bind("<Double-1>", self.on_double_click_krar_to_account)

    def get_krar_customer_data(self, customer_id_list):
        # (Keep implementation from the previous step)
        customer_details_list = []
        for cust_id in customer_id_list:
            details = accounts.get_customer_details(cust_id)
            if details:
                customer_details_list.append(details) # (id, name, details)
        return customer_details_list

    def on_double_click_krar_to_account(self, event):
        # (Keep implementation from the previous step)
        tree = event.widget
        region = tree.identify("region", event.x, event.y)
        if region == "cell":
            item_iid = tree.identify_row(event.y)
            if not item_iid: return
            row_data = tree.item(item_iid)['values']
            if not row_data: return

            try:
                customer_id = row_data[0]
                customer_name = row_data[1]
                detail_table_name = f"{customer_id} {customer_name}"

                if hasattr(self.master, 'master') and hasattr(self.master.master, 'reportframe'):
                    reports_page = self.master.master.reportframe
                    reports_page.db_var.set("accounts.db")
                    reports_page.handle_db_selection()

                    if detail_table_name in reports_page.table_dropdown.cget('values'):
                        reports_page.table_var.set(detail_table_name)
                        reports_page.show_table()
                        if hasattr(self.master.master, 'report_frame_label'):
                             self.master.master.report_frame_label.on_click(None)
                        else: print("Could not find report_frame_label.")
                    else:
                        print(f"Target table '{detail_table_name}' not found.")
                        if hasattr(self.master.master, 'report_frame_label'):
                             self.master.master.report_frame_label.on_click(None)
                else: print("Error: Cannot access ReportsPage instance.")
            except Exception as e: print(f"Error processing Krar double click: {e}")


    def show_low_stock_list(self, parent_frame, low_stock_data):
        """Displays a list of low stock items."""
        column_names = ["ID", "Name", "Qty"]
        if not low_stock_data:
            tk.Label(parent_frame, text="No low stock items.",
                     bg=self.Colors.BACKGROUND2, fg=self.Colors.FOREGROUND).pack(pady=10)
            return

        tree = ttk.Treeview(parent_frame, columns=column_names, show='headings', height=4, style="List.Treeview")

        tree.column('#0', width=0, stretch='no')
        tree.column("ID", width=40, anchor='e')
        tree.column("Name", width=150, anchor='w')
        tree.column("Qty", width=50, anchor='e')

        for col_name in column_names:
            tree.heading(col_name, text=col_name, anchor='w')

        for i, (item_id, name, qty) in enumerate(low_stock_data):
             tag = 'even_low' if i % 2 == 0 else 'odd_low'
             # Add visual cue for very low stock
             if qty <= 2: tag = 'critical_low'
             tree.insert('', 'end', values=(item_id, name, qty), tags=(tag,))

        tree.tag_configure('odd_low', background=self.Colors.BACKGROUND2, foreground=self.Colors.FOREGROUND)
        tree.tag_configure('even_low', background=self.Colors.BACKGROUND3, foreground=self.Colors.FOREGROUND)
        tree.tag_configure('critical_low', background=self.Colors.DELETE, foreground="#FFFFFF") # Highlight critical

        scrollbar = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,2), pady=2)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(2,0), pady=2)
        # Optional: Bind double-click to go to inventory report page
        # tree.bind("<Double-1>", self.on_double_click_inventory)

    def show_crop_summary_list(self, parent_frame, crop_data):
         """Displays a summary of crop stock."""
         # crop_data format: [Crop, Unit, Quantity, Avg Cost, Total Value]
         column_names = ["Crop", "Qty", "Value"] # Simplified view

         if not crop_data:
             tk.Label(parent_frame, text="No crop stock data.",
                      bg=self.Colors.BACKGROUND2, fg=self.Colors.FOREGROUND).pack(pady=10)
             return

         tree = ttk.Treeview(parent_frame, columns=column_names, show='headings', height=4, style="List.Treeview")

         tree.column('#0', width=0, stretch='no')
         tree.column("Crop", width=120, anchor='w')
         tree.column("Qty", width=60, anchor='e')
         tree.column("Value", width=80, anchor='e')

         for col_name in column_names:
             tree.heading(col_name, text=col_name, anchor='w')

         for i, row in enumerate(crop_data):
             tag = 'even_crop' if i % 2 == 0 else 'odd_crop'
             try:
                 # Extract relevant data: Name (row[0]), Qty (row[2]), Total Value (row[4])
                 qty_str = f"{row[2]:.2f}" if isinstance(row[2], (float, int)) else str(row[2])
                 val_str = f"₹{row[4]:,.0f}" if isinstance(row[4], (float, int)) else str(row[4])
                 tree.insert('', 'end', values=(row[0], qty_str, val_str), tags=(tag,))
             except (IndexError, TypeError, ValueError) as e:
                  print(f"Error processing crop row: {row}, Error: {e}")
                  tree.insert('', 'end', values=(row[0] if row else 'ERR', 'ERR', 'ERR'), tags=(tag,))


         tree.tag_configure('odd_crop', background=self.Colors.BACKGROUND2, foreground=self.Colors.FOREGROUND)
         tree.tag_configure('even_crop', background=self.Colors.BACKGROUND3, foreground=self.Colors.FOREGROUND)

         scrollbar = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL, command=tree.yview)
         tree.configure(yscrollcommand=scrollbar.set)
         scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,2), pady=2)
         tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(2,0), pady=2)
         # Optional: Bind double-click to go to crop report page
         # tree.bind("<Double-1>", self.on_double_click_crop)


    def redraw_graphs(self):
        """Redraws graphs and lists, useful for theme changes."""
        # KPIs are Labels, update their config directly or rely on ttk style
        for card in self.kpi_frame.winfo_children():
             if isinstance(card, tk.Frame): # Assuming tk Frame for KPIs
                for widget in card.winfo_children():
                    if isinstance(widget, tk.Label):
                         # Update colors based on current theme stored in self.Colors
                         if 'bold' in widget.cget('font'): # Value label
                             # Keep specific value color logic if needed, else use default
                             # For simplicity, just updating bg/fg here. Needs refinement
                             # if title requires specific color.
                             widget.config(bg=self.Colors.BACKGROUND1) # Reapply bg
                             # Keep value_color logic here if it's dynamic
                             # widget.config(fg=value_color)
                         else: # Title label
                             widget.config(bg=self.Colors.BACKGROUND1, fg=self.Colors.FOREGROUND)

        # Check if data exists before trying to redraw graphs/lists
        if not self.accounts_df.empty:
            self._clear_frame(self.financial_frame)
            self._clear_frame(self.activity_frame) # Clear activity too

            # Re-create graph sections
            self.create_financial_graphs()
            # Re-create activity section (Krar, Low Stock, Crop)
            self.create_activity_section()
        else:
            # If no data, ensure loading or error message is shown correctly
            self._clear_frame(self.kpi_frame) # Clear potentially stale KPIs too
            self._clear_frame(self.financial_frame)
            self._clear_frame(self.activity_frame)
            if not self.loading_label.winfo_ismapped(): # Check if loading label is active
                 error_label = ttk.Label(self, text="No Data Loaded",
                                       font="Consolas 20", background=Colors.BACKGROUND,
                                       foreground=Colors.ERROR, anchor='center')
                 error_label.place(relx=0.5, rely=0.5, anchor='center')


# --- Main execution for testing (keep as is or update mock data) ---
if __name__ == "__main__":
    # (Keep the mock data setup and app execution from the previous step)
    # Mock data function for testing without full DB access
    def get_mock_all_list():
        data = {
            'customer_id': [1, 2, 3, 4, 5, 6],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
            'detail': ['Detail A', 'Detail B', 'Detail C', 'Detail D', 'Detail E', 'Detail F'],
            'Amount': [1500.50, -500.75, 25000.00, 800.00, -1200.00, 0.0],
            'Days': [30, 65, 15, 90, 45, 120]
        }
        df = pd.DataFrame(data)
        df['account_score'] = np.random.rand(len(df))
        return df

    # Replace real function with mock for testing
    import mypandasfile
    mypandasfile.get_all_list = get_mock_all_list
    # Mock other DB functions
    inventory.get_total_inventory_value = lambda: 123456.78
    inventory.get_low_stock_items = lambda threshold=10: [(101,'Low Item 1', 3), (102,'Low Item 2', 9)]
    inventory.get_item_quantity = lambda item_id: 5 # Mock quantity
    crop_database.get_stock_summary = lambda: [('WHEAT','KG', 500.5, 25.50, 12762.75), ('CORN','KG', 1200, 18.00, 21600.00)]
    daily_db.get_todays_notes_summary = lambda: 7
    krar.get_customers_with_last_krar_today = lambda: [1, 3]
    krar.get_customers_with_last_krar_past = lambda: [2]
    krar.get_customers_with_last_krar_future = lambda: [4, 5]
    accounts.get_customer_details = lambda cid: (cid, f'Mock Name {cid}', f'Mock Details {cid}')


    app = tk.Tk()
    app.title("Dashboard Enhanced Test")
    app.geometry("1200x750")

    # Mock main app structure
    class MockReportPage: pass
    class MockModifyPage: pass
    class MockApp:
        reportframe = MockReportPage()
        modifyframe = MockModifyPage()
        def set_status(self, msg): print(f"Status: {msg}")
        def report_frame_label(self): pass
        def my_parallel_processes(self): # Mock the refresh trigger target
             print("MockApp: my_parallel_processes called")
             # Simulate data loading and calling back to homepage
             mock_data_new = get_mock_all_list() # Get fresh mock data
             homepage.all_graphs_function(mock_data_new)

    mock_app_instance = MockApp()

    # --- Apply Theme ---
    style = ttk.Style(app)
    style.theme_use('clam')
    # (Keep style configurations from previous step)
    style.configure("Treeview", background=Colors.BACKGROUND, foreground=Colors.FOREGROUND, fieldbackground=Colors.BACKGROUND, rowheight=25, font=('Consolas', 10))
    style.configure("Treeview.Heading", background=Colors.BACKGROUND1, foreground=Colors.FG_SHADE_3, font=('Consolas', 11, 'bold'), relief="flat")
    style.map("Treeview.Heading", relief=[('active','groove'),('pressed','sunken')])
    style.configure("TNotebook", background=Colors.BACKGROUND, borderwidth=0)
    style.configure("TNotebook.Tab", background=Colors.BACKGROUND1, foreground=Colors.FOREGROUND, padding=[5, 2], font=('Consolas', 10))
    style.map("TNotebook.Tab", background=[("selected", Colors.ACTIVE_BACKGROUND)], foreground=[("selected", Colors.FG_SHADE_1)])
    style.configure('Card.TLabelframe', background=Colors.BACKGROUND1, borderwidth=1, relief=tk.GROOVE)
    style.configure('Card.TLabelframe.Label', background=Colors.BACKGROUND1, foreground=Colors.ACTIVE_FOREGROUND, font=("Consolas", 12, "bold"))
    style.configure('List.Treeview', background=Colors.BACKGROUND2, fieldbackground=Colors.BACKGROUND2, foreground=Colors.FOREGROUND, font=('Consolas', 9))
    style.configure('List.Treeview.Heading', background=Colors.BG_SHADE_1, foreground=Colors.ACTIVE_FOREGROUND, font='Consolas 9 bold')
    style.configure("Refresh.TButton", font=("Consolas", 10), padding=5)
    style.map("Refresh.TButton", background=[('active', Colors.LIGHT_BG), ('!active', Colors.BACKGROUND1)], foreground=[('active', Colors.ACTIVE_FOREGROUND)])


    homepage = HomePage(app)
    homepage.pack(fill=tk.BOTH, expand=True)
    homepage.master.master = mock_app_instance # Assign mock app

    # Simulate data loading
    mock_data = get_mock_all_list()
    app.after(500, lambda: homepage.all_graphs_function(mock_data)) # Load after slight delay

    app.mainloop()