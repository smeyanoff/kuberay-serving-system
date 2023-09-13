from pydantic import BaseModel


class ResponseModel(BaseModel):
    model_name: str
    model_unswer: float
    model_data: dict
