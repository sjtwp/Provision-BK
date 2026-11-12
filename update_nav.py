#!/usr/bin/env python3
"""Rebuild the top menu (with dropdowns) on every page of the site.

Run from the website folder:  python update_nav.py
generate_article.py runs this automatically after adding an article, so the
Blog dropdown always shows the 5 newest articles.

To change a menu item or a city, edit the lists below and run this script.
"""
import os, re, json, glob
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(ROOT, "Articles", "articles_metadata.json")

CITIES = [
    ("gilbert", "Gilbert"), ("mesa", "Mesa"), ("chandler", "Chandler"),
    ("queen-creek", "Queen Creek"), ("phoenix", "Phoenix"), ("scottsdale", "Scottsdale"),
]

SERVICES = [
    ("monthly-bookkeeping", "Monthly Bookkeeping"),
    ("catch-up-bookkeeping", "Catch-Up & Cleanup"),
    ("quickbooks-online-setup", "QuickBooks Online Setup & Training"),
    ("payroll-services", "Payroll & 1099s"),
    ("financial-statements", "Monthly Financial Statements"),
    ("year-end-tax-ready-books", "Year-End & Tax-Ready Books"),
]

INDUSTRIES = [
    ("bookkeeping-for-contractors", "Contractors & Construction"),
    ("real-estate-agent-bookkeeping", "Real Estate Agents"),
    ("rental-property-bookkeeping", "Rental Property Owners"),
    ("fix-and-flip-bookkeeping", "Fix & Flip Investors"),
    ("medical-practice-bookkeeping", "Doctors & Medical Practices"),
    ("dental-practice-bookkeeping", "Dentists & Dental Practices"),
    ("restaurant-bookkeeping", "Restaurants & Food Service"),
    ("ecommerce-bookkeeping", "E-commerce & Retail"),
    ("professional-services-bookkeeping", "Professional Services"),
    ("salon-spa-bookkeeping", "Salons, Spas & Fitness"),
]

CALENDLY = "https://calendly.com/provisionbk/30min?hide_event_type_details=1&hide_gdpr_banner=1&text_color=00446f&primary_color=00446f"
PHONE_DISPLAY, PHONE_TEL = "(602) 767-3829", "+16027673829"
EMAIL = "contact@provisionbk.com"

START, END = "<!-- NAV START -->", "<!-- NAV END -->"
CSS_LINK = '<link rel="stylesheet" href="/Styles/Nav_Dropdown.css?v=202611122311">'


def recent_articles(n=5):
    try:
        with open(META, encoding="utf-8") as f:
            arts = json.load(f)
    except Exception:
        return []
    def when(a):
        try:
            return datetime.fromisoformat(str(a.get("parsed_date", ""))[:19])
        except Exception:
            return datetime.min
    out = []
    for a in sorted(arts, key=when, reverse=True)[:n]:
        slug = a.get("safe_title", "")
        if slug.lower().endswith(".html"):
            slug = slug[:-5]
        slug = slug.rstrip(".")
        title = a.get("title", "").strip().rstrip(".")
        out.append((f"/Articles/Article_HTMLs/{slug}", title))
    return out


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def dropdown(label, href, items, key):
    links = "\n".join(f'          <a href="{h}"{extra}>{esc(t) if not raw else t}</a>'
                      for h, t, extra, raw in items)
    return (f'        <div class="nav-item has-dropdown">\n'
            f'          <a href="{href}">{label}</a><button class="dd-toggle" type="button" aria-label="Show {label} menu" aria-expanded="false">&#9662;</button>\n'
            f'          <div class="dropdown" id="dd-{key}">\n{links}\n          </div>\n'
            f'        </div>')


def build_nav():
    blog_items = [(h, t, "", False) for h, t in recent_articles()]
    blog_items.append(("/blog", "All articles &rarr;", ' class="dd-all"', True))
    fr_items = [
        ("/free-resources#guides", "Guides", "", False),
        ("/free-resources#checklists", "Checklists", "", False),
        ("/free-resources#templates", "Templates & Calculators", "", False),
        ("/free-resources#forms", "New Hire & Vendor Forms", "", False),
    ]
    svc_items = [(f"/{s}", n, "", False) for s, n in SERVICES]
    svc_items.append(("/services", "All services &rarr;", ' class="dd-all"', True))
    ind_items = [(f"/{s}", n, "", False) for s, n in INDUSTRIES]
    ind_items.append(("/industries", "All industries &rarr;", ' class="dd-all"', True))
    sa_items = [(f"/{s}-az-bookkeeping", n, "", False) for s, n in CITIES]
    sa_items.append(("/service-areas", "All of Arizona &rarr;", ' class="dd-all"', True))
    cal_onclick = ("if(window.Calendly){Calendly.initPopupWidget({url:'" + CALENDLY + "'});return false;}")
    contact_items = [
        (CALENDLY, "Schedule a Meeting", f' target="_blank" rel="noopener" onclick="{cal_onclick}"', False),
        (f"tel:{PHONE_TEL}", f"Call {PHONE_DISPLAY}", "", False),
        (f"mailto:{EMAIL}", f"Email {EMAIL}", "", False),
        ("/contact-us", "Contact Form", "", False),
    ]
    return "\n".join([
        START,
        '      <nav class="nav-menu">',
        '        <a href="/">Home</a>',
        '        <a href="/about-us">About</a>',
        dropdown("Services", "/services", svc_items, "services"),
        dropdown("Industries", "/industries", ind_items, "industries"),
        dropdown("Blog", "/blog", blog_items, "blog"),
        dropdown("Free Resources", "/free-resources", fr_items, "resources"),
        dropdown("Service Areas", "/service-areas", sa_items, "areas"),
        dropdown("Contact", "/contact-us", contact_items, "contact"),
        '      </nav>',
        '      <script>',
        '        document.querySelectorAll(".dd-toggle").forEach(function (b) {',
        '          b.addEventListener("click", function (e) {',
        '            e.stopPropagation();',
        '            var item = b.parentElement, open = !item.classList.contains("open");',
        '            document.querySelectorAll(".has-dropdown.open").forEach(function (o) { o.classList.remove("open"); o.querySelector(".dd-toggle").setAttribute("aria-expanded", "false"); });',
        '            if (open) { item.classList.add("open"); b.setAttribute("aria-expanded", "true"); }',
        '          });',
        '        });',
        '        document.addEventListener("click", function () { document.querySelectorAll(".has-dropdown.open").forEach(function (o) { o.classList.remove("open"); }); });',
        '      </script>',
        '      ' + END,
    ])


NAV_RE = re.compile(r'(' + re.escape(START) + r'.*?' + re.escape(END) + r'|<nav class="nav-menu">.*?</nav>)', re.S)


def apply(path, nav):
    with open(path, encoding="utf-8", newline="") as f:
        s = f.read()
    nl = "\r\n" if "\r\n" in s else "\n"
    body = s.replace("\r\n", "\n")
    if not NAV_RE.search(body):
        return False
    new = NAV_RE.sub(lambda m: nav, body, count=1)
    if "Nav_Dropdown.css" not in new:
        new = re.sub(r'(<link rel="stylesheet" href="[^"]*Header\.css"\s*/?>)', lambda m: m.group(1) + "\n    " + CSS_LINK, new, count=1)
    new = new.replace("\n", nl)
    if new != s:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new)
        return True
    return False


def main():
    nav = build_nav()
    files = glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "Articles", "Article_HTMLs", "*.html"))
    changed = sum(apply(p, nav) for p in files)
    print(f"Menu updated on {changed} of {len(files)} pages.")


if __name__ == "__main__":
    main()
