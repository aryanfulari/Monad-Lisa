# AgentPassport

AI Worker + Judge Agent module built using the **Google Gemini API** for the **Monad Blitz Hackathon**.

The project consists of two AI agents:

- **Worker Agent** – Completes any task provided by the user.
- **Judge Agent** – Evaluates how well the Worker Agent completed that task and assigns a score with feedback.

---

# Project Structure

```
AgentPassport/
│
├── agents.py          # Worker Agent + Judge Agent
├── test_gemini.py     # Simple Gemini API test
├── requirements.txt   # Required Python packages
├── .env.example       # Example environment variables
├── .gitignore
└── README.md
```

---

# Requirements

- Python 3.10+
- A Google Gemini API Key

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/aryanfulari/AgentPassport.git
```

Go into the project folder:

```bash
cd AgentPassport
```

---

## 2. Create a virtual environment

### macOS / Linux

```bash
python3 -m venv venv
```

### Windows

```cmd
python -m venv venv
```

---

## 3. Activate the virtual environment

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows (Command Prompt)

```cmd
venv\Scripts\activate
```

### Windows (PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Configure the API Key

Create a file named:

```
.env
```

Add the following line:

```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Replace `YOUR_GEMINI_API_KEY` with your own Gemini API key.

---

# Running the Project

Run:

```bash
python agents.py
```

The program will prompt you to enter **any task**.

Example tasks:

```
Write a 100-word paragraph on pollution.
```

```
Translate "Good morning" into French.
```

```
Explain blockchain in simple words.
```

```
Write a Python function that calculates factorial.
```

The Worker Agent completes the task.

The Judge Agent evaluates the Worker's response and returns:

- Score (0–100)
- Feedback

---

# Architecture

```
User Task
     │
     ▼
Worker Agent
     │
     ▼
Gemini API
     │
     ▼
Generated Output
     │
     ▼
Judge Agent
     │
     ▼
Gemini API
     │
     ▼
{
    "score": 95,
    "feedback": "Accurate answer with good clarity."
}
```

---

# Using the Agents

Import the functions:

```python
from agents import worker_agent, judge_agent
```

Run the Worker Agent:

```python
task = "Write a 100-word paragraph on pollution."

output = worker_agent(task)
```

Evaluate the result:

```python
result = judge_agent(
    task,
    output
)

print(output)

print(result["score"])
print(result["feedback"])
```

---

# API

## Worker Agent

```python
worker_agent(task: str) -> str
```

**Input**

- Any task as a string.

**Returns**

- Gemini's generated response.

---

## Judge Agent

```python
judge_agent(task: str, output: str) -> dict
```

**Input**

- Original task.
- Worker's output.

**Returns**

```python
{
    "score": int,
    "feedback": str
}
```

---

# Notes

- The Worker Agent can perform **any natural language task**.
- The Judge Agent evaluates the quality of the Worker's response.
- The API key is loaded from `.env`.
- The `.env` file is intentionally ignored by Git for security.

---

# Authors

Developed for the **Monad Blitz Hackathon**.