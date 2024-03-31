import random
import datetime

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
    bills_per_day = total_bills // total_days

    # Calculate random variation for each day
    daily_variations = [random.randint(-1, 2) for _ in range(total_days)]  # Adjust variation as needed

    # bill_distribution = {}
    final_distribution = {}
    start_bill = 1
    total = 0
    for i in range(total_days):
        date = start_date + datetime.timedelta(days=i)
        num_bills = bills_per_day + daily_variations[i]
        if num_bills >0:
            total += num_bills
            # bill_distribution[date] = num_bills
            for _ in range(num_bills):
                final_distribution[start_bill] = date
                start_bill += 1

    return total, final_distribution



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
        item_id: max(1, quantity[0] // ((end_date - quantity[1]).days +1))  # Set minimum target quantity to 1
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
            total_items_in_bill = random.randint(1, min(6, len(items_remaining_today)))
        else:
            total_items_in_bill = len(items_remaining_today)


        while len(bill_items) < total_items_in_bill and items_remaining:
            item_id, (quantity, item_start_date) = random.choice(list(items_remaining_today.items()))

            if date >= item_start_date:
                quantity_to_sell = random.randint(1, min(quantity, 5))
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


    if items_remaining:
        print("Warning: Some items remained unsold:")
        for item_id, (quantity, _) in items_remaining.items():
            print(f"- {item_id}: {quantity}")
    return bills


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
# for i in bill_distribution.items():
#     print(i) 