import json

import requests
import streamlit as st

from src.data_models import DataModel

FILE_PATH = "data/sample.json"
API_URL = "http://94.142.138.188:8000"


# Функция для открытия json файла
def load_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


# Функция для отправки данных на сервис Ray Serve
def send_data_to_serve(url, data):
    dm = DataModel(**data)
    response = requests.get(f"{API_URL}/{url}", json=dm.json().replace("NaN", "None"))
    result = response.json()
    return {
        "Код ответа HTTP-статуса": response.status_code,
        "Ответ модели": round(result["model_unswer"], 5),
    }  # Вернуть ответ от модели


# Json для примера
init_json = load_json(FILE_PATH)

# Заголовок и описание интерфейса
st.title("Демострация проекта BASA")
st.write("Введите значения для полей и отправьте для предсказания на выбранную модель.")

# Поля ввода для важных столбцов с ограничениями и параметрами по умолчанию
app_info_6_value = st.number_input(
    "Введите значение фичи №1 (от -1 до 4)", value=0, min_value=-1, max_value=4
)
type_value = st.number_input(
    "Введите значение фичи №2 (от 0 до 39)", value=0, min_value=0, max_value=39
)
e_ch_vars_3_value = st.number_input(
    "Введите значение фичи №3 (от 0 до 72)", value=0, min_value=0, max_value=72
)
app_info_9_value = st.number_input(
    "Введите значение фичи №4 (от 0 до 100000)", value=0, min_value=0, max_value=1000000
)
e_ch_vars_85_value = st.number_input(
    "Введите значение фичи №5 (от 0 до 150000)", value=0, min_value=0, max_value=72
)
e_ch_vars_111_value = st.number_input(
    "Введите значение фичи №6 (от 0 до 200000)", value=0, min_value=0, max_value=2936017
)


st.write(
    "Выбор модели предсказывающая дефолт на 24 месяц (Model_D24) или на 36 месяц (Model_D36)"
)

model_choice = st.selectbox("Выберите модель", ["Model_D24", "Model_D36"])

# Кнопка для отправки данных на модель
if st.button("Предсказать"):
    # Проверка, что введены числовые значения
    try:
        # Создание словаря из введенных значений
        data = {
            "type": int(type_value),
            "app_info_6": float(app_info_6_value),
            "app_info_9": float(app_info_9_value),
            "e_ch_vars_111": float(e_ch_vars_111_value),
            "e_ch_vars_3": float(e_ch_vars_3_value),
            "e_ch_vars_85": float(e_ch_vars_85_value),
        }

        # на полученные значения
        for key, value in data.items():
            init_json[key] = value

    except ValueError:
        st.warning("Пожалуйста, введите числовые значения в поля.")

    # Определение адрес в зависимости от выбранной модели
    if model_choice == "Model_D24":
        model_uri = "D_24_MODEL"
    elif model_choice == "Model_D36":
        model_uri = "D_36_MODEL"
    else:
        st.warning("Выберите модель для отправки")

    # Отправка данных на модель
    result = send_data_to_serve(model_uri, init_json)

    # Отображение результата от модели
    st.write("Результат от модели:")
    st.write(result)  # Отображение результата от модели
