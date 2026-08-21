from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# load the env variables
load_dotenv()

# initializing the model
model = ChatOpenAI(model="gpt-5.5")

# researcher agent
researcher_agent = create_agent(
    model=model,  # brain
    system_prompt="""
			You are a researcher. Provide well-researched, detailed, 
					factually correct information on any topic
		""",
)


# exposing the above agent via a tool
@tool
def researcher_tool(query: str):
    """call the research agent to gather necessary information"""
    print("Calling researcher_tool")
    print(query)
    print("========")
    researcher_output = researcher_agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    return researcher_output["messages"][-1].content


# writer agent
writer_agent = create_agent(
    model=model,  # brain
    system_prompt="""
			You are a writer. 
      Write clear, concise, engaging content on any topic
		""",
)


# exposing the above agent via a tool
@tool
def writer_tool(query: str):
    """call the writer agent to write or summarize the content"""
    print("Calling writer_tool")
    print(query)
    print("========")
    writer_output = writer_agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    return writer_output["messages"][-1].content


# supervisor agent
supervisor_agent = create_agent(
    model=model,  # brain
    tools=[researcher_tool, writer_tool],
    system_prompt=(
        """You are a supervisor agent. You coordinate tasks between specialized agents:
        Analyze the requirement clearly and decide what action to take.
        - Use researcher_tool if you feel like more research to be done on the query 
        - Use writer_tool for writng, editing, summarizing
        Delegate tasks to the appropriate tool and combine their outputs to
        answer the user."""
    ),
)

my_task = " the benefits of protein and write a 3-paragraph summary"

supervisors_output = supervisor_agent.invoke(
    {"messages": [{"role": "user", "content": my_task}]}
)

print("========")
print(supervisors_output["messages"][-1].content)
