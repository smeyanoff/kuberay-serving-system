import os
import pickle

from ray import serve
from ray.serve.drivers import DAGDriver
from ray.serve.deployment_graph import InputNode
from ray.serve.http_adapters import json_request
from dotenv import load_dotenv
import xgboost

from src.data_models import DataModel, ResponseModel

load_dotenv()


@serve.deployment
class ModelC:
    def __init__(self, model_path: str) -> None:
        with open(model_path, "rb") as file:
            self.model: xgboost.Booster = pickle.load(file)

    def get_unswer(self, data_string: str) -> ResponseModel:
        data = DataModel.from_string(data_string)
        prediction = self.model.predict(data.values_to_dmatrix())[0]

        return ResponseModel(
            model_name="D_24_MODEL_V_1", model_unswer=prediction, model_data=data.dict()
        )


model = ModelC.bind(os.environ.get("XGBOOST_D24_W"))
with InputNode() as data_string:
    unswer = model.get_unswer.bind(data_string)

app = DAGDriver.options(route_prefix="/D_24_MODEL").bind(
    unswer, http_adapter=json_request
)
