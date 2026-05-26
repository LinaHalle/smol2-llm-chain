from pydantic import BaseModel

class Uploadresponse(BaseModel):
    rows: int
    columns: list[str]
    dtypes: dict[str, str]