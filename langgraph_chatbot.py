from langgraph.graph import StateGraph
from typing import TypedDict, List
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

# Load env vars from .env file
load_dotenv()

# Azure OpenAI LLM config
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0.7,
)

# Define prompt template for the conversation
prompt_template = PromptTemplate(
    input_variables=["history", "input"],
    template="""
The following is a conversation between a helpful AI assistant and a human.

Conversation history:
{history}

Human: {input}
AI:""",
)

# Define state type
class ChatState(TypedDict):
    user_input: str
    history: str
    messages: List

# Initialize conversation memory
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# Input node: Get user input and add to state
def input_node(state: ChatState) -> ChatState:
    user_input = input("You: ").strip()
    if not user_input:
        print("⚠️ Please enter something.")
        return state
    state["user_input"] = user_input
    return state

# LLM node: Use prompt template + memory to get response
def llm_node(state: ChatState) -> ChatState:
    # Get conversation history text from memory buffer
    history_messages = memory.buffer  # List of messages
    history_text = ""
    for msg in history_messages:
        role = "Human" if msg.type == "human" else "AI" if msg.type == "ai" else "System"
        history_text += f"{role}: {msg.content}\n"
    state["history"] = history_text.strip()
    
    # Format prompt text
    prompt_text = prompt_template.format(history=state["history"], input=state["user_input"])
    
    # Invoke LLM with prompt wrapped as SystemMessage
    response = llm.invoke([SystemMessage(content=prompt_text)])
    
    # Update memory with latest interaction
    memory.save_context({"input": state["user_input"]}, {"output": response.content})
    
    # Append messages to state messages list
    state.setdefault("messages", [])
    state["messages"].append(HumanMessage(content=state["user_input"]))
    state["messages"].append(AIMessage(content=response.content))
    
    return state

# Memory node (optional here because using ConversationBufferMemory)
def memory_node(state: ChatState) -> ChatState:
    # Memory handled inside llm_node
    return state

# Output node: print AI response
def output_node(state: ChatState) -> ChatState:
    print("AI:", state["messages"][-1].content)
    return state

# Build LangGraph workflow
builder = StateGraph(ChatState)
builder.add_node("input", input_node)
builder.add_node("llm", llm_node)
builder.add_node("memory", memory_node)
builder.add_node("output", output_node)

# Define flow: input -> llm -> memory -> output -> input (loop)
builder.set_entry_point("input")
builder.add_edge("input", "llm")
builder.add_edge("llm", "memory")
builder.add_edge("memory", "output")
builder.add_edge("output", "input")

# Compile the graph
graph = builder.compile()

print("🔹 LangGraph Chatbot with LangChain Memory\nType Ctrl+C to exit.")

try:
    graph.invoke({
        "user_input": "",
        "history": "",
        "messages": []
    })
except KeyboardInterrupt:
    print("\n👋 Chat ended.")
