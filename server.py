from flask import Flask, request, jsonify
from langgraph.graph import StateGraph
from typing import TypedDict, List
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
import re
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0.7,
)

# In-memory user memory storage: {session_id: ConversationBufferMemory}
user_memories = {}

class ChatState(TypedDict):
    user_input: str
    messages: List

def get_memory(session_id: str) -> ConversationBufferMemory:
    # Create memory for session if not exists
    if session_id not in user_memories:
        user_memories[session_id] = ConversationBufferMemory(memory_key="history", return_messages=True)
    return user_memories[session_id]

def calculator_node(state: ChatState, memory: ConversationBufferMemory) -> ChatState:
    expr = state["user_input"]
    try:
        if not re.fullmatch(r"[0-9+\-*/().\s]+", expr):
            raise ValueError("Invalid characters in expression.")
        result = eval(expr)
        answer = f"Result: {result}"
    except Exception as e:
        answer = f"Sorry, I couldn't calculate that. Error: {e}"

    state.setdefault("messages", [])
    state["messages"].append(HumanMessage(content=expr))
    state["messages"].append(AIMessage(content=answer))

    memory.save_context({"input": expr}, {"output": answer})
    return state

def llm_node(state: ChatState, memory: ConversationBufferMemory) -> ChatState:
    memory_data = memory.load_memory_variables({})
    chat_history = memory_data.get("history", [])

    chat_history.append(HumanMessage(content=state["user_input"]))
    response_message = llm.invoke(chat_history)

    state.setdefault("messages", [])
    state["messages"].append(HumanMessage(content=state["user_input"]))
    state["messages"].append(response_message)

    memory.save_context({"input": state["user_input"]}, {"output": response_message.content})
    return state

def memory_node(state: ChatState) -> ChatState:
    return state

def output_node(state: ChatState) -> ChatState:
    return state

def decision_node(state: ChatState, memory: ConversationBufferMemory) -> ChatState:
    user_input = state.get("user_input", "").strip().lower()

    is_math_expr = bool(re.fullmatch(r"[0-9+\-*/().\s]+", user_input))
    calc_keywords = ["calculate", "solve", "compute"]

    if not user_input:
        return llm_node(state, memory)
    elif is_math_expr:
        return calculator_node(state, memory)
    elif any(k in user_input for k in calc_keywords):
        return calculator_node(state, memory)
    else:
        return llm_node(state, memory)

builder = StateGraph(ChatState)

# Updated node functions now require memory argument; use lambdas to inject memory:
builder.add_node("decision", lambda state: decision_node(state, get_memory(current_session)), return_type=dict)
builder.add_node("memory", memory_node, return_type=dict)
builder.add_node("output", output_node, return_type=dict)

builder.set_entry_point("decision")

builder.add_edge("decision", "memory")
builder.add_edge("memory", "output")

graph = builder.compile()

@app.route("/chat", methods=["POST"])
def chat():
    global current_session
    data = request.json
    user_input = data.get("user_input", "").strip()
    session_id = data.get("session_id", "default_session")  # Replace with real session or user ID

    if not user_input:
        return jsonify({"error": "user_input is required"}), 400

    # Set current session globally for graph nodes to access memory
    current_session = session_id

    initial_state: ChatState = {"user_input": user_input, "messages": []}

    state = graph.invoke(initial_state)

    ai_message = None
    for msg in reversed(state.get("messages", [])):
        if isinstance(msg, AIMessage):
            ai_message = msg.content
            break

    if not ai_message:
        ai_message = "Sorry, no response generated."

    return jsonify({"response": ai_message})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
