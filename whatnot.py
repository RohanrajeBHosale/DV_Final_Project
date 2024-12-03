import os
import json
import pycountry

# Define the input and output folders
input_folder = "converted_json_files"  # Replace with your local input folder path
output_folder = "Cleaned2"  # Replace with your local output folder path
os.makedirs(output_folder, exist_ok=True)

# Function to convert country names to ISO Alpha-3 codes
def convert_to_iso3(entity_name):
    try:
        return pycountry.countries.lookup(entity_name).alpha_3
    except LookupError:
        return None

# Process all JSON files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".json"):
        file_path = os.path.join(input_folder, file_name)

        # Load the JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Update missing ISO codes
        for entry in data:
            if entry.get("code") is None:
                entry["code"] = convert_to_iso3(entry["entity"])

        # Save the updated JSON file
        updated_file_path = os.path.join(output_folder, file_name)
        with open(updated_file_path, 'w') as updated_file:
            json.dump(data, updated_file, indent=4)

        print(f"Updated {file_name} and saved to {updated_file_path}")