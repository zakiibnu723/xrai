from flask import Blueprint, request, jsonify
from extensions import db
from datetime import datetime
from models import XrayTest, Patient

xray_test_blueprint = Blueprint('xray_test', __name__)


# GET: Retrieve all X-ray tests for a specific patient
@xray_test_blueprint.route('/xray-tests/<int:patient_id>', methods=['GET'])
def get_xray_tests(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    xray_tests = XrayTest.query.filter_by(patient_id=patient_id).all()
    return jsonify([{
        "id": test.id,
        # "test_date": test.test_date,
        "result": test.result
    } for test in xray_tests]), 200
