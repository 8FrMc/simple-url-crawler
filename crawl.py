#if you skid this...

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawl_url(url, target_patterns):
    try:
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.content, 'html.parser')

        links = soup.find_all('a', href=True)

        subdomains = set()
        urls = set()
        target_pages = set()

        for link in links:
            href = link['href']
            parsed_url = urlparse(href)

            if parsed_url.scheme and parsed_url.netloc:
                subdomain = re.sub(r'^www\.', '', parsed_url.netloc.split('.')[0])
                subdomains.add(subdomain)
                urls.add(href)

            if any(pattern in href for pattern in target_patterns):
                target_pages.add(href)

        return list(subdomains), list(urls), list(target_pages)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return [], [], []

if __name__ == "__main__":
    # Replace 'LINK HERE' with the URL you want to crawl
    base_url = 'LINK HERE'
    
    target_patterns = ['/download']

    subdomains, urls, target_pages = crawl_url(base_url, target_patterns)

    if subdomains:
        print("Subdomains found:")
        for subdomain in subdomains:
            print(subdomain)

    if urls:
        print("\nURLs found:")
        for url in urls:
            print(url)

    if target_pages:
        print("\nTarget pages found:")
        for target_page in target_pages:
            print(target_page)
    else:
        print("No subdomains, URLs, or target pages found.")
