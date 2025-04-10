# gui/crop_trading.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

from .mytheme import Colors
from .searchbar import SearchBar
from database import crop_database # Keep this import

class CropTradingPage(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg=Colors.BACKGROUND)

        # --- Main Layout Frames ---
        self.top_frame = tk.Frame(self, bg=Colors.BACKGROUND)
        self.top_frame.pack(fill=tk.X, padx=5, pady=(5,0)) # Frame for Mgmt and Transactions

        self.report_frame = tk.Frame(self, bg=Colors.BACKGROUND, bd=1, relief=tk.GROOVE)
        self.report_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(5,5)) # Frame for Reports

        # Use PanedWindow inside top_frame for adjustable Mgmt/Transaction sections
        self.paned_window = tk.PanedWindow(self.top_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, bg=Colors.BACKGROUND)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # --- Populate PanedWindow ---
        # Frame for Management (Farmers, Crops)
        self.mgmt_frame = tk.Frame(self.paned_window, bg=Colors.BACKGROUND, bd=1, relief=tk.SUNKEN, padx=5)
        self.paned_window.add(self.mgmt_frame, width=250, stretch="never")

        # Frame for Transactions (Purchase, Sale)
        self.trans_frame = tk.Frame(self.paned_window, bg=Colors.BACKGROUND)
        self.paned_window.add(self.trans_frame)

        # --- Populate Frames ---
        self.create_mgmt_widgets() # In mgmt_frame

        # Put Purchase/Sale inside trans_frame
        self.purchase_frame = tk.LabelFrame(self.trans_frame, text="Record Purchase", padx=10, pady=10,
                                            bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND,
                                            font=("Consolas", 14))
        self.purchase_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.sale_frame = tk.LabelFrame(self.trans_frame, text="Record Sale", padx=10, pady=10,
                                        bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND,
                                        font=("Consolas", 14))
        self.sale_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.create_purchase_widgets() # In purchase_frame
        self.create_sale_widgets()     # In sale_frame

        # --- Populate Report Frame ---
        self.create_report_widgets()   # In report_frame

        # --- Initial Data Load ---
        self.refresh_all_lists()
        self.show_crop_report() # Show default report (e.g., stock summary)


    # --- Management Widgets (No Change) ---
    def create_mgmt_widgets(self):
        # ... (Keep implementation from previous correct version) ...
        mgmt_title = tk.Label(self.mgmt_frame, text="Manage", font=("Consolas", 16, "bold"), bg=Colors.BACKGROUND1, fg=Colors.FG_SHADE_3); mgmt_title.pack(fill=tk.X, pady=(0, 10))
        farmer_frame = tk.LabelFrame(self.mgmt_frame, text="Add Farmer", padx=5, pady=5, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND); farmer_frame.pack(fill=tk.X, padx=5, pady=5)
        self.new_farmer_name_var = tk.StringVar(); self.new_farmer_details_var = tk.StringVar()
        tk.Label(farmer_frame, text="Name:", bg=Colors.BACKGROUND, fg=Colors.FOREGROUND).grid(row=0, column=0, sticky='w', pady=2)
        tk.Entry(farmer_frame, textvariable=self.new_farmer_name_var, font="Consolas 12", width=20, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1).grid(row=0, column=1, sticky='ew', pady=2, padx=5)
        tk.Label(farmer_frame, text="Details:", bg=Colors.BACKGROUND, fg=Colors.FOREGROUND).grid(row=1, column=0, sticky='w', pady=2)
        tk.Entry(farmer_frame, textvariable=self.new_farmer_details_var, font="Consolas 12", width=20, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1).grid(row=1, column=1, sticky='ew', pady=2, padx=5)
        tk.Button(farmer_frame, text="Add", font="Consolas 10", command=self.add_new_farmer_action, bg=Colors.BACKGROUND1, fg=Colors.SUCCESS).grid(row=2, column=0, columnspan=2, pady=5)
        farmer_frame.grid_columnconfigure(1, weight=1)
        crop_frame = tk.LabelFrame(self.mgmt_frame, text="Add Crop", padx=5, pady=5, bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND); crop_frame.pack(fill=tk.X, padx=5, pady=5)
        self.new_crop_name_var = tk.StringVar(); self.new_crop_unit_var = tk.StringVar(value="KG")
        tk.Label(crop_frame, text="Name:", bg=Colors.BACKGROUND, fg=Colors.FOREGROUND).grid(row=0, column=0, sticky='w', pady=2)
        tk.Entry(crop_frame, textvariable=self.new_crop_name_var, font="Consolas 12", width=20, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1).grid(row=0, column=1, sticky='ew', pady=2, padx=5)
        tk.Label(crop_frame, text="Unit:", bg=Colors.BACKGROUND, fg=Colors.FOREGROUND).grid(row=1, column=0, sticky='w', pady=2)
        tk.Entry(crop_frame, textvariable=self.new_crop_unit_var, font="Consolas 12", width=20, bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1).grid(row=1, column=1, sticky='ew', pady=2, padx=5)
        tk.Button(crop_frame, text="Add", font="Consolas 10", command=self.add_new_crop_action, bg=Colors.BACKGROUND1, fg=Colors.SUCCESS).grid(row=2, column=0, columnspan=2, pady=5)
        crop_frame.grid_columnconfigure(1, weight=1)

    # --- Actions for Management Widgets (No Change) ---
    def add_new_farmer_action(self):
        # ... (Keep implementation from previous correct version) ...
        name = self.new_farmer_name_var.get().strip().upper(); details = self.new_farmer_details_var.get().strip().upper()
        if not name: messagebox.showwarning("Input Missing", "Farmer Name cannot be empty."); return
        farmer_id = crop_database.add_farmer(name, details)
        if farmer_id: self._set_status(f"Farmer '{name}' added (ID: {farmer_id})."); self.new_farmer_name_var.set(""); self.new_farmer_details_var.set(""); self.refresh_purchase_lists()
        elif farmer_id is None: self._set_status(f"[Warning/Error] Could not add farmer '{name}'. Check console.")

    def add_new_crop_action(self):
        # ... (Keep implementation from previous correct version) ...
        name = self.new_crop_name_var.get().strip().upper(); unit = self.new_crop_unit_var.get().strip().upper() or "KG"
        if not name: messagebox.showwarning("Input Missing", "Crop Name cannot be empty."); return
        crop_id = crop_database.add_crop(name, unit)
        if crop_id: self._set_status(f"Crop '{name}' added (ID: {crop_id})."); self.new_crop_name_var.set(""); self.new_crop_unit_var.set("KG"); self.refresh_all_lists()
        elif crop_id is None: self._set_status(f"[Warning/Error] Could not add crop '{name}'. Check console.")


    # --- Helper to create input rows (No Change) ---
    def _create_input_row(self, parent, label_text, entry_var=None, widget_type='entry', dropdown_options=None, use_searchbar=False):
        # ... (Keep implementation from previous correct version) ...
        frame = tk.Frame(parent, bg=Colors.BACKGROUND); frame.pack(fill=tk.X, pady=5)
        label = tk.Label(frame, text=label_text, font="Consolas 12", width=15, anchor='w', bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND); label.pack(side=tk.LEFT, padx=(0, 10))
        widget = None
        if use_searchbar and dropdown_options is not None:
             widget = SearchBar(frame, data=dropdown_options); widget.set_data(dropdown_options); widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
        elif widget_type == 'entry':
            widget = tk.Entry(frame, textvariable=entry_var, font="Consolas 14", bg=Colors.BACKGROUND3, fg=Colors.FG_SHADE_1, relief='solid', bd=1); widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
        elif widget_type == 'combobox' and dropdown_options is not None:
             widget = ttk.Combobox(frame, textvariable=entry_var, values=dropdown_options, font="Consolas 14", state="readonly"); widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
             if dropdown_options: widget.current(0)
        return widget

    # --- Purchase Widgets (No Change) ---
    def create_purchase_widgets(self):
        # ... (Keep implementation from previous correct version) ...
        self.p_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d')); self.p_net_qty_var = tk.StringVar(); self.p_k_qty_var = tk.StringVar(value="0"); self.p_rate_var = tk.StringVar(); self.p_actual_qty_var = tk.StringVar(value="Calculated..."); self.p_total_amt_var = tk.StringVar(value="Calculated...")
        self._create_input_row(self.purchase_frame, "Date:", self.p_date_var)
        self.p_farmer_searchbar = self._create_input_row(self.purchase_frame, "Farmer:", dropdown_options=[], use_searchbar=True)
        self.p_crop_searchbar = self._create_input_row(self.purchase_frame, "Crop:", dropdown_options=[], use_searchbar=True)
        net_entry = self._create_input_row(self.purchase_frame, "Net Qty:", self.p_net_qty_var); k_entry = self._create_input_row(self.purchase_frame, "K-Qty:", self.p_k_qty_var); rate_entry = self._create_input_row(self.purchase_frame, "Rate:", self.p_rate_var)
        net_entry.bind("<KeyRelease>", self.calculate_purchase_totals); k_entry.bind("<KeyRelease>", self.calculate_purchase_totals); rate_entry.bind("<KeyRelease>", self.calculate_purchase_totals)
        calc_frame = tk.Frame(self.purchase_frame, bg=Colors.BACKGROUND); calc_frame.pack(fill=tk.X, pady=5); tk.Label(calc_frame, text="Actual Qty:", font="Consolas 12", width=15, anchor='w', bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND).pack(side=tk.LEFT, padx=(0, 10)); tk.Label(calc_frame, textvariable=self.p_actual_qty_var, font="Consolas 14 bold", anchor='w', bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_3).pack(side=tk.LEFT, fill=tk.X, expand=True)
        calc_frame2 = tk.Frame(self.purchase_frame, bg=Colors.BACKGROUND); calc_frame2.pack(fill=tk.X, pady=5); tk.Label(calc_frame2, text="Total Amount:", font="Consolas 12", width=15, anchor='w', bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND).pack(side=tk.LEFT, padx=(0, 10)); tk.Label(calc_frame2, textvariable=self.p_total_amt_var, font="Consolas 14 bold", anchor='w', bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_3).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(self.purchase_frame, text="Record Purchase", font="Consolas 14", command=self.record_purchase_action, bg=Colors.BACKGROUND1, fg=Colors.SUCCESS, relief='raised', bd=2).pack(pady=15, fill=tk.X)
        tk.Button(self.purchase_frame, text="Refresh Lists", font="Consolas 10", command=self.refresh_all_lists, bg=Colors.BACKGROUND2, fg=Colors.ACTIVE_FOREGROUND, relief='raised', bd=1).pack(pady=5, side=tk.BOTTOM)

    # --- Sale Widgets (No Change) ---
    def create_sale_widgets(self):
        # ... (Keep implementation from previous correct version) ...
        self.s_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d')); self.s_qty_var = tk.StringVar(); self.s_rate_var = tk.StringVar(); self.s_buyer_var = tk.StringVar(); self.s_total_amt_var = tk.StringVar(value="Calculated...")
        self._create_input_row(self.sale_frame, "Date:", self.s_date_var)
        self.s_crop_searchbar = self._create_input_row(self.sale_frame, "Crop:", dropdown_options=[], use_searchbar=True)
        qty_entry = self._create_input_row(self.sale_frame, "Sale Qty:", self.s_qty_var); rate_entry = self._create_input_row(self.sale_frame, "Rate:", self.s_rate_var); self._create_input_row(self.sale_frame, "Buyer Details:", self.s_buyer_var)
        qty_entry.bind("<KeyRelease>", self.calculate_sale_total); rate_entry.bind("<KeyRelease>", self.calculate_sale_total)
        calc_frame_s = tk.Frame(self.sale_frame, bg=Colors.BACKGROUND); calc_frame_s.pack(fill=tk.X, pady=5); tk.Label(calc_frame_s, text="Total Amount:", font="Consolas 12", width=15, anchor='w', bg=Colors.BACKGROUND, fg=Colors.ACTIVE_FOREGROUND).pack(side=tk.LEFT, padx=(0, 10)); tk.Label(calc_frame_s, textvariable=self.s_total_amt_var, font="Consolas 14 bold", anchor='w', bg=Colors.BACKGROUND, fg=Colors.FG_SHADE_3).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(self.sale_frame, text="Record Sale", font="Consolas 14", command=self.record_sale_action, bg=Colors.BACKGROUND1, fg=Colors.SUCCESS, relief='raised', bd=2).pack(pady=15, fill=tk.X, side=tk.BOTTOM)
        tk.Button(self.sale_frame, text="Refresh Lists", font="Consolas 10", command=self.refresh_all_lists, bg=Colors.BACKGROUND2, fg=Colors.ACTIVE_FOREGROUND, relief='raised', bd=1).pack(pady=5, side=tk.BOTTOM)

    # --- Formatting for SearchBar (No Change) ---
    def _format_for_searchbar(self, data_list, id_index, name_index):
        # ... (Keep implementation from previous correct version) ...
        if not data_list: return []; return [f"{item[id_index]} {item[name_index]}" for item in data_list]

    # --- Refresh Dropdown/SearchBar Data (No Change) ---
    def refresh_purchase_lists(self):
        # ... (Keep implementation from previous correct version) ...
        farmer_list = self._format_for_searchbar(crop_database.get_farmers(), 0, 1); crop_list = self._format_for_searchbar(crop_database.get_crops(), 0, 1)
        if self.p_farmer_searchbar: self.p_farmer_searchbar.set_data(farmer_list)
        if self.p_crop_searchbar: self.p_crop_searchbar.set_data(crop_list)
        # self._set_status("Purchase lists refreshed.") # Can be combined in refresh_all_lists

    def refresh_sale_lists(self):
        # ... (Keep implementation from previous correct version) ...
        crop_list = self._format_for_searchbar(crop_database.get_crops(), 0, 1)
        if self.s_crop_searchbar: self.s_crop_searchbar.set_data(crop_list)
        # self._set_status("Sale crop list refreshed.") # Can be combined in refresh_all_lists

    def refresh_all_lists(self):
        # ... (Keep implementation from previous correct version) ...
        self.refresh_purchase_lists(); self.refresh_sale_lists()
        self._set_status("Farmer and Crop lists refreshed.")

    # --- Calculation Logic (No Change) ---
    def calculate_purchase_totals(self, event=None):
        # ... (Keep implementation from previous correct version) ...
         try:
             net_q=float(self.p_net_qty_var.get() or 0);k_q=float(self.p_k_qty_var.get() or 0);rate=float(self.p_rate_var.get() or 0)
             if k_q > net_q: raise ValueError("K>Net")
             actual_q=net_q-k_q; total_amt=actual_q*rate
             self.p_actual_qty_var.set(f"{actual_q:.2f}"); self.p_total_amt_var.set(f"{total_amt:.2f}")
         except ValueError as e: self.p_actual_qty_var.set(f"Error: {e}"); self.p_total_amt_var.set("Invalid Input")
         except Exception as e: print(f"Calc err: {e}"); self.p_actual_qty_var.set("Error"); self.p_total_amt_var.set("Error")

    def calculate_sale_total(self, event=None):
        # ... (Keep implementation from previous correct version) ...
         try: qty=float(self.s_qty_var.get() or 0); rate=float(self.s_rate_var.get() or 0); total_amt=qty*rate; self.s_total_amt_var.set(f"{total_amt:.2f}")
         except ValueError: self.s_total_amt_var.set("Invalid Input")
         except Exception as e: print(f"Sale calc err: {e}"); self.s_total_amt_var.set("Error")

    # --- Helper: Get ID or Add New (No Change) ---
    def _get_or_add_farmer(self, farmer_input_str):
        # ... (Keep implementation from previous correct version) ...
        farmer_input_str=farmer_input_str.strip().upper();
        if not farmer_input_str: return None
        farmers=crop_database.get_farmers(); farmer_map={f"{f[0]} {f[1]}": f[0] for f in farmers}; exact_match_map={f[1]: f[0] for f in farmers}
        if farmer_input_str in farmer_map: return farmer_map[farmer_input_str]
        if farmer_input_str in exact_match_map: return exact_match_map[farmer_input_str]
        msg=f"Farmer '{farmer_input_str}' not found.\nAdd this farmer?";
        if messagebox.askyesno("Add Farmer?", msg):
            details=simpledialog.askstring("Farmer Details", f"Details for '{farmer_input_str}' (optional):", parent=self) or ""
            farmer_id=crop_database.add_farmer(farmer_input_str, details)
            if farmer_id: self._set_status(f"Added new farmer '{farmer_input_str}' (ID: {farmer_id})"); self.refresh_purchase_lists(); self.p_farmer_searchbar.set_text(f"{farmer_id} {farmer_input_str}"); return farmer_id
            else: messagebox.showerror("Error", f"Failed to add farmer '{farmer_input_str}'."); return None
        else: return None

    def _get_or_add_crop(self, crop_input_str, target_searchbar):
        # ... (Keep implementation from previous correct version) ...
        crop_input_str=crop_input_str.strip().upper();
        if not crop_input_str: return None
        crops=crop_database.get_crops(); crop_map={f"{c[0]} {c[1]}": c[0] for c in crops}; exact_match_map={c[1]: c[0] for c in crops}
        if crop_input_str in crop_map: return crop_map[crop_input_str]
        if crop_input_str in exact_match_map: return exact_match_map[crop_input_str]
        msg=f"Crop '{crop_input_str}' not found.\nAdd this crop?";
        if messagebox.askyesno("Add Crop?", msg):
            unit=simpledialog.askstring("Crop Unit", f"Unit for '{crop_input_str}' (default KG):", parent=self) or "KG"
            crop_id=crop_database.add_crop(crop_input_str, unit.upper())
            if crop_id: self._set_status(f"Added new crop '{crop_input_str}' (ID: {crop_id})"); self.refresh_all_lists(); target_searchbar.set_text(f"{crop_id} {crop_input_str}"); return crop_id
            else: messagebox.showerror("Error", f"Failed to add crop '{crop_input_str}'."); return None
        else: return None

    # --- Action Methods (No Change) ---
    def record_purchase_action(self):
        # ... (Keep implementation from previous correct version) ...
        date_str=self.p_date_var.get(); farmer_input=self.p_farmer_searchbar.get_text(); crop_input=self.p_crop_searchbar.get_text(); net_qty_str=self.p_net_qty_var.get(); k_qty_str=self.p_k_qty_var.get(); rate_str=self.p_rate_var.get()
        try: datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError: messagebox.showerror("Input Error", f"Invalid Date format: '{date_str}'. Use YYYY-MM-DD."); self._set_status("[Error] Invalid Date format."); return
        farmer_id=self._get_or_add_farmer(farmer_input)
        if farmer_id is None: self._set_status("[Cancelled/Error] Farmer ID process stopped."); self.p_farmer_searchbar.search_bar.focus(); return
        crop_id=self._get_or_add_crop(crop_input, self.p_crop_searchbar)
        if crop_id is None: self._set_status("[Cancelled/Error] Crop ID process stopped."); self.p_crop_searchbar.search_bar.focus(); return
        purchase_id, message = crop_database.record_purchase(farmer_id, crop_id, date_str, net_qty_str, k_qty_str, rate_str)
        if purchase_id: self._set_status(f"Purchase recorded (ID: {purchase_id}). {message}")
        else: messagebox.showerror("Database Error", f"Failed purchase record.\nReason: {message}"); self._set_status(f"[Error] Purchase failed: {message}")

    def record_sale_action(self):
        # ... (Keep implementation from previous correct version) ...
        date_str=self.s_date_var.get(); crop_input=self.s_crop_searchbar.get_text(); qty_str=self.s_qty_var.get(); rate_str=self.s_rate_var.get(); buyer_details=self.s_buyer_var.get()
        try: datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError: messagebox.showerror("Input Error", f"Invalid Date format: '{date_str}'. Use YYYY-MM-DD."); self._set_status("[Error] Invalid Date format."); return
        crop_id=self._get_or_add_crop(crop_input, self.s_crop_searchbar)
        if crop_id is None: self._set_status("[Cancelled/Error] Crop ID process stopped."); self.s_crop_searchbar.search_bar.focus(); return
        sale_id, message = crop_database.record_sale(crop_id, date_str, qty_str, rate_str, buyer_details)
        if sale_id: self._set_status(f"Sale recorded (ID: {sale_id}). {message}")
        else: messagebox.showerror("Database Error", f"Failed sale record.\nReason: {message}"); self._set_status(f"[Error] Sale failed: {message}")

    # --- Status Update Helper (No Change) ---
    def _set_status(self, message):
        # ... (Keep implementation from previous correct version) ...
        try:
            if hasattr(self.master, 'master') and hasattr(self.master.master, 'set_status'): self.master.master.set_status(f"|Crop Trading| {message}")
            else: print(f"Crop Trading Status: {message}")
        except Exception as e: print(f"Status Update Error: {e}")


    # --- NEW: Report Widgets ---
    def create_report_widgets(self):
        """Creates the controls and display area for crop reports."""
        # Frame for Controls
        report_controls_frame = tk.Frame(self.report_frame, bg=Colors.BACKGROUND)
        report_controls_frame.pack(fill=tk.X, pady=(5, 2))

        tk.Label(report_controls_frame, text="Select Report:", bg=Colors.BACKGROUND,
                 fg=Colors.ACTIVE_FOREGROUND, font="Consolas 12").pack(side=tk.LEFT, padx=5)

        report_types = ["Stock Summary", "Purchase History", "Sales History"]
        self.report_type_var = tk.StringVar(value=report_types[0]) # Default to Stock Summary
        report_dropdown = ttk.Combobox(report_controls_frame, textvariable=self.report_type_var,
                                        values=report_types, width=20, font="Consolas 12", state="readonly")
        report_dropdown.pack(side=tk.LEFT, padx=5)
        report_dropdown.bind("<<ComboboxSelected>>", self.show_crop_report)

        # Optional: Add date filters or other filters here later

        show_button = tk.Button(report_controls_frame, text="Show Report", font="Consolas 11",
                                command=self.show_crop_report, bg=Colors.BACKGROUND1, fg=Colors.ACTIVE_FOREGROUND)
        show_button.pack(side=tk.LEFT, padx=10)

        # Frame for Treeview display
        self.report_display_frame = tk.Frame(self.report_frame, bg=Colors.BACKGROUND2) # Slightly different bg?
        self.report_display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Placeholder label for reports initially
        self.report_placeholder_label = tk.Label(self.report_display_frame,
                                                  text="Select a report to view.",
                                                  font="Consolas 14", bg=Colors.BACKGROUND2, fg=Colors.FOREGROUND)
        self.report_placeholder_label.pack(pady=20)


    # --- NEW: Clear Report Display ---
    def clear_report_frame(self):
        """Removes previous report Treeview and scrollbars."""
        for widget in self.report_display_frame.winfo_children():
            widget.destroy()


    # --- NEW: Show Crop Report ---
    def show_crop_report(self, event=None):
        """Fetches and displays the selected crop report."""
        report_type = self.report_type_var.get()
        self.clear_report_frame() # Clear previous report

        column_names = []
        column_widths = []
        report_data = []

        try:
            if report_type == "Stock Summary":
                column_names = ["Crop", "Unit", "Quantity", "Avg Cost", "Total Value"]
                column_widths = [150, 60, 100, 100, 120]
                report_data = crop_database.get_stock_summary()
                self._set_status("Displayed Stock Summary.")
            elif report_type == "Purchase History":
                column_names = ["ID", "Date", "Farmer", "Crop", "Net Q", "K Q", "Actual Q", "Rate", "Amount"]
                column_widths = [40, 90, 150, 120, 70, 70, 80, 80, 100]
                report_data = crop_database.get_purchase_history() # Add filters later
                self._set_status("Displayed Purchase History.")
            elif report_type == "Sales History":
                column_names = ["ID", "Date", "Crop", "Sale Q", "Rate", "Amount", "Buyer"]
                column_widths = [40, 90, 120, 80, 80, 100, 150]
                report_data = crop_database.get_sales_history() # Add filters later
                self._set_status("Displayed Sales History.")
            else:
                self._set_status(f"Unknown report type: {report_type}")
                return # Should not happen with Combobox

        except Exception as e:
             self._set_status(f"[Error] Failed to fetch report data: {e}")
             print(f"Error fetching report '{report_type}': {e}")
             tk.Label(self.report_display_frame, text=f"Error loading report:\n{e}",
                      font="Consolas 12", fg="red", bg=Colors.BACKGROUND2).pack(pady=20)
             return


        # Display data if found
        if not report_data:
            tk.Label(self.report_display_frame, text=f"No data found for {report_type}.",
                     font="Consolas 14", bg=Colors.BACKGROUND2, fg=Colors.FOREGROUND).pack(pady=20)
            return

        # Create Treeview
        report_tree = ttk.Treeview(self.report_display_frame, columns=column_names, show='headings')

        # Configure Columns & Headings
        report_tree.column('#0', width=0, stretch='no') # Hide default column
        for i, col_name in enumerate(column_names):
            width = column_widths[i] if i < len(column_widths) else 100 # Default width
            report_tree.column(col_name, width=width, anchor='w', stretch=True)
            report_tree.heading(col_name, text=col_name, anchor='w')
            # Add sorting later if desired, using a similar function to reports.py

        # Insert Data
        for i, row in enumerate(report_data):
            tag = 'even_rep' if i % 2 == 0 else 'odd_rep'
            try:
                # Ensure row length matches columns
                values_to_insert = list(row); padding = len(column_names) - len(values_to_insert)
                if padding > 0: values_to_insert.extend([''] * padding)
                elif padding < 0: values_to_insert = values_to_insert[:len(column_names)]
                report_tree.insert('', 'end', values=values_to_insert, tags=(tag,))
            except Exception as e_insert:
                print(f"Error inserting report row {i+1}: {row}\n{e_insert}")


        # Configure Row Tags (use different names than main reports)
        report_tree.tag_configure('odd_rep', background=Colors.BACKGROUND, foreground=Colors.FOREGROUND)
        report_tree.tag_configure('even_rep', background=Colors.BACKGROUND1, foreground=Colors.FOREGROUND)

        # Scrollbars
        rep_yscroll = ttk.Scrollbar(self.report_display_frame, orient=tk.VERTICAL, command=report_tree.yview)
        rep_xscroll = ttk.Scrollbar(self.report_display_frame, orient=tk.HORIZONTAL, command=report_tree.xview)
        report_tree.configure(yscrollcommand=rep_yscroll.set, xscrollcommand=rep_xscroll.set)

        # Pack Treeview and Scrollbars
        rep_yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        rep_xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        report_tree.pack(fill=tk.BOTH, expand=True)


# --- Main execution for testing ---
if __name__ == "__main__":
    # ... (Test code remains the same) ...
    app = tk.Tk()
    app.title("Crop Trading Page Test w/ Reports")
    app.geometry("1100x750") # Wider/Taller for reports
    class MockMaster:
         def set_status(self, msg): print(f"Status Bar: {msg}")
    class MockApp: master = MockMaster()

    crop_database.initialize_database()

    page = CropTradingPage(app)
    page.master.master = MockApp()
    page.pack(fill=tk.BOTH, expand=True)
    app.mainloop()