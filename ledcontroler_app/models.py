from ledcontroler_app import db

class Triggers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description