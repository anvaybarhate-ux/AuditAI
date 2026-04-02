from fastapi import APIRouter, UploadFile, File, Form, Depends  
from sqlalchemy.orm import Session  
from db.database import get_db, Document  
from utils.pdf_parser import extract_text  

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    POST /api/upload
    Accepts a PDF, CSV, or Excel file.
    Extracts text content and saves a Document record to the DB.
    Returns: document_id, filename, extracted_text, preview
    """
    print(f"📁 Uploading: {file.filename}")

    
    file_bytes = await file.read()

    if len(file_bytes) == 0:
        return {"success": False, "error": "Empty file uploaded"}

    if len(file_bytes) > 10 * 1024 * 1024:  
        return {"success": False, "error": "File too large. Maximum size is 10MB"}

    
    text = extract_text(file_bytes, str(file.filename or "unknown"))
    if not text.strip():
        return {"success": False, "error": "Could not extract text from this file. Please use PDF, CSV, or Excel."}

    
    doc = Document(filename=file.filename, user_id=user_id)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    print(f"   ✅ Extracted {len(text)} characters from {file.filename} (doc_id={doc.id})")

    return {
        "success":        True,
        "document_id":    doc.id,
        "filename":       file.filename,
        "extracted_text": text,
        "preview":        text[:400],
        "char_count":     len(text),
    }