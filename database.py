import sqlite3

from datetime import datetime, timedelta
from sqlite3 import Error

try:
    daily_conn = sqlite3.connect('new/daily_notes.db')
    daily_cursor = daily_conn.cursor()
    today = datetime.now().strftime('%Y_%m_%d')
    daily_cursor.execute(f"CREATE TABLE IF NOT EXISTS d{today} (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT)")
    daily_conn.commit()

except Error as e:
    print(e, "error")

def table_exists(table_name):
    daily_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = daily_cursor.fetchone()
    return result is not None

def last_7_day_report():
    today = datetime.now().date()

    # Create a list of the last 7 dates
    last_7_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    last_7_dates = [i.strftime('%Y_%m_%d') for i in last_7_dates]

    last7dayslist = []
    for i in last_7_dates:
        temp = [i.split("_")[2]]
        if table_exists(f"d{i}"):
            daily_cursor.execute(f"SELECT COUNT(*) FROM d{i}")
            x = daily_cursor.fetchone()[0]
            temp.append(x)
        
        else:
            temp.append(0)

        last7dayslist.append(temp)
        # print(temp)
        # for k in j:
        #     print(k)

    # Print the list of dates
    # print(last7dayslist)
    return last7dayslist


def add_today_table(daily_notes_conn, daily_notes_cursor):
    # Get today's date
    today = datetime.now().strftime('%Y_%m_%d')
    
    # Check if table already exists for today's date
    daily_notes_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=f'd{today}'")
    if daily_notes_cursor.fetchone() is not None:
        print("Table already exists for today's date")
        return
    
    # Create table for today's date
    daily_notes_cursor.execute(f"CREATE TABLE IF NOT EXISTS d{today} (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT)")
    daily_notes_conn.commit()
    
    print(f"Table d{today} created successfully")

    
def add_note_to_date(note, date=datetime.now().strftime('%Y_%m_%d') ):
    try:
        
        # Create table if not exists
        table_name = date
        daily_cursor.execute(f"CREATE TABLE IF NOT EXISTS d{table_name} (id INTEGER PRIMARY KEY, description TEXT)")
        
        # Insert new note
        daily_cursor.execute(f"INSERT INTO d{table_name} (description) VALUES (?)", (note,))
        id = daily_cursor.lastrowid
        daily_conn.commit()
        print("Note added successfully.")
        return id
        
    except Error as e:       
        print(e)
        return 0

def get_notes(date):
    table_name = date.replace("-", "_")
    daily_cursor.execute(f"SELECT * FROM d{table_name}")
    notes = daily_cursor.fetchall()
    
    return notes

def update_note(date, note_id, new_description):
    table_name = date.replace("-", "_")
    daily_cursor.execute(f"UPDATE d{table_name} SET description=? WHERE id=?", (new_description, note_id))
    daily_conn.commit()
    

def delete_note(date, note_id):
    table_name = date.replace("-", "_")
    daily_cursor.execute(f"DELETE FROM d{table_name} WHERE id=?", (note_id,))
    daily_conn.commit()


def get_table(table_name):
    daily_cursor.execute(f"select * from {table_name}")
    return daily_cursor.fetchall()


if __name__ == '__main__':
    print('main')
    last_7_day_report()