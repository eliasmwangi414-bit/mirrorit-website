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
        <li><a href="blog.html">Blog</a></li>
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
          <div class="footer-socials" style="display: flex; gap: 12px; margin-top: 16px;">
            <a href="https://wa.me/254794439669" class="social-btn" target="_blank" aria-label="WhatsApp" rel="noopener noreferrer">
              <svg width="18" height="18" fill="currentColor" viewBox="0 0 448 512"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zM223.9 414.7c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 334.1l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-2.1-3.6 2.1-3.2 7.6-14.1 1.4-2.8 2.8-5.6 1.4-8.4-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
            </a>
            <a href="https://www.instagram.com/mirrorit.ke/" class="social-btn" target="_blank" aria-label="Instagram" rel="noopener noreferrer">
              <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.051.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z"/></svg>
            </a>
          </div>
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
          <div class="footer-socials" style="display: flex; gap: 12px; margin-top: 16px;">
            <a href="https://wa.me/254794439669" class="social-btn" target="_blank" aria-label="WhatsApp" rel="noopener noreferrer">
              <svg width="18" height="18" fill="currentColor" viewBox="0 0 448 512"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zM223.9 414.7c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 334.1l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-2.1-3.6 2.1-3.2 7.6-14.1 1.4-2.8 2.8-5.6 1.4-8.4-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
            </a>
            <a href="https://www.instagram.com/mirrorit.ke/" class="social-btn" target="_blank" aria-label="Instagram" rel="noopener noreferrer">
              <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.051.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z"/></svg>
            </a>
          </div>
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
        nav_html = SUBPAGE_NAV_HTML_TEMPLATE
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
