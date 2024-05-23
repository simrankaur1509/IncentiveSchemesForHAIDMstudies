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

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Generate HTML table from DataFrame
html_table = df.to_html(index=False)

# Write HTML table to file
with open('index.html', 'w') as f:
    f.write(html_table)
