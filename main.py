import pathway as pw
from google import genai
import os
import json
import re
from dotenv import load_dotenv

# Load from .env file or environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found! Set it in your .env file.")

client = genai.Client(api_key=api_key)

# --- 1. AI REASONING LOGIC ---
def process_data_stream(text, mode="audit"):
    """Core AI processing logic."""
    if mode == "audit":
        prompt = f"""You are an expert Environmental Auditor and Event Sustainability Analyst. Your task is to critically evaluate the provided event sustainability report and assign a precise sustainability score from 1.0 to 10.0. 

Evaluate the report based on the following core criteria:
1. Waste Management: Active reduction of single-use plastics, recycling, and composting.
2. Energy & Carbon Footprint: Tracked emissions, renewable energy, carbon offsets.
3. Sourcing & Procurement: Eco-friendly materials, local and plant-forward catering.
4. Transparency & Metrics: Hard data and measurable outcomes vs. vague buzzwords.

Return ONLY the numerical score (e.g., 7.5). Do not include any explanations.

Content: {text}"""
    else:
        # RAG / Consultant prompt
        prompt = f"Using this sustainability context, act as a Prakrit AI Consultant and provide a brief tip: {text}"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        raw_text = response.text.strip()
        
        if mode == "audit":
            # Safety Net: Extract decimal number
            match = re.search(r"\d+(\.\d+)?", raw_text)
            return float(match.group()) if match else 0.0
        else:
            return raw_text
            
    except Exception as e:
        if mode == "audit":
            return 0.0
        else:
            # This will force the exact Google error to appear on your Streamlit dashboard!
            return f"API ERROR: {str(e)}"


# --- 2. PATHWAY TYPE-HINT WRAPPERS ---
# These force Pathway to strictly recognize the column data types!

def get_audit_score(text: str) -> float:
    return float(process_data_stream(text, "audit"))

def get_rag_tip(text: str) -> str:
    return str(process_data_stream(text, "rag"))


# --- 3. LIVE INGESTION ---
# Watch the 'data/input' folder in streaming mode
input_data = pw.io.fs.read("./data/input", format="plaintext", mode="streaming", with_metadata=True)


# --- 4. STREAMING TRANSFORMATION: Audit & RAG ---
processed_stream = input_data.select(
    filename=pw.this._metadata.get("path"),
    # We now pass the strictly typed functions, making Pathway perfectly happy!
    ai_score=pw.apply(get_audit_score, pw.this.data),
    consultant_tip=pw.apply(get_rag_tip, pw.this.data),
    processed_at=pw.this._metadata.get("modified_at")
)


# --- 5. STREAMING AGGREGATIONS: Live Ticker ---
ticker_stats = processed_stream.groupby().reduce(
    avg_score=pw.reducers.avg(pw.this.ai_score),
    total_events=pw.reducers.count()
)


# --- 6. LIVE SINKS ---
pw.io.csv.write(processed_stream, "data/pathway_results.csv")
pw.io.jsonlines.write(ticker_stats, "data/live_pulse.jsonl")

pw.run()

