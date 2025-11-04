# Multi-Agent LinkedIn Blog Post Writer

This project is a multi-agent system designed to automate the creation of SEO-optimized LinkedIn blog posts. The system uses a sequential workflow where each agent performs a specialized task: researching a topic, writing a draft, and refining it for SEO.

The application is built as a command-line tool and is wrapped in a user-friendly Streamlit web interface.

## Features
- **Web Research Agent:** Uses the Tavily API to find relevant, up-to-date information on any given topic.
- **Blog Writer Agent:** Uses a Hugging Face language model (`Qwen/Qwen2-0.5B-Instruct`) to generate a structured blog post based on the research.
- **SEO Improvement Agent:** Analyzes the draft and rewrites it with SEO best practices in mind, including an optimized title and meta description.
- **Interactive UI:** A Streamlit application provides a simple interface for users to enter a topic and receive the final blog post.

## How to Run
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `.\venv\Scripts\Activate.ps1` (Windows) or `source venv/bin/activate` (Mac/Linux).
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file and add your `TAVILY_API_KEY` and `HUGGINGFACE_HUB_TOKEN`.
6. Run the Streamlit app: `streamlit run app.py`

## Technologies Used
- **Frontend:** Streamlit
- **Web Search:** Tavily API
- **Language Models:** Hugging Face Transformers
- **Core Models:** `Qwen/Qwen2-0.5B-Instruct`