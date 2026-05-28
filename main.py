# API endpoints
from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from app.schemas import UploadResponse
from pydantic import BaseModel
from llm.llm import TicketInput, ticket_pipeline
from app.data import save_dataframe, get_dataframe

app = FastAPI()

class LLMRequest(BaseModel):
    id: int
    message: str

class AIQueryRequest(BaseModel):
    message: str

# tar input, kör pipeline, returnerar resultat, AI-delen
@app.post("/llm")
def llm_route(body: LLMRequest):
    incoming_ticket = TicketInput(
        customer_id=body.id,
        message=body.message
    )
    return ticket_pipeline.invoke(incoming_ticket)

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

@app.post("/ai/query")
def ai_query(body: AIQueryRequest):
    df = get_dataframe()

    if df is None:
        raise HTTPException(
            status_code=404,
            detail="No dataset uploaded yet"
        )
    
    sample_data = df.head(10).to_string(index=False)

    prompt = f"""
You are a data analyst AI.

Dataset:
{sample_data}

User question:
{body.message}

Answer clearly and based on the dataset.AIQueryRequest.
"""
    ticket = TicketInput(
        customer_id=0,
        message=prompt
    )

    result = ticket_pipeline.invoke(ticket)
    return result
