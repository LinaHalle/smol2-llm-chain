# SmolLM2 Data Analysis API

Ett FastAPI-projekt som låter användaren:

- Ladda upp CSV-filer
- Generera statistik från uppladdad data
- Ställa frågor om datasetet med hjälp av AI
- Analysera data genom en egen Runnable-kedja

---

## Funktionalitet

### Datauppladdning

Användaren kan ladda upp en CSV-fil som lagras i minnet för vidare analys.

### Statistik

API:et kan generera beskrivande statistik för det uppladdade datasetet.

### AI-frågor

Användaren kan ställa frågor om datasetet på naturligt språk.

Modellen är primärt optimerad för engelska instruktioner, därför används engelska frågor i exemplena och rekommenderas för bästa resultat.

### AI-pipeline

Projektet använder en egen Runnable-kedja:

```text
PromptBuilder → LLMRunner → ResponseParser
```

### Beskrivning av kedjan

- **PromptBuilder** skapar en prompt baserad på användarens fråga och datasetets statistik.
- **LLMRunner** skickar prompten till SmolLM2-modellen för generering av svar.
- **ResponseParser** extraherar och formaterar modellens svar innan det returneras till klienten.

---

## Installation

### Klona projektet

```bash
git clone <repo-url>
cd smol2-llm-chain
```

### Skapa virtuell miljö

```bash
uv venv
```

### Installera beroenden

```bash
uv sync
```

---

## Starta applikationen

```bash
uv run uvicorn app.main:app --reload
```

Applikationen startar på:

```text
http://127.0.0.1:8000
```

Swagger-dokumentation:

```text
http://127.0.0.1:8000/docs
```

---

## API-endpoints

### Hälsokontroll

```http
GET /health
```

Exempel:

```bash
curl http://127.0.0.1:8000/health
```

Svar:

```json
{
  "status": "ok"
}
```

---

### Ladda upp CSV-fil

```http
POST /data/upload
```

Exempel:

```bash
curl -X POST \
  -F "file=@sleep_health_dataset.csv" \
  http://127.0.0.1:8000/data/upload
```

Svar:

```json
{
  "rows": 374,
  "columns": [...],
  "dtypes": {...}
}
```

---

### Hämta statistik

```http
GET /data/stats
```

Exempel:

```bash
curl http://127.0.0.1:8000/data/stats
```

---

### Ställ en AI-fråga

```http
POST /ai/ask
```

Request:

```json
{
  "question": "What insights can you find in the dataset?"
}
```

Exempel:

```bash
curl -X POST \
  http://127.0.0.1:8000/ai/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What insights can you find in the dataset?"}'
```

Svar:

```json
{
  "question": "What insights can you find in the dataset?",
  "answer": "...",
  "model": "HuggingFaceTB/smolLM2-135M-Instruct"
}
```

---

## Tester

Kör alla tester:

```bash
uv run pytest
```

Kör ett specifikt test:

```bash
uv run pytest app/tests/test_endpoints.py -v
```

---

## Antaganden

Följande antaganden har gjorts under utvecklingen:

- Endast CSV-filer accepteras.
- Uppladdad data lagras endast i minnet.
- Maximal filstorlek är 5 MB.
- CSV-filer måste vara UTF-8-kodade.
- AI-modellen får endast tillgång till sammanfattande statistik från datasetet.
- Projektet är utvecklat för lokalt bruk som en del av kursuppgiften.

---

## Projektstruktur

```text
app/
│
├── __init__.py
│
├── chain/
│   ├── __init__.py
│   ├── pipeline.py
│   ├── runnable.py
│   └── steps.py
│
├── tests/
│   ├── __init__.py
│   ├── test_chain.py
│   └── test_endpoints.py
│
├── data.py
├── schemas.py
└── main.py
```

---

## Modell

Projektet använder:

```text
HuggingFaceTB/smolLM2-135M-Instruct
```

---
