from pydantic import BaseModel, Field


class PDFPage(BaseModel):
    page_number: int = Field(ge=1)
    text: str


class PDFDocument(BaseModel):
    filename: str
    pages: list[PDFPage]
