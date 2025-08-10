# azure-openai-test
LangGraph and lagchain chatbot using Azure OpenAI 
# Azure OpenAI GPT-3.5 Turbo Chatbot

This is a simple Python command-line chatbot using Azure OpenAI GPT-3.5 Turbo model.

## Features

- Conversational AI powered by Azure OpenAI Service.
- Chat loop with user input and AI response.
- Supports exiting the chat by typing "exit" or "quit".

## Prerequisites

- Python 3.8+
- Install the official OpenAI Python SDK:
  ```bash
  pip install openai


This project is a chatbot backend built with **Flask**, **LangGraph**, and **LangChain's AzureChatOpenAI** integration. It supports conversational memory per user session and can answer general questions or perform simple math calculations.

---

## Features

- Conversational AI powered by Azure OpenAI GPT models.
- Stateful dialogue management using LangGraph.
- Per-session conversation memory with LangChain's `ConversationBufferMemory`.
- Calculator support for simple math expressions.
- REST API for integration with frontend apps.
- CORS enabled for cross-origin requests.




-----------------------------------------------------------------------------
1. Learn Azure OpenAI Basics
Objectives:
•	Understand what Azure OpenAI is
•	Learn how it differs from OpenAI.com
•	Learn to access models via the Azure portal
Concepts:
•	What is LLM?
•	Azure OPEN AI Models
•	Tokens, prompts, completions
•	Azure resource creation
•	API Key & Endpoint config
Task:
•	Create an Azure OpenAI Resource
•	Use the Playground to test a chat prompt
•	Write a Python script to call Azure OpenAI API
________________________________________
2. Learn LangChain & LangGraph Basics
Objectives:
•	Understand how LangChain connects tools, memory, and LLMs
•	Learn how LangGraph builds multi-node LLM workflows
Concepts:
•	LangChain: LLMs, Chains, Memory, Tools
•	LangGraph: Graph, Nodes, Edges, State Management
•	Differences between linear chains and LangGraph DAGs
Task:
•	Install langchain, langgraph, openai Build a simple LangChain with:
o	Prompt Template
o	ChatOpenAI model
o	Memory (ConversationBufferMemory)
•	Then build a LangGraph flow with:
o	Input Node → LLM Node → Output Node
________________________________________
3. Build a Simple LangGraph Flow
Goal:
Create a minimal chatbot using LangGraph with conversational memory.
Sample Workflow:
1.	User Input Node
2.	LLM Node (using Azure GPT-3.5)
3.	Memory Node (stores past messages)
4.	Output Node (returns response)
________________________________________







4. What is Docker & How to Use It
Objectives:
•	Understand what Docker is and why it's used
•	Learn how to create a containerized environment for your chatbot
Concepts:
•	Image vs Container
•	Dockerfile
•	Docker Compose
•	Benefits: Isolation, Portability, Consistency
Task:
•	Install Docker Desktop
•	Create a Dockerfile for your LangGraph chatbot
________________________________________
5. What is DAG & How to Implement It
Objectives:
•	Understand DAG (Directed Acyclic Graph) concept in LangGraph
•	Learn how workflows are modeled as nodes and edges
Concepts:
•	DAG = No cycles, directed from input to output
•	LangGraph is a DAG engine for LLM workflows
•	Each node = a function (e.g., LLM call, tool use)
•	Each edge = data/state transition
Task:
•	Build a DAG with multiple decision paths:
o	If user asks for a calculation, route to a tool
o	If user asks for text, route to LLM


---

## Setup

 Clone the repository


