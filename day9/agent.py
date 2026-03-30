import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
# Use the classic package for AgentExecutor patterns in Python 3.14+
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import file_writer

load_dotenv()

# 1. Initialize LLM (Groq)
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0
)

# 2. Define Tools
search_tool = TavilySearchResults(max_results=3)
tools = [search_tool, file_writer]

# 3. Create the Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research assistant. "
               "Step 1: Search for info. "
               "Step 2: Summarize it. "
               "Step 3: Save it to a file. "
               "Step 4: Once the file is saved, you MUST stop and give a final response starting with 'FINAL ANSWER:'"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 4. Construct Agent & Executor
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,        # <--- Safety Brake: Stops the loop after 5 steps
    early_stopping_method="generate" # <--- Tells it to give a final summary even if it's forced to stop
)

if __name__ == "__main__":
    topic = input("Enter research topic: ")
    agent_executor.invoke({"input": topic})