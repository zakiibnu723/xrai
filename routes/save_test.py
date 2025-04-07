from flask import Blueprint, request, jsonify
from extensions import db
from models import Patient, Prediction

save_test_blueprint = Blueprint("save_test", __name__)

@save_test_blueprint.route('/save-test', methods=['POST'])
def save_test():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request. No data provided"}), 400

        patient_info = data.get("patientInfo")
        predictions = data.get("predictions")

        if not patient_info or not predictions:
            return jsonify({"error": "Missing patient info or predictions"}), 400

        # Create new Patient instance
        new_patient = Patient(
            first_name=patient_info.get("firstName"),
            age=patient_info.get("age"),
            gender=patient_info.get("gender"),
            blood_type=patient_info.get("bloodType"),
            allergies=patient_info.get("allergies")
        )

        db.session.add(new_patient)
        db.session.commit()  # Save patient info to database

        # Save disease predictions
        for pred in predictions:
            new_prediction = Prediction(
                disease=pred["disease"],
                value=pred["value"],
                patient_id=new_patient.id  # Link prediction to the patient
            )
            db.session.add(new_prediction)

        try:
          db.session.commit()
        except Exception as e:
          db.session.rollback()
          print(f"Error committing to the database: {e}")

        return jsonify({"message": "Data saved successfully!"}), 200

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"error": str(e)}), 500
