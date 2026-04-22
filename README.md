
```markdown
# Agentic AI Learning 🤖

Welcome to my learning repository for **Agentic AI**! This project serves as a personal workspace where I practice, implement, and document all the concepts and techniques I am learning about AI agents, orchestration, and Retrieval-Augmented Generation (RAG).

## 🧠 About This Repository

As I dive deeper into the world of Agentic AI, this repository acts as a hands-on sandbox. It contains various scripts, modules, and sub-projects focused on building intelligent, autonomous agents and connecting them with modern AI frameworks. All current implementations are written entirely in **Python**.

## 📁 Repository Structure & Topics

Here is an overview of the modules and topics actively being explored in this repository:

### 1. `learn_langgraph/`
* **Focus:** Agent orchestration and state management.
* **Description:** Contains practice code and implementations using LangGraph. This module explores how to build stateful, multi-actor applications with LLMs by modeling agent workflows and reasoning cycles as graphs.

### 2. `mem_agent/`
* **Focus:** AI Agent Memory.
* **Description:** Experiments with giving AI agents the ability to remember past context. This includes implementing conversation history (short-term memory) and potentially semantic retrieval (long-term memory) to make agents more contextual and conversational.

### 3. `rag_queue/`
* **Focus:** Retrieval-Augmented Generation (RAG).
* **Description:** Contains implementations related to building robust RAG pipelines. It explores document retrieval, data queuing, and grounding LLM responses in external data sources.

### Core Standalone Scripts
* **`indexing.py` & `index.py`**: Scripts dedicated to data ingestion, chunking, embedding, and indexing documents into a vector database for RAG pipelines.
* **`thought.py`**: An implementation focusing on the reasoning engine of an AI agent (e.g., Chain of Thought, ReAct prompting frameworks).
* **`cheese.pdf`**: A sample data document used locally for testing document parsing, text extraction, and vector indexing capabilities.

## 🛠️ Technologies & Concepts

* **Language:** Python
* **Core Concepts:** Agentic AI, Retrieval-Augmented Generation (RAG), Agent Memory, Chain of Thought Processing
* **Libraries/Frameworks:** LangChain, LangGraph (indicated by active modules)

## 🚀 Getting Started

To explore or run the code in this repository locally:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/harshendrak/Learning.git](https://github.com/harshendrak/Learning.git)
   cd Learning
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install necessary dependencies:**
   Depending on the script you want to run, you may need to install standard AI packages:
   ```bash
   pip install langchain langgraph openai 
   ```

4. **Set up Environment Variables:**
   To run the agent scripts, you will need access to LLM APIs. Create a `.env` file in the root directory and add your keys:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## 🤝 Purpose & Feedback
This is primarily a personal learning repository to track my journey into Agentic AI. While it is not designed as an open-source library for public consumption, feedback, code reviews, or suggestions on better Agentic AI design patterns are always welcome! Feel free to open an issue if you want to discuss a specific implementation.
```