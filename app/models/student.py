from db import db

# CREATE TABLE Student (
# 		id INT PRIMARY KEY,
#       student_id VARCHAR(11) NOT NULL,
# 		name VARCHAR(50) NOT NULL,
# 		password VARCHAR(255) NOT NULL,
# 		wechat_number VARCHAR(50),
# 		school VARCHAR(50),
# 		breach_count INT DEFAULT 0
# );


class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(11), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    wechat_number = db.Column(db.String(50))
    school = db.Column(db.String(50))
    breach_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "name": self.name,
            "wechat_id": self.wechat_number,
            "school": self.school,
            "breach_count": self.breach_count,
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_student_id(cls, student_id):
        return cls.query.filter_by(student_id=student_id).first()
    
    def find_by_breach_count(cls, breach_count):
        return cls.query.filter_by(breach_count>breach_count).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
