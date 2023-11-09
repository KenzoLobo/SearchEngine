import json
from bs4 import BeautifulSoup

# currently testing one file locally

filename = "C:/Users/aditm/OneDrive/Desktop/UCI/UCI Fall 2023/CS121/Assignment 3/M1/CS121---A3-M1/0a0095d4c7566f38a53f76c4f90ce6ca4c6aa7103c9c17c88ed66802e0f55926.json"

# Open the JSON file for reading
with open(filename, "r") as json_file:
    # Parses JSON from the file into a Python dictionary
    parsed_data = json.load(json_file)

# JSON has three fields - "url": stores url, "content": - stores HTML content, "encoding" - usually ASCII but encoding
url = parsed_data["url"]
content = parsed_data["content"]
encoding = parsed_data["encoding"]




