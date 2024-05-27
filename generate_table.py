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

def generate_html_table(data):
    headers = extract_headers(data)
    
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
    
    # Generate header rows
    html += '<thead>'
    html += '<tr>'
    for key, subkeys in headers.items():
        if subkeys:
            for subkey, nested_subkeys in subkeys.items():
                if nested_subkeys:
                    col_span = len(nested_subkeys)
                    html += f'<th colspan="{col_span}">{key}.{subkey}</th>'
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
                    for nested_subkey in nested_subkeys.keys():
                        html += f'<th>{nested_subkey}</th>'
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
                        for nested_subkey in nested_subkeys.keys():
                            nested_record = get_nested_record(record, [key, subkey])
                            html += f'<td>{nested_record.get(nested_subkey, "")}</td>'
                    else:
                        nested_record = record.get(key, {})
                        html += f'<td>{nested_record.get(subkey, "")}</td>'
            else:
                html += f'<td>{record.get(key, "")}</td>'
        html += '</tr>'
    html += '</tbody>'
    
    html += '''
    </table>
    <script>
    $(document).ready(function() {
        $('#example').DataTable({
            "columnDefs": [
                { "orderable": true, "targets": [2, 3] },  // "year" and "venue" columns (adjust indices if necessary)
                { "orderable": false, "targets": "_all" }
            ]
        });
    });
    </script>
    </body>
    </html>
    '''
    return html

def get_nested_record(record, keys):
    for key in keys:
        record = record.get(key, {})
    return record

# Generate HTML table from data
html_table = generate_html_table(data)

# Write HTML table to file
with open('index.html', 'w') as f:
    f.write(html_table)
