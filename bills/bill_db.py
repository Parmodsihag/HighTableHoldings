import sqlite3

db_name = "C://JBB//data//bills.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS item_details (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        unit TEXT,
        month_year TEXT,
        rate REAL,
        type TEXT,
        start_date TEXT,
        batch TEXT,
        expiry_date TEXT,
        quantity TEXT
    
    )
""")

# Create bill_details table (consolidated for the year)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bill_details (
        id INTEGER PRIMARY KEY,
        bill_number INTEGER NOT NULL,
        date TEXT NOT NULL,
        customer_name TEXT,
        customer_address TEXT
    )
""")
# Create bill_and_items table (consolidated for the year)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bill_and_items (
        id INTEGER PRIMARY KEY,
        bill_number INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        item_quantity INTEGER NOT NULL,
        FOREIGN KEY (bill_number) REFERENCES bill_details(bill_number),
        FOREIGN KEY (item_id) REFERENCES item_details(id)
    )
""")

conn.commit()
conn.close()

def insert_item(item_data):
    """Inserts an item into the item_details table."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO item_details (name, unit, month_year, rate, type, start_date, batch, expiry_date, quantity) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, item_data)

    conn.commit()
    conn.close()

def get_items_by_month_year(month_year):
    """Retrieves all item details for a specific month_year."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM item_details WHERE month_year = ?", (month_year,))
    items = cursor.fetchall()

    conn.close()
    return items


def get_all_month_years():
    """Retrieves all distinct month_year values from the item_details table."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT month_year FROM item_details")
    month_years = [row[0] for row in cursor.fetchall()]

    conn.close()
    return month_years

def insert_bill(bill_data):
    """Inserts a bill into the bill_details table."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO bill_details (bill_number, date, customer_name, customer_address) VALUES (?, ?, ?, ?)", bill_data)

    conn.commit()
    conn.close()

def insert_bill_item(bill_item_data):
    """Inserts a bill item into the bill_and_items table."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO bill_and_items (bill_number, item_id, item_quantity) VALUES (?, ?, ?)", bill_item_data)

    conn.commit()
    conn.close()

def get_bills_by_month(month_year):
    """Retrieves bills for a specific month."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bill_details WHERE month_year = ?", (month_year,))
    bills = cursor.fetchall()

    conn.close()
    return bills

def get_bill_items(bill_number):
    """Retrieves items for a specific bill."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bill_and_items WHERE bill_number = ?", (bill_number,))
    bill_items = cursor.fetchall()

    conn.close()
    return bill_items

def update_item_quantity(item_id, new_quantity):
    """Updates the quantity of an item in the item_details table."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("UPDATE item_details SET quantity = ? WHERE id = ?", (new_quantity, item_id))

    conn.commit()
    conn.close()


def get_all_items():
    """Retrieves all items from the item_details table."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM item_details")
    items = cursor.fetchall()

    conn.close()
    return items

def get_item_by_id(item_id):
    """Retrieves an item by its ID."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM item_details WHERE id = ?", (item_id,))
    item = cursor.fetchone()

    conn.close()
    return item

def delete_bill(bill_number):
    """Deletes a bill and its associated items."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Delete bill items first to maintain foreign key constraints
    cursor.execute("DELETE FROM bill_and_items WHERE bill_number = ?", (bill_number,))
    cursor.execute("DELETE FROM bill_details WHERE bill_number = ?", (bill_number,))

    conn.commit()
    conn.close()

def get_total_sales_by_month(month_year):
    """Calculates the total sales for a specific month."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(item_quantity * i.rate) AS total_sales
        FROM bill_and_items bi
        JOIN bill_details bd ON bi.bill_number = bd.bill_number
        JOIN item_details i ON bi.item_id = i.id
        WHERE bd.month_year = ?
    """, (month_year,))

    total_sales = cursor.fetchone()[0]

    conn.close()
    return total_sales