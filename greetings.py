from typing import TypedDict, Dict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    message:str

def greeting_node(state: AgentState)->AgentState:
    """Perform the greeting to user"""
    
    state['message'] = 'Hey' + state['message'] + 'It is nice to meet you'

    return state

graph = StateGraph(AgentState)

graph.add_node('greeter', greeting_node)
graph.set_entry_point('greeter')
graph.set_finish_point('greeter')

app = graph.compile()
app.invoke({"message":'Temitayo'})


from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png() ))

