import requests
from bs4 import BeautifulSoup
import re
import validators
from urllib.parse import urlparse, urljoin
import tldextract
import os
import shutil

def main():
    base_url_nexus = "https://brave-rock-0eeda700f.4.azurestaticapps.net/nexus-landingpage/index.html"
    file_name = "nexus.md"

    session = create_session()

    read_page(session, base_url_nexus, file_name, [])
    clean_empty_lines(file_name)
    
def read_page(session, base_url, file_name, visited_urls):
    url_infos = get_url_infos(base_url)

    if (url_infos in visited_urls): return

    visited_urls.append(url_infos)

    raw_urls = get_included_urls(base_url, session)
    valid_urls = []
    valid_urls = get_urls(raw_urls, base_url)

    for url in valid_urls:
        read_page(session, url, file_name, visited_urls)
    
    generate_doc_file(base_url,session, file_name)
    
def get_url_infos(url):
    parsed_url = urlparse(url)
    return (parsed_url.netloc, parsed_url.path)

def create_session():
    session = requests.Session()
    session.cookies.set(name="", value="")
    session.cookies.set(name="", value="")
    session.cookies.set(name="", value="")
    return session

def get_included_urls(base_url, session):
    response = session.get(base_url)
    if (response.ok):
        html_content = BeautifulSoup(response.content, 'html.parser')
        body = html_content.find('div', {'class': 'body'})
        if (body is not None):
            urls = body.find_all('a', href=True)
            return list(set(urls))
    return []

def get_webpage_content(base_url, session):
    response = session.get(base_url)
    if (response.ok):
        try:
            html_content = BeautifulSoup(response.content, 'html.parser')
            main = html_content.find('main', {'class': 'article'})
            if (main is not None):
                text_content = main.find_all(['div', 'h1', 'h2', 'h3', 'p', 'a'] , recursive=True)   
                return [text.get_text() for text in text_content]
        except:
            print("url: " + base_url)
            return []
        
    return []

def generate_doc_file(base_url, session, file_name):
    content = get_webpage_content(base_url, session)

    with open(file_name, 'a', encoding="utf-8") as f:
        f.write(base_url + '\n\n')
        for c in content:
            if c.strip():
                f.write(c + '\n')

    print("Documentation exported!")

def clean_empty_lines(file_path):
    temp_file_path = file_path + ".tmp"

    with open(file_path, 'r', encoding="utf-8") as infile, open(temp_file_path, 'w', encoding="utf-8") as outfile:
        for line in infile:
            if line.strip():
                outfile.write(line)

    shutil.copy(temp_file_path, file_path)
    os.remove(temp_file_path)

def is_relative_url(url_string):
    parsed_url = urlparse(url_string)
    return not parsed_url.scheme and not parsed_url.netloc

def resolve_relative_url(url, base_url):
    return urljoin(base_url, url)

def get_urls(docs, base_url):
    base_domain = tldextract.extract(base_url).domain
    urls = []
    
    for doc in docs:
        url = doc['href']

        if (is_relative_url(url)):
            url = resolve_relative_url(url, base_url)

        domain = tldextract.extract(url).domain
        if domain == base_domain and is_url_valid(url):
            urls.append(url)

    return urls

def is_url_valid(url):
    match = re.search(r"(?i)\.(jpg|png|svg)$", url)
    return (validators.url(url)) and (match is None) and (url != '#') and not ("apidocs" in url )

if __name__ == "__main__":
    main()
