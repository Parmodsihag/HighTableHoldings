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

def modify_item_details(item_id, new_item_data):
    """
    Modifies an item in the item_details table.

    Args:
        item_id (int): The ID of the item to modify.
        new_item_data (tuple): A tuple containing the new values for 
                              (name, unit, month_year, rate, type, start_date, batch, expiry_date, quantity).
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    update_query = """
        UPDATE item_details 
        SET name = ?, unit = ?, month_year = ?, rate = ?, type = ?, start_date = ?,
            batch = ?, expiry_date = ?, quantity = ?
        WHERE id = ?
    """
    cursor.execute(update_query, new_item_data + (item_id,))
    conn.commit()
    conn.close()


def modify_bill_details(bill_number, new_bill_data):
    """
    Modifies a bill in the bill_details table.

    Args:
        bill_number (int): The bill number to modify.
        new_bill_data (tuple): A tuple containing the new values for 
                               (date, customer_name, customer_address).
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    update_query = """
        UPDATE bill_details 
        SET date = ?, customer_name = ?, customer_address = ?
        WHERE bill_number = ?
    """
    cursor.execute(update_query, new_bill_data + (bill_number,))
    conn.commit()
    conn.close()

def modify_bill_item(bill_number, item_id, new_item_quantity):
    """
    Modifies the quantity of an item associated with a bill in the bill_and_items table.

    Args:
        bill_number (int): The bill number.
        item_id (int): The ID of the item.
        new_item_quantity (int): The new quantity of the item.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    update_query = """
        UPDATE bill_and_items
        SET item_quantity = ?
        WHERE bill_number = ? AND item_id = ?
    """
    cursor.execute(update_query, (new_item_quantity, bill_number, item_id))
    conn.commit()
    conn.close()

def delete_row(table_name, row_id):
    """
    Deletes a row from a specified table based on its ID.

    Args:
        table_name (str): The name of the table.
        row_id (int): The ID of the row to delete.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    delete_query = f"DELETE FROM {table_name} WHERE id = ?"
    cursor.execute(delete_query, (row_id,))
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

def get_all_bill_numbers():
    """Retrieves bills for a specific month."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT bill_number FROM bill_details")
    bills = cursor.fetchall()

    conn.close()
    return bills

def get_all_details_bill_numbers(bill_number):
    """Retrieves bills for a specific month."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bill_details where bill_number = ?", (bill_number,))
    bills = cursor.fetchone()

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


def check_bills_exist_for_month_year(month_year):
    """Checks if bills exist for a given month and year."""

    conn = sqlite3.connect(db_name)  # Assuming db_name is defined as in your provided code
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM bill_details WHERE strftime('%Y-%m', date) = ?", (month_year,))
    num_bills = cursor.fetchone()[0]

    conn.close()

    return num_bills > 0

def delete_bills_for_month_year(month_year):
    """Deletes bills and their associated items for a given month and year."""

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Get bill numbers for the specified month_year
    cursor.execute("SELECT bill_number FROM bill_details WHERE strftime('%Y-%m', date) = ?", (month_year,))
    bill_numbers = [row[0] for row in cursor.fetchall()]

    # Delete bill items first to maintain foreign key constraints
    for bill_number in bill_numbers:
        cursor.execute("DELETE FROM bill_and_items WHERE bill_number = ?", (bill_number,))

    # Delete bills
    cursor.execute("DELETE FROM bill_details WHERE strftime('%Y-%m', date) = ?", (month_year,))

    conn.commit()
    conn.close()

# x = check_bills_exist_for_month_year("2024-01")

# print(x)



def get_item_date_matrix(month_year):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Get distinct dates and item names
    cursor.execute("SELECT DISTINCT date FROM bill_details WHERE strftime('%Y-%m', date) = ?", (month_year,))
    dates = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT name FROM item_details")
    item_names = [row[0] for row in cursor.fetchall()]

    # Create a matrix filled with zeros
    matrix = [[0 for _ in dates] for _ in item_names]

    # Query to get item counts for each date
    cursor.execute("""
        SELECT i.name, bd.date, SUM(bi.item_quantity)
        FROM bill_and_items bi
        JOIN bill_details bd ON bi.bill_number = bd.bill_number
        JOIN item_details i ON bi.item_id = i.id
        WHERE strftime('%Y-%m', bd.date) = ?
        GROUP BY i.name, bd.date
    """, (month_year,))

    # Fill the matrix with item counts
    for item_name, date, count in cursor:
        row_index = item_names.index(item_name)
        col_index = dates.index(date)
        matrix[row_index][col_index] = count

    conn.close()
    return matrix, dates, item_names


if __name__ == "__main__":
    # Replace with desired month_year
    matrix , dates, item_names = get_item_date_matrix("2024-03")
    print(" "*20, end="")
    for i in dates:
        print(i.split('-')[2], end="  ")

    print()
    j = 0
    for row in matrix:
        print(item_names[j], end=" "*(20 -len(item_names[j])))
        j += 1
        for i in row:
            if i:
                print(i, end='   ')
            else:
                print('-', end='   ')
        print()

