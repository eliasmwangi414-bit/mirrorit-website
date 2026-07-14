import glob
import os

root_dir = r"C:\Users\kerry\.gemini\antigravity\scratch\abrit-glass-replica"
html_files = glob.glob(os.path.join(root_dir, "*.html"))

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if "instagram" in content.lower():
        print(f"Found in {os.path.basename(filepath)}")
        # Print matching lines
        for line in content.splitlines():
            if "instagram" in line.lower():
                print("  ", line.strip())
