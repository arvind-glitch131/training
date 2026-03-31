import asyncio
import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server

server = Server("Stateful-Finance-Server")

# Internal Server Memory
transaction_history = []

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="record_transaction",
            description="Calculates profit/loss for a single deal and stores it.",
            inputSchema={
                "type": "object",
                "properties": {
                    "buy_price": {"type": "number"},
                    "sell_price": {"type": "number"},
                    "item_name": {"type": "string"}
                },
                "required": ["buy_price", "sell_price", "item_name"],
            },
        ),
        types.Tool(
            name="get_final_summary",
            description="Retrieves the total profit/loss from all previous transactions.",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    global transaction_history
    
    if name == "record_transaction":
        buy = arguments.get("buy_price")
        sell = arguments.get("sell_price")
        item = arguments.get("item_name")
        diff = sell - buy
        
        # Save to server memory
        transaction_history.append({"item": item, "amount": diff})
        
        status = "Profit" if diff >= 0 else "Loss"
        return [types.TextContent(type="text", text=f"Recorded {item}. {status} of ${abs(diff):.2f} added to history.")]

    if name == "get_final_summary":
        total = sum(t["amount"] for t in transaction_history)
        count = len(transaction_history)
        return [types.TextContent(type="text", text=f"Total Transactions: {count}. Net Profit/Loss: ${total:.2f}")]
    
    raise ValueError(f"Tool {name} not found")

async def main():
    # Explicitly run the server on stdio
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="Stateful-Finance-Server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    # This was the missing required argument:
                    experimental_capabilities={}, 
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())