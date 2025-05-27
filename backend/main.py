from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.api.routes import router as api_router
from backend.utils.glossary import load_glossary
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")
app.mount("/static", StaticFiles(directory="frontend/public/static"), name="static")

glossary = load_glossary()
app.state.glossary = glossary

app.include_router(api_router)