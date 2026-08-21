# greet example is using langgraph with custom state
from langgraph.graph import StateGraph, START, END
from typing import TypedDict


# 1. defining custom state
class SimpleState(TypedDict):
    user_name: str
    message: str
    status: str


def greet_node(state: SimpleState):
    print("\n ================== 1. GREET NODE =========")
    print("State Received:", state)  # current state

    # Update the state
    my_message = "Hello, " + state["user_name"]
    return {"message": my_message}


def status_node(state: SimpleState):
    print("\n ================== 2. STATUS NODE =========")
    print("State Received:", state)  # current state

    # Update the state
    my_status = "Workflow Completed for the user " + state["user_name"]
    return {"status": my_status}


# 2. defining the graph
workflow = StateGraph(SimpleState)

workflow.add_node("greet", greet_node)
workflow.add_node("status", status_node)

workflow.add_edge(START, "greet")
workflow.add_edge("greet", "status")
workflow.add_edge("status", END)

workflow = workflow.compile()

# generating and saving the graph visualization
graph_image = workflow.get_graph().draw_mermaid_png()
with open("examples/ex2_greet.png", "wb") as f:
    f.write(graph_image)

result = workflow.invoke({"user_name": "Alice"})
print(result)
