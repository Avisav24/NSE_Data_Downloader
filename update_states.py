import re

with open('nse_downloader.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'\.config\(state=tk\.DISABLED\)', '.configure(state="disabled")', content)
content = re.sub(r'\.config\(state=tk\.NORMAL\)', '.configure(state="normal")', content)

with open('nse_downloader.py', 'w', encoding='utf-8') as f:
    f.write(content)
