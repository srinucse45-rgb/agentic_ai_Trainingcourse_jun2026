# uv add python-dotenv langchain langchain-openai
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

# load the env variables
load_dotenv()

model = init_chat_model("openai:gpt-5.5")

response = model.invoke("hey!")
print(response.content)


# to run
# python examples/ex1_greet.py
