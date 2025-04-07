from extensions import db

# Create a Patient model to store data
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    blood_type = db.Column(db.String(10), nullable=False)
    allergies = db.Column(db.String(255))
    predictions = db.relationship('Prediction', backref='patient', lazy=True, cascade='all, delete-orphan')

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
