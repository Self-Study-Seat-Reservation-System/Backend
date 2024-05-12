from db import db

# CREATE TABLE Reservation (
# 		id INT PRIMARY KEY,
# 		user_id INT,
# 		room_id INT,
# 		seat_id INT,
# 		create_time DATETIME NOT NULL,
# 		start_time DATETIME NOT NULL,
# 		end_time DATETIME NOT NULL,
# 		status ENUM('waiting', 'checked', 'timeout', 'canceled') DEFAULT 'waiting' NOT NULL,
# 		FOREIGN KEY (user_id) REFERENCES Student(id),
# 		FOREIGN KEY (room_id) REFERENCES Room(id),
# 		FOREIGN KEY (seat_id) REFERENCES Seat(id)
# );

status_mapping = {0: "waiting", 1: "checked", 2: "timeout", 3: "canceled"}


class Reservation(db.Model):
    __tablename__ = "reservation"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    room_id = db.Column(db.Integer, nullable=False)
    seat_id = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, default=0, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "room_id": self.room_id,
            "seat_id": self.seat_id,
            "create_time": self.create_time.isoformat(),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "status": self.status,
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_room_id(cls, room_id):
        return cls.query.filter_by(room_id=room_id).all()

    @classmethod
    def find_by_seat_id(cls, seat_id):
        return cls.query.filter_by(seat_id=seat_id).all()
    
    @classmethod
    def find(cls, **args):
        query = cls.query
        for key, value in args.items():
            if value is None:
                continue
            query = query.filter(getattr(cls, key) == value)
        query = query.order_by(cls.start_time)
        return query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
