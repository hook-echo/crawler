import requests
from bs4 import BeautifulSoup
import urllib.parse

def crawl_subdirectories(base_url, output_file):
  """
  Crawls a web domain looking for subdirectories and outputs them to a text file.

  Args:
    base_url: The base URL of the domain to crawl.
    output_file: The filename to write the subdirectories to.
  """
  with open(output_file, "w") as file:
    # Make an initial request to the base URL
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract all links from the page
    links = soup.find_all("a", href=True)

    # Keep track of visited URLs to avoid infinite loops
    visited_urls = set()

    # Crawl links recursively
    crawl_links(base_url, links, visited_urls, file)

def crawl_links(base_url, links, visited_urls, file):
  """
  Crawls a list of links, checking for subdirectories and writing them to a file.

  Args:
    base_url: The base URL of the domain.
    links: A list of links to crawl.
    visited_urls: A set of already visited URLs.
    file: The file to write the subdirectories to.
  """
  for link in links:
    href = link["href"]

    # Ignore external links and fragment anchors
    if href.startswith("#") or href.startswith("http"):
      continue

    # Construct the full URL
    url = urllib.parse.urljoin(base_url, href)

    # Check if URL has already been visited
    if url in visited_urls:
      continue

    visited_urls.add(url)

    # Check if the URL leads to a subdirectory
    if "/" in url and url != base_url:
      file.write(url + "\n")

    # Recursively crawl this link's subdirectories
    try:
      response = requests.get(url)
      soup = BeautifulSoup(response.content, "html.parser")
      new_links = soup.find_all("a", href=True)
      crawl_links(url, new_links, visited_urls, file)
    except requests.exceptions.RequestException as e:
      print(f"Error crawling URL: {url} - {e}")

# Example usage
base_url = "https://example.com"
output_file = "subdirectories.txt"
crawl_subdirectories(base_url, output_file)

print(f"Subdirectories saved to: {output_file}")
