from pydantic import BaseModel

class UploadResponse(BaseModel):
    rows: int
    columns: list[str]
    dtypes: dict[str, str]

class AskRequest(BaseModel):
    question:str

class PromptBuilderInput(BaseModel):
    question: str
    dataset_summary: str

class PromptBuilderOutput(BaseModel):
    prompt: str

class LLMRunnerOutput(BaseModel):
    raw_response: str

class AskResponse(BaseModel):
    question: str
    answer: str
    model: str