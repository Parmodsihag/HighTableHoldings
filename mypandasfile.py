
# import numpy as np
import pandas as pd
# import time

import accounts
import datetime

def get_all_list():
    try:
        result = accounts.get_table("customers")
        column_names = ['customer_id', 'name', 'detail']
        customer_df = pd.DataFrame(result, columns=column_names)
    except:
        print('error in get all list line 15 of mypandasfile')
    
    customer_df[['Amount', 'Days']] = customer_df.apply(lambda row: pd.Series(get_one_total(row['customer_id'])), axis=1)

    # customer_df.to_csv("mydata.csv", index=False)

    # print(customer_df.head())
    return customer_df
    

def get_one_total(customer_id):
    # print(customer_id)
    result = accounts.get_table1(f"customer_{customer_id}")

    table_df = pd.DataFrame(result)
    table_df[0] = pd.to_datetime(table_df[0])
    today = pd.to_datetime(datetime.date.today())

    table_df[3] = (today-table_df[0]).dt.days
    interest_one_day = 0.0006575342465753425
    table_df[4] = table_df[3]*interest_one_day
    table_df['result'] = table_df[1]
    table_df[2] = table_df[2].str.lower()
    table_df.loc[table_df[2] == "p" , 'result'] *= table_df[4]
    table_df.loc[table_df[2] == "m", 'result'] *= -table_df[4]

    s1 = table_df['result'].sum()
    s = table_df.loc[table_df[2] == "p", 1].sum() -  table_df.loc[table_df[2] == "m", 1].sum()

    last_days = table_df[3].min()
    # print(table_df)
    # print(last_days)
    mysum = round(s+s1, 2)

    return mysum, last_days

    # print(s1, s, s+s1)

    
customer_df = get_all_list()
# s = time.time()
# get_all_list()
# e = time.time()
# print(e-s)
# get_one_total(10)