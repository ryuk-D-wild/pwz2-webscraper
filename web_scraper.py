import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_webpage(url):
    """Fetch the content of a webpage."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def analyze_webpage(html, base_url):
    """Analyze the HTML content and suggest data to scrape."""
    soup = BeautifulSoup(html, 'html.parser')

    suggestions = {}

    headings = []
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        for heading in soup.find_all(tag):
            headings.append(heading.get_text(strip=True))
    if headings:
        suggestions['Headings'] = headings

    links = []
    for a_tag in soup.find_all('a', href=True):
        links.append(urljoin(base_url, a_tag['href']))
    if links:
        suggestions['Links'] = links

    images = []
    for img_tag in soup.find_all('img', src=True):
        images.append(urljoin(base_url, img_tag['src']))
    if images:
        suggestions['Images'] = images

    tables = soup.find_all('table')
    if tables:
        suggestions['Tables'] = [f"Table with {len(table.find_all('tr'))} rows" for table in tables]

    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]
    if paragraphs:
        suggestions['Paragraphs'] = paragraphs[:10]  

    return suggestions

def main():
    url = input("Enter the URL to analyze: ")
    html = fetch_webpage(url)

    if html:
        suggestions = analyze_webpage(html, url)
        print("\n--- Suggested Data to Scrape ---\n")
        for key, items in suggestions.items():
            print(f"{key}:")
            if isinstance(items, list):
                for item in items[:5]: 
                    print(f"  - {item}")
            else:
                print(f"  - {items}")
            print()

if __name__ == "__main__":
    main()
