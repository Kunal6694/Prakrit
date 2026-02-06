import pathway as pw
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def audit_document(text):
    # Using the 2.0 or 2.5 Flash model
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=f"Analyze this NGO document for green impact. 2-sentence summary: {text}"
    )
    return response.text

input_data = pw.io.fs.read("./data/input", format="plaintext", mode="streaming")

audited_data = input_data.select(
    summary=pw.apply(audit_document, pw.this.data)
)

pw.debug.compute_and_print(audited_data)
