<<<<<<< HEAD
﻿# KnowledgeAssist AI

## Description

This project is a simple, lightweight customer support chatbot built for a fictional SaaS company named **KnowledgeAssist AI**. It uses a locally hosted LLM via Ollama (`gemma4:e4b`), FastAPI, and Pydantic to answer support queries accurately based strictly on a local knowledge base (`knowledge.json`).
=======
# CloudDesk AI Customer Support Assistant

## Description

This project is a simple, lightweight customer support chatbot built for a fictional SaaS company named **CloudDesk**. It uses a locally hosted LLM via Ollama (`gemma4:e4b`), FastAPI, and Pydantic to answer support queries accurately based strictly on a local knowledge base (`knowledge.json`).
>>>>>>> 733022452e2f5b7445b8711f9ae90780738d6219

If a question cannot be answered using the provided knowledge base, the assistant safely refrains from inventing an answer and marks `needs_human: true`.

---

## Features

- **LLM-Powered Support**: Delivers helpful, accurate support answers.
- **Local LLM**: Powered locally using Ollama and `gemma4:e4b`.
- **Structured JSON Responses**: Guaranteed schema validation using Pydantic.
- **Knowledge-Based Answers**: Answers strictly grounded in `knowledge.json`.
- **Unknown-Question Fallback**: Recommends human support if information is missing or out of scope.
- **Error Handling & Resilience**: Graceful fallback when inputs are empty/whitespace, Ollama is unreachable, models are missing, or outputs are unparseable.
- **Markdown-Fence Cleansing**: Automatically strips markdown code fences (` ```json `) to prevent JSON decode failures.
- **Category Consistency**: Ensures `unknown` or `error` categories reliably flag `needs_human: true`.
- **No Paid API**: 100% free, local, and private.

---

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com/)
- Local model: `gemma4:e4b`

---

## Installation & Setup

1. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure Ollama is running and verify the model:**

   ```bash
   ollama list
   ```

   The output should list:

   ```text
   gemma4:e4b
   ```

   *(If not installed, run `ollama pull gemma4:e4b`)*

3. **Run the FastAPI server:**

   ```bash
   uvicorn main:app --reload
   ```

4. **Open Swagger UI in your browser:**

   Navigate to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Testing

The project includes automated tests covering both live LLM interactions (with Ollama running) and unit tests for edge cases (Ollama unavailable, invalid model output, empty messages).

To execute the test suite:

```bash
python -m unittest test_main.py -v
```

### Covered Test Scenarios:
1. **Password Reset (Direct)**: Verifies that exact knowledge base answers are returned.
2. **Password Reset (Paraphrased)**: Verifies topic recognition for paraphrased inputs.
3. **Subscription Cancellation**: Verifies documented cancellation instructions.
4. **Unknown Topic (Salesforce integration)**: Verifies that unsupported features trigger the unknown-question fallback (`needs_human: true`).
5. **Out of Scope (Weather)**: Verifies that general/unrelated queries are politely refused (`needs_human: true`).
6. **Input Validation**: Verifies that empty and whitespace-only queries are rejected with HTTP 400.
7. **Ollama Service Unavailable**: Verifies HTTP 503 response when Ollama is offline.
8. **Ollama Model Missing**: Verifies descriptive HTTP 503 guidance if the model is not pulled.
9. **Invalid / Incomplete LLM JSON**: Verifies graceful fallback (`category: error`, `needs_human: true`) without crashing.
10. **Markdown-Wrapped Output**: Verifies that responses with markdown code blocks parse cleanly.

---

## Usage Examples

<<<<<<< HEAD
### Example 1 â€” Known Question (Password Reset)
=======
### Example 1 — Known Question (Password Reset)
>>>>>>> 733022452e2f5b7445b8711f9ae90780738d6219

**POST** `/chat`
```json
{
  "message": "How do I reset my password?"
}
```

**Response:**
```json
{
  "answer": "Go to the login page and click Forgot Password. Then follow the instructions sent to your email.",
  "category": "account",
  "needs_human": false
}
```

---

<<<<<<< HEAD
### Example 2 â€” Known Question (Subscription Cancel)
=======
### Example 2 — Known Question (Subscription Cancel)
>>>>>>> 733022452e2f5b7445b8711f9ae90780738d6219

**POST** `/chat`
```json
{
  "message": "How can I cancel my subscription?"
}
```

**Response:**
```json
{
  "answer": "Go to Settings, then Billing, and select Cancel Subscription.",
  "category": "subscription",
  "needs_human": false
}
```

---

<<<<<<< HEAD
### Example 3 â€” Unknown / Out-of-Scope Question
=======
### Example 3 — Unknown / Out-of-Scope Question
>>>>>>> 733022452e2f5b7445b8711f9ae90780738d6219

**POST** `/chat`
```json
{
<<<<<<< HEAD
  "message": "Does KnowledgeAssist AI integrate with Salesforce?"
=======
  "message": "Does CloudDesk integrate with Salesforce?"
>>>>>>> 733022452e2f5b7445b8711f9ae90780738d6219
}
```

**Response:**
```json
{
  "answer": "I apologize, but the provided support information does not contain details about integrations with Salesforce. I can only help you with topics covered in the knowledge base.",
  "category": "unknown",
  "needs_human": true
}
```

---

## Internship Requirements

This project demonstrates core AI/LLM engineering fundamentals:

- **System Prompting**: Enforces scope boundary rules and persona guidelines.
- **Structured Output**: Uses JSON schema formatting and Pydantic validation.
- **Context/Knowledge Handling**: Passes local FAQ context dynamically into the model prompt.
- **Safe Fallback & Error Handling**: Avoids hallucinations and prevents server crashes on edge cases.
- **LLM Integration**: Interacts directly with a local Ollama model endpoint.

---

## Cost

> The application uses Ollama and the locally installed `gemma4:e4b` model, so no paid API or cloud service is required.
