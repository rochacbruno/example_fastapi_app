import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from main import SystemMetrics, app

client = TestClient(app)


def test_metrics_endpoint_status_code():
    """Testa se o endpoint /metrics retorna status code 200"""
    os.environ.pop("SIMULATE_HEAVY_LOAD", None)
    os.environ.pop("SIMULATE_UNHEALTHY_BEHAVIOR", None)

    response = client.get("/metrics")
    assert response.status_code == 200


def test_metrics_endpoint_response_model():
    """Testa se a resposta do endpoint /metrics está de acordo com o SystemMetrics model"""
    os.environ.pop("SIMULATE_HEAVY_LOAD", None)
    os.environ.pop("SIMULATE_UNHEALTHY_BEHAVIOR", None)

    response = client.get("/metrics")

    assert response.status_code == 200

    data = response.json()

    assert "memoria" in data
    assert "cpu" in data
    assert "disk" in data

    assert isinstance(data["memoria"], (int, float))
    assert isinstance(data["cpu"], (int, float))
    assert isinstance(data["disk"], (int, float))

    assert 0 <= data["memoria"] <= 100
    assert 0 <= data["cpu"] <= 100
    assert 0 <= data["disk"] <= 100

    try:
        metrics = SystemMetrics(**data)
        assert metrics.memoria == data["memoria"]
        assert metrics.cpu == data["cpu"]
        assert metrics.disk == data["disk"]
    except Exception as e:
        pytest.fail(f"Resposta não está de acordo com o modelo SystemMetrics: {e}")


@patch("psutil.virtual_memory")
@patch("psutil.cpu_percent")
@patch("psutil.disk_usage")
def test_metrics_endpoint_with_mocked_values(mock_disk, mock_cpu, mock_memory):
    """Testa o endpoint /metrics com valores mockados para garantir consistência"""
    os.environ.pop("SIMULATE_HEAVY_LOAD", None)
    os.environ.pop("SIMULATE_UNHEALTHY_BEHAVIOR", None)

    mock_memory_obj = MagicMock()
    mock_memory_obj.percent = 45.5
    mock_memory.return_value = mock_memory_obj

    mock_cpu.return_value = 23.8

    mock_disk_obj = MagicMock()
    mock_disk_obj.percent = 67.2
    mock_disk.return_value = mock_disk_obj

    response = client.get("/metrics")

    assert response.status_code == 200

    data = response.json()
    assert data["memoria"] == 45.5
    assert data["cpu"] == 23.8
    assert data["disk"] == 67.2


def test_metrics_endpoint_content_type():
    """Testa se o endpoint /metrics retorna o content-type correto"""
    os.environ.pop("SIMULATE_HEAVY_LOAD", None)
    os.environ.pop("SIMULATE_UNHEALTHY_BEHAVIOR", None)

    response = client.get("/metrics")

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
