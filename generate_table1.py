import os
import json

# Directory where JSON files are stored
json_dir = 'Incentive Scheme Data'

# List to hold data from each JSON file
data = []

# Iterate over all JSON files and read data
for json_file in os.listdir(json_dir):
    if json_file.endswith('.json'):
        with open(os.path.join(json_dir, json_file)) as f:
            data.append(json.load(f))

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

def generate_html_table(data):
    html = '''
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.3/css/jquery.dataTables.css">
        <script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.5.1.js"></script>
        <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.11.3/js/jquery.dataTables.js"></script>
    </head>
    <body>
    <table id="example" class="display" style="width:100%">
    '''
    
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
    html += '''
    </table>
    <script>
    $(document).ready(function() {
        $('#example').DataTable({
            "columnDefs": [
                { "type": "num", "targets": 3 },  // Adjust the index for "year"
                { "type": "string", "targets": 2 }  // Adjust the index for "venue"
            ]
        });
    });
    </script>
    </body>
    </html>
    '''
    return html

# Generate HTML table from data
html_table = generate_html_table(data)

# Write HTML table to file
with open('index.html', 'w') as f:
    f.write(html_table)
