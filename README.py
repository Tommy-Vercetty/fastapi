import json

postmanTests = 'tests/postmanTests.json'
READMEFile = 'README.txt'

with open(postmanTests, 'r') as f:
    collection = json.load(f)

lines = ["Assignment 1 README", "API Endpoints Overview:\n"]

for item in collection.get('item', []):
    req = item.get('request', {})
    url = req.get('url', {}).get('raw', 'Unknown URL')
    method = req.get('method', 'GET')
    lines.append(f"Endpoint: {url}")
    lines.append(f"Method: {method}")

    query_params = req.get('url', {}).get('query', [])
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