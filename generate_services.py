import os
import urllib.parse

services = [
    (
        "custom-fabrication.html", 
        "Custom Mirror Fabrication",
        "We cut, shape, and edge-polish mirrors to your exact specifications in our dedicated factory.",
        [
            ("Precision Cutting", "Our CNC machinery ensures every curve and corner is cut to perfection, allowing us to create unique geometric and organic shapes."),
            ("Premium Silvering", "We use high-grade 5mm and 6mm copper-free silver glass that guarantees crystal clear reflections without distortion over time."),
            ("Custom LED Integration", "We seamlessly integrate customized LED lighting solutions, sandblasting patterns perfectly to match your design intent.")
        ]
    ),
    (
        "professional-installation.html", 
        "Professional Installation",
        "Expert fitting and mounting by our trained technicians for a flawless, secure finish.",
        [
            ("Site Survey & Measurement", "We conduct precise on-site measurements to ensure your custom mirror fits perfectly into the designated space, taking into account wall plumbness and structural supports."),
            ("Secure Mounting Systems", "Depending on the mirror size and wall type, we use hidden heavy-duty brackets, specialized adhesives, or custom standoffs for ultimate safety."),
            ("Electrical Connection", "For backlit and front-lit mirrors, our technicians safely connect the integrated LEDs to your existing electrical provisions.")
        ]
    ),
    (
        "design-consultation.html", 
        "Design Consultation",
        "Collaborate with our design workshop to build custom mirror furniture or bespoke accents tailored to your rooms.",
        [
            ("Aesthetic Planning", "We help you select the right mirror style, size, and lighting color temperature to complement your room's existing decor and lighting."),
            ("Technical Recommendations", "Our team advises on anti-fog integration, touch sensors, edge finishes, and the optimal glass thickness for your specific application."),
            ("3D Visualization", "For large commercial projects or complex residential installations, we can provide shop drawings and visual references before fabrication begins.")
        ]
    ),
    (
        "delivery-logistics.html", 
        "Delivery & Logistics",
        "Safe, insured transport of fragile glass products directly to your doorstep or project site.",
        [
            ("Specialized Packaging", "Every mirror is meticulously wrapped in protective foam, edge guards, and custom wooden crating to prevent any damage during transit."),
            ("Dedicated Fleet", "We use our own specialized glass-transport vehicles equipped with secure A-frames to ensure a smooth journey to your location."),
            ("Nationwide Shipping", "While based in Nairobi, we coordinate safe logistics and delivery for large custom orders across all 47 counties in Kenya.")
        ]
    )
]

template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | MIRROR-IT</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Montserrat:wght@400;500;600&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet" />
  <style>
    /* Add basic styles */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'DM Sans', sans-serif;
      background: #ffffff;
      color: #000000;
      overflow-x: hidden;
      line-height: 1.6;
    }}
    :root {{
      --bg-primary:   #ffffff;
      --bg-secondary: #f9fafb;
      --border:       rgba(0, 0, 0, 0.12);
      --glass-bg:     rgba(255, 255, 255, 0.85);
      --glass-border: rgba(0, 0, 0, 0.06);
      --text-primary: #000000;
      --text-secondary: #111111;
      --text-muted:   #9ca3af;
      --accent:       #000000;
      --accent-mid:   #111111;
      --accent-bright: #000000;
      --accent-light: #f3f4f6;
      --accent-dark:  #000000;
      --divider:      rgba(0, 0, 0, 0.06);
      --transition:   all 0.3s ease;
    }}
    a {{ text-decoration: none; }}
    
    /* Navbar styles */
    #navbar {{
      position: fixed;
      top: 0; left: 0; right: 0;
      z-index: 1000;
      padding: 0 5%;
      height: 72px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border);
    }}
    .nav-logo {{ display: flex; align-items: center; gap: 10px; }}
    .logo-icon {{ height: 40px; width: 40px; border-radius: 50%; object-fit: contain; flex-shrink: 0; display: block; }}
    .logo-text-wrap {{ display: flex; flex-direction: column; gap: 0px; }}
    .logo-text {{ font-family: 'Cinzel', serif; font-weight: 700; font-size: 20px; color: var(--text-primary); letter-spacing: 0.5px; text-transform: uppercase; line-height: 1.1; }}
    .logo-tagline {{ font-family: 'Montserrat', sans-serif; font-size: 8px; font-weight: 500; color: var(--text-muted); letter-spacing: 1px; text-transform: uppercase; margin-top: 2px; }}
    .nav-links {{ display: flex; align-items: center; gap: 36px; list-style: none; }}
    .nav-links a {{ color: var(--text-secondary); font-size: 14px; font-weight: 500; position: relative; }}
    .nav-links a:hover {{ color: var(--text-primary); }}
    .dropdown {{ position: relative; }}
    .dropdown-content {{
      display: none;
      position: absolute;
      top: 100%;
      left: 0;
      background: var(--bg-primary);
      min-width: 220px;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 8px 0;
      z-index: 2000;
      box-shadow: 0 16px 48px rgba(0,0,0,0.06);
    }}
    .dropdown:hover .dropdown-content {{ display: block; }}
    .dropdown-content a {{
      display: block;
      padding: 10px 20px;
      color: var(--text-secondary) !important;
      font-size: 14px;
      text-decoration: none;
    }}
    .dropdown-content a::after {{ display: none !important; }}
    .dropdown-content a:hover {{
      background: var(--accent-light);
      color: var(--accent) !important;
    }}
    .nav-cta {{ padding: 9px 22px; background: var(--accent); color: var(--text-primary) !important; border-radius: 4px; font-weight: 600 !important; font-size: 13px !important; }}

    /* ===== MOBILE NAV ===== */
    .nav-hamburger {{
      display: none;
      flex-direction: column;
      gap: 5px;
      cursor: pointer;
      padding: 4px;
    }}
    .nav-hamburger span {{
      display: block; width: 24px; height: 2px;
      background: var(--text-primary);
      border-radius: 2px;
      transition: var(--transition);
    }}
    @media (max-width: 768px) {{
      .nav-links {{ display: none; }}
      .nav-hamburger {{ display: flex; }}
      .nav-links.open {{
        display: flex;
        flex-direction: column;
        position: fixed;
        top: 72px; left: 0; right: 0;
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(20px);
        padding: 24px;
        border-bottom: 1px solid var(--border);
        gap: 20px;
        z-index: 999;
        max-height: calc(100vh - 72px);
        overflow-y: auto;
      }}
      .dropdown-content {{
        position: static;
        display: none;
        background: rgba(0,0,0,0.03);
        border: none;
        box-shadow: none;
        padding: 4px 0 4px 15px;
        margin-top: 5px;
        min-width: unset;
      }}
      .dropdown.active .dropdown-content {{
        display: block;
      }}
    }}

    /* WhatsApp Float */
    .whatsapp-float {{
      position: fixed;
      bottom: 30px;
      right: 30px;
      z-index: 1000;
      transition: transform 0.3s ease;
      text-decoration: none;
    }}
    .whatsapp-float:hover {{
      transform: scale(1.1);
    }}
    .whatsapp-float svg {{
      width: 56px;
      height: 56px;
      fill: #ffffff;
      filter: drop-shadow(0px 4px 10px rgba(0,0,0,0.5));
    }}

    /* Service Hero styles */
    .service-hero {{
      padding: 140px 5% 80px;
      background: #ffffff;
      text-align: center;
    }}
    .service-hero-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 48px;
      font-weight: 800;
      color: var(--text-primary);
      margin-bottom: 16px;
    }}
    .service-hero-desc {{
      font-size: 16px;
      color: var(--text-secondary);
      max-width: 600px;
      margin: 0 auto;
    }}

    /* Details layout */
    .details-container {{
      padding: 80px 5%;
      display: flex;
      flex-direction: column;
      gap: 80px;
    }}
    .detail-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 60px;
      align-items: center;
    }}
    .detail-row:nth-child(even) {{
      direction: rtl;
    }}
    .detail-row:nth-child(even) .detail-content {{
      direction: ltr;
    }}
    .detail-img-wrapper {{
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid var(--border);
      aspect-ratio: 4/3;
    }}
    .detail-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}
    .detail-content {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .detail-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 32px;
      font-weight: 700;
      color: var(--text-primary);
    }}
    .detail-desc {{
      font-size: 15px;
      color: var(--text-secondary);
      line-height: 1.8;
    }}
    .inquire-btn {{
      align-self: flex-start;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 12px 24px;
      background: var(--accent);
      color: var(--text-primary);
      font-family: 'DM Sans', sans-serif;
      font-weight: 700;
      font-size: 14px;
      border-radius: 4px;
      transition: var(--transition);
      border: 2px solid var(--accent);
    }}
    .inquire-btn:hover {{
      background: transparent;
      color: var(--accent);
    }}
    @media (max-width: 900px) {{
      .detail-row {{ grid-template-columns: 1fr; gap: 32px; }}
      .detail-row:nth-child(even) {{ direction: ltr; }}
    }}

    /* Footer styles */
    footer {{ padding: 64px 2rem 32px; background: hsl(0 0% 5%); border-top: 1px solid var(--border); }}
    .footer-grid {{ display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 48px; padding-bottom: 48px; border-bottom: 1px solid rgba(255,255,255,0.06); }}
    .footer-brand p {{ color: rgba(255,255,255,0.7); font-size: 14px; margin: 16px 0 24px; max-width: 280px; line-height: 1.75; }}
    .footer-socials {{ display: flex; gap: 10px; }}
    .social-btn {{ width: 36px; height: 36px; border-radius: calc(var(--radius) - 4px); background: hsl(0 0% 14%); border: 1px solid rgba(255,255,255,0.06); display: flex; align-items: center; justify-content: center; color: rgba(255,255,255,0.7); transition: var(--transition); text-decoration: none; }}
    .social-btn:hover {{ background: #ffffff; color: #000000; border-color: #ffffff; }}
    .footer-col-title {{ font-family: 'Cinzel', serif; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #ffffff; margin-bottom: 20px; }}
    .footer-links {{ list-style: none; display: flex; flex-direction: column; gap: 10px; }}
    .footer-links li {{ font-size: 13px; color: rgba(255,255,255,0.7); }}
    .footer-links a {{ color: rgba(255,255,255,0.7); font-size: 13px; transition: var(--transition); text-decoration: none; }}
    .footer-links a:hover {{ color: #ffffff; }}
    .footer-bottom {{ display: flex; justify-content: space-between; align-items: center; padding-top: 32px; }}
    .footer-copy {{ color: rgba(255,255,255,0.5); font-size: 12px; }}
    .footer-copy span {{ color: #ffffff; }}
    .footer-bottom-links {{ display: flex; gap: 24px; }}
    .footer-bottom-links a {{ color: var(--text-muted); font-size: 13px; text-decoration: none; transition: var(--transition); }}
    .footer-bottom-links a:hover {{ color: var(--accent-bright); }}
    @media (max-width: 900px) {{ .footer-grid {{ grid-template-columns: 1fr 1fr; }} }}
    @media (max-width: 600px) {{ .footer-grid {{ grid-template-columns: 1fr; }} .footer-bottom {{ flex-direction: column; gap: 16px; text-align: center; }} }}
  </style>
</head>
<body>
  <nav id="navbar">
    <a href="index.html" class="nav-logo">
      <img src="images/logo.png" class="logo-icon" alt="MIRRORIT logo" />
      <div class="logo-text-wrap">
        <div class="logo-text">MIRRORIT</div>
        <div class="logo-tagline">You Are Enough</div>
      </div>
    </a>
    <ul class="nav-links" id="navLinks">
      <li><a href="index.html#hero">Home</a></li>
      <li class="dropdown">
        <a href="index.html#products">Products</a>
        <div class="dropdown-content">
          <a href="wooden-framed.html">Wooden Framed Mirrors</a>
          <a href="thin-framed.html">Thin Framed Mirrors</a>
          <a href="frameless.html">Frameless Mirrors</a>
          <a href="wall-mirrors.html">Wall Mirrors</a>
          <a href="aluminium-framed.html">Aluminium Framed Mirrors</a>
          <a href="smart-mirrors.html">Smart Mirrors</a>
          <a href="vanity.html">Vanity Mirrors</a>
          <a href="accent.html">Accent Mirrors</a>
          <a href="custom.html">Custom Mirrors</a>
        </div>
      </li>
      <li class="dropdown">
        <a href="index.html#services">Services</a>
        <div class="dropdown-content">
          <a href="custom-fabrication.html">Custom Mirror Fabrication</a>
          <a href="professional-installation.html">Professional Fitting</a>
          <a href="design-consultation.html">Furniture Crafting</a>
          <a href="delivery-logistics.html">Safe Delivery</a>
        </div>
      </li>
      <li><a href="index.html#why-us">About</a></li>
      <li><a href="index.html#contact">Contact</a></li>
      <li><a href="tel:+254794439669" class="nav-cta">Call Us</a></li>
    </ul>
    <div class="nav-hamburger" id="hamburger" onclick="toggleNav()">
      <span></span><span></span><span></span>
    </div>
  </nav>

  <section class="service-hero">
    <h1 class="service-hero-title">{title}</h1>
    <p class="service-hero-desc">{subtitle}</p>
  </section>

  <div class="details-container">
    {details}
  </div>

  <footer>
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="index.html" class="nav-logo" style="display:inline-flex;">
          <img src="images/logo.png" class="logo-icon" alt="MIRROR-IT diamond logo" />
          <div class="logo-text-wrap">
            <div class="logo-text" style="color: #ffffff;">MIRRORIT</div>
            <div class="logo-tagline" style="color: rgba(255,255,255,0.45);">You Are Enough</div>
          </div>
        </a>
        <p>Specialists in premium custom LED, vanity, and decorative mirrors, plus custom mirrored furniture on request. Based in Nairobi, Kenya.</p>
        <div class="footer-socials">
          <a href="https://www.facebook.com/profile.php?id=61565452296495" class="social-btn" id="facebook-btn" title="Facebook" target="_blank" rel="noopener noreferrer">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 320 512" fill="currentColor"><path d="M279.14 288l14.22-92.66h-88.91v-60.13c0-25.35 12.42-50.06 52.24-50.06h40.42V6.26S260.43 0 225.36 0c-73.22 0-121.08 44.38-121.08 124.72v70.62H22.89V288h81.39v224h100.17V288z"/></svg>
          </a>
          <a href="https://www.instagram.com/mirrorit.ke/" class="social-btn" id="instagram-btn" title="Instagram" target="_blank" rel="noopener noreferrer">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 448 512" fill="currentColor"><path d="M224.1 141c-63.6 0-114.9 51.3-114.9 114.9s51.3 114.9 114.9 114.9S339 319.5 339 255.9 287.7 141 224.1 141zm0 189.6c-41.1 0-74.7-33.5-74.7-74.7s33.5-74.7 74.7-74.7 74.7 33.5 74.7 74.7-33.6 74.7-74.7 74.7zm146.4-194.3c0 14.9-12 26.8-26.8 26.8-14.9 0-26.8-12-26.8-26.8s12-26.8 26.8-26.8 26.8 12 26.8 26.8zm76.1 27.2c-1.7-35.9-9.9-67.7-36.2-93.9-26.2-26.2-58-34.4-93.9-36.2-37-2.1-147.9-2.1-184.9 0-35.8 1.7-67.6 9.9-93.9 36.1s-34.4 58-36.2 93.9c-2.1 37-2.1 147.9 0 184.9 1.7 35.9 9.9 67.7 36.2 93.9s58 34.4 93.9 36.2c37 2.1 147.9 2.1 184.9 0 35.9-1.7 67.7-9.9 93.9-36.2 26.2-26.2 34.4-58 36.2-93.9 2.1-37 2.1-147.8 0-184.8zM398.8 388c-7.8 19.6-22.9 34.7-42.6 42.6-29.5 11.7-99.5 9-132.1 9s-102.7 2.6-132.1-9c-19.6-7.8-34.7-22.9-42.6-42.6-11.7-29.5-9-99.5-9-132.1s-2.6-102.7 9-132.1c7.8-19.6 22.9-34.7 42.6-42.6 29.5-11.7 99.5-9 132.1-9s102.7-2.6 132.1 9c19.6 7.8 34.7 22.9 42.6 42.6 11.7 29.5 9 99.5 9 132.1s2.7 102.7-9 132.1z"/></svg>
          </a>
          <a href="https://wa.me/254794439669" class="social-btn" id="whatsapp-social-btn" title="WhatsApp" target="_blank" rel="noopener noreferrer">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 448 512" fill="currentColor"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zM223.9 414.7c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 334.1l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-2.1-3.6 2.1-3.2 7.6-14.1 1.4-2.8 2.8-5.6 1.4-8.4-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
          </a>
        </div>
      </div>
      <div>
        <div class="footer-col-title">Our Mirrors</div>
        <ul class="footer-links">
          <li><a href="wooden-framed.html">Wooden Framed Mirrors</a></li>
          <li><a href="thin-framed.html">Thin Framed Mirrors</a></li>
          <li><a href="frameless.html">Frameless Mirrors</a></li>
          <li><a href="wall-mirrors.html">Wall Mirrors</a></li>
          <li><a href="aluminium-framed.html">Aluminium Framed Mirrors</a></li>
          <li><a href="smart-mirrors.html">Smart Mirrors</a></li>
          <li><a href="vanity.html">Vanity Mirrors</a></li>
          <li><a href="accent.html">Accent Mirrors</a></li>
          <li><a href="custom.html">Custom Mirrors</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-col-title">Services</div>
        <ul class="footer-links">
          <li><a href="custom-fabrication.html">Mirror Fabrication</a></li>
          <li><a href="professional-installation.html">Professional Fitting</a></li>
          <li><a href="design-consultation.html">Furniture Crafting</a></li>
          <li><a href="delivery-logistics.html">Safe Delivery</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-col-title">Contact</div>
        <ul class="footer-links">
          <li><a href="tel:+254794439669">+254 794 439 669</a></li>
          <li><a href="https://www.instagram.com/mirrorit.ke/" target="_blank">@mirrorit.ke on Instagram</a></li>
          <li><a href="#">Manyanja Rd, Nairobi</a></li>
          <li><a href="#">Opp. Gertrude's Children Hospital</a></li>
          <li><a href="#">Mon to Sat: 8am to 6pm</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="footer-copy">© 2025 <span>MIRRORIT Ltd</span>. All rights reserved. &nbsp;&middot;&nbsp; Premium Mirror Solutions in Africa</p>
      <div class="footer-bottom-links">
      </div>
    </div>
  </footer>

  <a href="https://wa.me/254794439669" class="whatsapp-float" target="_blank" rel="noopener noreferrer" aria-label="Chat on WhatsApp">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zM223.9 414.7c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 334.1l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-2.1-3.6 2.1-3.2 7.6-14.1 1.4-2.8 2.8-5.6 1.4-8.4-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
  </a>

  <script>
    function toggleNav() {{
      document.getElementById('navLinks').classList.toggle('open');
    }}
    document.querySelectorAll('.dropdown > a').forEach(trigger => {{
      trigger.addEventListener('click', function(e) {{
        if (window.innerWidth <= 768) {{
          e.preventDefault();
          const parent = this.parentElement;
          parent.classList.toggle('active');
          document.querySelectorAll('.dropdown').forEach(d => {{
            if (d !== parent) d.classList.remove('active');
          }});
        }}
      }});
    }});

    async function loadDynamicLogo() {{
      try {{
        const t = Date.now();
        let res;
        try {{ res = await fetch('/api/site-content?t=' + t); if (!res.ok) throw new Error(); }}
        catch {{ res = await fetch('site-content.json?t=' + t); }}
        const data = await res.json();
        
        // Logo
        if (data.logo) {{
          document.querySelectorAll('.logo-icon').forEach(img => {{
            img.src = data.logo.path;
          }});
        }}
        
        // Service detail images
        if (data.serviceDetails) {{
          Object.entries(data.serviceDetails).forEach(([key, val]) => {{
            if (val && val.path) {{
              const imgEl = document.getElementById('detail-img-' + key);
              if (imgEl) imgEl.src = val.path;
            }}
          }});
        }}
      }} catch(e) {{}}
    }}
    document.addEventListener("DOMContentLoaded", loadDynamicLogo);
  </script>
</body>
</html>
"""

for filename, title, subtitle, sections in services:
    details_html = ""
    for idx, (sec_title, sec_desc) in enumerate(sections):
        wa_message = f"Hello MIRROR-IT! I am inquiring about {title} - {sec_title}."
        wa_url = f"https://wa.me/254794439669?text={urllib.parse.quote(wa_message)}"
        
        img_text = urllib.parse.quote(f"{title}\n{sec_title}")
        
        # Determine the key name for this service detail section
        key_name = f"{filename.replace('.html','')}-{idx}"
        
        details_html += f'''
    <div class="detail-row">
      <div class="detail-img-wrapper">
        <img src="https://placehold.co/800x600?text={img_text}" id="detail-img-{key_name}" alt="{sec_title}" class="detail-img" />
      </div>
      <div class="detail-content">
        <h2 class="detail-title">{sec_title}</h2>
        <p class="detail-desc">{sec_desc}</p>
        <a href="{wa_url}" class="inquire-btn" target="_blank" rel="noopener noreferrer">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 448 512" style="fill:currentColor;"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zM223.9 414.7c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 334.1l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-2.1-3.6 2.1-3.2 7.6-14.1 1.4-2.8 2.8-5.6 1.4-8.4-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
          Inquire about this
        </a>
      </div>
    </div>
'''
    
    html_content = template.format(title=title, subtitle=subtitle, details=details_html)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

print("Services pages generated successfully.")
