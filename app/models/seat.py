from db import db

# CREATE TABLE Seat (
# 		id INT PRIMARY KEY,
# 		room_id INT NOT NULL,
# 		near_fixed_socket BOOLEAN,
# 		near_movable_socket BOOLEAN,
# 		near_window BOOLEAN,
# 		deprecated BOOLEAN DEFAULT False NOT NULL,
# 		FOREIGN KEY (room_id) REFERENCES Room(id)
# );


class Seat(db.Model):
    __tablename__ = "seat"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, nullable=False)
    near_fixed_socket = db.Column(db.Boolean)
    near_movable_socket = db.Column(db.Boolean)
    near_window = db.Column(db.Boolean)
    deprecated = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "near_fixed_socket": self.near_fixed_socket,
            "near_movable_socket": self.near_movable_socket,
            "near_window": self.near_window,
            "deprecated": self.deprecated,
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_room_id(cls, room_id):
        return cls.query.filter_by(room_id=room_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
