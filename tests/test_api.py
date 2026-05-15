import allure
import requests
import pytest
from app.model import Location as DBLocation


@allure.feature("Тестирование бэкенда")
class TestApi:
    @allure.story("1: Успешное отображение локации (проверка на стороне API)")
    @pytest.mark.parametrize(
        "country, zip_code, expected_city",
        [
            ("ru", "101000", "Москва"),
            ("ru", "183000", "Мурманск"),
            ("ru", "450000", "Уфа"),
            ("us", "90210", "Beverly Hills"),
        ],
        ids=["Москва", "Мурманск", "Уфа", "Beverly Hills"],
    )
    def test_external_zip_api(self, country, zip_code, expected_city):
        url = f"https://api.zippopotam.us/{country}/{zip_code}"
        response = requests.get(url)

        assert response.status_code == 200
        data = response.json()
        assert data["places"][0]["place name"] == expected_city

    @allure.story("2: Успешное сохранение локации")
    def test_success_save(self, api_run, db_session, make_payload):
        payload = make_payload(city="Москва", country="ru", zip="101000")
        with allure.step("Отправка запроса на сохранение"):
            response = api_run.post("/api/save_location", json=payload)
            assert response.status_code == 200

        with allure.step("Проверка названия города через обращение к БД"):
            record = (
                db_session.query(DBLocation)
                .filter(DBLocation.zip == payload["zip"])
                .first()
            )
            assert record is not None, "запись не дошла до БД"

            allure.attach(f"значение: {record.city}", name="DB content")
            assert record.city == "Москва", f"в базе {record.city}"

    @allure.story("3: Проверка обрезки данных")
    def test_data_loss(self, api_run, db_session, make_payload):
        payload = make_payload(
            city="Мурманск", country="ru", zip="183000", data_loss=True
        )

        with allure.step("Отправка запроса с багом"):
            response = api_run.post("/api/save_location", json=payload)
            assert response.status_code == 200

        with allure.step("Проверка обрезки через обращение к БД"):
            record = (
                db_session.query(DBLocation)
                .filter(DBLocation.zip == payload["zip"])
                .first()
            )

            assert record is not None, "запись не дошла до бд"

            allure.attach(f"значение: {record.city}", name="DB content")
            assert record.city == "Мур", f"в базе {record.city}"

    @allure.story("4: Проверка дублирования записей")
    def test_duplicate(self, api_run, db_session, make_payload):
        payload = make_payload(
            city="New York City", country="us", zip="10101", integrity=True
        )

        with allure.step("Первый POST данных, ожидаем код 200"):
            response = api_run.post("api/save_location", json=payload)
            assert response.status_code == 200
        with allure.step("Повторная отправка идентичных данных, ожидаем код 500"):
            response2 = api_run.post("api/save_location", json=payload)
            assert (
                response2.status_code == 409
            ), f"сервер не выдал код 409 на дубликат, получили {response2.status_code}"

        with allure.step("Проверка данных в БД"):
            count = (
                db_session.query(DBLocation)
                .filter(DBLocation.zip == payload["zip"])
                .count()
            )

            allure.attach(str(count), name="кол-во записей в БД по индексу")
            assert count == 1, f"в базе {count} записей вместо 1"

    @allure.story("5: Проверка медленного ответа БД")
    def test_slow_db(self, api_run, db_session, make_payload):
        payload = make_payload(
            city="New York City", country="us", zip="10001", slow_db=True
        )

        with allure.step("Отправка данных, ждем 200"):
            response = api_run.post("api/save_location", json=payload)
            assert response.status_code == 200

        with allure.step("Проверяем появилась ли запись в БД"):
            record = (
                db_session.query(DBLocation)
                .filter(DBLocation.zip == payload["zip"])
                .first()
            )

            assert record is not None, "запись не дошла до бд"

            allure.attach(f"значение: {record.city}", name="DB content")
            assert record.city == "New York City"

    @allure.story("7: Валидация пустого ввода")
    @pytest.mark.parametrize(
        "country, zip_code, city",
        [("", "", ""), (" ", " ", " "), ("\n", "\n", "\n")],
        ids=["empty_strings", "spaces", "newlines"],
    )
    def test_empty_field(self, api_run, make_payload, country, zip_code, city):
        payload = make_payload(city=city, country=country, zip=zip_code)

        with allure.step("Отправляем запрос с пустыми полями, ждем 400"):
            response = api_run.post("api/save_location", json=payload)
            assert (
                response.status_code == 400
            ), f"ожидали 400, получили {response.status_code}"
            assert response.json() == {"detail": "Empty fields"}

    @allure.story("8: Некорректный ZIP")
    def test_incorrect_zip(self):
        url = f"https://api.zippopotam.us/ru/123"
        response = requests.get(url)

        assert response.status_code == 404

    @allure.story("9: Очистка данных перед тестом")
    @allure.description("Технический тест для проверки эндпоинта самоочистки БД")
    def test_verify_clean_db_logic(self, api_run, db_session, make_payload):
        payload = make_payload()
        api_run.post("/api/save_location", json=payload)

        record_before = (
            db_session.query(DBLocation).filter_by(zip=payload["zip"]).first()
        )
        assert record_before is not None

        response = api_run.delete("/api/danger/clear_db")
        assert response.status_code == 200

        db_session.expire_all()
        record_after = (
            db_session.query(DBLocation).filter_by(zip=payload["zip"]).first()
        )
        assert record_after is None
