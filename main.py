<<<<<<< HEAD
﻿import json
=======
import json
>>>>>>> 733022452e2f5b7445b8711f9ae90780738d6219
from pathlib import Path
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import requests

# Ollama settings directly configured
MODEL = "gemma4:e4b"
OLLAMA_URL = "http://localhost:11434"

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge.json"

app = FastAPI(
<<<<<<< HEAD
    title="KnowledgeAssist AI",
=======
    title="AI Customer Support Assistant",
>>>>>>> 733022452e2f5b7445b8711f9ae90780738d6219
    description="Simple local LLM Customer Support Assistant for SaaS",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    message: str


class SupportResponse(BaseModel):
    answer: str
    category: str
    needs_human: bool


def load_knowledge_base() -> List[Dict[str, str]]:
    """Load support information from knowledge.json."""
    if not KNOWLEDGE_FILE.exists():
        return []
    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def build_system_prompt(knowledge: List[Dict[str, str]]) -> str:
    """Construct prompt with system rules and knowledge context."""
    return f"""You are the Customer Support Assistant.

Your job is to answer questions using ONLY the provided support information.

Rules:
1. Do not invent information.
2. Do not guess.
3. If the provided information does not answer the question, set needs_human to true and category to "unknown".
4. If the question is unrelated, explain that you can only help with support, set needs_human to true and category to "unknown".
5. Keep answers short and helpful.
6. Always return ONLY a valid JSON object matching the required structure.

Required JSON Structure:
{{
  "answer": "string",
  "category": "string (e.g. account, subscription, team, project, notification, unknown)",
  "needs_human": boolean
}}

Knowledge Base:
{json.dumps(knowledge, indent=2)}
"""


@app.get("/", response_class=PlainTextResponse)
def root():
    """Root endpoint returning application title."""
<<<<<<< HEAD
    return "KnowledgeAssist AI"
=======
    return "AI Customer Support"
>>>>>>> 733022452e2f5b7445b8711f9ae90780738d6219


@app.post("/chat", response_model=SupportResponse)
def chat(request: ChatRequest):
    """Chat endpoint processing user support queries using local Ollama model."""
    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Please enter a question.")

    knowledge = load_knowledge_base()
    system_prompt = build_system_prompt(knowledge)
    prompt = f"{system_prompt}\nUser Question: {user_message}\nJSON Response:"

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        res_data = response.json()
        raw_llm_response = res_data.get("response", "")
    except requests.exceptions.RequestException as e:
        detail = "The AI service is unavailable. Please make sure Ollama is running."
        if isinstance(e, requests.exceptions.HTTPError) and e.response is not None:
            if e.response.status_code == 404:
                detail = f"Model '{MODEL}' not found in Ollama. Run 'ollama pull {MODEL}'."
        raise HTTPException(
            status_code=503,
            detail=detail
        )

    try:
        clean_response = raw_llm_response.strip()
        if clean_response.startswith("```"):
            lines = clean_response.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]
            clean_response = "\n".join(lines).strip()

        parsed_data = json.loads(clean_response)
        if not isinstance(parsed_data, dict):
            raise ValueError("Response must be a JSON object.")

        # Ensure safety consistency: unknown or error categories require human support
        if str(parsed_data.get("category", "")).strip().lower() in ["unknown", "error"]:
            parsed_data["needs_human"] = True

        return SupportResponse(**parsed_data)
    except Exception:
        # Fallback response for unparseable or invalid LLM output
        return SupportResponse(
            answer="I couldn't process that request. Please contact human support.",
            category="error",
            needs_human=True
        )
