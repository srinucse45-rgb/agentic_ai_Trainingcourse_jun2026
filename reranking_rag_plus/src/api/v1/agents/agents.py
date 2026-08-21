# nodes we want
# 1. vector_search (top-k=20)
# 2. rerank
# 3. generate_answer

import os
import cohere
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from src.api.v1.states.rag_state import RAGState
from src.api.v1.tools.vector_search_tool import vector_search_node
from src.api.v1.schemas.query_schema import AIResponse
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


def _get_llm():
    return ChatOpenAI(
        model=os.getenv("OPENAI_CHAT_MODEL"), api_key=os.getenv("OPENAI_API_KEY")
    )


def rerank_node(state: RAGState):
    # establish connection with the cohere reranking model
    co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))
    # send the query and the retrieved_docs to the reranking model

    docs = state["retrieved_docs"]

    print("=======3. INSIDE rerank_node. Before calling reranker =========")
    rerank_response = co.rerank(
        model="rerank-v3.5",
        query=state["query"],
        documents=[doc.page_content for doc in docs],
        top_n=5,
    )

    # Map Cohere result indices back to LangChain Document objects
    reranked_docs = [docs[r.index] for r in rerank_response.results]

    print(f"[rerank_node] Top {len(reranked_docs)} chunks after reranking:")
    for i, r in enumerate(rerank_response.results):
        print(
            f"  Rank {i+1} | Cohere score: {r.relevance_score:.4f} | original index: {r.index}"
        )

    return {**state, "reranked_docs": reranked_docs}


def generate_answer_node(state: RAGState):
    llm = _get_llm()
    structured_llm = llm.with_structured_output(AIResponse)

    print("=========4. INSIDE GENERATE ANSWER NODE==========")

    for doc in state["reranked_docs"]:
        print("Metadata: ", doc.metadata)

    # let's prepare the context
    context = "\n\n".join(
        [
            f"[Source: {doc.metadata.get('source', 'unknown')} | Page: {doc.metadata.get('page', -1) + 1 if doc.metadata.get('page') is not None else '?'}]\n{doc.page_content}"
            for doc in state["reranked_docs"]
        ]
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                    You are a helpful assistant. Answer the user's question using only the
                    provided context.

                    IMPORTANT:
                    The context may contain chunks from MULTIPLE versions of the same
                    document (e.g. a 2025 edition and a 2026 edition).

                    When the answer differs across versions, do NOT pick only one. Instead:
                    - Lead with the most recent / current version's answer (highest year).
                    - Then explicitly note how earlier versions differed
                    (e.g. "As of the 2026 policy ...; previously, under the 2025 policy ...").
                    - If all versions agree, just give the single answer.

                    Citation rules (fill the structured fields):
                    - document_name: comma-separated list of EVERY source document you used.
                    - page_no: comma-separated page numbers, aligned with the documents above.
                    - policy_citations: a readable citation combining each document and its page
                    (e.g. "HR_Knowledge_Base_2026.pdf, Page 1; HR_Knowledge_Base_2025.pdf, Page 1").
                    - Always cite ALL versions you drew the answer from, not just one.
            """,
            ),
            (
                "human",
                """
                    Context:
                    {context}

                    Question:
                    {query}
                """,
            ),
        ]
    )

    chain = prompt | structured_llm
    result = chain.invoke({"context": context, "query": state["query"]})

    print(f"[generate_answer_node] Answer generated.")
    return {**state, "response": result.model_dump()}


def build_rag_graph():
    workflow = StateGraph(RAGState)
    workflow.add_node("vector_search", vector_search_node)
    workflow.add_node("rerank", rerank_node)
    workflow.add_node("generate_answer", generate_answer_node)

    # the following is the starting point
    workflow.set_entry_point("vector_search")

    workflow.add_edge("vector_search", "rerank")
    workflow.add_edge("rerank", "generate_answer")
    workflow.add_edge("generate_answer", END)

    search_agent = workflow.compile()

    # generating and saving the graph visualization
    graph_image = search_agent.get_graph().draw_mermaid_png()
    with open("search_agent.png", "wb") as f:
        f.write(graph_image)

    return search_agent


rag_graph = build_rag_graph()


def run_search_agent(query: str):
    print("============1. INSIDE run_search_agent ")
    initial_state = {
        "query": query,
        "retrieved_docs": [],
        "reranked_docs": [],
        "response": {},
    }

    final_state = rag_graph.invoke(initial_state)
    return final_state["response"]
