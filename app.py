import streamlit as st
from groq import Groq
from pypdf import PdfReader
from validator import validate_invoice
import json
import re

st.set_page_config(page_title="Invoice AI", layout="wide")
st.title("📄 Smart Invoice Intelligence System")

# -------------------------
# FILE UPLOAD (PDF ONLY)
# -------------------------
uploaded_file = st.file_uploader("Upload Invoice PDF", type="pdf")

if uploaded_file:
    st.success(f"✅ Uploaded: {uploaded_file.name}")

    # -------------------------
    # PDF TEXT EXTRACTION
    # -------------------------
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    st.subheader("🔍 Extracted Text")
    st.write(text)

    # -------------------------
    # CHECK TEXT QUALITY
    # -------------------------
    if not text or len(text.strip()) < 20:
        st.error("❌ Could not extract text from PDF.")
        st.stop()

    # -------------------------
    # GROQ CLIENT
    # -------------------------
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    # -------------------------
    # PROMPT (FINAL)
    # -------------------------
    prompt = f"""
    You are an AI system that extracts structured data from invoice text.

    RULES:
    - Extract ONLY from given text
    - Do NOT add explanation
    - Return ONLY valid JSON

    Invoice Text:
    {text}

    Output format:
    {{
      "vendor": "",
      "invoice_number": "",
      "date": "",
      "total_amount": "",
      "tax": ""
    }}
    """

    # -------------------------
    # LLM RESPONSE
    # -------------------------
    with st.spinner("🤖 Analyzing invoice..."):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

    result = response.choices[0].message.content

    st.subheader("🧠 Extracted Data (Raw)")
    st.code(result)

    # -------------------------
    # CLEAN JSON PARSE
    # -------------------------
    try:
        json_match = re.search(r"\{.*\}", result, re.DOTALL)
        if json_match:
            clean_json = json_match.group()
            data = json.loads(clean_json)
        else:
            data = {}
    except:
        data = {}
        st.warning("⚠️ Could not parse JSON properly")

    st.subheader("✅ Parsed Data")
    st.write(data)

    # -------------------------
    # VALIDATION
    # -------------------------
    issues = validate_invoice(data)

    st.subheader("⚠️ Validation")

    if issues:
        for issue in issues:
            st.write(f"- {issue}")
    else:
        st.success("✅ All fields look good!")

    # -------------------------
    # INSIGHTS
    # -------------------------
    st.subheader("📊 Insights")

    if data.get("total_amount"):
        st.write("✔ Invoice processed successfully")

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.markdown("Built by Kiran Kaduluri 🚀")
