# ResearchFlow AI 🔬

ResearchFlow AI is an advanced, multi-agent system that autonomously researches, synthesizes, and critiques information on any given topic. Powered by LangGraph and Groq, this application employs a team of specialized AI agents working in tandem to deliver comprehensive and accurate research reports.

## Features ✨

- **Multi-Agent Architecture**: Uses a dedicated team of AI agents for distinct tasks (Search, Reader, Writer, Critic).
- **Automated Web Research**: Intelligently searches the web to find the most relevant and reliable information.
- **Deep Content Scraping**: Extracts and synthesizes detailed content from top web sources.
- **Automated Review**: A built-in Critic Agent evaluates the generated report for quality and accuracy.
- **Interactive UI**: A sleek, modern Streamlit frontend for interacting with the multi-agent pipeline and viewing detailed results and feedback.

## Technology Stack 🛠️

- **Framework**: [LangChain](https://www.langchain.com/)
- **LLM Engine**: [Groq](https://groq.com/) (Llama 3)
- **Web Search API**: [Tavily](https://tavily.com/)
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Web Scraping**: BeautifulSoup4 & Requests

## Getting Started 🚀

### Prerequisites
- Python 3.8+
- [Groq API Key](https://console.groq.com/keys)
- [Tavily API Key](https://app.tavily.com/home)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mystery-Shashwat/ResearchFlow.git
   cd ResearchFlow
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .\.venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

### Usage

Start the Streamlit application by running:
```bash
streamlit run app.py
```


## Architecture Details 🤖

The pipeline runs sequentially through four main agents:
1. **Search Agent**: Evaluates the topic and retrieves a list of promising sources and snippets using Tavily.
2. **Reader Agent**: Analyzes the search results and scrapes deep content from the most relevant URLs using BeautifulSoup.
3. **Writer Agent**: Synthesizes the scraped data and search results into a structured, professional report.
4. **Critic Agent**: Reviews the final report, scores it, identifies strengths, and provides actionable feedback on areas for improvement.
