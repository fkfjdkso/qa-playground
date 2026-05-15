import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fastapi.testclient import TestClient
from app.main import app
from pages.base_page import BasePage
from app.database import SessionLocal

client = TestClient(app)


@pytest.fixture(scope="function")
def clean_db():
    response = client.delete("/api/danger/clear_db")

    if response.status_code != 200:
        pytest.fail(f"error: {response.text}")

    yield


@pytest.fixture
def run(clean_db):
    options = Options()

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)

    driver.get("http://127.0.0.1:8000")

    yield driver
    driver.quit()


@pytest.fixture
def api_run(clean_db):
    return client


@pytest.fixture
def main_page(run):
    return BasePage(run)


@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def make_payload():
    def _make(city="Москва", country="ru", zip="101000", **bugs):
        return {
            "country": country,
            "zip": zip,
            "city": city,
            "bugs": {
                "slow_db": bugs.get("slow_db", False),
                "data_loss": bugs.get("data_loss", False),
                "integrity": bugs.get("integrity", False),
            },
        }

    return _make
