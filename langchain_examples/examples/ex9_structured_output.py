from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv
from tavily import TavilyClient  # uv add tavily-python
from pydantic import BaseModel, Field
from typing import List
import os

# load the env variables
load_dotenv()


# 1. let's define the structure of 1 news (Output Schema)
class NewsArticle(BaseModel):
    "A single News Article"

    title: str = Field(
        description="Title of the news article", min_length=5, max_length=100
    )
    summary: str = Field(description="Brief Summary of the news article")
    url: str = Field(description="url of the news, empty string if not available")
    source: str = Field(description="Publisher or Source name")


# 2. let's make the news article list
class AINewsResponse(BaseModel):
    """Structured response from AI"""

    topic: str = Field(description="The specific topic")
    articles: List[NewsArticle] = Field(description="List of relevant news found")
    overall_summary: str = Field(description="High level summary of the topic")


# setting up tavily search client
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search_tool(query: str):
    """use this tool to search the web"""
    print("Searching the web for the query: ")
    print(query)
    search_results = tavily_client.search(query)
    return search_results


general_purpose_agent = create_agent(
    model="openai:gpt-5.5",
    tools=[web_search_tool],
    response_format=AINewsResponse,  # it must output in this structure
    system_prompt="""
			You are a helpful assistant capable of 
			getting real-time information from the web.  
      Use the websearch tool to answer the query. 
      If you are not able to find right/relevant info for the query, 
      tell the user that the answer not found, instead of making up answers.
		""",
)


response = general_purpose_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Tell me about latest AI News",
            }
        ]
    }
)

news: AINewsResponse = response["structured_response"]

# print(news)  # pydantic format of the structure response

# if you only json format
print(news.model_dump_json(indent=2))
