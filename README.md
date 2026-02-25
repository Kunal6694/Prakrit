🌿 Prakrit: AI-Verified Sustainability Ecosystem

Deciphering Nature with AI-Verified Integrity. Built for the Hack For Green Bharat Hackathon.

Prakrit is a dual-engine platform designed to eliminate "greenwashing" in the event industry. By combining Pathway’s real-time streaming engine with Google Gemini’s AI reasoning, Prakrit provides an automated, transparent, and rewarding ecosystem for organizers, customers, and auditors.

✨ Key Features
🛡️ AI-Verified Audits: Real-time sustainability proof verification using Gemini 1.5 Flash.

📈 Live Pathway Ticker: A global "Eco-Pulse" that updates incrementally as new events are verified.

💬 Prakrit AI Consultant: A real-time RAG (Retrieval-Augmented Generation) assistant that answers sustainability queries based on live-indexed data.

🪙 PrakritMudra Economy: A digital reward system that incentivizes green choices for both customers and organizers.

🆔 Prakrit ID: A unique, unified identifier for every stakeholder in the green ecosystem.

🛠️ Tech Stack
Streaming Engine: Pathway (Real-time data ingestion & RAG)

AI Reasoning: Google Gemini 1.5 Flash (via google-generativeai)

Frontend: Streamlit (Cinematic "Veridian Mirror" UI)

Database: SQLite3 (Persistent local storage)

Environment: Python 3.10+

🚀 Quick Start
To run Prakrit on your local machine, follow these steps in order.

1. Clone the Repository
Bash
git clone https://github.com/Kunal6694/Prakrit.git
cd Prakrit

3. Setup Environment Variables
Create a .env file in the root directory and add your Google API Key:

Plaintext
GOOGLE_API_KEY=your_gemini_api_key_here

3. Install Dependencies
Bash
pip install -r requirements.txt

4. Launch the Pathway Engine (Backend)
Open a terminal and run the streaming processor. This must stay running to process audits and the RAG index in real-time.
Bash
python main.py
5. Launch the Prakrit App (Frontend)

Open a second terminal and run the Streamlit application.
Bash
streamlit run prakrit_app.py

🏗️ Architecture: The "One-Line Rule"
Prakrit follows the mandatory Pathway requirement: the system updates automatically when new data arrives.

Ingestion: Files (PDF/TXT) uploaded to data/input/ are detected instantly by Pathway.

Reasoning: main.py uses pw.apply to score the reports and generate RAG insights via Gemini.

Synchronization: Pathway sinks the results to pathway_results.csv and live_pulse.jsonl.

UI Refresh: The Streamlit frontend monitors these sinks and updates the Live Ticker and Consultant Tip without requiring a page reload.

⚖️ License
This project is licensed under the MIT License - see the LICENSE file for details.

🌿 Our Vision
To move from a world of "claimed" sustainability to "verified" impact, one event at a time.
