# introducing checkpoint
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI  # uv add langchain-openai python-dotenv
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5.5")

# users preference
LONG_TERM_MEMORY = ["user prefers simple explanations"]

# original content from vector db
DOCUMENTS = {
    "solar_system": "The Solar System consists of the Sun, eight planets, their moons, dwarf planets, asteroids, comets, and other celestial bodies bound by gravity. It formed about 4.6 billion years ago from a collapsing cloud of gas and dust.",
    "rag_system": "A Retrieval-Augmented Generation (RAG) system combines information retrieval with a language model to generate accurate, context-aware responses. It retrieves relevant documents from a knowledge base before generating an answer.",
}


# state
class AgentState(TypedDict):
    query: str
    memory: List[str]
    context: str
    answer: str
    is_good: bool
    attempts: int


def retrieve_memory_node(state: AgentState):
    print("-------- Retrieving Already saved Memory ----------")
    return {**state, "memory": LONG_TERM_MEMORY}


def retrieve_docs_node(state: AgentState):
    print("-------- Retrieving Chunks from Vector DB ----------")

    query = state["query"].lower()
    context = ""

    # The following is a fake search -- replace the logic properly with your own tools
    for key, value in DOCUMENTS.items():
        if key in query:
            context += value + "\n"

    if not context:
        context = "No relevant documents found!"

    return {**state, "context": context}


def generate_node(state: AgentState):
    print("-------- Generating Answer ----------")
    memory_text = "\n".join(state["memory"])

    prompt = f"""
        User Preferences: {memory_text}

        Context: 
        {state['context']}

        Question: 
        {state['query'].lower()}

        Answer clearly and exactly without exaggerating. 
        You are a RAG bot. Do not generate answers on your own
    """

    answer = llm.invoke(prompt).content
    return {**state, "answer": answer, "attempts": state["attempts"] + 1}


def evaluate_node(state: AgentState):
    print("-------- Evaluating Answer ----------")
    memory_text = "\n".join(state["memory"])

    prompt = f"""
            User Preferences: {memory_text}

            Question: {state['query'].lower()}

            Context: {state['context']}

            Answer: {state["answer"]}
    
            Is the answer is correct and complete based on the context?
            Respond with only: yes or no
        """

    result = llm.invoke(prompt).content
    return {**state, "is_good": result == "yes"}


def route(state: AgentState):
    if state["is_good"] or state["attempts"] >= 3:
        return "NO_RETRY_REQUIRED"

    return "RETRY_REQUIRED"


workflow = StateGraph(AgentState)
workflow.add_node("memory", retrieve_memory_node)
workflow.add_node("search", retrieve_docs_node)
workflow.add_node("generate", generate_node)
workflow.add_node("evaluate", evaluate_node)

workflow.add_edge(START, "memory")
workflow.add_edge("memory", "search")
workflow.add_edge("search", "generate")
workflow.add_edge("generate", "evaluate")

workflow.add_conditional_edges(
    "evaluate", route, {"RETRY_REQUIRED": "generate", "NO_RETRY_REQUIRED": END}
)


checkpoint = InMemorySaver()

# compiling the graph with checkpointing
app = workflow.compile(checkpointer=checkpoint)


# generating and saving the graph visualization
graph_image = app.get_graph().draw_mermaid_png()
with open("examples/ex10_rag_system.png", "wb") as f:
    f.write(graph_image)


# generate random chat id
chatId = "6a6197c6-23f0-83ee-92c2-e440d204f3d6"

result = app.invoke(
    {
        "query": "langgraph",
        "memory": [],
        "context": "",
        "answer": "",
        "is_good": False,
        "attempts": 0,
    },
    config={"configurable": {"thread_id": chatId}},
)

print("Final Answer: ", result["answer"])


# How to access the saved checkpoint
# saved_state = app.get_state({"configurable": {"thread_id": chatId}})
# print(saved_state.values)

# # Inspect the checkpoint history
# history = list(app.get_state({"configurable": {"thread_id": chatId}}))

# for single_checkpoint in history:
#     print(single_checkpoint)


# what tables will get auto create if you are using PostgresSaver
# checkpoints, checkpoint_blobs, checkpoint_writes

# what will be stored in checkpoint data
# graph state, channel values, node execution progress, metadata, thread id,
# checkpoint id , parent checkpoint (for branching/resuming)
