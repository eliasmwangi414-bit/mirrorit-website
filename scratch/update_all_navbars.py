import os
import glob
import re

root_dir = r"C:\Users\kerry\.gemini\antigravity\scratch\abrit-glass-replica"
html_files = glob.glob(os.path.join(root_dir, "*.html"))

for filepath in html_files:
    filename = os.path.basename(filepath)
    if filename in ["index.html", "blog.html"]:
        continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    
    # 1. Replace any existing #blog or index.html#blog links in nav or footer
    content = re.sub(r'<a href="index\.html#blog">Blog</a>', r'<a href="blog.html">Blog</a>', content)
    content = re.sub(r'<a href="#blog">Blog</a>', r'<a href="blog.html">Blog</a>', content)
    content = re.sub(r'<a href="index\.html#blog">Design Blog</a>', r'<a href="blog.html">Design Blog</a>', content)
    content = re.sub(r'<a href="#blog">Design Blog</a>', r'<a href="blog.html">Design Blog</a>', content)
    
    # 2. If nav-links doesn't have blog.html, insert it right before Get a Quote
    if 'href="blog.html">Blog</a>' not in content:
        # Check if Get a Quote is there
        pattern = r'(<li><a href="[^"]*#contact" class="nav-cta">Get a Quote</a></li>)'
        replacement = r'<li><a href="blog.html">Blog</a></li>\n        \1'
        content = re.sub(pattern, replacement, content)
        
    # 3. If footer doesn't have Design Blog, insert it under Quick Links or Services
    if 'href="blog.html">Design Blog</a>' not in content:
        # Let's see if there's Safe Delivery in footer
        pattern_footer = r'(<li><a href="[^"]*#services">Safe Delivery</a></li>)'
        replacement_footer = r'\1\n            <li><a href="blog.html">Design Blog</a></li>'
        content = re.sub(pattern_footer, replacement_footer, content)
        
    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filename}")
    else:
        print(f"No changes needed for {filename}")
