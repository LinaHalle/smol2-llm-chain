# API endpoints
from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from app.schemas import UploadResponse, AskInput, AskRequest
from pydantic import BaseModel
from app.data import save_dataframe, get_dataframe
from app.chain.pipeline import oraklet_pipeline

app = FastAPI()

class LLMRequest(BaseModel):
    id: int
    message: str

class AIQueryRequest(BaseModel):
    message: str

# tar csv, laddar pandas, sparar i minnet, data-ingestion
@app.post("/data/upload")
def upload_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    save_dataframe(df)

    response = UploadResponse(
        rows=len(df),
        columns=list(df.columns),
        dtypes={col: str(dtype) for col, dtype in df.dtypes.items()}
    )
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
