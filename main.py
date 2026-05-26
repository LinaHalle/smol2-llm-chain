from fastapi import FastAPI, UploadFile, File
import pandas as pd
from io import StringIO
from app.schemas import UploadResponse
from pydantic import BaseModel
from llm.llm import TicketInput, ticket_pipeline

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
    content = file.file.read().ddecode("utf-8")
    df = pd.read_csv(StringIO(content))

    response = UploadResponse(
        rows=len(df),
        columns=list(df.columns),
        dtypes={col: str(dtype) for col, dtype in df.dtypes.items()}
    )

    return response