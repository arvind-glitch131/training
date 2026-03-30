from langgraph.graph import StateGraph, START, END
from state import AgentState
from nodes import problem_planner, step_solver

# 1. Initialize the Graph with our State schema
workflow = StateGraph(AgentState)

# 2. Add Nodes
workflow.add_node("planner", problem_planner)
workflow.add_node("solver", step_solver)

# 3. Define Edges (The Logic Flow)
workflow.add_edge(START, "planner")
workflow.add_edge("planner", "solver")

# 4. Conditional Edge: Decide if we need to solve more steps
def should_continue(state: AgentState):
    if state["current_step"] < len(state["steps"]):
        return "continue"
    return "end"

workflow.add_conditional_edges(
    "solver",
    should_continue,
    {
        "continue": "solver", # Loop back to solve next step
        "end": END            # We are done
    }
)

# 5. Compile the Graph
app = workflow.compile()