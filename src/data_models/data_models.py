from pydantic import BaseModel


class DataModel(BaseModel):
    val1: int
    val2: str
