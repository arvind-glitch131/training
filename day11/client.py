import asyncio
import os
import warnings
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
load_dotenv()

async def run_stateful_client():
    server_params = StdioServerParameters(command="python", args=["server.py"])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
            
            print("--- Persistent Finance Session Active ---")

            while True:
                print("\n1. Record New Transaction")
                print("2. Get Final Summary & Exit")
                choice = input("Select an option (1/2): ")

                if choice == "1":
                    item = input("Item Name: ")
                    buy = float(input("Buying Price: $"))
                    sell = float(input("Selling Price: $"))
                    
                    # Call Tool 1
                    result = await session.call_tool("record_transaction", 
                                                    arguments={"item_name": item, "buy_price": buy, "sell_price": sell})
                    print(f"\n[Server]: {result.content[0].text}")
                
                elif choice == "2":
                    # Call Tool 2 (Retrieving memory from server)
                    result = await session.call_tool("get_final_summary", arguments={})
                    summary_text = result.content[0].text
                    
                    # LLM generates final report
                    final_report = llm.invoke(f"The finance server reports: {summary_text}. Provide a concluding summary.")
                    print(f"\n--- FINAL AUDIT REPORT ---\n{final_report.content}")
                    break
                else:
                    print("Invalid choice.")

if __name__ == "__main__":
    asyncio.run(run_stateful_client())