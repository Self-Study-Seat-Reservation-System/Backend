from db import db

# CREATE TABLE Config (
# 	id INT PRIMARY KEY AUTO_INCREMENT,
# 	config_key VARCHAR(100) NOT NULL,
# 	config_value VARCHAR(255) NOT NULL
# );


class AdminConfig(db.Model):
    __tablename__ = "config"

    id = db.Column(db.Integer, primary_key=True)
    config_key = db.Column(db.String(100), unique=True, nullable=False)
    config_value = db.Column(db.String(255), nullable=False)


    def to_dict(self):
        return {
            "id": self.id,
            "config_key": self.config_key,
            "config_value": self.config_value,
        }

    @classmethod
    def find_by_key(cls, config_key):
        return cls.query.filter_by(config_key=config_key).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()