from typing import Dict, List, Optional, Tuple
import poetry_version

__version__ = poetry_version.extract(source_file=__file__)

def run_turing_machine(
    machine: Dict,
    input_: str,
    steps: Optional[int] = None,
) -> Tuple[str, List[Dict], bool]:
    
    state = machine["start state"]
    blank = machine["blank"]
    table = machine["table"]
    final_states = machine["final states"]
    
    tape = [blank] + list(input_) + [blank]
    head = 1
    
    execution_history = []
    
    step_count = 0
    while state not in final_states and (steps is None or step_count < steps):
        reading = tape[head]
        
        execution = {
            "state": state,
            "reading": reading,
            "position": head,
            "memory": ''.join(tape).strip(blank)
        }
        
        action = table[state][reading]
        
        if isinstance(action, dict):
            if "write" in action:
                tape[head] = action["write"]
            
            if "R" in action:
                head += 1
                state = action["R"]
            elif "L" in action:
                head -= 1
                state = action["L"]
        elif action == "L":
            head -= 1
        elif action == "R":
            head += 1
        
        if head == 0:
            tape.insert(0, blank)
            head = 1
        elif head == len(tape):
            tape.append(blank)
        
        execution["transition"] = state
        execution_history.append(execution)
        
        step_count += 1
    
    output = ''.join(tape).strip(blank)
    accepted = state in final_states
    
    return output, execution_history, accepted