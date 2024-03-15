import PyPDF2

def count_pdf_pages(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        return num_pages


def order_cost(pages,type,copies):
    if type == 'Single Side':
        return float(float(pages) * 1 * float(copies))
    elif type == 'Double Side':
        return float(float(pages) * 0.5 * float(copies))
    elif type == 'Two pages':
        return float(float(pages) * 0.25 * float(copies))
    else:
        return float(pages)
    
    

