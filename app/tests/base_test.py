from app import app, db
import unittest

class BasicUtil():
    def __init__(self):
        with app.app_context():
            app.config["TESTING"] = True
            app.config["DEBUG"] = False
            self.app = app.test_client()
            db.drop_all()
            db.create_all()
        
        self.headers = {
            "Content-Type": "application/json"
        }

class BasicTest(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()