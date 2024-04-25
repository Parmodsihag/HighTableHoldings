import sqlite3

def convert_inventory_to_nosql(db_path="C://JBB//data//inventory.db"):
    """
    Retrieves tables from inventory.db and converts them to a NoSQL-like structure.

    Args:
        db_path (str, optional): Path to the inventory.db file. Defaults to "C://JBB//data//inventory.db".

    Returns:
        dict: A dictionary representing the NoSQL-like structure.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    nosql_data = {}

    # Get list of item tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'item_%'")
    item_tables = [row[0] for row in cursor.fetchall()]

    # Process item data and transactions
    for table_name in item_tables:
        item_id = int(table_name.split("_")[1])
        item_data = cursor.execute(f"SELECT * FROM items WHERE id={item_id}").fetchone()
        transactions = cursor.execute(f"SELECT * FROM {table_name}").fetchall()

        nosql_data[item_id] = {
            "name": item_data[1],
            "stock_value": item_data[2],
            "last_value": item_data[3],
            "unit": item_data[4],
            "batch": item_data[5],
            "expiry_date": item_data[6],
            "gst_rate": item_data[7],
            "item_type": item_data[8],
            "pakka_kacha": item_data[9],
            "transactions": [
                {
                    "date": transaction[1],
                    "received": transaction[2],
                    "sale": transaction[3],
                    "description": transaction[4],
                    "tags": transaction[5]
                } for transaction in transactions
            ]
        }

    conn.close()
    return nosql_data

def convert_accounts_to_nosql(db_path="C://JBB//data//accounts.db"):
    """
    Retrieves tables from accounts.db and converts them to a NoSQL-like structure.

    Args:
        db_path (str, optional): Path to the accounts.db file. Defaults to "C://JBB//data//accounts.db".

    Returns:
        dict: A dictionary representing the NoSQL-like structure.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    nosql_data = {}

    # Get list of customer tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'customer_%'")
    customer_tables = [row[0] for row in cursor.fetchall()][1:]


    # Process customer data and transactions
    for table_name in customer_tables:
        print(table_name)
        customer_id = int(table_name.split("_")[1])
        customer_data = cursor.execute(f"SELECT * FROM customers WHERE id={customer_id}").fetchone()
        transactions = cursor.execute(f"SELECT * FROM {table_name}").fetchall()

        nosql_data[customer_id] = {
            "name": customer_data[1],
            "other_details": customer_data[2],
            "transactions": [
                {
                    "date": transaction[1],
                    "description": transaction[2],
                    "amount": transaction[3],
                    "type": transaction[4],
                    "tags": transaction[5]
                } for transaction in transactions
            ]
        }

    conn.close()
    return nosql_data

nosql_data = convert_accounts_to_nosql()
for i in nosql_data.items():
    print(i)