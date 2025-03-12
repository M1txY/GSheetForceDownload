import requests
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
import sys
import re

def generate_htmlview_link(url):
    parsed_url = urlparse(url)
    if '/edit' not in parsed_url.path:
        print("⚠️ Invalid or unsupported Google Sheets URL.")
        sys.exit(1)
    base_path = parsed_url.path.split('/edit')[0] + '/htmlview'
    html_url = urlunparse(parsed_url._replace(path=base_path, query='', fragment=''))
    return html_url

def get_sheet_name(html):
    soup = BeautifulSoup(html, 'html.parser')
    title_tag = soup.find('title')
    if title_tag:
        
        title_text = re.sub(r'\s*-\s*Google.*$', '', title_tag.text).strip()
        sanitized_title = re.sub(r'[\\/*?:"<>|]', "_", title_text)
        return sanitized_title
    return 'google_sheet'

def download_google_sheet(url):
    html_url = generate_htmlview_link(url)
    print(f"🔗 Download URL: {html_url}")

    response = requests.get(html_url)

    if response.status_code == 200:
        filename = get_sheet_name(response.text) + ".html"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"✅ Successfully downloaded as '{filename}'.")
    else:
        print(f"❌ Error: Unable to download (HTTP status code: {response.status_code})")


def get_sheet_name(html):
    soup = BeautifulSoup(html, 'html.parser')
    title_tag = soup.find('title')
    if title_tag:
        title_text = re.sub(r'\s*-\s*Google.*$', '', title_tag.text).strip()
        sanitized_title = re.sub(r'[\\/*?:"<>|]', "_", title_text)
        return sanitized_title
    return 'google_sheet'

if __name__ == "__main__":
    sheet_url = input("🌐 Enter Google Sheets URL: ")
    download_google_sheet(sheet_url)
