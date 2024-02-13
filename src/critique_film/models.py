from .database import db

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # nom = 
    # email = 
    # mot_de_passe_hash = 