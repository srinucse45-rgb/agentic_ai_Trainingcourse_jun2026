from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv
from tavily import TavilyClient  # uv add tavily-python
import requests
import os

# load the env variables
load_dotenv()

# what's a tool?
# Tool is a function that the agent can call
# tool must have a name and description
# tool must return data
# tool can have parameter
# tool must be called by your agent
# tool in langchain must have @tool decorator


# setting up tavily search client
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def weather_tool(latitude: str, longitude: str):
    """
    use this tool to get weather info for a valid city
    """
    print("Checking the weather for : " + latitude + " and " + longitude)

    weather_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    weather_output = requests.get(weather_api_url)
    current_weather = weather_output.json()
    return current_weather


@tool
def web_search_tool(query: str):
    """use this tool to search the web"""
    print("Searching the web for the query: ")
    print(query)
    search_results = tavily_client.search(query)
    return search_results


general_purpose_agent = create_agent(
    model="openai:gpt-5.5",
    tools=[weather_tool, web_search_tool],
    system_prompt="""
			You are a helpful assistant capable of giving weather updates,
			and real-time information from the web.
			You must provide accurate weather information for given city's latitude and longitude.
			If the city is invalid or fictional, inform the user accordingly.
      You are given access to right tools to get weather info and 
      real-time updated from the web
		""",
)


response = general_purpose_agent.invoke(
    {
        "messages": [
            # {
            #     "role": "user",
            #     "content": "what's the weather in chennai",
            # }
            # {
            #     "role": "user",
            #     "content": "tell me the gold rate in chennai",
            # }
            # {
            #     "role": "user",
            #     "content": "what's the weather in chennai and tell me the gold rate there",
            # }
            # {
            #     "role": "user",
            #     "content": "What's the weather in Chennai, London, Tokyo, and compare their gold rates?",
            # }
            # {
            #     "role": "user",
            #     "content": "What's the weather in Chennai and convert the temperature to Fahrenheit and Kelvin while also giving the gold rate in USD per ounce?",
            # }
            {
                "role": "user",
                "content": "Tell me the weather in the place where the next Olympics will be held and summarize the three biggest headlines from that country today and also give the links to original news website",
            }
        ]
    }
)

print(response["messages"][-1].text)
