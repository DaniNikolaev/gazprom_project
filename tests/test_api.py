# tests/test_api.py
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import schemas  # Импортируем схемы
from app.models import DeviceData
from datetime import datetime

# Тесты для endpoint /data/ (POST)
def test_create_data(test_client: TestClient):
    """
    Тест для создания данных с помощью POST /data/.
    """
    data = {"device_id": "test_device_1", "x": 1.0, "y": 2.0, "z": 3.0}
    response = test_client.post("/data/", json=data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["device_id"] == "test_device_1"
    assert response_data["x"] == 1.0
    assert response_data["y"] == 2.0
    assert response_data["z"] == 3.0
    assert "id" in response_data  # Проверяем, что вернулся id


def test_create_data_invalid_data(test_client: TestClient):
    """
    Тест для создания данных с невалидными данными (проверка валидации Pydantic).
    """
    data = {"device_id": "test_device", "x": "invalid", "y": 2.0, "z": 3.0}  # x - не число
    response = test_client.post("/data/", json=data)
    assert response.status_code == 422  # Unprocessable Entity -  код для ошибки валидации
    # Можно добавить более детальные проверки ошибок, например,
    # assert response.json()["detail"][0]["msg"] == "value is not a valid float"  # Проверка конкретного сообщения об ошибке

# Тесты для endpoint /data/{device_id} (GET)
def test_read_data(test_client: TestClient, db_session: Session):
    """
    Тест для получения данных с помощью GET /data/{device_id}.
    """
    # Создаем тестовые данные в базе данных
    data1 = DeviceData(device_id="test_device_1", x=1.0, y=2.0, z=3.0)
    data2 = DeviceData(device_id="test_device_1", x=4.0, y=5.0, z=6.0)
    db_session.add_all([data1, data2])
    db_session.commit()

    response = test_client.get("/data/test_device_1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Проверяем, что вернулось две записи
    assert data[0]["device_id"] == "test_device_1"
    assert data[0]["x"] == 1.0
    assert data[1]["x"] == 4.0

def test_read_data_not_found(test_client: TestClient):
    """
    Тест для проверки обработки случая, когда данные не найдены.
    """
    response = test_client.get("/data/nonexistent_device")
    assert response.status_code == 404
    assert response.json()["detail"] == "Data not found"

def test_read_data_with_time_range(test_client: TestClient, db_session: Session):
    """
    Тест для получения данных с фильтрацией по времени.
    """
    # Создаем тестовые данные с разными временными метками
    now = datetime.utcnow()
    data1 = DeviceData(device_id="test_device_1", x=1.0, y=2.0, z=3.0, timestamp=now - timedelta(hours=1))
    data2 = DeviceData(device_id="test_device_1", x=4.0, y=5.0, z=6.0, timestamp=now)
    data3 = DeviceData(device_id="test_device_1", x=7.0, y=8.0, z=9.0, timestamp=now + timedelta(hours=1))
    db_session.add_all([data1, data2, data3])
    db_session.commit()

    # Запрашиваем данные в определенном временном диапазоне
    start_time = (now - timedelta(minutes=30)).isoformat()  # ISO формат
    end_time = (now + timedelta(minutes=30)).isoformat()
    response = test_client.get(f"/data/test_device_1?start_time={start_time}&end_time={end_time}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1  # Должна вернуться только одна запись (data2)
    assert data[0]["x"] == 4.0

# Тесты для endpoint /analysis/{device_id} (GET)
from datetime import timedelta
def test_analyze_data(test_client: TestClient, db_session: Session):
    """
    Тест для анализа данных с помощью GET /analysis/{device_id}.
    """
    # Создаем тестовые данные
    data1 = DeviceData(device_id="test_device_1", x=1.0, y=2.0, z=3.0)
    data2 = DeviceData(device_id="test_device_1", x=4.0, y=5.0, z=6.0)
    data3 = DeviceData(device_id="test_device_1", x=7.0, y=8.0, z=9.0)
    db_session.add_all([data1, data2, data3])
    db_session.commit()

    response = test_client.get("/analysis/test_device_1")
    assert response.status_code == 200
    data = response.json()
    assert data["min_x"] == 1.0
    assert data["max_x"] == 7.0
    assert data["count"] == 3
    assert data["sum_x"] == 12.0
    assert data["median_x"] == 4.0

def test_analyze_data_not_found(test_client: TestClient):
    """
    Тест для проверки обработки случая, когда данные для анализа не найдены.
    """
    response = test_client.get("/analysis/nonexistent_device")
    assert response.status_code == 404
    assert response.json()["detail"] == "No data found for this device and time range"

def test_analyze_data_with_time_range(test_client: TestClient, db_session: Session):
    """
    Тест для анализа данных с фильтрацией по времени.
    """
    now = datetime.utcnow()
    data1 = DeviceData(device_id="test_device_1", x=1.0, y=2.0, z=3.0, timestamp=now - timedelta(hours=1))
    data2 = DeviceData(device_id="test_device_1", x=4.0, y=5.0, z=6.0, timestamp=now)
    data3 = DeviceData(device_id="test_device_1", x=7.0, y=8.0, z=9.0, timestamp=now + timedelta(hours=1))
    db_session.add_all([data1, data2, data3])
    db_session.commit()

    # Запрашиваем анализ в определенном временном диапазоне
    start_time = (now - timedelta(minutes=30)).isoformat()  # ISO формат
    end_time = (now + timedelta(minutes=30)).isoformat()
    response = test_client.get(f"/analysis/test_device_1?start_time={start_time}&end_time={end_time}")

    assert response.status_code == 200
    data = response.json()
    assert data["min_x"] == 4.0  # Проверяем, что анализ верен для одного элемента
    assert data["max_x"] == 4.0
    assert data["count"] == 1
    assert data["sum_x"] == 4.0
    assert data["median_x"] == 4.0