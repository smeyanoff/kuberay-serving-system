import json
import random

from locust import HttpUser, constant_throughput, task

from src.data_models import DataModel

FILE_PATH = "data/sample.json"


# Функция для открытия json файла
def load_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    if "type" in data:
        data["type"] = random.randint(0, 39)
    if "app_info_6" in  data:
        data["app_info_6" ] = random.randint(-1, 4)
    if "app_info_9" in data:
        data["app_info_9"] = random.randint(0, 1000000)
    if "e_ch_vars_111" in  data:
        data["e_ch_vars_111"] = random.randint(0, 2000000)
    if "e_ch_vars_3" in  data:
        data["e_ch_vars_3"] = random.randint(0, 1500000)
    if "e_ch_vars_85" in  data:
        data["e_ch_vars_85"] = random.randint(0, 72)
    return data


test_application = load_json(FILE_PATH)
dm = DataModel(**test_application)


class MyUser(HttpUser):
    wait_time = constant_throughput(1)

    @task
    def predict_model1(self):
        self.client.get(
            "/D_24_MODEL",
            json=dm.json().replace("NaN", "None").replace("null", "None"),
            timeout=1,
        )

    @task
    def predict_model2(self):
        self.client.get(
            "/D_36_MODEL",
            json=dm.json().replace("NaN", "None").replace("null", "None"),
            timeout=1,
        )
