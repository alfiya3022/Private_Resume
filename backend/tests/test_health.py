
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.main import app

client = TestClient(app)


def test_health_check_returns_ok():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_database_health_check_returns_connected():
    with patch("app.main.engine.connect") as mock_connect:
        mock_connection = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_connection

        response = client.get("/api/health/db")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "database": "connected",
    }
    mock_connection.execute.assert_called_once()


def test_database_health_check_returns_503_on_database_error():
    with patch(
        "app.main.engine.connect",
        side_effect=SQLAlchemyError("Database unavailable"),
    ):
        response = client.get("/api/health/db")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Database connection unavailable"
    }
