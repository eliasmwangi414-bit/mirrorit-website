import os
import glob
import re

root_dir = r"C:\Users\kerry\.gemini\antigravity\scratch\abrit-glass-replica"
html_files = glob.glob(os.path.join(root_dir, "*.html"))

# 1. Standard CSS block to inject
STANDARD_NAV_FOOTER_CSS = """
    /* ===== STANDARD NAVBAR CSS ===== */
    #navbar {
      position: sticky; top: 0; left: 0; right: 0; z-index: 1000;
      height: 80px; display: flex; align-items: center;
      padding: 0 2rem;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid rgba(0, 0, 0, 0.08);
      transition: all 0.3s ease;
    }
    #navbar.scrolled {
      background: rgba(255, 255, 255, 0.98);
      box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    }
    .nav-inner { display: flex; align-items: center; justify-content: space-between; width: 100%; max-width: 1400px; margin: 0 auto; }
    .nav-logo { display: flex; align-items: center; gap: 12px; text-decoration: none; }
    .logo-img, .logo-icon { height: 44px; width: 44px; border-radius: 50%; object-fit: contain; flex-shrink: 0; display: block; border: 1px solid rgba(0,0,0,0.08); }
    .logo-text-wrap { display: flex; flex-direction: column; gap: 0px; }
    .logo-text { font-family: 'Cinzel', serif; font-size: 20px; font-weight: 700; color: #000000; letter-spacing: 0.3px; line-height: 1.1; }
    .logo-tagline { font-family: 'Montserrat', sans-serif; font-size: 8px; font-weight: 500; color: #555555; letter-spacing: 1px; text-transform: uppercase; margin-top: 2px; }
    .nav-links { display: flex; align-items: center; gap: 8px; list-style: none; }
    .nav-links a {
      padding: 8px 14px; border-radius: 6px;
      font-size: 14px; font-weight: 500; color: rgba(0, 0, 0, 0.65);
      transition: color 0.2s, background 0.2s;
      text-decoration: none;
    }
    .nav-links a:hover, .nav-links a.active { color: #000000; background: rgba(0, 0, 0, 0.05); }
    .nav-links a.active { border-bottom: 2px solid #000000; border-radius: 6px 6px 0 0; }
    .dropdown { position: relative; }
    .dropdown-menu {
      display: none; position: absolute; top: calc(100% + 8px); left: 0;
      min-width: 220px; padding: 8px;
      background: #ffffff; border: 1px solid rgba(0,0,0,0.12);
      border-radius: 8px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.06);
      z-index: 2000;
    }
    .dropdown-menu::before {
      content: ''; position: absolute; top: -12px; left: 0; right: 0; height: 12px;
    }
    .dropdown:hover .dropdown-menu { display: block; }
    .dropdown-menu a {
      display: block; padding: 8px 12px; border-radius: 4px;
      font-size: 13px; color: rgba(0, 0, 0, 0.65) !important;
      transition: color 0.2s, background 0.2s;
      text-decoration: none;
    }
    .dropdown-menu a::after { display: none !important; }
    .dropdown-menu a:hover {
      background: #000000;
      color: #ffffff !important;
    }
    .nav-cta { padding: 9px 22px !important; background: #000000 !important; color: #ffffff !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 13px !important; }
    .nav-cta:hover { background: #222222 !important; color: #ffffff !important; }

    /* Hamburger & Responsive Nav */
    .nav-hamburger { display: none; background: none; border: none; cursor: pointer; padding: 8px; }
    .nav-hamburger span { display: block; width: 24px; height: 2px; background: #000; margin: 5px 0; transition: all 0.3s ease; }
    @media (max-width: 1024px) {
      .nav-links {
        display: none; position: absolute; top: 80px; left: 0; right: 0;
        background: #ffffff; flex-direction: column; padding: 20px;
        border-bottom: 1px solid rgba(0, 0, 0, 0.08); box-shadow: 0 4px 20px rgba(0,0,0,0.05);
      }
      .nav-links.show, .nav-links.open { display: flex; }
      .nav-hamburger { display: block; }
      .dropdown-menu { position: static; display: none; background: rgba(0,0,0,0.03); border: none; box-shadow: none; padding: 4px 0 4px 15px; margin-top: 5px; min-width: unset; }
      .dropdown.active .dropdown-menu { display: block; }
    }

    /* ===== STANDARD FOOTER CSS ===== */
    footer {
      background: hsl(0 0% 5%);
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      padding: 64px 2rem 32px;
      color: rgba(255, 255, 255, 0.7);
    }
    .footer-inner { max-width: 1400px; margin: 0 auto; }
    .footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 48px; padding-bottom: 48px; border-bottom: 1px solid rgba(255, 255, 255, 0.06); }
    .footer-brand-desc { font-size: 14px; color: rgba(255,255,255,0.7); line-height: 1.75; margin: 16px 0 24px; max-width: 280px; }
    .footer-socials { display: flex; gap: 10px; }
    .social-btn {
      width: 36px; height: 36px; border-radius: 4px;
      background: hsl(0 0% 14%); border: 1px solid rgba(255, 255, 255, 0.06);
      display: flex; align-items: center; justify-content: center;
      color: rgba(255,255,255,0.7); transition: all 0.3s ease; text-decoration: none;
    }
    .social-btn:hover { background: #ffffff; color: #000000; border-color: #ffffff; }
    .footer-col-title { font-family: 'Cinzel', serif; font-weight: 600; font-size: 13px; text-transform: uppercase; letter-spacing: 0.08em; color: #ffffff; margin-bottom: 20px; }
    .footer-links { list-style: none; display: flex; flex-direction: column; gap: 10px; }
    .footer-links li { font-size: 13px; color: rgba(255,255,255,0.7); }
    .footer-links a { font-size: 13px; color: rgba(255,255,255,0.7); transition: color 0.2s; text-decoration: none; }
    .footer-links a:hover { color: #ffffff; }
    .footer-bottom { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; padding-top: 32px; }
    .footer-copy { font-size: 12px; color: rgba(255,255,255,0.5); }
    .footer-copy span { color: #ffffff; }
    @media (max-width: 900px) { .footer-grid { grid-template-columns: 1fr 1fr; } }
    @media (max-width: 600px) { .footer-grid { grid-template-columns: 1fr; } .footer-bottom { flex-direction: column; gap: 16px; text-align: center; } }
"""

# 2. Standard HTML blocks
HOMEPAGE_NAV_HTML = """  <nav id="navbar">
    <div class="nav-inner">
      <a href="#" class="nav-logo">
        <img src="images/logo.png" class="logo-img" alt="MIRRORIT logo" />
        <div class="logo-text-wrap">
          <span class="logo-text">MIRRORIT</span>
          <span class="logo-tagline">You Are Enough</span>
        </div>
      </a>
      <ul class="nav-links" id="navLinks">
        <li><a href="#hero">Home</a></li>
        <li class="dropdown">
          <a href="#products">Products ▾</a>
          <div class="dropdown-menu">
            <a href="wooden-framed.html">Wooden Mirrors</a>
            <a href="thin-framed.html">Thin Framed Mirrors</a>
            <a href="frameless.html">Frameless Mirrors</a>
            <a href="aluminium-framed.html">Aluminium Framed</a>
            <a href="smart-mirrors.html">Smart Mirrors</a>
            <a href="vanity.html">Vanity Mirrors</a>
            <a href="accent.html">Artistic Mirrors</a>
            <a href="wall-mirrors.html">Wall Mirrors</a>
            <a href="furniture.html">Mirror Furniture</a>
          </div>
        </li>
        <li><a href="#services">Services</a></li>
        <li><a href="#process">How We Work</a></li>
        <li><a href="#testimonials">Reviews</a></li>
        <li><a href="blog.html">Blog</a></li>
        <li><a href="#contact" class="nav-cta">Get a Quote</a></li>
      </ul>
      <button class="nav-hamburger" onclick="toggleNav()" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>"""

SUBPAGE_NAV_HTML_TEMPLATE = """  <nav id="navbar">
    <div class="nav-inner">
      <a href="index.html" class="nav-logo">
        <img src="images/logo.png" class="logo-img" alt="MIRRORIT logo" />
        <div class="logo-text-wrap">
          <span class="logo-text">MIRRORIT</span>
          <span class="logo-tagline">You Are Enough</span>
        </div>
      </a>
      <ul class="nav-links" id="navLinks">
        <li><a href="index.html#hero">Home</a></li>
        <li class="dropdown">
          <a href="index.html#products">Products ▾</a>
          <div class="dropdown-menu">
            <a href="wooden-framed.html">Wooden Mirrors</a>
            <a href="thin-framed.html">Thin Framed Mirrors</a>
            <a href="frameless.html">Frameless Mirrors</a>
            <a href="aluminium-framed.html">Aluminium Framed</a>
            <a href="smart-mirrors.html">Smart Mirrors</a>
            <a href="vanity.html">Vanity Mirrors</a>
            <a href="accent.html">Artistic Mirrors</a>
            <a href="wall-mirrors.html">Wall Mirrors</a>
            <a href="furniture.html">Mirror Furniture</a>
          </div>
        </li>
        <li><a href="index.html#services">Services</a></li>
        <li><a href="index.html#process">How We Work</a></li>
        <li><a href="index.html#testimonials">Reviews</a></li>
        <li><a href="blog.html" class="{blog_active}">Blog</a></li>
        <li><a href="index.html#contact" class="nav-cta">Get a Quote</a></li>
      </ul>
      <button class="nav-hamburger" onclick="toggleNav()" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>"""

HOMEPAGE_FOOTER_HTML = """  <footer>
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="#" class="nav-logo" style="margin-bottom: 16px; pointer-events: none;">
            <img src="images/logo.png" class="logo-img" alt="MIRRORIT logo" />
            <div class="logo-text-wrap">
              <span class="logo-text" style="color: #ffffff;">MIRRORIT</span>
              <span class="logo-tagline" style="color: #888888;">You Are Enough</span>
            </div>
          </a>
          <p class="footer-brand-desc">Specialists in premium custom LED, vanity, and decorative mirrors. We focus exclusively on mirrors, with custom mirror furniture available on request.</p>
        </div>
        <div>
          <div class="footer-col-title">Products</div>
          <ul class="footer-links">
            <li><a href="wooden-framed.html">Wooden Mirrors</a></li>
            <li><a href="thin-framed.html">Thin Framed Mirrors</a></li>
            <li><a href="frameless.html">Frameless Mirrors</a></li>
            <li><a href="aluminium-framed.html">Aluminium Framed</a></li>
            <li><a href="smart-mirrors.html">Smart Mirrors</a></li>
            <li><a href="vanity.html">Vanity Mirrors</a></li>
            <li><a href="accent.html">Artistic Mirrors</a></li>
            <li><a href="wall-mirrors.html">Wall Mirrors</a></li>
            <li><a href="furniture.html">Mirror Furniture</a></li>
          </ul>
        </div>
        <div>
          <div class="footer-col-title">Services</div>
          <ul class="footer-links">
            <li><a href="#services">Mirror Fabrication</a></li>
            <li><a href="#services">Professional Fitting</a></li>
            <li><a href="#services">Furniture Crafting</a></li>
            <li><a href="#services">Safe Delivery</a></li>
            <li><a href="blog.html">Design Blog</a></li>
          </ul>
        </div>
        <div>
          <div class="footer-col-title">Contact</div>
          <ul class="footer-links">
            <li><a href="tel:+254794439669">+254 794 439 669</a></li>
            <li><a href="mailto:mirroritco@gmail.com">mirroritco@gmail.com</a></li>
            <li>Next to Getrudes, Nairobi</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <div class="footer-copy">&copy; 2026 <span>MIRRORIT</span>. All rights reserved.</div>
      </div>
    </div>
  </footer>"""

SUBPAGE_FOOTER_HTML = """  <footer>
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="index.html" class="nav-logo" style="margin-bottom: 16px;">
            <img src="images/logo.png" class="logo-img" alt="MIRRORIT logo" />
            <div class="logo-text-wrap">
              <span class="logo-text" style="color: #ffffff;">MIRRORIT</span>
              <span class="logo-tagline" style="color: #888888;">You Are Enough</span>
            </div>
          </a>
          <p class="footer-brand-desc">Specialists in premium custom LED, vanity, and decorative mirrors. We focus exclusively on mirrors, with custom mirror furniture available on request.</p>
        </div>
        <div>
          <div class="footer-col-title">Products</div>
          <ul class="footer-links">
            <li><a href="wooden-framed.html">Wooden Mirrors</a></li>
            <li><a href="thin-framed.html">Thin Framed Mirrors</a></li>
            <li><a href="frameless.html">Frameless Mirrors</a></li>
            <li><a href="aluminium-framed.html">Aluminium Framed</a></li>
            <li><a href="smart-mirrors.html">Smart Mirrors</a></li>
            <li><a href="vanity.html">Vanity Mirrors</a></li>
            <li><a href="accent.html">Artistic Mirrors</a></li>
            <li><a href="wall-mirrors.html">Wall Mirrors</a></li>
            <li><a href="furniture.html">Mirror Furniture</a></li>
          </ul>
        </div>
        <div>
          <div class="footer-col-title">Services</div>
          <ul class="footer-links">
            <li><a href="index.html#services">Mirror Fabrication</a></li>
            <li><a href="index.html#services">Professional Fitting</a></li>
            <li><a href="index.html#services">Furniture Crafting</a></li>
            <li><a href="index.html#services">Safe Delivery</a></li>
            <li><a href="blog.html">Design Blog</a></li>
          </ul>
        </div>
        <div>
          <div class="footer-col-title">Contact</div>
          <ul class="footer-links">
            <li><a href="tel:+254794439669">+254 794 439 669</a></li>
            <li><a href="mailto:mirroritco@gmail.com">mirroritco@gmail.com</a></li>
            <li>Next to Getrudes, Nairobi</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <div class="footer-copy">&copy; 2026 <span>MIRRORIT</span>. All rights reserved.</div>
      </div>
    </div>
  </footer>"""

for filepath in html_files:
    filename = os.path.basename(filepath)
    if filename in ["index-mirrorit-backup.html"]:
        continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Determine nav and footer HTML
    if filename == "index.html":
        nav_html = HOMEPAGE_NAV_HTML
        footer_html = HOMEPAGE_FOOTER_HTML
    else:
        blog_active = "active" if filename == "blog.html" else ""
        nav_html = SUBPAGE_NAV_HTML_TEMPLATE.format(blog_active=blog_active)
        footer_html = SUBPAGE_FOOTER_HTML

    # Replace nav element
    content = re.sub(
        r'<nav id="navbar">.*?</nav>',
        nav_html,
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<nav>.*?</nav>',
        nav_html,
        content,
        flags=re.DOTALL
    )

    # Replace footer element
    content = re.sub(
        r'<footer>.*?</footer>',
        footer_html,
        content,
        flags=re.DOTALL
    )

    # Clean up old nav/footer styles in style tags and insert standard style blocks
    # We will inject standard CSS right before </style> if not already present
    if "/* ===== STANDARD NAVBAR CSS ===== */" not in content:
        # Remove any existing navbar/footer CSS definitions
        # A simple replacement before </style> works great
        content = content.replace("</style>", STANDARD_NAV_FOOTER_CSS + "\n  </style>", 1)

    # Write changes
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Standardized: {filename}")
