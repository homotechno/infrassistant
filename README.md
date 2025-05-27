# Infra-Assistant: AI-Powered PostgreSQL Incident Reporter 💡

This project is a full-stack AI assistant designed to analyze PostgreSQL database incidents based on meeting transcripts or user queries. It automatically generates structured incident reports or suggests relevant solutions using RAG (retrieval-augmented generation) and large language models (LLMs).

---

## 🔧 Features

- Upload meeting transcript files to generate structured incident reports (summary, type, cause, solution)
- Ask follow-up questions in natural language
- Uses GigaChat API (GigaChat-Max) for analysis and report generation
- Integrates RAG via ChromaDB to retrieve past solutions
- React-based chat interface with light/dark themes
- Supports Markdown rendering, animated typing, and file uploads

---

## 🖼️ UI Preview

![screenshot](./frontend/public/static/main.png)

---

## 🚀 Tech Stack

### Frontend
- React + Vite
- `marked.js` for Markdown rendering
- Theming with `light.css` / `dark.css`

### Backend
- FastAPI
- GigaChat API (GigaChat-Max)
- MongoDB (for storing structured reports)
- ChromaDB (for RAG knowledge base)

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/homotechno/infrassistant.git
cd infrassistant
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a .env file in the project root with the following:

```.env
GIGA_MODEL=GigaChat-Max
GLOSSARY_PATH=backend/glossary.json
CHROMA_PATH=backend/chroma_db
MONGO_URI=mongodb://<user>:<pass>@localhost:27017/tks?authSource=tks
MONGO_DB=tks
MONGO_COLLECTION=incident_report
BASE_URL_GIGA=https://gigachat.devices.sberbank.ru/api/v1
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
```

### 4. Run the backend

```bash
uvicorn backend.main:app --reload
```
By default, the API will be accessible at:
📍 http://127.0.0.1:8000

### 5. Set up the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at:
🌐 http://localhost:5173

To build the frontend for production:

```bash
npm run build
```

This will generate a production-ready build in frontend/dist/.

## 🔌 API Endpoints

### `GET /`
**Description**:  
Serves the built React frontend (`index.html`).  
If the frontend is not yet built, returns an error message.

---

### `POST /ask_solution/`
**Description**:  
Retrieves similar solutions from the RAG knowledge base (ChromaDB) and asks GigaChat to compose an answer.

**Request Body** (`application/x-www-form-urlencoded`):
- `prompt` – User question or incident description

**Response**:
```json
{
  "solution": "Markdown-formatted answer with proposed solution"
}
```

---

### `POST /get_incident_report/`
**Description**:  
Generates a structured PostgreSQL incident report from a file, text prompt, or both.

**Request Body** (`multipart/form-data`):
- `prompt` (optional): Question or additional context
- `file` (optional): Uploaded `.txt` file with transcription content

**Response**:
```json
{
  "incident_summary": "...",
  "incident_type": "...",
  "root_cause": "...",
  "solution": "..."
}
```