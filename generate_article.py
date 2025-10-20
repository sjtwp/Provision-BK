import os
import sys
from datetime import datetime
import textwrap
import re

def generate_article_from_txt(txt_file):
    # Make sure Articles folder exists
    articles_folder = "Articles"
    images_folder = "../Article_Images/"
    
    os.makedirs(articles_folder, exist_ok=True)

    if not os.path.exists(txt_file):
        print(f"Error: File {txt_file} not found!")
        return

    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse the content using regex patterns
    patterns = {
        'title': r'Title:\s*(.+?)(?=\n)',
        'author': r'Author:\s*(.+?)(?=\n)',
        'date': r'Date:\s*(.+?)(?=\n)',
        'readtime': r'ReadTime:\s*(.+?)(?=\n)',
        'image': r'Image:\s*(.+?)(?=\n)',
        'summary': r'Summary:\n((?:.|\n)+?)(?=Sections:)'
    }
    
    # Extract basic fields
    title = re.search(patterns['title'], content, re.IGNORECASE).group(1).strip()
    author = re.search(patterns['author'], content, re.IGNORECASE).group(1).strip()
    date_str = re.search(patterns['date'], content, re.IGNORECASE).group(1).strip()
    mins_read = re.search(patterns['readtime'], content, re.IGNORECASE).group(1).strip()
    image_name = re.search(patterns['image'], content, re.IGNORECASE).group(1).strip()
    summary_match = re.search(patterns['summary'], content, re.IGNORECASE | re.DOTALL)
    summary = summary_match.group(1).strip() if summary_match else ""

    # Parse date to standard format
    try:
        if "October" in date_str:
            date_obj = datetime.strptime(date_str, "%B %d, %Y")
        else:
            date_obj = datetime.strptime(date_str, "%m/%d/%Y")
        formatted_date = date_obj.strftime("%m/%d/%Y")
    except:
        formatted_date = date_str

    # Parse sections
    sections_content = re.search(r'Sections:\n((?:.|\n)+?)(?=Final Thoughts:|$)', content, re.IGNORECASE | re.DOTALL)
    sections_text = sections_content.group(1).strip() if sections_content else ""
    
    # Parse numbered sections (1. Title\nContent\n2. Title\nContent...)
    section_pattern = r'(\d+)\.\s*(.+?)(?=\n\d+\.|$)(?:[\s\S]*?)(?=\n\d+\.|\nFinal|\Z)'
    sections = []
    for match in re.finditer(section_pattern, sections_text, re.DOTALL):
        num = match.group(1)
        title = match.group(2).strip()
        content = re.sub(r'^\d+\.\s*.+\n', '', match.group(0), flags=re.MULTILINE).strip()
        sections.append({"title": title, "content": content})

    # Parse final thoughts
    final_thoughts_match = re.search(r'Final Thoughts:\n((?:.|\n)+?)$', content, re.IGNORECASE | re.DOTALL)
    final_thoughts = final_thoughts_match.group(1).strip() if final_thoughts_match else ""

    # Generate safe filename
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
    html_file_path = os.path.join(articles_folder, f"{safe_title}.html")
    image_path = f"{images_folder}{image_name}"

    # Generate HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{summary[:160]}">
    <title>{title}</title>
    <link rel="stylesheet" href="../Styles/Header.css" />
    <link rel="stylesheet" href="../Styles/Opening Picture.css" />
    <link rel="stylesheet" href="../Styles/How_We_Differ.css" />
    <link rel="stylesheet" href="../Styles/Welcome.css" />
    <link rel="stylesheet" href="../Styles/How_It_Works.css">
    <link rel="stylesheet" href="../Styles/contact-us.css">
    <link rel="stylesheet" href="../Styles/Footer.css">
    <link rel="stylesheet" href="../Styles/About_Us.css">
    <link rel="stylesheet" href="../Styles/Blog.css">
    <link rel="stylesheet" href="../Styles/Articles.css">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;800&display=swap" rel="stylesheet">
</head>
<body>

<header>
    <div class="header-container">
        <a href="/" class="logo">
            <img src="../Provision Bookkeeping Logo.ico.png" alt="Provision Bookkeeping LLC Logo">
            <span>PROVISION BOOKKEEPING</span>
        </a>
        <nav class="nav-menu">
            <a href="../">Home</a>
            <a href="../about-us">About</a>
            <a href="../blog">Blog</a>
            <a href="../contact-us">Contact</a>
        </nav>
        <button class="menu-toggle" aria-label="Toggle navigation">☰</button>
    </div>
</header>

<main>
    <section class="previous_page1">
        <a href="../blog"><p>Back</p></a>
    </section>

    <section class="article-main">
        <div class="article-title"><h1>{title}</h1></div>
    </section>

    <div class="date-author">
        <p>{author}</p>
        <p>{formatted_date}  -  {mins_read}</p>
    </div>

    <article>
        <div class="article-image-summary">
            <img src="{image_path}" alt="{title}" class="article-image">
            <div class="article-summary">{summary}</div>
        </div>
"""

    # Add all sections
    for section in sections:
        content_wrapped = textwrap.fill(section['content'], width=100)
        html_content += f"""
        <section>
            <h2>{section['title']}</h2>
            <p>{content_wrapped}</p>
        </section>
"""

    # Final thoughts
    if final_thoughts:
        html_content += f"""
        <section>
            <h2>Final Thoughts</h2>
            <p>{textwrap.fill(final_thoughts, width=100)}</p>
        </section>
"""

    # Footer and closing
    html_content += """
</article>

<section class="previous_page2">
    <a href="../blog"><p>Back</p></a>
</section>
</main>

<footer role="contentinfo">
<div class="footer-content">
    <img src="../Provision Bookkeeping Logo.ico.png" alt="Provision Bookkeeping LLC Gilbert AZ" style="height: 20px;">
    &copy; 2025 Provision Bookkeeping LLC
    <a href="https://www.google.com/maps/search/?api=1&query=865+East+Baseline+Rd+%231091,+Gilbert,+AZ+85233" target="_blank" rel="noopener noreferrer">
      865 East Baseline Rd #1091, Gilbert, AZ 85233<br>
      <a href="tel:+16027673829">602-767-3829</a> | <a href="mailto:info@provisionbookkeeping.com">contact@provisionbk.com</a>
    </a>
</div>
</footer>

<script>
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    menuToggle.addEventListener('click', () => {{
        navMenu.classList.toggle('active');
    }});
</script>

</body>
</html>
"""

    # Save HTML
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Article HTML generated: {html_file_path}")
    print(f"📁 Image used: {image_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_article.py new_article.txt")
        sys.exit(1)
    else:
        generate_article_from_txt(sys.argv[1])