from langchain_text_splitters import RecursiveCharacterTextSplitter
from Schema.document_check import PDFDocument

def chunk_pdf(pdf: PDFDocument):
    chunker = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 150
    )

    chunks = []

    for page in pdf.pages:
        if not page.text.strip():
            continue
        
        page_chunks = chunker.create_documents(
            texts = [page.text],
            metadatas=[
                {
                    "filename": pdf.filename,
                    "page_number": page.page_number
                }
            ]
        )

    chunks.extend(page_chunks)
    return chunks