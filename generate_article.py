import os
import sys
import json
import uuid
from datetime import datetime
import math

def parse_article_metadata(txt_file):
    """Parse metadata from a single article text file."""
    if not os.path.exists(txt_file):
        print(f"❌ Error: Input file {txt_file} not found")
        sys.exit(1)

    print(f"📄 Parsing metadata from: {txt_file}")
    title = ""
    summary = ""
    author = ""
    date = ""
    mins = ""
    image = ""
    in_summary = False

    try:
        with open(txt_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Error reading {txt_file}: {e}")
        sys.exit(1)

    for line in lines:
        line = line.strip()
        if line.startswith("Title:"):
            title = line.replace("Title:", "").strip()
        elif line.startswith("Summary:"):
            in_summary = True
            summary = line.replace("Summary:", "").strip()
        elif line.startswith("Author:"):
            in_summary = False
            author = line.replace("Author:", "").strip()
        elif line.startswith("Date:"):
            in_summary = False
            date = line.replace("Date:", "").strip()
        elif line.startswith("ReadTime:"):
            in_summary = False
            mins = line.replace("ReadTime:", "").strip()
        elif line.startswith("Image:"):
            in_summary = False
            image = line.replace("Image:", "").strip()
        elif in_summary and line:
            summary += " " + line

    # Truncate summary to 1-2 sentences for blog.html
    summary_sentences = summary.split(". ")
    short_summary = ". ".join(summary_sentences[:2]).strip()
    if short_summary and not short_summary.endswith("."):
        short_summary += "."

    try:
        # Parse date for sorting (format: Month DD, YYYY)
        parsed_date = datetime.strptime(date, "%B %d, %Y")
    except ValueError:
        print(f"⚠️ Warning: Invalid date format in {txt_file}: {date}. Using fallback date.")
        parsed_date = datetime.min

    metadata = {
        "title": title,
        "summary": short_summary,
        "author": author,
        "date": date,
        "parsed_date": parsed_date,
        "mins": mins,
        "image": f"Articles/Article_Images/{image}",
        "safe_title": title.replace(" ", "_").replace(":", "").replace("/", "_")  # Removed .html
    }
    print(f"✅ Parsed metadata: {metadata}")
    return metadata

def generate_article_html(txt_file):
    """Generate HTML for a single article."""
    if not os.path.exists(txt_file):
        print(f"❌ Error: Input file {txt_file} not found")
        sys.exit(1)

    print(f"📝 Generating article HTML for: {txt_file}")
    try:
        with open(txt_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Error reading {txt_file}: {e}")
        sys.exit(1)

    # Extract metadata
    title = ""
    summary = ""
    author = ""
    date = ""
    mins = ""
    image = ""
    sections = []
    final = []
    current_section = None
    in_summary = False
    in_final = False

    for line in lines:
        line = line.strip()
        if line.startswith("Title:"):
            in_summary = False
            in_final = False
            title = line.replace("Title:", "").strip()
        elif line.startswith("Summary:"):
            in_summary = True
            in_final = False
            summary = line.replace("Summary:", "").strip()
        elif line.startswith("Author:"):
            in_summary = False
            in_final = False
            author = line.replace("Author:", "").strip()
        elif line.startswith("Date:"):
            in_summary = False
            in_final = False
            date = line.replace("Date:", "").strip()
        elif line.startswith("ReadTime:"):
            in_summary = False
            in_final = False
            mins = line.replace("ReadTime:", "").strip()
        elif line.startswith("Image:"):
            in_summary = False
            in_final = False
            image = line.replace("Image:", "").strip()
        elif line.startswith("Section:"):
            in_summary = False
            in_final = False
            if current_section:
                sections.append(current_section)
            current_section = {"title": line.replace("Section:", "").strip(), "content": ""}
        elif line.startswith("Final:"):
            in_summary = False
            in_final = True
            if current_section:
                sections.append(current_section)
                current_section = None
        elif in_summary and line:
            summary += " " + line
        elif in_final and line:
            if line != "Final Thoughts":
                final.append(line)
        elif current_section and line:
            current_section["content"] += line + "\n"

    if current_section:
        sections.append(current_section)

    # Join final content with newlines for rendering
    final_content = "\n".join(final).strip()

    # Make sure HTML folder exists
    output_folder = os.path.join(os.path.dirname(txt_file), "Article_HTMLs")
    try:
        os.makedirs(output_folder, exist_ok=True)
    except Exception as e:
        print(f"❌ Error creating directory {output_folder}: {e}")
        sys.exit(1)

    # Generate safe file name (without .html for links, but keep .html for file output)
    safe_title = title.replace(" ", "_").replace(":", "").replace("/", "_")
    output_file = os.path.join(output_folder, f"{safe_title}.html")  # File still needs .html

    # HTML template for article
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{summary}">
    <meta name="keywords" content="bookkeeping, contractor vs employee, business finance, {author}">
    <link rel="canonical" href="https://provisionbk.com/Articles/Article_HTMLs/{safe_title}">
    <title>{title}</title>
    <link rel="stylesheet" href="../../Styles/Header.css">
    <link rel="stylesheet" href="../../Styles/Opening Picture.css">
    <link rel="stylesheet" href="../../Styles/How_We_Differ.css">
    <link rel="stylesheet" href="../../Styles/Welcome.css">
    <link rel="stylesheet" href="../../Styles/How_It_Works.css">
    <link rel="stylesheet" href="../../Styles/contact-us.css">
    <link rel="stylesheet" href="../../Styles/Footer.css">
    <link rel="stylesheet" href="../../Styles/About_Us.css">
    <link rel="stylesheet" href="../../Styles/Blog.css">
    <link rel="stylesheet" href="../../Styles/Articles.css">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;800&display=swap" rel="stylesheet">
    <link href="https://fonts.g
oogleapis.com/css2?family=Google+Sans+Code:ital,wght@0,300..800;1,300..800&display=swap" rel="stylesheet">
    <link rel="icon" type="image/x-icon" href="/Images/Provision Bookkeeping Logo.ico">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-V4S9TY013M"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-V4S9TY013M');
    </script>
    <!-- Calendly badge widget -->
    <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
    <script src="https://assets.calendly.com/assets/external/widget.js" type="text/javascript" async></script>
    <script type="text/javascript">
      window.onload = function() {{ 
        Calendly.initBadgeWidget({{ 
          url: 'https://calendly.com/provisionbk/30min?hide_event_type_details=1&hide_gdpr_banner=1&text_color=00446f&primary_color=00446f', 
          text: 'Schedule a Call', 
          color: '#fad962', 
          textColor: '#00446f', 
          branding: false 
        }}); 
      }}
    </script>
    <!-- JSON-LD Schema -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "headline": "{title}",
      "image": "https://provisionbk.com/Articles/Article_Images/{image}",
      "author": {{
        "@type": "Person",
        "name": "{author}"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "Provision Bookkeeping LLC",
        "logo": {{
          "@type": "ImageObject",
          "url": "https://provisionbk.com/Images/Provision Bookkeeping Logo.png"
        }}
      }},
      "datePublished": "{date}",
      "description": "{summary}"
    }}
    </script>
</head>
<body>
    <header>
        <div class="header-container">
            <a href="/index" class="logo">
                <img src="/Images/Provision Bookkeeping Logo.png" alt="Provision Bookkeeping LLC Logo">
                <span>PROVISION BOOKKEEPING</span>
            </a>
            <nav class="nav-menu">
                <a href="/index">Home</a>
                <a href="/about-us">About</a>
                <a href="/blog">Blog</a>
                <a href="/contact-us">Contact</a>
            </nav>
            <button class="menu-toggle" aria-label="Toggle navigation">☰</button>
        </div>
    </header>
    <main>
        <section class="previous_page1">
            <a href="/blog"><p>Back</p></a>
        </section>
        <section class="article-main">
            <div class="article-title">
                <h1>{title}</h1>
            </div>
        </section>
        <div class="date-author">
            <p>{author}</p>
            <p>{date} - {mins} read</p>
        </div>
        <article>
            <div class="article-image-summary">
                <img src="../Article_Images/{image}" alt="{title}" class="article-image">
                <div class="article-summary">{summary}</div>
            </div>
"""

    for section in sections:
        html += f"""
            <section>
                <h2>{section['title']}</h2>
                <p>{section['content'].strip().replace('\n', '</p>\n<p>')}</p>
            </section>
"""

    html += f"""
            <section>
                <h2>Final Thoughts</h2>
                <p>{final_content.replace('\n', '</p>\n<p>')}</p>
            </section>
        </article>
        <section class="previous_page2">
            <a href="/blog"><p>Back</p></a>
        </section>
    </main>
    <footer role="contentinfo">
        <div class="footer-content">
            <img src="/Images/Provision Bookkeeping Logo.png" alt="Provision Bookkeeping LLC Gilbert AZ" style="height: 20px;">
            &copy; 2025 Provision Bookkeeping LLC
            <a href="https://www.google.com/maps/search/?api=1&query=865+East+Baseline+Rd+%231091,+Gilbert,+AZ+85233" target="_blank" rel="noopener noreferrer">
                865 East Baseline Rd #1091, Gilbert, AZ 85233
            </a><br>
            <a href="tel:+16027673829">602-767-3829</a> | <a href="mailto:contact@provisionbk.com">contact@provisionbk.com</a><br>
            <div class="footer_icons">
                <a href="https://g.co/kgs/SA8hz3A" aria-label="Google"><img src="/Images/google_logo.png" alt="Google"></a>
                <a href="https://www.yelp.com/biz/provision-bookkeeping-mesa?uid=546ch3YcGUOeta71sLnMVg&utm_campaign=www_business_share_popup&utm_medium=copy_link&utm_source=(direct)" aria-label="Yelp"><img src="/Images/yelp_logo.png" alt="Yelp"></a>
                <a href="https://linkedin.com/company/provisionbookkeeping" aria-label="LinkedIn"><img src="/Images/linkedin_logo.png" alt="LinkedIn"></a>
                <a href="https://www.facebook.com/profile.php?id=61563494094507" aria-label="Facebook"><img src="/Images/facebook_logo.png" alt="Facebook"></a>
                <a href="https://www.instagram.com/provision_bookkeeping/?igsh=MXhvcnBrdTI3OGF5cA%3D%3D&utm_source=qr" aria-label="Instagram"><img src="/Images/instagram_logo.png" alt="Instagram"></a>
            </div>
            <nav class="footer-nav">
                <a href="/index" style="flex: 1; margin: 0 10px; padding: 0px 0px;">Home</a>
                <a href="/about-us" style="flex: 1; margin: 0 10px; padding: 0px 0px;">About Us</a>
                <a href="/blog" style="flex: 1; margin: 0 10px; padding: 0px 0px;">Blog</a>
                <a href="/contact-us" style="flex: 1; margin: 0 10px; padding: 0px 0px;">Contact</a>
                <a href="/sitemap" style="flex: 1; margin: 0 10px; padding: 0px 0px;">Sitemap</a>
                <a href="/privacy-policy" style="flex: 1; margin: 0 10px; padding: 0px 0px;">Privacy Policy</a>
                <a href="/terms-of-service" style="flex: 1; margin: 0 10px; padding: 0px 0px;">Terms of Service</a>
            </nav>
            <div class="cta">
                <a href="" onclick="Calendly.initPopupWidget({{url: 'https://calendly.com/provisionbk/30min?hide_event_type_details=1&hide_gdpr_banner=1&text_color=00446f&primary_color=00446f'}});return false;">Schedule a FREE Meeting</a>
            </div>
            Expert <strong>bookkeeping services</strong>, <strong>small business bookkeeping</strong>, <strong>payroll processing</strong>, and <strong>QuickBooks services</strong> serving <strong>Phoenix</strong>, <strong>Scottsdale</strong>, <strong>Tempe</strong>, <strong>Gilbert</strong>, <strong>Queen Creek</strong>, <strong>Tucson</strong>, <strong>Mesa</strong>, <strong>Chandler</strong>, <strong>Glendale</strong>, <strong>Peoria</strong>, <strong>Surprise</strong>, and <strong>Yuma</strong>.
        </div>
    </footer>
    <script>
        const menuToggle = document.querySelector('.menu-toggle');
        const navMenu = document.querySelector('.nav-menu');
        menuToggle.addEventListener('click', () => {{
            navMenu.classList.toggle('active');
        }});
        const currentPage = window.location.pathname.split('/').pop() || 'index';
        const navLinks = document.querySelectorAll('.nav-menu a');
        navLinks.forEach(link => {{
            if (link.getAttribute('href') === currentPage) {{
                link.classList.add('active');
            }} else {{
                link.classList.remove('active');
            }}
        }});
    </script>
</body>
</html>
"""

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Article HTML written to: {output_file}")
    except Exception as e:
        print(f"❌ Error writing {output_file}: {e}")
        sys.exit(1)

    return {
        "title": title,
        "summary": summary,
        "author": author,
        "date": date,
        "mins": mins,
        "image": image,
        "safe_title": safe_title  # Without .html
    }

def initialize_articles_metadata(articles_dir):
    """Initialize articles_metadata.json with existing articles if it doesn't exist."""
    metadata_file = os.path.join(articles_dir, "articles_metadata.json")
    
    if os.path.exists(metadata_file):
        print(f"📂 articles_metadata.json already exists at: {metadata_file}")
        return

    # Hardcoded metadata for existing articles from provided blog.html
    initial_articles = [
        {
            "title": "5 Things to Look for in a Bookkeeper",
            "summary": "Hiring a bookkeeper is one of the most important financial decisions a business owner can make. The right partner can provide clarity and confidence, while the wrong choice can cause stress and serious financial setbacks.",
            "author": "Matthew Jacob, MAcc",
            "date": "October 3, 2025",
            "parsed_date": datetime.strptime("October 3, 2025", "%B %d, %Y").isoformat(),
            "mins": "5 min",
            "image": "Images/5 Qualities Bookkeepers Must Have.avif",
            "safe_title": "5_Things_To_Look_For_In_A_Bookkeeper"  # Without .html
        },
        {
            "title": "Save Money. Be Frugal!",
            "summary": "As business owners, it’s easy to get caught up in the day-to-day grind and lose sight of where money is actually being wasted. Here are five areas where every business owner should be frugal.",
            "author": "",
            "date": "September 26, 2025",
            "parsed_date": datetime.strptime("September 26, 2025", "%B %d, %Y").isoformat(),
            "mins": "",
            "image": "Images/Save_Money.jpg",
            "safe_title": "Save_Money._Be_Frugal"  # Without .html
        },
        {
            "title": "Understanding Financial Statements",
            "summary": "Financial statements can feel intimidating, but the goal here is not to overcomplicate something that often seems confusing.",
            "author": "",
            "date": "September 19, 2025",
            "parsed_date": datetime.strptime("September 19, 2025", "%B %d, %Y").isoformat(),
            "mins": "",
            "image": "Images/financial_statements.png",
            "safe_title": "Financial_Statements_guide"  # Without .html
        },
        {
            "title": "CPA vs. Bookkeeper: Understanding the Difference",
            "summary": "In business finances, two key professionals often come up in conversation: the CPA (Certified Public Accountant) and the bookkeeper. Many business owners wonder, “Do I really need both?”",
            "author": "",
            "date": "September 12, 2025",
            "parsed_date": datetime.strptime("September 12, 2025", "%B %d, %Y").isoformat(),
            "mins": "",
            "image": "Images/CPA_v_BK.jpg",
            "safe_title": "cpa_vs_bookkeeper"  # Without .html
        }
    ]

    try:
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(initial_articles, f, indent=2)
        print(f"✅ Initialized articles_metadata.json at: {metadata_file}")
        print(f"📄 Initial articles: {[a['title'] for a in initial_articles]}")
    except Exception as e:
        print(f"❌ Error creating {metadata_file}: {e}")
        sys.exit(1)

def load_articles_metadata(articles_dir):
    """Load articles metadata from JSON file."""
    metadata_file = os.path.join(articles_dir, "articles_metadata.json")
    print(f"📂 Attempting to load: {metadata_file}")

    if not os.path.exists(metadata_file):
        print(f"⚠️ {metadata_file} not found, initializing...")
        initialize_articles_metadata(articles_dir)
    
    try:
        with open(metadata_file, "r", encoding="utf-8") as f:
            articles = json.load(f)
    except Exception as e:
        print(f"❌ Error reading {metadata_file}: {e}")
        sys.exit(1)
    
    # Convert parsed_date strings back to datetime objects
    for article in articles:
        article["parsed_date"] = datetime.fromisoformat(article["parsed_date"])
    
    print(f"✅ Loaded {len(articles)} articles from {metadata_file}")
    return articles

def save_articles_metadata(articles_dir, articles):
    """Save articles metadata to JSON file."""
    metadata_file = os.path.join(articles_dir, "articles_metadata.json")
    print(f"📝 Saving metadata to: {metadata_file}")

    # Convert datetime objects to ISO format for JSON serialization
    articles_to_save = []
    for article in articles:
        article_copy = article.copy()
        article_copy["parsed_date"] = article["parsed_date"].isoformat()
        articles_to_save.append(article_copy)
    
    try:
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(articles_to_save, f, indent=2)
        print(f"✅ Updated articles_metadata.json with {len(articles)} articles")
    except Exception as e:
        print(f"❌ Error writing {metadata_file}: {e}")
        sys.exit(1)

def generate_blog_html(articles, output_dir):
    """Generate blog.html and additional pages with up to 6 articles each."""
    print(f"📝 Generating blog pages in: {output_dir}")
    # Sort articles by date (newest first)
    articles.sort(key=lambda x: x["parsed_date"], reverse=True)

    # Calculate total pages (6 articles per page)
    articles_per_page = 6
    total_pages = math.ceil(len(articles) / articles_per_page)
    print(f"📄 Total articles: {len(articles)}, Total pages: {total_pages}")

    for page in range(1, total_pages + 1):
        # Determine articles for this page
        start_idx = (page - 1) * articles_per_page
        end_idx = start_idx + articles_per_page
        page_articles = articles[start_idx:end_idx]
        
        # Determine output file
        output_file = os.path.join(output_dir, "blog.html" if page == 1 else f"blog_page_{page}.html")
        print(f"📝 Generating page {page}: {output_file}")

        # HTML template for blog page
        blog_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "Provision Bookkeeping LLC",
      "image": "/Images/Provision Bookkeeping Logo.png",
      "url": "https://provisionbk.com",
      "telephone": "+1-602-767-3829",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "865 East Baseline Rd #1091",
        "addressLocality": "Gilbert",
        "addressRegion": "AZ",
        "postalCode": "85233",
        "addressCountry": "US"
      }},
      "geo": {{
        "@type": "GeoCoordinates",
        "latitude": "33.3772794",
        "longitude": "-111.8123101"
      }},
      "openingHours": "Mo-Fr 8:00-17:00",
      "sameAs": [
        "https://g.co/kgs/SA8hz3A",
        "https://www.yelp.com/biz/provision-bookkeeping-mesa?uid=546ch3YcGUOeta71sLnMVg&utm_campaign=www_business_share_popup&utm_medium=copy_link&utm_source=(direct)",
        "https://www.facebook.com/profile.php?id=61563494094507",
        "https://www.instagram.com/provision_bookkeeping/?igsh=MXhvcnBrdTI3OGF5cA%3D%3D&utm_source=qr"
      ]
    }}
    </script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-V4S9TY013M"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-V4S9TY013M');
    </script>
    <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
    <script src="https://assets.calendly.com/assets/external/widget.js" type="text/javascript" async></script>
    <script type="text/javascript">window.onload = function() {{ Calendly.initBadgeWidget({{ url: 'https://calendly.com/provisionbk/30min?hide_event_type_details=1&hide_gdpr_banner=1&text_color=00446f&primary_color=00446f', text: 'Schedule a Call', color: '#fad962', textColor: '#00446f', branding: false }}); }}</script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="About Provision Bookkeeping LLC in AZ. Trusted bookkeeping experts for family-owned businesses. Learn more!">
    <meta name="keywords" content="about bookkeeping, Chandler AZ bookkeeping, bookkeeping near me, family business financial services">
    <title>Blog{' - Page ' + str(page) if page > 1 else ''}</title>
    <link rel="stylesheet" href="/Styles/Header.css">
    <link rel="icon" type="image/x-icon" href="/Images/Provision Bookkeeping Logo.ico">
    <link rel="stylesheet" href="/Styles/Opening Picture.css">
    <link rel="stylesheet" href="/Styles/How_We_Differ.css">
    <link rel="stylesheet" href="/Styles/Welcome.css">
    <link rel="stylesheet" href="/Styles/How_It_Works.css">
    <link rel="stylesheet" href="/Styles/contact-us.css">
    <link rel="stylesheet" href="/Styles/Footer.css">
    <link rel="stylesheet" href="/Styles/About_Us.css">
    <link rel="stylesheet" href="/Styles/Blog.css">
    <link rel="stylesheet" href="/Styles/Articles.css">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;800&display=swap" rel="stylesheet">
</head>
<body>
  <header>
    <div class="header-container">
      <a href="/index" class="logo">
        <img src="/Images/Provision Bookkeeping Logo.png" alt="Provision Bookkeeping LLC Logo">
        <span>PROVISION BOOKKEEPING</span>
      </a>
      <nav class="nav-menu">
        <a href="/index">Home</a>
        <a href="/about-us">About</a>
        <a href="/blog">Blog</a>
        <a href="/contact-us">Contact</a>
      </nav>
      <button class="menu-toggle" aria-label="Toggle navigation">☰</button>
    </div>
  </header>
  <section class="Blog-main">
    <div class="Blog-title">
      <h1>Blog{' - Page ' + str(page) if page > 1 else ''}</h1>
    </div>
    <div class="blog-container">
"""

        # Add articles for this page
        for article in page_articles:
            # Convert date to MM/DD/YYYY for display
            try:
                display_date = datetime.strptime(article['date'], "%B %d, %Y").strftime("%m/%d/%Y")
            except ValueError:
                display_date = article['date']
            
            blog_html += f"""
      <div class="blog-article">
        <a href="/Articles/Article_HTMLs/{article['safe_title']}">
          <h2>{article['title']}</h2>
        </a>
        <div class="meta">{display_date}<span class="highlight"></span></div>
        <a href="/Articles/Article_HTMLs/{article['safe_title']}">
          <img src="/{article['image']}" alt="{article['title']}">
        </a>
        <p>{article['summary']}</p>
        <p>
          <a href="/Articles/Article_HTMLs/{article['safe_title']}">
            Read More
          </a>
        </p>
      </div>
"""

        # Add pagination navigation
        blog_html += """
    </div>
    <div class="pagination">
"""
        if page > 1:
            prev_page = "blog" if page == 2 else f"blog_page_{page-1}"
            blog_html += f"""
      <a href="/{prev_page}" class="pagination-link">Previous</a>
"""
        if page < total_pages:
            next_page = f"blog_page_{page+1}"
            blog_html += f"""
      <a href="/{next_page}" class="pagination-link">Next</a>
"""
        blog_html += """
    </div>
  </section>
  <footer role="contentinfo">
    <div class="footer-content">
      <img src="/Images/Provision Bookkeeping Logo.png" alt="Provision Bookkeeping LLC Gilbert AZ" style="height: 20px;">
      &copy; 2025 Provision Bookkeeping LLC
      <a href="https://www.google.com/maps/search/?api=1&query=865+East+Baseline+Rd+%231091,+Gilbert,+AZ+85233" target="_blank" rel="noopener noreferrer">
        865 East Baseline Rd #1091, Gilbert, AZ 85233
      </a><br>
      <a href="tel:+16027673829">602-767-3829</a> | <a href="mailto:contact@provisionbk.com">contact@provisionbk.com</a><br>
      <div class="footer_icons">
        <a href="https://g.co/kgs/SA8hz3A" aria-label="Google">
          <img src="/Images/google_logo.png" alt="Google">
        </a>
        <a href="https://www.yelp.com/biz/provision-bookkeeping-mesa?uid=546ch3YcGUOeta71sLnMVg&utm_campaign=www_business_share_popup&utm_medium=copy_link&utm_source=(direct)" aria-label="Yelp">
          <img src="/Images/yelp_logo.png" alt="Yelp">
        </a>
        <a href="https://linkedin.com/company/provisionbookkeeping" aria-label="LinkedIn">
          <img src="/Images/linkedin_logo.png" alt="LinkedIn">
        </a>
        <a href="https://www.facebook.com/profile.php?id=61563494094507" aria-label="Facebook">
          <img src="/Images/facebook_logo.png" alt="Facebook">
        </a>
        <a href="https://www.instagram.com/provision_bookkeeping/?igsh=MXhvcnBrdTI3OGF5cA%3D%3D&utm_source=qr" aria-label="Instagram">
          <img src="/Images/instagram_logo.png" alt="Instagram">
        </a>
      </div>
      <nav class="footer-nav">
        <a href="/index" style="flex: 1; margin: 0 10px; padding: 0px 0px;">Home</a>
        <a href="/about-us" style="flex: 1; margin: 0 10px; padding: 0px 0px;">About Us</a>
        <a href="/blog" style="flex: 1; margin: 0 10px; padding: 0px 0px;">Blog</a>
        <a href="/contact-us" style="flex: 1; margin: 0 10px; padding: 0px 0px;">Contact</a>
        <a href="/sitemap" style="flex: 1; margin: 0 10px; padding: 0px 0px;">Sitemap</a>
        <a href="/privacy-policy" style="flex: 1; margin: 0 10px; padding: 0px 0px;">Privacy Policy</a>
        <a href="/terms-of-service" style="flex: 1; margin: 0 10px; padding: 0px 0px;">Terms of Service</a>
      </nav>
      <div class="cta">
        <a href="" onclick="Calendly.initPopupWidget({url: 'https://calendly.com/provisionbk/30min?hide_event_type_details=1&hide_gdpr_banner=1&text_color=00446f&primary_color=00446f'});return false;">Schedule a FREE Meeting</a>
      </div>
      Expert <strong>bookkeeping services</strong>, <strong>small business bookkeeping</strong>, <strong>payroll processing</strong>, and <strong>QuickBooks services</strong> serving <strong>Phoenix</strong>, <strong>Scottsdale</strong>, <strong>Tempe</strong>, <strong>Gilbert</strong>, <strong>Queen Creek</strong>, <strong>Tucson</strong>, <strong>Mesa</strong>, <strong>Chandler</strong>, <strong>Glendale</strong>, <strong>Peoria</strong>, <strong>Surprise</strong>, and <strong>Yuma</strong>.
    </div>
  </footer>
  <script>
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    menuToggle.addEventListener('click', () => {
      navMenu.classList.toggle('active');
    });
    const currentPage = window.location.pathname.split('/').pop() || 'index';
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
      if (link.getAttribute('href') === currentPage) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  </script>
</body>
</html>
"""

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(blog_html)
            print(f"✅ Blog page {page} generated at: {output_file}")
        except Exception as e:
            print(f"❌ Error writing {output_file}: {e}")
            sys.exit(1)

def generate_article_from_txt(txt_file):
    """Main function to generate article HTML and update blog.html."""
    # Verify input file
    if not os.path.exists(txt_file):
        print(f"❌ Error: Input file {txt_file} not found")
        sys.exit(1)

    print(f"🚀 Starting processing for: {txt_file}")
    # Generate article HTML and get metadata
    article_metadata = generate_article_html(txt_file)
    articles_dir = os.path.dirname(txt_file)

    # Load existing articles metadata
    articles = load_articles_metadata(articles_dir)

    # Check if the new article is already in the metadata (to avoid duplicates)
    new_article = parse_article_metadata(txt_file)
    if not any(a["safe_title"] == new_article["safe_title"] for a in articles):
        articles.append(new_article)
        save_articles_metadata(articles_dir, articles)
    else:
        print(f"⚠️ Article {new_article['title']} already exists in metadata, skipping addition")

    # Generate blog.html and additional pages
    output_dir = os.path.dirname(articles_dir)
    generate_blog_html(articles, output_dir)

    print(f"✅ Article HTML generated at: {os.path.join(articles_dir, 'Article_HTMLs', article_metadata['safe_title'] + '.html')}")
    print(f"✅ Process completed for: {txt_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_article.py Articles\\new_article.txt")
        sys.exit(1)
    else:
        # Normalize path to handle different OS separators and spaces
        txt_file = os.path.normpath(sys.argv[1])
        generate_article_from_txt(txt_file)