from flask import Blueprint, jsonify, request
from models import Patient
from extensions import db

patients_blueprint = Blueprint('patients', __name__)

# Get all patients
@patients_blueprint.route('/patients', methods=['GET'])
def get_patients():
    try:
        patients = Patient.query.all()
        patient_list = [
            {
                "id": patient.id,
                "first_name": patient.first_name,
                "age": patient.age,
                "blood_type": patient.blood_type,
                "gender": patient.gender
            }
            for patient in patients
        ]
        return jsonify(patient_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a patient by ID
@patients_blueprint.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    try:
        # Log incoming request
        print(f"Attempting to delete patient with ID: {patient_id}")

        # Fetch the patient by ID
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Log patient details
        print(f"Deleting patient: {patient}")

        # Delete the patient
        db.session.delete(patient)
        db.session.commit()

        return jsonify({"message": "Patient deleted successfully"}), 200
    except Exception as e:
        # Log the exact error
        print(f"Error occurred while deleting patient: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
