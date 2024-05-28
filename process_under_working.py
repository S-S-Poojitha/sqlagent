import re
import streamlit as st
from graphviz import Digraph
import svglib
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

def remove_runtimes(output):
    clean_output = re.sub(r'\[\d+m', '', output)
    clean_output = re.sub(r'\[\d{2};\d{1,2};\d{1,2}m', '', clean_output)  # Handle cases like "\033[38;5;196m"
    clean_output = re.sub(r'\[.*?\]', '', clean_output)
    clean_output = re.sub(r'\[.*?m', '', clean_output)
    # Remove custom formatting like "[36;1m[1;3m"
    return clean_output

def create_and_save_flowchart(action_input_output_list, filename="flowchart.svg"):
    graph = Digraph(format='svg')
    for i, action_input in enumerate(action_input_output_list):
        name = f"{action_input['action']}\n\nInput: {action_input['action_input']}\n"
        graph.node(str(i), name)
        if i > 0:
            graph.edge(str(i - 1), str(i), label="Next")
    graph.render(filename, view=False)
    return filename

def svg_to_image(svg_file, output_file, format='png'):
    drawing = svg2rlg(svg_file)
    renderPM.drawToFile(drawing, output_file, fmt=format)

with open('output.txt', 'r') as file:
    output_text = file.read()
clean_output = remove_runtimes(output_text)

action_input_output_list = []
pattern = r'Action: (.+?)\nAction Input: (.+?)(?=\nAction:|$)'
matches = re.findall(pattern, clean_output, re.DOTALL)
for match in matches:
    action_input_output_list.append({'action': match[0].strip(), 'action_input': match[1].strip()})

svg_file = create_and_save_flowchart(action_input_output_list)
with open(svg_file, "r") as f:
    svg_content = f.read()
svg_to_image('flowchart.svg', 'flowchart.png')
st.image(svg_content, use_column_width=True, format='svg')
