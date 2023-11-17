import json
import nltk

import sys
from os.path import getsize
from collections import defaultdict

from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from posting import Posting
from collections import defaultdict
from pathlib import Path

# downloads tokenizing libraries
nltk.download("punkt")

# creates a set of unique tokens - set access is O(1), so we can easily hold a set of unique tokens in here
tokens = set() # do we even need this idk i thought we did but idk now

# creates a dictionary to store our index
# KEY: token, VALUE: List of Posting (object)
index = dict()

# creates a dictionary to store unique URL ids
# KEY: url, VALUE: id
url_ids = dict()

# initial id for our url dictionary
current_id = 0

# currently testing one file locally
# filename = "/home/lobokj/IR23F-A3-G27/0a0095d4c7566f38a53f76c4f90ce6ca4c6aa7103c9c17c88ed66802e0f55926.json"


def navigate_through_directories():
    # assign directory
    # iterate over files in
    # that directory
    dir="DEV"
    subdirs = Path(dir).glob('*')
    for sub in subdirs:
        # parse_json(file)
        files = Path(sub).glob('*')
        for file in files:
            parse_json(file)

def tokenize(soup):
    '''
    Tokenize titles, headings, and body content of parsed HTML content in JSON. AS OF RIGHT NOW, returns a list of JUST
    the body content of the HTML.
    '''
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
    # print("Filtered title tokens", filtered_title_tokens)

    # Tokenize the headings
    headings = [heading.text for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    heading_tokens = [word_tokenize(heading) for heading in headings if heading.isalnum()]

    # print("Heading_tokens:")
    # for heading_token in heading_tokens:
    #     print (heading_token)

    # Filter out non-alphanumeric tokens in headings
    filtered_heading_tokens = []
    for tokens in heading_tokens:
        filtered_tokens = [token for token in tokens if token.isalnum()]
        filtered_heading_tokens.append(filtered_tokens)

    # print(filtered_heading_tokens)
    # print("Filtered Heading Tokens:")
    # for heading_token in heading_tokens:
    #     print(heading_token)

    # Tokenize the body content
    body = [paragraph.text for paragraph in soup.find_all("p")]
    body_tokens = [word_tokenize(text) for text in body]

    # Filter out non-alphanumeric tokens in body content
    filtered_body_tokens = []
    for tokens in body_tokens:
        filtered_tokens = [token.lower().lower() for token in tokens if token.isalnum()]
        filtered_body_tokens.append(filtered_tokens)
                
    # print("Filtered Body Tokens:")
    # for filtered_body_token in filtered_body_tokens:
    #     print(filtered_body_token)

    # transforms all the tokens from the sublist structure to a single array
    all_tokens = []
    for sublist in filtered_body_tokens:
        all_tokens.extend(sublist)

    # print("All Body Tokens:")
    # print(all_tokens)

    return all_tokens

def parse_json(filename):
    '''
    Loads JSON file into parsed_data dictionary, updates frequency dictionary, tokenizes HTML content in JSON file,
    updates the index, and returns the HTML content of the JSON

    :param filename:
    :return html:
    '''
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
    else: 
        return #if we have already seen the url we don't need to parse through the html
    
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

# query_tokens -> list of query tokens inputed by the user
def getPages(query_tokens):
    
    matched_urls=set()
    for posting in index[query_tokens[0]]:
        matched_urls.add(posting.get_url())
       
    for query_token in query_tokens:
        curr_urls=set()
        for posting in index[query_token]:
            curr_urls.add(posting.get_url())
        matched_urls=matched_urls.intersection(curr_urls)

    return matched_urls

def fill_dict(file_path):
    postings = {}
    current_token = None

    with open(file_path, 'r',  encoding='utf-8-sig', errors='ignore') as file:
        for line in file.readlines():
            line = line.strip()
            if line.endswith(':'):
                current_token = line[:-1].strip()
                postings[current_token] = []
            else:
                data = line.split(', ')
                id = int(data[0])
                url = ', '.join(data[1:-1]) 
                tfidf = int(data[-1].rstrip(','))

                posting = Posting(url, id, tfidf)
                postings[current_token].append(posting)

    return postings
            
if __name__ == "__main__":
    user_input = input("Enter a string: ")
    query_list =word_tokenize(user_input)

    # parses the HTML using BeautifulSoup and tokenizes the html content
    # content = parse_json(filename)

    # fille the index by parsing through the DEV folder
    # navigate_through_directories()


    # uncomment this line to test with a fake index created from fakeindex.txt file
    index = fill_dict("./fakeindex.txt")

    print (getPages(query_list))

    # # prints index
    # for token, postings in index.items():
    #     print(f"{token}:")
    #     for posting in postings:
    #         print(f"  Posting ID: {posting.get_id()}, URL: {posting.get_url()}, Frequency: {posting.get_tfidf()}")

    # print("\n------------------------------\n")

    
    #write to file all of index
    # with open('indexreport.txt', 'w') as file:
    #     for token, postings in index.items():
    #         file.write(f"{token} :\n")
    #         for posting in postings:
    #             file.write(f"{posting.get_id()}, {posting.get_url()}, {posting.get_tfidf()}, ")
    #             file.write("\n")

    # #write to file report
    # with open('report.txt', 'w') as f:
    #     f.write(f" Number of indexed documents: {current_id}")
    #     f.write('\n')
    #     f.write(f" Number of unique words: {len(index.items())}")
    #     f.write('\n')
    #     f.write(f" Size of dictionary in KB: {sys.getsizeof(index)/1000}")
    #     f.write('\n')
    #     f.write(f" Size of index file in KB: {getsize('indexreport.txt')/1000}")
