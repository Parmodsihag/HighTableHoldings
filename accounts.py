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


def set_all_transaction_tags_to_zero(customer_id):
    """
    Updates all transactions in a customer's account to have "0" as the tags value.

    Args:
        customer_id (int): The ID of the customer whose transactions need to be updated.
    """

    table_name = f"customer_{customer_id}"
    query = f"UPDATE {table_name} SET tags = '0'"
    accounts_cursor.execute(query)
    accounts_conn.commit()


def calculate_interest(amt, from_date, today_date_1=datetime.date.today()):
    interest_rate_one_day = 0.0006575342465753425
    dt2 = from_date.split("-")
    date_of_entry = datetime.date(int(dt2[0]), int(dt2[1]), int(dt2[2]))
    date_difference = today_date_1 - date_of_entry
    interest = amt*date_difference.days*interest_rate_one_day
    return round(interest, 2)


def get_account_balace(customer_id):
    table_data = get_table1(f"customer_{customer_id}")
    total_sum = 0.0
    # total_sum_without_interest = 0.0
    # total_interest = 0.0
    for row in table_data:
        date = row[0]
        amount = row[1]
        transction_type = row[2]
        tag = row[3]
        # print(tag == "1")
        if tag == "1":
            intrest = calculate_interest(amount, date)
        else:
            intrest = 0
        ttl = float(amount) + intrest
        if transction_type.upper() == "P":
            # total_interest += intrest
            # total_sum_without_interest += float(amount)
            total_sum += ttl
        else:
            # total_interest -= intrest
            # total_sum_without_interest -= float(amount)
            total_sum -= ttl

    return round(total_sum, 2)


# print(get_account_balace(1))


if __name__ =='__main__':
    x = get_all_customers_name_and_id()
    x = [f"{i[0]} {i[1]}" for i in x]
    for i in x:
        print(i)