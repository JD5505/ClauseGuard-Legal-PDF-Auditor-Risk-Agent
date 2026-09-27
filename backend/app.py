from fastapi import FastAPI, UploadFile, File, Form
from Schema.chat_data import CheckInput
from model.inference import invoke_agent
from uuid import UUID
from VectorDB.pdf_loader import extract_pdf
from VectorDB.chunking import chunk_pdf
from VectorDB.vector_embedding import create_vector_store
from fastapi.responses import JSONResponse
app = FastAPI(
    title = "ClauseGuard: Legal PDF Auditor & Risk Agent",
    version = "0.1.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to ClauseGuard: Legal PDF Auditor & Risk Agent"
    }

@app.get("/health")
def health():
    return {
        "status": "Running",
        "version": "0.1.0"
    }

@app.post("/document")
async def upload_pdf(file: UploadFile = File(...), thread_id: UUID = Form(...)):

    pdf_bytes = await file.read()

    document = extract_pdf(
        pdf_bytes,
        file.filename
    )
    chunked = chunk_pdf(document)
    create_vector_store(chunked)
    return True

@app.post("/invoke")
def infer_chat(data: CheckInput):
    output = invoke_agent(data.user_msg, data.thread_id)

    return JSONResponse(status_code=200, content={"message": output})