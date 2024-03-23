
from docx2pdf import convert
from PyPDF2 import PdfMerger, PdfReader
import os

def get_all_list():
    lst = os.listdir("bills")
    lst2 = os.listdir("pdfs")
    docx_list = []
    num_list = []
    for i in lst:
        if i.endswith(".docx"):
            first = i.split(".")[0]
            docx_list.append(first)
    for i in lst2:
        if i.endswith(".pdf"):
            first = i.split(".")[0]
            num_list.append(first)
            
    # print(docx_list, num_list)
    return docx_list, num_list
    


def my_sort(strt, nd, lst):
    res = []
    for i in range(strt, nd+1):
        if str(i) in lst:
            res.append(str(i))
    return res

def my_converter(docx_list, num_list):
    for i in docx_list:
        if i in num_list:
            print(i+" Pdf Found")
        else:
            print(i)
            try:
                convert(f"bills/"+str(i)+".docx", f"pdfs/{str(i)}.pdf")
                
            except Exception as e:
                print(f"!!!! Error in Converting {i} \n Error {e}")

def my_merger(lst, from_num, to_num):
    merged_object = PdfMerger()
    print(f"Merging {from_num} to {to_num}")
    for num in lst:
        try:
            merged_object.append(PdfReader( "pdfs/"+num+ '.pdf', 'rb'))
            print(num, end=" done ")
        except Exception as e:
            print(f"*** Error in Merging {num} \n Error {e}")
    merged_name = "merged_pdfs/"+str(from_num) + "to" + str(to_num)+".pdf"
    merged_object.write(merged_name)

def docs_to_pdf_main(from_num, to_num):
    docxs, pdfs = get_all_list()
    docxsm = my_sort(int(from_num), int(to_num), docxs)
    pdfsm = my_sort(int(from_num), int(to_num), pdfs)
    
    my_converter(docxsm, pdfsm)
    
    my_merger(docxsm, from_num, to_num)
    
    
    x = input('\n Operation completed successfully!!!!!!!!')


docs_to_pdf_main(101, 130)