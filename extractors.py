import os
from docx import Document
import fitz  # PyMuPDF
from PIL import Image
import pytesseract

# Point pytesseract to the installed location
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# For .doc (old Word format)
import win32com.client as win32

def extract_docx_text(path):
    """Extract text from .docx file"""
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)
def extract_doc_text(path):
    """Extract text from .doc (old Word format) using Word COM automation"""
    import os, win32com.client as win32

    abs_path = os.path.abspath(path)  # convert to full absolute path
    print("🔎 Trying to open DOC file at:", abs_path)  # debug log

    word = win32.Dispatch("Word.Application")
    word.visible = False
    try:
        doc = word.Documents.Open(abs_path)
        text = doc.Content.Text
        doc.Close()
        return text
    finally:
        word.Quit()


def extract_pdf_text(path):
    """Extract text from PDF using PyMuPDF"""
    doc = fitz.open(path)
    return "\n".join([page.get_text("text") for page in doc])

def extract_image_text(path):
    """Extract text from images using OCR (pytesseract)"""
    img = Image.open(path)
    return pytesseract.image_to_string(img)

def extract_text_from_file(path):
    """Route extraction based on file extension"""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_pdf_text(path)
    elif ext == ".docx":
        return extract_docx_text(path)
    elif ext == ".doc":
        return extract_doc_text(path)
    elif ext in (".jpg", ".jpeg", ".png"):
        return extract_image_text(path)
    else:
        return f"❌ Unsupported file type: {ext}"