import fitz
import pytesseract
from PIL import Image
import io

def extract_text(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    
    for page in doc:
        page_text = page.get_text()
        
        # If page has very little text, try OCR
        if len(page_text.strip()) < 50:
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            try:
                ocr_text = pytesseract.image_to_string(img)
                text += ocr_text + "\n"
            except pytesseract.TesseractNotFoundError:
                 # Fallback if tesseract is not installed on system
                 text += page_text
        else:
            text += page_text
            
    return text.strip()
