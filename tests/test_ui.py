import allure


@allure.feature("Тестирование фронтенда")
class TestUI:
    @allure.story("1: Успешное отображение локации")
    def test_city_field(self, main_page):
        with allure.step("Заполнение формы: ru, 450000"):
            main_page.fill_form("ru", "450000")
        with allure.step("Проверка автоопределения города"):
            city = main_page.city_detect()
            assert city == "Уфа"

    @allure.story("2: Успешное сохранение локации")
    def test_success_save(self, main_page):

        zip_value = "101000"
        with allure.step(f"Поиск города по индексу {zip_value}"):
            main_page.fill_form("ru", zip_value)
            main_page.city_detect()
        with allure.step("Нажатие кнопки сохранения"):
            main_page.click_save()
        with allure.step("Проверка статус-сообщения"):
            message = main_page.get_status()

            assert "Saved" in message
            assert zip_value in message, f"get {message}"

    @allure.story("4: Проверка дублирования записей")
    def test_duplicate(self, main_page):
        with allure.step("Активация бага дубликатов"):
            main_page.toggle_bug("duplicates")

        with allure.step("Первичное сохранение"):
            main_page.fill_form("ru", "101000")
            main_page.city_detect()
            main_page.click_save()
            main_page.get_status(expected="Saved")

        with allure.step("Повторное нажатие кнопки сохранения"):
            main_page.click_save()
            message = main_page.get_status(expected="Error")
            assert "Error" in message

    @allure.story("5: Проверка медленного ответа БД")
    def test_slow_db_response(self, main_page):
        with allure.step("Активация бага медленного ответа БД"):
            main_page.toggle_bug("slow_db")

        zip_value = "10101"
        with allure.step("Ввод индекса и города"):
            main_page.fill_form("us", zip_value)
            main_page.city_detect()
        with allure.step("Нажатие кнопки сохранения в БД и ожидание"):
            main_page.click_save()
            message = main_page.get_status(timeout=50)
            assert "Saved" in message
            assert zip_value in message, f"get {message}"

    @allure.story("6: Неактивная кнопка")
    def test_ghost_button(self, main_page):
        with allure.step("Активация бага с неактивной кнопкой отправки"):
            main_page.toggle_bug("ghost_button")
        with allure.step("Ввод индекса и города"):
            main_page.fill_form("ru", "450000")
            main_page.city_detect()
        with allure.step("Попытка нажать на кнопку отправки в БД"):
            main_page.click_save()
            message = main_page.get_status(expected="Error")
            assert "Error" in message
