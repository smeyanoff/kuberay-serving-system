from pydantic import BaseModel
from src.data_models import DataModel


class RequestModel(BaseModel):
    model_name: str
    data_model: DataModel
