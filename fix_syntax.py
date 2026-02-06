import os

file_path = r"f:/New folder (7)/Mechatronics-Data/Mechatronics-Data/templates/hub/resource_detail.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the specific error pattern
# Using a robust replacement that handles potential variations if possible, but specific is best
if "category=='Sheets'" in content:
    new_content = content.replace("category=='Sheets'", "category == 'Sheets'")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed category=='Sheets'")
else:
    print("Pattern category=='Sheets' not found (maybe already fixed?)")
