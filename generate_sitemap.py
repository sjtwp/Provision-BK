import os
from datetime import date

# Your site's base URL
BASE_URL = "https://provisionbk.com"

# List your pages manually or read from folder structure
pages = [
    "/", "/about-us", "/services", "/contact-us", "/blog",
    "/privacy-policy", "/terms-of-service", "/sitemap"
]

# Service areas
areas = [
    "gilbert-az-bookkeeping", "phoenix-az-bookkeeping", "scottsdale-az-bookkeeping",
    "tempe-az-bookkeeping", "tucson-az-bookkeeping", "mesa-az-bookkeeping",
    "chandler-az-bookkeeping", "glendale-az-bookkeeping", "peoria-az-bookkeeping",
    "surprise-az-bookkeeping", "yuma-az-bookkeeping"
]

# Blog articles
articles = [
    "articles/5-things-to-look-for-in-a-bookkeeper",
    "articles/financial-statements-guide",
    "articles/small-business-bookkeeping",
    "articles/payroll-processing",
    "articles/quickbooks-bookkeeping-setup",
    "articles/tax-preparation-bookkeeping",
    "articles/bookkeeping-for-real-estate-agents",
    "articles/nonprofit-bookkeeping-services"
]

# Priority mapping (you can adjust)
priority = {
    "homepage": 1.0,
    "main": 0.9,
    "blog": 0.9,
    "area": 0.8,
    "legal": 0.5
}

today = date.today().isoformat()

# Generate sitemap.xml
with open("sitemap.xml", "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n\n')

    # Main pages
    for page in pages:
        prio = 0.9 if page in ["/services", "/blog"] else 0.5
        if page == "/":
            prio = 1.0
        f.write(f"  <url>\n    <loc>{BASE_URL}{page}</loc>\n")
        f.write(f"    <lastmod>{today}</lastmod>\n")
        f.write(f"    <changefreq>weekly</changefreq>\n")
        f.write(f"    <priority>{prio}</priority>\n  </url>\n\n")

    # Service areas
    for area in areas:
        f.write(f"  <url>\n    <loc>{BASE_URL}/{area}</loc>\n")
        f.write(f"    <lastmod>{today}</lastmod>\n")
        f.write(f"    <changefreq>monthly</changefreq>\n")
        f.write(f"    <priority>0.8</priority>\n  </url>\n\n")

    # Articles
    for article in articles:
        f.write(f"  <url>\n    <loc>{BASE_URL}/{article}</loc>\n")
        f.write(f"    <lastmod>{today}</lastmod>\n")
        f.write(f"    <changefreq>weekly</changefreq>\n")
        f.write(f"    <priority>0.9</priority>\n  </url>\n\n")

    f.write('</urlset>\n')
