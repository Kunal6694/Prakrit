🌿 Prakrit | AI Sustainability Ecosystem
Prakrit is a live AI-driven protocol designed to decipher nature's integrity using real-time data processing and verified sustainability audits. Built on the Pathway framework, it bridges the gap between industrial neglect and a regenerative future through a "Cyber-Nature" digital mirror. 

🚀 The Core Vision
In current systems, sustainability data is often stale or static. Prakrit solves this by utilizing LiveAI™ to ingest, process, and verify eco-proofs the millisecond they arrive. 
Real-Time Ingestion: Powered by Pathway, the system monitors live streams of audit documents and transaction logs. 
AI-Verified Integrity: Uses Gemini 2.5 Flash to perform deep-reasoning audits on sustainability reports to generate a dynamic "Eco-Index."
Mudra Economy: A reward system that credits PrakritMudra to organizers and customers upon successful, verified green transitions.

🛠️ Tech Stack

Engine: Pathway (Streaming Data Processing & Live RAG) 
AI Model: Google Gemini (Real-time Audit Analysis)
Frontend: Streamlit (Cinematic Veridian-Mirror UI)
Database: SQLite (User Persistence & Transaction History)

🏗️ Pathway Integration
Prakrit strictly adheres to the Pathway Framework requirements for the "Hack For Green Bharat" hackathon: 
Live Streaming: Ingests data using pw.io.fs.read in streaming mode to ensure zero-latency updates.
RAG Pipeline: Maintains a live hybrid index that updates the instant a sustainability report is added to the ./data/input directory.
Automatic Synchronization: If a report is modified or deleted, Pathway automatically synchronizes the index without manual re-ingestion. 

📦 Installation & Setup
Clone the Repository
git clone https://github.com/your-username/prakrit.git
cd prakrit

Install Dependencies
pip install -r requirements.txt
Environment Variables

Create a .env file and add your Gemini API Key:
Code snippet
GEMINI_API_KEY=your_api_key_here

Run the Pathway Engine
python main.py

Launch the Ecosystem
streamlit run prakrit_app.py

🛡️ Hackathon Track: Sustainability
This project is built for the AI/Machine Learning & Sustainability track. It demonstrates how streaming ML can be used for live monitoring, eco-score optimization, and real-time fraud detection in "Green Claims."

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
