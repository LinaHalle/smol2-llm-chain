from fastapi.testclient import TestClient
from app.main import app

# BytesIO = fejkat filobject som beter sig som en riktig fil
from io import BytesIO

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_stats_no_dataset():
    response = client.get("/data/stats")

    assert response.status_code == 404
    assert response.json()["detail"] == "No dataset uploaded yet"

def test_upload_csv_succsess():
    csv_content = b"""a,b
1,2
3,4
"""

    file = BytesIO(csv_content)

    response = client.post(
        "/data/upload",
        files={"file": ("test.csv", file, "text.csv")}
    )

    assert response.status_code == 200
    data = response.json()

    assert data ["rows"] == 2
    assert "columns" in data
    assert "dtypes" in data
