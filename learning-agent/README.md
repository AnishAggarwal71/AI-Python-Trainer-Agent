```markdown
# Personal AI Learning Agent (CLI)

A minimal AI-powered learning agent built to understand how modern **LLM applications are architected and orchestrated**.

This project is intentionally simple and built as a **learning exercise**, not a production-ready product. The goal was to understand how to design AI systems where deterministic program logic works together with a language model.

The agent runs locally using **Ollama** and a small open model.

---

# What This Project Does

The program acts as a simple **AI tutor in the terminal**.

Workflow:

1. Determine the next skill from a predefined skill graph
2. Explain the concept using an LLM
3. Generate a practice exercise
4. Accept the learner’s answer
5. Evaluate the response
6. Mark the skill as completed

Example flow:

```

Next Skill: Python Variables

Explanation:
...

Exercise:
...

Your answer: x = 10

Evaluation:
Score: 3/5

```

---

# Project Architecture

The system was intentionally separated into layers to mirror how real AI products are structured.

```

learning-agent

skills.py   → Knowledge Layer
prompts.py  → Prompt Layer
llm.py      → Model Interface Layer
agent.py    → Agent / Orchestration Layer
main.py     → Interface Layer (CLI)

```

---

# Layer Breakdown

## Knowledge Layer

`skills.py`

Defines the **skill graph and dependencies**.

Example:

```

python_variables
↓
python_loops
↓
python_dicts

```

The curriculum is deterministic so the LLM cannot hallucinate learning paths.

---

## Prompt Layer

`prompts.py`

Stores reusable prompt templates that instruct the LLM to:

- explain concepts
- generate exercises
- evaluate answers

Separating prompts from logic makes the system easier to iterate on.

---

## Model Interface Layer

`llm.py`

Handles interaction with the language model.

Currently uses:

```

Ollama + qwen2.5:3b

```

Because the model is abstracted behind an interface, the system could easily switch to:

- OpenAI
- Anthropic
- Groq
- different local models

without changing the rest of the code.

---

## Agent Layer

`agent.py`

The **core orchestrator** of the system.

Responsibilities:

- determine the next skill
- generate explanations
- generate exercises
- evaluate answers
- update learning progress

The agent coordinates:

```

skills → prompts → LLM

```

---

## Interface Layer

`main.py`

Provides a simple **CLI interface** that runs the learning loop.

```

python main.py

```

---

# Key Concepts Learned

This project focused on understanding **how LLM applications are structured**, not just how to call an API.

### 1. LLM Applications Are Systems

A real AI tool consists of multiple layers:

```

Knowledge layer
Prompt layer
Model interface
Agent orchestration
User interface

```

The model itself is only one component.

---

### 2. Deterministic Logic + Probabilistic Reasoning

The system separates:

Deterministic logic:

- skill dependencies
- curriculum flow
- progress tracking

Probabilistic reasoning:

- explanations
- exercise generation
- answer evaluation

This separation makes the system more reliable.

---

### 3. Prompt Engineering is Constraint Engineering

Small models behave much better when prompts:

- clearly define output structure
- explicitly state constraints
- enforce formats (JSON, sections, etc.)

---

### 4. Model Abstraction is Important

The architecture was designed so the model provider can be swapped easily:

```

agent → LLMClient → model provider

```

Only `llm.py` would need to change to switch from Ollama to OpenAI or another provider.

---

### 5. AI Products Are Mostly System Design

The majority of work in LLM products is not the model itself but:

- architecture
- control logic
- prompt structure
- state management
- user interaction

---

# Limitations of This Prototype

This project intentionally kept the system minimal.

### No Persistent Memory

Progress resets when the program restarts.

A better system would store progress in:

```

user_progress.json

```

or a database.

---

### Weak Exercise Reliability

Small models sometimes:

- generate incomplete exercises
- ignore constraints
- produce inconsistent formatting

This can be improved with:

- stronger prompts
- structured outputs
- larger models

---

### No Guided Practice

The system jumps directly from explanation to exercise.

Better learning systems include:

```

Explanation
Worked Example
Guided Practice
Independent Exercise
Evaluation

```

---

### No Skill Selection

The system automatically selects the next skill.

Future versions could allow the learner to choose:

```

1. Python Loops
2. Python Functions
3. Python Lists

```

---

### Weak Evaluation Logic

Currently the agent relies entirely on the LLM to judge answers.

More robust systems combine:

- rule-based checks
- unit tests
- LLM evaluation

---

# Future Improvements

Possible upgrades:

- persistent user progress tracking
- skill mastery scoring
- worked examples before exercises
- vector memory for storing learning history
- web interface (Streamlit / FastAPI)
- retrieval-augmented explanations (RAG)

---

# How to Run

Install dependencies:

```

pip install -r requirements.txt

```

Install Ollama:

```

https://ollama.com

```

Download the model:

```

ollama run qwen2.5:3b

```

Start the learning agent:

```

python main.py

```

---

# Purpose of This Project

This repository is meant to serve as **a reference project for understanding how AI systems are structured**.

The focus was on learning:

- AI application architecture
- agent orchestration
- prompt design
- model abstraction
- system thinking for LLM products
```
