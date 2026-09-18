import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from langgraph.graph import START, END
from langgraph.graph.state import StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated
from IPython.display import Image

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGGRAPH_PROJECT"] = "TestProject"

llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0)


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


graph_builder = StateGraph(State)


def make_tool_graph():

    @tool
    def add(a: int, b: int):
        """add two numbers"""
        return a + b

    tools = [add]
    tool_node = ToolNode(tools)

    llm_with_tools = llm.bind_tools(tools)

    def call_llm(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    ##graph creating

    graph_builder = StateGraph(State)

    ##adding nodes
    graph_builder.add_node("call_llm", call_llm)
    graph_builder.add_node("tools", ToolNode(tools))

    ##adding edges
    graph_builder.add_edge(START, "call_llm")
    graph_builder.add_conditional_edges("call_llm", tools_condition)
    graph_builder.add_edge("tools", "call_llm")

    # memory = InMemorySaver()
    graph = graph_builder.compile()

    return graph


tool_agent = make_tool_graph()
