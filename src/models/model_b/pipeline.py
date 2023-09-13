import os

from ray import serve
from ray.serve.drivers import DAGDriver
from ray.serve.deployment_graph import InputNode
from ray.serve.http_adapters import json_request
from dotenv import load_dotenv

from src.data_models import DataModel, ResponseModel

load_dotenv("configs/.env")


@serve.deployment
class ModelB:

    def __init__(self, model_path: str) -> None:
        self.model = model_path
    
    def get_unswer(self, data_json: dict) -> ResponseModel:
        data = DataModel(data_json)
        return ResponseModel("model_B", 1., data)

model = ModelB.bind(os.environ.get("MODEL_B_WEIGHTS"))

with InputNode() as data_json:  
    unswer = model.get_unswer.bind(data_json)

app = (DAGDriver.options(route_prefix="/model-B")
                .bind(unswer, http_adapter=json_request))