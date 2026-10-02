from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import shutil


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)


# ============================================================
# IMPORT RAG PIPELINE
# ============================================================

from rag_pipeline import run_rag_pipeline


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="AI Coding Documentation Assistant",
    description="RAG-based coding documentation assistant",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# UPLOAD DIRECTORY
# ============================================================

UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)


# ============================================================
# REQUEST MODEL
# ============================================================

class QuestionRequest(BaseModel):
    question: str


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "status": "success",
        "message": "AI Coding Documentation Assistant API is running"
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/api/health")
def health():

    return {
        "status": "success",
        "message": "Backend is healthy"
    }


# ============================================================
# ASK
# ============================================================

@app.post("/api/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question is required."
        )

    try:

        result = run_rag_pipeline(question)

        return {
            "status": "success",
            "question": question,
            "answer": result.get("answer", ""),
            "sources": result.get("sources", [])
        }

    except Exception as e:

        return {
            "status": "error",
            "question": question,
            "message": str(e)
        }


# ============================================================
# UPLOAD DOCUMENT
# ============================================================

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):

    try:

        # ----------------------------------------------------
        # Check filename
        # ----------------------------------------------------

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No file selected."
            )


        # ----------------------------------------------------
        # Check extension
        # ----------------------------------------------------

        allowed_extensions = [
            ".pdf",
            ".txt",
            ".docx"
        ]

        extension = os.path.splitext(
            file.filename
        )[1].lower()


        if extension not in allowed_extensions:

            raise HTTPException(
                status_code=400,
                detail="Only PDF, TXT and DOCX files are allowed."
            )


        # ----------------------------------------------------
        # Save file
        # ----------------------------------------------------

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )


        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return {

            "status": "success",

            "message": "Document uploaded successfully",

            "filename": file.filename,

            "path": file_path

        }


    except HTTPException:

        raise


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )