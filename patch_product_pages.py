"""
Patch all product pages to dynamically load gallery images filtered by mirror type.
Replaces the static hardcoded product-card grid with a JS-driven dynamic grid.
"""
import os
import re

# Mapping: filename -> (mirror type label used in admin dropdown, display name, num)
PAGES = {
    'wooden-framed.html':    ('Wooden Framed Mirror',    'Wooden Framed Mirrors',    20),
    'thin-framed.html':      ('Thin Framed Mirror',      'Thin Framed Mirrors',      20),
    'frameless.html':        ('Frameless Mirror',        'Frameless Mirrors',        20),
    'wall-mirrors.html':     ('Wall Mirror',             'Wall Mirrors',             20),
    'aluminium-framed.html': ('Aluminium Framed Mirror', 'Aluminium Framed Mirrors', 20),
    'smart-mirrors.html':    ('Smart Mirror',            'Smart Mirrors',            20),
    'vanity.html':           ('Vanity Mirror',           'Vanity Mirrors',           20),
    'accent.html':           ('Accent Mirror',           'Accent Mirrors',           20),
    'custom.html':           ('Custom Mirror',           'Custom Mirrors',           20),
}

WA = '254794439669'

DYNAMIC_SCRIPT = '''
    async function loadPageContent() {{
      const MIRROR_TYPE = "{mirror_type}";
      const DISPLAY_NAME = "{display_name}";
      const TOTAL_SLOTS = {total};
      const grid = document.querySelector('.gallery-grid');
      if (!grid) return;

      let gallery = [];
      try {{
        let res;
        try {{ res = await fetch('/api/site-content?t=' + Date.now()); if (!res.ok) throw new Error(); }}
        catch {{ res = await fetch('site-content.json?t=' + Date.now()); }}
        const data = await res.json();
        gallery = (data.gallery || []).filter(img => img.mirrorType === MIRROR_TYPE);

        // Dynamic logo
        if (data.logo) {{
          document.querySelectorAll('.logo-icon').forEach(img => {{
            img.src = data.logo.path;
          }});
        }}
      }} catch(e) {{}}

      // Build cards: uploaded images first, then empty placeholder slots
      let html = '';
      for (let i = 0; i < TOTAL_SLOTS; i++) {{
        const img = gallery[i];
        const num = i + 1;
        const waMsg = encodeURIComponent('Hello MIRROR-IT! I am inquiring about: ' + DISPLAY_NAME + ' #' + num + '.');
        const waUrl = 'https://wa.me/' + '{wa}' + '?text=' + waMsg;

        if (img) {{
          // Real uploaded image
          const src = img.path.startsWith('http') ? img.path : img.path;
          const desc = img.description || ('Premium ' + DISPLAY_NAME.toLowerCase() + ' custom fabricated to your exact specifications. Contact us to order.');
          html += `
            <div class="product-card" onclick="window.open('${{waUrl}}', '_blank')">
              <img src="${{src}}" alt="${{DISPLAY_NAME}} #${{num}}" class="product-card-img" />
              <div class="product-card-overlay"></div>
              <div class="product-card-content">
                <div class="product-name">${{DISPLAY_NAME}} #${{num}}</div>
                <p class="product-desc">${{desc}}</p>
                <a href="${{waUrl}}" class="product-link" target="_blank" rel="noopener noreferrer">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 448 512" style="fill:currentColor; margin-right:6px;"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zM223.9 414.7c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 334.1l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-2.1-3.6 2.1-3.2 7.6-14.1 1.4-2.8 2.8-5.6 1.4-8.4-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
                  Inquire on WhatsApp
                </a>
              </div>
            </div>`;
        }} else {{
          // Empty placeholder slot
          html += `
            <div class="product-card placeholder-card" onclick="window.open('${{waUrl}}', '_blank')">
              <div class="product-card-img placeholder-img">
                <div class="placeholder-inner">
                  <div class="placeholder-icon">🪞</div>
                  <div class="placeholder-text">Coming Soon</div>
                </div>
              </div>
              <div class="product-card-overlay"></div>
              <div class="product-card-content">
                <div class="product-name">${{DISPLAY_NAME}} #${{num}}</div>
                <p class="product-desc">This spot is available. Contact us about your custom order.</p>
                <a href="${{waUrl}}" class="product-link" target="_blank" rel="noopener noreferrer">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 448 512" style="fill:currentColor; margin-right:6px;"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zM223.9 414.7c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 334.1l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-2.1-3.6 2.1-3.2 7.6-14.1 1.4-2.8 2.8-5.6 1.4-8.4-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
                  Inquire on WhatsApp
                </a>
              </div>
            </div>`;
        }}
      }}
      grid.innerHTML = html;
    }}
    document.addEventListener('DOMContentLoaded', loadPageContent);
'''

PLACEHOLDER_CSS = """
    .placeholder-card { cursor: pointer; }
    .placeholder-img {
      width: 100%; aspect-ratio: 1/1;
      background: linear-gradient(135deg, #1a1a1a 0%, #222 50%, #1a1a1a 100%);
      display: flex; align-items: center; justify-content: center;
      border: 2px dashed rgba(255,255,255,0.1);
    }
    .placeholder-inner { text-align: center; opacity: 0.4; }
    .placeholder-icon { font-size: 40px; margin-bottom: 8px; }
    .placeholder-text { font-size: 12px; color: #888; letter-spacing: 1px; text-transform: uppercase; }
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

for filename, (mirror_type, display_name, total) in PAGES.items():
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        print(f'SKIP (not found): {filename}')
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove all static product-card divs from inside gallery-grid
    # Replace everything between <div class="gallery-grid"> and the next </div> that closes it
    # We replace the grid contents with an empty container (JS will fill it)
    content = re.sub(
        r'(<div class="gallery-grid">)(.*?)(</div>\s*\n\s*</section)',
        r'<div class="gallery-grid" id="dynamic-product-grid">\n      <!-- Loaded dynamically by JS -->\n    </div>\n  </section',
        content,
        count=1,
        flags=re.DOTALL
    )

    # 2. Inject placeholder CSS before </style>
    if '.placeholder-card' not in content:
        content = content.replace('</style>', PLACEHOLDER_CSS + '\n  </style>', 1)

    # 3. Replace old static script block with dynamic loader
    script_body = DYNAMIC_SCRIPT.format(
        mirror_type=mirror_type,
        display_name=display_name,
        total=total,
        wa=WA
    )

    # Replace the existing script block content
    old_script_pattern = r'<script>\s*function toggleNav\(\).*?</script>'
    new_script = f'''<script>
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
{script_body}
  </script>'''

    content = re.sub(old_script_pattern, new_script, content, count=1, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'OK Patched: {filename}')

print('\nAll product pages patched!')
