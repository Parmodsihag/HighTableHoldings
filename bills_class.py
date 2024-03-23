from docxtpl import DocxTemplate


class Num2wordshindi:
    
    low_num_dict = {'1':'एक','2':'दौ','3':'तीन','4':'चार','5':'पाँच',
    '6':'छः','7':'सात','8':'आठ','9':'नौ', '0':'शून्य'
    }
    mid_num_dict = {'10':'दस', '11': 'ग्यारह', '12': 'बारह', '13': 'तेरह', '14':'चौदह', '15': 'पंद्रह', '16': 'सोलह', '17': 'सत्रह', '18': 'अठारह', '19': 'उन्नीस',
    '20': 'बीस', '21': 'इक्कीस', '22': 'बाईस', '23': 'तेईस', '24': 'चौबीस', '25': 'पच्चीस', '26': 'छब्बीस', '27': 'सत्ताईस', '28': 'अट्ठाईस', '29': 'उनतीस',
    '30': 'तीस', '31': 'इकतीस', '32': 'बत्तीस', '33': 'तैंतीस', '34': 'चौंतीस', '35': 'पैंतीस', '36': 'छतीस', '37': 'सैंतीस', '38': 'अड़तीस', '39': 'उनतालीस',
    '40': 'चालीस', '41': 'इकतालीस', '42': 'बयालीस', '43': 'तैंतालीस', '44': 'चवालीस', '45': 'पैंतालीस', '46': 'छियालीस', '47': 'सैंतालीस', '48': 'अड़तालीस', '49': 'उड़ंचास',
    '50': 'पचास', '51': 'इक्यावन', '52': 'बावन', '53': 'तिरेपन', '54': 'चौवन', '55': 'पचपन', '56': 'छप्पन', '57': 'सत्तावन', '58': 'अट्ठावन', '59': 'उनसठ',
    '60': 'साठ', '61': 'इकसठ', '62': 'बासठ', '63': 'तिरेसठ', '64': 'चौसठ', '65': 'पैंसठ', '66': 'छियासठ', '67': 'सड़सठ', '68': 'अड़सठ', '69': 'उनहत्तर',
    '70': 'सत्तर', '71': 'इकहत्तर', '72': 'बहत्तर', '73': 'तिहत्तर', '74': 'चौहत्तर', '75': 'पिचहत्तर', '76': 'छिहत्तर', '77': 'सतत्तर', '78': 'अठहत्तर', '79': 'उनासी',
    '80': 'अस्सी', '81': 'इक्यासी', '82': 'बियासी', '83': 'तिरासी', '84': 'चौरासी', '85': 'पिचासी', '86': 'छियासी', '87': 'सत्तासी', '88': 'अट्ठासी', '89': 'नवासी',
    '90': 'नब्बे', '91': 'इक्यानवे', '92': 'बानवे', '93': 'तिरानवे', '94': 'चौरानवे', '95': 'पिचानवे', '96': 'छियानवे', '97': 'सत्तानवे', '98': 'अट्ठानवे', '99': 'निन्यानवे',
    '100': 'सौ' , '00': ' '
    }
    
    def __init__(self, number):
        self.nummber_to_change = number
        
    def change_to_lst(self):
        my_lst = str(self.nummber_to_change).split('.')
        return my_lst

    def lst1str(self, lst):
        if lst == '0':
            return ''
        else:
            return self.low_num_dict.get(lst)
    
    def lst2str(self, lst):
        
        if lst == '00':
            return ''
        
        elif lst[0] == '0':
            return self.low_num_dict.get(lst[1])
        
        else:
            return self.mid_num_dict.get(lst)

    def lst3str(self, lst):
        if lst == '000':
            return ''
        
        elif lst[0] == '0':
            return self.lst2str(lst[1:])

        else:
            return f'{self.lst1str(lst[0])} सौ {self.lst2str(lst[1:])}'

    def lst4str(self, lst):
        if lst == '0000':
            return ''
        elif lst[0] == '0':
            return self.lst3str(lst[1:])
        else:
            return f'{self.lst1str(lst[0])} हजार {self.lst3str(lst[1:])}'

    def lst5str(self, lst):
        if lst == '00000':
            return ''
        elif lst[0] == '0':
            return self.lst4str(lst[1:])
        else:
            return f'{self.lst2str(lst[0])} हजार {self.lst3str(lst[1:])}'
    
    def lst_to_str(self, lst):
        length = len(lst)
        name_list = ['हज़ार', 'हज़ार','लाख','लाख', 'करोड़', 'करोड़', 'अरब', 'अरब', 'खरब', 'खरब', \
        'नील', 'नील', 'पद्म', 'पद्म', 'शंख', 'शंख', 'महाशंख', 'महाशंख', 'महाउपाध', 'महाउपाध', 'जलद', 
        'जलद', 'माध', 'माध', 'परार्ध', 'परार्ध', 'अंत', 'अंत', 'महा अंत', 'महा अंत', 'शिष्ट', 'शिष्ट', 'सिंघर', 'सिंघर', 
        'महा सिंघर', 'महा सिंघर', 'अदंत सिंघर', 'अदंत सिंघर']

        if lst == '0':
            return self.low_num_dict.get(lst)

        elif length == 1:
            return self.lst1str(lst)

        elif length == 2:
            return self.lst2str(lst)

        elif length == 3:
            return self.lst3str(lst)

        elif 42 > length > 3:# 35 23 548
            n = length - 3
            lst2 = lst[:n]
            return_str = ''
            while length > 3:
                if length%2 == 0:
                    if lst2[0] == '0':
                        length -= 1
                        lst2 = lst2[1:]
                        
                    else:
                        return_str = return_str + f'{self.lst1str(lst2[0])} {name_list[length-3]} '
                        length -= 1
                        lst2 = lst2[1:]
                else:
                    if lst2[0:2] == '00':
                        length -= 2
                        lst2 = lst2[2:]

                    else:
                        return_str = return_str + f'{self.lst2str(lst2[0:2])} {name_list[length-4]} '
                        length -= 2
                        lst2 = lst2[2:]
            
            return_str =  return_str + self.lst3str(lst[n:])
    
            return return_str
        else:
            return 'Number Too Long must be <= pow(10, 41)' 
                
    def to_currency(self):
        length = len(self.change_to_lst())
        lst1 = self.change_to_lst()[0]

        if length == 1:
            if lst1 == '1' :
                return 'एक रुपया'
            else:
                return f'{self.lst_to_str(lst1)} रूपये'
            
        elif length == 2:
            lst2 = self.change_to_lst()[1]
            if lst1 == '1' and lst2 == '01':
                return 'एक रुपया, एक पैसा'
            elif lst2 == '01':
                return f'{self.lst_to_str(lst1)} रूपये, एक पैसा'
            elif lst2 == '00':
                return f'{self.lst_to_str(lst1)} रूपये, शून्य पैसे'
            elif len(lst2) == 1:
                lst2 = lst2+'0'
                return f'{self.lst_to_str(lst1)} रूपये, {self.lst_to_str(lst2)} पैसे'
            else: 
                return f'{self.lst_to_str(lst1)} रूपये, {self.lst_to_str(lst2)} पैसे'
        
    def to_words(self):
        length = len(self.change_to_lst())
        lst1 = self.change_to_lst()[0]
        if length == 1:
            return self.lst_to_str(lst1)
        elif length == 2:
            lst2 = self.change_to_lst()[1]
            return f'{self.lst_to_str(lst1)} दशमलव {self.lst_to_str(lst2)}'
        elif length == 3:
            lst2 = self.change_to_lst()[1]
            lst3 = self.change_to_lst()[2]
            return f'{self.lst_to_str(lst1)} दशमलव {self.lst_to_str(lst2)} दशमलव {self.lst_to_str(lst3)}'
        else:
            return None


class Bill:
    item_name_list = []
    item_unit_list = []
    item_batch_list = []
    item_expiry_list = []
    item_rate_list = []
    item_type_list = []
    item_quantity_list = []
    item_counts = 0

    def __init__(self, customer_name, customer_address, bill_date, bill_number):
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.bill_date = bill_date
        self.bill_number = bill_number

    def add_item(self, item_details):
        # ['urea', 'bag', '123s3d', '12-6-2026', 300, 'P', 3]
        if len(item_details) == 7:
            self.item_name_list.append(item_details[0])
            self.item_unit_list.append(item_details[1])
            self.item_batch_list.append(item_details[2])
            self.item_expiry_list.append(item_details[3])
            self.item_rate_list.append(item_details[4])
            self.item_type_list.append(item_details[5])
            self.item_quantity_list.append(item_details[6])
            self.item_counts += 1
        else:
            print("Cannot add item to bill")
    
    def make_bill(self):
        if self.item_counts:
            item_name = self.convert_to_str(self.item_name_list, 30)
            batch_str = self.convert_to_str(self.item_batch_list, 11)
            serial_number_str = self.convert_to_str(range(1, self.item_counts + 1), 3)
            quantity_str = self.convert_to_str(self.item_quantity_list, 4)
            unit_str = self.convert_to_str(self.item_unit_list, 8)
            exp_str = self.convert_to_str(self.item_expiry_list, 10)
            rate_str = self.convert_to_str(self.item_rate_list, 4)
            sum_total_sale, total_sale_str = self.total_sale()
            sum_total_tax, comp_cgst_rate_str, comp_cgst_cost_str, comp_sgst_cost_str = self.total_cgst_sale()
            comp_total_relief_str = self.comp_total_relief(self.item_counts)
            comp_igst_rate_str = self.comp_total_relief(self.item_counts, 3)
            grand_total = sum_total_sale + sum_total_tax + sum_total_tax
            p = Num2wordshindi(grand_total)
            total_in_words = p.to_currency()

            if grand_total< 20000:
                self.add_in_templet(self.bill_date, 
                    self.bill_number,
                    self.customer_name,
                    self.customer_address,
                    item_name,
                    serial_number_str,
                    quantity_str,
                    unit_str,
                    batch_str,
                    exp_str,
                    rate_str,
                    total_sale_str, 
                    comp_total_relief_str, 
                    total_sale_str, 
                    comp_cgst_rate_str, 
                    comp_cgst_cost_str, 
                    comp_cgst_rate_str, 
                    comp_sgst_cost_str, 
                    comp_igst_rate_str, 
                    comp_total_relief_str,  
                    sum_total_sale, 
                    sum_total_tax, 
                    sum_total_tax, 
                    grand_total,  
                    total_in_words)
                print('[+]', self.bill_number, ' done')

            else:
                print("Total amount more than 20000")

        else:
            print('Please add items to bill')

    def convert_to_str(self, lst, avilable_length):
        final_str = ''
        for name in lst:
            blanks = ' '* (avilable_length - len(str(name)))*2 
            full_str = ''+ str(name) + blanks + '    '
            final_str = final_str + full_str
        return final_str

    def total_sale(self):
        if self.item_counts:
            total_amount = 0
            final_str = ''
            for i in range(self.item_counts):
                amount = self.item_quantity_list[i] * self.item_rate_list[i]
                blanks = ' '* (7 - len(str(amount)))*2 
                full_str = ''+ str(amount) + blanks+ '    '
                final_str = final_str + full_str
                total_amount += amount
        return total_amount, final_str

    def comp_str(self, s,n):
        blanks = ' '* (n - len(str(s)))*2 
        return ''+ str(s) + blanks+ '    '

    def total_cgst_sale(self):
        total_tax = 0.0
        total_rate_str = ''
        total_cgst_str = ''
        total_sgst_str = ''
        for i in range(self.item_counts):
            amount = self.item_rate_list[i] * self.item_quantity_list[i]
            if self.item_type_list[i] == 'P':
                total_rate_str += self.comp_str('9', 3)
                tax = amount * 9 / 100

            elif self.item_type_list[i] == "F":
                total_rate_str += self.comp_str('2.5', 3)
                tax = amount * 2.5 / 100
                
            else:
                total_rate_str += self.comp_str('0', 3)
                tax = 0
            
            total_tax += tax
            total_cgst_str += self.comp_str(str(tax), 8)
            total_sgst_str += self.comp_str(str(tax), 7)
        return total_tax, total_rate_str, total_cgst_str, total_sgst_str
                
    def comp_total_relief(self, m,n=6):
        comp = ''
        for i in range(m):
            comp += self.comp_str('-', 2*n)
        return comp
            
    def add_in_templet(self, b_date, bill_num, cust_name, cust_add, item_details, sr_num, quantity, unit, batch, expiry, rate, total_sale, total_dis, taxable_amt, crte, ck, sr, sk, ir, ik, taxable_amt_total, ct, st, gt, tmw ):
        tpl = DocxTemplate("mytamplet.docx")
        context = {
            'bill_number': bill_num,
            'given_date': b_date,
            'customer_name': cust_name,
            'customer_address': cust_add,
            'all_items_details': item_details,
            'serial_number': sr_num,
            'quantity': quantity,
            'item_unit': unit,
            'batch_number': batch,
            'expiry_date': expiry,
            'rate': rate,
            'total_sale': total_sale,
            'total_discount': total_dis,
            'taxable_amount': taxable_amt,
            'crate': crte,
            'ccost': ck,
            'srate': sr,
            'scost': sk,
            'irate': ir,
            'icost': ik,
            'taxable_amount_total': taxable_amt_total,
            'ctotal': ct,
            'stotal': st,
            'total_amount_in_words': tmw,
            'grand_total': gt
            }
        tpl.render(context)
        tpl.save(f'C://JBB//bills//{bill_num}.docx')









b = Bill('ramesh', 'dnx', '12-04-2024', 1)
b.add_item(['urea P', 'bag', '123s3d', '12-6-2026', 300, 'P', 3])
b.add_item(['urea2 S', 'bag', '123s3d', '12-6-2026', 300, 'S', 2])
b.add_item(['urea3 F', 'bag', '123s3d', '12-6-2026', 300, 'F', 2])

b.make_bill()

