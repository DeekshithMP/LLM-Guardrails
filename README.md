<h1> LLM GUARDRAILS</h1>
<p>This project implements a real-time AI guardrails system** to ensure safe interaction with Large Language Models (LLMs). It detects and blocks unsafe user prompts such as harmful instructions, self-harm content, and prompt injection attacks before they reach the model.
The system uses a **zero-shot classification approach** combined with a **confidence-based decision layer** to balance safety and usability.</p>

<h2>Problem Statement</h2>
LLMs can generate unsafe or harmful responses when given malicious or sensitive inputs such as:
<li><ol>Hacking instructions</ol></li>
<li><ol>Self-harm queries</ol></li>
<li><ol>Prompt injection attempts</ol></li>

<p>This project addresses the need for a **pre-response safety layer** that filters such inputs in real time.</p>

<h2>Approach</h2>
<li><ol>Zero-shot classification using **BART MNLI (Hugging Face Transformers)</ol></li>
<li><ol>Semantic category design (no keyword hardcoding)</ol></li>
<li><ol>Confidence-based filtering to reduce false positives</ol></li>
<li><ol>Tiered decision system:</ol></li>
<ol>Block unsafe inputs</ol>
<ol>Allow safe inputs</ol>

---

## Architecture

```
User Input → Classifier → Decision Layer → LLM / Block → UI
```

---


##  Setup Instructions

```bash
# 1. Clone repo
git clone https://github.com/DeekshithMP/LLM-Guardrails.git

# 2. Move into project
cd llm-guardrails

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add API key
echo GROQ_API_KEY=your_api_key_here > .env

# 5. Run App (Terminal 1)
uvicorn app:app --reload

# 6. Run App (Terminal 2)
python -m streamlit run ui.py

```

---

##  Results

* Successfully blocks:

  * harmful instructions (e.g., hacking)
  * self-harm prompts
* Reduced false positives using confidence-based filtering
* Achieved stable real-time performance

---

##  P95 Latency

* **~300–500 ms per request** (CPU-based inference)
* Includes classification + decision + response pipeline

---

## Application URL
https://llm-guardrails.streamlit.app/

