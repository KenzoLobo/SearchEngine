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
urlIDs = dict()

# creates a dictionary to store our index
# KEY: token, VALUE: Posting (object)
index = dict()

# initial id for our url dictionary
id = 1

# currently testing one file locally
filename = "C:/Users/aditm/OneDrive/Desktop/UCI/UCI Fall 2023/CS121/Assignment 3/M1/CS121---A3-M1/0a0095d4c7566f38a53f76c4f90ce6ca4c6aa7103c9c17c88ed66802e0f55926.json"

def tokenize(soup):
    # Here, tokenize the title and headings separately to give them more weight later

    # Tokenize the title
    title = soup.title.text if soup.title else ""
    title_tokens = word_tokenize(title)

    # Filtering out each tokens separately to keep them separated for now due to weight requirement

    # Filter out non-alphanumeric tokens
    filtered_title_tokens = []
    for token in title_tokens:
        if token.isalnum():
            filtered_title_tokens.append(token)
    # print(filtered_title_tokens)

    # Tokenize the headings
    headings = [heading.text for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    heading_tokens = [word_tokenize(heading) for heading in headings if token.isalnum()]

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

    # print(filtered_body_tokens)

    # transforms all the tokens from the sublist structure to a single array
    all_tokens = []
    for sublist in filtered_body_tokens:
        all_tokens.extend(sublist)
    print(all_tokens)

    return all_tokens

def parse_json(filename):
    # Open the JSON file for reading
    with open(filename, "r") as json_file:
        
        # Parses JSON from the file into a Python dictionary
        parsed_data = json.load(json_file)

    # JSON has three fields - "url": stores url, "content": - stores HTML content, "encoding" - usually ASCII but encoding
    url = parsed_data["url"]
    html = parsed_data["content"]
    encoding = parsed_data["encoding"]

    # adds current URL we are parsing and its id (first iteration being one, each subsequent iteration ++) to the dictionary of urls
    # Need to enclose this in a loop where every iteration id increments
    urlIDs[url] = id
    id = id + 1

    print("---------- URL PARSED: ", url, " ----------")

    return html

# parses the HTML using BeautifulSoup and tokenizes the html content
content = parse_json(filename)
soup = BeautifulSoup(content, 'html.parser')
tokens = tokenize(soup)

print("\n------------------------------\n")