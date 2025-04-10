import pandas as pd
from database import accounts
# import accounts
import datetime
from datetime import date
# import time

def get_all_list():
    try:
        result = accounts.get_table("customers")
        column_names = ['customer_id', 'name', 'detail']
        customer_df = pd.DataFrame(result, columns=column_names)
    except Exception as e:
        print(f'Error in get_all_list: {str(e)}')
        return pd.DataFrame()
    
    try:
        customer_df[['Amount', 'Days']] = customer_df['customer_id'].apply(get_one_total).apply(pd.Series)
    except Exception as e:
        print(e)

    return customer_df

def get_one_total(customer_id):
    """
    Calculates the total amount and minimum days for a given customer, 
    taking into account compound interest and settlement dates.
    """
    try:
        transactions = accounts.get_normal_customer_transactions(customer_id)
        if not transactions:
            return pd.Series([0, 0])

        df = pd.DataFrame(transactions, columns=['id', 'date', 'description', 'amount', 'type', 'tags'])
        
        df['date'] = pd.to_datetime(df['date'])
        today_datetime = pd.to_datetime(date.today())
        df['days'] = (today_datetime - df['date']).dt.days
        min_days = df['days'].min() if not df.empty else 0
        total_balance = accounts.get_account_balance(customer_id)

        return pd.Series([round(total_balance, 2), min_days])

    except Exception as e:
        print(f'Error in get_one_total for customer {customer_id}: {str(e)}')
        return pd.Series([0, 0])



if __name__ == "__main__":
    print("hello")
    x = get_one_total(2)
    # x = get_all_list()
    print(x)