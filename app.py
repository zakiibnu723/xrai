from flask import Flask, make_response
from flask_cors import CORS
from extensions import db
from routes.save_test import save_test_blueprint
from routes.predict import predict_blueprint
from routes.patients import patients_blueprint
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS globally
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

# After request to add headers
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
    return response

# Handle OPTIONS preflight requests globally
@app.route('/api/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    return response

# Initialize the database
db.init_app(app)

# Register Blueprints
app.register_blueprint(save_test_blueprint, url_prefix="/api")
app.register_blueprint(predict_blueprint, url_prefix="/api")
app.register_blueprint(patients_blueprint, url_prefix="/api")

# Only for local development
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
        print("Database and tables created successfully.")
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Running locally
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
