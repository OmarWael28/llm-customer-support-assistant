<<<<<<< HEAD
﻿# Audit and Test Report: LLM Customer Support Assistant
=======
# Audit and Test Report: LLM Customer Support Assistant
>>>>>>> 733022452e2f5b7445b8711f9ae90780738d6219

**Date:** 2026-10-19  
**Auditor:** Antigravity AI  
**Project:** LLM Customer Support Assistant  
**Repository Path:** `c:\Users\omarw\OneDrive\Desktop\LLM Customer Support Assistant`  
**Overall Status:** **READY**

---

## Executive Summary

The **LLM Customer Support Assistant** is a local, privacy-focused customer support chatbot built with **FastAPI**, **Pydantic**, and **Ollama** running the local model `gemma4:e4b`.

The project was comprehensively inspected, audited, tested, hardened, and verified against all internship requirements. All 8 required operational scenarios and 6 additional defensive edge cases passed automated tests.

---

## Requirement Verification Matrix

| # | Requirement | Status | Verification Evidence |
|---|---|:---:|---|
| 1 | Answers questions using support knowledge | **PASS** | `load_knowledge_base()` injects `knowledge.json` into the prompt. Verified with password reset and subscription queries. |
| 2 | Uses an appropriate system prompt | **PASS** | System prompt sets persona, 6 strict behavioral constraints, JSON schema, and FAQ context. |
| 3 | Returns valid structured JSON | **PASS** | Ollama called with `"format": "json"`; code strips markdown code fences and validates via Pydantic. |
| 4 | Uses consistent Pydantic response schema | **PASS** | Defined as `SupportResponse` (`answer: str`, `category: str`, `needs_human: bool`) and bound to FastAPI route. |
| 5 | Handles paraphrased support questions | **PASS** | Paraphrased query ("I forgot my password. How can I access my account?") correctly routed to password reset FAQ. |
| 6 | Does not invent unsupported answers | **PASS** | Unsupported feature query ("Salesforce integration") triggered safe fallback refusing to guess. |
| 7 | Safe fallback for unknown questions | **PASS** | Returns `category="unknown"` and `needs_human=True` when questions are not answered in knowledge base. |
| 8 | Handles unrelated questions appropriately | **PASS** | Out-of-scope query ("What is the weather today?") politely rejected with `category="unknown"`, `needs_human=True`. |
| 9 | Rejects empty and whitespace messages | **PASS** | Returns `HTTP 400 Bad Request` with message `"Please enter a question."`. |
| 10 | Handles Ollama connection errors | **PASS** | Catches `requests.exceptions.RequestException` and returns `HTTP 503 Service Unavailable`. |
| 11 | Handles invalid LLM responses safely | **PASS** | Malformed JSON, non-dict payloads, or missing fields return safe fallback (`category="error"`, `needs_human=True`) without crashing. |
| 12 | Uses configured `gemma4:e4b` model | **PASS** | Configured via `MODEL = "gemma4:e4b"`; verified installed in local Ollama instance (9.6 GB). |
| 13 | Does not require paid APIs | **PASS** | 100% free, local stack (Ollama + local Gemma model; zero cloud API dependencies). |

---

## Test Results

Automated test suite (`test_main.py`) executed with Python's standard `unittest` framework:
**14 tests ran, 14 passed, 0 failed, 0 skipped.**

```text
test_empty_and_whitespace_message_rejected .......... ok
test_incomplete_llm_schema_fallback ................ ok
test_invalid_llm_json_fallback ..................... ok
test_knowledge_base_loading ........................ ok
test_live_cancel_subscription ...................... ok
test_live_out_of_scope_weather ..................... ok
test_live_paraphrased_password_reset ............... ok
test_live_password_reset ........................... ok
test_live_unknown_integration_question ............. ok
test_markdown_code_fenced_json_parsed .............. ok
test_ollama_model_not_found_returns_clear_message .. ok
test_ollama_unavailable_returns_503 ................ ok
test_root_endpoint ................................. ok
test_unknown_category_enforces_needs_human ......... ok

<<<<<<< HEAD
Ran 14 tests in 36.548s â€” OK
=======
Ran 14 tests in 36.548s — OK
>>>>>>> 733022452e2f5b7445b8711f9ae90780738d6219
```

### Required Scenarios & Actual Responses

#### Scenario 1: Direct Support Question (Password Reset)
- **Input:** `"How do I reset my password?"`
- **HTTP Status:** `200 OK`
- **Response:**
  ```json
  {
    "answer": "Go to the login page and click Forgot Password. Then follow the instructions sent to your email.",
    "category": "account",
    "needs_human": false
  }
  ```
- **Evaluation:** **PASS**. Directly matches knowledge base content.

#### Scenario 2: Paraphrased Support Question
- **Input:** `"I forgot my password. How can I access my account?"`
- **HTTP Status:** `200 OK`
- **Response:**
  ```json
  {
    "answer": "Go to the login page and click Forgot Password. Then follow the instructions sent to your email.",
    "category": "account",
    "needs_human": false
  }
  ```
- **Evaluation:** **PASS**. Correctly identified semantic intent and retrieved the matching answer.

#### Scenario 3: Documented Feature (Cancel Subscription)
- **Input:** `"How do I cancel my subscription?"`
- **HTTP Status:** `200 OK`
- **Response:**
  ```json
  {
    "answer": "Go to Settings, then Billing, and select Cancel Subscription.",
    "category": "subscription",
    "needs_human": false
  }
  ```
- **Evaluation:** **PASS**. Documented instructions accurately returned.

#### Scenario 4: Unknown Topic (Salesforce Integration)
<<<<<<< HEAD
- **Input:** `"Does KnowledgeAssist AI integrate with Salesforce?"`
=======
- **Input:** `"Does CloudDesk integrate with Salesforce?"`
>>>>>>> 733022452e2f5b7445b8711f9ae90780738d6219
- **HTTP Status:** `200 OK`
- **Response:**
  ```json
  {
    "answer": "I apologize, but the provided support information does not contain details about integrations with Salesforce. I can only help you with topics covered in the knowledge base.",
    "category": "unknown",
    "needs_human": true
  }
  ```
- **Evaluation:** **PASS**. Model safely declined to invent an integration answer and flagged human intervention.

#### Scenario 5: Out of Scope (Weather)
- **Input:** `"What is the weather today?"`
- **HTTP Status:** `200 OK`
- **Response:**
  ```json
  {
    "answer": "I can only help with support questions related to our service.",
    "category": "unknown",
    "needs_human": true
  }
  ```
- **Evaluation:** **PASS**. Refused unrelated topic and set `needs_human: true`.

#### Scenario 6: Empty and Whitespace Inputs
- **Inputs:** `""` and `"    "`
- **HTTP Status:** `400 Bad Request`
- **Response:**
  ```json
  {
    "detail": "Please enter a question."
  }
  ```
- **Evaluation:** **PASS**. Prompt rejected before calling Ollama.

#### Scenario 7: Ollama Unavailable
- **Condition:** Ollama process stopped or unreachable (`ConnectionRefusedError`).
- **HTTP Status:** `503 Service Unavailable`
- **Response:**
  ```json
  {
    "detail": "The AI service is unavailable. Please make sure Ollama is running."
  }
  ```
- **Evaluation:** **PASS**. Handled gracefully with clear operator guidance.

#### Scenario 8: Invalid Model JSON Output
- **Condition:** LLM output is malformed, not JSON, or missing required keys.
- **HTTP Status:** `200 OK`
- **Response:**
  ```json
  {
    "answer": "I couldn't process that request. Please contact human support.",
    "category": "error",
    "needs_human": true
  }
  ```
- **Evaluation:** **PASS**. Handled safely without raising an unhandled 500 error.

---

## Hallucination & Fallback Logic Audit

> **Key Audit Finding:** While system prompts guide LLM behavior, system prompts alone do not provide a cryptographic or programmatic guarantee against hallucinations.

1. **Prompt-Level Boundary:** The system prompt explicitly instructs:
   - "Do not invent information."
   - "Do not guess."
   - "If the provided information does not answer the question, set needs_human to true and category to 'unknown'."
2. **Schema-Level Enforcement:** Ollama's `"format": "json"` prevents free-form prose.
3. **Programmatic Safeguards Added:**
   - Markdown code fence cleanser (`clean_response`) prevents JSON decode errors when the model encloses output in ```` ```json ````.
   - Type assertion ensures the parsed JSON is a mapping (`dict`), avoiding type crashes.
   - Category-consistency validation: if `category` is `"unknown"` or `"error"`, `needs_human` is programmatically enforced to `True`.
   - Clear diagnostics if Ollama returns 404 (model missing).

---

## Bugs Found & Fixes Applied

1. **Missing Test Suite:**
   - *Issue:* The repository had no automated test files, making regression testing impossible.
   - *Fix:* Created [`test_main.py`](file:///c:/Users/omarw/OneDrive/Desktop/LLM%20Customer%20Support%20Assistant/test_main.py) with 14 automated tests covering live integration and mocked edge cases.
2. **Missing `httpx` in Dependencies:**
   - *Issue:* FastAPI/Starlette's `TestClient` requires `httpx`, which was omitted from `requirements.txt`.
   - *Fix:* Added `httpx` to [`requirements.txt`](file:///c:/Users/omarw/OneDrive/Desktop/LLM%20Customer%20Support%20Assistant/requirements.txt).
3. **Markdown-Wrapped JSON Crash Risk:**
   - *Issue:* If the model ever enclosed JSON inside markdown code blocks (e.g. ```` ```json ... ``` ````), `json.loads()` would fail and cause a fallback even on a valid answer.
   - *Fix:* Added clean-up preprocessing in [`main.py`](file:///c:/Users/omarw/OneDrive/Desktop/LLM%20Customer%20Support%20Assistant/main.py) before `json.loads()`.
4. **Potential State Inconsistency Between Category and `needs_human`:**
   - *Issue:* If an LLM classified an answer as `"unknown"` but mistakenly returned `"needs_human": false`, the user could receive conflicting signals.
   - *Fix:* Added safety normalization ensuring `category in ["unknown", "error"]` forces `needs_human = True`.
5. **Generic Error on Missing Ollama Model:**
   - *Issue:* If Ollama was running but `gemma4:e4b` was not pulled (HTTP 404), the error claimed Ollama was not running.
   - *Fix:* Added specific 404 detection advising to run `ollama pull gemma4:e4b`.
6. **Incomplete README Documentation:**
   - *Issue:* README did not describe how to run tests or explain edge cases.
   - *Fix:* Updated [`README.md`](file:///c:/Users/omarw/OneDrive/Desktop/LLM%20Customer%20Support%20Assistant/README.md) with test commands, scenario breakdowns, and dependency details.

---

## Remaining Limitations

1. **No Semantic Search / Vector Retrieval (By Design):**
   The entire `knowledge.json` is passed directly in the system prompt. While simple, fast, and sufficient for smaller FAQ sets, very large knowledge bases will exceed context windows and require chunking/retrieval.
2. **Deterministic Grounding Verification:**
   The assistant relies on the instruction-following ability of `gemma4:e4b` to state when it lacks information. In rare edge cases where a model disregards instructions and confidently asserts a fact not present in the FAQ, programmatic string entailment is not performed.
3. **Single Turn Statelessness:**
   The `/chat` endpoint operates statelessly per request; conversational multi-turn context (e.g., following up on a previous answer) is not preserved.

---

## Commands to Install, Run, and Test

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Ollama & Model
```bash
ollama list
# Should display gemma4:e4b. If missing:
ollama pull gemma4:e4b
```

### 3. Run Automated Tests
```bash
python -m unittest test_main.py -v
```

### 4. Start the Application
```bash
uvicorn main:app --reload
```
Interactive API documentation will be available at: **http://127.0.0.1:8000/docs**

---

## Verdict

**READY**  
The project meets all functional, architectural, and educational goals of the internship task without introducing unnecessary complexity, external databases, or paid APIs.
