import random
import datetime
if __name__ == "__main__":
    import bill_db
    import bills_class
else:
    import bills.bill_db as bill_db
    import bills.bills_class as bills_class


random_name_list = ['रमेश', 'लेखरम', 'सुभाष', 'राजेश', 'महावीर', 'सुरेश', 'माईलाल', 'हवासिंघ', 'बलबीर', 'मोमन', 'संदीप ', 'लुणाराम ', 'सोनू ', 'लिलु', 'मोलुराम', 'हनुमान', 'सतबीर', 'हंशराज', 'विजय', 'अनूप', 'सुशील ', 'उमेद ', 'सतपाल', 'शंकर', 'ईस्वर', 'कृष्ण ', 'मंजीत', 'मनीराम', 'दिलबाग', 'बुधराम','उग्रसेन ', 'राहुल ', 'बजीर ', 'मंगतुराम ', 'विष्णु', 'रोहताश ', 'रामभगत', 'बंशी', 'दारासिंह ', 'दर्शन ', 'जोगेन्दर ', 'पप्पू', 'संतलाल', 'बिंदर', 'रामनिवास ', 'भूप','भूपसिंघ', 'बलवंत', 'ज्वाहरलाल ', 'फुसाराम ', 'नेकीराम', 'सुरेंदर', 'मदन', 'आत्माराम', 'कालूरम', 'सज्जन', 'जगमाल', 'रामजीलाल', 'नवीन ', 'विक्रम ', 'दीपक ', 'दिनेश ', 'बंटी', 'राजबीर', 'रामलाल', 'रणवीर ', 'मोहित ', 'जगदीश ', 'नरेंदर', 'सुमित ', 'सिशपाल ', 'कालूरम', 'भालसिंघ ', 'विकास', 'बलवंत ', 'मंदीप', 'बलराज', 'ओमप्रकाश ', 'अशोक', 'विनोद', 'रमेश', 'रामफल', 'संजय', 'सुल्तान', 'राजेंदर', 'विरेंदर', 'अनिल', 'महावीर' ]


def calculate_total_amount(items_with_quantities_and_prices):
    """
    Calculates the total amount of money involved based on item quantities and prices.
    """

    total_amount = 0
    for item_id, quantity, price in items_with_quantities_and_prices:
        total_amount += quantity * price

    return total_amount

def calculate_total_bills(total_amount, approx_bill_value):
    """
    Calculates the approximate number of bills needed based on the total amount and desired bill value.
    """

    total_bills = int(total_amount / approx_bill_value)

    # Add some random variation to the number of bills
    variation = random.randint(-5, 5)  # Adjust variation as needed
    total_bills += variation

    return total_bills

def distribute_bills_to_dates(total_bills, start_date, end_date):
    """
    Distributes the total number of bills across the given date range.
    """

    total_days = (end_date - start_date).days + 1
    bills_per_day = round(total_bills / total_days)
    # bills_per_day1 = total_bills // total_days
    # print(bills_per_day)

    # Calculate random variation for each day
    # daily_variations = [random.randint(-1, 2) for _ in range(total_days)]  # Adjust variation as needed

    # bill_distribution = {}
    final_distribution = {}
    start_bill = 1
    for i in range(total_days):
        date = start_date + datetime.timedelta(days=i)
        num_bills = random.randint(bills_per_day-1, bills_per_day+1)
        if num_bills >0:
            for _ in range(num_bills):
                final_distribution[start_bill] = date
                start_bill += 1

    return final_distribution



def distribute_quantities(items_with_quantities_and_start_dates, final_distribution, start_bill_number):
    """
    Distributes item quantities across bills based on the bill distribution and constraints.
    """

    bills = []
    items_remaining = {
        item_id: (quantity, item_start_date)
        for item_id, quantity, item_start_date in items_with_quantities_and_start_dates
    }
    # total_days = (end_date - start_date).days + 1
    target_quantities = {
        item_id: max(1, quantity[0] // ((end_date - quantity[1]).days +1)) 
        for item_id, quantity in items_remaining.items()
    }
    # Calculate x for each item at the start
    total_bills = len(final_distribution)
    x_values = {
        item_id: round(quantity[0] / total_bills) + 1
        for item_id, quantity in items_remaining.items()
    }
    for bill_number, date in final_distribution.items():
        bill_items = {}
        items_remaining_today = {
            item_id : (quantity[0], quantity[1])
            for item_id , quantity in items_remaining.items()
            if quantity[1] <= date
        }
        if len(items_remaining_today) > 1:
            total_items_in_bill = random.randint(1, min(3, len(items_remaining_today)))
        else:
            total_items_in_bill = len(items_remaining_today)


        while len(bill_items) < total_items_in_bill and items_remaining:
            item_id, (quantity, item_start_date) = random.choice(list(items_remaining_today.items()))

            if date >= item_start_date:
                # Use the pre-calculated x value
                x = x_values[item_id]
                quantity_to_sell = random.randint(max(1, x - 2), min(x+1, quantity))

                # quantity_to_sell = random.randint(1, min(quantity, 5 ))
                bill_items[item_id] = quantity_to_sell
                items_remaining[item_id] = (quantity - quantity_to_sell, item_start_date)

                if items_remaining[item_id][0] == 0:
                    del items_remaining[item_id]

            # If no items can be added, break the loop to avoid infinite loop
            else:
                break  # Exit the loop if no items can be added

        if bill_items:
            bill = {
                "bill_number": start_bill_number,
                "date": date,
                "items": bill_items
            }
            start_bill_number+=1
            bills.append(bill)

    status = 1
    if items_remaining:
        status = 0
        print("Warning: Some items remained unsold:")
        for item_id, (quantity, _) in items_remaining.items():
            print(f"- {item_id}: {quantity}")

    return bills, status



def make_bills(year_month, number_of_bills, start_bill_number):
    year, month = map(int, year_month.split("-"))
    start_date = datetime.date(year, month, 1)
    if month == 12:
        end_date = (datetime.date(year+1, 1, 1) - datetime.timedelta(days=1))
    else:
        end_date = (datetime.date(year, month + 1, 1) - datetime.timedelta(days=1))
    # if month<10:
    #     start_bill_number = int(f"{year}0{month}001")
    # else:    
    #     start_bill_number = int(f"{year}{month}001")
    # start_bill_number = 2324379
    # start_bill_number = 2324481
    item_details = bill_db.get_items_by_month_year(year_month)

    if not number_of_bills:
        print("number of bills is zero")
    
    fd = distribute_bills_to_dates(number_of_bills, start_date, end_date)
    items_with_quantities_and_start_dates = []
    for i in item_details:
        y,m,d = map(int, i[6].split("-"))
        temp = [int(i[0]), int(i[9]), datetime.date(y,m,d)]
        items_with_quantities_and_start_dates.append(temp)

    bils, status = distribute_quantities(items_with_quantities_and_start_dates, fd, start_bill_number)
    if status:
        for i in bils:
            bill_number = i['bill_number']
            bill_date = i['date']
            bill_items = i['items']
            customer_name = random.choice(random_name_list)
            customer_address = 'Dhansu'
            bill_data = [bill_number, bill_date, customer_name, customer_address]
            bill_db.insert_bill(bill_data)
            # print()
            bill_obj = bills_class.Bill(customer_name, customer_address, bill_date, bill_number)
            for item in bill_items.items():
                bill_item_data = [bill_number, item[0], item[1]]
                bill_db.insert_bill_item(bill_item_data)
                item_details1 = bill_db.get_item_by_id(item[0])
                item_name = item_details1[1]
                unit = item_details1[2]
                rate = item_details1[4]
                item_type = item_details1[5]
                batch = item_details1[7]
                exp = item_details1[8]
                item_data_list = [item_name, unit, batch, exp , rate, item_type, item[1]]
                bill_obj.add_item(item_data_list)
            
            bill_obj.make_bill()
            del bill_obj
            
        return True
    else:
        return False




items_with_quantities_and_prices = [
    ("apple", 50, 100),
    ("banana", 100, 100),
    ("orange", 200,100),
]
items_with_quantities_and_start_dates = [
    ("apple", 50, datetime.date(2023, 11, 10)),
    ("banana", 100, datetime.date(2023, 11, 15)),
    ("orange", 200, datetime.date(2023, 11, 1)),
]
start_date = datetime.date(2023, 11, 1)
end_date = datetime.date(2023, 11, 30)

def test():
    start_bill_number = 1001
    approx_bill_value = 100
    total_amount = calculate_total_amount(items_with_quantities_and_prices)
    total_bills = calculate_total_bills(total_amount, approx_bill_value)
    total_bills = 40
    total, fd = distribute_bills_to_dates(total_bills, start_date, end_date)
    bils = distribute_quantities(items_with_quantities_and_start_dates, fd, start_bill_number)

    print(total_amount)
    print(total_bills)
    print(total)
    for i in bils:
        print(i)


if __name__ == '__main__':
    make_bills("2024-1", 80)
    # print(i) 
    # test()