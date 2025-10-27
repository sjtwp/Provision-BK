#!/usr/bin/env python3
import os
import json
from datetime import datetime

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
BASE_URL         = "https://provisionbk.com"
PROJECT_ROOT     = os.getcwd()
OUTPUT_PATH      = os.path.join(PROJECT_ROOT, "public", "sitemap.xml")
META_PATH        = os.path.join(PROJECT_ROOT, "Articles", "articles_metadata.json")
HTML_DIR         = os.path.join(PROJECT_ROOT, "Articles", "Article_HTMLs")  # <-- HTML files here

# Static pages
STATIC_PAGES = [
    "/", "/about-us", "/services", "/contact-us", "/blog",
    "/privacy-policy", "/terms-of-service", "/sitemap"
]

# Service area slugs
SERVICE_AREAS = [
    "gilbert-az-bookkeeping", "phoenix-az-bookkeeping", "scottsdale-az-bookkeeping",
    "tempe-az-bookkeeping", "tucson-az-bookkeeping", "mesa-az-bookkeeping",
    "chandler-az-bookkeeping", "glendale-az-bookkeeping", "peoria-az-bookkeeping",
    "surprise-az-bookkeeping", "yuma-az-bookkeeping"
]

# ----------------------------------------------------------------------
# Load metadata + match with real HTML files
# ----------------------------------------------------------------------
blog_entries = []  # (url_path, lastmod_date)

if not os.path.isfile(META_PATH):
    print(f"ERROR: Metadata file not found: {META_PATH}")
else:
    print(f"Found metadata: {META_PATH}")
    try:
        with open(META_PATH, "r", encoding="utf-8") as f:
            articles = json.load(f)

        print(f"Found {len(articles)} articles in metadata.")

        for art in articles:
            safe_title = art.get("safe_title", "").strip()
            if not safe_title:
                print("  Skipping article with no safe_title")
                continue

            # Normalize filename
            if not safe_title.lower().endswith(".html"):
                safe_title += ".html"
            html_filename = safe_title

            # Build expected HTML path
            html_path = os.path.join(HTML_DIR, html_filename)

            # 1. Try to get real file modification date
            if os.path.isfile(html_path):
                mod_timestamp = os.path.getmtime(html_path)
                iso_date = datetime.fromtimestamp(mod_timestamp).date().isoformat()
                source = "file"
            else:
                # 2. Fallback: use parsed_date from JSON
                parsed = art.get("parsed_date", "").split("T")[0]
                if parsed:
                    iso_date = parsed
                    source = "JSON parsed_date"
                else:
                    # 3. Ultimate fallback: parse "date" field
                    raw = art.get("date", "")
                    try:
                        iso_date = datetime.strptime(raw, "%B %d, %Y").date().isoformat()
                        source = "JSON date field"
                    except:
                        iso_date = datetime.today().date().isoformat()
                        source = "today (fallback)"
                print(f"  Warning: HTML not found: {html_path} → using {source}")

            url_path = f"articles/{html_filename}"
            blog_entries.append((url_path, iso_date))

    except Exception as e:
        print(f"ERROR parsing JSON: {e}")

# ----------------------------------------------------------------------
# Helper: write <url> block
# ----------------------------------------------------------------------
def write_url(f, loc: str, lastmod: str, changefreq: str, priority: float):
    f.write("  <url>\n")
    f.write(f"    <loc>{loc}</loc>\n")
    f.write(f"    <lastmod>{lastmod}</lastmod>\n")
    f.write(f"    <changefreq>{changefreq}</changefreq>\n")
    f.write(f"    <priority>{priority:.1f}</priority>\n")
    f.write("  </url>\n\n")

# ----------------------------------------------------------------------
# Generate sitemap.xml
# ----------------------------------------------------------------------
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
today = datetime.today().date().isoformat()

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n\n')

    # 1. Static pages
    for page in STATIC_PAGES:
        prio = 1.0 if page == "/" else 0.9 if page in ("/services", "/blog") else 0.5
        write_url(f, f"{BASE_URL}{page}", today, "weekly", prio)

    # 2. Service areas
    for area in SERVICE_AREAS:
        write_url(f, f"{BASE_URL}/{area}", today, "monthly", 0.8)

    # 3. Blog articles
    for rel_path, mod_date in blog_entries:
        write_url(f, f"{BASE_URL}/{rel_path}", mod_date, "weekly", 0.9)

    # 4. Sitemap itself
    write_url(f, f"{BASE_URL}/sitemap.xml", today, "monthly", 0.3)

    f.write('</urlset>\n')

# ----------------------------------------------------------------------
# Final Summary
# ----------------------------------------------------------------------
print(f"\nSitemap generated: {OUTPUT_PATH}")
print(f"   {len(STATIC_PAGES)} static pages")
print(f"   {len(SERVICE_AREAS)} service-area pages")
print(f"   {len(blog_entries)} blog articles (with real or fallback dates)")