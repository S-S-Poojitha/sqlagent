import re
import streamlit as st
import graphviz as g

def remove_runtimes(output):
    clean_output = re.sub(r'\[\d+m', '', output)
    clean_output = re.sub(r'\[\d{2};\d{1,2};\d{1,2}m', '', clean_output)  # Handle cases like "\033[38;5;196m"
    clean_output = re.sub(r'\[.*?\]', '', clean_output)
    clean_output = re.sub(r'\[.*?m', '', clean_output)
    # Remove custom formatting like "[36;1m[1;3m"
    return clean_output

def plot_flowchart(action_input_output_list):
    dot = g.Digraph()
    node_names = []  # Store node names
    for  item in (action_input_output_list):
        action = item['action']
        action_input = item['action_input']
        node_label = f"{action}\n\nInput: {action_input}\n"
        node_names.append(node_label) 
    for i in range(len(node_names) - 1):
        dot.edge(node_names[i], node_names[i + 1])  
    st.graphviz_chart(dot)

# Read and clean the output text
with open('output.txt', 'r') as file:
    output_text = file.read()
clean_output = remove_runtimes(output_text)

# Extract actions, inputs, and outputs using regex
action_input_output_list = []
pattern = r'Action: (.+?)\nAction Input: (.+?)(?=\nAction:|$)'
matches = re.findall(pattern, clean_output, re.DOTALL)
for match in matches:
    action_input_output_list.append({'action': match[0].strip(), 'action_input': match[1].strip()})

# Plot the flowchart
plot_flowchart(action_input_output_list)

# Display the action input-output list
#st.write(action_input_output_list)
