import json
import nltk
import sys
from os.path import getsize
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from posting import Posting

# downloads tokenizing libaries
nltk.download("punkt")

# creates a set of unique tokens - set access is O(1), so we can easily hold a set of unique tokens in here
tokens = set() # do we even need this idk i thought we did but idk now

# creates a dictionary to store our index
# KEY: token, VALUE: Posting (object)
index = dict()

# creates a dictionary to store unique URL ids
# KEY: url, VALUE: id
url_ids = dict()

# initial id for our url dictionary
current_id = 0

# currently testing one file locally
filename = "/home/joanau/IR23F-A3-G27/0a0095d4c7566f38a53f76c4f90ce6ca4c6aa7103c9c17c88ed66802e0f55926.json"

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
        filtered_tokens = [token.lower() for token in tokens if token.isalnum()]
        filtered_body_tokens.append(filtered_tokens)

    # print(filtered_body_tokens)

    # transforms all the tokens from the sublist structure to a single array
    all_tokens = []
    for sublist in filtered_body_tokens:
        all_tokens.extend(sublist)
    print(all_tokens)

    return all_tokens

def parse_json(filename):
    # tracks the current id of the posting
    global current_id

    # Open the JSON file for reading
    with open(filename, "r") as json_file:
        
        # Parses JSON from the file into a Python dictionary
        parsed_data = json.load(json_file)

    # JSON has three fields - "url": stores url, "content": - stores HTML content, "encoding" - usually ASCII but encoding
    url = parsed_data["url"]
    html = parsed_data["content"]
    encoding = parsed_data["encoding"]

    # adds current URL we are parsing and its id (first iteration being one, each subsequent iteration ++) to the dictionary of urls
    current_id += 1
    if url not in url_ids:
        url_ids[url] = current_id
    
    # creates a dictionary for counting tokens in the current url
    frequency = dict()

    # here, we need a set of tokens that belong to this url
    soup = BeautifulSoup(html, 'html.parser')
    tokens = tokenize(soup)

    # for every token, we first must add it to our index
    # then, increment the frequency of the token on each occurence of a token
    for token in tokens:
        if token not in index:
            index[token] = []
        if token not in frequency:
            frequency[token] = 1
        else:
            frequency[token] += 1

    for token, freq in frequency.items():
        # create a new Posting for this url
        posting = Posting(url, current_id, freq)
        # add our token and posting to our index
        index[token].append(posting)

        

    print("---------- URL PARSED: ", url, " ----------")

    return html

# parses the HTML using BeautifulSoup and tokenizes the html content
content = parse_json(filename)


#write to file all of index
with open('indexreport.txt', 'w') as file:
    for token, postings in index.items():
        file.write(f"{token}: ")
        for posting in postings:
            file.write(f"{posting.get_id()}, {posting.get_url()}, {posting.get_tfidf()} ")


#write to file report
with open('report.txt', 'w') as f:
    f.write(f" Number of indexed documents: {current_id}")
    f.write('\n')
    f.write(f" Number of unique words: {len(index.items())}")
    f.write('\n')
    f.write(f" Size of dictionary in KB: {sys.getsizeof(index)/1000}")
    f.write('\n')
    f.write(f" Size of index file in KB: {getsize('indexreport.txt')/1000}")

# prints index
for token, postings in index.items():
    print(f"{token}:")
    for posting in postings:
        print(f"  Posting ID: {posting.get_id()}, URL: {posting.get_url()}, Frequency: {posting.get_tfidf()}")

    print("\n")


print("\n------------------------------\n")