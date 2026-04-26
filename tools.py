from langchain.tools import tool
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
from bs4 import BeautifulSoup
import requests

load_dotenv()
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def search_web(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Return Titles, URLs and snippets."""
    results = tavily_client.search(query=query, max_results=5)
    out=[]
    for result in results['results']:
        out.append(
            f"Title:{result['title']}\nURL:{result['url']}\nSnippet:{result['content']}\n\n"
        ) 
    return "\n---------------\n".join(out)

@tool
def get_webpage_content(url: str) -> str:
    """Get the content of a webpage from a URL."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, 'html.parser')
        for tag in soup(['script', 'style', 'footer', 'nav','header']):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Error fetching webpage: {str(e)}"
