from flask import Blueprint, jsonify, request
import requests
import io

predict_bp = Blueprint("predict", __name__)


@predict_bp.post("/disease")
def predict_disease():
    # Ensure the file is provided
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    # Access the uploaded file
    image_file = request.files["file"]

    # Prepare the file for forwarding
    file_data = {
        "file": (image_file.filename, io.BytesIO(image_file.read()), image_file.mimetype)
    }

    # URL of the prediction service
    url = "http://127.0.0.1:8080/predict"

    try:
        # Forward the file to the prediction service
        response = requests.post(url, files=file_data)

        # Return the response from the prediction service
        return jsonify({"Response Text": response.text}), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
