# Personal AI Learning Agent — Architecture Notes

> A CLI-based AI tutor I built to understand how LLM applications are actually structured — not just how to call an API.

This is a learning project, not a production tool. The goal was to go from *"I can prompt a model"* to *"I understand how real AI systems are designed"*. Everything here is intentionally minimal so the architecture stays visible.

---

## What It Does

The agent acts as a terminal-based Python tutor. Given a predefined skill graph, it:

1. Determines the next concept to teach (deterministically)
2. Generates an explanation via LLM
3. Creates a practice exercise
4. Accepts and evaluates the learner's answer
5. Marks the skill complete and moves forward

```
$ python main.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Next Skill: Python Variables
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Explanation:
  Variables in Python are labels that point to values in memory...

Exercise:
  Create a variable called `name` and assign it your name as a string.

Your answer: name = "Alice"

Evaluation:
  ✓ Correct. Score: 4/5 — Consider also noting the type.
```

**Stack:** Python · Ollama · qwen2.5:3b (local)

---

## Project Structure

```
learning-agent/
├── skills.py       # Knowledge Layer   — what to teach and in what order
├── prompts.py      # Prompt Layer      — how to instruct the model
├── llm.py          # Model Interface   — abstracts the model provider
├── agent.py        # Agent Layer       — orchestrates the full loop
└── main.py         # Interface Layer   — CLI entry point
```

Each layer has a single responsibility. This separation isn't just clean code — it mirrors how real AI products are architected.

---

## Architecture Deep Dive

### How the layers connect

```
main.py
  └─▶ agent.py          ← the brain; coordinates everything
        ├─▶ skills.py   ← what skill comes next?
        ├─▶ prompts.py  ← build the right prompt for the task
        └─▶ llm.py      ← send it to the model, get a response
```

The agent never talks to the model directly. It builds intent (`skill + prompt`), hands it to the LLM interface, and acts on what comes back. This separation is what makes the system swappable and testable.

---

### Layer 1 — Knowledge Layer (`skills.py`)

Defines the skill graph and dependency order:

```
python_variables
      ↓
python_loops
      ↓
python_functions
      ↓
python_dicts
```

This is entirely deterministic. The LLM has no say in what gets taught next — it can only explain and evaluate. This was a key early insight: **you don't want the model deciding curriculum**. It will hallucinate a perfectly reasonable-sounding learning path that has no coherent structure.

**Lesson:** Constrain the model to the decisions it's actually good at. Hand off structure to deterministic logic.

---

### Layer 2 — Prompt Layer (`prompts.py`)

Stores reusable, parameterized prompt templates. For example:

- `explanation_prompt(skill)` → asks the model to teach a concept
- `exercise_prompt(skill)` → asks for a coding challenge
- `evaluation_prompt(skill, answer)` → asks for structured feedback

Separating prompts from agent logic was one of the most important structural decisions. When prompts are embedded inline, iteration is messy — you end up touching orchestration logic just to tweak wording. When they're a layer of their own, prompt engineering becomes its own discipline.

**Lesson:** Prompt files are config, not code. Treat them that way.

---

### Layer 3 — Model Interface (`llm.py`)

A thin wrapper around Ollama (currently `qwen2.5:3b`). The rest of the system only ever calls `llm.complete(prompt)`. It doesn't know or care what's underneath.

The value of this abstraction became obvious immediately. Switching from Ollama to OpenAI or Anthropic would require changing exactly one file. Everything else stays the same.

```python
# What the agent sees:
response = llm.complete(prompt)

# What could be underneath:
# - Ollama (local)
# - OpenAI API
# - Anthropic API
# - Groq
# - Any future provider
```

**Lesson:** Model abstraction isn't premature optimization — it's just good design. The model is a dependency, not a core.

---

### Layer 4 — Agent Layer (`agent.py`)

The orchestrator. This is where the "agentic" behavior lives.

Responsibilities:
- Read current learning state
- Decide the next skill
- Build the right prompt for each stage (explain → exercise → evaluate)
- Call the LLM
- Parse and act on the response
- Update progress state

The agent implements a fixed loop, not open-ended autonomy. It's *agentic* in the sense that it sequences multi-step behavior, not in the sense that it autonomously plans. That distinction matters a lot in practice.

```
┌─────────────────────────────────────────────┐
│                 Agent Loop                  │
│                                             │
│  load_state → next_skill → explain          │
│       ↑                        ↓            │
│  save_state ← evaluate ← exercise           │
└─────────────────────────────────────────────┘
```

**Lesson:** Most "agents" in production are really just well-structured loops with an LLM in the middle. The architecture matters more than the model.

---

### Layer 5 — Interface Layer (`main.py`)

A minimal CLI that drives the agent loop. Keeps I/O completely separate from logic — `agent.py` never prints anything directly.

**Lesson:** Separating interface from logic means you can later add a web UI (Streamlit, FastAPI) without touching the agent.

---

## Core Architectural Concepts Learned

### 1. LLM Apps Are Systems, Not Models

Before building this, I thought "building with AI" mostly meant crafting good prompts. It doesn't. The model is one component in a larger system:

```
Knowledge layer       — what the system knows
Prompt layer          — how it communicates with the model
Model interface       — which model, abstracted away
Orchestration layer   — the control flow and state machine
Interface layer       — how humans interact with it
```

The model does the probabilistic heavy lifting. Everything else is deterministic system design.

---

### 2. Deterministic vs. Probabilistic Separation

One of the clearest design principles in this project:

| Deterministic (code owns this) | Probabilistic (model owns this) |
|---|---|
| Skill ordering | Explanations |
| Progress tracking | Exercise generation |
| Loop control | Answer evaluation |
| State management | Feedback wording |

Mixing these up makes systems fragile. If you let the model decide what skill comes next, you get non-deterministic curricula. If you hard-code evaluation logic, you lose flexibility. The boundary matters.

---

### 3. Prompt Engineering Is Constraint Engineering

Working with a small local model (`qwen2.5:3b`) made this painfully obvious. The model will do almost anything if you ask vaguely. The job of a prompt is to constrain the space of valid responses.

Things that actually helped:
- Explicitly define the output format (JSON, numbered sections, etc.)
- State what the model should *not* do, not just what it should
- Give an example of ideal output
- Keep prompts single-purpose — one prompt, one task

Small models especially need structural scaffolding. But this discipline pays off on large models too.

---

### 4. Agents Are Mostly Architecture

The word "agent" suggests autonomous reasoning. In practice, building this made it clear that:

- The *agent loop* is a design pattern, not a model feature
- An agent is a program that sequences model calls with state and control logic between them
- Reliability comes from the structure around the model, not from the model itself
- "Agentic" behavior = deterministic orchestration + selective LLM delegation

This is the most important thing I took away from the project.

---

### 5. State Management Is the Hard Part

The agent needs to remember:
- What skills have been completed
- What skill is currently active
- What stage of the loop it's in (explain / exercise / evaluate)

In this prototype, state lives in memory and resets on restart. In any real system, state persistence is a first-class concern — and the shape of that state ends up defining the agent's capabilities more than any other design decision.

---

## Known Limitations (and What They Teach)

### No Persistent Memory
Progress resets on restart. A real system would persist to `user_progress.json` or a database. This is easy to add but was left out to keep the prototype focused.

### Weak Exercise Reliability
Small models sometimes ignore constraints, produce incomplete exercises, or format inconsistently. This is a prompt engineering problem, not a model capability problem. Structured output (forcing JSON responses with a schema) would fix most of it.

### No Guided Practice Scaffold
The system goes straight from explanation to independent exercise. Better learning systems use:
```
Explanation → Worked Example → Guided Practice → Independent Exercise → Evaluation
```
Each stage is a separate agent step with a separate prompt.

### LLM-Only Evaluation
Currently the agent trusts the model entirely to evaluate answers. More robust systems layer:
- Rule-based checks (does the code run? does it produce the right output?)
- Unit tests
- LLM evaluation for semantic correctness

### No Branching or Skill Selection
The curriculum is linear. Future versions could expose skill selection to the learner or adapt difficulty based on evaluation scores.

---

## Future Directions

Things I'd explore in a next iteration:

- **Persistent state** — JSON or SQLite progress tracking
- **Structured outputs** — force JSON from the LLM for reliable parsing
- **Mastery scoring** — track score history per skill, require mastery before advancing
- **Worked examples** — add a stage between explanation and exercise
- **Vector memory** — store past answers and reference them in future prompts (RAG-lite)
- **Web interface** — Streamlit frontend over the same agent layer, no logic changes needed
- **Multi-model routing** — use a fast/small model for exercises, larger model for evaluation
- **Tool use** — let the agent run the learner's code and use the output as evaluation context

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Install Ollama
# https://ollama.com

# Pull the model
ollama pull qwen2.5:3b

# Run the agent
python main.py
```

---

## Why I Built This

I wanted to understand how the pieces of an LLM application actually fit together — not from documentation, but by building something that breaks in interesting ways when the design is wrong.

The main thing I'd tell someone starting a similar project: **resist the urge to make the model do everything**. The more you offload to the model, the less predictable your system becomes. The best AI systems are the ones where the model is doing exactly what it's uniquely good at, surrounded by tight deterministic structure that makes the overall behavior reliable.

The model is powerful. The architecture is what makes it useful.
