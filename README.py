import json

postmanTests = 'tests/postmanTests.json'
READMEFile = 'README.txt'

with open(postmanTests, 'r') as f:
    collection = json.load(f)

lines = ["Assignment 1 README", "API Endpoints Overview:\n"]

for item in collection.get('item', []):
    req = item.get('request', {})
    url_field = req.get('url', 'Unknown URL')

    # Handle both string URLs and dict URLs
    if isinstance(url_field, dict):
        url = url_field.get('raw', 'Unknown URL')
        query_params = url_field.get('query', [])
    else:
        url = url_field
        query_params = []

    method = req.get('method', 'GET')
    lines.append(f"Endpoint: {url}")
    lines.append(f"Method: {method}")

    if query_params:
        lines.append("Parameters:")
        for q in query_params:
            lines.append(f" - {q['key']}: {q.get('value', '')}")
    else:
        lines.append("Parameters: None")
    lines.append("")

with open(READMEFile, 'w') as f:
    f.write("\n".join(lines))

print(f"README file '{READMEFile}' created successfully!")