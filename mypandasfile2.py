import pandas as pd
from database import accounts
# import accounts
import datetime
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
    try:
        result = accounts.get_table1(f"customer_{customer_id}")
    except Exception as e:
        print(f'Error in get_one_total: {str(e)}')
        return pd.Series([0, 0])
    try:
        table_df = pd.DataFrame(result)
        table_df[0] = pd.to_datetime(table_df[0])
        today = pd.to_datetime(datetime.date.today())

        table_df[3] = (today - table_df[0]).dt.days
        interest_one_day = 0.0006575342465753425
        table_df[4] = table_df[3] * interest_one_day
        table_df['result'] = table_df[1]
        table_df[2] = table_df[2].str.lower()
        table_df.loc[table_df[2] == "p", 'result'] *= table_df[4]
        table_df.loc[table_df[2] == "m", 'result'] *= -table_df[4]

        s1 = table_df['result'].sum()
        s = table_df.loc[table_df[2] == "p", 1].sum() - table_df.loc[table_df[2] == "m", 1].sum()

        last_days = table_df[3].min()
        mysum = round(s + s1, 2)

    except:
        return pd.Series([0, 0])

    return pd.Series([mysum, last_days])



