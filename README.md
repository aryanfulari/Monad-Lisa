# AgentPassport

## 1. One-Line Tagline
**AI-powered credentials and task execution stored permanently on the high-performance Monad Blockchain.**

---

## 2. Problem Statement
As AI agents become more autonomous, there is no verifiable, immutable record of their performance, reliability, or the quality of their work over time. Users cannot easily trust an agent without a transparent history of its past actions and evaluations.

---

## 3. Solution
**AgentPassport** introduces a dual-agent architecture to solve this. A **Worker Agent** completes tasks, and a **Judge Agent** evaluates the quality of the work. The resulting score and feedback are permanently logged on the **Monad Blockchain**, creating a verifiable, immutable "Passport" for AI models. 

---

## 4. Key Features
- 🤖 **Dual-Agent Architecture:** Worker Agent executes tasks; Judge Agent evaluates them.
- ⛓️ **Immutable Blockchain Logging:** All tasks, scores, and feedback are recorded on the Monad Testnet.
- ⚡ **High-Speed Execution:** Built on Monad for ultra-fast, low-latency transaction finality.
- 📊 **Dynamic Next.js Dashboard:** Real-time UI displaying agent stats, badges, and performance history.
- 🏆 **Model Leaderboard:** Compare different Gemini models (2.5 Flash, 2.5 Pro, etc.) based on their average Judge scores.
- 🏅 **Achievement System:** Earn badges (e.g., "Perfect Score", "High Performer") based on on-chain data.

---

## 5. Demo
*(Add your Screenshots / GIF / Video links here)*

---

## 6. System Architecture
```text
User ──> Next.js Frontend ──> FastAPI Backend
                                   │
                                   ├──> 1. Worker Agent (Gemini) generates output
                                   ├──> 2. Judge Agent (Gemini) scores output
                                   └──> 3. Web3.py records data on Monad Testnet
```

---

## 7. Workflow
1. **Request:** User submits a prompt and selects an AI model via the frontend.
2. **Execution:** The Python backend triggers the **Worker Agent** to complete the task.
3. **Evaluation:** The **Judge Agent** reviews the worker's output and assigns a score (0-100) with feedback.
4. **On-Chain Record:** The score, feedback, and task metadata are minted as an achievement on the Monad blockchain.
5. **UI Update:** The dashboard fetches the updated on-chain data to refresh stats, badges, and the leaderboard.

---

## 8. Tech Stack
- **Frontend:** Next.js (App Router), React, Vanilla CSS (Custom Glassmorphism UI)
- **Backend:** Python, FastAPI, Uvicorn
- **AI Integration:** Google Gemini API (`google-genai`)
- **Blockchain:** Monad Testnet, Web3.py, Solidity

---

## 9. Smart Contract Overview
The smart contract acts as the decentralized registry for the AgentPassport. It stores:
- `agent_address`: The wallet address representing the AI agent.
- `task`: A tagged string representing the executed prompt and model used.
- `score`: The numerical evaluation from the Judge Agent.
- `feedback`: Textual feedback justifying the score.

---

## 10. Project Structure
```text
Monad-Lisa/
│
├── frontend/               # Next.js React Dashboard
├── ai/                     # Worker and Judge Agent logic (Gemini)
├── blockchain/             # Web3.py integration and Monad interactions
├── dashboard/              # Data aggregation for Leaderboards and Badges
├── api.py                  # FastAPI Backend Server
├── pipeline.py             # Orchestrates the AI + Blockchain flow
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 11. Installation & Setup

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- A Monad Testnet Wallet with test tokens

### Clone the repository
```bash
git clone https://github.com/aryanfulari/Monad-Lisa.git
cd Monad-Lisa
```

---

## 12. Environment Variables (.env)
Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
# Add your Web3 Provider / Private Keys as required by the blockchain module
```

---

## 13. Running the Project

**Start the Python Backend (FastAPI):**
```bash
pip install -r requirements.txt
python -m uvicorn api:app --port 8000
```

**Start the Next.js Frontend:**
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```

---

## 14. Usage Guide
1. Open [http://localhost:3000](http://localhost:3000) in your browser.
2. View your agent's current Trust Score, Level, and Badges.
3. In the **Generate & Verify Credential** panel, enter a task (e.g., "Explain Quantum Computing").
4. Select a Gemini model from the dropdown.
5. Click **Generate & Verify**. Wait for the transaction to complete.
6. Click the Monad Explorer link to view your permanent on-chain credential!

---

## 15. Example Workflow
- **Task:** "Write a Python function to calculate the Fibonacci sequence."
- **Worker Agent:** Outputs the Python code.
- **Judge Agent:** Evaluates code correctness and efficiency. Assigns a score of `95/100` and feedback: *"Efficient O(n) implementation."*
- **Blockchain:** Transaction confirmed on Monad Testnet.
- **Dashboard:** "High Performer" badge unlocked.

---

## 16. Why Monad?
Agent interactions require high throughput and instant finality. Traditional blockchains are too slow and expensive to record every micro-action an AI takes. **Monad** provides the extreme EVM performance (10,000 TPS) necessary to log AI agent credentials in real-time without bottlenecks.

---

## 17. Future Scope
- **Multi-Agent Swarms:** Tracking credentials for autonomous teams of interacting agents.
- **Decentralized Judges:** Using a consensus of multiple LLMs to prevent judge bias.
- **Mainnet Deployment:** Transitioning the passport registry to Monad Mainnet.

---

## 18. Team Members
- **Aryan Fulari**

---

## 19. License
*MIT License* (Optional - Update as needed)

---

## 20. Acknowledgements
- Developed for the **Monad Blitz Hackathon**.
- Powered by the **Google Gemini API**.
