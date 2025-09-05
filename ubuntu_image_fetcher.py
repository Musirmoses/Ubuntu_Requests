import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:
        # Generate hash-based filename if no filename in URL
        hash_digest = hashlib.md5(url.encode()).hexdigest()
        filename = f"downloaded_{hash_digest}.jpg"
    return filename

def file_exists_with_same_content(filepath, content):
    if not os.path.exists(filepath):
        return False
    # Check if existing file content matches new one (avoid duplicates)
    with open(filepath, 'rb') as f:
        existing_content = f.read()
    return existing_content == content

def fetch_and_save_image(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        filename = get_filename_from_url(url)
        dir_path = "Fetched_Images"
        os.makedirs(dir_path, exist_ok=True)
        filepath = os.path.join(dir_path, filename)
        # Prevent duplicates by comparing content if file exists
        if file_exists_with_same_content(filepath, response.content):
            print(f"⚠ Skipped duplicate image: {filename}")
            return
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for URL '{url}': {e}")
    except Exception as e:
        print(f"✗ An error occurred for URL '{url}': {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    urls_input = input("https://unsplash.com/, https://www.pinterest.com/, https://www.pexels.com/: ")
    urls = [url.strip() for url in urls_input.split(",") if url.strip()]
    
    if not urls:
        print("✗ No valid URLs entered. Exiting.")
        return
    
    for url in urls:
        fetch_and_save_image(url)
    
    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
