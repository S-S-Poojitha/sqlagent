import re
import streamlit as st
from graphviz import Digraph

def remove_runtimes(output):
    clean_output = re.sub(r'\x1b\[\d+m', '', output)  # Handle ANSI escape sequences like "[0m"
    clean_output = re.sub(r'\x1b\[\d{2};\d{1,2};\d{1,2}m', '', clean_output)  # Handle cases like "\033[38;5;196m"
    clean_output = re.sub(r'\[.*?\]', '', clean_output)  # Remove any remaining brackets
    clean_output = re.sub(r'\x1b\[.*?m', '', clean_output)  # Remove other ANSI codes
    return clean_output

def create_graphviz_source(action_input_output_list):
    graph = Digraph(format='svg')
    for i, action_input in enumerate(action_input_output_list):
        name = f"{action_input['action']}\n\nInput: {action_input['action_input']}\n"
        graph.node(str(i), name)
        if i > 0:
            graph.edge(str(i - 1), str(i), label="Next")
    return graph

# Read and clean the output log
with open('output.txt', 'r') as file:
    output_text = file.read()
clean_output = remove_runtimes(output_text)

# Parse the cleaned output into a list of actions and inputs
action_input_output_list = []
pattern = r'Action: (.+?)\nAction Input: (.+?)(?=\nAction:|$)'
matches = re.findall(pattern, clean_output, re.DOTALL)
for match in matches:
    action_input_output_list.append({'action': match[0].strip(), 'action_input': match[1].strip()})

# Create the Graphviz source
graphviz_source = create_graphviz_source(action_input_output_list)

# Display the flowchart in Streamlit
st.graphviz_chart(graphviz_source)
