from flask import Flask, render_template, jsonify, abort
from flask_cors import CORS
import pandas as pd
import os
import re

app = Flask(__name__)
CORS(app)

EXCEL_FILE = 'subjects.xlsx'

LEVELS_INFO = [
    {"level_id": "000", "title": "Foundation Level", "icon_name": "Brick"},
    {"level_id": "100", "title": "Mechanical Fundamentals", "icon_name": "Gear"},
    {"level_id": "200", "title": "Electrical & Electronics", "icon_name": "Bulb"},
    {"level_id": "300", "title": "Robotics & Control", "icon_name": "Robot"},
    {"level_id": "400", "title": "Space & Advanced Systems", "icon_name": "Rocket"},
]

def get_visual_data(filter_level=None):
    if not os.path.exists(EXCEL_FILE):
        return {}
    
    df = pd.read_excel(EXCEL_FILE, header=None)
    data = {}
    current_level = None
    sem1_col = None
    sem2_col = None
    res_types = ["Explanation", "Lectures", "Sheets", "Midterm", "Final", "Revision"]
    
    for i, row in df.iterrows():
        row_list = row.tolist()
        for j, cell in enumerate(row_list):
            cell_str = str(cell).lower()
            if "level" in cell_str:
                match = re.search(r'(\d+)', cell_str)
                if match:
                    current_level = match.group(1).zfill(3)
                    sem1_col = None
                    sem2_col = None
                    if current_level not in data:
                        data[current_level] = {1: [], 2: []}
        
        if current_level:
            if filter_level and current_level != filter_level:
                continue
                
            for j, cell in enumerate(row_list):
                cell_str = str(cell).lower()
                if "semester" in cell_str:
                    if "(1)" in cell_str:
                        sem1_col = j
                    elif "(2)" in cell_str:
                        sem2_col = j
            
            if sem1_col is not None:
                subj_name = str(row_list[sem1_col]) if len(row_list) > sem1_col else ""
                if subj_name and subj_name.lower() != 'nan' and "semester" not in subj_name.lower() and "level" not in subj_name.lower():
                    resources = {res_type: (str(row_list[sem1_col + 1 + k]) if len(row_list) > (sem1_col + 1 + k) else "") 
                                 for k, res_type in enumerate(res_types)}
                    data[current_level][1].append({"name": subj_name, "resources": resources})
            
            if sem2_col is not None:
                subj_name = str(row_list[sem2_col]) if len(row_list) > sem2_col else ""
                if subj_name and subj_name.lower() != 'nan' and "semester" not in subj_name.lower() and "level" not in subj_name.lower():
                    resources = {res_type: (str(row_list[sem2_col + 1 + k]) if len(row_list) > (sem2_col + 1 + k) else "") 
                                 for k, res_type in enumerate(res_types)}
                    data[current_level][2].append({"name": subj_name, "resources": resources})

    return data

@app.route('/')
def index():
    return render_template('index.html', levels=LEVELS_INFO)

@app.route('/level/<level_id>')
def level_detail(level_id):
    # Validate level_id
    level = next((l for l in LEVELS_INFO if l['level_id'] == level_id), None)
    if not level:
        abort(404)
        
    data = get_visual_data(filter_level=level_id)
    subjects = data.get(level_id, {1: [], 2: []})
    
    return render_template('level_detail.html', 
                           level=level, 
                           subjects_s1=subjects[1], 
                           subjects_s2=subjects[2])

# API remains for compatibility if needed elsewhere
@app.route('/api/levels')
def api_levels():
    return jsonify(LEVELS_INFO)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
