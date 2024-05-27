import os
import json

# Directory where JSON files are stored
json_dir = 'Incentive Scheme Data'

# Function to read all JSON files from directory
def read_json_files(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename)) as f:
                data.append(json.load(f))
    return data

# Function to extract headers recursively
def extract_headers(data):
    headers = {}

    def add_to_headers(d, parent_key=''):
        for k, v in d.items():
            full_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                if parent_key not in headers:
                    headers[parent_key] = {}
                headers[parent_key][k] = {}
                add_to_headers(v, full_key)
            else:
                if parent_key not in headers:
                    headers[parent_key] = {}
                headers[parent_key][k] = None
    
    add_to_headers(data[0])
    return headers

# Function to generate HTML table
def generate_html_table(data):
    headers = extract_headers(data)
    
    html = '''
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.3/css/jquery.dataTables.css">
        <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        </style>
    </head>
    <body>
    <table id="example" class="display">
    '''
    
    # Generate header rows
    html += '<thead>'
    html += '<tr>'
    for key, subkeys in headers.items():
        if subkeys:
            for subkey, nested_subkeys in subkeys.items():
                if nested_subkeys:
                    html += f'<th colspan="{count_nested_keys(nested_subkeys)}">{key}</th>'
                    html += generate_nested_header(subkey, nested_subkeys)
                else:
                    html += f'<th>{key}.{subkey}</th>'
        else:
            html += f'<th>{key}</th>'
    html += '</tr>'
    
    html += '<tr>'
    for key, subkeys in headers.items():
        if subkeys:
            for subkey, nested_subkeys in subkeys.items():
                if nested_subkeys:
                    html += generate_nested_header('', nested_subkeys)
                else:
                    html += f'<th>{subkey}</th>'
        else:
            html += f'<th>{key}</th>'
    html += '</tr>'
    html += '</thead>'
    
    # Generate table rows
    html += '<tbody>'
    for record in data:
        html += '<tr>'
        for key, subkeys in headers.items():
            if subkeys:
                for subkey, nested_subkeys in subkeys.items():
                    if nested_subkeys:
                        html += generate_nested_cells(record, [key, subkey], nested_subkeys)
                    else:
                        nested_record = record.get(key, {})
                        html += f'<td>{nested_record.get(subkey, "")}</td>'
            else:
                html += f'<td>{record.get(key, "")}</td>'
        html += '</tr>'
    html += '</tbody>'
    
    html += '''
    </table>
    <script src="https://code.jquery.com/jquery-3.5.1.js"></script>
    <script src="https://cdn.datatables.net/1.11.3/js/jquery.dataTables.js"></script>
    <script>
    $(document).ready(function() {
        $('#example').DataTable({
            "order": [[2, 'asc'], [3, 'asc']],  // Default sorting by the third column (year) and fourth column (venue)
            "columnDefs": [
                { "orderable": true, "targets": [2, 3] },  // "year" and "venue" columns
                { "orderable": false, "targets": "_all" }
            ]
        });
    });
    </script>
    </body>
    </html>
    '''
    return html

# Function to count nested keys
def count_nested_keys(nested_dict):
    count = 0
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            count += count_nested_keys(value)
        else:
            count += 1
    return count

# Function to generate nested header rows
def generate_nested_header(parent_key, nested_dict):
    html = ''
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            html += generate_nested_header(f"{parent_key}.{key}", value)
        else:
            html += f'<th>{parent_key}.{key}</th>'
    return html

# Function to generate nested cells for table rows
def generate_nested_cells(record, keys, nested_dict):
    nested_record = get_nested_record(record, keys)
    html = ''
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            html += generate_nested_cells(nested_record, keys + [key], value)
        else:
            html += f'<td>{nested_record.get(key, "")}</td>'
    return html

# Function to get nested record value
def get_nested_record(record, keys):
    for key in keys:
        record = record.get(key, {})
    return record

# Read JSON data from directory
data = read_json_files(json_dir)

# Generate HTML table from data
html_table = generate_html_table(data)

# Write HTML table to file
with open('index.html', 'w') as f:
    f.write(html_table)
