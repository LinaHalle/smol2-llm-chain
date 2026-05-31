# API endpoints
from fastapi import FastAPI, UploadFile, File, HTTPException
from io import StringIO
import pandas as pd
from app.schemas import UploadResponse, AskInput, AskRequest
from pydantic import BaseModel
from app.data import save_dataframe, get_dataframe
from app.chain.pipeline import oraklet_pipeline
import logging

app = FastAPI()

class LLMRequest(BaseModel):
    id: int
    message: str

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/health")
def health():
    return {"status": "ok"}

# tar csv, laddar pandas, sparar i minnet, data-ingestion
@app.post("/data/upload")
def upload_csv(file: UploadFile = File(...)):

    logger.info("Upload endpoint called")

    if not file.filename.endswith(".csv"):
        logger.warning("Rejected file: not a CSV")
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )
    content = file.file.read()
    logger.info("File recieved")

    if not content:
        logger.warning("Rejected file: empty file")
        raise HTTPException(
            status_code=400,
            detail="File is empty"
        )
    
    if len(content) > 5 * 1024 * 1024:
        logger.warning("Rejected file: file too large")
        raise HTTPException(
            status_code=400,
            detail="File too large (max 5MB)"
        )
    
    try:
        decoded = content.decode("utf-8")
        df = pd.read_csv(StringIO(decoded))
        logger.info("CSV succesfully parsed")
    
    except UnicodeDecodeError:
        logger.error("Failed to decode file (not a UTF-8)")
        raise HTTPException(
            status_code=400,
            detail="File must be UTF-8 encoded"
        )
    
    save_dataframe(df)
    logger.info(f"Dataset saved: {len(df)} rows, {len(df.columns)} columns")

    response = UploadResponse(
        rows=len(df),
        columns=list(df.columns),
        dtypes={col: str(dtype) for col, dtype in df.dtypes.items()}
    )
    logger.info("Upload completed succesfully")
    return response

# analys-del
@app.get("/data/stats")
def get_stats():
    df = get_dataframe()

    if df is None:
        raise HTTPException(
            status_code=404,
            detail="No dataset uploaded yet"
        )
    stats = df.describe(include="all").fillna("").to_dict()
    
    return stats

class AskRequest(BaseModel):
    question: str


@app.post("/ai/ask")
def ai_ask(body: AskRequest):
    df = get_dataframe()

    if df is None:
        raise HTTPException(
            status_code=404,
            detail="No dataset uploaded yet"
        )

    dataset_summary = df.describe(include="all").fillna("").to_string()

    chain_input = AskInput(
        question=body.question,
        dataset_summary=dataset_summary
    )

    result = oraklet_pipeline.invoke(chain_input)

    return result
