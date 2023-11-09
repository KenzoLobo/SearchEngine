import json
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize

# downloads tokenizing libaries
nltk.download("punkt")

# imports the Posting class to use as our value for our dictionary
from posting import Posting

# creates a set of unique tokens - set access is O(1), so we can easily hold a set of unique tokens in here
tokens = set() # do we even need this idk i thought we did but idk now

# creates a dictionary of urls - key: url, token: id
urls = dict()

# creates a dictionary to store our index - key: token, value: Posting (object)
index = dict()

# initial id for our url dictionary
INITIAL_ID = 1

# currently testing one file locally
filename = "C:/Users/aditm/OneDrive/Desktop/UCI/UCI Fall 2023/CS121/Assignment 3/M1/CS121---A3-M1/0a0095d4c7566f38a53f76c4f90ce6ca4c6aa7103c9c17c88ed66802e0f55926.json"

# Open the JSON file for reading
with open(filename, "r") as json_file:
    # Parses JSON from the file into a Python dictionary
    parsed_data = json.load(json_file)

# JSON has three fields - "url": stores url, "content": - stores HTML content, "encoding" - usually ASCII but encoding
url = parsed_data["url"]
html = parsed_data["content"]
encoding = parsed_data["encoding"]

print("URL: ", url)

# parses the HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Here, tokenize the title and headings separately to give them more weight later

# Tokenize the title
title = soup.title.text if soup.title else ""
title_tokens = word_tokenize(title)

# Filter out non-alphanumeric tokens
filtered_title_tokens = []
for token in title_tokens:
    if token.isalnum():
        filtered_title_tokens.append(token)
print(filtered_title_tokens)

# print(title_tokens)

# Tokenize the headings
headings = [heading.text for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
heading_tokens = [word_tokenize(heading) for heading in headings]

# Filter out non-alphanumeric tokens in headings
filtered_heading_tokens = []
for tokens in heading_tokens:
    filtered_tokens = [token for token in tokens if token.isalnum()]
    filtered_heading_tokens.append(filtered_tokens)

# print(filtered_heading_tokens)

# Tokenize the body content
body = [paragraph.text for paragraph in soup.find_all("p")]
body_tokens = [word_tokenize(text) for text in body]

# Filter out non-alphanumeric tokens in body content
filtered_body_tokens = []
for tokens in body_tokens:
    filtered_tokens = [token for token in tokens if token.isalnum()]
    filtered_body_tokens.append(filtered_tokens)

print(filtered_body_tokens)

# transforms all the tokens from the sublist structure to a single array
# Flatten the list of lists into a single list of tokens
all_tokens = []
for sublist in filtered_body_tokens:
    all_tokens.extend(sublist)
print(all_tokens)

print("------------------------------")

# Extract the title
# title = soup.title
# if title:
#     print("Title:", title.text)

# # Extract and print all headings (h1, h2, h3, etc.)
# headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
# for heading in headings:
#     print("Heading:", heading.text)

# # Extract and print the body content
# body = soup.body
# if body:
#     print("Body:")
#     for paragraph in body.find_all("p"):
#         print(paragraph.text)