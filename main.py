import pathway as pw
from google import genai
import os
import json
from dotenv import load_dotenv

# Load from .env file or environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found! Set it in your .env file.")

client = genai.Client(api_key=api_key)

# --- 1. AI REASONING LOGIC ---
def process_data_stream(text, mode="audit"):
    """
    Pathway transformation for real-time scoring and RAG response generation.

    """
    if mode == "audit":
        prompt = f"Analyze this sustainability report. Provide a score from 1.0 to 10.0. Return ONLY the number.\n\nContent: {text}"
    else:
        # RAG / Consultant prompt for live context analysis
        prompt = f"Using this sustainability context, act as a Prakrit AI Consultant and provide a brief tip: {text}"

    try:
        # Using the stable gemini-1.5-flash model
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception:
        return "0.0" if mode == "audit" else "Context currently unavailable."


# --- 2. LIVE INGESTION ---
# Watch the 'data/input' folder in streaming mode for new reports and guidelines
#
input_data = pw.io.fs.read("./data/input", format="plaintext", mode="streaming")

# --- 3. STREAMING TRANSFORMATION: Audit & RAG ---
# Process each file for an audit score and a consultant insight
#
processed_stream = input_data.select(
    filename=pw.this._metadata.get("path"),
    ai_score=pw.apply(lambda x: float(process_data_stream(x, "audit")), pw.this.data),
    consultant_tip=pw.apply(lambda x: process_data_stream(x, "rag"), pw.this.data),
    processed_at=pw.this._metadata.get("modified_at")
)

# --- 4. STREAMING AGGREGATIONS: Live Ticker ---
# Compute global eco-metrics automatically as data arrives
#
ticker_stats = processed_stream.groupby().reduce(
    avg_score=pw.reducers.avg(pw.this.ai_score),
    total_events=pw.reducers.count()
)

# --- 5. LIVE SINKS ---
# Write audit results and RAG tips for the portals
pw.io.csv.write(processed_stream, "data/pathway_results.csv")

# Write global pulse to JSONL for the dynamic ticker
pw.io.jsonlines.write(ticker_stats, "data/live_pulse.jsonl")

pw.run()