from typing import List, Union, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
# from IPython.display import Image, display
from dotenv import load_dotenv

load_dotenv()


class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


def process(state: AgentState)->AgentState:
    print('before llm call', state)
    response = llm.invoke(state["messages"])
    # state["message"].append(response)
    state['messages'].append(AIMessage(content=response.content))
    print('after llm call \n', state)
    return state


graph = StateGraph(AgentState)

graph.add_node('processor', process)
graph.add_edge(START, 'processor')
graph.add_edge('processor', END)

app = graph.compile()


input_text = input("Enter: ")
chat_history=[]
while input_text != 'exit':
    chat_history.append(HumanMessage(content=input_text))
    app.invoke({'messages': chat_history})
    input_text = input('Enter: ')

file= open('logging.txt', 'w')
file.write('Logging History\n')

for msg in chat_history:
    if isinstance(msg, HumanMessage):
        file.write(f'You: {msg.content}\n', )
    elif isinstance(msg, AIMessage):
        file.write(f'AI: {msg.content}\n')
file.write('End of conversation')
print('conversation saved to logging file')
    