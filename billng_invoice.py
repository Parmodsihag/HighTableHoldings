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
        

    
def add_in_templet(b_date, bill_num, cust_name, cust_add, item_details, sr_num, quantity, unit, batch, expiry, rate, total_sale, total_dis, taxable_amt, crte, ck, sr, sk, ir, ik, taxable_amt_total, ct, st, gt, tmw ):
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
    tpl.save(f'bills/{bill_num}.docx')

def comp_this(n, lst):
    comp = ''
    for s in lst:
        comp += comp_str(str(s), n)
    return comp


def comp_str(s, n):
    sl = len(s)
    blanks = ' '*(n-sl)*2
    fullstr = ''+ s + blanks +'    '
    return fullstr

def comp_sr_number(m):
    comp = ''
    for i in range(m):
        comp += comp_str(str(i+1), 3)
    return comp

def comp_total_relief(m,n=6):
    comp = ''
    for i in range(m):
        cs = comp_str('-', 2*n)
        comp = comp+cs
    return comp

def comp_cgst_rate(*args):
    comp = ''
    for s in args:
        if s == "P":
            comp += comp_str('9', 3)
        elif s == "F":
            comp += comp_str('2.5', 3)
        else:
            comp += comp_str('0', 3)
    return comp

def comp_cgst_cost(l, item_type_list, rate_list, quanity_list, n ):
    comp = ''
    total_amt = 0
    for i in range(l):
        item_type = item_type_list[i]
        rate = rate_list[i]
        quantity = quanity_list[i]
        total = rate * quantity
        if item_type == "P":
            tax = total * 9/100
        elif item_type == 'F':
            tax = total * 2.5/100
        else:
            tax = 0
        comp += comp_str(str(tax), n)
        total_amt  += round(tax)
    return comp, total_amt

def comp_total_sale(l, rate_list, quanity_list):
    comp = ''
    total = 0
    for i in range(l):
        amt = int(rate_list[i]) * int(quanity_list[i])
        comp += comp_str(str(amt), 7)
        total += amt
    return comp, total 

'''
comp_det 30
comp_bat 11
comp_quantity 4
comp_unit 8
comp_exp 10
comp_rate 4
comp_total_sale 7:
'''

def make_bill(
        bill_number,
        bill_date,
        customer_name,
        customer_address,
        name_list, 
        unit_list,
        batch_list, 
        exp_list,
        rate_list,
        type_list,
        quanity_list
    ):
    total_sr_num = len(name_list)
    details = comp_this(30, name_list)
    comp_batch_str = comp_this(11,batch_list)
    total_sr_number_str = comp_sr_number(total_sr_num)
    comp_quantity_str = comp_this(4, quanity_list)
    comp_unit_str = comp_this(8, unit_list)
    comp_exp_str = comp_this(10, exp_list)
    comp_rate_str = comp_this(4, rate_list)
    comp_total_sale_str, sum_total_sale = comp_total_sale(total_sr_num, rate_list, quanity_list)
    comp_cgst_cost_str, sum_total_tax = comp_cgst_cost(total_sr_num, type_list, rate_list, quanity_list, 8)
    comp_sgst_cost_str, sum_total_tax = comp_cgst_cost(total_sr_num, type_list, rate_list, quanity_list, 7)
    comp_total_relief_str = comp_total_relief(total_sr_num)
    comp_igst_rate_str = comp_total_relief(total_sr_num, n=3)
    comp_cgst_rate_str = comp_cgst_rate(type_list)
    grand_total = sum_total_sale + sum_total_tax + sum_total_tax
    p = Num2wordshindi(grand_total)
    total_in_words = p.to_currency()

    if bill_number and bill_date and customer_name and customer_address and grand_total < 20000:
        add_in_templet(bill_date, bill_number, customer_name, customer_address, details, total_sr_number_str, comp_quantity_str, comp_unit_str, comp_batch_str, comp_exp_str, comp_rate_str, comp_total_sale_str, comp_total_relief_str, comp_total_sale_str, comp_cgst_rate_str, comp_cgst_cost_str, comp_cgst_rate_str, comp_sgst_cost_str, comp_igst_rate_str, comp_total_relief_str,  sum_total_sale, sum_total_tax, sum_total_tax, grand_total, total_in_words)
        print(bill_number, ' done')
    else:
        print('please fill OR AMOUNT SHOULD BE LESS THAN 20000')


