from graph import app
from dotenv import load_dotenv

load_dotenv()

def run_workflow():
    user_problem = input("What problem should I solve step-by-step? ")
    
    initial_state = {
        "problem": user_problem,
        "steps": [],
        "current_step": 0,
        "solution": ""
    }

    print("\n--- Starting Stateful Workflow ---")
    
    final_output = ""
    
    # We stream the events. The last event contains the final state.
    for event in app.stream(initial_state):
        for node_name, state_update in event.items():
            print(f"\n[Node '{node_name}' finished]")
            # Update our local tracker with whatever the node returned
            if 'solution' in state_update:
                final_output = state_update['solution']

    print("\n================ FINAL SOLUTION ================")
    print(final_output)
    print("================================================")

if __name__ == "__main__":
    run_workflow()