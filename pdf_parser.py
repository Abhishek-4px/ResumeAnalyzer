import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF file using PyMuPDF
    Args:
        pdf_path: Path to the PDF file
    Returns:
        Extracted text as string
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
        
        doc.close()
        return text.strip()
    
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_text_from_bytes(pdf_bytes):
    """
    Extract text from PDF bytes (for uploaded files)
    Args:
        pdf_bytes: PDF file as bytes
    Returns:
        Extracted text as string
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
        
        doc.close()
        return text.strip()
    
    except Exception as e:
        raise Exception(f"Error extracting text from PDF bytes: {str(e)}")
