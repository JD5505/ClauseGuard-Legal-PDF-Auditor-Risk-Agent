import pymupdf
from Schema.document_check import PDFPage, PDFDocument
def extract_pdf(pdf_bytes: bytes, filename: str) -> PDFDocument:

    document = pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text()

        pages.append(
            PDFPage(
                page_number=page_number,
                text=text
            )
        )

    document.close()

    return PDFDocument(
        filename=filename,
        pages=pages
    )