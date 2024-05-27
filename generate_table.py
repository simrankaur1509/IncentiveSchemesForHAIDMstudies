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

  # Recursive function to generate nested headers and data
  def generate_nested_headers_and_data(data, current_path=""):
    html = ""
    # Top-level header row
    if current_path == "":
      for key in data[0].keys():
        html += f'<th>{key}</th>'
    else:
      # Nested header row(s)
      # Identify unique nested key levels
      nested_key_levels = set([len(key.split(".")) for key in get_all_nested_keys(data[0], current_path)])
      # Generate headers for each level
      for level in sorted(nested_key_levels, reverse=True):
        html += '<tr>'
        for key in data[0].keys():
          if len(key.split(".")) == level:
            # Extract key part without path
            key_part = key.split(".")[-1]
            html += f'<th>{key_part}</th>'
          else:
            html += f'<th></th>'  # Placeholder for nested data cells
        html += '</tr>'

    # Rows
    html += '<tbody>'
    for record in data:
      html += '<tr>'
      for key in record.keys():
        nested_value = record.get(key)
        if isinstance(nested_value, dict):
          # Nested table for nested data
          colspan = len(get_all_nested_keys(nested_value, current_path + "." + key))
          html += f'<td colspan="{colspan}">'
          html += generate_nested_headers_and_data(list(nested_value.values()), current_path + "." + key)
          html += '</td>'
        else:
          html += f'<td>{nested_value}</td>'
      html += '</tr>'
    html += '</tbody>'
    return html

  # Function to get all nested keys (including current path)
  def get_all_nested_keys(data, current_path):
    nested_keys = []
    for key, value in data.items():
      nested_keys.append(current_path + "." + key)
      if isinstance(value, dict):
        nested_keys.extend(get_all_nested_keys(value, current_path + "." + key))
    return nested_keys

  # Generate nested headers and data
  html += generate_nested_headers_and_data(data)

  html += '''
  </table>
  <script>
  $(document).ready(function() {
    $('#example').DataTable({
      "columnDefs": [
        { "orderable": true, "targets": 0 },  # Assuming year is in first column
        { "orderable": true, "targets": 1 },  # Assuming venue is in second column
        { "orderable": false, "targets": "_all" }  # Make others non-sortable by default
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
