import os

file_path = r"F:\New folder (7)\Mechatronics-Data\Mechatronics-Data\templates\hub\resource_detail.html"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_next = False
for i, line in enumerate(lines):
    if skip_next:
        skip_next = False
        continue
    
    if "{% if '.pdf' in resource.download_url|default:''|lower or 'drive.google.com' in" in line:
        # Merge with next line
        next_line = lines[i+1].strip()
        merged_line = line.strip() + " " + next_line + "\n"
        # Preserve indentation
        indent = line[:line.find("{%")]
        new_lines.append(indent + merged_line)
        skip_next = True
    else:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Merged multi-line tag.")
