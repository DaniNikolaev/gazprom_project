from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def create_test_device(test_client: TestClient):
    """Создает тестовое устройство и возвращает его ID"""
    response = test_client.post("/api/devices")
    assert response.status_code == 200
    device_id = response.json()["id"]
    return device_id


@pytest.fixture
def create_test_data(test_client: TestClient, create_test_device: int):
    """Создает тестовые данные и возвращает их ID"""
    device_id = create_test_device

    data = {
        "id_device": device_id,
        "x": 1.0,
        "y": 2.0,
        "z": 3.0
    }
    response = test_client.post("/api/data/", json=data)
    assert response.status_code == 200
    data_id = response.json()["id"]
    return data_id


def test_get_devices(test_client: TestClient):
    """Проверка эндпоинта /devices"""
    response = test_client.get("/api/devices")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_device_by_id(test_client: TestClient, create_test_device: int):
    """Проверка эндпоинта /devices/{id}"""
    device_id = create_test_device
    response = test_client.get(f"/api/devices/{device_id}")
    assert response.status_code == 200
    assert response.json()["id"] == device_id


def test_get_device_by_id_not_found(test_client: TestClient):
    """Проверка эндпоинта /devices/{id} для несуществующего ID"""
    device_id = 999
    response = test_client.get(f"/api/devices/{device_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"


def test_get_data(test_client: TestClient):
    """Проверка эндпоинта /data"""
    response = test_client.get("/api/data")
    assert response.status_code == 200


def test_create_data(test_client: TestClient, create_test_device: int):
    """Проверка создания данных POST /data/"""
    device_id = create_test_device
    data = {
        "id_device": device_id,
        "x": 4.0,
        "y": 5.0,
        "z": 6.0
    }
    response = test_client.post("/api/data/", json=data)
    assert response.status_code == 200
    created_data = response.json()
    assert created_data["id_device"] == device_id
    assert created_data["x"] == 4.0
    assert created_data["y"] == 5.0
    assert created_data["z"] == 6.0


def test_get_data_by_id(test_client: TestClient, create_test_data: int):
    """Проверка эндпоинта /data/{id}"""
    data_id = create_test_data
    response = test_client.get(f"/api/data/{data_id}")
    assert response.status_code == 200
    assert response.json()["id"] == data_id


def test_get_data_by_id_not_found(test_client: TestClient):
    """Проверка эндпоинта /data/{id} для несуществующего ID"""
    data_id = 999
    response = test_client.get(f"/api/data/{data_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Data record not found"


def test_get_analysis(test_client: TestClient):
    """Проверка эндпоинта /analysis"""
    response = test_client.get("/api/analysis")
    assert response.status_code == 200
    analysis_data = response.json()
    assert "min_x" in analysis_data
    assert "max_x" in analysis_data
    assert "avg_x" in analysis_data
    assert "median_x" in analysis_data


def test_get_analysis_by_id(test_client: TestClient, create_test_device: int):
    """Проверка эндпоинта /analysis/{id}"""
    device_id = create_test_device
    response = test_client.get(f"/api/analysis/{device_id-1}")
    assert response.status_code == 200
    assert "min_x" in response.json()


def test_get_analysis_by_id_not_found(test_client: TestClient):
    """Проверка эндпоинта /analysis/{id} для несуществующего ID"""
    device_id = 999
    response = test_client.get(f"/api/analysis/{device_id}")
    assert response.status_code == 404
