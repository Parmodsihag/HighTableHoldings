import sqlite3

# connect to the inventory database
inventory_conn = sqlite3.connect('new/inventory.db')
inventory_cursor = inventory_conn.cursor()

# add auto-increment to the id column in the items table
inventory_cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        stock_value INTEGER DEFAULT 0,
        last_value INTEGER DEFAULT 0                        
    )
""")

alter_query = '''
    ALTER TABLE items
    ADD COLUMN last_value INTEGER DEFAULT 0;
'''
# inventory_cursor.execute("CREATE TABLE new_table AS SELECT id, name, stock_value FROM items")
# inventory_cursor.execute(" SELECT * FROM new_table")
# inventory_cursor.execute("DROP TABLE items")
# inventory_cursor.execute("ALTER TABLE new_table RENAME TO items")
# inventory_cursor.execute(alter_query)

# inventory_cursor.execute(" PRAGMA table_info(items);")
# print(inventory_cursor.fetchall())


# function to add a new item and create a table for it
def add_new_item(name, stock_value, last_value):
    # insert the new item into the items table and get its auto-incremented id
    inventory_cursor.execute("""
        INSERT INTO items (name, stock_value, last_value)
        VALUES (?, ?, ?)
    """, (name, stock_value, last_value))
    item_id = inventory_cursor.lastrowid
    
    # create a new table for the item with its id as the table name
    inventory_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS item_{item_id} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            received INTEGER,
            sale INTEGER,
            description TEXT,
            tags TEXT
        )
    """)
    
    # commit the changes to the database
    inventory_conn.commit()
    
    # return the id of the new item
    return item_id

def add_item_transaction(item_id, date, recieved, sale, description, tags=''):
    table_name = f'item_{item_id}'
    inventory_cursor.execute(f'''INSERT INTO {table_name}
                                 (date, received, sale, description, tags)
                                 VALUES (?, ?, ?, ?, ?)''',
                            (date, recieved, sale, description, tags))
    inventory_conn.commit()


# Function to modify an item
def modify_item(item_id, name, stock_value, last_value):
    inventory_cursor.execute("UPDATE items SET name=?, stock_value=?, last_value=? WHERE id=?", (name, stock_value, last_value, item_id))
    inventory_conn.commit()
    print("Item with id", item_id, "has been modified.")

# Function to delete an item
def delete_item(item_id):
    # First, drop the corresponding item table
    inventory_cursor.execute("DROP TABLE IF EXISTS item_{}".format(item_id))
    # Then, delete the item from the main items table
    inventory_cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
    inventory_conn.commit()
    print("Item with id", item_id, "has been deleted.")



# Define function to get all items
def get_all_items():
    inventory_cursor.execute('SELECT * FROM items')
    items = inventory_cursor.fetchall()
    return items

# Define function to get item by id
def get_item_by_id(item_id):
    inventory_cursor.execute('SELECT * FROM items WHERE id=?', (item_id,))
    item = inventory_cursor.fetchone()
    return item

# Define function to get all transactions for an item
def get_item_transactions(item_id):
    table_name = 'item_' + str(item_id)
    inventory_cursor.execute(f'SELECT * FROM {table_name}')
    transactions = inventory_cursor.fetchall()
    return transactions

def get_transaction_by_id(table_name, transaction_id):
    # table_name = "item_" + str(item_id)
    inventory_cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?", (transaction_id,))
    transaction = inventory_cursor.fetchone()
    return transaction


# function to modify transaction for an item
def modify_transaction(item_id, transaction_id, date, received, sale, description, tags):
    # check if the item exists in the inventory database
    inventory_cursor.execute('SELECT name FROM items WHERE id=?', (item_id,))
    item_name = inventory_cursor.fetchone()
    if item_name is None:
        print(f'Error: Item with ID {item_id} does not exist in the inventory database')
        return

    # check if the transaction exists in the item's transaction table
    item_table_name = f'item_{item_id}'
    inventory_cursor.execute(f'SELECT id FROM {item_table_name} WHERE id=?', (transaction_id,))
    transaction = inventory_cursor.fetchone()
    if transaction is None:
        print(f'Error: Transaction with ID {transaction_id} does not exist for item {item_name[0]}')
        return

    # update the transaction in the item's transaction table
    inventory_cursor.execute(f'UPDATE {item_table_name} SET date=?, received=?, sale=?, description=?, tags=? WHERE id=?',
                              (date, received, sale, description, tags, transaction_id))
    inventory_conn.commit()
    print(f'Transaction {transaction_id} for item {item_name[0]} has been modified successfully')


# function to delete a transaction for an item
def delete_transaction(item_id, transaction_id):
    # check if the item exists in the inventory database
    inventory_cursor.execute('SELECT name FROM items WHERE id=?', (item_id,))
    item_name = inventory_cursor.fetchone()
    if item_name is None:
        print(f'Error: Item with ID {item_id} does not exist in the inventory database')
        return

    # check if the transaction exists in the item's transaction table
    item_table_name = f'item_{item_id}'
    inventory_cursor.execute(f'SELECT id FROM {item_table_name} WHERE id=?', (transaction_id,))
    transaction = inventory_cursor.fetchone()
    if transaction is None:
        print(f'Error: Transaction with ID {transaction_id} does not exist for item {item_name[0]}')
        return

    # delete the transaction from the item's transaction table
    inventory_cursor.execute(f'DELETE FROM {item_table_name} WHERE id=?', (transaction_id,))
    inventory_conn.commit()
    print(f'Transaction {transaction_id} for item {item_name[0]} has been deleted successfully')

def get_item_transactions(item_id):
    transactions = []
    try:
        inventory_cursor.execute(f"SELECT * FROM item_{item_id}")
        rows = inventory_cursor.fetchall()
        for row in rows:
            transaction = {
                "id": row[0],
                "date": row[1],
                "received": row[2],
                "sale": row[3],
                "description": row[4],
                "tags": row[5]
            }
            transactions.append(transaction)
    except sqlite3.Error as e:
        print(f"Error getting transactions for item {item_id}: {e}")
    return transactions

def get_item_quantity(item_id):
    quantity = 0
    try:
        inventory_cursor.execute(f"SELECT SUM(received - sale) FROM item_{item_id}")
        row = inventory_cursor.fetchone()
        if row[0]:
            quantity = row[0]
    except sqlite3.Error as e:
        print(f"Error getting quantity for item {item_id}: {e}")
    return quantity

def get_item_value(item_id):
    quantity = get_item_quantity(item_id)
    inventory_cursor.execute(f"SELECT stock_value FROM items where id={item_id}")
    row = inventory_cursor.fetchone()[0]
    value = quantity * row
    return value

def get_inventory_value():
    value = 0
    try:
        inventory_cursor.execute("SELECT id, stock_value FROM items")
        rows = inventory_cursor.fetchall()
        for row in rows:
            item_value = get_item_value(row[0], row[1])
            value += item_value
    except sqlite3.Error as e:
        print(f"Error getting inventory value: {e}")
    return value

def get_last_value(item_id):
    inventory_cursor.execute(f"SELECT last_value FROM items where id={item_id}")
    row = inventory_cursor.fetchone()[0]
    return row

def set_last_value(item_id, value):
    inventory_cursor.execute("UPDATE items SET last_value=? WHERE id=?", (value, item_id))
    inventory_conn.commit()
    return f'Item Id {item_id} updated to value {value}'

def get_table(table_name):
    inventory_cursor.execute(f"select * from {table_name}")
    return inventory_cursor.fetchall()

if __name__ == '__main__':
    print('hello')
    print(get_last_value(4))
    # print(get_item_value(44))
    # get_item_value(44)