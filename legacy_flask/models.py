from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Level(db.Model):
    __tablename__ = 'levels'
    id = db.Column(db.Integer, primary_key=True)
    level_id = db.Column(db.String(10), unique=True, nullable=False) # e.g., "000"
    title = db.Column(db.String(100), nullable=False)
    icon_name = db.Column(db.String(50), nullable=False)
    semesters = db.relationship('Semester', backref='level', lazy=True)

class Semester(db.Model):
    __tablename__ = 'semesters'
    id = db.Column(db.Integer, primary_key=True)
    level_id = db.Column(db.String(10), db.ForeignKey('levels.level_id'), nullable=False)
    semester_num = db.Column(db.Integer, nullable=False) # 1 or 2
    title = db.Column(db.String(100), nullable=False)
    subjects = db.relationship('Subject', backref='semester', lazy=True)

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), nullable=True)
    icon_name = db.Column(db.String(50), nullable=True)
