#First off, we need to import the 'json' library, so that in our Python file,
# we can read and parse JSON files. Since our Postman tests are stored in JSON
#  format, we need to import the 'json' library
import json

#Here we declare the path so that our API points to our postman collection
postmanTests = 'tests/postmanTests.json'
#Here we declare the name of the output file that has our API documentation
READMEFile = 'README.txt'

#In this section we are opening our Postman collection.
# We use the 'with' statement to ensure the file is automatically closed after reading
# We use the open function and pass 'r' to indicate we are in read mode
#  'json.load(f)' converts our JSON tests into a Python dictionary, which is a format Python understands
with open(postmanTests, 'r') as f:
    collection = json.load(f)

#We prepare some little lines of content in the form of string that we will later join.
# We incldued these so that we can give an idea as to what the README file is for.
#  Using a list like this is efficient, especially when we have multi-line text.
lines = ["Assignment 1 README", "API Endpoints Overview:\n"]

#In our POSTMAN collection of tests, each request to the API is stored under the 'item' key
# This means, when we call '.get('item', []) we are retreiving the list of API requests 
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