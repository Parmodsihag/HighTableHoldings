import sqlite3
import datetime

'''
TAGS

0 = nill 
1 = normal
2 = no intrest
'''
# Create a connection to the accounts database
accounts_conn = sqlite3.connect('C://JBB//data//accounts.db')
accounts_cursor = accounts_conn.cursor()


# Create a table to store information about all customers
accounts_cursor.execute('''CREATE TABLE IF NOT EXISTS customers
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                other_details TEXT)''')

# Function to add a new customer to the database
def add_new_customer(name, other_details):
    accounts_cursor.execute("""
        INSERT INTO customers (name, other_details)
        VALUES (?, ?)
    """, (name, other_details))
    id = accounts_cursor.lastrowid
    # Create a new table for the customer with their ID
    accounts_cursor.execute(f'''CREATE TABLE IF NOT EXISTS customer_{id}
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       date TEXT,
                       description TEXT,
                       amount REAL,
                       type TEXT,
                       tags TEXT)''')
    # Insert the new customer into the main customers table
    accounts_conn.commit()

    return id


# Function to get a list of all customer IDs
def get_customer_ids():
    accounts_cursor.execute("SELECT id FROM customers")
    return [row[0] for row in accounts_cursor.fetchall()]

# Function to get customer details by ID
def get_customer_details(customer_id):
    accounts_cursor.execute(f"SELECT * FROM customers WHERE id = {customer_id}")
    return accounts_cursor.fetchone()

def get_all_customers():
    accounts_cursor.execute(f"select * from customers")
    return accounts_cursor.fetchall()

def get_all_customers_name_and_id():
    accounts_cursor.execute(f"select id, name from customers")
    return accounts_cursor.fetchall()

# Function to get all transactions for a specific customer
def get_customer_transactions(customer_id):
    table_name = f'customer_{customer_id}'
    accounts_cursor.execute(f"SELECT * FROM {table_name}")
    return accounts_cursor.fetchall()

def get_normal_customer_transactions(customer_id):
    table_name = f'customer_{customer_id}'
    accounts_cursor.execute(f"SELECT * FROM {table_name} where tags != '0'")
    return accounts_cursor.fetchall()

def get_transaction_by_id(table_name, transaction_id):
    # table_name = "customer_" + str(item_id)
    accounts_cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?", (transaction_id,))
    transaction = accounts_cursor.fetchone()
    return transaction

# Function to add a new transaction for a specific customer
def add_customer_transaction(customer_id, date, description, amount, transaction_type, tags=''):
    table_name = f'customer_{customer_id}'
    accounts_cursor.execute(f'''INSERT INTO {table_name}
                                 (date, description, amount, type, tags)
                                 VALUES (?, ?, ?, ?, ?)''',
                            (date, description, amount, transaction_type, tags))
    accounts_conn.commit()



def update_customer_details(customer_id, name=None, other_details=None):
    query = "UPDATE customers SET "
    updates = []
    if name:
        updates.append("name = '{}'".format(name))
    if other_details:
        updates.append("other_details = '{}'".format(other_details))
    if not updates:
        return False
    query += ", ".join(updates)
    query += " WHERE id = {}".format(customer_id)
    accounts_cursor.execute(query)
    accounts_conn.commit()
    return True

def delete_customer(customer_id):
    query = "DROP TABLE IF EXISTS customer_{}".format(customer_id)
    accounts_cursor.execute(query)
    query = "DELETE FROM customers WHERE id = {}".format(customer_id)
    accounts_cursor.execute(query)
    accounts_conn.commit()
    return True


def update_customer_transaction(table_name, transaction_id, date, description, amount, transaction_type, tags):
    """
    Update an existing transaction for a customer in the accounts database.
    """
    query = "UPDATE {} SET date=?, description=?, amount=?, type=?, tags=? WHERE id=?".format(table_name)
    values = (date, description, amount, transaction_type, tags, transaction_id)
    accounts_cursor.execute(query, values)
    accounts_conn.commit()

def delete_customer_transaction(customer_id, transaction_id):
    """
    Delete a transaction for a customer from the accounts database.
    """
    query = "DELETE FROM customer_{} WHERE id=?".format(customer_id)
    values = (transaction_id,)
    accounts_cursor.execute(query, values)
    accounts_conn.commit()
    

def get_table(table_name):
    accounts_cursor.execute(f"select * from {table_name}")
    return accounts_cursor.fetchall()

def get_table1(table_name):
    accounts_cursor.execute(f"select date, amount, type, tags from {table_name} where tags != '0'")
    return accounts_cursor.fetchall()


def calculate_interest(principle_amount, from_date_str, to_date=datetime.date.today()):
        """
        Calculates interest earned on a principle amount, considering financial year-end (March 31st).

        Args:
            principle_amount (float): The initial amount of money.
            from_date_str (str): The starting date for interest calculation in "YYYY-MM-DD" format.
            to_date (datetime.date, optional): The ending date for interest calculation. Defaults to today.

        Returns:
            float: The calculated interest amount.
        """
        daily_interest_rate = 0.0006575342465753425 
        from_date = datetime.datetime.strptime(from_date_str, "%Y-%m-%d").date()
        total_interest = 0

        while from_date < to_date:
            year_end = datetime.date(from_date.year, 3, 31) 
            if from_date.month > 3:
                year_end = datetime.date(from_date.year + 1, 3, 31)
            end_date = min(year_end, to_date)
            days = (end_date - from_date).days
            interest = principle_amount * days * daily_interest_rate
            total_interest += interest
            principle_amount += interest 
            from_date = end_date + datetime.timedelta(days=1)

        return round(total_interest, 2)

def find_last_settlement_date(customer_id):
    """Finds the date of the last settled transaction."""
    table_name = f"customer_{customer_id}"
    accounts_cursor.execute(f"SELECT MAX(date) FROM {table_name} WHERE tags = '0'")
    result = accounts_cursor.fetchone()
    return result[0] if result[0] is not None else None

def find_last_settlement_id_on_date(customer_id, last_settlement_date):
    """Finds the id of the last settled transaction on a given date."""
    table_name = f"customer_{customer_id}"
    accounts_cursor.execute(f"""
        SELECT id FROM {table_name}
        WHERE date = ? AND tags = '0'
        ORDER BY id DESC
    """, (last_settlement_date,))
    result = accounts_cursor.fetchone()
    return result[0] if result is not None else None

def get_account_balance(customer_id):
    """Calculates the account balance for a customer, including interest,
       considering only the current (unsettled) period.
    """
    table_name = f"customer_{customer_id}"
    last_settlement_date = find_last_settlement_date(customer_id)
    
    if last_settlement_date is not None:
        last_settlement_id_on_date = find_last_settlement_id_on_date(customer_id, last_settlement_date)

        accounts_cursor.execute(f"""
            SELECT * FROM {table_name}
            WHERE (date > ?) OR (date = ? AND id > ?) 
            ORDER BY date, id
        """, (last_settlement_date, last_settlement_date, last_settlement_id_on_date))

    else:
        # No settlements, include all transactions 
        accounts_cursor.execute(f"SELECT * FROM {table_name} ORDER BY date, id")

    transactions = accounts_cursor.fetchall()
    balance = 0.0

    for row in transactions:
        date_str = row[1]
        amount = row[3]
        transaction_type = row[4]
        tag = row[5]

        if tag == '1':  # Interest-bearing transaction
            interest = calculate_interest(amount, date_str)
            total = amount + interest
        else:  # No-interest transaction (tag=2) 
            total = amount

        if transaction_type == "P":
            balance += total
        else: # if transaciton type = "M"
            balance -= total

    return round(balance, 2)

# print(get_account_balace(1))


if __name__ =='__main__':
    while True:
        
        x = input(": ")
        if x == "q":
            break
        accounts_cursor.execute(x)
        for i in accounts_cursor.fetchall():
            print(i)
        accounts_conn.commit()
    
    # print(get_account_balance(2))
    # x = get_all_customers_name_and_id()
    # x = [f"{i[0]} {i[1]}" for i in x]
    # for i in x:
    #     print(i)