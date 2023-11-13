import json
from itertools import groupby

# Sample list of JSON objects with a nested "address" key
json_data = [
    {"name": "Alice", "age": 25, "address": {"city": "New York"}},
    {"name": "Bob", "age": 30, "address": {"city": "Los Angeles"}},
    {"name": "Charlie", "age": 35, "address": {"city": "New York"}},
    {"name": "David", "age": 28, "address": {"city": "Chicago"}},
    {"name": "Alice", "age": 22, "address": {"city": "New York"}},
]

# Function to group JSON objects by a specified nested key
def group_by_nested_key(json_list, nested_key):
    # Sort the list based on the nested key
    json_list.sort(key=lambda x: x.get(nested_key, None))

    # Use itertools.groupby to group objects by the nested key
    grouped_data = {k: list(group) for k, group in groupby(json_list, key=lambda x: x.get(nested_key, None))}

    return grouped_data

# Example: Grouping JSON objects by the "city" within the "address" key
grouped_json_data = group_by_nested_key(json_data, nested_key="address.city")

# Print the result
for city, group in grouped_json_data.items():
    print(f"Group {city}: {group}")
