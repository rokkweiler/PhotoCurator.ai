import csv
import json

# Specify the path to your CSV and JSON files
csv_file = 'image_scores.csv'  # Update with the actual path to your CSV file
json_file = 'image_scores.json'  # The name of the output JSON file

# Initialize an empty list to hold the JSON data
data = []

# Read the CSV file and process each row
with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        # Create a dictionary for each image
        entry = {
            "image_id": row["Filename"].strip(),
            "label": [0] * (int(row["Rating Nb"]) - 1) + [1] + [0] * (10 - int(row["Rating Nb"])),  # Convert rating to one-hot encoding
        }
        data.append(entry)

    
# Write the processed data to a JSON file

with open(json_file, 'w', encoding='utf-8') as jsonfile:
    jsonfile.write('[\n')
    for i, entry in enumerate(data):
        jsonfile.write('  {\n')
        jsonfile.write(f'    "image_id": "{entry["image_id"]}",\n')
        jsonfile.write(f'    "label": {json.dumps(entry["label"])}\n')
        jsonfile.write('  }')
        if i < len(data) - 1:
            jsonfile.write(',\n')
    jsonfile.write('\n]')
print(f'Converted {csv_file} to {json_file}')
