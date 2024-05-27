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

  # Header Row
  html += '<thead><tr>'
  headers = []

  # Collect top-level headers
  for key in data[0].keys():
    headers.append(key)

  for header in headers:
    html += f'<th>{header}</th>'

  html += '</tr></thead>'

  # Rows
  html += '<tbody>'
  for record in data:
    html += '<tr>'
    for key in record.keys():
      # Check for nested data
      if isinstance(record[key], dict):
        html += f'<td colspan="{len(record[key].keys())}">'  # Span for nested cells
        # Generate nested table for each record
        html += f'''
          <table style="width:100%">
            <tr>'''

        for nested_key in record[key].keys():
          html += f'<th>{nested_key}</th>'

        html += '</tr><tr>'
        for nested_value in record[key].values():
          html += f'<td>{nested_value}</td>'

        html += '</tr></table>'
        html += '</td>'
      else:
        html += f'<td>{record[key]}</td>'
    html += '</tr>'
  html += '</tbody>'
  html += '''
  </table>
  <script>
  $(document).ready(function() {
    $('#example').DataTable({
      "columnDefs": [
        { "orderable": true, "targets": 0 },  # Year (assuming first column)
        { "orderable": true, "targets": 1 },  # Venue (assuming second column)
        { "orderable": false, "targets": "_all" }
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
