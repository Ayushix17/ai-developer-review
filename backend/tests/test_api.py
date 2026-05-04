import sys

from fastapi.testclient import TestClient


def _make_client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path.as_posix()}")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    for name in list(sys.modules):
        if name == "app" or name.startswith("app."):
            sys.modules.pop(name)

    # Import after env setup so settings and engine use the test database.
    from app.main import app

    return TestClient(app)


def test_health_endpoint(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_endpoint_persists_analysis(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)

    response = client.post(
        "/analyze",
        json={
            "code": "import os\nprint('debug')",
            "language": "python",
            "source_type": "pasted_code",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["analysis_id"] > 0
    assert body["tokens_used"] == 0
    assert any(f["title"] == "Unused import" for f in body["findings"])
    assert any(f["title"] == "Debug print" for f in body["findings"])


def test_list_analyses_returns_saved_rows(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)

    client.post(
        "/analyze",
        json={"code": "print('debug')", "language": "python"},
    )

    response = client.get("/analyses")

    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == 1
    assert rows[0]["language"] == "python"


def test_get_analysis_by_id_returns_details(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)

    create_response = client.post(
        "/analyze",
        json={"code": "print('debug')", "language": "python"},
    )
    analysis_id = create_response.json()["analysis_id"]

    response = client.get(f"/analyses/{analysis_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["analysis_id"] == analysis_id
    assert body["input_code"] == "print('debug')"
    assert any(f["title"] == "Debug print" for f in body["findings"])


def test_get_analysis_by_id_returns_404_for_missing_row(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)

    response = client.get("/analyses/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Analysis not found"
