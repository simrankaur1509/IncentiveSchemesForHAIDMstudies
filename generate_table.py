import os
import json
import pandas as pd

# Directory where JSON files are stored
json_dir = 'Incentive Scheme Data'

# List to hold data from each JSON file
data = []

# Iterate over all JSON files and read data
for json_file in os.listdir(json_dir):
    if json_file.endswith('.json'):
        with open(os.path.join(json_dir, json_file)) as f:
            data.append(json.load(f))

# # Normalize nested fields
# df = pd.json_normalize(data)

# # Create a DataFrame from the data
# df = pd.DataFrame(data)

# # Generate HTML table from DataFrame
# html_table = df.to_html(index=False)

# # Write HTML table to file
# with open('index.html', 'w') as f:
#     f.write(html_table)
            
def generate_html_table(data):
    html = '<table border="1">'
    
    # Header
    html += '<thead><tr>'
    for key in data[0].keys():
        if isinstance(data[0][key], dict):
            nested_keys = data[0][key].keys()
            for nested_key in nested_keys:
                html += f'<th>{key}.{nested_key}</th>'
        else:
            html += f'<th>{key}</th>'
    html += '</tr></thead>'
    
    # Rows
    html += '<tbody>'
    for record in data:
        html += '<tr>'
        for key, value in record.items():
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    html += f'<td>{nested_value}</td>'
            else:
                html += f'<td>{value}</td>'
        html += '</tr>'
    html += '</tbody>'
    html += '</table>'
    return html

# Generate HTML table from data
html_table = generate_html_table(data)

# Write HTML table to file
with open('index.html', 'w') as f:
    f.write(html_table)

# def generate_html_table(data):
#     html = '<table border="1">'
#     # Header
#     html += '<thead><tr>'
#     for key in data[0].keys():
#         html += f'<th>{key}</th>'
#     html += '</tr></thead>'
    
#     # Rows
#     html += '<tbody>'
#     for record in data:
#         html += '<tr>'
#         for key, value in record.items():
#             if isinstance(value, dict):
#                 html += f'<td>{generate_html_table_from_dict(value)}</td>'
#             else:
#                 html += f'<td>{value}</td>'
#         html += '</tr>'
#     html += '</tbody>'
#     html += '</table>'
#     return html

# def generate_html_table_from_dict(data_dict):
#     html = '<table border="1">'
#     for key, value in data_dict.items():
#         html += '<tr>'
#         html += f'<td>{key}</td>'
#         if isinstance(value, dict):
#             html += f'<td>{generate_html_table_from_dict(value)}</td>'
#         elif isinstance(value, list):
#             html += f'<td>{", ".join(value) if value else ""}</td>'
#         else:
#             html += f'<td>{value}</td>'
#         html += '</tr>'
#     html += '</table>'
#     return html

# # Generate HTML table from data
# html_table = generate_html_table(data)

# # Write HTML table to file
# with open('index.html', 'w') as f:
#     f.write(html_table)
