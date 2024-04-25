from docx2pdf import convert
from PyPDF2 import PdfMerger, PdfReader
import os

def get_all_list():
    bills_dir = "C://JBB/bills"
    pdfs_dir = "C://JBB//pdfs"
    docx_list = [f.split(".")[0] for f in os.listdir(bills_dir) if f.endswith(".docx")]
    pdf_list = [f.split(".")[0] for f in os.listdir(pdfs_dir) if f.endswith(".pdf")]
    return docx_list, pdf_list

def my_sort(start, end, lst):
    return [str(i) for i in range(start, end+1) if str(i) in lst]

def convert_to_pdf(i):
    if not os.path.exists(f"C://JBB//pdfs/{str(i)}.pdf"):
        try:
            convert(f"C://JBB//bills/"+str(i)+".docx", f"C://JBB//pdfs/{str(i)}.pdf")
            print(f"{i} converted to PDF")
        except Exception as e:
            print(f"!!!! Error in Converting {i} \n Error {e}")
    else:
        print(f'Pdf found {i}')



def my_merger(lst, from_num, to_num):
    merger = PdfMerger()
    print(f"Merging {from_num} to {to_num}")
    for num in lst:
        try:
            merger.append(PdfReader(f"C://JBB//pdfs/{num}.pdf", 'rb'))
            print(num, end=" done ")
        except Exception as e:
            print(f"*** Error in Merging {num} \n Error {e}")
    merger.write(f"C://JBB//merged_pdfs/{from_num}to{to_num}.pdf")

def docs_to_pdf_main(from_num, to_num):
    docxs, pdfs = get_all_list()
    docxsm = my_sort(int(from_num), int(to_num), docxs)
    pdfsm = my_sort(int(from_num), int(to_num), pdfs)

    for i in docxsm:
        convert_to_pdf(i)

    # Merge PDFs (Existing code)
    my_merger(docxsm, from_num, to_num)

    x = input('\n Operation completed successfully!!!!!!!!')

if __name__ == "__main__":
    docs_to_pdf_main(2324379, 2324608)
