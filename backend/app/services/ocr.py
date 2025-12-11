import fitz  # PyMuPDF
import os
import easyocr
from pdf2image import convert_from_path

reader = easyocr.Reader(['en'])


# ----------------------------------------
# 1. CHECK IF PDF HAS EXTRACTABLE TEXT
# ----------------------------------------
def extract_pdf_text_raw(path: str):
    """
    Tries to extract digital text from PDF (no OCR).
    If fails → return empty string.
    """
    text = ""
    doc = fitz.open(path)
    for page in doc:
        page_text = page.get_text()
        if page_text.strip():
            text += page_text + "\n"
    doc.close()
    return text


# ----------------------------------------
# 2. FULL OCR PIPELINE
# ----------------------------------------
def ocr_image(path: str):
    """
    OCR for JPG/PNG files.
    """
    result = reader.readtext(path)
    text = " ".join([r[1] for r in result])
    return text


def ocr_pdf(path: str):
    """
    OCR PDF page-by-page (slowest fallback).
    """
    pages = convert_from_path(path)
    final = ""
    for page in pages:
        result = reader.readtext(page)
        page_text = " ".join([r[1] for r in result])
        final += page_text + "\n"
    return final


# ----------------------------------------
# 3. MAIN EXTRACT FUNCTION
# ----------------------------------------
def extract_text(path: str):
    """
    Unified function → handles both PDF & images.

    Priority:
    1. If PDF → try raw text extraction.
    2. If empty → OCR the PDF.
    3. If image → OCR image.
    """
    ext = os.path.splitext(path)[1].lower()

    # PDF branch
    if ext == ".pdf":
        raw = extract_pdf_text_raw(path)
        if raw.strip():
            return raw
        else:
            return ocr_pdf(path)

    # Image branch
    return ocr_image(path)
