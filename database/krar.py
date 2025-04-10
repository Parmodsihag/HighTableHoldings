import sqlite3
from datetime import datetime, timedelta

# Connect to SQLite database (creates if not exists)
conn = sqlite3.connect('C://JBB//data//krar.db')
cursor = conn.cursor()


# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS all_krar (
        krar_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        is_nill INTEGER DEFAULT 0
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS by_krar_id (
        uid INTEGER PRIMARY KEY AUTOINCREMENT,
        kid INTEGER,
        date TEXT,
        FOREIGN KEY(kid) REFERENCES all_krar(krar_id)
    )
''')


# Function to add a new krar for a customer with checks for existing unsettled krar
def add_or_update_krar(customer_id, date):
    # Check if there's an unsettled krar for the customer
    cursor.execute('''
        SELECT krar_id FROM all_krar WHERE customer_id = ? AND is_nill = 0
    ''', (customer_id,))
    unsettled_krar = cursor.fetchone()

    if unsettled_krar:
        # If unsettled krar exists, get its krar_id and update 'by_krar_id' table
        krar_id = unsettled_krar[0]
        cursor.execute('''
            INSERT INTO by_krar_id (kid, date) VALUES (?, ?)
        ''', (krar_id, date))
        conn.commit()
        return krar_id
    else:
        # If no unsettled krar exists, add a new krar for the customer
        cursor.execute('''
            INSERT INTO all_krar (customer_id) VALUES (?)
        ''', (customer_id,))
        krar_id = cursor.lastrowid

        cursor.execute('''
            INSERT INTO by_krar_id (kid, date) VALUES (?, ?)
        ''', (krar_id, date))
        conn.commit()
        return krar_id



# Function to fetch details of unsettled krar for a customer
def get_unsettled_krar_dates(customer_id):
    cursor.execute('''
        SELECT b.date
        FROM all_krar a
        JOIN by_krar_id b ON a.krar_id = b.kid
        WHERE a.customer_id = ? AND a.is_nill = 0
    ''', (customer_id,))
    unsettled_dates = cursor.fetchall()
    return [date[0] for date in unsettled_dates]



# Function to fetch details of settled krar for a customer
def get_settled_krar_details(customer_id):
    cursor.execute('''
        SELECT a.krar_id, COUNT(*), MIN(b.date), MAX(b.date)
        FROM all_krar a
        JOIN by_krar_id b ON a.krar_id = b.kid
        WHERE a.customer_id = ? AND a.is_nill = 1
        GROUP BY a.krar_id
    ''', (customer_id,))
    settled_krar_details = cursor.fetchall()
    return settled_krar_details


# Function to set the settlement of krar by customer_id
def set_krar_settlement(customer_id):
    cursor.execute('''
        UPDATE all_krar SET is_nill = 1 WHERE customer_id = ? AND is_nill = 0
    ''', (customer_id,))
    conn.commit()

def modify_krar_customer_and_status(krar_id, new_customer_id, new_is_nill):
    cursor.execute('''
        UPDATE all_krar SET customer_id = ?, is_nill = ? WHERE krar_id = ?
    ''', (new_customer_id, new_is_nill, krar_id))
    conn.commit()


def modify_by_krar_id(uid, new_kid, new_date):
    cursor.execute('''
        UPDATE by_krar_id SET kid = ?, date = ? WHERE uid = ?
    ''', (new_kid, new_date, uid))
    conn.commit()



def delete_from_all_krar(krar_id):
    cursor.execute('''
        DELETE FROM by_krar_id WHERE kid = ?
    ''', (krar_id,))
    cursor.execute('''
        DELETE FROM all_krar WHERE krar_id = ?
    ''', (krar_id,))
    conn.commit()


def delete_from_by_krar_id(uid):
    cursor.execute('''
        DELETE FROM by_krar_id WHERE uid = ?
    ''', (uid,))
    conn.commit()

def get_accounts_with_unsettled_krars():
    cursor.execute('''
        SELECT DISTINCT customer_id
        FROM all_krar
        WHERE is_nill = 0
    ''')
    unsettled_accounts = cursor.fetchall()
    return [account[0] for account in unsettled_accounts]


def get_customers_with_last_krar_today():
    today = datetime.now().date()
    cursor.execute('''
        SELECT DISTINCT a.customer_id
        FROM all_krar a
        JOIN by_krar_id b ON a.krar_id = b.kid
        WHERE DATE(b.date) = ? AND DATE(b.date) = (SELECT MAX(DATE(date)) FROM by_krar_id WHERE kid = a.krar_id) AND is_nill = 0
    ''', (today,))
    customers_today = cursor.fetchall()
    return [customer[0] for customer in customers_today]


def get_customers_with_last_krar_past():
    today = datetime.now().date()
    cursor.execute('''
        SELECT DISTINCT a.customer_id
        FROM all_krar a
        JOIN by_krar_id b ON a.krar_id = b.kid
        WHERE DATE(b.date) < ? AND DATE(b.date) = (SELECT MAX(DATE(date)) FROM by_krar_id WHERE kid = a.krar_id) AND is_nill = 0
    ''', (today,))
    customers_past = cursor.fetchall()
    return [customer[0] for customer in customers_past]

def get_customers_with_last_krar_future():
    today = datetime.now().date()
    cursor.execute('''
        SELECT DISTINCT a.customer_id
        FROM all_krar a
        JOIN by_krar_id b ON a.krar_id = b.kid
        WHERE DATE(b.date) > ? AND DATE(b.date) = (SELECT MAX(DATE(date)) FROM by_krar_id WHERE kid = a.krar_id) AND is_nill = 0
    ''', (today,))
    customers_future = cursor.fetchall()
    return [customer[0] for customer in customers_future]
