# 🧾 InvoiceIQ
### AI-powered invoice processing pipeline that extracts, structures, and validates invoice data from PDFs using LLM intelligence.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_LLM-F55036?style=for-the-badge&logo=groq&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)

</div>

---

## 📌 What Is InvoiceIQ?

Manual invoice processing is slow, error-prone, and expensive. **InvoiceIQ** automates it end-to-end.

Upload any invoice PDF → InvoiceIQ extracts key fields using a Groq LLM, validates the data for completeness and format correctness, and returns a clean, structured JSON output — ready for downstream ERP or accounting workflows.

> Built to mirror enterprise invoice intelligence systems used in production at scale.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│                    Streamlit Web App (app.py)                   │
└────────────────────────────┬────────────────────────────────────┘
                             │  PDF Upload
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTRACTION LAYER                             │
│                     extractor.py                               │
│                                                                 │
│   PDF File ──► pdfplumber ──► Raw Text (per page)             │
│                                                                 │
│   • Multi-page support                                          │
│   • Preserves invoice table structure                           │
│   • Handles text-based PDFs reliably                           │
└────────────────────────────┬────────────────────────────────────┘
                             │  Raw Text
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      LLM PARSING LAYER                          │
│               Groq API — llama-3.1-8b-instant                  │
│                                                                 │
│   Structured Prompt ──► LLM ──► JSON Response                 │
│                                                                 │
│   Extracts:  vendor · invoice_number · date                    │
│              total_amount · tax                                 │
│                                                                 │
│   • Text truncated to 3000 chars (token safety)                │
│   • Regex JSON extraction as fallback parser                   │
└────────────────────────────┬────────────────────────────────────┘
                             │  Structured JSON
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VALIDATION LAYER                             │
│                      validator.py                              │
│                                                                 │
│   ✓ Required field presence checks                             │
│   ✓ Numeric format validation on amounts                       │
│   ✓ Currency symbol stripping (₹, $, ,)                       │
│   ✓ Returns structured error list for downstream handling      │
└────────────────────────────┬────────────────────────────────────┘
                             │  Validated Output
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT LAYER                               │
│                                                                 │
│   • Clean JSON displayed in UI                                  │
│   • Validation errors surfaced clearly                         │
│   • Ready for ERP / accounting system integration              │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| PDF Extraction | `pdfplumber` | Accurate text + table extraction from PDFs |
| LLM | `Groq (llama-3.1-8b-instant)` | Fast, free-tier structured data extraction |
| Validation | Custom `validator.py` | Field checks + numeric format validation |
| Backend API | `FastAPI` | REST endpoints for programmatic integration |
| Frontend UI | `Streamlit` | Clean, interactive web interface |
| Deployment | `Streamlit Cloud` | Zero-config cloud deployment |

---

## 🗂️ Project Structure

```
invoiceiq/
│
├── app.py              # Streamlit UI — upload, display, orchestrate
├── extractor.py        # PDF text extraction using pdfplumber
├── validator.py        # Field validation and format checks
├── api.py              # FastAPI REST backend
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── README.md
```

---

## 🚀 Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/invoiceiq
cd invoiceiq
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your Groq API key
Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free key at: https://console.groq.com

### 4. Run the Streamlit app
```bash
streamlit run app.py
```

### 5. OR run the FastAPI backend
```bash
uvicorn api:app --reload --port 8000
# Interactive docs: http://localhost:8000/docs
```

---

## 🔌 REST API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Service info + health |
| `GET` | `/health` | Health check |
| `POST` | `/extract` | Upload invoice PDF → get structured JSON |

### Example
```bash
curl -X POST "http://localhost:8000/extract" \
  -F "file=@invoice.pdf"
```

### Response
```json
{
  "success": true,
  "data": {
    "vendor": "Acme Corp",
    "invoice_number": "INV-2024-0042",
    "date": "2024-11-15",
    "total_amount": "12500.00",
    "tax": "1500.00"
  },
  "validation": {
    "errors": [],
    "status": "valid"
  }
}
```

---

## 💡 Key Design Decisions

**Why `pdfplumber` over `PyPDF2`?**
`pdfplumber` preserves invoice table structure during extraction. `PyPDF2` is deprecated and collapses table data into unstructured strings, making LLM parsing significantly harder.

**Why truncate text to 3000 characters?**
Prevents token overflow for the LLM context window. Invoice key fields (vendor, total, date) always appear in the first portion of the document.

**Why regex JSON extraction as a fallback?**
LLMs occasionally wrap JSON in markdown fences (` ```json ``` `). The regex pattern `\{.*\}` with `re.DOTALL` reliably extracts valid JSON regardless of formatting — a critical production robustness pattern.

**Why a separate `validator.py`?**
Separation of concerns. The validation logic is independently testable and reusable — it can be called from both the Streamlit UI and the FastAPI backend without duplication.

---

## 🏭 Real-World Relevance

InvoiceIQ mirrors the architecture of enterprise invoice automation systems:

| InvoiceIQ Component | Enterprise Equivalent |
|---|---|
| `pdfplumber` extraction | Document ingestion pipeline |
| Groq LLM parsing | Intelligent field extraction engine |
| `validator.py` | Data quality and reconciliation layer |
| FastAPI backend | Microservice API for ERP integration |
| JSON output | Structured data ready for SAP / QuickBooks |

---

## 📦 Requirements

```
streamlit
groq
pdfplumber
fastapi
uvicorn
python-dotenv
```

---

## 👤 Author

**Kiran Kaduluri**
[GitHub](https://github.com/yourusername) · [LinkedIn](https://linkedin.com/in/yourprofile) · k.kiran4900@gmail.com

---

<div align="center">
<i>Built as part of an AI engineering portfolio targeting enterprise AI use cases.</i>
</div>
