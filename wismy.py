import sqlite3
import accounts

# --- DATABASE CONNECTION (Adjust path if needed) ---
accounts_conn = sqlite3.connect('C://JBB//data//accounts.db')
accounts_cursor = accounts_conn.cursor() 

def update_settlement_tags():
    """Updates tag values for settlement transactions in the accounts database."""
    customer_ids = accounts.get_customer_ids() 

    for customer_id in customer_ids:
        table_name = f"customer_{customer_id}"
        try:
            accounts_cursor.execute(f"SELECT * FROM {table_name} ORDER BY date, id")
            transactions = accounts_cursor.fetchall()
            i = 0
            while i < len(transactions):
                row = transactions[i] 
                tag = row[5]

                if tag == '0' and row[2] == "Aaj tak total": 
                    if i + 2 < len(transactions):  # Make sure there are enough rows
                        next_row = transactions[i+1] 
                        next_next_row = transactions[i+2]
                        
                        if next_next_row[2] == "DISCOUNT" and next_row[5] == "0" and next_next_row[5] == '0':
                            # We've found the settlement group (3 transactions)
                            i += 2  # Skip the next two rows (original, discount) 
                        else:
                            # The tag=0 transaction isn't part of a settlement group, so update it 
                            accounts_cursor.execute(
                                f"UPDATE {table_name} SET tags = '1' WHERE id = ?",
                                (row[0],)
                            )
                    else:
                        # Handle cases where you're at the end of the table
                        accounts_cursor.execute(
                                f"UPDATE {table_name} SET tags = '1' WHERE id = ?",
                                (row[0],)
                            )
                else: 
                    if tag == '0': # handle transactions those are accidently set to 0
                        accounts_cursor.execute(
                            f"UPDATE {table_name} SET tags = '1' WHERE id = ?",
                            (row[0],)
                        )
                i += 1
            accounts_conn.commit()
            print(f"Updated settlement tags for customer ID: {customer_id}")

        except sqlite3.Error as e:
            print(f"Error updating settlement tags for customer ID: {customer_id}: {e}") 

if __name__ == "__main__":
    update_settlement_tags() 
    print("Database updated!") 
    accounts_conn.close()