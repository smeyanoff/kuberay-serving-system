import time

from ray import serve

from src.data_models import DataModel


@serve.deployment
class DataPrepare:
    def __call__(self, data: DataModel) -> DataModel:
        time.sleep(1)
        return DataModel(val1 = data.val1 + 1, val2 = data.val2)
