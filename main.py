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

@app.post("/llm")
def llm_route(body: LLMRequest):
    incoming_ticket = TicketInput(
        customer_id=body.id,
        message=body.message
    )
    return ticket_pipeline.invoke(incoming_ticket)

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