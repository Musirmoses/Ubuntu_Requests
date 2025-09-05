# 🖼️ Multi-Page Image Crawler

A Python script that **crawls websites** (e.g., Unsplash, Pinterest, Pexels) and **downloads images** across multiple pages into a local folder.  
It’s a handy tool for mindful image collection while avoiding duplicates.

---

## 🚀 Features
- 🔎 Scrapes `<img>` tags from a given website.
- 🌐 Crawls multiple pages within the same domain.
- 💾 Saves images into a `Fetched_Images/` folder.
- ⚡ Avoids duplicate downloads (content-based check).
- 🛡️ Handles connection errors gracefully.

---

## 📦 Installation

Clone the repository (or copy the script) and install dependencies:

```bash
git clone https://github.com/yourusername/multi-page-image-crawler.git
cd multi-page-image-crawler

pip install requests beautifulsoup4
