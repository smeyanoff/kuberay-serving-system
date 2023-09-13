from ray import serve

from src.data_models import DataModel


@serve.deployment
class DataPrepare:

    def __call__(self, data_json: dict) -> DataModel:
        data = DataModel(data_json)
        return DataModel(data["val1"]+1, data["val2"])
