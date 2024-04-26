from db import db

# CREATE TABLE Room (
# 		id INT PRIMARY KEY,
# 		building_id INT NOT NULL,
# 		school VARCHAR(50),
# 		name VARCHAR(100) NOT NULL,
# 		open_time TIME NOT NULL,
# 	  close_time TIME NOT NULL,
# 	  deprecated BOOLEAN DEFAULT False NOT NULL,
# 		FOREIGN KEY (building_id) REFERENCES Building(id)
# );


class Room(db.Model):
    __tablename__ = "room"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    building_id = db.Column(db.Integer, nullable=False)
    school = db.Column(db.String(50))
    name = db.Column(db.String(100), nullable=False)
    open_time = db.Column(db.Time, nullable=False)
    close_time = db.Column(db.Time, nullable=False)
    deprecated = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "building_id": self.building_id,
            "school": self.school,
            "name": self.name,
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

    @classmethod
    def find_by_building_id(cls, building_id):
        return cls.query.filter_by(building_id=building_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
