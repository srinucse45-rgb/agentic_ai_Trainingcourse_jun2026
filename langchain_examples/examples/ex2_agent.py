from langchain.agents import create_agent
from dotenv import load_dotenv

# load the env variables
load_dotenv()

my_agent = create_agent(
    model="openai:gpt-5.5",  # brain of the agent
    system_prompt="""You are a helpful assistant. " \
    "Your answers should be super simple and easy to understand. 
	Do not talk much""",  # roles and goals
)

response = my_agent.invoke(
    {"messages": [{"role": "user", "content": "what's the weather in chennai?"}]}
)

print(response["messages"][-1].text)

# This is looking like an agent. but it is not. it doesn't know how to fetch weather.
