from pydantic import BaseModel
from typing import Optional

class UploadResponse(BaseModel):
    rows: int
    columns: list[str]
    dtypes: dict[str, str]

class AskRequest(BaseModel):
    question:str

class AskInput(BaseModel):
    question: str
    dataset_summary: str

class PromptBuilderInput(BaseModel):
    question: str
    dataset_summary: str

class PromptBuilderOutput(BaseModel):
    prompt: str
    question: str

class LLMRunnerOutput(BaseModel):
    raw_response: str
    question: str

class AskResponse(BaseModel):
    question: str
    answer: str
    model: str
