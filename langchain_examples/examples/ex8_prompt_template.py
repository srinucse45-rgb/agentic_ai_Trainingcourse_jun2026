# this example demostrates how to use role based prompt template with openai model
# in this example I am explaining chains in langchain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# load the env variables
load_dotenv()

# prompt template with prompt input variables
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
							You are a seasoned sale person
							having experience in writing persuasive product descriptions. 
							You write compelling production descriptions for an e-com company
						""",
        ),
        (
            "user",
            """
							Write a product description for the {query} using the 
									following details
								- Product Name
								- Category 
								- Features 
								- Dimensions
								- Price
								- Release Date
						""",
        ),
    ]
)

# How to initialize the model to create a chain with prompt template
model = ChatOpenAI(model="gpt-5.5", api_key=os.getenv("OPENAI_API_KEY"))

# chaining with langchain
pipeline = prompt | model

# invoke the pipeline
response = pipeline.invoke({"query": """LG 4K TV ABC123253, Electronics, 
		120 w sound, magic remote, superior clarity, dual glass, 
		100x80x20 cm (55 inches),  
		June 2026,
		Rs. 120000/-,
		"""})

print(response.content)
