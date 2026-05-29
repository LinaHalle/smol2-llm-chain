from fastapi.testclient import TestClient
from app.main import app

# BytesIO = fejkat filobject som beter sig som en riktig fil
from io import BytesIO
from app.chain.steps import LLMRunner
import pandas as pd

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



def test_upload_invalid_file_type():
    file_content = b"Summer is here"

    file = BytesIO(file_content)

    response = client.post(
        "/data/upload",
        files={"file": ("test.txt", file, "text/plan")}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only CSV files are allowed"



def test_upload_empty_file():
    file = BytesIO(b"")

    response = client.post(
        "/data/upload",
        files={"file": ("empty.csv", file, "text/csv")}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "File is empty"



def test_upload_too_large_file():
    big_content = b"a" * (6 * 1024 * 1024) #6mb istället för max som är 5mb

    file = BytesIO(big_content)

    response = client.post(
        "/data/upload",
        files={"file": ("big.csv", file, "text.csv")}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "File too large (max 5MB)"

def test_ai_ask_pipeline(monkeypatch):
    # fake LLM så testet inte kör modellen
    def fake_llm(self, input):
        return type("obj", (), {
            "raw_response": "ANSWER: dataset looks consistent",
            "question": input.question
        })()
    
    monkeypatch.setattr(LLMRunner, "invoke", fake_llm)

    # skapar litet dataset 
    df = pd.DataFrame({
        "a": [1, 2, 3],
        "b": [4, 5, 6]
    })

    from app.data import save_dataframe
    save_dataframe(df)

    # API call
    response = client.post(
        "/ai/ask",
        json={"question": "What do you see in the dataset?"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["question"] == "What do you see in the dataset?"
    assert "answer" in data
    assert data["model"] == "HuggingFaceTB/smolLM2-135M-Instruct"
    

