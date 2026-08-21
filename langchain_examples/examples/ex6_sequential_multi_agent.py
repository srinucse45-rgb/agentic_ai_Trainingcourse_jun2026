# multiagent system without tools
from langchain.agents import create_agent
from dotenv import load_dotenv

# load the env variables
load_dotenv()

# let's create the first agent
writer_agent = create_agent(
    model="openai:gpt-5.5",
    system_prompt="""
				You are a creative writer, working in a top media company. 
				Your task is to write engaging content and provide insightful
					updates on various topics.
			""",
)

# let's create the second agent
editor_agent = create_agent(
    model="openai:gpt-5.5",
    system_prompt="""
				You are an editor, working in a top media company. 
				Your task is to review the draft content written by writer and provide 
				constructive feedback to enhance the quality and engagement of the content
				and along with it, you rewrite if necessary.
			""",
)

print("======Created 2 agents==========")


def sequential_pipeline(topic: str):
    print("======Executing writer agent ==========")
    # let's write the sequential execution pipeline
    writer_result = writer_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""Generate engaging content on the topic: {topic}""",
                }
            ]
        }
    )

    print("======Writer agent's draft is ready ==========")
    print(writer_result["messages"][-1].content)

    print("*************Sending writer's draft to editor **********")
    # let's write the sequential execution pipeline
    editor_result = editor_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
											Review the following content: 
											{writer_result["messages"][-1].content}

											Enhance if it is needed to make more engaging, clear, and insightful 
											while keeping the original meaning intact.

											Also provide a short feedback section covering: 
												- What was improved
												- Why the improvements help 
												- Any remaining suggestions

											Focus on: 
												- Clarity 
												- Readability 
												- Flow 
												- Engagement
												- Grammar and wording 
											
											You must provide 3 titles to this written content and recommend 
											one of the 3.
									""",
                }
            ]
        }
    )

    print("======Editor agent's output is ready ==========")
    print(editor_result["messages"][-1].content)


sequential_pipeline("How AI Agents will transform the way businesses run")
