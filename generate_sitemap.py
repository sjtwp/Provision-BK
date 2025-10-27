#!/usr/bin/env python3
import os
import json
from datetime import datetime
import urllib.request

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
BASE_URL         = "https://provisionbk.com"
PROJECT_ROOT     = os.getcwd()
OUTPUT_PATH      = os.path.join(PROJECT_ROOT, "sitemap.xml")
META_PATH        = os.path.join(PROJECT_ROOT, "Articles", "articles_metadata.json")
HTML_DIR         = os.path.join(PROJECT_ROOT, "Articles", "Article_HTMLs")

# Static pages
STATIC_PAGES = [
    "/", "/about-us", "/services", "/contact-us", "/blog",
    "/privacy-policy", "/terms-of-service", "/sitemap"
]

# Service areas
SERVICE_AREAS = [
    "gilbert-az-bookkeeping", "phoenix-az-bookkeeping", "scottsdale-az-bookkeeping",
    "tempe-az-bookkeeping", "tucson-az-bookkeeping", "mesa-az-bookkeeping",
    "chandler-az-bookkeeping", "glendale-az-bookkeeping", "peoria-az-bookkeeping",
    "surprise-az-bookkeeping", "yuma-az-bookkeeping"
]

# ----------------------------------------------------------------------
# Load metadata + get real file dates
# ----------------------------------------------------------------------
blog_entries = []

if not os.path.isfile(META_PATH):
    print(f"ERROR: Metadata file not found: {META_PATH}")
else:
    print(f"Found metadata: {META_PATH}")
    try:
        with open(META_PATH, "r", encoding="utf-8") as f:
            articles = json.load(f)

        for art in articles:
            safe_title = art.get("safe_title", "").strip()
            if not safe_title or not safe_title.lower().endswith(".html"):
                safe_title = (safe_title or "unknown") + ".html" if not safe_title.lower().endswith(".html") else safe_title

            html_path = os.path.join(HTML_DIR, safe_title)

            # Use file mod time if exists
            if os.path.isfile(html_path):
                iso_date = datetime.fromtimestamp(os.path.getmtime(html_path)).date().isoformat()
            else:
                # Fallback to JSON
                parsed = art.get("parsed_date", "").split("T")[0]
                if parsed:
                    iso_date = parsed
                else:
                    try:
                        iso_date = datetime.strptime(art.get("date", ""), "%B %d, %Y").date().isoformat()
                    except:
                        iso_date = datetime.today().date().isoformat()
                print(f"  Warning: HTML not found: {html_path} → using JSON date")

            url_path = f"articles/{safe_title}"
            blog_entries.append((url_path, iso_date))

    except Exception as e:
        print(f"ERROR parsing JSON: {e}")

# ----------------------------------------------------------------------
# Write XML
# ----------------------------------------------------------------------
def write_url(f, loc, lastmod, changefreq, priority):
    f.write("  <url>\n")
    f.write(f"    <loc>{loc}</loc>\n")
    f.write(f"    <lastmod>{lastmod}</lastmod>\n")
    f.write(f"    <changefreq>{changefreq}</changefreq>\n")
    f.write(f"    <priority>{priority:.1f}</priority>\n")
    f.write("  </url>\n\n")

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
today = datetime.today().date().isoformat()

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n\n')

    for page in STATIC_PAGES:
        prio = 1.0 if page == "/" else 0.9 if page in ("/services", "/blog") else 0.5
        write_url(f, f"{BASE_URL}{page}", today, "weekly", prio)

    for area in SERVICE_AREAS:
        write_url(f, f"{BASE_URL}/{area}", today, "monthly", 0.8)

    for rel_path, mod_date in blog_entries:
        write_url(f, f"{BASE_URL}/{rel_path}", mod_date, "weekly", 0.9)

    write_url(f, f"{BASE_URL}/sitemap.xml", today, "monthly", 0.3)

    f.write('</urlset>\n')

# ----------------------------------------------------------------------
# Ping Google & Bing
# ----------------------------------------------------------------------
def ping_search_engines():
    sitemap_url = f"{BASE_URL}/sitemap.xml"
    for url in [
        f"https://www.google.com/ping?sitemap={sitemap_url}",
        f"https://www.bing.com/ping?sitemap={sitemap_url}"
    ]:
        try:
            urllib.request.urlopen(url, timeout=10)
            print(f"Pinged: {url}")
        except:
            print(f"Ping failed: {url}")

ping_search_engines()

# ----------------------------------------------------------------------
# Done
# ----------------------------------------------------------------------
print(f"\nSitemap generated: {OUTPUT_PATH}")
print(f"   {len(STATIC_PAGES)} static pages")
print(f"   {len(SERVICE_AREAS)} service areas")
print(f"   {len(blog_entries)} blog articles")