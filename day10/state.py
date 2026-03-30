from typing import TypedDict, List

class AgentState(TypedDict):
    # The problem description provided by user
    problem: str
    # The list of steps generated so far
    steps: List[str]
    # To track which step we are currently solving
    current_step: int
    # The final combined solution
    solution: str