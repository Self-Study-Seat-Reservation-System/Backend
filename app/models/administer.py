from db import db

# CREATE TABLE Administer (
# 		id INT PRIMARY KEY,
# 		name VARCHAR(50) NOT NULL,
# 		password VARCHAR(255) NOT NULL,
# 		wechat_number VARCHAR(50)
# );


class Administer(db.Model):
    __tablename__ = "administer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    wechat_number = db.Column(db.String(50))

    def to_dict(self):
        return {"id": self.id, "name": self.name, "wechat_number": self.wechat_number}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
