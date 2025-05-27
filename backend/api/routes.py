"""
API routes for the backend.

Includes endpoints for:
- Serving frontend
- Asking questions using RAG + GigaChat
- Generating structured incident reports from text or file
"""

from fastapi import APIRouter, UploadFile, Form, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from backend.utils.glossary import create_system_prompt
from backend.db.mongo import incident_collection
from backend.services.rag import find_similar_solution
from backend.services.llm import call_gigachat
import pathlib
from fastapi.responses import FileResponse
import json
import os

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """
    Serves the built React frontend.
    """
    index_path = pathlib.Path("frontend/dist/index.html")
    if index_path.exists():
        return FileResponse(index_path)
    return HTMLResponse(
        content="React app not built. Please run `npm run build` in the frontend dir.",
        status_code=500,
    )


@router.post("/ask_solution/")
async def ask_solution(prompt: str = Form(...)):
    """
    Uses RAG to retrieve similar solutions and asks GigaChat
    to generate a formatted answer.
    """
    retrieved = find_similar_solution(prompt, top_k=3)
    if not retrieved:
        return JSONResponse(
            content={"solution": "Извините, решение не найдено в базе знаний."}
        )

    combined = "\n\n".join(
        [f"💡 Решение {i+1}:\n{sol}" for i, sol in enumerate(retrieved)]
    )
    context = (
        f"Вот похожие инциденты из базы знаний и предложенные решения:\n\n"
        f"{combined}\n\n"
        f"Теперь, исходя из этого, ответь на следующий вопрос пользователя:\n"
        f"Оформи ответ с использованием Markdown: используй списки, заголовки (###), выделения (**жирный текст**) и переносы строк."
    )

    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": prompt},
    ]

    try:
        reply = await call_gigachat(messages)
        return JSONResponse(content={"solution": reply})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.post("/get_incident_report/")
async def get_incident_report(
    request: Request, prompt: str = Form(None), file: UploadFile = File(None)
):
    """
    Handles generation of incident reports based on either a prompt, file, or both.
    Stores and updates results in MongoDB. Falls back to RAG if no solution is found.
    """
    if not prompt and not file:
        return JSONResponse(
            content={"error": "Пожалуйста, предоставьте файл или вопрос"},
            status_code=400,
        )

    # Case: Prompt only
    if prompt and not file:
        retrieved = find_similar_solution(prompt, top_k=3)
        if not retrieved:
            return JSONResponse(
                content={"solution": "Извините, решение не найдено в базе знаний."}
            )

        combined = "\n\n".join(
            [f"💡 Решение {i+1}:\n{sol}" for i, sol in enumerate(retrieved)]
        )
        context = (
            f"Вот похожие инциденты из базы знаний и предложенные решения:\n\n"
            f"{combined}\n\n"
            f"Теперь, исходя из этого, ответь на следующий вопрос пользователя:"
        )

        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt},
        ]

        try:
            reply = await call_gigachat(messages)
            return JSONResponse(content={"solution": reply})
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)

    # Case: File uploaded (with or without prompt)
    file_id = os.path.splitext(file.filename)[0]
    content = await file.read()
    file_text = content.decode("utf-8")

    # Create structured prompt
    glossary = request.app.state.glossary
    system_prompt = create_system_prompt(glossary)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": file_text},
    ]
    if prompt:
        messages.append({"role": "user", "content": prompt})

    await incident_collection.update_one(
        {"_id": file_id}, {"$set": {"content": file_text}}, upsert=True
    )

    try:
        response_text = await call_gigachat(messages)
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            result = {"incident_summary": response_text}

        await incident_collection.update_one(
            {"_id": file_id}, {"$set": result}, upsert=True
        )

        # Fallback to RAG if no solution found
        solution = result.get("solution", "")
        if not solution or "решение не обсуждалось" in solution.lower():
            query = result.get("incident_summary", "") or file_text
            retrieved = find_similar_solution(query, top_k=3)
            if retrieved:
                combined = "\n\n".join(
                    [f"💡 Решение {i+1}:\n{sol}" for i, sol in enumerate(retrieved)]
                )
                context = (
                    f"Похожие инциденты и предложенные решения:\n\n"
                    f"{combined}\n\n"
                    f"Предложи на основе этого подходящее решение:"
                )
                messages = [
                    {"role": "system", "content": context},
                    {"role": "user", "content": query},
                ]
                final_solution = await call_gigachat(messages)
                result["solution"] = final_solution.strip()

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(
            content={"error": f"Ошибка при анализе файла: {str(e)}"},
            status_code=500)
