from flask_sqlalchemy import SQLAlchemy, model
import secrets
db = SQLAlchemy()

class Subscribe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    APIKey = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, default=0)

    @staticmethod
    def generate_apiKey():
        return secrets.token_hex(16)

    def check_apikey(self):
        pass
        
    

