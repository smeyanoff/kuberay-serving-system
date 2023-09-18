import os

from ray import serve, get
from ray.serve.handle import RayServeDeploymentHandle
from ray.serve.drivers import DAGDriver
from ray.serve.deployment_graph import InputNode
from ray.serve.http_adapters import json_request
from dotenv import load_dotenv

from src.data_models import DataModel, ResponseModel
from src.models.model_a import DataPrepare

load_dotenv()


@serve.deployment
class ModelA:
    def __init__(self, 
                 model_path: str, 
                 data_prepare_class: RayServeDeploymentHandle) -> None:
        self.model = model_path
        self.data_prepare_class = data_prepare_class

    async def get_unswer(self, data_json: dict) -> ResponseModel:
        data = DataModel(**data_json)
        prepared_json_ref = await self.data_prepare_class.remote(data)
        prepared_json = await prepared_json_ref
        return ResponseModel(model_name = "model_A", 
                             model_unswer = 1.0, 
                             model_data = prepared_json)


data_prepare_class = DataPrepare.bind()
model = ModelA.bind(os.environ.get("MODEL_A_WEIGHTS"), data_prepare_class)

with InputNode() as data_json:
    unswer = model.get_unswer.bind(data_json)

app = DAGDriver.options(route_prefix="/model-A").bind(unswer, http_adapter=json_request)
