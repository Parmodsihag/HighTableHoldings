import pandas as pd
import random
from datetime import datetime, timedelta
from billng_invoice import make_bill



random_name_list = ['RAMESH', 'लेखरम', 'सुभाष', 'राजेश', 'महावीर', 'सुरेश', 'माईलाल', 'हवासिंघ', 'बलबीर', 'मोमन', 'संदीप ', 'लुणाराम ', 'सोनू ', 'लिलु', 'मोलुराम', 'हनुमान', 'सतबीर', 'हंशराज', 'विजय', 'अनूप', 'सुशील ', 'उमेद ', 'सतपाल', 'शंकर', 'ईस्वर', 'कृष्ण ', 'मंजीत', 'मनीराम', 'दिलबाग', 'बुधराम','उग्रसेन ', 'राहुल ', 'बजीर ', 'मंगतुराम ', 'विष्णु', 'रोहताश ', 'रामभगत', 'बंशी', 'दारासिंह ', 'दर्शन ', 'जोगेन्दर ', 'पप्पू', 'संतलाल', 'बिंदर', 'रामनिवास ', 'भूप','भूपसिंघ', 'बलवंत', 'ज्वाहरलाल ', 'फुसाराम ', 'नेकीराम', 'सुरेंदर', 'मदन', 'आत्माराम', 'भादर', 'कालूरम', 'सज्जन', 'जगमाल', 'रामजीलाल', 'नवीन ', 'विक्रम ', 'दीपक ', 'दिनेश ', 'बंटी', 'राजबीर', 'रामलाल', 'रणवीर ', 'मोहित ', 'जगदीश ', 'नरेंदर', 'सुमित ', 'सिशपाल ', 'कालूरम', 'भालसिंघ ', 'विकास', 'बलवंत ', 'मंदीप', 'बलराज', 'ओमप्रकाश ', 'अशोक', 'विनोद', 'रमेश', 'रामफल', 'संजय', 'सुल्तान', 'राजेंदर', 'विरेंदर', 'अनिल', 'महावीर' ]
# Replace 'your_csv_file.csv' with the actual path to your CSV file
csv_file_path = 'test.csv'

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file_path)
# print(df)

year = 2023
mon = 11
date = 30


def generate_random_values(year, month, sdate, edate, month_end_date, quantity):
    final_list = []
    for i in range(1, sdate):
        final_list.append(0)
    start_date = datetime(year, month, sdate)
    end_date = datetime(year, month, edate)
        
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    # Generate random values
    random_values = [random.uniform(0, 1) for _ in range(len(date_range))]
    
    # Calculate the sum of random values
    sum_random_values = sum(random_values)
    
    # Scale the values to make their sum exactly equal to the given quantity
    scaled_values = [int(round(value * quantity / sum_random_values)) for value in random_values]
    
    # Adjust the last value to ensure the sum is exactly equal to the quantity
    scaled_values[-1] += quantity - sum(scaled_values)
    final_list.extend(scaled_values)
    for i in range(edate, month_end_date):
        final_list.append(0)

    return final_list

# Example usage:
# start_date = datetime(2024, 1, 1)
# end_date = datetime(2024, 1, 30)
# quantity = 24
# result = generate_random_values(start_date, end_date, quantity)
# print(result)
# print(sum(result))
# print(len(result))


# for i, r in df.iterrows():
#     print(i, r['Start_date'])

def make_final_list(df):
    final_list = []
    for index, row in df.iterrows():
        temp = [index]
        sdate = row['Start_date']
        edate = row['End_date']
        quantity = row['quantity']
        random_distribution = generate_random_values(2023, 11, sdate, edate, 30, quantity)
        temp.append(random_distribution)
        # final_list.append(temp)
        final_list.append(random_distribution)

    
    return final_list

def convert_to_df(lst, df3, year,  month):
    max_date = 30
    column_names = list(range(1, max_date + 1))
    df = pd.DataFrame(lst, columns=column_names)
    bill_number = 100
    for i in df.columns.to_list():
        quantity_list = df[i].tolist()
        list1 = quantity_list
        df2 = df3.iloc[[i for i, val in enumerate(list1) if val != 0]]
        quantity_list2 = []
        for j in quantity_list:
            if j:
                quantity_list2.append(j)

        bill_number += 1
        bill_date = f"{year}-{month}-{i}"
        customer_name = random.choice(random_name_list)
        customer_address = "Dhansu"
        name_list = df2['item_name'].tolist()
        unit_list = df2['Unit'].tolist()
        batch_list = df2['Batch'].tolist()
        exp_list = df2['Expiry Date'].tolist()
        rate_list = df2['rate'].tolist()
        type_list = df2['Type'].tolist()

        print(bill_number)

        make_bill(bill_number, bill_date, customer_name, customer_address, name_list, unit_list, batch_list,
                  exp_list, rate_list, type_list, quantity_list2)
        
    
    

    

fl = make_final_list(df)
convert_to_df(fl, df, 2023, 11)

# # Fetch information from specific columns
# names = df['name']
# units = df['unit']
# batches = df['batch']
# expiration_dates = df['exp']
# rates = df['rate']
# types = df['type']
# quantities = df['quantity']
# start_dates = df['start_date']

# # Now you can use these variables as needed in your Python code
# # For example, you can print the names:
# print(names)
















'''

to_add
    name
    unit
    batch
    exp
    rate
    type

to_bill 
    bill_Number - autoincrement 
    customer_name- random auto genrate
    Bill date 
    Customer address - dhansu default

    per_item
        item_name 
        batch 
        quantity




        


1 an item list include all above details about items
2 quanity list
3 start_date list

genrate a 2d list 

user enter details in 









'''