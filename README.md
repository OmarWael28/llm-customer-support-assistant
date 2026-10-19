# KnowledgeAssist AI

## Description

KnowledgeAssist AI is a simple, lightweight customer support chatbot built for a fictional SaaS company named **KnowledgeAssist AI**. It uses a locally hosted LLM via Ollama (`gemma4:e4b`), FastAPI, and Pydantic to answer support queries accurately based strictly on a local knowledge base (`knowledge.json`).

If a question cannot be answered using the provided knowledge base, the assistant safely refrains from inventing an answer and marks `needs_human: true`.

---

## Features

- **LLM-Powered Support:** Delivers helpful, accurate support answers.
- **Local LLM:** Powered locally using Ollama and `gemma4:e4b`.
- **Structured JSON Responses:** Uses Pydantic for schema validation.
- **Knowledge-Based Answers:** Answers are grounded strictly in `knowledge.json`.
- **Unknown-Question Fallback:** Recommends human support when information is missing or out of scope.
- **Error Handling & Resilience:** Handles empty inputs, unavailable Ollama services, missing models, and invalid model outputs.
- **Markdown-Fence Cleansing:** Removes Markdown code fences from model responses to prevent JSON parsing failures.
- **Category Consistency:** Ensures `unknown` and `error` categories reliably set `needs_human: true`.
- **No Paid API:** Uses a local LLM without requiring a paid API or cloud inference service.

---

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com/)
- Local model: `gemma4:e4b`

---

## Installation & Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Ensure Ollama Is Running

Check whether the required model is installed:

```bash
ollama list
```

If `gemma4:e4b` is not listed, download it:

```bash
ollama pull gemma4:e4b
```

### 3. Run the FastAPI Server

```bash
uvicorn main:app --reload
```

### 4. Open Swagger UI

Navigate to:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Testing

The project includes automated tests covering live LLM interactions and edge cases such as unavailable Ollama services, invalid model outputs, and empty messages.

Run the test suite:

```bash
python -m unittest test_main.py -v
```

### Covered Test Scenarios

1. **Password Reset (Direct):** Verifies that exact knowledge base answers are returned.
2. **Password Reset (Paraphrased):** Verifies topic recognition for paraphrased inputs.
3. **Subscription Cancellation:** Verifies documented cancellation instructions.
4. **Unknown Topic (Salesforce Integration):** Verifies that unsupported features trigger the fallback with `needs_human: true`.
5. **Out-of-Scope Question (Weather):** Verifies that unrelated queries are handled safely.
6. **Input Validation:** Verifies that empty and whitespace-only queries are rejected with HTTP 400.
7. **Ollama Service Unavailable:** Verifies an HTTP 503 response when Ollama is offline.
8. **Ollama Model Missing:** Verifies that missing-model errors provide descriptive HTTP 503 guidance.
9. **Invalid or Incomplete LLM JSON:** Verifies graceful fallback without crashing.
10. **Markdown-Wrapped Output:** Verifies that responses wrapped in Markdown code fences are parsed correctly.

---

## Usage Examples

### Example 1 — Known Question: Password Reset

**POST** `/chat`

Request:

```json
{
  "message": "How do I reset my password?"
}
```

Response:

```json
{
  "answer": "Go to the login page and click Forgot Password. Then follow the instructions sent to your email.",
  "category": "account",
  "needs_human": false
}
```

---

### Example 2 — Known Question: Subscription Cancellation

**POST** `/chat`

Request:

```json
{
  "message": "How can I cancel my subscription?"
}
```

Response:

```json
{
  "answer": "Go to Settings, then Billing, and select Cancel Subscription.",
  "category": "subscription",
  "needs_human": false
}
```

---

### Example 3 — Unknown or Out-of-Scope Question

**POST** `/chat`

Request:

```json
{
  "message": "Does KnowledgeAssist AI integrate with Salesforce?"
}
```

Response:

```json
{
  "answer": "I apologize, but the provided support information does not contain details about integrations with Salesforce. I can only help you with topics covered in the knowledge base.",
  "category": "unknown",
  "needs_human": true
}
```

---

## Internship Requirements

This project demonstrates core AI and LLM engineering fundamentals:

- **System Prompting:** Enforces scope boundaries and persona guidelines.
- **Structured Output:** Uses JSON schema formatting and Pydantic validation.
- **Context and Knowledge Handling:** Passes local FAQ context dynamically into the model prompt.
- **Safe Fallback and Error Handling:** Avoids unsupported answers and handles edge cases.
- **LLM Integration:** Interacts directly with a locally hosted Ollama model.

---

## Cost

The application uses Ollama and the locally installed `gemma4:e4b` model, so no paid API or cloud inference service is required.
