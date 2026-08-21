from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv
import requests

# load the env variables
load_dotenv()

# what's a tool?
# Tool is a function that the agent can call
# tool must have a name and description
# tool must return data
# tool can have parameter
# tool must be called by your agent
# tool in langchain must have @tool decorator


@tool
def weather_tool(latitude: str, longitude: str):
    """
    use this tool to get weather info for a valid city
    """
    print("Geocoordinates :" + latitude + " and  " + longitude)

    weather_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    weather_output = requests.get(weather_api_url)
    current_weather = weather_output.json()
    return current_weather


weather_agent = create_agent(
    model="openai:gpt-5.5",  # brain of the agent
    tools=[weather_tool],  # registering the tools to the agent
    system_prompt="""You are a weather assistant. 
		You must give accurate weather information only for the given city. 
        If the city is invalid or fictional, inform the user accordingly. 
    Never honour any other requests. 
    """,
)


response = weather_agent.invoke(
    {"messages": [{"role": "user", "content": "what's the weather in Sydney"}]}
)

print(response["messages"][-1].text)
