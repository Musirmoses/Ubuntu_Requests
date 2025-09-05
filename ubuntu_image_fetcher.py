import requests
import os
from urllib.parse import urlparse, urljoin
import hashlib
from bs4 import BeautifulSoup
from collections import deque

def get_filename_from_url(url, content_type=None):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:
        hash_digest = hashlib.md5(url.encode()).hexdigest()[:10]
        ext = content_type.split("/")[-1] if content_type else "jpg"
        filename = f"downloaded_{hash_digest}.{ext}"
    return filename

def file_exists_with_same_content(filepath, content):
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'rb') as f:
        return f.read() == content

def fetch_and_save_image(url, dir_path="Fetched_Images"):
    try:
        with requests.get(url, stream=True, timeout=10) as response:
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "")
            if "image" not in content_type:
                return False
            
            filename = get_filename_from_url(url, content_type)
            os.makedirs(dir_path, exist_ok=True)
            filepath = os.path.join(dir_path, filename)

            content = response.content
            if file_exists_with_same_content(filepath, content):
                print(f"⚠ Skipped duplicate image: {filename}")
                return False

            with open(filepath, 'wb') as f:
                f.write(content)

            print(f"✓ Saved image: {filename}")
            return True
    except Exception as e:
        print(f"✗ Failed to fetch {url}: {e}")
        return False

def scrape_images_and_links(page_url, domain):
    img_urls = []
    page_links = []
    try:
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Collect images
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src")
            if src:
                img_urls.append(urljoin(page_url, src))

        # Collect same-domain links
        for a in soup.find_all("a", href=True):
            href = urljoin(page_url, a["href"])
            if domain in href:  # stay within the same site
                page_links.append(href)

    except Exception as e:
        print(f"✗ Error scraping {page_url}: {e}")
    
    return list(set(img_urls)), list(set(page_links))

def crawl_website(start_url, max_pages=5):
    domain = urlparse(start_url).netloc
    visited = set()
    queue = deque([start_url])
    all_images = []

    while queue and len(visited) < max_pages:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)

        print(f"\n🔎 Crawling: {url}")
        img_urls, links = scrape_images_and_links(url, domain)

        # Save images
        for img_url in img_urls:
            fetch_and_save_image(img_url)
        all_images.extend(img_urls)

        # Add new links to crawl
        for link in links:
            if link not in visited:
                queue.append(link)

    print(f"\n✅ Crawling finished. Visited {len(visited)} pages, found {len(all_images)} images.")

def main():
    print("🖼️  Welcome to the Multi-Page Image Crawler")
    print("Paste a website URL (e.g., Unsplash, Pinterest, Pexels) and I’ll fetch images across multiple pages.\n")

    urls_input = input("https://unsplash.com/, https://www.pexels.com/, https://pixabay.com/, https://www.pinterest.com/:")
    websites = [url.strip() for url in urls_input.split(",") if url.strip()]

    if not websites:
        print("✗ No valid websites entered. Exiting.")
        return

    max_pages = input("How many pages to crawl per site? (default=5): ")
    max_pages = int(max_pages) if max_pages.isdigit() else 5

    for site in websites:
        crawl_website(site, max_pages=max_pages)

if __name__ == "__main__":
    main()
