from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
import requests
import io

from models import Disease, History, Product

predict_bp = Blueprint("predict", __name__)


@predict_bp.post("/disease")
@jwt_required()
def predict_disease():
    # Ensure the file is provided
    if "file" not in request.files:
        return jsonify({"Response Text": "Invalid file format"}), 400

    # Access the uploaded file
    image_file = request.files["file"]

    # Read the file content into a variable
    file_content = image_file.read()

    # Prepare the file for forwarding (prediction service)
    file_data = {
        "file": (
            image_file.filename,
            io.BytesIO(file_content),  # Create a fresh stream for forwarding
            image_file.mimetype,
        )
    }

    # Reset the original stream for further operations
    image_file.stream.seek(0)

    # URL of the prediction service
    url = "http://127.0.0.1:8080/predict"

    try:
        # Forward the file to the prediction service
        response = requests.post(url, files=file_data)

        # Parse the response text from the prediction service
        response_data = response.json()

        if "error" in response_data:
            return (
                jsonify({"Response Text": response_data["error"]}),
                response.status_code,
            )

        # If prediction response contains confidence and predicted class
        if "confidence" in response_data and "predicted_class" in response_data:
            # Convert to percentage
            confidence_percentage = round(response_data["confidence"] * 100, 2)
            predicted_class = response_data["predicted_class"]
            print(predicted_class)
            # Get disease details from the mapping
            disease = Disease.get_disease_from_name(disease_name=predicted_class)

            if not disease:
                return jsonify({"Response Text": "Unknown disease"}), 500

            # Get related products
            product_list = Product.get_product_from_diseaseid(disease_id=disease.id)

            product_data = [
                {
                    "product_name": product.product_name,
                    "product_image": product.product_image,
                    "product_link": product.product_link,
                    "active_ingredient": product.active_ingredient,
                }
                for product in product_list
            ]

            # Save the image to Google Cloud Storage
            image_url = History.save_image(image_file)

            # TODO: save prediction into History
            history = History(
                percentage=confidence_percentage,
                user_id=get_jwt_identity(),
                disease_id=disease.id,
                images=image_url,
            )

            try:
                history.save()
            except Exception as e:
                return jsonify({"error": f"fail to save history : {e}"}), 500

            return (
                jsonify(
                    {
                        "nama_penyakit": disease.disease_name,
                        "deskripsi": disease.description,
                        "confidence": f"{confidence_percentage}%",
                        "solusi": disease.solution,
                        "rekomendasi_product": product_data,
                    }
                ),
                response.status_code,
            )

        return (
            jsonify(
                {"response_text": "Unknown response format from prediction service"}
            ),
            500,
        )

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


@predict_bp.get("/history")
@jwt_required()
def histories():
    histories = History.get_histories_from_user_id(user_id=get_jwt_identity())

    history_data = [
        {
            "id": history.id,
            "disease_name": Disease.get_disease_name_from_id(
                disease_id=history.disease_id
            ),
            "image_link": history.images,
        }
        for history in histories
    ]

    return jsonify({"histories": history_data}), 200


@predict_bp.get("/history/<id>")
@jwt_required()
def history(id: str):
    history = History.get_history_from_id(id=id)

    if not history:
        return jsonify({"error": "History not found"}), 404

    disease = Disease.get_disease_from_id(id=history.disease_id)

    if not disease:
        return jsonify({"error": "Disease not found"}), 404

    product_list = Product.get_product_from_diseaseid(disease_id=disease.id)

    product_data = [
        {
            "product_name": product.product_name,
            "product_image": product.product_image,
            "product_link": product.product_link,
            "active_ingredient": product.active_ingredient,
        }
        for product in product_list
    ]

    return (
        jsonify(
            {
                "id": history.id,
                "disease_name": disease.disease_name,
                "confidence": f"{history.percentage}%",
                "description": disease.description,
                "solution": disease.solution,
                "product_list": product_data,
                "image_link": history.images,
            }
        ),
        200,
    )
