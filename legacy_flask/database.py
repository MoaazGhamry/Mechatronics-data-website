from flask import Flask
from models import db, Level, Semester, Subject
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mechatronics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def seed_db():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        levels_data = [
            {"id": "000", "title": "Foundation Level", "icon": "Brick"},
            {"id": "100", "title": "Mechanical Fundamentals", "icon": "Gear"},
            {"id": "200", "title": "Electrical & Electronics", "icon": "Bulb"},
            {"id": "300", "title": "Robotics & Control", "icon": "Robot"},
            {"id": "400", "title": "Space & Advanced Systems", "icon": "Rocket"},
        ]

        # Seed Levels
        for l_data in levels_data:
            level = Level(level_id=l_data["id"], title=l_data["title"], icon_name=l_data["icon"])
            db.session.add(level)
            
            # Seed Semesters for each level
            for sem_num in [1, 2]:
                semester = Semester(
                    level_id=l_data["id"],
                    semester_num=sem_num,
                    title=f"Semester {sem_num}"
                )
                db.session.add(semester)
                db.session.flush() # To get semester.id

                # Seed Sample Subjects for each semester
                if l_data["id"] == "000":
                    subjects = [
                        {"name": "Intro to Mechatronics", "code": "MECH001"},
                        {"name": "Mathematics I" if sem_num == 1 else "Mathematics II", "code": f"MATH00{sem_num}"},
                        {"name": "Physics I" if sem_num == 1 else "Physics II", "code": f"PHYS00{sem_num}"}
                    ]
                elif l_data["id"] == "100":
                    subjects = [
                        {"name": "Statics" if sem_num == 1 else "Dynamics", "code": "ENG101"},
                        {"name": "Thermodynamics", "code": "MECH102"},
                        {"name": "Manufacturing Processes", "code": "MECH103"}
                    ]
                elif l_data["id"] == "200":
                    subjects = [
                        {"name": "Circuit Analysis", "code": "ELEC201"},
                        {"name": "Microcontrollers", "code": "ELEC202"},
                        {"name": "Digital Systems", "code": "ELEC203"}
                    ]
                elif l_data["id"] == "300":
                    subjects = [
                        {"name": "Control Systems", "code": "MECH301"},
                        {"name": "Robotics I", "code": "MECH302"},
                        {"name": "Hydraulics & Pneumatics", "code": "MECH303"}
                    ]
                else: # 400
                    subjects = [
                        {"name": "Space Engineering", "code": "AERO401"},
                        {"name": "Autonomous Systems", "code": "MECH402"},
                        {"name": "Graduation Project", "code": "MECH403"}
                    ]

                for s_data in subjects:
                    subject = Subject(
                        semester_id=semester.id,
                        name=s_data["name"],
                        code=s_data["code"],
                        icon_name="Book" # Placeholder icon for subjects
                    )
                    db.session.add(subject)

        db.session.commit()
        print("Database seeded successfully with Level -> Semester -> Subject hierarchy.")

if __name__ == '__main__':
    seed_db()
