# database/crop_database.py
import sqlite3
import os
from datetime import datetime

DB_FOLDER = "C://JBB//data"
DB_NAME = os.path.join(DB_FOLDER, "crop_trading.db")

# Ensure the data folder exists
os.makedirs(DB_FOLDER, exist_ok=True)

def get_db_connection():
    """Establishes and returns a database connection."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row # Return rows as dictionary-like objects
        # Enable foreign key support
        conn.execute("PRAGMA foreign_keys = ON")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def initialize_database():
    """Creates the necessary tables if they don't exist."""
    conn = get_db_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        # Farmers Table (Similar to customers)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS farmers (
                farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                details TEXT
            )
        ''')

        # Crops Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crops (
                crop_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                unit TEXT DEFAULT 'KG'
            )
        ''')

        # Purchases Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchases (
                purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id INTEGER NOT NULL,
                crop_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                net_quantity REAL NOT NULL,
                k_quantity REAL DEFAULT 0,
                actual_quantity REAL NOT NULL, -- Calculated: net_quantity - k_quantity
                purchase_rate REAL NOT NULL,
                total_amount REAL NOT NULL,    -- Calculated: actual_quantity * purchase_rate
                FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id) ON DELETE RESTRICT,
                FOREIGN KEY (crop_id) REFERENCES crops(crop_id) ON DELETE RESTRICT
            )
        ''')

        # Sales Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                crop_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                sale_quantity REAL NOT NULL,
                sale_rate REAL NOT NULL,
                total_amount REAL NOT NULL, -- Calculated: sale_quantity * sale_rate
                buyer_details TEXT,        -- Optional: Name or 'Cash Sale' etc.
                FOREIGN KEY (crop_id) REFERENCES crops(crop_id) ON DELETE RESTRICT
            )
        ''')

        # Stock Table (To maintain current levels and average cost)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock (
                crop_id INTEGER PRIMARY KEY,
                current_quantity REAL DEFAULT 0,
                average_cost REAL DEFAULT 0, -- Weighted average cost
                FOREIGN KEY (crop_id) REFERENCES crops(crop_id) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        print("Crop trading database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Error initializing crop trading database: {e}")
    finally:
        if conn:
            conn.close()

# --- Farmer Functions ---
def add_farmer(name, details=""):
    sql = 'INSERT INTO farmers (name, details) VALUES (?, ?)'
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (name.upper(), details.upper()))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
         print(f"Farmer '{name}' already exists.")
         return None # Indicate failure due to unique constraint
    except sqlite3.Error as e:
        print(f"Error adding farmer: {e}")
        return None
    finally:
        if conn: conn.close()

def get_farmers():
    sql = 'SELECT farmer_id, name, details FROM farmers ORDER BY name'
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        farmers = cursor.fetchall()
        # Convert Row objects to simple lists or tuples if needed by GUI
        return [list(f) for f in farmers]
    except sqlite3.Error as e:
        print(f"Error getting farmers: {e}")
        return []
    finally:
        if conn: conn.close()

# --- Crop Functions ---
def add_crop(name, unit="KG"):
    sql = 'INSERT INTO crops (name, unit) VALUES (?, ?)'
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (name.upper(), unit.upper()))
        conn.commit()
        crop_id = cursor.lastrowid
        # Initialize stock entry for the new crop
        cursor.execute('INSERT OR IGNORE INTO stock (crop_id) VALUES (?)', (crop_id,))
        conn.commit()
        return crop_id
    except sqlite3.IntegrityError:
         print(f"Crop '{name}' already exists.")
         return None
    except sqlite3.Error as e:
        print(f"Error adding crop: {e}")
        return None
    finally:
        if conn: conn.close()

def get_crops():
    sql = 'SELECT crop_id, name, unit FROM crops ORDER BY name'
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        crops = cursor.fetchall()
        return [list(c) for c in crops]
    except sqlite3.Error as e:
        print(f"Error getting crops: {e}")
        return []
    finally:
        if conn: conn.close()

# --- Stock Update (Helper Function) ---
def _update_stock_on_purchase(cursor, crop_id, purchased_actual_quantity, purchase_rate):
    """Updates stock quantity and average cost upon purchase."""
    cursor.execute('SELECT current_quantity, average_cost FROM stock WHERE crop_id = ?', (crop_id,))
    stock_data = cursor.fetchone()

    if stock_data:
        old_quantity = stock_data['current_quantity']
        old_avg_cost = stock_data['average_cost']

        new_quantity = old_quantity + purchased_actual_quantity

        if new_quantity <= 0 or purchased_actual_quantity <= 0 : # Avoid division by zero or illogical updates
             new_avg_cost = old_avg_cost # Keep old cost if purchase qty is zero
        elif old_quantity <= 0 :
             new_avg_cost = purchase_rate # If starting from zero stock, cost is just the purchase rate
        else:
             # Calculate weighted average cost
             new_avg_cost = ((old_avg_cost * old_quantity) + (purchase_rate * purchased_actual_quantity)) / new_quantity

        cursor.execute('''
            UPDATE stock
            SET current_quantity = ?, average_cost = ?
            WHERE crop_id = ?
        ''', (new_quantity, new_avg_cost, crop_id))
    else:
        # Should not happen if add_crop initializes stock, but handle defensively
        new_quantity = purchased_actual_quantity
        new_avg_cost = purchase_rate
        cursor.execute('''
             INSERT INTO stock (crop_id, current_quantity, average_cost)
             VALUES (?, ?, ?)
        ''', (crop_id, new_quantity, new_avg_cost))


def _update_stock_on_sale(cursor, crop_id, sold_quantity):
    """Updates stock quantity upon sale. Does NOT change average cost."""
    cursor.execute('SELECT current_quantity FROM stock WHERE crop_id = ?', (crop_id,))
    stock_data = cursor.fetchone()

    if stock_data:
        old_quantity = stock_data['current_quantity']
        new_quantity = old_quantity - sold_quantity
        # Optional: Add check here to prevent selling more than available
        # if new_quantity < 0:
        #    raise ValueError("Insufficient stock for this sale.")

        cursor.execute('''
            UPDATE stock SET current_quantity = ? WHERE crop_id = ?
        ''', (new_quantity, crop_id))
    else:
         # This indicates an issue - trying to sell a crop not in stock table
         print(f"Warning: Trying to sell crop_id {crop_id} which has no stock record.")


# --- Purchase Functions ---
def record_purchase(farmer_id, crop_id, date_str, net_quantity, k_quantity, purchase_rate):
    if not all([farmer_id, crop_id, date_str, net_quantity is not None, k_quantity is not None, purchase_rate is not None]):
         print("Error: Missing data for purchase.")
         return None, "Missing data"

    try:
        net_q = float(net_quantity)
        k_q = float(k_quantity)
        rate = float(purchase_rate)

        if net_q < 0 or k_q < 0 or rate < 0:
             raise ValueError("Quantities and rate cannot be negative.")
        if k_q > net_q:
             raise ValueError("K-Quantity cannot be greater than Net Quantity.")

        actual_quantity = net_q - k_q
        total_amount = actual_quantity * rate

    except ValueError as e:
        print(f"Invalid input for purchase: {e}")
        return None, str(e)

    sql = '''
        INSERT INTO purchases
        (farmer_id, crop_id, date, net_quantity, k_quantity, actual_quantity, purchase_rate, total_amount)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''
    conn = get_db_connection()
    if not conn: return None, "Database connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (farmer_id, crop_id, date_str, net_q, k_q, actual_quantity, rate, total_amount))
        purchase_id = cursor.lastrowid
        # Update stock
        _update_stock_on_purchase(cursor, crop_id, actual_quantity, rate)
        conn.commit()
        return purchase_id, "Success"
    except sqlite3.Error as e:
        conn.rollback() # Rollback on error
        print(f"Error recording purchase: {e}")
        return None, str(e)
    finally:
        if conn: conn.close()


# --- Sale Functions ---
def record_sale(crop_id, date_str, sale_quantity, sale_rate, buyer_details=""):
    if not all([crop_id, date_str, sale_quantity is not None, sale_rate is not None]):
         print("Error: Missing data for sale.")
         return None, "Missing data"

    try:
        sale_q = float(sale_quantity)
        rate = float(sale_rate)

        if sale_q <= 0 or rate <= 0:
            raise ValueError("Sale quantity and rate must be positive.")

        total_amount = sale_q * rate

    except ValueError as e:
        print(f"Invalid input for sale: {e}")
        return None, str(e)

    sql = '''
        INSERT INTO sales
        (crop_id, date, sale_quantity, sale_rate, total_amount, buyer_details)
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    conn = get_db_connection()
    if not conn: return None, "Database connection failed"
    cursor = conn.cursor()
    try:
        # Optional: Check stock before recording sale
        # cursor.execute('SELECT current_quantity FROM stock WHERE crop_id = ?', (crop_id,))
        # current_stock = cursor.fetchone()
        # if not current_stock or current_stock['current_quantity'] < sale_q:
        #     return None, f"Insufficient stock for crop ID {crop_id}. Available: {current_stock['current_quantity'] if current_stock else 0}"

        cursor.execute(sql, (crop_id, date_str, sale_q, rate, total_amount, buyer_details.upper()))
        sale_id = cursor.lastrowid
        # Update stock
        _update_stock_on_sale(cursor, crop_id, sale_q)
        conn.commit()
        return sale_id, "Success"
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error recording sale: {e}")
        return None, str(e)
    finally:
        if conn: conn.close()

# --- Reporting Functions ---
def get_stock_summary():
    """Gets current stock levels and average costs."""
    sql = '''
        SELECT c.name, c.unit, s.current_quantity, s.average_cost,
               (s.current_quantity * s.average_cost) AS total_value
        FROM stock s
        JOIN crops c ON s.crop_id = c.crop_id
        ORDER BY c.name
    '''
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        summary = cursor.fetchall()
        return [list(s) for s in summary] # Return as list of lists
    except sqlite3.Error as e:
        print(f"Error getting stock summary: {e}")
        return []
    finally:
        if conn: conn.close()

def get_purchase_history(farmer_id=None, crop_id=None, start_date=None, end_date=None):
    """Gets purchase history, optionally filtered."""
    base_sql = '''
        SELECT p.purchase_id, p.date, f.name as farmer_name, c.name as crop_name,
               p.net_quantity, p.k_quantity, p.actual_quantity, p.purchase_rate, p.total_amount
        FROM purchases p
        JOIN farmers f ON p.farmer_id = f.farmer_id
        JOIN crops c ON p.crop_id = c.crop_id
    '''
    filters = []
    params = []

    if farmer_id:
        filters.append("p.farmer_id = ?")
        params.append(farmer_id)
    if crop_id:
        filters.append("p.crop_id = ?")
        params.append(crop_id)
    if start_date:
        filters.append("p.date >= ?")
        params.append(start_date)
    if end_date:
        filters.append("p.date <= ?")
        params.append(end_date)

    if filters:
        base_sql += " WHERE " + " AND ".join(filters)

    base_sql += " ORDER BY p.date DESC, p.purchase_id DESC"

    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        cursor.execute(base_sql, params)
        history = cursor.fetchall()
        return [list(h) for h in history]
    except sqlite3.Error as e:
        print(f"Error getting purchase history: {e}")
        return []
    finally:
        if conn: conn.close()


def get_sales_history(crop_id=None, start_date=None, end_date=None):
    """Gets sales history, optionally filtered."""
    base_sql = '''
        SELECT s.sale_id, s.date, c.name as crop_name, s.sale_quantity, s.sale_rate,
               s.total_amount, s.buyer_details
        FROM sales s
        JOIN crops c ON s.crop_id = c.crop_id
    '''
    filters = []
    params = []

    if crop_id:
        filters.append("s.crop_id = ?")
        params.append(crop_id)
    if start_date:
        filters.append("s.date >= ?")
        params.append(start_date)
    if end_date:
        filters.append("s.date <= ?")
        params.append(end_date)

    if filters:
        base_sql += " WHERE " + " AND ".join(filters)

    base_sql += " ORDER BY s.date DESC, s.sale_id DESC"

    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        cursor.execute(base_sql, params)
        history = cursor.fetchall()
        return [list(h) for h in history]
    except sqlite3.Error as e:
        print(f"Error getting sales history: {e}")
        return []
    finally:
        if conn: conn.close()

# --- General DB Utility ---
def get_table_data(table_name):
    """Generic function to get all data from a table."""
    conn = get_db_connection()
    if not conn: return [], []
    cursor = conn.cursor()
    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()] # Get column names
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        return columns, [list(row) for row in data]
    except sqlite3.Error as e:
        print(f"Error getting data for table {table_name}: {e}")
        return [], []
    finally:
        if conn: conn.close()

def get_table_names():
     """Gets all table names from the database."""
     conn = get_db_connection()
     if not conn: return []
     cursor = conn.cursor()
     try:
         cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
         tables = cursor.fetchall()
         return [t['name'] for t in tables]
     except sqlite3.Error as e:
        print(f"Error getting table names: {e}")
        return []
     finally:
        if conn: conn.close()


# --- Initialization ---
if __name__ == "__main__":
    print("Initializing Crop Trading Database...")
    initialize_database()
    print("Adding sample data (if needed)...")
    # Example: Add a farmer and crop if they don't exist
    # farmer_id = add_farmer("DEFAULT FARMER", "Initial Sample")
    # crop_id = add_crop("WHEAT", "KG")
    # if farmer_id and crop_id:
    #     print("Sample farmer and crop added/exist.")
    #     # You could add a sample purchase here for testing
    #     # record_purchase(farmer_id, crop_id, datetime.now().strftime('%Y-%m-%d'), 1000, 10, 20)

    print("Testing get functions:")
    print("Farmers:", get_farmers())
    print("Crops:", get_crops())
    print("Stock Summary:", get_stock_summary())