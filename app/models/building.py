from db import db

# CREATE TABLE Building (
# 		id INT PRIMARY KEY,
# 		name VARCHAR(50) NOT NULL,
# 		campus VARCHAR(20) NOT NULL,
# 	  open_time TIME NOT NULL,
# 	  close_time TIME NOT NULL,
# 	  deprecated BOOLEAN DEFAULT False NOT NULL
# );


class Building(db.Model):
    __tablename__ = "building"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    campus = db.Column(db.String(20), nullable=False)
    open_time = db.Column(db.Time, nullable=False)
    close_time = db.Column(db.Time, nullable=False)
    deprecated = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "campus": self.campus,
            "open_time": self.open_time.isoformat(),
            "close_time": self.close_time.isoformat(),
            "deprecated": self.deprecated,
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
